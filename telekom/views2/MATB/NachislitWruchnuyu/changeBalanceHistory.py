from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.models import ChangeBalanceWithComment
from django.db.models import Q
from datetime import datetime
import tablib
from django.http import HttpResponse

def changeBalanceHistory(request):
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow',
              'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']

    request_user = request.user
    groups = request_user.groups.all()
    request_user_type = ''
    request_user_etrap = ''
    for g in groups:
        request_user_etrap, request_user_type = g.name.split('_')
        if request_user_type == 'MTB':
            break

    if request_user_type != 'MTB' and (not request.user.is_superuser and request.user.username != 'admin1'):
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')

    context = {}
    context['etraps'] = etraps

    # Фильтры
    etrap_filter = request.GET.get('etrap', '')
    number_filter = request.GET.get('number', '')
    type_filter = request.GET.get('type', '')

    history = []
    if etrap_filter or number_filter or type_filter:
        history = ChangeBalanceWithComment.objects.all().order_by('-date')

        # Ограничение для обычного пользователя
        if not request.user.is_superuser:
            history = history.filter(etrap=request_user_etrap)

        # Применение фильтров
        if etrap_filter:
            history = history.filter(etrap=etrap_filter)
        if number_filter:
            history = history.filter(number__icontains=number_filter)
        if type_filter:
            history = history.filter(change_type=type_filter)

    context['history'] = history
    context['etrap_filter'] = etrap_filter
    context['number_filter'] = number_filter
    context['type_filter'] = type_filter
    
    

    # Экспорт в Excel
    if 'export' in request.GET:
        dataset = tablib.Dataset()
        dataset.headers = ['Номер', 'Этрап', 'Старый баланс', 'Новый баланс', 'Тип', 'Комментарий', 'Дата', 'Оператор']
        for h in history:
            dataset.append([
                h.number,
                h.etrap,
                h.old_balance,
                h.new_balance,
                h.change_type,
                h.comment,
                h.date.strftime('%Y-%m-%d %H:%M:%S'),
                h.operator,
            ])
        response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="history.xlsx"'
        return response

    return render(request, 'telekom/MATB/NachislitWruchnuyu/changeBalanceHistory.html', context)
