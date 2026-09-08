from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from datetime import datetime
import urllib.parse
import tablib

from telekom.models import UserTable, OldLoginDogowor, OnceDogoworAdd, StaffAction, etraps, DOGOWOR_ADD_SERVICE_TYPES, DOGOWOR_FIELD_BY_SERVICE

import logging

logger = logging.getLogger(__name__)

ALLOWED_USERNAMES = ['Gayyp', 'yhlas_mtb']

EXPECTED_HEADERS_BY_TYPE = {
    'belet': ['Пользователь', 'Договор Belet', 'Договор Internet', 'Учетное имя', 'etrap'],
}

SERVICE_TYPE_LABELS = {'belet': 'Belet'}


def build_problem_rows_xlsx_response(rows):
    headers = ('Пользователь', 'Новый договор', 'Договор для поиска', 'Учетное имя', 'etrap', 'Причина')
    data = tablib.Dataset(headers=headers)
    for row in rows:
        data.append((row['fio'], row['new_dogowor'], row['search_dogowor'], row['login'], row['etrap'], row['reason']))

    filename = f"onceDogoworAdd_problem_rows_{datetime.now().strftime('%Y-%m-%d_%H%M')}.xlsx"
    encoded_filename = urllib.parse.quote(filename.encode('utf-8'))

    response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
    return response


def _problem(fio, new_dogowor, search_dogowor, login, etrap, reason):
    return {'fio': fio, 'new_dogowor': new_dogowor, 'search_dogowor': search_dogowor, 'login': login, 'etrap': etrap, 'reason': reason}


def _read_row(d):
    fio = str(d[0]).strip() if d[0] is not None else ''
    new_dogowor = str(d[1]).strip() if d[1] is not None else ''
    search_dogowor = str(d[2]).strip() if d[2] is not None else ''
    login = str(d[3]).strip() if d[3] is not None else ''
    row_etrap = str(d[4]).strip() if d[4] is not None else ''
    return fio, new_dogowor, search_dogowor, login, row_etrap


def match_rows(dataset, etrap, service_type):
    """Сопоставляет строки dataset с абонентами по колонке поиска (search_dogowor).
    Возвращает (rows_to_create, skipped_count, problem_rows)."""

    existing_values = set()
    dogowor_to_user = {}
    for u in UserTable.objects.filter(etrap=etrap):
        if u.dogowor:
            dogowor_to_user.setdefault(u.dogowor.strip().upper(), u)
        target_value = getattr(u, DOGOWOR_FIELD_BY_SERVICE[service_type], '')
        if target_value:
            existing_values.add(target_value.strip().upper())

    dogowor_to_old = {}
    for o in OldLoginDogowor.objects.filter(etrap=etrap):
        if o.dogowor:
            dogowor_to_old.setdefault(o.dogowor.strip().upper(), o)
        target_value = getattr(o, DOGOWOR_FIELD_BY_SERVICE[service_type], '')
        if target_value:
            existing_values.add(target_value.strip().upper())

    # уже застейджено (в т.ч. ещё не применено) — не даём задублировать
    for staged in OnceDogoworAdd.objects.filter(etrap=etrap, service_type=service_type).values_list('new_dogowor', flat=True):
        if staged:
            existing_values.add(staged.strip().upper())

    rows_to_create = []
    problem_rows = []
    skipped_count = 0

    for row_num, d in enumerate(dataset, start=2):
        fio, new_dogowor, search_dogowor, login, row_etrap = _read_row(d)

        if row_etrap != etrap:
            problem_rows.append(_problem(fio, new_dogowor, search_dogowor, login, row_etrap, f'Этрап в файле ({row_etrap}) не совпадает с выбранным ({etrap}), строка {row_num}'))
            continue

        if not new_dogowor:
            problem_rows.append(_problem(fio, new_dogowor, search_dogowor, login, row_etrap, f'Пустой новый договор, строка {row_num}'))
            continue

        if new_dogowor.upper() in existing_values:
            skipped_count += 1
            continue

        found = dogowor_to_user.get(search_dogowor.upper())
        if found:
            rows_to_create.append(OnceDogoworAdd(
                service_type=service_type, etrap=etrap, fio=fio, new_dogowor=new_dogowor,
                search_dogowor=search_dogowor, login=login, number=found.number, found_in='usertable',
            ))
            continue

        found_old = dogowor_to_old.get(search_dogowor.upper())
        if found_old:
            rows_to_create.append(OnceDogoworAdd(
                service_type=service_type, etrap=etrap, fio=fio, new_dogowor=new_dogowor,
                search_dogowor=search_dogowor, login=login, number=found_old.number or '', found_in='old',
            ))
            continue

        problem_rows.append(_problem(fio, new_dogowor, search_dogowor, login, row_etrap, f'Абонент не найден ни в UserTable, ни в OldLoginDogowor по договору "{search_dogowor}", строка {row_num}'))

    return rows_to_create, skipped_count, problem_rows


def onceDogoworAdd(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентифицированы')
        return redirect('user-login')

    if not (request.user.is_superuser or request.user.username in ALLOWED_USERNAMES):
        messages.error(request, 'Доступ разрешен только администратору')
        return redirect('user-login')

    context['onceDogoworAdd'] = True
    context['matbIndex'] = True
    context['etraps'] = etraps
    context['service_types'] = DOGOWOR_ADD_SERVICE_TYPES

    etrap = request.POST.get('etrap') or ''
    service_type = request.POST.get('service_type') or ''
    context['etrap'] = etrap
    context['service_type'] = service_type

    if request.method == 'POST':
        if not etrap:
            messages.error(request, 'Выберите этрап')
            return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworAdd.html', context)

        if service_type not in EXPECTED_HEADERS_BY_TYPE:
            messages.error(request, 'Выберите тип договора')
            return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworAdd.html', context)

        try:
            uploaded_file = request.FILES['my_file']
        except Exception:
            messages.error(request, 'Выберите файл')
            return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworAdd.html', context)

        if not str(uploaded_file).lower().endswith('.xlsx'):
            messages.error(request, 'Файл должен быть формата xlsx')
            return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworAdd.html', context)

        filename_lower = str(uploaded_file).lower()
        service_label = SERVICE_TYPE_LABELS[service_type]
        name_checks = {
            f'тип договора ({service_label})': service_label.lower(),
            f'этрап ({etrap})': etrap.lower(),
        }
        missing = [label for label, value in name_checks.items() if value not in filename_lower]
        if missing:
            messages.error(request, f'Имя файла "{uploaded_file}" должно содержать: {", ".join(name_checks.keys())}. Не найдено: {", ".join(missing)}')
            return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworAdd.html', context)

        try:
            dataset = tablib.Dataset()
            dataset.load(uploaded_file.read(), format='xlsx')
        except Exception as e:
            messages.error(request, f'Ошибка чтения файла: {e}')
            return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworAdd.html', context)

        expected_headers = EXPECTED_HEADERS_BY_TYPE[service_type]
        headers = [str(h).strip() if h is not None else '' for h in (dataset.headers or [])]
        if headers != expected_headers:
            messages.error(request, f'Неверные колонки в файле. Ожидались: {", ".join(expected_headers)}. Получено: {", ".join(headers)}')
            return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworAdd.html', context)

        if len(dataset) == 0:
            messages.error(request, 'Файл пустой')
            return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworAdd.html', context)

        rows_to_create, skipped_count, problem_rows = match_rows(dataset, etrap, service_type)

        if request.POST.get('onceDogoworAddExportProblems'):
            if not problem_rows:
                messages.success(request, 'Проблемных строк нет')
                return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworAdd.html', context)
            return build_problem_rows_xlsx_response(problem_rows)

        totalCount = len(dataset)
        context['totalCount'] = totalCount
        context['matched_count'] = len(rows_to_create)
        context['skipped_count'] = skipped_count
        context['problem_count'] = len(problem_rows)
        context['is_test_mode'] = bool(request.POST.get('onceDogoworAddTest'))

        if context['is_test_mode']:
            messages.success(request, 'Проверка прошла успешно (ничего не сохранено в БД)')
        elif problem_rows:
            messages.error(request, f'Добавление запрещено: {len(problem_rows)} проблемных строк из {totalCount}. Скачайте список проблемных строк, исправьте и загрузите файл заново.')
        else:
            for r in rows_to_create:
                r.who_add = request.user.username
                r.file_name = str(uploaded_file)
            try:
                if rows_to_create:
                    OnceDogoworAdd.objects.bulk_create(rows_to_create)
                StaffAction.objects.create(
                    user=request.user,
                    comment=f'Добавление в OnceDogoworAdd, услуга {service_type}, этрап {etrap}, файл {str(uploaded_file)}, создано {len(rows_to_create)}, пропущено (уже есть) {skipped_count}, добавил {request.user.username}',
                    action='Импорт с xlsx Интернет Начисления в БД',
                )
                messages.success(request, f'Успешно добавлено {len(rows_to_create)} записей в OnceDogoworAdd (этрап {etrap}, {SERVICE_TYPE_LABELS[service_type]}), пропущено (уже есть в БД) {skipped_count}')
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении, тип ошибки == {e}')
                logger.error(f'Ошибка при сохранении OnceDogoworAdd, тип ошибки == {e}')

    return render(request, 'telekom/MATB/MBnachisleniya/onceDogoworAdd.html', context)
