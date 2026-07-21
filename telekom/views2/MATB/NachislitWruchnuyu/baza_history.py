from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.models import BazaChangeInfo  # импортируем модель
from datetime import datetime

def baza_history(request):
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

    request_user = request.user
    groups = request_user.groups.all()
    request_user_etrap = ''
    request_user_type = ''
    
    for g in groups:
        request_user_etrap, request_user_type = g.name.split('_')
        if request_user_type == 'MTB':
            break

    if request_user_type != 'MTB' and (not request.user.is_superuser and request.user.username != 'admin1'):
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')

    context = {}
    context['all_new_for_mtb'] = True

    current_date = datetime.now().date()
    formatted_date = current_date.strftime('%Y-%m-%d')
    current_year, current_month, current_day = formatted_date.split('-')

    context['formatted_date'] = formatted_date
    context['current_year'] = current_year
    context['current_month'] = current_month
    context['current_day'] = current_day
    context['baza_history'] = True
    
    if request_user_type == 'MTB':
        context['matbIndex'] = True 
        context['request_user_etrap'] = request_user_etrap 

    context['etraps'] = etraps

    selected_etrap = request.GET.get('etrap')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    akt_raport = request.GET.get('akt_raport')
    comment = request.GET.get('comment')
    number = request.GET.get('number')

    # Фильтрация данных на основе параметров GET
    filter_args = {}
    
    if selected_etrap:
        filter_args['etrap'] = selected_etrap
    
    if number:
        filter_args['number__icontains'] = number
    
    if comment:
        filter_args['comment__icontains'] = comment
    
    if akt_raport:
        filter_args['akt_raport__icontains'] = akt_raport

    if date_from:
        filter_args['date__gte'] = date_from  # Дата от
    
    if date_to:
        filter_args['date__lte'] = date_to  # Дата до

    # Получаем отфильтрованные данные
    baza_changes = BazaChangeInfo.objects.filter(**filter_args).order_by('-date')[:100]

    context['baza_changes'] = baza_changes
    context['selected_etrap'] = selected_etrap
    context['date_from'] = date_from
    context['date_to'] = date_to
    context['akt_raport'] = akt_raport
    context['comment'] = comment
    context['number'] = number

    return render(request, 'telekom/MATB/NachislitWruchnuyu/baza_history.html', context)

