from django.shortcuts import render, redirect
from django.db.models import Q
from django.db.models import Sum
from django.core.paginator import Paginator
from django.contrib import messages

from telekom.models import ImportAlemNachisleniyaOFF, ImportAlemNachisleniyaON, ImportInternetNachisleniyaOFF
from telekom.views2.myFunc.myFunc import getLoggedUserEtrap, loggedUserEtrapAndGroup



def alemNachisleniyaSearch(request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    context={}
    # log = getLoggedUserEtrap(request.user.username)
    context['log'] = log
    context['matbIndex'] = True
    context['alemNachisleniyaSearch'] = True
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035', '2036', '2037']
    context['etraps'] = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

    year = request.GET.get('year') if request.GET.get('year') else ''
    month = request.GET.get('month') if request.GET.get('month') else ''
    etrap = request.GET.get('etrap') if request.GET.get('etrap') else ''

    context['year'] = year
    context['month'] = month
    context['etrap'] = etrap

    dogowor = request.GET.get('dogowor') if request.GET.get('dogowor') != None else ''
    login = request.GET.get('login') if request.GET.get('login') != None else ''
    FAO = request.GET.get('FAO') if request.GET.get('FAO') != None else ''

    context['dogowor'] = dogowor
    context['FAO'] = FAO
    context['login'] = login
    context['off'] = True if request.GET.get('off') != None else False

    if year and month and etrap:
        if request.GET.get('off') == None:
            tables = ImportAlemNachisleniyaON.objects.filter(
                Q(dogowor__icontains=dogowor) &
                Q(FAO__icontains=FAO) &
                Q(login__icontains=login) &
                Q(year__icontains=year) &
                Q(month__icontains=month) &
                Q(etrap__icontains=etrap)
                ).order_by('-price')
        else:
            tables = ImportAlemNachisleniyaOFF.objects.filter(
                Q(dogowor__icontains=dogowor) &
                Q(FAO__icontains=FAO) &
                Q(login__icontains=login) &
                Q(year__icontains=year) &
                Q(month__icontains=month) &
                Q(etrap__icontains=etrap)
                ).order_by('-price')
            
        # Если нажал на посмотреть все 
        if request.method == 'POST':
            context['tables'] = tables
            context['totalSum'] = tables.aggregate(Sum('price'))['price__sum']
        else:
            context['tables'] = tables[:20]
            context['totalSum'] = tables[:20].aggregate(Sum('price'))['price__sum']
            context['lenTables'] = len(tables)



    return render(request, 'telekom/MATB/xlsx/xlsxSearch/alemNachisleniyaSearch.html', context)