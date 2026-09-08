from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Max
from django.db import transaction

from telekom.models import OnceDogoworAdd, UserTable, OldLoginDogowor, StaffAction, DOGOWOR_FIELD_BY_SERVICE

from datetime import datetime

import logging
logger = logging.getLogger(__name__)

ROLLBACK_PASSWORD = '543569145637383'


def MBonceDogoworNachAdmin(request):
    context = {}

    if not request.user.is_superuser or not request.user.username == 'admin1':
        return redirect('HomePage')

    context['MBonceDogoworNachAdmin'] = True
    context['admin_allow'] = True

    if request.method == 'POST' and 'rollback_nach_etrap' in request.POST:
        etrap = request.POST.get('rollback_nach_etrap')
        service_type = request.POST.get('rollback_nach_service_type', '')
        entered_password = request.POST.get('rollback_password', '')

        field_name = DOGOWOR_FIELD_BY_SERVICE.get(service_type)

        if entered_password != ROLLBACK_PASSWORD:
            messages.error(request, f'Неверный пароль отката. Применение этрапа "{etrap}" ({service_type}) не тронуто.')
        elif not field_name:
            messages.error(request, f'Неизвестный тип договора "{service_type}".')
        else:
            rows = list(OnceDogoworAdd.objects.filter(etrap=etrap, service_type=service_type, is_applied=True))
            if not rows:
                messages.error(request, f'Для этрапа "{etrap}" ({service_type}) нет применённых строк.')
            else:
                try:
                    with transaction.atomic():
                        numbers_user = {r.number for r in rows if r.number and r.found_in == 'usertable'}
                        numbers_old = {r.number for r in rows if r.number and r.found_in == 'old'}
                        usertable_by_number = {u.number: u for u in UserTable.objects.select_for_update().filter(etrap=etrap, number__in=numbers_user)}
                        old_by_number = {o.number: o for o in OldLoginDogowor.objects.select_for_update().filter(etrap=etrap, number__in=numbers_old)}

                        mismatched = []
                        missing = []
                        for r in rows:
                            target = usertable_by_number.get(r.number) if r.found_in == 'usertable' else old_by_number.get(r.number)
                            if not target:
                                missing.append(r.number)
                                continue
                            current_value = (getattr(target, field_name) or '').strip()
                            if current_value.upper() != r.new_dogowor.strip().upper():
                                mismatched.append(r.number)

                        if missing:
                            messages.error(request, f'Откат прерван: {len(missing)} абонентов не найдены (номера: {", ".join(missing[:10])}...). Ничего не изменено.')
                        elif mismatched:
                            messages.error(request, f'Откат прерван: у {len(mismatched)} абонентов поле {field_name} изменилось после применения (номера: {", ".join(mismatched[:10])}...). Ничего не изменено.')
                        else:
                            bulk_update_user = []
                            bulk_update_old = []
                            bulk_update_staging = []

                            for r in rows:
                                target = usertable_by_number.get(r.number) if r.found_in == 'usertable' else old_by_number.get(r.number)
                                setattr(target, field_name, r.previous_value)
                                if r.found_in == 'usertable':
                                    bulk_update_user.append(target)
                                else:
                                    bulk_update_old.append(target)

                                r.is_applied = False
                                r.who_apply = ''
                                r.applied_at = None
                                r.previous_value = ''
                                bulk_update_staging.append(r)

                            if bulk_update_user:
                                UserTable.objects.bulk_update(bulk_update_user, [field_name])
                            if bulk_update_old:
                                OldLoginDogowor.objects.bulk_update(bulk_update_old, [field_name])
                            OnceDogoworAdd.objects.bulk_update(bulk_update_staging, ['is_applied', 'who_apply', 'applied_at', 'previous_value'])

                            StaffAction.objects.create(user=request.user, comment=f'Откат применения OnceDogoworAdd -> {field_name}, этрап {etrap}, услуга {service_type}, строк {len(rows)}, откатил {request.user.username}', action='Импорт с xlsx Интернет Начисления в БД')
                            messages.success(request, f'Применение этрапа "{etrap}" ({service_type}) откачено: {len(rows)} строк.')
                except Exception as e:
                    messages.error(request, f'Ошибка при откате применения, тип ошибки == {e}')
                    logger.error(f'Ошибка при откате применения OnceDogoworAdd, тип ошибки == {e}')

    groups_data = OnceDogoworAdd.objects.filter(is_applied=True).values('etrap', 'service_type').annotate(
        count=Count('id'),
        who_apply=Max('who_apply'),
        applied_at=Max('applied_at'),
    ).order_by('etrap', 'service_type')

    context['groups_data'] = groups_data

    return render(request, 'telekom/admin_pages/MBonceDogoworNachAdmin.html', context)
