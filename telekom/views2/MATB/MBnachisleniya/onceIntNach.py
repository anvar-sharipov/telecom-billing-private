from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction

from datetime import datetime
import re
import urllib.parse
import tablib

from telekom.models import UserTable, OldLoginDogowor, YhlasIyul2026InternetNach, StaffAction, etraps, SERVICE_TYPE_CHOICES

import logging

logger = logging.getLogger(__name__)


EXPECTED_HEADERS_BY_TYPE = {
    'internet': ['Пользователь', 'Договор', 'Учетное имя', 'Аренда', 'etrap'],
    'alem': ['Пользователь', 'Договор', 'Учетное имя', 'Списание за услугу', 'etrap'],
    'belet': ['Пользователь', 'Договор', 'Учетное имя', 'Списание за услугу', 'etrap'],
}

SERVICE_TYPE_LABELS = {
    'internet': 'Internet',
    'alem': 'Alem',
    'belet': 'Belet',
}

MONTH_CHOICES = [(f'{m:02d}', f'{m:02d}') for m in range(1, 13)]
_current_year = datetime.now().year
YEAR_CHOICES = [(str(y), str(y)) for y in range(_current_year - 1, _current_year + 3)]

# Код этрапа в contractCode/dogowor старого образца (lanbilling), используется для Alem IPTV-XXX кодов
ETRAP_CODES = {
    'Dashoguz': '322',
    'Akdepe': '344',
    'Boldumsaz': '346',
    'Gorogly': '340',
    'Koneurgench': '347',
    'Turkmenbashy': '349',
    'S.A.Nyyazow': '348',
    'Ruhubelent': '342',
    'Garashsyzlyk': '343',
    'Gubadag': '345',
}


def build_problem_rows_xlsx_response(rows):
    headers = ('Пользователь', 'Договор', 'Учетное имя', 'Сумма', 'etrap', 'Причина')
    data = tablib.Dataset(headers=headers)
    for row in rows:
        data.append((row['fio'], row['dogowor'], row['login'], row['arenda'], row['etrap'], row['reason']))

    filename = f"onceNachAdd_problem_rows_{datetime.now().strftime('%Y-%m-%d_%H%M')}.xlsx"
    encoded_filename = urllib.parse.quote(filename.encode('utf-8'))

    response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
    return response


def match_rows(dataset, etrap, service_type):
    """Сопоставляет строки dataset с абонентами по договору, проверяет что этрап в файле
    совпадает с выбранным. Логика сопоставления зависит от service_type.
    Возвращает (rows_to_create, problem_rows)."""

    if service_type == 'internet':
        rows_to_create, problem_rows = _match_internet(dataset, etrap)
    elif service_type == 'belet':
        rows_to_create, problem_rows = _match_belet(dataset, etrap)
    elif service_type == 'alem':
        rows_to_create, problem_rows = _match_alem(dataset, etrap)
    else:
        raise ValueError(f'Неизвестный service_type: {service_type}')

    for r in rows_to_create:
        r.service_type = service_type

    return rows_to_create, problem_rows


def _match_internet(dataset, etrap):
    dogowor_to_user = {}
    for u in UserTable.objects.filter(etrap=etrap).exclude(dogowor__isnull=True).exclude(dogowor=''):
        dogowor_to_user[u.dogowor.strip().upper()] = u

    dogowor_to_old = {}
    for o in OldLoginDogowor.objects.filter(etrap=etrap).exclude(dogowor=''):
        key = o.dogowor.strip().upper()
        if key not in dogowor_to_old:
            dogowor_to_old[key] = o

    rows_to_create = []
    problem_rows = []

    for row_num, d in enumerate(dataset, start=2):
        fio, dogowor_raw, login, arenda_raw, row_etrap = _read_row(d)

        if row_etrap != etrap:
            problem_rows.append(_problem(fio, dogowor_raw, login, arenda_raw, row_etrap, f'Этрап в файле ({row_etrap}) не совпадает с выбранным ({etrap}), строка {row_num}'))
            continue

        arenda, err = _parse_arenda(arenda_raw, row_num)
        if err:
            problem_rows.append(_problem(fio, dogowor_raw, login, arenda_raw, row_etrap, err))
            continue

        dogowor_key = dogowor_raw.upper()

        user = dogowor_to_user.get(dogowor_key)
        if user:
            number, is_enterprises = user.number, str(user.is_enterprises)
        else:
            old = dogowor_to_old.get(dogowor_key)
            if old:
                number, is_enterprises = old.number or '', str(old.is_enterprises)
            else:
                problem_rows.append(_problem(fio, dogowor_raw, login, arenda_raw, row_etrap, f'Договор не найден ни в UserTable, ни в OldLoginDogowor, строка {row_num}'))
                continue

        rows_to_create.append(_make_row(fio, dogowor_raw, login, arenda, row_etrap, number, is_enterprises))

    return rows_to_create, problem_rows


def _match_belet(dataset, etrap):
    dogowor_to_user = {}
    dogowor_belet_to_user = {}
    for u in UserTable.objects.filter(etrap=etrap):
        if u.dogowor:
            dogowor_to_user.setdefault(u.dogowor.strip().upper(), u)
        if u.dogowor_belet:
            dogowor_belet_to_user.setdefault(u.dogowor_belet.strip().upper(), u)

    dogowor_to_old = {}
    dogowor_belet_to_old = {}
    for o in OldLoginDogowor.objects.filter(etrap=etrap):
        if o.dogowor:
            dogowor_to_old.setdefault(o.dogowor.strip().upper(), o)
        if o.dogowor_belet:
            dogowor_belet_to_old.setdefault(o.dogowor_belet.strip().upper(), o)

    rows_to_create = []
    problem_rows = []

    for row_num, d in enumerate(dataset, start=2):
        fio, dogowor_raw, login, arenda_raw, row_etrap = _read_row(d)

        if row_etrap != etrap:
            problem_rows.append(_problem(fio, dogowor_raw, login, arenda_raw, row_etrap, f'Этрап в файле ({row_etrap}) не совпадает с выбранным ({etrap}), строка {row_num}'))
            continue

        arenda, err = _parse_arenda(arenda_raw, row_num)
        if err:
            problem_rows.append(_problem(fio, dogowor_raw, login, arenda_raw, row_etrap, err))
            continue

        dogowor_key = dogowor_raw.upper()

        found = dogowor_to_user.get(dogowor_key) or dogowor_belet_to_user.get(dogowor_key)
        if found:
            number, is_enterprises = found.number, str(found.is_enterprises)
        else:
            old = dogowor_to_old.get(dogowor_key) or dogowor_belet_to_old.get(dogowor_key)
            if old:
                number, is_enterprises = old.number or '', str(old.is_enterprises)
            else:
                problem_rows.append(_problem(fio, dogowor_raw, login, arenda_raw, row_etrap, f'Договор не найден ни в UserTable (dogowor/dogowor_belet), ни в OldLoginDogowor, строка {row_num}'))
                continue

        rows_to_create.append(_make_row(fio, dogowor_raw, login, arenda, row_etrap, number, is_enterprises))

    return rows_to_create, problem_rows


def _match_alem(dataset, etrap):
    code = ETRAP_CODES.get(etrap)

    user_by_number = {}
    dogowor_to_user = {}
    dogowor_alem_to_user = {}
    login_to_user = {}
    for u in UserTable.objects.filter(etrap=etrap):
        if u.number:
            user_by_number.setdefault(u.number, u)
        if u.dogowor:
            dogowor_to_user.setdefault(u.dogowor.strip().upper(), u)
        if u.dogowor_alem:
            dogowor_alem_to_user.setdefault(u.dogowor_alem.strip().upper(), u)
        if u.login:
            login_to_user.setdefault(u.login.strip().upper(), u)

    dogowor_to_old = {}
    dogowor_alem_to_old = {}
    login_to_old = {}
    for o in OldLoginDogowor.objects.filter(etrap=etrap):
        if o.dogowor:
            dogowor_to_old.setdefault(o.dogowor.strip().upper(), o)
        if o.dogowor_alem:
            dogowor_alem_to_old.setdefault(o.dogowor_alem.strip().upper(), o)
        if o.login:
            login_to_old.setdefault(o.login.strip().upper(), o)

    rows_to_create = []
    problem_rows = []

    for row_num, d in enumerate(dataset, start=2):
        fio, dogowor_raw, login, arenda_raw, row_etrap = _read_row(d)

        if row_etrap != etrap:
            problem_rows.append(_problem(fio, dogowor_raw, login, arenda_raw, row_etrap, f'Этрап в файле ({row_etrap}) не совпадает с выбранным ({etrap}), строка {row_num}'))
            continue

        arenda, err = _parse_arenda(arenda_raw, row_num)
        if err:
            problem_rows.append(_problem(fio, dogowor_raw, login, arenda_raw, row_etrap, err))
            continue

        dogowor_key = dogowor_raw.upper()
        login_key = login.upper()

        found = None  # UserTable или OldLoginDogowor

        # 1) IPTV-код: 993<код этрапа><номер абонента>
        digits = re.sub(r'\D', '', dogowor_raw)
        if len(digits) in (10, 11) and code:
            digits_code = digits[-8:-5]
            digits_number = digits[-5:]
            if digits_code == code:
                found = user_by_number.get(digits_number)

        # 2) Договор напрямую как dogowor_alem
        if not found:
            found = dogowor_alem_to_user.get(dogowor_key)
        if not found:
            found = dogowor_alem_to_old.get(dogowor_key)

        # 3) Учетное имя как dogowor / login абонента
        if not found:
            found = dogowor_to_user.get(login_key)
        if not found:
            found = login_to_user.get(login_key)
        if not found:
            found = dogowor_to_old.get(login_key)
        if not found:
            found = login_to_old.get(login_key)

        if found:
            number = found.number
            is_enterprises = str(found.is_enterprises)
        else:
            problem_rows.append(_problem(fio, dogowor_raw, login, arenda_raw, row_etrap, f'Абонент не найден (проверены IPTV-код, dogowor_alem, Учетное имя как dogowor/login, включая OldLoginDogowor), строка {row_num}'))
            continue

        rows_to_create.append(_make_row(fio, dogowor_raw, login, arenda, row_etrap, number, is_enterprises))

    return rows_to_create, problem_rows


def _read_row(d):
    fio = str(d[0]).strip() if d[0] is not None else ''
    dogowor_raw = str(d[1]).strip() if d[1] is not None else ''
    login = str(d[2]).strip() if d[2] is not None else ''
    arenda_raw = d[3]
    row_etrap = str(d[4]).strip() if d[4] is not None else ''
    return fio, dogowor_raw, login, arenda_raw, row_etrap


def _parse_arenda(arenda_raw, row_num):
    try:
        return float(str(arenda_raw).replace(',', '.')), None
    except (TypeError, ValueError):
        return None, f'Некорректная сумма, строка {row_num}'


def _problem(fio, dogowor, login, arenda, etrap, reason):
    return {'fio': fio, 'dogowor': dogowor, 'login': login, 'arenda': arenda, 'etrap': etrap, 'reason': reason}


def _make_row(fio, dogowor, login, arenda, etrap, number, is_enterprises):
    return YhlasIyul2026InternetNach(
        fio=fio,
        dogowor=dogowor,
        login=login,
        arenda=arenda,
        etrap=etrap,
        number=number,
        is_enterprises=is_enterprises,
    )


def onceIntNach(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентифицированы')
        return redirect('user-login')

    if not (request.user.is_superuser or request.user.username in ['Gayyp', 'yhlas_mtb']):
        messages.error(request, 'Доступ разрешен только администратору')
        return redirect('user-login')

    context['onceIntNach'] = True
    context['matbIndex'] = True
    context['etraps'] = etraps
    context['service_types'] = SERVICE_TYPE_CHOICES
    context['months'] = MONTH_CHOICES
    context['years'] = YEAR_CHOICES

    etrap = request.POST.get('etrap') or ''
    service_type = request.POST.get('service_type') or ''
    year = request.POST.get('year') or ''
    month = request.POST.get('month') or ''
    context['etrap'] = etrap
    context['service_type'] = service_type
    context['year'] = year
    context['month'] = month

    if request.method == 'POST':
        if not etrap:
            messages.error(request, 'Выберите этрап')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        if service_type not in EXPECTED_HEADERS_BY_TYPE:
            messages.error(request, 'Выберите услугу (Internet/Alem/Belet)')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        if not year or not month:
            messages.error(request, 'Выберите год и месяц начисления')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        if YhlasIyul2026InternetNach.objects.filter(etrap=etrap, service_type=service_type, year=year, month=month).exists():
            messages.error(request, f'Этрап "{etrap}" для услуги "{SERVICE_TYPE_LABELS[service_type]}" за {year}-{month} уже был добавлен ранее в YhlasIyul2026InternetNach. Повторное добавление запрещено.')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        try:
            uploaded_file = request.FILES['my_file']
        except Exception:
            messages.error(request, 'Выберите файл')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        if not str(uploaded_file).lower().endswith('.xlsx'):
            messages.error(request, 'Файл должен быть формата xlsx')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        filename_lower = str(uploaded_file).lower()
        service_label = SERVICE_TYPE_LABELS[service_type]
        name_checks = {
            f'услуга ({service_label})': service_label.lower(),
            f'этрап ({etrap})': etrap.lower(),
            f'год ({year})': year.lower(),
            f'месяц ({month})': month.lower(),
        }
        missing = [label for label, value in name_checks.items() if value not in filename_lower]
        if missing:
            messages.error(request, f'Имя файла "{uploaded_file}" должно содержать: {", ".join(name_checks.keys())}. Не найдено: {", ".join(missing)}')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        try:
            dataset = tablib.Dataset()
            dataset.load(uploaded_file.read(), format='xlsx')
        except Exception as e:
            messages.error(request, f'Ошибка чтения файла: {e}')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        expected_headers = EXPECTED_HEADERS_BY_TYPE[service_type]
        headers = [str(h).strip() if h is not None else '' for h in (dataset.headers or [])]
        if headers != expected_headers:
            messages.error(request, f'Неверные колонки в файле. Ожидались: {", ".join(expected_headers)}. Получено: {", ".join(headers)}')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        if len(dataset) == 0:
            messages.error(request, 'Файл пустой')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        file_etraps = sorted({(str(d[4]).strip() if d[4] is not None else '') for d in dataset} - {etrap})
        print("file_etraps", file_etraps)
        if file_etraps:
            messages.error(request, f'Этрап в файле не совпадает с выбранным этрапом "{etrap}". Найдены другие значения в колонке etrap: {", ".join(file_etraps)}')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        rows_to_create, problem_rows = match_rows(dataset, etrap, service_type)

        # Скачать список проблемных строк, ничего не сохраняя
        if request.POST.get('onceIntNachExportProblems'):
            if not problem_rows:
                messages.success(request, 'Проблемных строк нет')
                return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)
            return build_problem_rows_xlsx_response(problem_rows)

        totalCount = len(dataset)
        context['totalCount'] = totalCount
        context['matched_count'] = len(rows_to_create)
        context['problem_count'] = len(problem_rows)
        context['totalArenda'] = float('%.2f' % sum(r.arenda for r in rows_to_create))
        context['is_test_mode'] = bool(request.POST.get('onceIntNachTest'))

        if context['is_test_mode']:
            messages.success(request, 'Проверка прошла успешно (ничего не сохранено в БД)')
        elif problem_rows:
            messages.error(request, f'Добавление запрещено: {len(problem_rows)} проблемных строк из {totalCount}. Скачайте список проблемных строк, исправьте и загрузите файл заново.')
        else:
            for r in rows_to_create:
                r.who_add = request.user.username
                r.file_name = str(uploaded_file)
                r.year = year
                r.month = month
            try:
                with transaction.atomic():
                    if YhlasIyul2026InternetNach.objects.select_for_update().filter(etrap=etrap, service_type=service_type, year=year, month=month).exists():
                        messages.error(request, f'Этрап "{etrap}" для услуги "{SERVICE_TYPE_LABELS[service_type]}" за {year}-{month} уже был добавлен ранее в YhlasIyul2026InternetNach. Повторное добавление запрещено.')
                        return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)
                    YhlasIyul2026InternetNach.objects.bulk_create(rows_to_create)
                    StaffAction.objects.create(
                        user=request.user,
                        comment=f'Добавление в YhlasIyul2026InternetNach, услуга {service_type}, этрап {etrap}, период {year}-{month}, файл {str(uploaded_file)}, строк {len(rows_to_create)}, добавил {request.user.username}',
                        action='Импорт с xlsx Интернет Начисления в БД',
                    )
                messages.success(request, f'Успешно добавлено {len(rows_to_create)} записей в YhlasIyul2026InternetNach ({year}-{month})')
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении, тип ошибки == {e}')
                logger.error(f'Ошибка при сохранении YhlasIyul2026InternetNach, тип ошибки == {e}')

    return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)
