"""
Откат файлов, добавленных через "Внешние платежи add v2" (nachMilliBillingPay2, новый формат Milli Billing).

То же самое, что VneshniePlatejiAddAdmin, но показывает и откатывает ТОЛЬКО файлы v2 —
их отличает метка SaveInfoAboutWhoAddAndNachPaysFromBilling.etrap_add == ETRAP_ADD_V2.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Count, Sum, Max
from django.contrib.postgres.aggregates import BoolOr

from telekom.models import PlatejiWhichAddKassirsEveryDay, SaveInfoAboutWhoAddAndNachPaysFromBilling, StaffAction
from telekom.views2.admin_pages.VneshniePlatejiAddAdmin import ROLLBACK_PASSWORD, KASSA_MANAGERS
from telekom.views2.MATB.MBnachisleniya.nachMilliBillingPay2 import ETRAP_ADD_V2

from datetime import datetime
import urllib.parse
import tablib

import logging
logger = logging.getLogger(__name__)

TEMPLATE = 'telekom/admin_pages/VneshniePlatejiAddAdmin2.html'


def _v2_file_names():
    return set(SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.filter(etrap_add=ETRAP_ADD_V2).values_list('file_name', flat=True))


def VneshniePlatejiAddAdmin2(request):
    context = {}

    if not request.user.is_superuser or not request.user.username == 'admin1':
        return redirect('HomePage')

    context['VneshniePlatejiAddAdmin2'] = True
    context['admin_allow'] = True

    v2_files = _v2_file_names()

    if request.method == 'GET' and request.GET.get('download_file'):
        file_name = request.GET.get('download_file')
        if file_name not in v2_files:
            messages.error(request, f'Файл "{file_name}" не добавлялся через "Внешние платежи add v2".')
            return redirect('VneshniePlatejiAddAdmin2')

        rows = PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=file_name, manager__in=KASSA_MANAGERS).order_by('id')

        headers = ('KASSA', 'Услуга', 'Ф.И.О', 'Договор', '№ платежа', 'Дата', 'Сумма', 'Этрап', 'Номер', 'Начислено', 'Кто добавил', 'Когда добавлено')
        data = tablib.Dataset(headers=headers)
        for r in rows:
            data.append((r.manager, r.type_pay, r.name, r.dogowor, r.kodOplaty, r.date, r.price, r.user_etrap, r.number, r.file_is_nach, r.who_add_file, r.when_added_file.strftime('%d.%m.%Y %H:%M') if r.when_added_file else ''))

        filename = f"VneshniePlateji_v2_{file_name}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.xlsx"
        encoded_filename = urllib.parse.quote(filename.encode('utf-8'))

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
        return response

    if request.method == 'POST' and 'rollback_file_name' in request.POST:
        file_name = request.POST.get('rollback_file_name')
        entered_password = request.POST.get('rollback_password', '')

        if entered_password != ROLLBACK_PASSWORD:
            messages.error(request, f'Неверный пароль отката. Файл "{file_name}" не тронут.')
        elif file_name not in v2_files:
            messages.error(request, f'Файл "{file_name}" не добавлялся через "Внешние платежи add v2" — здесь его откатить нельзя.')
        else:
            try:
                with transaction.atomic():
                    rows = PlatejiWhichAddKassirsEveryDay.objects.select_for_update().filter(file_name=file_name, manager__in=KASSA_MANAGERS)
                    if rows.filter(file_is_nach=True).exists():
                        messages.error(request, f'Откат запрещён: файл "{file_name}" уже начислен. Сначала нужно откатить начисление.')
                    else:
                        deleted_count = rows.count()
                        rows.delete()
                        SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.filter(file_name=file_name, etrap_add=ETRAP_ADD_V2).delete()
                        StaffAction.objects.create(user=request.user, comment=f'Откат внешних платежей v2 (Milli Billing, новый формат), файл {file_name}, удалено записей {deleted_count}, дата отката {datetime.now()}, откатил {request.user.username}', action='Импорт с xlsx внешние платежи в БД')
                        messages.success(request, f'Файл "{file_name}" откачен, удалено записей: {deleted_count}')
            except Exception as e:
                messages.error(request, f'Ошибка при откате, ничего не удалено, тип ошибки == {e}')
                logger.error(f'Ошибка при откате внешних платежей v2, файл {file_name}, тип ошибки == {e}')
            v2_files = _v2_file_names()

    files_data = PlatejiWhichAddKassirsEveryDay.objects.filter(manager__in=KASSA_MANAGERS, file_name__in=v2_files).values('file_name').annotate(
        count=Count('id'),
        total_price=Sum('price'),
        is_nach=BoolOr('file_is_nach'),
        who_add_file=Max('who_add_file'),
        when_added_file=Max('when_added_file'),
    ).order_by('-when_added_file')

    context['files_data'] = files_data

    return render(request, TEMPLATE, context)
