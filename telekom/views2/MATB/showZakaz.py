from django.shortcuts import render
from telekom.models import Zakaz

from telekom.views2.myFunc.myFunc import getLoggedUserEtrap

from datetime import date

def showZakaz(request):
    context = {}
    current_date = str(date.today())
    # context['current_date'] = current_date
    # current_year = current_date[0:4]
    # current_month = current_date[5:7]
    # current_day = current_date[8:]
    # days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]
    
    log = getLoggedUserEtrap(request.user.username)

    context['log'] = log
    context['matbIndex'] = True
    context['showZakaz'] = True
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['etraps'] = etraps
    context['etrap'] = request.GET.get('etrap') if request.GET.get('etrap') in etraps else ''

    start = f"{request.GET.get('start')} 00:00:00" if request.GET.get('start') != None else f"{current_date} 00:00:00"
    end = f"{request.GET.get('end')} 23:59:59" if request.GET.get('end') != None else f"{current_date} 23:59:59"

    context['start'] = request.GET.get('start') if request.GET.get('start') != None else current_date
    context['end'] = request.GET.get('end') if request.GET.get('end') != None else current_date

    if log in etraps:
        etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else log
    else:
        etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else ''

    actions = ['повторно', 'бно', 'заказ подтвержден']
    action = request.GET.get('action') if request.GET.get('action') != None else ''
    context['actions'] = actions
    context['action'] = action


    if action in actions:
        ZakazCallsList = Zakaz.objects.filter(DATE__range=[start,end], etrap=etrap, action=action)
    else:
        ZakazCallsList = Zakaz.objects.filter(DATE__range=[start,end], etrap=etrap)
    context['ZakazCalls'] = ZakazCallsList
    context['lenZakazCalls'] = len(ZakazCallsList)
    
    return render(request, 'telekom/MATB/showZakaz.html', context)