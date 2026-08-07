from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction

from datetime import datetime
import urllib.parse
import tablib

from telekom.models import UserTable, OldLoginDogowor, YhlasIyul2026InternetNach, StaffAction, etraps

import logging

logger = logging.getLogger(__name__)


EXPECTED_HEADERS = ['Пользователь', 'Договор', 'Учетное имя', 'Аренда', 'etrap']


def build_problem_rows_xlsx_response(rows):
    headers = ('Пользователь', 'Договор', 'Учетное имя', 'Аренда', 'etrap', 'Причина')
    data = tablib.Dataset(headers=headers)
    for row in rows:
        data.append((row['fio'], row['dogowor'], row['login'], row['arenda'], row['etrap'], row['reason']))

    filename = f"onceIntNach_problem_rows_{datetime.now().strftime('%Y-%m-%d_%H%M')}.xlsx"
    encoded_filename = urllib.parse.quote(filename.encode('utf-8'))

    response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
    return response


def match_rows(dataset, etrap):
    """Сопоставляет строки dataset с абонентами по договору (UserTable -> OldLoginDogowor),
    проверяет что этрап в файле совпадает с выбранным.
    Возвращает (rows_to_create, problem_rows)."""

    dogowor_to_user = {}
    for u in UserTable.objects.exclude(dogowor__isnull=True).exclude(dogowor=''):
        dogowor_to_user[u.dogowor.strip().upper()] = u

    dogowor_to_old = {}
    for o in OldLoginDogowor.objects.exclude(dogowor=''):
        key = o.dogowor.strip().upper()
        if key not in dogowor_to_old:
            dogowor_to_old[key] = o

    rows_to_create = []
    problem_rows = []

    for row_num, d in enumerate(dataset, start=2):
        fio = str(d[0]).strip() if d[0] is not None else ''
        dogowor_raw = str(d[1]).strip() if d[1] is not None else ''
        login = str(d[2]).strip() if d[2] is not None else ''
        arenda_raw = d[3]
        row_etrap = str(d[4]).strip() if d[4] is not None else ''

        if row_etrap != etrap:
            problem_rows.append({'fio': fio, 'dogowor': dogowor_raw, 'login': login, 'arenda': arenda_raw, 'etrap': row_etrap, 'reason': f'Этрап в файле ({row_etrap}) не совпадает с выбранным ({etrap}), строка {row_num}'})
            continue

        try:
            arenda = float(str(arenda_raw).replace(',', '.'))
        except (TypeError, ValueError):
            problem_rows.append({'fio': fio, 'dogowor': dogowor_raw, 'login': login, 'arenda': arenda_raw, 'etrap': row_etrap, 'reason': f'Некорректная сумма, строка {row_num}'})
            continue

        dogowor_key = dogowor_raw.upper()

        user = dogowor_to_user.get(dogowor_key)
        if user:
            number = user.number
            is_enterprises = str(user.is_enterprises)
        else:
            old = dogowor_to_old.get(dogowor_key)
            if old:
                number = old.number or ''
                is_enterprises = str(old.is_enterprises)
            else:
                problem_rows.append({'fio': fio, 'dogowor': dogowor_raw, 'login': login, 'arenda': arenda_raw, 'etrap': row_etrap, 'reason': f'Договор не найден ни в UserTable, ни в OldLoginDogowor, строка {row_num}'})
                continue

        rows_to_create.append(YhlasIyul2026InternetNach(
            fio=fio,
            dogowor=dogowor_raw,
            login=login,
            arenda=arenda,
            etrap=row_etrap,
            number=number,
            is_enterprises=is_enterprises,
        ))

    return rows_to_create, problem_rows


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

    etrap = request.POST.get('etrap') or ''
    context['etrap'] = etrap

    if request.method == 'POST':
        if not etrap:
            messages.error(request, 'Выберите этрап')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        if YhlasIyul2026InternetNach.objects.filter(etrap=etrap).exists():
            messages.error(request, f'Этрап "{etrap}" уже был добавлен ранее в YhlasIyul2026InternetNach. Повторное добавление запрещено.')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        try:
            uploaded_file = request.FILES['my_file']
        except Exception:
            messages.error(request, 'Выберите файл')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        if not str(uploaded_file).lower().endswith('.xlsx'):
            messages.error(request, 'Файл должен быть формата xlsx')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        try:
            dataset = tablib.Dataset()
            dataset.load(uploaded_file.read(), format='xlsx')
        except Exception as e:
            messages.error(request, f'Ошибка чтения файла: {e}')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        headers = [str(h).strip() if h is not None else '' for h in (dataset.headers or [])]
        if headers != EXPECTED_HEADERS:
            messages.error(request, f'Неверные колонки в файле. Ожидались: {", ".join(EXPECTED_HEADERS)}. Получено: {", ".join(headers)}')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        if len(dataset) == 0:
            messages.error(request, 'Файл пустой')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        file_etraps = sorted({(str(d[4]).strip() if d[4] is not None else '') for d in dataset} - {etrap})
        if file_etraps:
            messages.error(request, f'Этрап в файле не совпадает с выбранным этрапом "{etrap}". Найдены другие значения в колонке etrap: {", ".join(file_etraps)}')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)

        rows_to_create, problem_rows = match_rows(dataset, etrap)

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
            try:
                with transaction.atomic():
                    if YhlasIyul2026InternetNach.objects.select_for_update().filter(etrap=etrap).exists():
                        messages.error(request, f'Этрап "{etrap}" уже был добавлен ранее в YhlasIyul2026InternetNach. Повторное добавление запрещено.')
                        return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)
                    YhlasIyul2026InternetNach.objects.bulk_create(rows_to_create)
                    StaffAction.objects.create(
                        user=request.user,
                        comment=f'Добавление в YhlasIyul2026InternetNach, этрап {etrap}, файл {str(uploaded_file)}, строк {len(rows_to_create)}, добавил {request.user.username}',
                        action='Импорт с xlsx Интернет Начисления в БД',
                    )
                messages.success(request, f'Успешно добавлено {len(rows_to_create)} записей в YhlasIyul2026InternetNach')
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении, тип ошибки == {e}')
                logger.error(f'Ошибка при сохранении YhlasIyul2026InternetNach, тип ошибки == {e}')

    return render(request, 'telekom/MATB/MBnachisleniya/onceIntNach.html', context)
