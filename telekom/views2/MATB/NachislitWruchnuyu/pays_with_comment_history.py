from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from datetime import datetime
from telekom.models import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q

from django.utils import timezone


def pays_with_comment_history(request):

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    request_user = request.user
    groups = request_user.groups.all()
    request_user_etrap = ''
    request_user_type = ''
    for g in groups:
        request_user_etrap, request_user_type = g.name.split('_')
        if request_user_type == 'MTB':# or request.user.username == 'admin1':
            break

    if request_user_type != 'MTB' and (not request.user.is_superuser and request.user.username != 'admin1') and (request.user.username != 'lenashb'):
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')

    context = {}

    context['pays_with_comment_history'] = True
    context['etraps'] = etraps
    # context['all_new_for_mtb'] = True


    current_date = datetime.now().date()
    formatted_date = current_date.strftime('%Y-%m-%d')
    current_year, current_month, current_day = formatted_date.split('-')

    context['formatted_date'] = formatted_date
    context['current_year'] = current_year
    context['current_month'] = current_month
    context['current_day'] = current_day
    if (request.user.is_superuser and request.user.username == 'admin1') or request.user.username == 'lenashb':
        request_user_etrap = 'Dashoguz'
        context['request_user_etrap'] = request_user_etrap 
    
    if request_user_type == 'MTB':
        context['matbIndex'] = True 
        context['request_user_etrap'] = request_user_etrap 






    etrap = request.GET.get('etrap') if request.GET.get('etrap') else ''
    number = request.GET.get('number') if request.GET.get('number') else ''
    comment = request.GET.get('comment') if request.GET.get('comment') else ''
    date_from = request.GET.get('date_from') if request.GET.get('date_from') else ''
    date_to = request.GET.get('date_to') if request.GET.get('date_to') else ''

    # Начинаем с пустого Q
    filters = Q()

    if etrap:
        filters &= Q(etrap__icontains=etrap)
    if number:
        filters &= Q(number__icontains=number)
    if comment:
        filters &= Q(comment__icontains=comment)
    if date_from:
        filters &= Q(date_pay__gte=date_from)
    if date_to:
        filters &= Q(date_pay__lte=date_to)

    pays = PaysWithComment.objects.filter(filters).order_by('-date_pay')

    context['pays'] = pays
    context['selected_etrap'] = etrap
    context['number'] = number
    context['comment'] = comment
    context['date_from'] = date_from
    context['date_to'] = date_to




    return render(request, 'telekom/MATB/NachislitWruchnuyu/pays_with_comment_history.html', context)
