from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from datetime import datetime
from telekom.models import *



def snyatie_new_history(request):
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

    # Получаем фильтры из запроса
    filter_number = request.GET.get('number', '')
    filter_etrap = request.GET.get('etrap', '')
    filter_comment = request.GET.get('comment_galochka', '')

    context = {
        'all_new_for_mtb': True,
        'etraps': etraps,
        'snyatie_new_history': True,
        'request_user_etrap': request_user_etrap,
        'current_date': datetime.now().date()
    }

    if filter_number or filter_etrap or filter_comment:
        queryset = SnyatieInfo.objects.all()
        
        if filter_number:
            queryset = queryset.filter(number__icontains=filter_number)
        if filter_etrap:
            queryset = queryset.filter(etrap=filter_etrap)
        if filter_comment:
            queryset = queryset.filter(comment_galochka__icontains=filter_comment)
        
        context['snyatie_info_list'] = queryset.order_by('-date_galochka')

    

    return render(request, 'telekom/MATB/NachislitWruchnuyu/snyatie_new_history.html', context)

