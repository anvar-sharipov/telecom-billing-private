from django.shortcuts import render, redirect
from django.db.models import Q
from django.db.models import Sum
from django.contrib import messages

from datetime import date

from telekom.models import ImportInternetPlateji, ImportInternetPlatejiOFF
from telekom.views2.myFunc.myFunc import getLoggedUserEtrap, loggedUserEtrapAndGroup



def internetPlatejiSearch(request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    context={}
    context['matbIndex'] = True
    context['InternetPlatejiSearch'] = True
    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date
    # log = getLoggedUserEtrap(request.user.username)
    context['log'] = log
    
    start = request.GET.get('start') if request.GET.get('start') != None else current_date
    end = request.GET.get('end') if request.GET.get('end') != None else current_date
    context['start'] = start
    context['end'] = end

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

    context['etraps'] = etraps

    context['log'] = log if log in etraps else ''


    getAllPayTypes = ImportInternetPlateji.objects.values('type')
    type_list = []
    for i in getAllPayTypes: 
        for key, val in i.items():
            if val not in type_list:
                type_list.append(val)
    context['type_list'] = type_list



    dogowor = request.GET.get('dogowor') if request.GET.get('dogowor') != None else ''
    FAO = request.GET.get('FAO') if request.GET.get('FAO') != None else ''
    type_ = request.GET.get('type_') if request.GET.get('type_') != None else ''
    etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else ''

    context['etrap'] = etrap
    context['dogowor'] = dogowor
    context['FAO'] = FAO
    context['get_type'] = type_
    context['off'] = True if request.GET.get('off') != None else False


    if request.GET.get('off') == None:
        tables = ImportInternetPlateji.objects.filter(
            Q(dogowor__icontains=dogowor) &
            Q(FAO__icontains=FAO) &
            Q(type__icontains=type_) &
            Q(etrap__icontains=etrap)
            ).filter(pay_date__range=[start,end])
    else:
        tables = ImportInternetPlatejiOFF.objects.filter(
            Q(dogowor__icontains=dogowor) &
            Q(FAO__icontains=FAO) &
            Q(type__icontains=type_) &
            Q(etrap__icontains=etrap)
            ).filter(pay_date__range=[start,end])

     # Если нажал на посмотреть все 
    if request.method == 'POST':
        context['tables'] = tables
        context['totalSum'] = tables.aggregate(Sum('price'))['price__sum']
    else:
        context['tables'] = tables[:20]
        context['totalSum'] = tables[:20].aggregate(Sum('price'))['price__sum']
        context['lenTables'] = len(tables)
        


    return render(request, 'telekom/MATB/xlsx/xlsxSearch/InternetPlatejiSearch.html', context)