from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Sum, Max, Q
from django.contrib.postgres.aggregates import BoolOr

from telekom.models import MilliBillingPay, SaveInfoAboutWhoAddAndNachPaysFromBilling, StaffAction, KassaExcelFiles

from datetime import datetime

import logging
logger = logging.getLogger(__name__)

ROLLBACK_PASSWORD = '543569145637383'


def milliBillingPayAdmin(request):
    context = {}

    if not request.user.is_superuser or not request.user.username == 'admin1':
        return redirect('HomePage')

    context['milliBillingPayAdmin'] = True
    context['admin_allow'] = True

    if request.method == 'POST' and 'delete_file_name' in request.POST:
        file_name = request.POST.get('delete_file_name')
        entered_password = request.POST.get('rollback_password', '')

        if entered_password != ROLLBACK_PASSWORD:
            messages.error(request, f'Неверный пароль отката. Файл "{file_name}" не тронут.')
        elif MilliBillingPay.objects.filter(file_name=file_name, is_nach=True).exists():
            messages.error(request, f'Откат запрещён: платежи файла "{file_name}" уже начислены в UserTable. Сначала нужно откатить начисление.')
        else:
            deleted_count = MilliBillingPay.objects.filter(file_name=file_name).count()
            MilliBillingPay.objects.filter(file_name=file_name).delete()
            SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.filter(file_name=file_name).delete()
            StaffAction.objects.create(user=request.user, comment=f'Откат платежей Milli Billing, файл {file_name}, удалено записей {deleted_count}, дата отката {datetime.now()}, откатил {request.user.username}', action='Откат платежей Milli Billing')
            messages.success(request, f'Файл "{file_name}" откачен, удалено записей: {deleted_count}')

    files = MilliBillingPay.objects.values('file_name').annotate(
        count=Count('id'),
        total_price=Sum('price'),
        matched_count=Count('id', filter=Q(is_matched=True)),
        unmatched_count=Count('id', filter=Q(is_matched=False)),
        is_nach=BoolOr('is_nach'),
        who_add_file=Max('who_add_file'),
        when_added_file=Max('when_added_file'),
    ).order_by('-when_added_file')

    context['files'] = files

    return render(request, 'telekom/admin_pages/milliBillingPayAdmin.html', context)
