from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Sum, Max
from django.db import transaction

from telekom.models import YhlasIyul2026InternetNach, UserTable, NachMinus, StaffAction

from datetime import datetime

import logging
logger = logging.getLogger(__name__)

ROLLBACK_PASSWORD = '543569145637383'
NACH_YEAR = '2026'
NACH_MONTH = '07'


def MBonceIntNachAdmin(request):
    context = {}

    if not request.user.is_superuser or not request.user.username == 'admin1':
        return redirect('HomePage')

    context['MBonceIntNachAdmin'] = True
    context['admin_allow'] = True

    if request.method == 'POST' and 'rollback_nach_etrap' in request.POST:
        etrap = request.POST.get('rollback_nach_etrap')
        entered_password = request.POST.get('rollback_password', '')

        if entered_password != ROLLBACK_PASSWORD:
            messages.error(request, f'Неверный пароль отката. Начисление этрапа "{etrap}" не тронуто.')
        else:
            rows = list(YhlasIyul2026InternetNach.objects.filter(etrap=etrap, is_nach=True))
            if not rows:
                messages.error(request, f'Для этрапа "{etrap}" нет начисленных строк.')
            else:
                try:
                    with transaction.atomic():
                        numbers = {r.number for r in rows if r.number}
                        users_by_number = {u.number: u for u in UserTable.objects.select_for_update().filter(etrap=etrap, number__in=numbers)}

                        user_charge_total = {}  # user.pk -> сумма
                        users_by_pk = {}
                        missing_users = []
                        for r in rows:
                            user = users_by_number.get(r.number)
                            if not user:
                                missing_users.append(r.number)
                                continue
                            users_by_pk[user.pk] = user
                            user_charge_total[user.pk] = user_charge_total.get(user.pk, 0) + r.arenda

                        if missing_users:
                            messages.error(request, f'Откат прерван: {len(missing_users)} абонентов не найдены в UserTable (номера: {", ".join(missing_users[:10])}...). Ничего не изменено.')
                        else:
                            nach_rows = {nm.user_id: nm for nm in NachMinus.objects.select_for_update().filter(user_id__in=user_charge_total.keys(), year=NACH_YEAR, month=NACH_MONTH)}

                            missing_nach = [pk for pk in user_charge_total if pk not in nach_rows]
                            if missing_nach:
                                messages.error(request, f'Откат прерван: для {len(missing_nach)} абонентов нет записи NachMinus за {NACH_YEAR}-{NACH_MONTH}. Ничего не изменено.')
                            else:
                                bulk_update_user = []
                                bulk_update_nach = []

                                for user_pk, total_amount in user_charge_total.items():
                                    user = users_by_pk[user_pk]
                                    user.b_internet += total_amount
                                    bulk_update_user.append(user)

                                    nm = nach_rows[user_pk]
                                    nm.internet -= total_amount
                                    bulk_update_nach.append(nm)

                                UserTable.objects.bulk_update(bulk_update_user, ['b_internet'])
                                NachMinus.objects.bulk_update(bulk_update_nach, ['internet'])

                                YhlasIyul2026InternetNach.objects.filter(etrap=etrap).update(is_nach=False, who_nach='', nach_at=None)

                                StaffAction.objects.create(user=request.user, comment=f'Откат начисления YhlasIyul2026InternetNach -> NachMinus, этрап {etrap}, {NACH_YEAR}-{NACH_MONTH}, строк {len(rows)}, абонентов {len(user_charge_total)}, откатил {request.user.username}', action='Импорт с xlsx Интернет Начисления в БД')
                                messages.success(request, f'Начисление этрапа "{etrap}" откачено: {len(rows)} строк, {len(user_charge_total)} абонентов.')
                except Exception as e:
                    messages.error(request, f'Ошибка при откате начисления, тип ошибки == {e}')
                    logger.error(f'Ошибка при откате начисления YhlasIyul2026InternetNach -> NachMinus, тип ошибки == {e}')

    etraps_data = YhlasIyul2026InternetNach.objects.filter(is_nach=True).values('etrap').annotate(
        count=Count('id'),
        total_arenda=Sum('arenda'),
        who_nach=Max('who_nach'),
        nach_at=Max('nach_at'),
    ).order_by('etrap')

    context['etraps_data'] = etraps_data

    return render(request, 'telekom/admin_pages/MBonceIntNachAdmin.html', context)
