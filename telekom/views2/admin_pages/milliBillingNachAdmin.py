from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Sum, Max

from telekom.models import MilliBillingPay, PayHistory, KabelTvPayHistory, UserTable, KabelTvNew, SaveInfoAboutWhoAddAndNachPaysFromBilling, StaffAction, CheckMilliBillingPaysWithKassirs

from datetime import datetime

from django.db import transaction

import logging
logger = logging.getLogger(__name__)

ROLLBACK_PASSWORD = '543569145637383'


def milliBillingNachAdmin(request):
    context = {}

    if not request.user.is_superuser or not request.user.username == 'admin1':
        return redirect('HomePage')

    context['milliBillingNachAdmin'] = True
    context['admin_allow'] = True

    if request.method == 'POST' and 'rollback_nach_file_name' in request.POST:
        file_name = request.POST.get('rollback_nach_file_name')
        entered_password = request.POST.get('rollback_password', '')

        if entered_password != ROLLBACK_PASSWORD:
            messages.error(request, f'Неверный пароль отката. Начисление файла "{file_name}" не тронуто.')
        else:
            try:
                with transaction.atomic():
                    pay_rows = PayHistory.objects.filter(milli_billing_file_name=file_name)
                    kabel_rows = KabelTvPayHistory.objects.filter(milli_billing_file_name=file_name)

                    user_delta = {}  # {abonent_pk: [prochee, internet, alem]}
                    affected_check_keys = set()  # {(etrap, checked_date, checked_kassir)}
                    for p in pay_rows:
                        v = user_delta.setdefault(p.abonent_id, [0, 0, 0])
                        v[0] += p.prochee
                        v[1] += p.internet
                        v[2] += p.alem
                        if p.kassir_etrap and p.kassir:
                            affected_check_keys.add((p.kassir_etrap, p.date.strftime('%Y-%m-%d'), p.kassir))

                    kabel_delta = {}  # {kabel_pk: balance}
                    for k in kabel_rows:
                        kabel_delta[k.user_id] = kabel_delta.get(k.user_id, 0) + k.pay
                        if k.pay_kassir:
                            affected_check_keys.add(('Dashoguz', k.pay_date.strftime('%Y-%m-%d'), k.pay_kassir))

                    bulk_update_user = []
                    for pk, v in user_delta.items():
                        user = UserTable.objects.get(pk=pk)
                        user.b_prochee -= v[0]
                        user.b_internet -= v[1]
                        user.b_alem -= v[2]
                        bulk_update_user.append(user)
                    if bulk_update_user:
                        UserTable.objects.bulk_update(bulk_update_user, ['b_prochee', 'b_internet', 'b_alem'])

                    bulk_update_kabel = []
                    for pk, balance in kabel_delta.items():
                        user_k = KabelTvNew.objects.get(pk=pk)
                        user_k.balance -= balance
                        bulk_update_kabel.append(user_k)
                    if bulk_update_kabel:
                        KabelTvNew.objects.bulk_update(bulk_update_kabel, ['balance'])

                    deleted_pay_count = pay_rows.count()
                    deleted_kabel_count = kabel_rows.count()
                    pay_rows.delete()
                    kabel_rows.delete()

                    updated_nach_count = MilliBillingPay.objects.filter(file_name=file_name, is_nach=True).update(is_nach=False)

                    SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.filter(file_name=file_name).update(
                        etrap_nach='',
                        who_nach='',
                        when_nach=None,
                    )

                    # Откатываем и сверку (проверку/закрытие дня), т.к. данные, которые она подтверждала, удалены
                    deleted_check_count = 0
                    for etrap_, checked_date_, checked_kassir_ in affected_check_keys:
                        deleted_check_count += CheckMilliBillingPaysWithKassirs.objects.filter(
                            etrap=etrap_, checked_date=checked_date_, checked_kassir=checked_kassir_
                        ).delete()[0]

                    StaffAction.objects.create(user=request.user, comment=f'Откат начисления Milli Billing, файл {file_name}, откачено начислений {updated_nach_count} (PayHistory {deleted_pay_count}, KabelTvPayHistory {deleted_kabel_count}), откачено сверок {deleted_check_count}, дата отката {datetime.now()}, откатил {request.user.username}', action='Откат начисления Milli Billing')
                    messages.success(request, f'Начисление файла "{file_name}" откачено: {updated_nach_count} платежей (PayHistory {deleted_pay_count}, KabelTvPayHistory {deleted_kabel_count}), сверок отменено: {deleted_check_count}')
            except Exception as e:
                messages.error(request, f'ошибка с transaction при откате начисления, тип ошибки == {e}')
                logger.error(f'ошибка с transaction при откате начисления Milli Billing == {e}')

    files = MilliBillingPay.objects.filter(is_nach=True).values('file_name').annotate(
        count=Count('id'),
        total_price=Sum('price'),
        who_add_file=Max('who_add_file'),
        when_added_file=Max('when_added_file'),
    ).order_by('-when_added_file')

    context['files'] = files

    return render(request, 'telekom/admin_pages/milliBillingNachAdmin.html', context)
