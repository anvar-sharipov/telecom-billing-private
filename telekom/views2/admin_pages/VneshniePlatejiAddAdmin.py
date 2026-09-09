from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count, Sum, Max
from django.contrib.postgres.aggregates import BoolOr

from telekom.models import PlatejiWhichAddKassirsEveryDay, SaveInfoAboutWhoAddAndNachPaysFromBilling, StaffAction

from datetime import datetime
import urllib.parse
import tablib

import logging
logger = logging.getLogger(__name__)

ROLLBACK_PASSWORD = '543569145637383'
KASSA_MANAGERS = ['Capar', 'eGov', 'Saray', 'Toleg', 'Turkmenpost diller']


def VneshniePlatejiAddAdmin(request):
    context = {}

    if not request.user.is_superuser or not request.user.username == 'admin1':
        return redirect('HomePage')

    context['VneshniePlatejiAddAdmin'] = True
    context['admin_allow'] = True

    if request.method == 'GET' and request.GET.get('download_file'):
        file_name = request.GET.get('download_file')
        rows = PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=file_name, manager__in=KASSA_MANAGERS).order_by('id')

        headers = ('KASSA', 'Услуга', 'Ф.И.О', 'Договор', '№ платежа', 'Дата', 'Сумма', 'Этрап', 'Номер', 'Начислено', 'Кто добавил', 'Когда добавлено')
        data = tablib.Dataset(headers=headers)
        for r in rows:
            data.append((r.manager, r.type_pay, r.name, r.dogowor, r.kodOplaty, r.date, r.price, r.user_etrap, r.number, r.file_is_nach, r.who_add_file, r.when_added_file.strftime('%d.%m.%Y %H:%M') if r.when_added_file else ''))

        filename = f"VneshniePlateji_{file_name}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.xlsx"
        encoded_filename = urllib.parse.quote(filename.encode('utf-8'))

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
        return response

    if request.method == 'POST' and 'rollback_file_name' in request.POST:
        file_name = request.POST.get('rollback_file_name')
        entered_password = request.POST.get('rollback_password', '')

        if entered_password != ROLLBACK_PASSWORD:
            messages.error(request, f'Неверный пароль отката. Файл "{file_name}" не тронут.')
        elif PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=file_name, manager__in=KASSA_MANAGERS, file_is_nach=True).exists():
            messages.error(request, f'Откат запрещён: файл "{file_name}" уже начислен. Сначала нужно откатить начисление.')
        else:
            deleted_count = PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=file_name, manager__in=KASSA_MANAGERS).count()
            PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=file_name, manager__in=KASSA_MANAGERS).delete()
            SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.filter(file_name=file_name).delete()
            StaffAction.objects.create(user=request.user, comment=f'Откат внешних платежей (Milli Billing), файл {file_name}, удалено записей {deleted_count}, дата отката {datetime.now()}, откатил {request.user.username}', action='Импорт с xlsx внешние платежи в БД')
            messages.success(request, f'Файл "{file_name}" откачен, удалено записей: {deleted_count}')

    files_data = PlatejiWhichAddKassirsEveryDay.objects.filter(manager__in=KASSA_MANAGERS).values('file_name').annotate(
        count=Count('id'),
        total_price=Sum('price'),
        is_nach=BoolOr('file_is_nach'),
        who_add_file=Max('who_add_file'),
        when_added_file=Max('when_added_file'),
    ).order_by('-when_added_file')

    context['files_data'] = files_data

    return render(request, 'telekom/admin_pages/VneshniePlatejiAddAdmin.html', context)
