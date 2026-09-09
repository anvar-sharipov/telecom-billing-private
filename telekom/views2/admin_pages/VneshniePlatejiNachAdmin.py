from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Sum, Max
from django.db import transaction

from telekom.models import PlatejiWhichAddKassirsEveryDay, UserTable, PayHistory, SaveInfoAboutWhoAddAndNachPaysFromBilling, StaffAction

from datetime import datetime

import logging
logger = logging.getLogger(__name__)

ROLLBACK_PASSWORD = '543569145637383'
KASSA_MANAGERS = ['Capar', 'eGov', 'Saray', 'Toleg', 'Turkmenpost diller']


def VneshniePlatejiNachAdmin(request):
    context = {}

    if not request.user.is_superuser or not request.user.username == 'admin1':
        return redirect('HomePage')

    context['VneshniePlatejiNachAdmin'] = True
    context['admin_allow'] = True

    if request.method == 'POST' and 'rollback_nach_file_name' in request.POST:
        file_name = request.POST.get('rollback_nach_file_name')
        entered_password = request.POST.get('rollback_password', '')

        if entered_password != ROLLBACK_PASSWORD:
            messages.error(request, f'Неверный пароль отката. Начисление файла "{file_name}" не тронуто.')
        else:
            pay_rows = PayHistory.objects.filter(pays_from_billing_file_name=file_name)
            if not pay_rows.exists():
                messages.error(request, f'Для файла "{file_name}" не найдено начисленных платежей (PayHistory).')
            else:
                try:
                    with transaction.atomic():
                        pay_rows = list(PayHistory.objects.select_for_update().filter(pays_from_billing_file_name=file_name))

                        user_delta = {}  # abonent_id -> [prochee, internet, alem]
                        for ph in pay_rows:
                            v = user_delta.setdefault(ph.abonent_id, [0, 0, 0])
                            v[0] += ph.prochee
                            v[1] += ph.internet
                            v[2] += ph.alem

                        bulk_update_user = []
                        for pk, v in user_delta.items():
                            user = UserTable.objects.select_for_update().get(pk=pk)
                            user.b_prochee -= v[0]
                            user.b_internet -= v[1]
                            user.b_alem -= v[2]
                            bulk_update_user.append(user)
                        if bulk_update_user:
                            UserTable.objects.bulk_update(bulk_update_user, ['b_prochee', 'b_internet', 'b_alem'])

                        deleted_count = len(pay_rows)
                        PayHistory.objects.filter(pays_from_billing_file_name=file_name).delete()

                        PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=file_name, manager__in=KASSA_MANAGERS).update(file_is_nach=False)

                        try:
                            info_obj = SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.get(file_name=file_name)
                            info_obj.etrap_nach = ''
                            info_obj.who_nach = ''
                            info_obj.when_nach = None
                            info_obj.save()
                        except SaveInfoAboutWhoAddAndNachPaysFromBilling.DoesNotExist:
                            pass

                        StaffAction.objects.create(user=request.user, comment=f'Откат начисления внешних платежей (Milli Billing), файл {file_name}, откачено платежей {deleted_count}, абонентов {len(user_delta)}, дата отката {datetime.now()}, откатил {request.user.username}', action='Импорт с xlsx внешние платежи в БД')
                        messages.success(request, f'Начисление файла "{file_name}" откачено: {deleted_count} платежей, {len(user_delta)} абонентов.')
                except Exception as e:
                    messages.error(request, f'Ошибка при откате начисления, тип ошибки == {e}')
                    logger.error(f'Ошибка при откате начисления внешних платежей, тип ошибки == {e}')

    files_data = PlatejiWhichAddKassirsEveryDay.objects.filter(manager__in=KASSA_MANAGERS, file_is_nach=True).values('file_name').annotate(
        count=Count('id'),
        total_price=Sum('price'),
        who_add_file=Max('who_add_file'),
    ).order_by('file_name')

    context['files_data'] = files_data

    return render(request, 'telekom/admin_pages/VneshniePlatejiNachAdmin.html', context)
