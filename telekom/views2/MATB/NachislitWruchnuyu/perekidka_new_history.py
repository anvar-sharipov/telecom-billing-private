from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from datetime import datetime
from telekom.models import *
from django.contrib.auth.models import User



def perekidka_new_history(request):
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
    context['perekidka_new_history'] = True

    current_date = datetime.now().date()
    formatted_date = current_date.strftime('%Y-%m-%d')
    context['formatted_date'] = formatted_date
    context['etraps'] = etraps

    if request_user_type == 'MTB':
        context['matbIndex'] = True 
        context['request_user_etrap'] = request_user_etrap 

    # Получение списка пользователей для выпадающего списка операторов
    context['users'] = User.objects.all()

    # Обработка фильтра
    user1_number = request.GET.get('user1Number', '')
    user2_number = request.GET.get('user2Number', '')
    operator = request.GET.get('operator', '')
    etrap = request.GET.get('etrap', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    comment = request.GET.get('comment', '')

    # Применение фильтров к запросу
    perekidka_records = PerekidkaInfoNew.objects.all()

    if user1_number or user2_number or operator or etrap or date_from or date_to or comment:
        if user1_number:
            perekidka_records = perekidka_records.filter(user1Number__icontains=user1_number) | perekidka_records.filter(user2KabelNumber__icontains=user1_number)
        if user2_number:
            perekidka_records = perekidka_records.filter(user2Number__icontains=user2_number) 
        if operator:
            perekidka_records = perekidka_records.filter(operator=operator)
        if etrap:
            perekidka_records = perekidka_records.filter(user1Etrap=etrap) | perekidka_records.filter(user2Etrap=etrap)
        if date_from:
            perekidka_records = perekidka_records.filter(date__date__gte=date_from)
        if date_to:
            perekidka_records = perekidka_records.filter(date__date__lte=date_to)
        if comment:
            perekidka_records = perekidka_records.filter(comment__icontains=comment)

        context['date_from'] = date_from
        context['date_to'] = date_to
        context['perekidka_records'] = perekidka_records.order_by('-date')

    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new_history.html', context)