from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

import re
import urllib.parse
from collections import Counter
from datetime import datetime

import pdfplumber
import tablib

import logging
logger = logging.getLogger(__name__)


COLUMN_NAMES = ['shertnama', 'telefon', 'nyrhnama', 'login', 'ip', 'doly_ady', 'doly_salgysy']
COLUMN_HEADERS = ('Şertnama Belgisi', 'Telefon Belgisi', 'Nyrhnama', 'Login', 'Ip-salgysy', 'Doly Ady', 'Doly Salgysy')

# запасные границы колонок (px), если на странице не нашлось ни одной "закрашенной" строки для авто-определения
FALLBACK_COL_BOUNDS = [18.0, 94.6, 169.6, 334.7, 421.0, 496.4, 645.1, 823.9]

ANCHOR_RE = re.compile(r'^[A-Za-z][A-Za-z0-9\-]*\d[A-Za-z0-9\-]*$')
DATE_RE = re.compile(r'^\d{2}\.\d{2}\.\d{4}$')


def detect_column_bounds(page):
    """Ищет строку из 7 закрашенных ячеек (rects) с одинаковым top, чтобы взять их x0/x1 как границы колонок."""
    tops = {}
    for r in page.rects:
        top = round(r['top'], 1)
        tops.setdefault(top, []).append(r)

    for top, rects in tops.items():
        if len(rects) == 7:
            rects = sorted(rects, key=lambda r: r['x0'])
            bounds = [rects[0]['x0']] + [r['x1'] for r in rects]
            return bounds

    return FALLBACK_COL_BOUNDS


def col_for_x(x0, bounds):
    for i in range(len(COLUMN_NAMES)):
        if bounds[i] <= x0 < bounds[i + 1]:
            return COLUMN_NAMES[i]
    return None


def join_col(name, parts):
    if name == 'ip':
        return ''.join(parts)
    return ' '.join(parts)


def parse_intizar_pdf(file_obj):
    """Парсит отчёт Milli Billing "Döredilen Şertnamalar" (созданные договора).
    Возвращает список словарей с полями COLUMN_NAMES."""
    records = []

    with pdfplumber.open(file_obj) as pdf:
        bounds = None
        for page in pdf.pages:
            words = page.extract_words(keep_blank_chars=False)
            if not words:
                continue

            if bounds is None:
                bounds = detect_column_bounds(page)

            footer_tops = [w['top'] for w in words if DATE_RE.match(w['text'])]
            footer_top = footer_tops[0] if footer_tops else None
            body_words = [w for w in words if footer_top is None or abs(w['top'] - footer_top) > 2]

            anchors = [w for w in body_words if col_for_x(w['x0'], bounds) == 'shertnama' and ANCHOR_RE.match(w['text'])]
            anchors = sorted(anchors, key=lambda w: w['top'])

            for i, a in enumerate(anchors):
                top_start = (anchors[i - 1]['top'] + a['top']) / 2 if i > 0 else a['top'] - 20
                top_end = (a['top'] + anchors[i + 1]['top']) / 2 if i + 1 < len(anchors) else a['top'] + 20
                row_words = [w for w in body_words if top_start <= w['top'] < top_end]

                cols = {name: [] for name in COLUMN_NAMES}
                for w in sorted(row_words, key=lambda w: (w['top'], w['x0'])):
                    c = col_for_x(w['x0'], bounds)
                    if c:
                        cols[c].append(w['text'])

                record = {name: join_col(name, cols[name]).strip() for name in COLUMN_NAMES}
                records.append(record)

    return records


def intizarInternetNyrhnamaSort(request):
    context = {}

    if not request.user.is_superuser or not request.user.username == 'admin1':
        return redirect('HomePage')

    context['intizarInternetNyrhnamaSort'] = True
    context['admin_allow'] = True

    if request.method == 'POST' and 'pdf_file' in request.FILES:
        pdf_file = request.FILES['pdf_file']

        if not pdf_file.name.lower().endswith('.pdf'):
            messages.error(request, 'Файл должен быть формата PDF')
            return render(request, 'telekom/admin_pages/intizarInternetNyrhnamaSort.html', context)

        try:
            records = parse_intizar_pdf(pdf_file)
        except Exception as e:
            messages.error(request, f'Не удалось разобрать PDF, ошибка: {e}')
            logger.error(f'Ошибка парсинга PDF в intizarInternetNyrhnamaSort: {e}')
            return render(request, 'telekom/admin_pages/intizarInternetNyrhnamaSort.html', context)

        if not records:
            messages.error(request, 'В файле не найдено ни одной строки договора')
            return render(request, 'telekom/admin_pages/intizarInternetNyrhnamaSort.html', context)

        # Вкладка 1: сырые данные 1:1 как в PDF
        sheet1 = tablib.Dataset(headers=COLUMN_HEADERS)
        sheet1.title = 'Sertnamalar'
        for r in records:
            sheet1.append((r['shertnama'], r['telefon'], r['nyrhnama'], r['login'], r['ip'], r['doly_ady'], r['doly_salgysy']))

        # Вкладка 2: количество абонентов по каждому Nyrhnama
        counts = Counter(r['nyrhnama'] for r in records)
        sheet2 = tablib.Dataset(headers=('Nyrhnama', 'Kol-wo abonentow'))
        sheet2.title = 'Nyrhnama sort'
        for nyrh, count in counts.most_common():
            sheet2.append((nyrh, count))
        sheet2.append(('ITOGO', len(records)))

        book = tablib.Databook((sheet1, sheet2))

        filename = f"intizar_internet_nyrhnama_sort_{datetime.now().strftime('%Y-%m-%d_%H%M')}.xlsx"
        encoded_filename = urllib.parse.quote(filename.encode('utf-8'))

        response = HttpResponse(book.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
        return response

    return render(request, 'telekom/admin_pages/intizarInternetNyrhnamaSort.html', context)
