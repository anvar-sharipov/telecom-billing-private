from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.models import Group

import re
from datetime import date

from telekom.models import PayHistory
from telekom.views2.myFunc.myFunc import get_etrap_and_types, getLoggedUserEtrap, loggedUserEtrapAndGroup



def receipts(request):
    # EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    # if EtrapAndGroup[1] == 'Kassa' or request.user.is_superuser:
    #     log = EtrapAndGroup[0]
    # else:
    #     messages.error(request,"Доступ только соотрудникам Кассы")
    #     return redirect('user-login')
    
    context={}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            log = 'Dashoguz'
            context['kassaIndex'] = True
            context['kassa'] = True
            context['allow_to_pay'] = True
        else:
            etrap_types = get_etrap_and_types(request.user)
            etraps = etrap_types['etraps']
            log = etraps[0]
            types = etrap_types['types']
            if 'Kassa' in types:
                context['kassaIndex'] = True
                context['receipts'] = True
            else:
                messages.error(request, f'У вас нет доступа к Кассе')
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')
    # log = getLoggedUserEtrap(request.user.username)
    # context['log'] = log
    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date

    context['kassaIndex'] = True
    context['receipts'] = True
    context['etraps'] = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['number'] = request.GET.get('number')
    context['etrap'] = request.GET.get('etrap')
    context['name'] = request.GET.get('name')
    context['surname'] = request.GET.get('surname')
    context['street'] = request.GET.get('street')
    context['home'] = request.GET.get('home')
    context['flat'] = request.GET.get('flat')
    context['get_kassir'] = request.GET.get('kassir')
    context['date_start'] = request.GET.get('date_start')
    context['date_end'] = request.GET.get('date_end')


    lists_of_kassir = []
    for user in Group.objects.get(name="Dashoguz_Kassa").user_set.all():
        if user.username not in lists_of_kassir:
            lists_of_kassir.append(user.username)
    for user in Group.objects.get(name="Akdepe_Kassa").user_set.all():
        if user.username not in lists_of_kassir:
            lists_of_kassir.append(user.username)
    for user in Group.objects.get(name="Gorogly_Kassa").user_set.all():
        if user.username not in lists_of_kassir:
            lists_of_kassir.append(user.username)
    for user in Group.objects.get(name="Ruhubelent_Kassa").user_set.all():
        if user.username not in lists_of_kassir:
            lists_of_kassir.append(user.username)
    for user in Group.objects.get(name="S.A.Nyyazow_Kassa").user_set.all():
        if user.username not in lists_of_kassir:
            lists_of_kassir.append(user.username)
    for user in Group.objects.get(name="Turkmenbashy_Kassa").user_set.all():
        if user.username not in lists_of_kassir:
            lists_of_kassir.append(user.username)
    for user in Group.objects.get(name="Boldumsaz_Kassa").user_set.all():
        if user.username not in lists_of_kassir:
            lists_of_kassir.append(user.username)
    for user in Group.objects.get(name="Koneurgench_Kassa").user_set.all():
        if user.username not in lists_of_kassir:
            lists_of_kassir.append(user.username)
    context['kassirs'] = lists_of_kassir
    
    # kassirs_obj = User.objects.all()
    # lists_of_kassir = []
    # for kassir in kassirs_obj:
    #     if kassir.username[:5] == 'kassa' or kassir.username[:5] == 'admin':
    #         lists_of_kassir.append(kassir.username)
    # context['kassirs'] = lists_of_kassir

    if request.GET.get('number'):
        numb = re.sub('[-]', '', request.GET.get('number'))
    else:
        numb = ''

    number = numb
    etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else ''
    name = request.GET.get('name') if request.GET.get('name') != None else ''
    surname = request.GET.get('surname') if request.GET.get('surname') != None else ''
    street = request.GET.get('street') if request.GET.get('street') != None else ''
    home = request.GET.get('home') if request.GET.get('home') != None else ''
    flat = request.GET.get('flat') if request.GET.get('flat') != None else ''
    kassir = request.GET.get('kassir') if request.GET.get('kassir') != None else ''

 

    context['objs'] = PayHistory.objects.filter(
        Q(abonent__number__icontains=number) &
        Q(abonent__etrap__icontains=etrap) &
        Q(abonent__name__icontains=name) &
        Q(abonent__surname__icontains=surname) &
        Q(abonent__street__icontains=street) &
        Q(abonent__home__icontains=home) &
        Q(abonent__flat__icontains=flat) &
        Q(kassir__icontains=kassir)
        ).filter(date__range=[request.GET.get('date_start'),request.GET.get('date_end')]).order_by('-date')[:50]

    return render(request, 'telekom/Kassa/receipts.html', context)



