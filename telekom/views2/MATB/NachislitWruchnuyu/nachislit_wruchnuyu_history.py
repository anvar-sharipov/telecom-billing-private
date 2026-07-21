from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from datetime import datetime
from telekom.models import *




def nachislit_wruchnuyu_history(request):
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

    request_user = request.user
    groups = request_user.groups.all()
    request_user_etrap = ''
    request_user_type = ''
    for g in groups:
        request_user_etrap, request_user_type = g.name.split('_')
        if request_user_type == 'MTB':# or request.user.username == 'admin1':
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

    context['nachislit_wruchnuyu_history'] = True
    if request_user_type == 'MTB':
        context['matbIndex'] = True 
        context['request_user_etrap'] = request_user_etrap 

    context['etraps'] = etraps

    etrap = request.GET.get('etrap')
    number = request.GET.get('number', '')
    comment = request.GET.get('comment', '')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    context['number'] = number
    context['selected_etrap'] = etrap
    context['comment'] = comment
    context['date_from'] = date_from
    context['date_to'] = date_to

  



    if etrap and (number or comment or date_from or date_to):

        allow = False
        if not request.user.is_superuser and request.user.username != 'admin1':
            if etrap == request_user_etrap:
                allow = True
        else:
            allow = True

        if not allow:
            messages.error(request, f"Выберите абонента с своего этрапа")
            return render(request, 'telekom/MATB/NachislitWruchnuyu/nachislit_wruchnuyu_history.html', context)


        queryset = NachislitWruchnuyuHistory.objects.all()
        if etrap:
            queryset = queryset.filter(etrap=etrap)
            ic('queryset2', queryset)
        
        
        if number:
            queryset = queryset.filter(number=number)
        
        if comment:
            queryset = queryset.filter(comment__icontains=comment)

        # Фильтрация по датам
        if date_from:
            queryset = queryset.filter(date__gte=date_from)

        if date_to:
            queryset = queryset.filter(date__lte=date_to)
    
        context['results'] = queryset.order_by('-date')


    return render(request, 'telekom/MATB/NachislitWruchnuyu/nachislit_wruchnuyu_history.html', context)
