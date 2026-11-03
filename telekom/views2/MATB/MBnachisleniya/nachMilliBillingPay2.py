"""
Внешние платежи Milli Billing — НОВЫЙ формат файла "Online toleg" (с октября 2026).

Отличия от старого формата (см. vneshniePlatejiAdd.py):
  - появилась колонка 7 "Töleg Ýe Ýet  Senesi" (дата подтверждения платежа) — не используем,
    дата платежа как и раньше берётся из колонки 5 "Töleg Senesi";
  - "Şertnama Belgisi" (договор) переехал из колонки 10 в колонку 13;
  - "Möçberi" (сумма) переехал из колонки 23 в колонку 24;
  - появилась колонка 21 "Beýany" (описание) — пока всегда пустая, не используем;
  - внутри каждой KASSA-группы появилась подгруппа "TÖLEG GÖRNÜŞI" (Bank Karty и т.п.);
  - маркер строки платежа теперь " Online" (с пробелом в начале).

Логика сопоставления абонентов, проверки дублей и запись в PlatejiWhichAddKassirsEveryDay —
те же самые, что в vneshniePlatejiAdd (общие функции импортируются оттуда), поэтому
начисление делается так же, через nach_pays_from_billing.

Дополнительно: суммы платежей сверяются с итогами "JEMI" по каждой KASSA и с общим "SUM"
из самого файла — если не сходится (сдвинулись колонки / файл обрезан), ничего не сохраняется.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction

from datetime import datetime
import io
import openpyxl

from telekom.models import PlatejiWhichAddKassirsEveryDay, SaveInfoAboutWhoAddAndNachPaysFromBilling, StaffAction
from telekom.views2.MATB.MBnachisleniya.vneshniePlatejiAdd import (
    KASSA_MANAGERS,
    TARIFF_TO_TYPE,
    months_ru,
    build_problem_rows_xlsx_response,
    build_lookup_dicts,
    resolve_subscriber,
)

import logging

logger = logging.getLogger(__name__)

TEMPLATE = 'telekom/MATB/MBnachisleniya/nachMilliBillingPay2.html'

# Пишется в SaveInfoAboutWhoAddAndNachPaysFromBilling.etrap_add — по ней VneshniePlatejiAddAdmin2
# отличает файлы, добавленные через эту страницу, от файлов старой vneshniePlatejiAdd.
ETRAP_ADD_V2 = 'Внешние платежи v2'

COL_MARKER = 0
COL_TARIFF = 4
COL_DATE = 5
COL_PAY_ID = 8
COL_DOGOWOR = 13
COL_FIO = 15
COL_AMOUNT = 24

EXPECTED_HEADER_CELLS = {
    COL_MARKER: 'Operator',
    COL_TARIFF: 'Nyrhnama Topary',
    COL_DATE: 'Töleg Senesi',
    COL_PAY_ID: 'Töleg Belgisi',
    COL_DOGOWOR: 'Şertnama Belgisi',
    COL_FIO: 'Müşderiniň Doly Ady',
    COL_AMOUNT: 'Möçberi',
}

ROW_WIDTH = 26


def _cell(r, idx):
    return r[idx] if idx < len(r) else None


def _str(v):
    return str(v).strip() if v is not None else ''


def _find_total(r):
    """Итоговые строки: [..., 'Kassa Capar', ..., 'JEMI', ..., 1403672.66] или [..., 'SUM', ..., 9177536.3].
    Возвращает (label, value) или None. Значение — последняя числовая ячейка в строке."""
    texts = [_str(v) for v in r if isinstance(v, str)]
    nums = [v for v in r if isinstance(v, (int, float)) and not isinstance(v, bool)]
    if not nums:
        return None
    if 'JEMI' in texts:
        labels = [t for t in texts if t != 'JEMI']
        return (labels[0] if labels else ''), float(nums[-1])
    if 'SUM' in texts:
        return 'SUM', float(nums[-1])
    return None


def parse_workbook(uploaded_file):
    """Возвращает (rows, error). rows — тот же контракт, что parse_workbook в vneshniePlatejiAdd."""
    wb = openpyxl.load_workbook(io.BytesIO(uploaded_file.read()), data_only=True, read_only=True)
    try:
        ws = wb.worksheets[0]
        all_rows = [tuple(r) + (None,) * (ROW_WIDTH - len(r)) for r in ws.iter_rows(values_only=True)]
    finally:
        wb.close()

    header_row = None
    for r in all_rows[:15]:
        if _str(_cell(r, COL_MARKER)) == 'Operator':
            header_row = r
            break

    if header_row is None:
        return None, 'Не найдена строка заголовков ("Operator") в первых 15 строках файла — формат файла не распознан.'

    for idx, expected in EXPECTED_HEADER_CELLS.items():
        actual = _str(_cell(header_row, idx))
        if actual != expected:
            return None, f'Формат файла изменился: в колонке {idx} ожидалось "{expected}", получено "{actual}".'

    rows = []
    current_manager = None
    current_pay_kind = None
    kassa_sums = {}
    kassa_totals_in_file = {}
    grand_total_in_file = None

    for r in all_rows:
        marker = _str(_cell(r, COL_MARKER))
        if marker == 'KASSA':
            current_manager = _str(_cell(r, 1))
            current_pay_kind = None
            continue
        if marker == 'TÖLEG GÖRNÜŞI':
            current_pay_kind = next((_str(v) for v in r[1:] if v is not None), '')
            continue
        if marker == 'Online':
            amount = _cell(r, COL_AMOUNT)
            rows.append({
                'manager': current_manager,
                'pay_kind': current_pay_kind,
                'tariff': _cell(r, COL_TARIFF),
                'date': _cell(r, COL_DATE),
                'pay_id': _cell(r, COL_PAY_ID),
                'dogowor': _str(_cell(r, COL_DOGOWOR)),
                'fio': _str(_cell(r, COL_FIO)),
                'amount': amount,
            })
            if isinstance(amount, (int, float)):
                kassa_sums[current_manager] = kassa_sums.get(current_manager, 0) + float(amount)
            continue

        total = _find_total(r)
        if total:
            label, value = total
            if label == 'SUM':
                grand_total_in_file = value
            elif label.startswith('Kassa '):
                kassa_totals_in_file[label[len('Kassa '):].strip()] = value

    # Сверка с итогами самого файла
    if grand_total_in_file is None:
        return None, 'В файле не найдена итоговая строка "SUM" — файл неполный или формат изменился.'

    parsed_total = sum(kassa_sums.values())
    if round(parsed_total, 2) != round(grand_total_in_file, 2):
        return None, f'Сумма прочитанных платежей ({parsed_total:.2f}) не совпадает с итогом "SUM" в файле ({grand_total_in_file:.2f}) — формат файла изменился, ничего не сохранено.'

    for manager, file_total in kassa_totals_in_file.items():
        if round(kassa_sums.get(manager, 0), 2) != round(file_total, 2):
            return None, f'KASSA "{manager}": сумма прочитанных платежей ({kassa_sums.get(manager, 0):.2f}) не совпадает с итогом "JEMI" в файле ({file_total:.2f}).'

    return rows, None


def nachMilliBillingPay2(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентифицированы')
        return redirect('user-login')

    if not (request.user.is_superuser or request.user.username in ['Gayyp', 'yhlas_mtb']):
        messages.error(request, 'Доступ разрешен только администратору')
        return redirect('user-login')

    context['nachMilliBillingPay2'] = True
    context['matbIndex'] = True
    context['months'] = months_ru
    context['years'] = ['2025', '2026', '2027', '2028']

    year = request.POST.get('year') or ''
    month = request.POST.get('month') or ''
    context['year'] = year
    context['month'] = month

    if request.method == 'POST':
        if not year or not month or month not in months_ru:
            messages.error(request, 'Выберите год и месяц')
            return render(request, TEMPLATE, context)

        month_num = months_ru.index(month) + 1

        try:
            uploaded_file = request.FILES['my_file']
        except Exception:
            messages.error(request, 'Выберите файл')
            return render(request, TEMPLATE, context)

        if not str(uploaded_file).lower().endswith('.xlsx'):
            messages.error(request, 'Файл должен быть формата xlsx')
            return render(request, TEMPLATE, context)

        if PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=str(uploaded_file)).exists():
            messages.error(request, f'Файл "{str(uploaded_file)}" уже был добавлен ранее.')
            return render(request, TEMPLATE, context)

        try:
            parsed_rows, header_error = parse_workbook(uploaded_file)
        except Exception as e:
            messages.error(request, f'Ошибка чтения файла: {e}')
            return render(request, TEMPLATE, context)

        if header_error:
            messages.error(request, header_error)
            return render(request, TEMPLATE, context)

        if not parsed_rows:
            messages.error(request, 'В файле не найдено ни одной строки платежей')
            return render(request, TEMPLATE, context)

        # Защита от дурака: даты платежей должны быть датами и попадать в выбранный год/месяц
        not_dates = [r for r in parsed_rows if not isinstance(r['date'], datetime)]
        if not_dates:
            messages.error(request, f'В файле {len(not_dates)} строк с пустой/некорректной датой платежа (например № платежа {not_dates[0]["pay_id"]}).')
            return render(request, TEMPLATE, context)

        bad_dates = sorted({r['date'].strftime('%d.%m.%Y') for r in parsed_rows if r['date'].year != int(year) or r['date'].month != month_num})
        if bad_dates:
            messages.error(request, f'В файле есть платежи с датой вне выбранного периода {month} {year}: {", ".join(bad_dates[:10])}{"..." if len(bad_dates) > 10 else ""}')
            return render(request, TEMPLATE, context)

        lookups = build_lookup_dicts()

        existing_pay_ids = set(
            PlatejiWhichAddKassirsEveryDay.objects.filter(manager__in=KASSA_MANAGERS).exclude(kodOplaty='').exclude(kodOplaty__isnull=True).values_list('kodOplaty', flat=True)
        )
        seen_pay_ids_in_file = set()

        rows_to_create = []
        problem_rows = []

        for r in parsed_rows:
            pay_id_str = str(r['pay_id']).strip() if r['pay_id'] is not None else ''

            if not r['manager'] or r['manager'] not in KASSA_MANAGERS:
                problem_rows.append({**r, 'reason': f'Неизвестная KASSA-группа "{r["manager"]}" (не входит в список {KASSA_MANAGERS})'})
                continue

            if r['tariff'] not in TARIFF_TO_TYPE:
                problem_rows.append({**r, 'reason': f'Неизвестный тип услуги "{r["tariff"]}"'})
                continue

            if not pay_id_str:
                problem_rows.append({**r, 'reason': 'Пустой № платежа (Töleg Belgisi)'})
                continue

            if pay_id_str in existing_pay_ids:
                problem_rows.append({**r, 'reason': f'Платёж № {pay_id_str} уже был добавлен ранее (дубликат)'})
                continue

            if pay_id_str in seen_pay_ids_in_file:
                problem_rows.append({**r, 'reason': f'Платёж № {pay_id_str} повторяется несколько раз в этом же файле'})
                continue
            seen_pay_ids_in_file.add(pay_id_str)

            try:
                # в файле суммы вида 199.99999999999997 — округляем до копеек
                amount = round(float(r['amount']), 2)
            except (TypeError, ValueError):
                problem_rows.append({**r, 'reason': f'Некорректная сумма "{r["amount"]}"'})
                continue

            resolved = resolve_subscriber(r['tariff'], r['dogowor'], lookups)
            if not resolved:
                problem_rows.append({**r, 'reason': 'Абонент не найден в UserTable/OldLoginDogowor'})
                continue

            number, etrap, is_enterprises = resolved

            rows_to_create.append(PlatejiWhichAddKassirsEveryDay(
                number=number,
                user_etrap=etrap,
                kassir_etrap='Внешние платежи',
                type_pay=TARIFF_TO_TYPE[r['tariff']],
                pay_category='Внешние Платежи',
                manager=r['manager'],
                date=r['date'].date(),
                kodOplaty=pay_id_str,
                dogowor=r['dogowor'],
                name=r['fio'],
                is_enterprises=is_enterprises,
                price=amount,
                file_name=str(uploaded_file),
                who_add_file=request.user.username,
            ))

        if request.POST.get('vneshniePlatejiExportProblems'):
            if not problem_rows:
                messages.success(request, 'Проблемных строк нет')
                return render(request, TEMPLATE, context)
            return build_problem_rows_xlsx_response(problem_rows)

        totalCount = len(parsed_rows)
        context['totalCount'] = totalCount
        context['matched_count'] = len(rows_to_create)
        context['problem_count'] = len(problem_rows)
        context['totalAmount'] = round(sum(r.price for r in rows_to_create), 2)
        context['fileAmount'] = round(sum(float(r['amount']) for r in parsed_rows), 2)
        context['is_test_mode'] = bool(request.POST.get('vneshniePlatejiTest'))

        by_kassa = {}
        for r in rows_to_create:
            k = by_kassa.setdefault(r.manager, {'count': 0, 'amount': 0.0})
            k['count'] += 1
            k['amount'] += r.price
        context['by_kassa'] = [(m, v['count'], round(v['amount'], 2)) for m, v in by_kassa.items()]

        if context['is_test_mode']:
            messages.success(request, 'Проверка прошла успешно (ничего не сохранено в БД)')
        elif problem_rows:
            messages.error(request, f'Добавление запрещено: {len(problem_rows)} проблемных строк из {totalCount}. Скачайте список проблемных строк, исправьте и загрузите файл заново.')
        else:
            try:
                with transaction.atomic():
                    if PlatejiWhichAddKassirsEveryDay.objects.select_for_update().filter(file_name=str(uploaded_file)).exists():
                        messages.error(request, f'Файл "{str(uploaded_file)}" уже был добавлен ранее (повторная проверка).')
                        return render(request, TEMPLATE, context)
                    PlatejiWhichAddKassirsEveryDay.objects.bulk_create(rows_to_create)
                    SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.create(
                        file_name=str(uploaded_file),
                        etrap_add=ETRAP_ADD_V2,  # метка: файл добавлен через v2 (по ней фильтрует VneshniePlatejiAddAdmin2)
                        who_add=request.user.username,
                        when_add=datetime.now(),
                    )
                    StaffAction.objects.create(
                        user=request.user,
                        comment=f'Добавление в PlatejiWhichAddKassirsEveryDay (Внешние платежи Milli Billing, новый формат), файл {str(uploaded_file)}, строк {len(rows_to_create)}, добавил {request.user.username}',
                        action='Импорт с xlsx внешние платежи в БД',
                    )
                messages.success(request, f'Успешно добавлено {len(rows_to_create)} записей')
            except Exception as e:
                messages.error(request, f'Ошибка при сохранении, тип ошибки == {e}')
                logger.error(f'Ошибка при сохранении PlatejiWhichAddKassirsEveryDay (внешние платежи, новый формат), тип ошибки == {e}')

    return render(request, TEMPLATE, context)
