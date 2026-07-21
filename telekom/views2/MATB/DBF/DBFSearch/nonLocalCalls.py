from django.shortcuts import render, redirect
from django.db.models import Sum, F
from django.db.models.functions import Cast
from django.db.models import IntegerField
from django.contrib import messages

import re
from datetime import datetime
from datetime import date
from calendar import monthrange
# для удаления дубликатов с списка
from collections import OrderedDict

from telekom.views2.myFunc.myFunc import get_etrap_and_types, getLoggedUserEtrap
from telekom.models import NonLocalCall, UserTable, Zakaz


def nonLocalCalls(request):
    context={}
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.username == 'Gayyp' or request.user.username == 'Halekowa_Gulshat' or request.user.username == 'lenashb':
            log = 'Dashoguz'
            context['matbIndex'] = True
            context['nonLocalCalls'] = True
        else:
            etrap_types = get_etrap_and_types(request.user)
            etraps = etrap_types['etraps']
            log = etraps[0]
            types = etrap_types['types']
            if 'MTB' in types or request.user.username == 'lenashb': # request.user.username == 'Halekowa_Gulshat'
                if request.user.username == 'lenashb':
                    context['SHBIndex'] = True  
                else:
                    context['matbIndex'] = True
                context['nonLocalCalls'] = True
            else:
                messages.error(request, f'Доступ только для MTB')
                return redirect('user-login')
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')

    # if request.user.username != 'lenashb' and not (request.user.is_superuser and request.user.username == 'admin1') and request.user.username != 'AyshatGoroglyMtb' and  request.user.username != 'Gayyp':
    # if request.user.username != 'lenashb' and not (request.user.is_superuser and request.user.username == 'admin1') and request.user.username != 'AyshatGoroglyMtb' and  request.user.username != 'Gayyp':
    #     messages.error(request, f'У вас нет доступа')
    #     return redirect('user-login')




    # context = {}
    # context['matbIndex'] = True
    # context['nonLocalCalls'] = True


    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date

    # log = getLoggedUserEtrap(request.user.username)
    context['log'] = log
    context['etrap'] = request.GET.get('etrap')
    context['etraps'] = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['number'] = request.GET.get('number')

    

    if request.GET.get('number'):
        number = re.sub('[-]', '', request.GET.get('number'))
    else:
        number = False

    if request.user.username == 'lenashb' and number:
        context['show_calls'] = False
        print(number)
        try:
            user = UserTable.objects.get(etrap = 'Dashoguz', number=number)
            if user.is_enterprises:
                context['show_calls'] = True
        except:
            pass

    start = request.GET.get('start') if request.GET.get('start') != None else current_date
    end = request.GET.get('end') if request.GET.get('end') != None else current_date
    context['start'] = start
    context['end'] = end

    tables = NonLocalCall.objects.filter(SUB_A=number, SUB_A_etrap=request.GET.get('etrap'), DATE__range=[start, end]).order_by("DATE")

    
    if request.GET.get('etrap') == 'Dashoguz':
        zakaz_cals = Zakaz.objects.filter(NUMBER_A=number, DATE__range=[start, end]).exclude(total_price="0")
        total_zakaz = 0
        total_zakaz_minut = 0
        for z in zakaz_cals:
            total_zakaz += float(z.total_price)
            total_zakaz_minut += int(z.MT)
        print('tut')
        context['zakaz_cals'] = zakaz_cals
        context['total_zakaz'] = total_zakaz
        context['total_zakaz_minut'] = total_zakaz_minut


        



    context['tables'] = tables

    # context['total_MT'] = tables.aggregate(Sum('MT'))['MT__sum']
    context['total_MT'] = tables.aggregate(
        total=Sum(Cast(F('MT'), output_field=IntegerField()))
        )['total']
    
    context['total_price'] = tables.aggregate(Sum('total_price'))['total_price__sum']

    if request.GET.get('etrap') == 'Dashoguz':
        if tables and zakaz_cals:
                umumy_minut = context['total_MT'] + total_zakaz_minut
                umumy_price = context['total_price'] + total_zakaz
                context['umumy_minut'] = umumy_minut
                context['umumy_price'] = umumy_price


    
   




    return render(request, 'telekom/MATB/DBF/DBFSearch/nonLocalCalls.html', context)