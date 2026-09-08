from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Count, Max, Q

from datetime import datetime
import urllib.parse
import tablib

from telekom.models import UserTable, OldLoginDogowor, OnceDogoworAdd, StaffAction, DOGOWOR_FIELD_BY_SERVICE

import logging

logger = logging.getLogger(__name__)

ALLOWED_USERNAMES = ['Gayyp', 'yhlas_mtb']

SERVICE_TYPE_LABELS = {'belet': 'Belet'}


def build_problem_rows_xlsx_response(rows):
    headers = ('Пользователь', 'Новый договор', 'etrap', 'Номер абонента', 'Найден в', 'Причина')
    data = tablib.Dataset(headers=headers)
    for row in rows:
        data.append((row['fio'], row['new_dogowor'], row['etrap'], row['number'], row['found_in'], row['reason']))

    filename = f"onceDogoworNach_problem_rows_{datetime.now().strftime('%Y-%m-%d_%H%M')}.xlsx"
    encoded_filename = urllib.parse.quote(filename.encode('utf-8'))

    response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
    return response


def build_applied_rows_xlsx_response(rows, etrap, service_type):
    headers = ('Услуга', 'Пользователь', 'Новый договор', 'Договор для поиска', 'Учетное имя', 'etrap', 'Номер абонента', 'Найден в', 'Кто применил', 'Когда применено')
    data = tablib.Dataset(headers=headers)
    for r in rows:
        data.append((r.service_type, r.fio, r.new_dogowor, r.search_dogowor, r.login, r.etrap, r.number, r.found_in, r.who_apply, r.applied_at.strftime('%d.%m.%Y %H:%M') if r.applied_at else ''))

    filename = f"OnceDogoworAdd_applied_{etrap}_{service_type}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.xlsx"
    encoded_filename = urllib.parse.quote(filename.encode('utf-8'))

    response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
    return response


def resolve_targets_and_problems(rows, etrap):
    """Заново находит цель (UserTable/OldLoginDogowor) по number+found_in для каждой строки
    и проверяет, что целевое поле либо пусто, либо уже равно new_dogowor.
    Возвращает (usertable_by_number, old_by_number, problem_rows, noop_ids)."""

    numbers_user = {r.number for r in rows if r.number and r.found_in == 'usertable'}
    numbers_old = {r.number for r in rows if r.number and r.found_in == 'old'}

    usertable_by_number = {u.number: u for u in UserTable.objects.filter(etrap=etrap, number__in=numbers_user)}
    old_by_number = {o.number: o for o in OldLoginDogowor.objects.filter(etrap=etrap, number__in=numbers_old)}

    problem_rows = []
    noop_ids = []

    for r in rows:
        target = None
        if r.found_in == 'usertable':
            target = usertable_by_number.get(r.number)
        elif r.found_in == 'old':
            target = old_by_number.get(r.number)

        if not target:
            problem_rows.append({'fio': r.fio, 'new_dogowor': r.new_dogowor, 'etrap': r.etrap, 'number': r.number, 'found_in': r.found_in, 'reason': 'Абонент не найден по number+etrap (изменился/удалён после add)'})
            continue

        field_name = DOGOWOR_FIELD_BY_SERVICE[r.service_type]
        current_value = (getattr(target, field_name) or '').strip()

        if current_value and current_value.upper() != r.new_dogowor.strip().upper():
            problem_rows.append({'fio': r.fio, 'new_dogowor': r.new_dogowor, 'etrap': r.etrap, 'number': r.number, 'found_in': r.found_in, 'reason': f'Поле {field_name} уже занято другим значением ("{current_value}"), нужна ручная проверка'})
            continue

        if current_value:
            noop_ids.append(r.id)

    return usertable_by_number, old_by_number, problem_rows, noop_ids


def get_groups_data():
    return OnceDogoworAdd.objects.values('etrap', 'service_type').annotate(
        count=Count('id'),
        applied_count=Count('id', filter=Q(is_applied=True)),
        who_add=Max('who_add'),
    ).order_by('etrap', 'service_type')


def onceDogoworNach(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентифицированы')
        return redirect('user-login')

    if not (request.user.is_superuser or request.user.username in ALLOWED_USERNAMES):
        messages.error(request, 'Доступ разрешен только администратору')
        return redirect('user-login')

    context['onceDogoworNach'] = True
    context['matbIndex'] = True
    context['groups_data'] = get_groups_data()

    if request.method == 'GET' and request.GET.get('download_applied_etrap'):
        etrap = request.GET.get('download_applied_etrap')
        service_type = request.GET.get('service_type', '')
        rows = OnceDogoworAdd.objects.filter(etrap=etrap, service_type=service_type, is_applied=True).order_by('id')
        return build_applied_rows_xlsx_response(rows, etrap, service_type)

    if request.method == 'POST':
        etrap = request.POST.get('etrap') or ''
        service_type = request.POST.get('service_type') or ''

        if not etrap or service_type not in SERVICE_TYPE_LABELS:
            messages.error(request, 'Не выбран этрап/услуга')
            return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworNach.html', context)

        rows_qs = OnceDogoworAdd.objects.filter(etrap=etrap, service_type=service_type, is_applied=False)
        if not rows_qs.exists():
            messages.error(request, f'Этрап "{etrap}" ({SERVICE_TYPE_LABELS[service_type]}) — нет неприменённых записей')
            return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworNach.html', context)

        who_add_values = sorted(set(rows_qs.exclude(who_add='').values_list('who_add', flat=True)))
        if not request.user.is_superuser and request.user.username not in who_add_values:
            messages.error(request, f'Применять может только тот пользователь, который делал добавление ({", ".join(who_add_values) or "неизвестно"})')
            return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworNach.html', context)

        rows = list(rows_qs)
        usertable_by_number, old_by_number, problem_rows, noop_ids = resolve_targets_and_problems(rows, etrap)

        if request.POST.get('onceDogoworNachExportProblems'):
            if not problem_rows:
                messages.success(request, 'Проблемных строк нет')
                return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworNach.html', context)
            return build_problem_rows_xlsx_response(problem_rows)

        totalCount = len(rows)
        context['applyEtrap'] = etrap
        context['applyServiceType'] = SERVICE_TYPE_LABELS[service_type]
        context['totalCount'] = totalCount
        context['problem_count'] = len(problem_rows)
        context['noop_count'] = len(noop_ids)
        context['is_test_mode'] = bool(request.POST.get('onceDogoworNachTest'))

        if context['is_test_mode']:
            messages.success(request, 'Проверка прошла успешно (ничего не применено)')
        elif problem_rows:
            messages.error(request, f'Применение запрещено: {len(problem_rows)} проблемных строк из {totalCount}. Скачайте список проблемных строк.')
        else:
            try:
                with transaction.atomic():
                    numbers_user = {r.number for r in rows if r.number and r.found_in == 'usertable'}
                    numbers_old = {r.number for r in rows if r.number and r.found_in == 'old'}
                    usertable_by_number = {u.number: u for u in UserTable.objects.select_for_update().filter(etrap=etrap, number__in=numbers_user)}
                    old_by_number = {o.number: o for o in OldLoginDogowor.objects.select_for_update().filter(etrap=etrap, number__in=numbers_old)}

                    field_name = DOGOWOR_FIELD_BY_SERVICE[service_type]
                    bulk_update_user = []
                    bulk_update_old = []
                    bulk_update_staging = []
                    now = datetime.now()

                    for r in rows:
                        target = usertable_by_number.get(r.number) if r.found_in == 'usertable' else old_by_number.get(r.number)
                        if not target:
                            raise ValueError(f'Абонент {r.number} ({r.found_in}) исчез во время применения')

                        current_value = getattr(target, field_name) or ''
                        r.previous_value = current_value

                        if not current_value:
                            setattr(target, field_name, r.new_dogowor)
                            if r.found_in == 'usertable':
                                bulk_update_user.append(target)
                            else:
                                bulk_update_old.append(target)

                        r.is_applied = True
                        r.who_apply = request.user.username
                        r.applied_at = now
                        bulk_update_staging.append(r)

                    if bulk_update_user:
                        UserTable.objects.bulk_update(bulk_update_user, [field_name])
                    if bulk_update_old:
                        OldLoginDogowor.objects.bulk_update(bulk_update_old, [field_name])
                    OnceDogoworAdd.objects.bulk_update(bulk_update_staging, ['previous_value', 'is_applied', 'who_apply', 'applied_at'])

                    StaffAction.objects.create(
                        user=request.user,
                        comment=f'Применение OnceDogoworAdd -> {field_name}, этрап {etrap}, услуга {service_type}, строк {totalCount}, применил {request.user.username}',
                        action='Импорт с xlsx Интернет Начисления в БД',
                    )
                messages.success(request, f'Успешно применено {totalCount} записей (этрап {etrap}, {SERVICE_TYPE_LABELS[service_type]})')
            except Exception as e:
                messages.error(request, f'Ошибка при применении, тип ошибки == {e}')
                logger.error(f'Ошибка при применении OnceDogoworAdd, тип ошибки == {e}')

        context['groups_data'] = get_groups_data()

    return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworNach.html', context)
