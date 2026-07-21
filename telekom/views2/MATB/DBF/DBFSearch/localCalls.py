import collections
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

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup
from telekom.models import LocalCall



def localCalls(request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    context = {}
    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date

    # log = getLoggedUserEtrap(request.user.username)
    context['matbIndex'] = True
    context['localCalls'] = True
    context['log'] = log
    context['etrap'] = request.GET.get('etrap')
    context['etraps'] = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['number'] = request.GET.get('number')
    if request.GET.get('number'):
        number = re.sub('[-]', '', request.GET.get('number'))
    else:
        number = False

    start = request.GET.get('start') if request.GET.get('start') != None else current_date
    end = request.GET.get('end') if request.GET.get('end') != None else current_date
    context['start'] = start
    context['end'] = end

    if start[5:7] != end[5:7]:
        messages.error(request, f'Диапозон поиска не должно превышать 1 месяц')
        return render(request, 'telekom/MATB/DBF/DBFSearch/localCalls.html', context)

    tables = LocalCall.objects.filter(SUB_A=number, etrap=request.GET.get('etrap'), DATE__range=[start, end])
    context['tables'] = tables

    
    if tables:
        # Если фильтр по дате только в отрезке 1 дня 
        if start[-2:] == end[-2:]:
            
            total_mt = tables.aggregate(Sum('MT'))
            if int(total_mt['MT__sum']) > 5:
                context['OneDay'] = True
            context['total_MT'] = total_mt['MT__sum']
            context['total_price'] = (total_mt['MT__sum'] - 5) * 0.0006
        # Если фильтр отрезок > 1 дня
        else:
            umumyTotal_MT_Netto = 0
            # {date: total_MT}
            check_list = {}
            for table in tables:
                if table.DATE not in check_list:
                    check_list[table.DATE] = [int(table.MT)]
                else:
                    check_list[table.DATE][0] += int(table.MT)

            # Удаляем дни с разговорами < 6 минут из check_list
            check_listCopy = check_list.copy()
            for i,v in check_listCopy.items():
                if v[0] > 5:
                    check_list[i].append((check_list[i][0]-5) * 0.0006)
                    check_list[i][0] -= 5
                    umumyTotal_MT_Netto += check_list[i][0]
                else:
                    del check_list[i]

            context['check_list'] = collections.OrderedDict(sorted(check_list.items()))
            # collections.OrderedDict(sorted(check_list.items()))



            # Узнаем сколько дней надо фильтрвоать
            iter = int(end[-2:]) - int(start[-2:])

            # {'tables1': obj, 'tables2': obj} Nitem = Ntables
            list_of_tables = {}
            #  Сначала берем первый день отрезка
            firstTable = LocalCall.objects.filter(SUB_A=number, etrap=request.GET.get('etrap'), DATE__range=[start, start])
            # Если разговор первого дня отрезка > 5 то добавляем его в наш словарь 
            # firstTableAggregate = firstTable.aggregate(Sum('MT'))
            firstTableAggregate = firstTable.aggregate(
                total=Sum(Cast(F('MT'), output_field=IntegerField()))
            )['total']
            print('firstTableAggregate', firstTableAggregate)
            if firstTableAggregate:
                if int(firstTableAggregate) > 5:
                    list_of_tables['tables0'] = firstTable

            # теперь проходимся по остольным дням отрезка в цикле
            for i in range(1, iter + 1):
                # При каждой итерации увеличиваем день поиска на 1 при помощти цикла и фильтруем каждый день  
                iterStart = f"{start[:-2]}{int(start[-1:])+i}"
                iterEnd = f"{start[:-2]}{int(start[-1:])+i}"
                iterTable = LocalCall.objects.filter(SUB_A=number, etrap=request.GET.get('etrap'), DATE__range=[iterStart, iterEnd])

                # iterTableAggregate = iterTable.aggregate(Sum('MT'))
                iterTableAggregate = iterTable.aggregate(
                    total=Sum(Cast(F('MT'), output_field=IntegerField()))
                )['total']
                # Если разговор очередного дня  > 5  то добавляем его в наш словарь 
                if iterTableAggregate:
                    if int(iterTableAggregate) > 5:
                        list_of_tables[f'tables{i}'] = LocalCall.objects.filter(SUB_A=number, etrap=request.GET.get('etrap'), DATE__range=[iterStart, iterEnd])


            context['iterTables'] =  list_of_tables #collections.OrderedDict(sorted(list_of_tables.items()))
            context['umumyTotal_MT_Netto'] = umumyTotal_MT_Netto
            context['umumyTotal_Price_Netto'] = umumyTotal_MT_Netto * 0.0006



    return render(request, 'telekom/MATB/DBF/DBFSearch/localCalls.html', context)
