from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count, Sum, Max
from django.contrib.postgres.aggregates import BoolOr

from telekom.models import YhlasIyul2026InternetNach, StaffAction

from datetime import datetime
import urllib.parse
import tablib

import logging
logger = logging.getLogger(__name__)

ROLLBACK_PASSWORD = '543569145637383'


def MBonceIntAddAdmin(request):
    context = {}

    if not request.user.is_superuser or not request.user.username == 'admin1':
        return redirect('HomePage')

    context['MBonceIntAddAdmin'] = True
    context['admin_allow'] = True

    if request.method == 'GET' and request.GET.get('download_etrap'):
        etrap = request.GET.get('download_etrap')
        rows = YhlasIyul2026InternetNach.objects.filter(etrap=etrap).order_by('id')

        headers = ('Пользователь', 'Договор', 'Учетное имя', 'Аренда', 'etrap', 'Номер абонента', 'Предприятия', 'Начислено', 'Кто добавил', 'Когда добавлено', 'Файл')
        data = tablib.Dataset(headers=headers)
        for r in rows:
            data.append((r.fio, r.dogowor, r.login, r.arenda, r.etrap, r.number, r.is_enterprises, r.is_nach, r.who_add, r.created_at.strftime('%d.%m.%Y %H:%M') if r.created_at else '', r.file_name))

        filename = f"YhlasIyul2026InternetNach_{etrap}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.xlsx"
        encoded_filename = urllib.parse.quote(filename.encode('utf-8'))

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
        return response

    if request.method == 'POST' and 'rollback_etrap' in request.POST:
        etrap = request.POST.get('rollback_etrap')
        entered_password = request.POST.get('rollback_password', '')

        if entered_password != ROLLBACK_PASSWORD:
            messages.error(request, f'Неверный пароль отката. Этрап "{etrap}" не тронут.')
        elif YhlasIyul2026InternetNach.objects.filter(etrap=etrap, is_nach=True).exists():
            messages.error(request, f'Откат запрещён: этрап "{etrap}" уже начислен в NachMinus. Сначала нужно откатить начисление.')
        else:
            deleted_count = YhlasIyul2026InternetNach.objects.filter(etrap=etrap).count()
            YhlasIyul2026InternetNach.objects.filter(etrap=etrap).delete()
            StaffAction.objects.create(user=request.user, comment=f'Откат YhlasIyul2026InternetNach, этрап {etrap}, удалено записей {deleted_count}, дата отката {datetime.now()}, откатил {request.user.username}', action='Импорт с xlsx Интернет Начисления в БД')
            messages.success(request, f'Этрап "{etrap}" откачен, удалено записей: {deleted_count}')

    etraps_data = YhlasIyul2026InternetNach.objects.values('etrap').annotate(
        count=Count('id'),
        total_arenda=Sum('arenda'),
        is_nach=BoolOr('is_nach'),
        who_add=Max('who_add'),
        created_at=Max('created_at'),
    ).order_by('etrap')

    context['etraps_data'] = etraps_data

    return render(request, 'telekom/admin_pages/MBonceIntAddAdmin.html', context)
