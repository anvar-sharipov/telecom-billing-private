"""
Админ -> Отчёты.

Страница для выгрузки отчётов в Excel. Пока один отчёт: "Внешние платежи" за любой
период (или за всё время) с фильтрами и сортировкой.

ТОЛЬКО ЧТЕНИЕ: ничего в базе не меняет.

Внешние платежи = PlatejiWhichAddKassirsEveryDay с pay_category из VNESHNIE_CATEGORIES:
  - 'Внешние плптежи'  — так (с опечаткой) категория приходила из lanbilling (2024 — 18.07.2026)
  - 'Внешние Платежи'  — так её пишет импорт milli billing (vneshniePlatejiAdd / nachMilliBillingPay2)
Период фильтруется по дате платежа (поле date).
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import FileResponse
from django.db.models import Count, Sum, Min, Max

from telekom.models import PlatejiWhichAddKassirsEveryDay

from datetime import datetime, date
import tempfile
import xlsxwriter

import logging
logger = logging.getLogger(__name__)

TEMPLATE = 'telekom/admin_pages/adminReports.html'

VNESHNIE_CATEGORIES = ['Внешние плптежи', 'Внешние Платежи']

# Лимит строк на одном листе Excel — 1 048 576. Берём с запасом (2 строки шапки),
# при превышении строки продолжаются на следующем листе.
MAX_ROWS_PER_SHEET = 1_000_000

# (ключ для формы, поле модели, подпись)
SORT_FIELDS = [
    ('date', 'date', 'Дата платежа'),
    ('manager', 'manager', 'Касса'),
    ('user_etrap', 'user_etrap', 'Этрап абонента'),
    ('type_pay', 'type_pay', 'Услуга'),
    ('price', 'price', 'Сумма'),
    ('number', 'number', 'Номер'),
    ('dogowor', 'dogowor', 'Договор'),
    ('name', 'name', 'Ф.И.О'),
    ('when_added_file', 'when_added_file', 'Когда добавлено'),
    ('file_name', 'file_name', 'Файл'),
]
SORT_MAP = {k: f for k, f, _ in SORT_FIELDS}

# (поле, заголовок, ширина колонки)
COLUMNS = [
    ('id', 'ID', 10),
    ('date', 'Дата платежа', 12),
    ('manager', 'Касса', 20),
    ('pay_category', 'Категория', 16),
    ('type_pay', 'Услуга', 12),
    ('number', 'Номер', 12),
    ('user_etrap', 'Этрап абонента', 15),
    ('dogowor', 'Договор', 14),
    ('name', 'Ф.И.О', 35),
    ('is_enterprises', 'ЮЛ/ФЛ', 8),
    ('kodOplaty', '№ платежа', 18),
    ('price', 'Сумма', 12),
    ('kassir_etrap', 'Этрап кассира', 15),
    ('file_is_nach', 'Начислено', 10),
    ('file_name', 'Файл', 30),
    ('who_add_file', 'Кто добавил', 15),
    ('when_added_file', 'Когда добавлено', 17),
]
COL_IDX = {f: i for i, (f, _, _) in enumerate(COLUMNS)}


def _parse_date(s):
    try:
        return datetime.strptime(s, '%Y-%m-%d').date() if s else None
    except ValueError:
        return None


def _read_params(qd):
    """Читает параметры отчёта из GET. Возвращает dict (и для фильтра, и для формы)."""
    p = {
        'all_time': qd.get('all_time') == '1',
        'date_from': _parse_date(qd.get('date_from', '')),
        'date_to': _parse_date(qd.get('date_to', '')),
        'managers': [m for m in qd.getlist('manager') if m],
        'etraps': [e for e in qd.getlist('user_etrap') if e],
        'type_pays': [t for t in qd.getlist('type_pay') if t],
        'nach': qd.get('nach', ''),  # '' / 'yes' / 'no'
        'sort1': qd.get('sort1', 'date') if qd.get('sort1', 'date') in SORT_MAP else 'date',
        'dir1': 'desc' if qd.get('dir1') == 'desc' else 'asc',
        'sort2': qd.get('sort2', '') if qd.get('sort2', '') in SORT_MAP else '',
        'dir2': 'desc' if qd.get('dir2') == 'desc' else 'asc',
    }
    return p


def _build_queryset(p):
    qs = PlatejiWhichAddKassirsEveryDay.objects.filter(pay_category__in=VNESHNIE_CATEGORIES)
    if not p['all_time']:
        if p['date_from']:
            qs = qs.filter(date__gte=p['date_from'])
        if p['date_to']:
            qs = qs.filter(date__lte=p['date_to'])
    if p['managers']:
        qs = qs.filter(manager__in=p['managers'])
    if p['etraps']:
        qs = qs.filter(user_etrap__in=p['etraps'])
    if p['type_pays']:
        qs = qs.filter(type_pay__in=p['type_pays'])
    if p['nach'] == 'yes':
        qs = qs.filter(file_is_nach=True)
    elif p['nach'] == 'no':
        qs = qs.filter(file_is_nach=False)
    return qs


def _ordering(p):
    order = [('-' if p['dir1'] == 'desc' else '') + SORT_MAP[p['sort1']]]
    if p['sort2'] and p['sort2'] != p['sort1']:
        order.append(('-' if p['dir2'] == 'desc' else '') + SORT_MAP[p['sort2']])
    order.append('id')  # стабильный порядок при равных значениях
    return order


def _period_label(p):
    if p['all_time'] or (not p['date_from'] and not p['date_to']):
        return 'за всё время'
    f = p['date_from'].strftime('%d.%m.%Y') if p['date_from'] else '...'
    t = p['date_to'].strftime('%d.%m.%Y') if p['date_to'] else '...'
    return f'{f} — {t}'


def _ul_fl(v):
    # В базе встречаются 'ЮЛ'/'ФЛ' (milli billing) и 'True'/'False' (lanbilling, True = юр. лицо)
    if v == 'True':
        return 'ЮЛ'
    if v == 'False':
        return 'ФЛ'
    return v or ''


def _export_xlsx(request, p):
    qs = _build_queryset(p).order_by(*_ordering(p))
    fields = [f for f, _, _ in COLUMNS]

    output = tempfile.TemporaryFile()  # на диске, а не в памяти Apache; удаляется сам после отдачи
    wb = xlsxwriter.Workbook(output, {'constant_memory': True, 'remove_timezone': True})

    f_head = wb.add_format({'bold': True, 'bg_color': '#D9E1F2', 'border': 1, 'text_wrap': True, 'valign': 'vcenter'})
    f_info = wb.add_format({'bold': True})
    f_total = wb.add_format({'bold': True, 'num_format': '#,##0.00'})
    f_date = wb.add_format({'num_format': 'dd.mm.yyyy'})
    f_dt = wb.add_format({'num_format': 'dd.mm.yyyy hh:mm'})
    f_money = wb.add_format({'num_format': '#,##0.00'})

    i_date, i_dt, i_price = COL_IDX['date'], COL_IDX['when_added_file'], COL_IDX['price']
    i_ulfl, i_nach = COL_IDX['is_enterprises'], COL_IDX['file_is_nach']
    last_col = len(COLUMNS) - 1
    price_letter = xlsxwriter.utility.xl_col_to_name(i_price)
    period = _period_label(p)

    sheets = []  # (ws, количество строк данных)

    def new_sheet():
        n = len(sheets) + 1
        ws = wb.add_worksheet('Внешние платежи' if n == 1 else f'Внешние платежи {n}')
        for i, (_, _, w) in enumerate(COLUMNS):
            ws.set_column(i, i, w)
        # Строка 1: итог (SUBTOTAL считает только видимые строки — учитывает автофильтр)
        ws.write(0, 0, f'Внешние платежи {period}' + (f' (лист {n})' if n > 1 else ''), f_info)
        ws.write(0, i_price - 1, 'Итого (видимые):', f_info)
        ws.write_formula(0, i_price, f'=SUBTOTAL(9,{price_letter}3:{price_letter}1048576)', f_total)
        # Строка 2: шапка
        ws.set_row(1, 30)
        for i, (_, title, _) in enumerate(COLUMNS):
            ws.write(1, i, title, f_head)
        ws.freeze_panes(2, 0)
        sheets.append([ws, 0])
        return sheets[-1]

    cur = new_sheet()
    total_rows = 0
    total_sum = 0.0

    for row in qs.values_list(*fields).iterator(chunk_size=5000):
        if cur[1] >= MAX_ROWS_PER_SHEET:
            cur = new_sheet()
        ws = cur[0]
        r = cur[1] + 2
        for i, v in enumerate(row):
            if v is None or v == '':
                continue
            if i == i_date:
                ws.write_datetime(r, i, v, f_date)
            elif i == i_dt:
                ws.write_datetime(r, i, v, f_dt)
            elif i == i_price:
                ws.write_number(r, i, round(v, 2), f_money)
            elif i == i_ulfl:
                ws.write_string(r, i, _ul_fl(v))
            elif i == i_nach:
                ws.write_string(r, i, 'Да' if v else 'Нет')
            elif isinstance(v, (int, float)):
                ws.write_number(r, i, v)
            else:
                ws.write_string(r, i, str(v))
        cur[1] += 1
        total_rows += 1
        total_sum += row[i_price] or 0

    # Автофильтр на шапку и все строки данных каждого листа
    for ws, n in sheets:
        if n:
            ws.autofilter(1, 0, n + 1, last_col)
        else:
            ws.autofilter(1, 0, 1, last_col)

    ws_sum = wb.add_worksheet('Итого')
    ws_sum.set_column(0, 0, 45)
    ws_sum.set_column(1, 1, 20)
    ws_sum.write(0, 0, 'Внешние платежи', f_info)
    ws_sum.write(1, 0, 'Период (по дате платежа)')
    ws_sum.write(1, 1, period)
    ws_sum.write(2, 0, 'Фильтры')
    filt = []
    if p['managers']:
        filt.append('Касса: ' + ', '.join(p['managers']))
    if p['etraps']:
        filt.append('Этрап: ' + ', '.join(p['etraps']))
    if p['type_pays']:
        filt.append('Услуга: ' + ', '.join(p['type_pays']))
    if p['nach']:
        filt.append('Начислено: ' + ('Да' if p['nach'] == 'yes' else 'Нет'))
    ws_sum.write(2, 1, '; '.join(filt) if filt else 'нет')
    ws_sum.write(3, 0, 'Всего строк')
    ws_sum.write_number(3, 1, total_rows)
    ws_sum.write(4, 0, 'Общая сумма')
    ws_sum.write_number(4, 1, round(total_sum, 2), f_total)
    ws_sum.write(5, 0, 'Сумма видимых строк (с учётом автофильтра), по листам:')
    for k, (ws, n) in enumerate(sheets):
        ws_sum.write(6 + k, 0, ws.name)
        if n:
            ws_sum.write_formula(6 + k, 1, f"=SUBTOTAL(9,'{ws.name}'!{price_letter}3:{price_letter}{n + 2})", f_total)
        else:
            ws_sum.write_number(6 + k, 1, 0, f_total)
    ws_sum.write(7 + len(sheets), 0, 'Сформировано')
    ws_sum.write(7 + len(sheets), 1, f"{datetime.now().strftime('%d.%m.%Y %H:%M')} ({request.user.username})")

    wb.close()

    logger.info(f'adminReports: внешние платежи выгружены {request.user.username}, {period}, строк {total_rows}, листов {len(sheets)}')

    period_fn = 'all_time' if period == 'за всё время' else period.replace(' — ', '_').replace('.', '-')
    filename = f"VneshniePlateji_{period_fn}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.xlsx"
    output.seek(0)
    return FileResponse(output, as_attachment=True, filename=filename, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


def adminReports(request):
    if not request.user.is_superuser or not request.user.username == 'admin1':
        return redirect('HomePage')

    context = {'adminReports': True, 'admin_allow': True}
    p = _read_params(request.GET)

    if request.GET.get('action') == 'download':
        if not p['all_time'] and not p['date_from'] and not p['date_to']:
            messages.error(request, 'Укажите период или отметьте "За всё время".')
        else:
            try:
                return _export_xlsx(request, p)
            except Exception as e:
                logger.error(f'adminReports: ошибка выгрузки внешних платежей: {e}')
                messages.error(request, f'Ошибка при формировании Excel: {e}')

    base = PlatejiWhichAddKassirsEveryDay.objects.filter(pay_category__in=VNESHNIE_CATEGORIES)

    # Списки для фильтров
    context['manager_list'] = list(base.values('manager').annotate(c=Count('id')).order_by('manager'))
    context['etrap_list'] = list(base.exclude(user_etrap='').values_list('user_etrap', flat=True).distinct().order_by('user_etrap'))
    context['type_pay_list'] = list(base.exclude(type_pay='').values_list('type_pay', flat=True).distinct().order_by('type_pay'))
    context['all_range'] = base.aggregate(mn=Min('date'), mx=Max('date'))
    context['sort_fields'] = [(k, label) for k, _, label in SORT_FIELDS]

    # Предпросмотр: сколько строк и какая сумма попадёт в выгрузку
    if request.GET.get('action') == 'preview':
        if not p['all_time'] and not p['date_from'] and not p['date_to']:
            messages.error(request, 'Укажите период или отметьте "За всё время".')
        else:
            qs = _build_queryset(p)
            context['preview'] = qs.aggregate(c=Count('id'), s=Sum('price'), mn=Min('date'), mx=Max('date'))
            context['preview_by_manager'] = list(qs.values('manager').annotate(c=Count('id'), s=Sum('price')).order_by('-s'))
            context['preview_sheets'] = (context['preview']['c'] + MAX_ROWS_PER_SHEET - 1) // MAX_ROWS_PER_SHEET if context['preview']['c'] else 0

    context['p'] = p
    context['p_date_from'] = p['date_from'].isoformat() if p['date_from'] else ''
    context['p_date_to'] = p['date_to'].isoformat() if p['date_to'] else ''
    context['today'] = date.today().isoformat()
    context['max_rows_per_sheet'] = MAX_ROWS_PER_SHEET

    return render(request, TEMPLATE, context)
