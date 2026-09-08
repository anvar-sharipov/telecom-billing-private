from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count, Max, Q
from django.contrib.postgres.aggregates import BoolOr

from telekom.models import OnceDogoworAdd, StaffAction

from datetime import datetime
import urllib.parse
import tablib

import logging
logger = logging.getLogger(__name__)

ROLLBACK_PASSWORD = '543569145637383'

SERVICE_TYPE_LABELS = {'belet': 'Belet'}


def MBonceDogoworAddAdmin(request):
    context = {}

    if not request.user.is_superuser or not request.user.username == 'admin1':
        return redirect('HomePage')

    context['MBonceDogoworAddAdmin'] = True
    context['admin_allow'] = True

    if request.method == 'GET' and request.GET.get('download_etrap'):
        etrap = request.GET.get('download_etrap')
        service_type = request.GET.get('service_type', '')
        rows = OnceDogoworAdd.objects.filter(etrap=etrap, service_type=service_type).order_by('id')

        headers = ('Услуга', 'Пользователь', 'Новый договор', 'Договор для поиска', 'Учетное имя', 'etrap', 'Номер абонента', 'Найден в', 'Применено', 'Кто добавил', 'Когда добавлено', 'Файл')
        data = tablib.Dataset(headers=headers)
        for r in rows:
            data.append((r.service_type, r.fio, r.new_dogowor, r.search_dogowor, r.login, r.etrap, r.number, r.found_in, r.is_applied, r.who_add, r.created_at.strftime('%d.%m.%Y %H:%M') if r.created_at else '', r.file_name))

        filename = f"OnceDogoworAdd_{etrap}_{service_type}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.xlsx"
        encoded_filename = urllib.parse.quote(filename.encode('utf-8'))

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
        return response

    if request.method == 'POST' and 'rollback_etrap' in request.POST:
        etrap = request.POST.get('rollback_etrap')
        service_type = request.POST.get('rollback_service_type', '')
        entered_password = request.POST.get('rollback_password', '')

        if entered_password != ROLLBACK_PASSWORD:
            messages.error(request, f'Неверный пароль отката. Этрап "{etrap}" ({service_type}) не тронут.')
        elif OnceDogoworAdd.objects.filter(etrap=etrap, service_type=service_type, is_applied=True).exists():
            messages.error(request, f'Откат запрещён: этрап "{etrap}" ({service_type}) уже применён в UserTable/OldLoginDogowor. Сначала нужно откатить применение (MB once dogowor nach).')
        else:
            deleted_count = OnceDogoworAdd.objects.filter(etrap=etrap, service_type=service_type).count()
            OnceDogoworAdd.objects.filter(etrap=etrap, service_type=service_type).delete()
            StaffAction.objects.create(user=request.user, comment=f'Откат OnceDogoworAdd, этрап {etrap}, услуга {service_type}, удалено записей {deleted_count}, дата отката {datetime.now()}, откатил {request.user.username}', action='Импорт с xlsx Интернет Начисления в БД')
            messages.success(request, f'Этрап "{etrap}" ({service_type}) откачен, удалено записей: {deleted_count}')

    groups_data = OnceDogoworAdd.objects.values('etrap', 'service_type').annotate(
        count=Count('id'),
        applied_count=Count('id', filter=Q(is_applied=True)),
        is_applied=BoolOr('is_applied'),
        who_add=Max('who_add'),
        created_at=Max('created_at'),
    ).order_by('etrap', 'service_type')

    context['groups_data'] = groups_data
    context['SERVICE_TYPE_LABELS'] = SERVICE_TYPE_LABELS

    return render(request, 'telekom/admin_pages/MBonceDogoworAddAdmin.html', context)
