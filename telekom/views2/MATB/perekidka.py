from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.models import *

import re
from datetime import datetime
from datetime import date

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert



def perekidka(request):

    # test = PayHistory.objects.create(abonent=UserTable.objects.get(number='20000', etrap='Dashoguz'), internet=33, date=datetime.now(), kassir=request.user.username)
    # InterpayBilling.objects.create(pay_history=test)


    context={}
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser or request.user.username == "lenashb":
        log = EtrapAndGroup[0]
        context['log'] = log
        context['matbIndex'] = True
        context['perekidka'] = True
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    cols = ['Абонплата', 'Слр', 'Код', 'Заказ', 'Прочее', 'Доп.услуги', 'Интернет','Кабель', 'Alem']
    context['cols'] = cols
    context['etraps'] = etraps

    current_date = str(date.today())
    context['current_date'] = current_date
    current_year = current_date[0:4]
    context['current_year'] = current_year
    current_month = current_date[5:7]
    current_day = current_date[8:]
    month_word = monthСonvert(current_month)

    
    etrap1 = request.GET.get('etrap1')
    number1 = re.sub('[-]', '', request.GET.get('number1')) if request.GET.get('number1') != None else False

    

    etrap2 = request.GET.get('etrap2')
    number2 = re.sub('[-]', '', request.GET.get('number2')) if request.GET.get('number2') != None else False

    context['etrap1'] = etrap1
    context['etrap2'] = etrap2
    context['number1'] = request.GET.get('number1')
    context['number2'] = request.GET.get('number2')

    if number1:
        if len(number1) <= 4:
            abonent1 = UserTable.objects.filter(ids=number1, etrap=etrap1)
            try:
                abonent1 = UserTable.objects.get(ids=number1, etrap=etrap1)
                context['abonent1'] = abonent1
                context['lastPays1'] = abonent1.payhistory_set.order_by('-date')
            except:
                abonent1 = False
        else:

            try:
                abonent1 = UserTable.objects.get(number=number1, etrap=etrap1)
                context['abonent1'] = abonent1
                context['lastPays1'] = abonent1.payhistory_set.order_by('-date')
            except:
                abonent1 = False
    else:
        abonent1 = False


    if number2:
        if len(number2) <= 4:
            abonent2 = UserTable.objects.filter(ids=number2, etrap=etrap2)
            try:
                abonent2 = UserTable.objects.get(ids=number2, etrap=etrap2)
                context['abonent2'] = abonent2
                context['lastPays2'] = abonent2.payhistory_set.order_by('-date')
            except:
                abonent2 = False
        else:

            try:
                abonent2 = UserTable.objects.get(number=number2, etrap=etrap2)
                context['abonent2'] = abonent2
                context['lastPays2'] = abonent2.payhistory_set.order_by('-date')
            except:
                abonent2 = False
    else:
        abonent2 = False

    if abonent1:
        if abonent1.service:
            service_total_sum1 = 0
            for service in abonent1.service.all():
                service_total_sum1 += service.price
        context['service_total_sum1'] = service_total_sum1

    if abonent2:
        if abonent2.service:
            service_total_sum2 = 0
            for service in abonent2.service.all():
                service_total_sum2 += service.price
        context['service_total_sum2'] = service_total_sum2

    context['abonent1'] = abonent1
    context['abonent2'] = abonent2

    try:
        perekInfoMinus1 = PerekidkaInfo.objects.filter(createDate__range = [f'{current_year}-01-01', f'{current_year}-12-31'], user1Etrap = abonent1.etrap, user1Number = abonent1.number)
        perekInfoPlus1 = PerekidkaInfo.objects.filter(createDate__range = [f'{current_year}-01-01', f'{current_year}-12-31'], user2Etrap = abonent1.etrap, user2Number = abonent1.number)
        context['perekInfoMinus1'] = perekInfoMinus1
        context['perekInfoPlus1'] = perekInfoPlus1
    except:
        pass

    try:
        perekInfoMinus2 = PerekidkaInfo.objects.filter(createDate__range = [f'{current_year}-01-01', f'{current_year}-12-31'], user1Etrap = abonent2.etrap, user1Number = abonent2.number)
        perekInfoPlus2 = PerekidkaInfo.objects.filter(createDate__range = [f'{current_year}-01-01', f'{current_year}-12-31'], user2Etrap = abonent2.etrap, user2Number = abonent2.number)
        context['perekInfoMinus2'] = perekInfoMinus2
        context['perekInfoPlus2'] = perekInfoPlus2
    except:
        pass

###################################################################################################################
    nachMinus = NachMinus.objects.filter(user=abonent1)
    try:
        context['jan'] = nachMinus.get(user=abonent1, year=current_year, month='01')
        if nachMinus.get(user=abonent1, year=current_year, month='01').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent1, year=current_year, month='01').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_jan'] = end_list
    except: 
        pass

    try:
        context['feb'] = nachMinus.get(user=abonent1, year=current_year, month='02')
        if nachMinus.get(user=abonent1, year=current_year, month='02').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent1, year=current_year, month='02').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_feb'] = end_list
    except: 
        pass
    try:
        context['mar'] = nachMinus.get(user=abonent1, year=current_year, month='03')
        if nachMinus.get(user=abonent1, year=current_year, month='03').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent1, year=current_year, month='03').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_mar'] = end_list
    except: 
        pass
    try:
        context['apr'] = nachMinus.get(user=abonent1, year=current_year, month='04')
        if nachMinus.get(user=abonent1, year=current_year, month='04').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent1, year=current_year, month='04').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_apr'] = end_list
    except: 
        pass
    try:
        context['may'] = nachMinus.get(user=abonent1, year=current_year, month='05')
        if nachMinus.get(user=abonent1, year=current_year, month='05').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent1, year=current_year, month='05').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_may'] = end_list
    except: 
        pass
    try:
        context['jun'] = nachMinus.get(user=abonent1, year=current_year, month='06')
        if nachMinus.get(user=abonent1, year=current_year, month='06').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent1, year=current_year, month='06').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_jun'] = end_list
    except: 
        pass
    try:
        context['jul'] = nachMinus.get(user=abonent1, year=current_year, month='07')
        if nachMinus.get(user=abonent1, year=current_year, month='07').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent1, year=current_year, month='07').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_jul'] = end_list
    except: 
        pass
    try:
        context['aug'] = nachMinus.get(user=abonent1, year=current_year, month='08')
        if nachMinus.get(user=abonent1, year=current_year, month='08').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent1, year=current_year, month='08').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_aug'] = end_list
    except: 
        pass
    try:
        context['sep'] = nachMinus.get(user=abonent1, year=current_year, month='09')
        if nachMinus.get(user=abonent1, year=current_year, month='09').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent1, year=current_year, month='09').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_sep'] = end_list
    except: 
        pass
    try:
        context['oct'] = nachMinus.get(user=abonent1, year=current_year, month='10')
        if nachMinus.get(user=abonent1, year=current_year, month='10').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent1, year=current_year, month='10').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_oct'] = end_list
    except: 
        pass
    try:
        context['nov'] = nachMinus.get(user=abonent1, year=current_year, month='11')
        if nachMinus.get(user=abonent1, year=current_year, month='11').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent1, year=current_year, month='11').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_nov'] = end_list
    except: 
        pass
    try:
        context['dec'] = nachMinus.get(user=abonent1, year=current_year, month='12')
        if nachMinus.get(user=abonent1, year=current_year, month='12').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent1, year=current_year, month='12').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_dec'] = end_list
    except: 
        pass
######################################################################################################################

    nachMinus = NachMinus.objects.filter(user=abonent2)
    try:
        context['jan2'] = nachMinus.get(user=abonent2, year=current_year, month='01')
        if nachMinus.get(user=abonent2, year=current_year, month='01').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent2, year=current_year, month='01').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_jan2'] = end_list
    except: 
        pass

    try:
        context['feb2'] = nachMinus.get(user=abonent2, year=current_year, month='02')
        if nachMinus.get(user=abonent2, year=current_year, month='02').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent2, year=current_year, month='02').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_feb2'] = end_list
    except: 
        pass
    try:
        context['mar2'] = nachMinus.get(user=abonent2, year=current_year, month='03')
        if nachMinus.get(user=abonent2, year=current_year, month='03').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent2, year=current_year, month='03').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_mar2'] = end_list
    except: 
        pass
    try:
        context['apr2'] = nachMinus.get(user=abonent2, year=current_year, month='04')
        if nachMinus.get(user=abonent2, year=current_year, month='04').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent2, year=current_year, month='04').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_apr2'] = end_list
    except: 
        pass
    try:
        context['may2'] = nachMinus.get(user=abonent2, year=current_year, month='05')
        if nachMinus.get(user=abonent2, year=current_year, month='05').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent2, year=current_year, month='05').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_may2'] = end_list
    except: 
        pass
    try:
        context['jun2'] = nachMinus.get(user=abonent2, year=current_year, month='06')
        if nachMinus.get(user=abonent2, year=current_year, month='06').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent2, year=current_year, month='06').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_jun2'] = end_list
    except: 
        pass
    try:
        context['jul2'] = nachMinus.get(user=abonent2, year=current_year, month='07')
        if nachMinus.get(user=abonent2, year=current_year, month='07').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent2, year=current_year, month='07').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_jul2'] = end_list
    except: 
        pass
    try:
        context['aug2'] = nachMinus.get(user=abonent2, year=current_year, month='08')
        if nachMinus.get(user=abonent2, year=current_year, month='08').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent2, year=current_year, month='08').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_aug2'] = end_list
    except: 
        pass
    try:
        context['sep2'] = nachMinus.get(user=abonent2, year=current_year, month='09')
        if nachMinus.get(user=abonent2, year=current_year, month='09').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent2, year=current_year, month='09').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_sep2'] = end_list
    except: 
        pass
    try:
        context['oct2'] = nachMinus.get(user=abonent2, year=current_year, month='10')
        if nachMinus.get(user=abonent2, year=current_year, month='10').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent2, year=current_year, month='10').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_oct2'] = end_list
    except: 
        pass
    try:
        context['nov2'] = nachMinus.get(user=abonent2, year=current_year, month='11')
        if nachMinus.get(user=abonent2, year=current_year, month='11').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent2, year=current_year, month='11').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_nov2'] = end_list
    except: 
        pass
    try:
        context['dec2'] = nachMinus.get(user=abonent2, year=current_year, month='12')
        if nachMinus.get(user=abonent2, year=current_year, month='12').dop_usligi_added_Pk:
            added = eval(nachMinus.get(user=abonent2, year=current_year, month='12').dop_usligi_added_Pk)
            end_list = []
            for i in range(len(added['added'])):
                start_list = []
                date_ = added['added'][i][-2]
                nach = added['added'][i][-1]
                start_list.append(date_)
                start_list.append(nach)
                start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                end_list.append(start_list)
            context['end_list_dec2'] = end_list
    except: 
        pass

####################################################################################################################################



    # Если нажал на перекинуть (баланс или все данные)
    if request.method == 'POST' and 'perekidkaAbonplata' in request.POST:
        # Перекидка со всеми данными
        if request.POST.get('perkidkaAll'):
            if request.POST.get('comment') == '':
                messages.error(request, 'Добавьте комментарий')
            else:

                if (abonent1.pk == abonent2.pk):
                    messages.error(request, f"Ошибка! Абонент номер один и тот")
                elif abonent2.name == '' and abonent2.surname == '':

                    
                    num1Edara = False
                    num2Edara = False
                    edara_to_nasel = False
                    nasel_to_edara = False
                    if request.POST.get('num2Edara') and request.POST.get('hOrb') == '':
                            messages.error(request, f"Выберите хоз или буджет")
                            return render(request, 'telekom/MATB/perekidka/perekidka.html', context)
                    num2hb = None if request.POST.get('hOrb') == '' else request.POST.get('hOrb')
                    if num2hb:
                        num2Edara = True
                    if request.POST.get('num2Edara') and abonent1.is_enterprises == False:
                        nasel_to_edara = True
                    elif request.POST.get('num2Edara') == None and abonent1.is_enterprises == True:
                        edara_to_nasel = True
                    

                    
                    # Если перекидка с предпр на насел или наоборот то сохранить в месячный отчет
                    if edara_to_nasel or nasel_to_edara:
                        if abonent1.etrap != abonent2.etrap:
                            try:
                                nachisleniyaOtchet1 = NachisleniyaOtchet.objects.get(year=current_year, month=month_word, etrap=abonent1.etrap)
                            except:
                                nachisleniyaOtchet1 = NachisleniyaOtchet.objects.create(year=current_year, month=month_word, etrap=abonent1.etrap)

                            try:
                                nachisleniyaOtchet2 = NachisleniyaOtchet.objects.get(year=current_year, month=month_word, etrap=abonent2.etrap)
                            except:
                                nachisleniyaOtchet2 = NachisleniyaOtchet.objects.create(year=current_year, month=month_word, etrap=abonent2.etrap)
                        else:
                            try:
                                nachisleniyaOtchet = NachisleniyaOtchet.objects.get(year=current_year, month=month_word, etrap=abonent1.etrap)
                            except:
                                nachisleniyaOtchet = NachisleniyaOtchet.objects.create(year=current_year, month=month_word, etrap=abonent1.etrap)


                        # print('######################################', nachisleniyaOtchet1, nachisleniyaOtchet2)
                     
                        debit = 0
                        kredit = 0
                        if abonent1.b_telefon < 0:
                            debit += abs(abonent1.b_telefon)
                        else:
                            kredit += abonent1.b_telefon

                        if abonent1.b_slr < 0:
                            debit += abs(abonent1.b_slr)
                        else:
                            kredit += abonent1.b_slr

                        if abonent1.b_kod < 0:
                            debit += abs(abonent1.b_kod)
                        else:
                            kredit += abonent1.b_kod

                        if abonent1.b_zakaz < 0:
                            debit += abs(abonent1.b_zakaz)
                        else:
                            kredit += abonent1.b_zakaz

                        if abonent1.b_prochee < 0:
                            debit += abs(abonent1.b_prochee)
                        else:
                            kredit += abonent1.b_prochee

                        if abonent1.b_dop_uslugi < 0:
                            debit += abs(abonent1.b_dop_uslugi)
                        else:
                            kredit += abonent1.b_dop_uslugi

                        if abonent1.b_internet < 0:
                            debit += abs(abonent1.b_internet)
                        else:
                            kredit += abonent1.b_internet
                    
                        if abonent1.b_kabel < 0:
                            debit += abs(abonent1.b_kabel)
                        else:
                            kredit += abonent1.b_kabel

                        if abonent1.b_alem < 0:
                            debit += abs(abonent1.b_alem)
                        else:
                            kredit += abonent1.b_alem
            

                        # 20002 n1 91456 n2 
                        if edara_to_nasel:
                            if abonent1.etrap != abonent2.etrap:
                                nachisleniyaOtchet2.perek_nasel_debit_plus += debit
                                nachisleniyaOtchet2.perek_nasel_kredit_plus += kredit

                                nachisleniyaOtchet1.perek_edara_debit_minus += debit
                                nachisleniyaOtchet1.perek_edara_kredit_minus += kredit
                                nachisleniyaOtchet1.save()
                                nachisleniyaOtchet2.save()
                            else:
                                nachisleniyaOtchet.perek_nasel_debit_plus += debit
                                nachisleniyaOtchet.perek_nasel_kredit_plus += kredit

                                nachisleniyaOtchet.perek_edara_debit_minus += debit
                                nachisleniyaOtchet.perek_edara_kredit_minus += kredit
                                nachisleniyaOtchet.save()
                                


                        elif nasel_to_edara:
                            if abonent1.etrap != abonent2.etrap:
                                nachisleniyaOtchet2.perek_edara_debit_plus += debit
                                nachisleniyaOtchet2.perek_edara_kredit_plus += kredit

                                nachisleniyaOtchet1.perek_nasel_debit_minus += debit
                                nachisleniyaOtchet1.perek_nasel_kredit_minus += kredit
                                nachisleniyaOtchet1.save()
                                nachisleniyaOtchet2.save()
                            else:
                                nachisleniyaOtchet.perek_nasel_debit_minus += debit
                                nachisleniyaOtchet.perek_nasel_kredit_minus += kredit

                                nachisleniyaOtchet.perek_edara_debit_plus += debit
                                nachisleniyaOtchet.perek_edara_kredit_plus += kredit
                                nachisleniyaOtchet.save()
                           
                        
                    

                    
                    arhiwUser = UserTableArhiw.objects.create(
                    number = abonent1.number,
                    etrap = abonent1.etrap,
                    surname = abonent1.surname,
                    name = abonent1.name,
                    street = abonent1.street,
                    home = abonent1.home,
                    flat = abonent1.flat,
                    sotowyy = abonent1.sotowyy,
                    is_enterprises = abonent1.is_enterprises,
                    alem = abonent1.alem,
                    alemCount = abonent1.alemCount,
                    alem_connect_date = abonent1.alem_connect_date,
                    alem_on_date = abonent1.alem_on_date,
                    alem_off_date = abonent1.alem_off_date,
                    alem_disconnect_date = abonent1.alem_disconnect_date,
                    account = abonent1.account,
                    accountName = abonent1.accountName,
                    hb = abonent1.hb,     
                    internet_tarif = abonent1.internet_tarif,
                    internet_connect_date = abonent1.internet_connect_date,
                    internet_disconnect_date = abonent1.internet_disconnect_date,
                    abonplata = abonent1.abonplata,
                    is_on = abonent1.is_on,
                    is_on_date = abonent1.is_on_date,
                    kabel_count = abonent1.kabel_count,
                    connect_date = abonent1.connect_date,
                    kabel_comments = abonent1.kabel_comments,
                    ids = abonent1.ids,
                    login = abonent1.login,
                    dogowor = abonent1.dogowor,
                    b_internet = abonent1.b_internet,
                    b_kabel = abonent1.b_kabel,
                    b_alem = abonent1.b_alem,
                    b_telefon = abonent1.b_telefon,
                    b_slr = abonent1.b_slr,
                    b_kod = abonent1.b_kod,
                    b_zakaz = abonent1.b_zakaz,
                    b_prochee = abonent1.b_prochee,
                    b_dop_uslugi = abonent1.b_dop_uslugi,

                    s_internet = abonent1.s_internet,
                    s_kabel = abonent1.s_kabel,
                    s_alem = abonent1.s_alem,
                    s_telefon = abonent1.s_telefon,
                    s_slr = abonent1.s_slr,
                    s_kod = abonent1.s_kod,
                    s_zakaz = abonent1.s_zakaz,
                    s_prochee = abonent1.s_prochee,
                    s_dop_uslugi = abonent1.s_dop_uslugi,
                    
                    addDate = abonent1.addDate,
                    snyat_date = datetime.now(),
                    snyat_bool = True
                    )
                    if abonent1.service:
                        for i in abonent1.service.all():
                            arhiwUser.service.add(i)
                        arhiwUser.save()
                    
                  
                    if num2Edara == True:
                        abonent2.hb = HozOrBudjet.objects.get(name=num2hb)
                        abonent2.is_enterprises = True
               
                    # №№№
                    InterpayPerekidkaBilling.objects.create(
                        number1=abonent1.number,
                        etrap1=abonent1.etrap,
                        surname1=abonent1.surname,
                        name1=abonent1.name,
                        abonent1_pk=abonent1.pk,

                        internet1 = abonent1.b_internet,
                        alem1 = abonent1.b_alem,
                        telefon1 = abonent1.b_telefon,
                        slr1 = abonent1.b_slr,
                        kod1 = abonent1.b_kod,
                        zakaz1 = abonent1.b_zakaz,
                        prochee1 = abonent1.b_prochee,
                        dop_uslugi1 =abonent1.b_dop_uslugi,
                        kabel1 =abonent1.b_kabel,
                        abonent2_pk=abonent2.pk,

                        number2=abonent2.number,
                        etrap2=abonent2.etrap,
                        surname2=abonent2.surname,
                        name2=abonent2.name,

                        alem2=abonent1.b_alem,
                        internet2 = abonent1.b_internet,
                        telefon2 = abonent1.b_telefon,
                        slr2 = abonent1.b_slr,
                        kod2 = abonent1.b_kod,
                        zakaz2 = abonent1.b_zakaz,
                        prochee2 = abonent1.b_prochee,
                        dop_uslugi2 =abonent1.b_dop_uslugi,
                        kabel2 =abonent1.b_kabel,

                        mtbUsername = request.user.username,
                        mtbEtrap = log,
                        date=datetime.now()
                        )
                    # №№№#


                    # №№№
                    
                    PerekidkaInfo.objects.create(
                        user1Number = abonent1.number,
                        user1Etrap = abonent1.etrap,
                        user2Number = abonent2.number,
                        user2Etrap = abonent2.etrap,
                        user1_is_enterprises = abonent1.is_enterprises,
                        user2_is_enterprises = abonent2.is_enterprises,

                        telefon1 = abonent1.b_telefon,
                        internet1 = abonent1.b_internet,
                        kabel1 = abonent1.b_kabel,
                        alem1 = abonent1.b_alem,
                        slr1 = abonent1.b_slr,
                        kod1 = abonent1.b_kod,
                        zakaz1 = abonent1.b_zakaz,
                        prochee1 = abonent1.b_prochee,
                        dop_uslugi1 = abonent1.b_dop_uslugi,

                        telefon2 = abonent1.b_telefon,
                        internet2 = abonent1.b_internet,
                        kabel2 = abonent1.b_kabel,
                        alem2 = abonent1.b_alem,
                        slr2 = abonent1.b_slr,
                        kod2 = abonent1.b_kod,
                        zakaz2 = abonent1.b_zakaz,
                        prochee2 = abonent1.b_prochee,
                        dop_uslugi2 = abonent1.b_dop_uslugi,
                        comment=f"{request.POST.get('comment')}\n\nполная перекидка с номера {abonent1.number}, {abonent1.etrap} на номер {abonent2.number}, {abonent2.etrap}",
                        operator = request.user
                    )

                    # №№№#

                        
                    abonent2.surname = abonent1.surname
                    abonent2.name = abonent1.name
                    abonent2.street = abonent1.street
                    abonent2.home = abonent1.home
                    abonent2.flat = abonent1.flat
                    abonent2.sotowyy = abonent1.sotowyy
                    # abonent2.is_enterprises = abonent1.is_enterprises

                    abonent2.alem = abonent1.alem
                    abonent2.alemCount = abonent1.alemCount
                    abonent2.alem_connect_date = abonent1.alem_connect_date
                    abonent2.alem_on_date = abonent1.alem_on_date
                    abonent2.alem_off_date = abonent1.alem_off_date
                    abonent2.alem_disconnect_date = abonent1.alem_disconnect_date

                    if abonent1.is_enterprises:
                        abonent2.is_enterprises=True
                        abonent2.account = abonent1.account
                        abonent2.hb = HozOrBudjet.objects.get(name=abonent1.hb.name)
                    abonent2.abonplata = abonent1.abonplata

                    abonent2.internet_tarif = abonent1.internet_tarif
                    abonent2.internet_connect_date = abonent1.internet_connect_date
                    abonent2.internet_disconnect_date = abonent1.internet_disconnect_date


                    abonent2.is_on = abonent1.is_on
                    abonent2.is_on_date = abonent1.is_on_date
                    abonent2.kabel_count = abonent1.kabel_count
                    abonent2.connect_date = abonent1.connect_date
                    abonent2.kabel_comments = abonent1.kabel_comments
                    abonent2.ids = abonent1.ids
                    
                    if abonent1.service:
                        for i in abonent1.service.all():
                            abonent2.service.add(i)

                    abonent2.login = abonent1.login
                    abonent2.dogowor = abonent1.dogowor
                    
                    
                    abonent2.b_internet += abonent1.b_internet
                    abonent2.b_kabel += abonent1.b_kabel
                    abonent2.b_alem += abonent1.b_alem
                    abonent2.b_telefon += abonent1.b_telefon
                    abonent2.b_slr += abonent1.b_slr
                    abonent2.b_kod += abonent1.b_kod
                    abonent2.b_zakaz += abonent1.b_zakaz
                    abonent2.b_prochee += abonent1.b_prochee
                    abonent2.b_dop_uslugi += abonent1.b_dop_uslugi
                    

                    abonent2.addDate = datetime.now()

                    abonent2.save()
                    
                    abonent1.surname = ''
                    abonent1.name = ''
                    abonent1.street = ''
                    abonent1.home = ''
                    abonent1.flat = ''
                    abonent1.sotowyy = ''
                    abonent1.is_enterprises = False
                    abonent1.alem = False
                    abonent1.alemCount = None
                    abonent1.alem_connect_date = None
                    abonent1.alem_on_date = None
                    abonent1.alem_off_date = None
                    abonent1.alem_disconnect_date = None
                    abonent1.account = None
                    abonent1.accountName = ''
                    abonent1.hb = None  
                    abonent1.internet_tarif = None
                    abonent1.internet_connect_date = None
                    abonent1.internet_disconnect_date = None
                    abonent1.abonplata = ''
                    abonent1.is_on = False
                    abonent1.is_on_date = None
                    abonent1.kabel_count = None
                    abonent1.connect_date = None
                    abonent1.kabel_comments = None
                    abonent1.ids = ''
                    abonent1.login = ''
                    abonent1.dogowor = ''
                    abonent1.addDate = None
                    abonent1.snyat_date = None
                    abonent1.snyat_bool = False

                    
                    if abonent1.service.all():
                        abonent1.service.clear()
                    abonent1.b_telefon = 0
                    abonent1.b_slr = 0
                    abonent1.b_kod = 0
                    abonent1.b_zakaz = 0
                    abonent1.b_prochee = 0
                    abonent1.b_dop_uslugi = 0
                    abonent1.b_internet = 0
                    abonent1.b_kabel = 0
                    abonent1.b_alem = 0
 
                    abonent1.save()
                    
                    



                    # refresh
                    abonent1 = UserTable.objects.get(number=number1, etrap=etrap1)
                    abonent2 = UserTable.objects.get(number=number2, etrap=etrap2)
                    context['abonent1'] = abonent1
                    context['abonent2'] = abonent2



                    messages.success(request, f"Успешно! перекидка данных")
                    StaffAction.objects.create(action='Перекидка',comment=f"{request.POST.get('comment')}\n\nполная перекидка с номера {abonent1.number}, {abonent1.etrap}, {abonent1.name}, {abonent1.surname}, {abonent1.street}, {abonent1.home} на номер {abonent2.number}, {abonent2.etrap}, {abonent2.name}, {abonent2.surname}, {abonent2.street}, {abonent2.home}", user=request.user)

                    # StaffAction.objects.create(action='Перекидка',comment=f"{request.POST.get('comment')}\n\nполная перекидка с номера {abonent1.number}, {abonent1.etrap} на номер {abonent2.number}, {abonent2.etrap}", user=request.user)


                else:
                    # перекидка даже если абонент 2 не свободный попросила махри
                    num1Edara = False
                    num2Edara = False
                    edara_to_nasel = False
                    nasel_to_edara = False
                    if request.POST.get('num2Edara') and request.POST.get('hOrb') == '':
                            messages.error(request, f"Выберите хоз или буджет")
                            return render(request, 'telekom/MATB/perekidka/perekidka.html', context)
                    num2hb = None if request.POST.get('hOrb') == '' else request.POST.get('hOrb')
                    if num2hb:
                        num2Edara = True
                    if request.POST.get('num2Edara') and abonent1.is_enterprises == False:
                        nasel_to_edara = True
                    elif request.POST.get('num2Edara') == None and abonent1.is_enterprises == True:
                        edara_to_nasel = True

                    # Если перекидка с предпр на насел или наоборот то сохранить в месячный отчет
                    if edara_to_nasel or nasel_to_edara:
                        if abonent1.etrap != abonent2.etrap:
                            try:
                                nachisleniyaOtchet1 = NachisleniyaOtchet.objects.get(year=current_year, month=month_word, etrap=abonent1.etrap)
                            except:
                                nachisleniyaOtchet1 = NachisleniyaOtchet.objects.create(year=current_year, month=month_word, etrap=abonent1.etrap)

                            try:
                                nachisleniyaOtchet2 = NachisleniyaOtchet.objects.get(year=current_year, month=month_word, etrap=abonent2.etrap)
                            except:
                                nachisleniyaOtchet2 = NachisleniyaOtchet.objects.create(year=current_year, month=month_word, etrap=abonent2.etrap)
                        else:
                            try:
                                nachisleniyaOtchet = NachisleniyaOtchet.objects.get(year=current_year, month=month_word, etrap=abonent1.etrap)
                            except:
                                nachisleniyaOtchet = NachisleniyaOtchet.objects.create(year=current_year, month=month_word, etrap=abonent1.etrap)


                        debit = 0
                        kredit = 0
                        if abonent1.b_telefon < 0:
                            debit += abs(abonent1.b_telefon)
                        else:
                            kredit += abonent1.b_telefon

                        if abonent1.b_slr < 0:
                            debit += abs(abonent1.b_slr)
                        else:
                            kredit += abonent1.b_slr

                        if abonent1.b_kod < 0:
                            debit += abs(abonent1.b_kod)
                        else:
                            kredit += abonent1.b_kod

                        if abonent1.b_zakaz < 0:
                            debit += abs(abonent1.b_zakaz)
                        else:
                            kredit += abonent1.b_zakaz

                        if abonent1.b_prochee < 0:
                            debit += abs(abonent1.b_prochee)
                        else:
                            kredit += abonent1.b_prochee

                        if abonent1.b_dop_uslugi < 0:
                            debit += abs(abonent1.b_dop_uslugi)
                        else:
                            kredit += abonent1.b_dop_uslugi

                        if abonent1.b_internet < 0:
                            debit += abs(abonent1.b_internet)
                        else:
                            kredit += abonent1.b_internet
                    
                        if abonent1.b_kabel < 0:
                            debit += abs(abonent1.b_kabel)
                        else:
                            kredit += abonent1.b_kabel

                        if abonent1.b_alem < 0:
                            debit += abs(abonent1.b_alem)
                        else:
                            kredit += abonent1.b_alem

                        if edara_to_nasel:
                            if abonent1.etrap != abonent2.etrap:
                                nachisleniyaOtchet2.perek_nasel_debit_plus += debit
                                nachisleniyaOtchet2.perek_nasel_kredit_plus += kredit

                                nachisleniyaOtchet1.perek_edara_debit_minus += debit
                                nachisleniyaOtchet1.perek_edara_kredit_minus += kredit
                                nachisleniyaOtchet1.save()
                                nachisleniyaOtchet2.save()
                            else:
                                nachisleniyaOtchet.perek_nasel_debit_plus += debit
                                nachisleniyaOtchet.perek_nasel_kredit_plus += kredit

                                nachisleniyaOtchet.perek_edara_debit_minus += debit
                                nachisleniyaOtchet.perek_edara_kredit_minus += kredit
                                nachisleniyaOtchet.save()
                                


                        elif nasel_to_edara:
                            if abonent1.etrap != abonent2.etrap:
                                nachisleniyaOtchet2.perek_edara_debit_plus += debit
                                nachisleniyaOtchet2.perek_edara_kredit_plus += kredit

                                nachisleniyaOtchet1.perek_nasel_debit_minus += debit
                                nachisleniyaOtchet1.perek_nasel_kredit_minus += kredit
                                nachisleniyaOtchet1.save()
                                nachisleniyaOtchet2.save()
                            else:
                                nachisleniyaOtchet.perek_nasel_debit_minus += debit
                                nachisleniyaOtchet.perek_nasel_kredit_minus += kredit

                                nachisleniyaOtchet.perek_edara_debit_plus += debit
                                nachisleniyaOtchet.perek_edara_kredit_plus += kredit
                                nachisleniyaOtchet.save()


                    # Сохранения в архив абонента 1

                    arhiwUser = UserTableArhiw.objects.create(
                    number = abonent1.number,
                    etrap = abonent1.etrap,
                    surname = abonent1.surname,
                    name = abonent1.name,
                    street = abonent1.street,
                    home = abonent1.home,
                    flat = abonent1.flat,
                    sotowyy = abonent1.sotowyy,
                    is_enterprises = abonent1.is_enterprises,
                    alem = abonent1.alem,
                    alemCount = abonent1.alemCount,
                    alem_connect_date = abonent1.alem_connect_date,
                    alem_on_date = abonent1.alem_on_date,
                    alem_off_date = abonent1.alem_off_date,
                    alem_disconnect_date = abonent1.alem_disconnect_date,
                    account = abonent1.account,
                    accountName = abonent1.accountName,
                    hb = abonent1.hb,     
                    internet_tarif = abonent1.internet_tarif,
                    internet_connect_date = abonent1.internet_connect_date,
                    internet_disconnect_date = abonent1.internet_disconnect_date,
                    abonplata = abonent1.abonplata,
                    is_on = abonent1.is_on,
                    is_on_date = abonent1.is_on_date,
                    kabel_count = abonent1.kabel_count,
                    connect_date = abonent1.connect_date,
                    kabel_comments = abonent1.kabel_comments,
                    ids = abonent1.ids,
                    login = abonent1.login,
                    dogowor = abonent1.dogowor,
                    b_internet = abonent1.b_internet,
                    b_kabel = abonent1.b_kabel,
                    b_alem = abonent1.b_alem,
                    b_telefon = abonent1.b_telefon,
                    b_slr = abonent1.b_slr,
                    b_kod = abonent1.b_kod,
                    b_zakaz = abonent1.b_zakaz,
                    b_prochee = abonent1.b_prochee,
                    b_dop_uslugi = abonent1.b_dop_uslugi,

                    s_internet = abonent1.s_internet,
                    s_kabel = abonent1.s_kabel,
                    s_alem = abonent1.s_alem,
                    s_telefon = abonent1.s_telefon,
                    s_slr = abonent1.s_slr,
                    s_kod = abonent1.s_kod,
                    s_zakaz = abonent1.s_zakaz,
                    s_prochee = abonent1.s_prochee,
                    s_dop_uslugi = abonent1.s_dop_uslugi,
                    
                    addDate = abonent1.addDate,
                    snyat_date = datetime.now(),
                    snyat_bool = True
                    )
                    if abonent1.service:
                        for i in abonent1.service.all():
                            arhiwUser.service.add(i)
                        arhiwUser.save()
                    
                  
                    if num2Edara == True:
                        abonent2.hb = HozOrBudjet.objects.get(name=num2hb)
                        abonent2.is_enterprises = True

                    
                    # Сохранения в архив абонента 2

                    arhiwUser2 = UserTableArhiw.objects.create(
                    number = abonent2.number,
                    etrap = abonent2.etrap,
                    surname = abonent2.surname,
                    name = abonent2.name,
                    street = abonent2.street,
                    home = abonent2.home,
                    flat = abonent2.flat,
                    sotowyy = abonent2.sotowyy,
                    is_enterprises = abonent2.is_enterprises,
                    alem = abonent2.alem,
                    alemCount = abonent2.alemCount,
                    alem_connect_date = abonent2.alem_connect_date,
                    alem_on_date = abonent2.alem_on_date,
                    alem_off_date = abonent2.alem_off_date,
                    alem_disconnect_date = abonent2.alem_disconnect_date,
                    account = abonent2.account,
                    accountName = abonent2.accountName,
                    hb = abonent2.hb,     
                    internet_tarif = abonent2.internet_tarif,
                    internet_connect_date = abonent2.internet_connect_date,
                    internet_disconnect_date = abonent2.internet_disconnect_date,
                    abonplata = abonent2.abonplata,
                    is_on = abonent2.is_on,
                    is_on_date = abonent2.is_on_date,
                    kabel_count = abonent2.kabel_count,
                    connect_date = abonent2.connect_date,
                    kabel_comments = abonent2.kabel_comments,
                    ids = abonent2.ids,
                    login = abonent2.login,
                    dogowor = abonent2.dogowor,
                    b_internet = abonent2.b_internet,
                    b_kabel = abonent2.b_kabel,
                    b_alem = abonent2.b_alem,
                    b_telefon = abonent2.b_telefon,
                    b_slr = abonent2.b_slr,
                    b_kod = abonent2.b_kod,
                    b_zakaz = abonent2.b_zakaz,
                    b_prochee = abonent2.b_prochee,
                    b_dop_uslugi = abonent2.b_dop_uslugi,

                    s_internet = abonent2.s_internet,
                    s_kabel = abonent2.s_kabel,
                    s_alem = abonent2.s_alem,
                    s_telefon = abonent2.s_telefon,
                    s_slr = abonent2.s_slr,
                    s_kod = abonent2.s_kod,
                    s_zakaz = abonent2.s_zakaz,
                    s_prochee = abonent2.s_prochee,
                    s_dop_uslugi = abonent2.s_dop_uslugi,
                    
                    addDate = abonent2.addDate,
                    snyat_date = datetime.now(),
                    snyat_bool = True
                    )
                    if abonent2.service:
                        for i in abonent2.service.all():
                            arhiwUser2.service.add(i)
                        arhiwUser2.save()
                    
                  
                    if num2Edara == True:
                        abonent2.hb = HozOrBudjet.objects.get(name=num2hb)
                        abonent2.is_enterprises = True

                    InterpayPerekidkaBilling.objects.create(
                        number1=abonent1.number,
                        etrap1=abonent1.etrap,
                        surname1=abonent1.surname,
                        name1=abonent1.name,
                        abonent1_pk=abonent1.pk,

                        internet1 = abonent1.b_internet,
                        alem1 = abonent1.b_alem,
                        telefon1 = abonent1.b_telefon,
                        slr1 = abonent1.b_slr,
                        kod1 = abonent1.b_kod,
                        zakaz1 = abonent1.b_zakaz,
                        prochee1 = abonent1.b_prochee,
                        dop_uslugi1 =abonent1.b_dop_uslugi,
                        kabel1 =abonent1.b_kabel,
                        abonent2_pk=abonent2.pk,

                        number2=abonent2.number,
                        etrap2=abonent2.etrap,
                        surname2=abonent2.surname,
                        name2=abonent2.name,

                        alem2=abonent1.b_alem,
                        internet2 = abonent1.b_internet,
                        telefon2 = abonent1.b_telefon,
                        slr2 = abonent1.b_slr,
                        kod2 = abonent1.b_kod,
                        zakaz2 = abonent1.b_zakaz,
                        prochee2 = abonent1.b_prochee,
                        dop_uslugi2 =abonent1.b_dop_uslugi,
                        kabel2 =abonent1.b_kabel,

                        mtbUsername = request.user.username,
                        mtbEtrap = log,
                        date=datetime.now()
                        )
                    
                    PerekidkaInfo.objects.create(
                        user1Number = abonent1.number,
                        user1Etrap = abonent1.etrap,
                        user2Number = abonent2.number,
                        user2Etrap = abonent2.etrap,
                        user1_is_enterprises = abonent1.is_enterprises,
                        user2_is_enterprises = abonent2.is_enterprises,

                        telefon1 = abonent1.b_telefon,
                        internet1 = abonent1.b_internet,
                        kabel1 = abonent1.b_kabel,
                        alem1 = abonent1.b_alem,
                        slr1 = abonent1.b_slr,
                        kod1 = abonent1.b_kod,
                        zakaz1 = abonent1.b_zakaz,
                        prochee1 = abonent1.b_prochee,
                        dop_uslugi1 = abonent1.b_dop_uslugi,

                        telefon2 = abonent1.b_telefon,
                        internet2 = abonent1.b_internet,
                        kabel2 = abonent1.b_kabel,
                        alem2 = abonent1.b_alem,
                        slr2 = abonent1.b_slr,
                        kod2 = abonent1.b_kod,
                        zakaz2 = abonent1.b_zakaz,
                        prochee2 = abonent1.b_prochee,
                        dop_uslugi2 = abonent1.b_dop_uslugi,
                        comment=f"{request.POST.get('comment')}\n\nполная перекидка с номера {abonent1.number}, {abonent1.etrap} на номер {abonent2.number}, {abonent2.etrap}",
                        operator = request.user
                    )

                    abonent2.surname = abonent1.surname
                    abonent2.name = abonent1.name
                    abonent2.street = abonent1.street
                    abonent2.home = abonent1.home
                    abonent2.flat = abonent1.flat
                    abonent2.sotowyy = abonent1.sotowyy
                    # abonent2.is_enterprises = abonent1.is_enterprises

                    abonent2.alem = abonent1.alem
                    abonent2.alemCount = abonent1.alemCount
                    abonent2.alem_connect_date = abonent1.alem_connect_date
                    abonent2.alem_on_date = abonent1.alem_on_date
                    abonent2.alem_off_date = abonent1.alem_off_date
                    abonent2.alem_disconnect_date = abonent1.alem_disconnect_date

                    if abonent1.is_enterprises:
                        abonent2.is_enterprises=True
                        abonent2.account = abonent1.account
                        abonent2.hb = HozOrBudjet.objects.get(name=abonent1.hb.name)
                    abonent2.abonplata = abonent1.abonplata

                    abonent2.internet_tarif = abonent1.internet_tarif
                    abonent2.internet_connect_date = abonent1.internet_connect_date
                    abonent2.internet_disconnect_date = abonent1.internet_disconnect_date
                        
                    # Кабель махри не перекидывает его перекидывает Бахбит и поэтому удаляем эту опцию с перекидки (но если обязаности за изменения перейдет мехри то надо убрать комментарии)
                    # abonent2.is_on = abonent1.is_on
                    # abonent2.is_on_date = abonent1.is_on_date
                    # abonent2.kabel_count = abonent1.kabel_count
                    # abonent2.connect_date = abonent1.connect_date
                    # abonent2.kabel_comments = abonent1.kabel_comments
                    # abonent2.ids = abonent1.ids
                    
                    if abonent1.service:
                        for i in abonent1.service.all():
                            abonent2.service.add(i)

                    abonent2.login = abonent1.login
                    abonent2.dogowor = abonent1.dogowor
                    
                    
                    abonent2.b_internet += abonent1.b_internet
                    abonent2.b_kabel += abonent1.b_kabel
                    abonent2.b_alem += abonent1.b_alem
                    abonent2.b_telefon += abonent1.b_telefon
                    abonent2.b_slr += abonent1.b_slr
                    abonent2.b_kod += abonent1.b_kod
                    abonent2.b_zakaz += abonent1.b_zakaz
                    abonent2.b_prochee += abonent1.b_prochee
                    abonent2.b_dop_uslugi += abonent1.b_dop_uslugi
                    

                    abonent2.addDate = datetime.now()

                    abonent2.save()
                    
                    abonent1.surname = ''
                    abonent1.name = ''
                    abonent1.street = ''
                    abonent1.home = ''
                    abonent1.flat = ''
                    abonent1.sotowyy = ''
                    abonent1.is_enterprises = False
                    abonent1.alem = False
                    abonent1.alemCount = None
                    abonent1.alem_connect_date = None
                    abonent1.alem_on_date = None
                    abonent1.alem_off_date = None
                    abonent1.alem_disconnect_date = None
                    abonent1.account = None
                    abonent1.accountName = ''
                    abonent1.hb = None  
                    abonent1.internet_tarif = None
                    abonent1.internet_connect_date = None
                    abonent1.internet_disconnect_date = None
                    abonent1.abonplata = ''

                    # Кабель махри не перекидывает его перекидывает Бахбит и поэтому удаляем эту опцию с перекидки (но если обязаности за изменения перейдет мехри то надо убрать комментарии)
                    # abonent1.is_on = False
                    # abonent1.is_on_date = None
                    # abonent1.kabel_count = None
                    # abonent1.connect_date = None
                    # abonent1.kabel_comments = None
                    # abonent1.ids = ''

                    abonent1.login = ''
                    abonent1.dogowor = ''
                    abonent1.addDate = None
                    abonent1.snyat_date = None
                    abonent1.snyat_bool = False

                    
                    if abonent1.service.all():
                        abonent1.service.clear()
                    abonent1.b_telefon = 0
                    abonent1.b_slr = 0
                    abonent1.b_kod = 0
                    abonent1.b_zakaz = 0
                    abonent1.b_prochee = 0
                    abonent1.b_dop_uslugi = 0
                    abonent1.b_internet = 0
                    abonent1.b_kabel = 0
                    abonent1.b_alem = 0
 
                    abonent1.save()

                    # refresh
                    abonent1 = UserTable.objects.get(number=number1, etrap=etrap1)
                    abonent2 = UserTable.objects.get(number=number2, etrap=etrap2)
                    context['abonent1'] = abonent1
                    context['abonent2'] = abonent2



                    messages.success(request, f"Успешно! перекидка данных")
                    StaffAction.objects.create(action='Перекидка',comment=f"{request.POST.get('comment')}\n\nполная перекидка с номера {abonent1.number}, {abonent1.etrap}, {abonent1.name}, {abonent1.surname}, {abonent1.street}, {abonent1.home} на номер {abonent2.number}, {abonent2.etrap}, {abonent2.name}, {abonent2.surname}, {abonent2.street}, {abonent2.home}", user=request.user)

                    

                    
                
        # Перекидка только баланса
        else:
            if request.POST.get('comment') == '':
                messages.error(request, 'Добавьте комментарий')
            else:
                er = False
                mes = 'Перекидка баланса: \n'

                perTelefonM = 0
                perSlrM = 0
                perKodM = 0
                perZakazM = 0
                perProcheeM = 0
                perUslugiM = 0
                perIntM = 0
                perKabM = 0
                perAlemM = 0

                perTelefonP = 0
                perSlrP = 0
                perKodP = 0
                perZakazP = 0
                perProcheeP = 0
                perUslugiP = 0
                perIntP = 0
                perKabP = 0
                perAlemP = 0

                if request.POST.get('perekidkaAbonplata') != '':
                    try:
                        telefon = float(request.POST.get('perekidkaAbonplata'))
                        telefonTo = request.POST.get('abonplataCol')
                    except:
                        er = 'Ошибка в ценах перекидки'
                        telefon = False
                else:
                    telefon = False
                    
                if request.POST.get('perekidkaSlr') != '':
                    try:
                        slr = float(request.POST.get('perekidkaSlr'))
                        slrTo = request.POST.get('slrCol')
                    except:
                        er = 'Ошибка! Возмошно вы ввели некорректные данные в ценах'
                        slr = False
                else:
                    slr = False

                if request.POST.get('perekidkaKod') != '':
                    try:
                        kod = float(request.POST.get('perekidkaKod'))
                        kodTo = request.POST.get('kodCol')
                    except:
                        er = 'Ошибка! Возмошно вы ввели некорректные данные в ценах'
                        kod = False
                else:
                    kod = False

                if request.POST.get('perekidkaZakaz') != '':
                    try:
                        zakaz = float(request.POST.get('perekidkaZakaz'))
                        zakazTo = request.POST.get('zakazCol')
                    except:
                        er = 'Ошибка! Возмошно вы ввели некорректные данные в ценах'
                        zakaz = False
                else:
                    zakaz = False

                if request.POST.get('perekidkaProchee') != '':
                    try:
                        prochee = float(request.POST.get('perekidkaProchee'))
                        procheeTo = request.POST.get('procheeCol')
                    except:
                        er = 'Ошибка! Возмошно вы ввели некорректные данные в ценах'
                        prochee = False
                else:
                    prochee = False

                if request.POST.get('perekidkaDop_uslugi') != '':
                    try:
                        dop_uslugi = float(request.POST.get('perekidkaDop_uslugi'))
                        dop_uslugiTo = request.POST.get('dop_uslugiCol')
                    except:
                        er = 'Ошибка! Возмошно вы ввели некорректные данные в ценах'
                        dop_uslugi = False
                else:
                    dop_uslugi = False

                if request.POST.get('perekidkaInternet') != '':
                    try:
                        internet = float(request.POST.get('perekidkaInternet'))
                        internetTo = request.POST.get('internetCol')
                    except:
                        er = 'Ошибка! Возмошно вы ввели некорректные данные в ценах'
                        internet = False
                else:
                    internet = False

                if request.POST.get('perekidkaKabel') != '':
                    try:
                        kabel = float(request.POST.get('perekidkaKabel'))
                        kabelTo = request.POST.get('kabelCol')
                    except:
                        er = 'Ошибка! Возмошно вы ввели некорректные данные в ценах'
                        kabel = False
                else:
                    kabel = False


                if request.POST.get('perekidkaAlem') != '':
                    try:
                        alem = float(request.POST.get('perekidkaAlem'))
                        alemTo = request.POST.get('alemCol')
                    except:
                        er = 'Ошибка! Возмошно вы ввели некорректные данные в ценах'
                        alem = False
                else:
                    alem = False

                if er:
                    messages.error(request, er)
                else:
                    

                    # Если номер1 и номер2 это один и тот же абонент
                    if (abonent1.pk == abonent2.pk):

                        if kabel:
                            messages.error(request, f"Все перекидки с кабеля делаются на KabelTVNew")
                            # refresh data
                            abonent1 = UserTable.objects.get(number=number1, etrap=etrap1)
                            abonent2 = UserTable.objects.get(number=number2, etrap=etrap2)
                            context['abonent1'] = abonent1
                            context['abonent2'] = abonent2
                            return render(request, 'telekom/MATB/perekidka/perekidka.html', context)

                        if telefonTo == 'Кабель' or alemTo == 'Кабель' or internetTo == 'Кабель' or dop_uslugiTo == 'Кабель' or procheeTo == 'Кабель' or zakazTo == 'Кабель' or kodTo == 'Кабель' or slrTo == 'Кабель':
                            try:
                                kabelTvUser = KabelTvNew.objects.get(number=number2)
                            except:
                                messages.error(request, f"Нет номера {number2} в базе Кабель TV")
                                # refresh data
                                abonent1 = UserTable.objects.get(number=number1, etrap=etrap1)
                                abonent2 = UserTable.objects.get(number=number2, etrap=etrap2)
                                context['abonent1'] = abonent1
                                context['abonent2'] = abonent2
                                return render(request, 'telekom/MATB/perekidka/perekidka.html', context)
                        else:
                            kabelTvUser = False

                        # №№№        
                        perekidkaInfo = PerekidkaInfo(
                            user1Number = abonent1.number,
                            user1Etrap = abonent1.etrap,
                            user2Number = abonent1.number,
                            user2Etrap = abonent1.etrap,
                            user1_is_enterprises = abonent1.is_enterprises,
                            user2_is_enterprises = abonent1.is_enterprises
                        )
                        # №№№#

                        kabelCommentStr = ''
                        kabelCommentObj = False

                        if telefon:
                            perekidkaInfo.telefon1 = telefon
                            abonent1.b_telefon -= telefon
                            if telefonTo == 'Абонплата':
                                abonent1.b_telefon += telefon
                                mes += f'c Абон: {telefon} на абон; \n'
                                perTelefonM -= telefon
                                perTelefonP += telefon
                                perekidkaInfo.telefon2 += telefon
                            elif telefonTo == 'Слр':
                                abonent1.b_slr += telefon
                                mes += f'c Абон: {telefon} на слр; \n'
                                perTelefonM -= telefon
                                perSlrP += telefon
                                perekidkaInfo.slr2 += telefon
                            elif telefonTo == 'Код':
                                abonent1.b_kod += telefon
                                mes += f'c Абон: {telefon} на код; \n'
                                perTelefonM -= telefon
                                perKodP += telefon
                                perekidkaInfo.kod2 += telefon
                            elif telefonTo == 'Заказ':
                                abonent1.b_zakaz += telefon
                                mes += f'c Абон: {telefon} на заказ; \n'
                                perTelefonM -= telefon
                                perZakazP += telefon
                                perekidkaInfo.zakaz2 += telefon
                            elif telefonTo == 'Прочее':
                                abonent1.b_prochee += telefon
                                mes += f'c Абон: {telefon} на прочее; \n'
                                perTelefonM -= telefon
                                perProcheeP += telefon
                                perekidkaInfo.prochee2 += telefon
                            elif telefonTo == 'Доп.услуги':
                                abonent1.b_dop_uslugi += telefon
                                mes += f'c Абон: {telefon} на доп. ус; \n'
                                perTelefonM -= telefon
                                perUslugiP += telefon
                                perekidkaInfo.dop_uslugi2 += telefon
                            elif telefonTo == 'Интернет':
                                abonent1.b_internet += telefon
                                mes += f'c Абон: {telefon} на internet; \n'
                                perTelefonM -= telefon
                                perIntP += telefon
                                perekidkaInfo.internet2 += telefon
                            elif telefonTo == 'Кабель':
                                # abonent1.b_kabel += telefon
                                kabelTvUser.balance += telefon  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с telefon на kabel сумма {telefon}
                                    """
                                else:
                                    kabelCommentStr += f"""с telefon на kabel сумма {telefon}
                                    """
                                mes += f'c Абон: {telefon} на кабель; \n'
                                perTelefonM -= telefon
                                perKabP += telefon
                                perekidkaInfo.kabel2 += telefon
                            elif telefonTo == 'Alem':
                                abonent1.b_alem += telefon
                                mes += f'c Абон: {telefon} на alem; \n'
                                perTelefonM -= telefon
                                perAlemP += telefon
                                perekidkaInfo.alem2 += telefon
                            
                        if slr:
                            perekidkaInfo.slr1 = slr
                            abonent1.b_slr -= slr
                            if slrTo == 'Абонплата':
                                abonent1.b_telefon += slr
                                mes += f'c слр: {slr} на абон; \n'
                                perSlrM -= slr
                                perTelefonP += slr
                                perekidkaInfo.telefon2 += slr
                            elif slrTo == 'Слр':
                                abonent1.b_slr += slr
                                mes += f'c слр: {slr} на слр; \n'
                                perSlrM -= slr
                                perSlrP += slr
                                perekidkaInfo.slr2 += slr
                            elif slrTo == 'Код':
                                abonent1.b_kod += slr
                                mes += f'c слр: {slr} на код; \n'
                                perSlrM -= slr
                                perKodP += slr
                                perekidkaInfo.kod2 += slr
                            elif slrTo == 'Заказ':
                                abonent1.b_zakaz += slr
                                mes += f'c слр: {slr} на заказ; \n'
                                perSlrM -= slr
                                perZakazP += slr
                                perekidkaInfo.zakaz2 += slr
                            elif slrTo == 'Прочее':
                                abonent1.b_prochee += slr
                                mes += f'c слр: {slr} на прочее; \n'
                                perSlrM -= slr
                                perProcheeP += slr
                                perekidkaInfo.prochee2 += slr
                            elif slrTo == 'Доп.услуги':
                                abonent1.b_dop_uslugi += slr
                                mes += f'c слр: {slr} на доп. услуги; \n'
                                perSlrM -= slr
                                perUslugiP += slr
                                perekidkaInfo.dop_uslugi2 += slr
                            elif slrTo == 'Интернет':
                                abonent1.b_internet += slr
                                mes += f'c слр: {slr} на интернет; \n'
                                perSlrM -= slr
                                perIntP += slr
                                perekidkaInfo.internet2 += slr
                            elif slrTo == 'Кабель':
                                # abonent1.b_kabel += slr
                                kabelTvUser.balance += slr  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с slr на kabel сумма {slr}
                                    """
                                else:
                                    kabelCommentStr += f"""с slr на kabel сумма {slr}
                                    """
                                mes += f'c слр: {slr} на кабель; \n'
                                perSlrM -= slr
                                perKabP += slr
                                perekidkaInfo.kabel2 += slr
                            elif slrTo == 'Alem':
                                abonent1.b_alem += slr
                                mes += f'c слр: {slr} на alem; \n'
                                perSlrM -= slr
                                perAlemP += slr
                                perekidkaInfo.alem2 += slr
                        
                        if kod:
                            perekidkaInfo.kod1 = kod
                            abonent1.b_kod -= kod
                            if kodTo == 'Абонплата':
                                abonent1.b_telefon += kod
                                mes += f'c код: {kod} на абон; \n'
                                perKodM -= kod
                                perTelefonP += kod
                                perekidkaInfo.telefon2 += kod
                            elif kodTo == 'Слр':
                                abonent1.b_slr += kod
                                mes += f'c код: {kod} на слр; \n'
                                perKodM -= kod
                                perSlrP += kod
                                perekidkaInfo.slr2 += kod
                            elif kodTo == 'Код':
                                abonent1.b_kod += kod
                                mes += f'c код: {kod} на код; \n'
                                perKodM -= kod
                                perKodP += kod
                                perekidkaInfo.kod2 += kod
                            elif kodTo == 'Заказ':
                                abonent1.b_zakaz += kod
                                mes += f'c код: {kod} на заказ; \n'
                                perKodM -= kod
                                perZakazP += kod
                                perekidkaInfo.zakaz2 += kod
                            elif kodTo == 'Прочее':
                                abonent1.b_prochee += kod
                                mes += f'c код: {kod} на прочее; \n'
                                perKodM -= kod
                                perProcheeP += kod
                                perekidkaInfo.prochee2 += kod
                            elif kodTo == 'Доп.услуги':
                                abonent1.b_dop_uslugi += kod
                                mes += f'c код: {kod} на доп. ус.; \n'
                                perKodM -= kod
                                perUslugiP += kod
                                perekidkaInfo.dop_uslugi += kod
                            elif kodTo == 'Интернет':
                                abonent1.b_internet += kod
                                mes += f'c код: {kod} на инт; \n'
                                perKodM -= kod
                                perIntP += kod
                                perekidkaInfo.internet2 += kod
                            elif kodTo == 'Кабель':
                                # abonent1.b_kabel += kod
                                kabelTvUser.balance += kod  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с kod на kabel сумма {kod}
                                    """
                                else:
                                    kabelCommentStr += f"""с kod на kabel сумма {kod}
                                    """
                                mes += f'c код: {kod} на кабель; \n'
                                perKodM -= kod
                                perKabP += kod
                                perekidkaInfo.kabel2 += kod
                            elif kodTo == 'Alem':
                                abonent1.b_alem += kod
                                mes += f'c код: {kod} на алем; \n'
                                perKodM -= kod
                                perAlemP += kod
                                perekidkaInfo.alem2 += kod
                    
                        if zakaz:
                            perekidkaInfo.zakaz1 = zakaz
                            abonent1.b_zakaz -= zakaz
                            if zakazTo == 'Абонплата':
                                abonent1.b_telefon += zakaz
                                mes += f'c заказ: {zakaz} на абон; \n'
                                perZakazM -= zakaz
                                perTelefonP += zakaz
                                perekidkaInfo.telefon2 += zakaz
                            elif zakazTo == 'Слр':
                                abonent1.b_slr += zakaz
                                mes += f'c заказ: {zakaz} на слр; \n'
                                perZakazM -= zakaz
                                perSlrP += zakaz
                                perekidkaInfo.slr2 += zakaz
                            elif zakazTo == 'Код':
                                abonent1.b_kod += zakaz
                                mes += f'c заказ: {zakaz} на код; \n'
                                perZakazM -= zakaz
                                perKodP += zakaz
                                perekidkaInfo.kod2 += zakaz
                            elif zakazTo == 'Заказ':
                                abonent1.b_zakaz += zakaz
                                mes += f'c заказ: {zakaz} на заказ; \n'
                                perZakazM -= zakaz
                                perZakazP += zakaz
                                perekidkaInfo.zakaz2 += zakaz
                            elif zakazTo == 'Прочее':
                                abonent1.b_prochee += zakaz
                                mes += f'c заказ: {zakaz} на прочее; \n'
                                perZakazM -= zakaz
                                perProcheeP += zakaz
                                perekidkaInfo.prochee2 += zakaz
                            elif zakazTo == 'Доп.услуги':
                                abonent1.b_dop_uslugi += zakaz
                                mes += f'c заказ: {zakaz} на доп. ус; \n'
                                perZakazM -= zakaz
                                perUslugiP += zakaz
                                perekidkaInfo.dop_uslugi2 += zakaz
                            elif zakazTo == 'Интернет':
                                abonent1.b_internet += zakaz
                                mes += f'c заказ: {zakaz} на инт; \n'
                                perZakazM -= zakaz
                                perIntP += zakaz
                                perekidkaInfo.internet2 += zakaz
                            elif zakazTo == 'Кабель':
                                # abonent1.b_kabel += zakaz
                                kabelTvUser.balance += zakaz  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с zakaz на kabel сумма {zakaz}
                                    """
                                else:
                                    kabelCommentStr += f"""с zakaz на kabel сумма {zakaz}
                                    """
                                mes += f'c заказ: {zakaz} на кабель; \n'
                                perZakazM -= zakaz
                                perKabP += zakaz
                                perekidkaInfo.kabel2 += zakaz
                            elif zakazTo == 'Alem':
                                abonent1.b_alem += zakaz
                                mes += f'c заказ: {zakaz} на алем; \n'
                                perZakazM -= zakaz
                                perAlemP += zakaz
                                perekidkaInfo.alem2 += zakaz
                        
                        if prochee:
                            perekidkaInfo.prochee1 = prochee
                            abonent1.b_prochee -= prochee
                            if procheeTo == 'Абонплата':
                                abonent1.b_telefon += prochee
                                mes += f'c прочее: {prochee} на абон; \n'
                                perProcheeM -= prochee
                                perTelefonP += prochee
                                perekidkaInfo.telefon2 += prochee
                            elif procheeTo == 'Слр':
                                abonent1.b_slr += prochee
                                mes += f'c прочее: {prochee} на слр; \n'
                                perProcheeM -= prochee
                                perSlrP += prochee
                                perekidkaInfo.slr2 += prochee
                            elif procheeTo == 'Код':
                                abonent1.b_kod += prochee
                                mes += f'c прочее: {prochee} на код; \n'
                                perProcheeM -= prochee
                                perKodP += prochee
                                perekidkaInfo.kod2 += prochee
                            elif procheeTo == 'Заказ':
                                abonent1.b_zakaz += prochee
                                mes += f'c прочее: {prochee} на заказ; \n'
                                perProcheeM -= prochee
                                perZakazP += prochee
                                perekidkaInfo.zakaz2 += prochee
                            elif procheeTo == 'Прочее':
                                abonent1.b_prochee += prochee
                                mes += f'c прочее: {prochee} на прочее; \n'
                                perProcheeM -= prochee
                                perProcheeP += prochee
                                perekidkaInfo.prochee2 += prochee
                            elif procheeTo == 'Доп.услуги':
                                abonent1.b_dop_uslugi += prochee
                                mes += f'c прочее: {prochee} на доп. ус.; \n'
                                perProcheeM -= prochee
                                perUslugiP += prochee
                                perekidkaInfo.dop_uslugi2 += prochee
                            elif procheeTo == 'Интернет':
                                abonent1.b_internet += prochee
                                mes += f'c прочее: {prochee} на инт; \n'
                                perProcheeM -= prochee
                                perIntP += prochee
                                perekidkaInfo.internet2 += prochee
                            elif procheeTo == 'Кабель':
                                # abonent1.b_kabel += prochee
                                kabelTvUser.balance += prochee  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с prochee на kabel сумма {prochee}
                                    """
                                else:
                                    kabelCommentStr += f"""с prochee на kabel сумма {prochee}
                                    """
                                mes += f'c прочее: {prochee} на кабель; \n'
                                perProcheeM -= prochee
                                perKabP += prochee
                                perekidkaInfo.kabel2 += prochee
                            elif procheeTo == 'Alem':
                                abonent1.b_alem += prochee
                                mes += f'c прочее: {prochee} на алем; \n'
                                perProcheeM -= prochee
                                perAlemP += prochee
                                perekidkaInfo.alem2 += prochee
                        
                        if dop_uslugi:
                            perekidkaInfo.dop_uslugi1 = dop_uslugi
                            abonent1.b_dop_uslugi -= dop_uslugi
                            if dop_uslugiTo == 'Абонплата':
                                abonent1.b_telefon += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на абон; \n'
                                perUslugiM -= dop_uslugi
                                perTelefonP += dop_uslugi
                                perekidkaInfo.telefon2 += dop_uslugi
                            elif dop_uslugiTo == 'Слр':
                                abonent1.b_slr += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на слр; \n'
                                perUslugiM -= dop_uslugi
                                perSlrP += dop_uslugi
                                perekidkaInfo.slr2 += dop_uslugi
                            elif dop_uslugiTo == 'Код':
                                abonent1.b_kod += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на код; \n'
                                perUslugiM -= dop_uslugi
                                perKodP += dop_uslugi
                                perekidkaInfo.kod2 += dop_uslugi
                            elif dop_uslugiTo == 'Заказ':
                                abonent1.b_zakaz += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на заказ; \n'
                                perUslugiM -= dop_uslugi
                                perZakazM += dop_uslugi
                                perekidkaInfo.zakaz2 += dop_uslugi
                            elif dop_uslugiTo == 'Прочее':
                                abonent1.b_prochee += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на прочее; \n'
                                perUslugiM -= dop_uslugi
                                perProcheeP += dop_uslugi
                                perekidkaInfo.prochee2 += dop_uslugi
                            elif dop_uslugiTo == 'Доп.услуги':
                                abonent1.b_dop_uslugi += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на доп. ус; \n'
                                perUslugiM -= dop_uslugi
                                perUslugiP += dop_uslugi
                                perekidkaInfo.dop_uslugi2 += dop_uslugi
                            elif dop_uslugiTo == 'Интернет':
                                abonent1.b_internet += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на инт; \n'
                                perUslugiM -= dop_uslugi
                                perIntP += dop_uslugi
                                perekidkaInfo.internet2 += dop_uslugi
                            elif dop_uslugiTo == 'Кабель':
                                # abonent1.b_kabel += dop_uslugi
                                kabelTvUser.balance += dop_uslugi  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с dop_uslugi на kabel сумма {dop_uslugi}
                                    """
                                else:
                                    kabelCommentStr += f"""с dop_uslugi на kabel сумма {dop_uslugi}
                                    """ 
                                mes += f'c доп. ус: {dop_uslugi} на кабель; \n'
                                perUslugiM -= dop_uslugi
                                perKabP += dop_uslugi
                                perekidkaInfo.kabel2 += dop_uslugi
                            elif dop_uslugiTo == 'Alem':
                                abonent1.b_alem += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на алем; \n'
                                perUslugiM -= dop_uslugi
                                perAlemP += dop_uslugi
                                perekidkaInfo.alem2 += dop_uslugi
                    
                        if internet:
                            perekidkaInfo.internet1 = internet
                            abonent1.b_internet -= internet
                            if internetTo == 'Абонплата':
                                abonent1.b_telefon += internet
                                mes += f'c интернет: {internet} на абон; \n'
                                perIntM -= internet
                                perTelefonP += internet
                                perekidkaInfo.telefon2 += internet
                            elif internetTo == 'Слр':
                                abonent1.b_slr += internet
                                mes += f'c интернет: {internet} на слр; \n'
                                perIntM -= internet
                                perSlrP += internet
                                perekidkaInfo.slr2 += internet
                            elif internetTo == 'Код':
                                abonent1.b_kod += internet
                                mes += f'c интернет: {internet} на код; \n'
                                perIntM -= internet
                                perKodP += internet
                                perekidkaInfo.kod2 += internet
                            elif internetTo == 'Заказ':
                                abonent1.b_zakaz += internet
                                mes += f'c интернет: {internet} на заказ; \n'
                                perIntM -= internet
                                perZakazP += internet
                                perekidkaInfo.zakaz2 += internet
                            elif internetTo == 'Прочее':
                                abonent1.b_prochee += internet
                                mes += f'c интернет: {internet} на прочее; \n'
                                perIntM -= internet
                                perProcheeP += internet
                                perekidkaInfo.prochee2 += internet
                            elif internetTo == 'Доп.услуги':
                                abonent1.b_dop_uslugi += internet
                                mes += f'c интернет: {internet} на доп. ус; \n'
                                perIntM -= internet
                                perUslugiP += internet
                                perekidkaInfo.dop_uslugi2 += internet
                            elif internetTo == 'Интернет':
                                abonent1.b_internet += internet
                                mes += f'c интернет: {internet} на интернет; \n'
                                perIntM -= internet
                                perIntP += internet
                                perekidkaInfo.internet2 += internet
                            elif internetTo == 'Кабель':
                                # abonent1.b_kabel += internet
                                kabelTvUser.balance += internet  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с internet на kabel сумма {internet}
                                    """
                                else:
                                    kabelCommentStr += f"""с internet на kabel сумма {internet}
                                    """ 
                                mes += f'c интернет: {internet} на кабель; \n'
                                perIntM -= internet
                                perKabP += internet
                                perekidkaInfo.kabel2 += internet
                            elif internetTo == 'Alem':
                                abonent1.b_alem += internet
                                mes += f'c интернет: {internet} на алем; \n'
                                perIntM -= internet
                                perAlemP += internet
                                perekidkaInfo.alem2 += internet
                        
                        if kabel:
                            pass
                            # abonent1.b_kabel -= kabel
                            # if kabelTo == 'Абонплата':
                            #     abonent1.b_telefon += kabel
                            #     mes += f'c кабель: {kabel} на абон; \n'
                            #     perKabM -= kabel
                            #     perTelefonP += kabel
                            #     perekidkaInfo.telefon2 = kabel
                            # elif kabelTo == 'Слр':
                            #     abonent1.b_slr += kabel
                            #     mes += f'c кабель: {kabel} на слр; \n'
                            #     perKabM -= kabel
                            #     perSlrP += kabel
                            #     perekidkaInfo.slr2 = kabel
                            # elif kabelTo == 'Код':
                            #     abonent1.b_kod += kabel
                            #     mes += f'c кабель: {kabel} на код; \n'
                            #     perKabM -= kabel
                            #     perKodP += kabel
                            #     perekidkaInfo.kod2 = kabel
                            # elif kabelTo == 'Заказ':
                            #     abonent1.b_zakaz += kabel
                            #     mes += f'c кабель: {kabel} на заказ; \n'
                            #     perKabM -= kabel
                            #     perZakazP += kabel
                            #     perekidkaInfo.zakaz2 = kabel
                            # elif kabelTo == 'Прочее':
                            #     abonent1.b_prochee += kabel
                            #     mes += f'c кабель: {kabel} на прочее; \n'
                            #     perKabM -= kabel
                            #     perProcheeP += kabel
                            #     perekidkaInfo.prochee2 = kabel
                            # elif kabelTo == 'Доп.услуги':
                            #     abonent1.b_dop_uslugi += kabel
                            #     mes += f'c кабель: {kabel} на доп. ус; \n'
                            #     perKabM -= kabel
                            #     perUslugiP += kabel
                            #     perekidkaInfo.dop_uslugi2 = kabel
                            # elif kabelTo == 'Интернет':
                            #     abonent1.b_internet += kabel
                            #     mes += f'c кабель: {kabel} на инт; \n'
                            #     perKabM -= kabel
                            #     perIntP += kabel
                            #     perekidkaInfo.internet2 = kabel
                            # elif kabelTo == 'Кабель':
                            #     abonent1.b_kabel += kabel
                            #     mes += f'c кабель: {kabel} на кабель; \n'
                            #     perKabM -= kabel
                            #     perKabP += kabel
                            #     perekidkaInfo.kabel2 = kabel
                            # elif kabelTo == 'Alem':
                            #     abonent1.b_alem += kabel
                            #     mes += f'c кабель: {kabel} на алем; \n'
                            #     perKabM -= kabel
                            #     perAlemP += kabel
                            #     perekidkaInfo.alem2 = kabel
                    
                        if alem:
                            perekidkaInfo.alem1 = alem
                            abonent1.b_alem -= alem
                            if alemTo == 'Абонплата':
                                abonent1.b_telefon += alem
                                mes += f'c alem: {alem} на абон; \n'
                                perAlemM -= alem
                                perTelefonP += alem
                                perekidkaInfo.telefon2 += alem
                            elif alemTo == 'Слр':
                                abonent1.b_slr += alem
                                mes += f'c alem: {alem} на слр; \n'
                                perAlemM -= alem
                                perSlrP += alem
                                perekidkaInfo.slr2 += alem
                            elif alemTo == 'Код':
                                abonent1.b_kod += alem
                                mes += f'c alem: {alem} на код; \n'
                                perAlemM -= alem
                                perKodP += alem
                                perekidkaInfo.kod2 += alem
                            elif alemTo == 'Заказ':
                                abonent1.b_zakaz += alem
                                mes += f'c alem: {alem} на заказ; \n'
                                perAlemM -= alem
                                perZakazP += alem
                                perekidkaInfo.zakaz2 += alem
                            elif alemTo == 'Прочее':
                                abonent1.b_prochee += alem
                                mes += f'c alem: {alem} на прочее; \n'
                                perAlemM -= alem
                                perProcheeP += alem
                                perekidkaInfo.prochee2 += alem
                            elif alemTo == 'Доп.услуги':
                                abonent1.b_dop_uslugi += alem
                                mes += f'c alem: {alem} на доп. ус.; \n'
                                perAlemM -= alem
                                perUslugiP += alem
                                perekidkaInfo.dop_uslugi2 += alem
                            elif alemTo == 'Интернет':
                                abonent1.b_internet += alem
                                mes += f'c alem: {alem} на инт; \n'
                                perAlemM -= alem
                                perIntP += alem
                                perekidkaInfo.internet2 += alem
                            elif alemTo == 'Кабель':
                                # abonent1.b_kabel += alem
                                kabelTvUser.balance += alem  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с alem на kabel сумма {alem}
                                    """
                                else:
                                    kabelCommentStr += f"""с alem на kabel сумма {alem}
                                    """ 
                                mes += f'c alem: {alem} на кабель; \n'
                                perAlemM -= alem
                                perKabP += alem
                                perekidkaInfo.kabel2 += alem
                            elif alemTo == 'Alem':
                                abonent1.b_alem += alem
                                mes += f'c alem: {alem} на алем; \n'
                                perAlemM -= alem
                                perAlemP += alem
                                perekidkaInfo.alem2 += alem

                        

                        mes += f'\nПерекидка баланса абонента {abonent1.number} {abonent1.etrap} {abonent1.name} {abonent1.surname}'
                        abonent1.save()
                        perekidkaInfo.comment = mes
                        perekidkaInfo.operator = request.user
                        perekidkaInfo.save()
                        if (perTelefonM + perSlrM + perKodM + perZakazM + perProcheeM + perUslugiM < 0) and (perIntP + perAlemP + perKabP > 0) or (perIntM + perAlemM + perKabM < 0) and (perTelefonP + perSlrP + perKodP + perZakazP + perProcheeP + perUslugiP > 0):
                            InterpayPerekidkaBilling.objects.create(
                                number1=abonent1.number,
                                etrap1=abonent1.etrap,
                                surname1=abonent1.surname,
                                name1=abonent1.name,
                                abonent1_pk=abonent1.pk,

                                internet1 = perIntM,

                                alem1 = perAlemM,
                                telefon1 = perTelefonM,
                                slr1 = perSlrM,
                                kod1 = perKodM,
                                zakaz1 = perZakazM,
                                prochee1 = perProcheeM,
                                dop_uslugi1 =perUslugiM,
                                kabel1 = perKabM,
                                abonent2_pk=abonent2.pk,

                                

                            

                                number2=abonent1.number,
                                etrap2=abonent1.etrap,
                                surname2=abonent1.surname,
                                name2=abonent1.name,

                                alem2=perAlemP,
                                internet2 = perIntP,
  
                                telefon2 = perTelefonP,
                                slr2 = perSlrP,
                                kod2 = perKodP,
                                zakaz2 = perZakazP,
                                prochee2 = perProcheeP,
                                dop_uslugi2 =perUslugiP,
                                kabel2 = perKabP,

                                mtbUsername = request.user.username,
                                mtbEtrap = log,
                                date=datetime.now()

                            )
                        
                        if kabelTvUser:
                            kabelTvUser.save()
                        if kabelCommentObj:
                            kabelCommentObj = KabelComment.objects.create(
                                user=kabelTvUser,
                                worker = request.user.username,
                                comment = f"""{kabelCommentStr}{request.POST.get('comment')}""",
                                action = 'Перекидка'
                            )
                        
                        abonent1 = UserTable.objects.get(number=number1, etrap=etrap1)
                        abonent2 = UserTable.objects.get(number=number2, etrap=etrap2)
                        context['abonent1'] = abonent1
                        context['abonent2'] = abonent2

                        # messages.success(request, f"Успешно! перекидка баланса абонента {abonent1.number[0]}-{abonent1.number[1-3]}{abonent1.number[4:]}")
                       
                    # Если разные абоненты
                    else:
                        print('raznye abonenty')
                        if kabel:
                            messages.error(request, f"Все перекидки с кабеля делаются на KabelTVNew")
                            # refresh data
                            abonent1 = UserTable.objects.get(number=number1, etrap=etrap1)
                            abonent2 = UserTable.objects.get(number=number2, etrap=etrap2)
                            context['abonent1'] = abonent1
                            context['abonent2'] = abonent2
                            return render(request, 'telekom/MATB/perekidka/perekidka.html', context)
                        
                        if telefonTo == 'Кабель' or alemTo == 'Кабель' or internetTo == 'Кабель' or dop_uslugiTo == 'Кабель' or procheeTo == 'Кабель' or zakazTo == 'Кабель' or kodTo == 'Кабель' or slrTo == 'Кабель':
                            try:
                                kabelTvUser = KabelTvNew.objects.get(number=number2)
                            except:
                                messages.error(request, f"Нет номера {number2} в базе Кабель TV")
                                # refresh data
                                abonent1 = UserTable.objects.get(number=number1, etrap=etrap1)
                                abonent2 = UserTable.objects.get(number=number2, etrap=etrap2)
                                context['abonent1'] = abonent1
                                context['abonent2'] = abonent2
                                return render(request, 'telekom/MATB/perekidka/perekidka.html', context)
                        else:
                            kabelTvUser = False


                        # №№№
                        # Теперь код для вычесления эта перекидка между edara и населения. для отчета который попросил ашир ага
                        # факт 1 тут не могут переводится дебет балансы так что будем использовать только кредит
                        
                        if (abonent1.is_enterprises != abonent2.is_enterprises):
                            if abonent1.etrap != abonent2.etrap:
                                try:
                                    nachisleniyaOtchet1 = NachisleniyaOtchet.objects.get(year=current_year, month=month_word, etrap=abonent1.etrap)
                                except:
                                    nachisleniyaOtchet1 = NachisleniyaOtchet.objects.create(year=current_year, month=month_word, etrap=abonent1.etrap)

                                try:
                                    nachisleniyaOtchet2 = NachisleniyaOtchet.objects.get(year=current_year, month=month_word, etrap=abonent2.etrap)
                                except:
                                    nachisleniyaOtchet2 = NachisleniyaOtchet.objects.create(year=current_year, month=month_word, etrap=abonent2.etrap)
                            else:
                                try:
                                    nachOtchet_akt_perek = NachisleniyaOtchet.objects.get(year=current_year, month=month_word, etrap=abonent1.etrap)
                                except:
                                    nachOtchet_akt_perek = NachisleniyaOtchet.objects.create(year=current_year, month=month_word, etrap=abonent1.etrap)

                            total_for_akt_perekidka = 0

                            if telefon:
                                total_for_akt_perekidka += telefon
                            if slr:
                                total_for_akt_perekidka += slr
                            if kod:
                                total_for_akt_perekidka += kod
                            if zakaz:
                                total_for_akt_perekidka += zakaz
                            if prochee:
                                total_for_akt_perekidka += prochee
                            if dop_uslugi:
                                total_for_akt_perekidka += dop_uslugi
                            if internet:
                                total_for_akt_perekidka += internet
                            if alem:
                                total_for_akt_perekidka += alem
                            if kabel:
                                total_for_akt_perekidka += kabel
                            

                            if abonent1.is_enterprises:
                                if abonent1.etrap != abonent2.etrap:
                                    nachisleniyaOtchet1.perek_edara_kredit_minus += total_for_akt_perekidka
                                    nachisleniyaOtchet2.perek_nasel_kredit_plus += total_for_akt_perekidka
                                    nachisleniyaOtchet1.save()
                                    nachisleniyaOtchet2.save()
                                else:
                                    nachOtchet_akt_perek.perek_edara_kredit_minus += total_for_akt_perekidka
                                    nachOtchet_akt_perek.perek_nasel_kredit_plus += total_for_akt_perekidka
                                    nachOtchet_akt_perek.save()
                            else:
                                if abonent1.etrap != abonent2.etrap:
                                    nachisleniyaOtchet1.perek_nasel_kredit_minus += total_for_akt_perekidka
                                    nachisleniyaOtchet2.perek_edara_kredit_plus += total_for_akt_perekidka
                                    nachisleniyaOtchet1.save()
                                    nachisleniyaOtchet2.save()
                                else:
                                    nachOtchet_akt_perek.perek_edara_kredit_plus += total_for_akt_perekidka
                                    nachOtchet_akt_perek.perek_nasel_kredit_minus += total_for_akt_perekidka
                                    nachOtchet_akt_perek.save()



                        # №№№#

                        kabelCommentStr = ''
                        kabelCommentObj = False

                        # №№№  
                        print('1111111111111111', abonent1.number, abonent2.number)      
                        perekidkaInfo = PerekidkaInfo(
                            user1Number = abonent1.number,
                            user1Etrap = abonent1.etrap,
                            user2Number = abonent2.number,
                            user2Etrap = abonent2.etrap,
                            user1_is_enterprises = abonent1.is_enterprises,
                            user2_is_enterprises = abonent2.is_enterprises
                        )
                        # №№№#

                        if telefon:
                            perekidkaInfo.telefon1 = telefon
                            abonent1.b_telefon -= telefon
                            if telefonTo == 'Абонплата':
                                abonent2.b_telefon += telefon
                                mes += f'c Абон: {telefon} на абон; \n'
                                perTelefonM -= telefon
                                perTelefonP += telefon
                                perekidkaInfo.telefon2 += telefon
                            elif telefonTo == 'Слр':
                                abonent2.b_slr += telefon
                                mes += f'c Абон: {telefon} на слр; \n'
                                perTelefonM -= telefon
                                perSlrP += telefon
                                perekidkaInfo.slr2 += telefon
                            elif telefonTo == 'Код':
                                abonent2.b_kod += telefon
                                mes += f'c Абон: {telefon} на код; \n'
                                perTelefonM -= telefon
                                perKodP += telefon
                                perekidkaInfo.kod2 += telefon
                            elif telefonTo == 'Заказ':
                                abonent2.b_zakaz += telefon
                                mes += f'c Абон: {telefon} на заказ; \n'
                                perTelefonM -= telefon
                                perZakazP += telefon
                                perekidkaInfo.zakaz2 += telefon
                            elif telefonTo == 'Прочее':
                                abonent2.b_prochee += telefon
                                mes += f'c Абон: {telefon} на прочее; \n'
                                perTelefonM -= telefon
                                perProcheeP += telefon
                                perekidkaInfo.prochee2 += telefon
                            elif telefonTo == 'Доп.услуги':
                                abonent2.b_dop_uslugi += telefon
                                mes += f'c Абон: {telefon} на доп. ус; \n'
                                perTelefonM -= telefon
                                perUslugiP += telefon
                                perekidkaInfo.dop_uslugi2 += telefon
                            elif telefonTo == 'Интернет':
                                abonent2.b_internet += telefon
                                mes += f'c Абон: {telefon} на internet; \n'
                                perTelefonM -= telefon
                                perIntP += telefon
                                perekidkaInfo.internet2 += telefon
                            elif telefonTo == 'Кабель':
                                # abonent2.b_kabel += telefon
                                kabelTvUser.balance += telefon  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с telefon на kabel сумма {telefon}
                                    """
                                else:
                                    kabelCommentStr += f"""с telefon на kabel сумма {telefon}
                                    """
                                mes += f'c Абон: {telefon} на кабель; \n'
                                perTelefonM -= telefon
                                perKabP += telefon
                                perekidkaInfo.kabel2 += telefon
                            elif telefonTo == 'Alem':
                                abonent2.b_alem += telefon
                                mes += f'c Абон: {telefon} на alem; \n'
                                perTelefonM -= telefon
                                perAlemP += telefon
                                perekidkaInfo.alem2 += telefon
                            
                        if slr:
                            perekidkaInfo.slr1 = slr
                            abonent1.b_slr -= slr
                            if slrTo == 'Абонплата':
                                abonent2.b_telefon += slr
                                mes += f'c слр: {slr} на абон; \n'
                                perSlrM -= slr
                                perTelefonP += slr
                                perekidkaInfo.telefon2 += slr
                            elif slrTo == 'Слр':
                                abonent2.b_slr += slr
                                mes += f'c слр: {slr} на слр; \n'
                                perSlrM -= slr
                                perSlrP += slr
                                perekidkaInfo.slr2 += slr
                            elif slrTo == 'Код':
                                abonent2.b_kod += slr
                                mes += f'c слр: {slr} на код; \n'
                                perSlrM -= slr
                                perKodP += slr
                                perekidkaInfo.kod2 += slr
                            elif slrTo == 'Заказ':
                                abonent2.b_zakaz += slr
                                mes += f'c слр: {slr} на заказ; \n'
                                perSlrM -= slr
                                perZakazP += slr
                                perekidkaInfo.zakaz2 += slr
                            elif slrTo == 'Прочее':
                                abonent2.b_prochee += slr
                                mes += f'c слр: {slr} на прочее; \n'
                                perSlrM -= slr
                                perProcheeP += slr
                                perekidkaInfo.prochee2 += slr
                            elif slrTo == 'Доп.услуги':
                                abonent2.b_dop_uslugi += slr
                                mes += f'c слр: {slr} на доп. услуги; \n'
                                perSlrM -= slr
                                perUslugiP += slr
                                perekidkaInfo.dop_uslugi2 += slr
                            elif slrTo == 'Интернет':
                                abonent2.b_internet += slr
                                mes += f'c слр: {slr} на интернет; \n'
                                perSlrM -= slr
                                perIntP += slr
                                perekidkaInfo.internet2 += slr
                            elif slrTo == 'Кабель':
                                # abonent2.b_kabel += slr
                                kabelTvUser.balance += slr  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с slr на kabel сумма {slr}
                                    """
                                else:
                                    kabelCommentStr += f"""с slr на kabel сумма {slr}
                                    """
                                mes += f'c слр: {slr} на кабель; \n'
                                perSlrM -= slr
                                perKabP += slr
                                perekidkaInfo.kabel2 += slr
                            elif slrTo == 'Alem':
                                abonent2.b_alem += slr
                                mes += f'c слр: {slr} на alem; \n'
                                perSlrM -= slr
                                perAlemP += slr
                                perekidkaInfo.alem2 += slr
                        
                        if kod:
                            perekidkaInfo.kod1 = kod
                            abonent1.b_kod -= kod
                            if kodTo == 'Абонплата':
                                abonent2.b_telefon += kod
                                mes += f'c код: {kod} на абон; \n'
                                perKodM -= kod
                                perTelefonP += kod
                                perekidkaInfo.telefon2 += kod
                            elif kodTo == 'Слр':
                                abonent2.b_slr += kod
                                mes += f'c код: {kod} на слр; \n'
                                perKodM -= kod
                                perSlrP += kod
                                perekidkaInfo.slr2 += kod
                            elif kodTo == 'Код':
                                abonent2.b_kod += kod
                                mes += f'c код: {kod} на код; \n'
                                perKodM -= kod
                                perKodP += kod
                                perekidkaInfo.kod2 += kod
                            elif kodTo == 'Заказ':
                                abonent2.b_zakaz += kod
                                mes += f'c код: {kod} на заказ; \n'
                                perKodM -= kod
                                perZakazP += kod
                                perekidkaInfo.zakaz2 += kod
                            elif kodTo == 'Прочее':
                                abonent2.b_prochee += kod
                                mes += f'c код: {kod} на прочее; \n'
                                perKodM -= kod
                                perProcheeP += kod
                                perekidkaInfo.prochee2 += kod
                            elif kodTo == 'Доп.услуги':
                                abonent2.b_dop_uslugi += kod
                                mes += f'c код: {kod} на доп. ус.; \n'
                                perKodM -= kod
                                perUslugiP += kod
                                perekidkaInfo.dop_uslugi2 += kod
                            elif kodTo == 'Интернет':
                                abonent2.b_internet += kod
                                mes += f'c код: {kod} на инт; \n'
                                perKodM -= kod
                                perIntP += kod
                                perekidkaInfo.internet2 += kod
                            elif kodTo == 'Кабель':
                                # abonent2.b_kabel += kod
                                kabelTvUser.balance += kod  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с kod на kabel сумма {kod}
                                    """
                                else:
                                    kabelCommentStr += f"""с kod на kabel сумма {kod}
                                    """
                                mes += f'c код: {kod} на кабель; \n'
                                perKodM -= kod
                                perKabP += kod
                                perekidkaInfo.kabel2 += kod
                            elif kodTo == 'Alem':
                                abonent2.b_alem += kod
                                mes += f'c код: {kod} на алем; \n'
                                perKodM -= kod
                                perAlemP += kod
                                perekidkaInfo.alem2 += kod
                    
                        if zakaz:
                            perekidkaInfo.zakaz1 = zakaz
                            abonent1.b_zakaz -= zakaz
                            if zakazTo == 'Абонплата':
                                abonent2.b_telefon += zakaz
                                mes += f'c заказ: {zakaz} на абон; \n'
                                perZakazM -= zakaz
                                perTelefonP += zakaz
                                perekidkaInfo.telefon2 += zakaz
                            elif zakazTo == 'Слр':
                                abonent2.b_slr += zakaz
                                mes += f'c заказ: {zakaz} на слр; \n'
                                perZakazM -= zakaz
                                perSlrP += zakaz
                                perekidkaInfo.slr2 += zakaz
                            elif zakazTo == 'Код':
                                abonent2.b_kod += zakaz
                                mes += f'c заказ: {zakaz} на код; \n'
                                perZakazM -= zakaz
                                perKodP += zakaz
                                perekidkaInfo.kod2 += zakaz
                            elif zakazTo == 'Заказ':
                                abonent2.b_zakaz += zakaz
                                mes += f'c заказ: {zakaz} на заказ; \n'
                                perZakazM -= zakaz
                                perZakazP += zakaz
                                perekidkaInfo.zakaz2 += zakaz
                            elif zakazTo == 'Прочее':
                                abonent2.b_prochee += zakaz
                                mes += f'c заказ: {zakaz} на прочее; \n'
                                perZakazM -= zakaz
                                perProcheeP += zakaz
                                perekidkaInfo.prochee2 += zakaz
                            elif zakazTo == 'Доп.услуги':
                                abonent2.b_dop_uslugi += zakaz
                                mes += f'c заказ: {zakaz} на доп. ус; \n'
                                perZakazM -= zakaz
                                perUslugiP += zakaz
                                perekidkaInfo.dop_uslugi2 += zakaz
                            elif zakazTo == 'Интернет':
                                abonent2.b_internet += zakaz
                                mes += f'c заказ: {zakaz} на инт; \n'
                                perZakazM -= zakaz
                                perIntP += zakaz
                                perekidkaInfo.internet2 += zakaz
                            elif zakazTo == 'Кабель':
                                # abonent2.b_kabel += zakaz
                                kabelTvUser.balance += zakaz  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с zakaz на kabel сумма {zakaz}
                                    """
                                else:
                                    kabelCommentStr += f"""с zakaz на kabel сумма {zakaz}
                                    """
                                mes += f'c заказ: {zakaz} на кабель; \n'
                                perZakazM -= zakaz
                                perKabP += zakaz
                                perekidkaInfo.kabel2 += zakaz
                            elif zakazTo == 'Alem':
                                abonent2.b_alem += zakaz
                                mes += f'c заказ: {zakaz} на алем; \n'
                                perZakazM -= zakaz
                                perAlemP += zakaz
                                perekidkaInfo.alem2 += zakaz
                        
                        if prochee:
                            perekidkaInfo.prochee1 = prochee
                            abonent1.b_prochee -= prochee
                            if procheeTo == 'Абонплата':
                                abonent2.b_telefon += prochee
                                mes += f'c прочее: {prochee} на абон; \n'
                                perProcheeM -= prochee
                                perTelefonP += prochee
                                perekidkaInfo.telefon2 += prochee
                            elif procheeTo == 'Слр':
                                abonent2.b_slr += prochee
                                mes += f'c прочее: {prochee} на слр; \n'
                                perProcheeM -= prochee
                                perSlrP += prochee
                                perekidkaInfo.slr2 += prochee
                            elif procheeTo == 'Код':
                                abonent2.b_kod += prochee
                                mes += f'c прочее: {prochee} на код; \n'
                                perProcheeM -= prochee
                                perKodP += prochee
                                perekidkaInfo.kod2 += prochee
                            elif procheeTo == 'Заказ':
                                abonent2.b_zakaz += prochee
                                mes += f'c прочее: {prochee} на заказ; \n'
                                perProcheeM -= prochee
                                perZakazP += prochee
                                perekidkaInfo.zakaz2 += prochee
                            elif procheeTo == 'Прочее':
                                abonent2.b_prochee += prochee
                                mes += f'c прочее: {prochee} на прочее; \n'
                                perProcheeM -= prochee
                                perProcheeP += prochee
                                perekidkaInfo.prochee2 += prochee
                            elif procheeTo == 'Доп.услуги':
                                abonent2.b_dop_uslugi += prochee
                                mes += f'c прочее: {prochee} на доп. ус.; \n'
                                perProcheeM -= prochee
                                perUslugiP += prochee
                                perekidkaInfo.dop_uslugi2 += prochee
                            elif procheeTo == 'Интернет':
                                abonent2.b_internet += prochee
                                mes += f'c прочее: {prochee} на инт; \n'
                                perProcheeM -= prochee
                                perIntP += prochee
                                perekidkaInfo.internet2 += prochee
                            elif procheeTo == 'Кабель':
                                # abonent2.b_kabel += prochee
                                kabelTvUser.balance += prochee  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с prochee на kabel сумма {prochee}
                                    """
                                else:
                                    kabelCommentStr += f"""с prochee на kabel сумма {prochee}
                                    """
                                mes += f'c прочее: {prochee} на кабель; \n'
                                perProcheeM -= prochee
                                perKabP += prochee
                                perekidkaInfo.kabel2 += prochee
                            elif procheeTo == 'Alem':
                                abonent2.b_alem += prochee
                                mes += f'c прочее: {prochee} на алем; \n'
                                perProcheeM -= prochee
                                perAlemP += prochee
                                perekidkaInfo.alem2 += prochee
                        
                        if dop_uslugi:
                            perekidkaInfo.dop_uslugi1 = dop_uslugi
                            abonent1.b_dop_uslugi -= dop_uslugi
                            if dop_uslugiTo == 'Абонплата':
                                abonent2.b_telefon += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на абон; \n'
                                perUslugiM -= dop_uslugi
                                perTelefonP += dop_uslugi
                                perekidkaInfo.telefon2 += dop_uslugi
                            elif dop_uslugiTo == 'Слр':
                                abonent2.b_slr += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на слр; \n'
                                perUslugiM -= dop_uslugi
                                perSlrP += dop_uslugi
                                perekidkaInfo.slr2 += dop_uslugi
                            elif dop_uslugiTo == 'Код':
                                abonent2.b_kod += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на код; \n'
                                perUslugiM -= dop_uslugi
                                perKodP += dop_uslugi
                                perekidkaInfo.kod2 += dop_uslugi
                            elif dop_uslugiTo == 'Заказ':
                                abonent2.b_zakaz += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на заказ; \n'
                                perUslugiM -= dop_uslugi
                                perZakazM += dop_uslugi
                                perekidkaInfo.zakaz2 += dop_uslugi
                            elif dop_uslugiTo == 'Прочее':
                                abonent2.b_prochee += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на прочее; \n'
                                perUslugiM -= dop_uslugi
                                perProcheeP += dop_uslugi
                                perekidkaInfo.prochee2 += dop_uslugi
                            elif dop_uslugiTo == 'Доп.услуги':
                                abonent2.b_dop_uslugi += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на доп. ус; \n'
                                perUslugiM -= dop_uslugi
                                perUslugiP += dop_uslugi
                                perekidkaInfo.dop_uslugi2 += dop_uslugi
                            elif dop_uslugiTo == 'Интернет':
                                abonent2.b_internet += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на инт; \n'
                                perUslugiM -= dop_uslugi
                                perIntP += dop_uslugi
                                perekidkaInfo.internet2 += dop_uslugi
                            elif dop_uslugiTo == 'Кабель':
                                # abonent2.b_kabel += dop_uslugi
                                kabelTvUser.balance += dop_uslugi  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с dop_uslugi на kabel сумма {dop_uslugi}
                                    """
                                else:
                                    kabelCommentStr += f"""с dop_uslugi на kabel сумма {dop_uslugi}
                                    """ 
                                mes += f'c доп. ус: {dop_uslugi} на кабель; \n'
                                perUslugiM -= dop_uslugi
                                perKabP += dop_uslugi
                                perekidkaInfo.kabel2 += dop_uslugi
                            elif dop_uslugiTo == 'Alem':
                                abonent2.b_alem += dop_uslugi
                                mes += f'c доп. ус: {dop_uslugi} на алем; \n'
                                perUslugiM -= dop_uslugi
                                perAlemP += dop_uslugi
                                perekidkaInfo.alem2 += dop_uslugi
                    
                        if internet:
                            perekidkaInfo.internet1 = internet
                            abonent1.b_internet -= internet
                            if internetTo == 'Абонплата':
                                abonent2.b_telefon += internet
                                mes += f'c интернет: {internet} на абон; \n'
                                perIntM -= internet
                                perTelefonP += internet
                                perekidkaInfo.telefon2 += internet
                            elif internetTo == 'Слр':
                                abonent2.b_slr += internet
                                mes += f'c интернет: {internet} на слр; \n'
                                perIntM -= internet
                                perSlrP += internet
                                perekidkaInfo.slr2 += internet
                            elif internetTo == 'Код':
                                abonent2.b_kod += internet
                                mes += f'c интернет: {internet} на код; \n'
                                perIntM -= internet
                                perKodP += internet
                                perekidkaInfo.kod2 += internet
                            elif internetTo == 'Заказ':
                                abonent2.b_zakaz += internet
                                mes += f'c интернет: {internet} на заказ; \n'
                                perIntM -= internet
                                perZakazP += internet
                                perekidkaInfo.zakaz2 += internet
                            elif internetTo == 'Прочее':
                                abonent2.b_prochee += internet
                                mes += f'c интернет: {internet} на прочее; \n'
                                perIntM -= internet
                                perProcheeP += internet
                                perekidkaInfo.prochee2 += internet
                            elif internetTo == 'Доп.услуги':
                                abonent2.b_dop_uslugi += internet
                                mes += f'c интернет: {internet} на доп. ус; \n'
                                perIntM -= internet
                                perUslugiP += internet
                                perekidkaInfo.dop_uslugi2 += internet
                            elif internetTo == 'Интернет':
                                abonent2.b_internet += internet
                                mes += f'c интернет: {internet} на интернет; \n'
                                perIntM -= internet
                                perIntP += internet
                                perekidkaInfo.internet2 += internet
                            elif internetTo == 'Кабель':
                                # abonent2.b_kabel += internet
                                kabelTvUser.balance += internet  
                                kabelCommentObj = True  
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с internet на kabel сумма {internet}
                                    """
                                else:
                                    kabelCommentStr += f"""с internet на kabel сумма {internet}
                                    """ 
                                mes += f'c интернет: {internet} на кабель; \n'
                                perIntM -= internet
                                perKabP += internet
                                perekidkaInfo.kabel2 += internet
                            elif internetTo == 'Alem':
                                abonent2.b_alem += internet
                                mes += f'c интернет: {internet} на алем; \n'
                                perIntM -= internet
                                perAlemP += internet
                                perekidkaInfo.alem2 += internet
                        
                        if kabel:
                            pass
                            # abonent1.b_kabel -= kabel
                            # if kabelTo == 'Абонплата':
                            #     abonent2.b_telefon += kabel
                            #     mes += f'c кабель: {kabel} на абон; \n'
                            #     perKabM -= kabel
                            #     perTelefonP += kabel
                            #     perekidkaInfo.telefon2 = kabel
                            # elif kabelTo == 'Слр':
                            #     abonent2.b_slr += kabel
                            #     mes += f'c кабель: {kabel} на слр; \n'
                            #     perKabM -= kabel
                            #     perSlrP += kabel
                            #     perekidkaInfo.slr2 = kabel
                            # elif kabelTo == 'Код':
                            #     abonent2.b_kod += kabel
                            #     mes += f'c кабель: {kabel} на код; \n'
                            #     perKabM -= kabel
                            #     perKodP += kabel
                            #     perekidkaInfo.kod2 = kabel
                            # elif kabelTo == 'Заказ':
                            #     abonent2.b_zakaz += kabel
                            #     mes += f'c кабель: {kabel} на заказ; \n'
                            #     perKabM -= kabel
                            #     perZakazP += kabel
                            #     perekidkaInfo.zakaz2 = kabel
                            # elif kabelTo == 'Прочее':
                            #     abonent2.b_prochee += kabel
                            #     mes += f'c кабель: {kabel} на прочее; \n'
                            #     perKabM -= kabel
                            #     perProcheeP += kabel
                            #     perekidkaInfo.prochee2 = kabel
                            # elif kabelTo == 'Доп.услуги':
                            #     abonent2.b_dop_uslugi += kabel
                            #     mes += f'c кабель: {kabel} на доп. ус; \n'
                            #     perKabM -= kabel
                            #     perUslugiP += kabel
                            #     perekidkaInfo.dop_uslugi2 = kabel
                            # elif kabelTo == 'Интернет':
                            #     abonent2.b_internet += kabel
                            #     mes += f'c кабель: {kabel} на инт; \n'
                            #     perKabM -= kabel
                            #     perIntP += kabel
                            #     perekidkaInfo.internet2 = kabel
                            # elif kabelTo == 'Кабель':
                            #     abonent2.b_kabel += kabel
                            #     mes += f'c кабель: {kabel} на кабель; \n'
                            #     perKabM -= kabel
                            #     perKabP += kabel
                            #     perekidkaInfo.kabel2 = kabel
                            # elif kabelTo == 'Alem':
                            #     abonent2.b_alem += kabel
                            #     mes += f'c кабель: {kabel} на алем; \n'
                            #     perKabM -= kabel
                            #     perAlemP += kabel
                            #     perekidkaInfo.alem2 = kabel
                    
                        if alem:
                            perekidkaInfo.alem1 = alem
                            abonent1.b_alem -= alem
                            if alemTo == 'Абонплата':
                                abonent2.b_telefon += alem
                                mes += f'c alem: {alem} на абон; \n'
                                perAlemM -= alem
                                perTelefonP += alem
                                perekidkaInfo.telefon2 += alem
                            elif alemTo == 'Слр':
                                abonent2.b_slr += alem
                                mes += f'c alem: {alem} на слр; \n'
                                perAlemM -= alem
                                perSlrP += alem
                                perekidkaInfo.slr2 += alem
                            elif alemTo == 'Код':
                                abonent2.b_kod += alem
                                mes += f'c alem: {alem} на код; \n'
                                perAlemM -= alem
                                perKodP += alem
                                perekidkaInfo.kod2 += alem
                            elif alemTo == 'Заказ':
                                abonent2.b_zakaz += alem
                                mes += f'c alem: {alem} на заказ; \n'
                                perAlemM -= alem
                                perZakazP += alem
                                perekidkaInfo.zakaz2 += alem
                            elif alemTo == 'Прочее':
                                abonent2.b_prochee += alem
                                mes += f'c alem: {alem} на прочее; \n'
                                perAlemM -= alem
                                perProcheeP += alem
                                perekidkaInfo.prochee2 += alem
                            elif alemTo == 'Доп.услуги':
                                abonent2.b_dop_uslugi += alem
                                mes += f'c alem: {alem} на доп. ус.; \n'
                                perAlemM -= alem
                                perUslugiP += alem
                                perekidkaInfo.dop_uslugi2 += alem
                            elif alemTo == 'Интернет':
                                abonent2.b_internet += alem
                                mes += f'c alem: {alem} на инт; \n'
                                perAlemM -= alem
                                perIntP += alem
                                perekidkaInfo.internet2 += alem
                            elif alemTo == 'Кабель':
                                # abonent2.b_kabel += alem
                                kabelTvUser.balance += alem  
                                kabelCommentObj = True 
                                if kabelCommentStr == '':
                                    kabelCommentStr += f"""Перекидка с номера {number1} на номер {number2}:
                                    с alem на kabel сумма {alem}
                                    """
                                else:
                                    kabelCommentStr += f"""с alem на kabel сумма {alem}
                                    """ 
                                mes += f'c alem: {alem} на кабель; \n'
                                perAlemM -= alem
                                perKabP += alem
                                perekidkaInfo.kabel2 += alem
                            elif alemTo == 'Alem':
                                abonent2.b_alem += alem
                                mes += f'c alem: {alem} на алем; \n'
                                perAlemM -= alem
                                perAlemP += alem
                                perekidkaInfo.alem2 += alem

                                
                        mes += f'\nПерекидка баланса абонентов:\n c {abonent1.number} {abonent1.etrap} {abonent1.name} {abonent1.surname}\n на {abonent2.number} {abonent2.etrap} {abonent2.name} {abonent2.surname}'
                        abonent1.save()
                        abonent2.save()
                        perekidkaInfo.comment = mes
                        perekidkaInfo.operator = request.user
                        perekidkaInfo.save()
                        InterpayPerekidkaBilling.objects.create(
                            number1=abonent1.number,
                            etrap1=abonent1.etrap,
                            surname1=abonent1.surname,
                            name1=abonent1.name,
                            abonent1_pk=abonent1.pk,

                            internet1 = perIntM,
                            alem1 = perAlemM,
                            telefon1 = perTelefonM,
                            slr1 = perSlrM,
                            kod1 = perKodM,
                            zakaz1 = perZakazM,
                            prochee1 = perProcheeM,
                            dop_uslugi1 =perUslugiM,
                            kabel1 = perKabM,
                            abonent2_pk=abonent2.pk,

                            number2=abonent2.number,
                            etrap2=abonent2.etrap,
                            surname2=abonent2.surname,
                            name2=abonent2.name,

                            alem2=perAlemP,
                            internet2 = perIntP,
                            telefon2 = perTelefonP,
                            slr2 = perSlrP,
                            kod2 = perKodP,
                            zakaz2 = perZakazP,
                            prochee2 = perProcheeP,
                            dop_uslugi2 =perUslugiP,
                            kabel2 = perKabP,

                            mtbUsername = request.user.username,
                            mtbEtrap = log,
                            date=datetime.now()
                        )

                        if kabelTvUser:
                            kabelTvUser.save()
                        if kabelCommentObj:
                            kabelCommentObj = KabelComment.objects.create(
                                user=kabelTvUser,
                                worker = request.user.username,
                                comment = f"""{kabelCommentStr}{request.POST.get('comment')}""",
                                action = 'Перекидка'
                            )
             

                    # refresh data
                    abonent1 = UserTable.objects.get(number=number1, etrap=etrap1)
                    abonent2 = UserTable.objects.get(number=number2, etrap=etrap2)
                    context['abonent1'] = abonent1
                    context['abonent2'] = abonent2

                    # print(perTelefonM,perSlrM,perKodM,perZakazM,perProcheeM,perUslugiM,perIntM,perKabM,perAlemM)
                    # print(perTelefonP,perSlrP,perKodP,perZakazP,perProcheeP,perUslugiP,perIntP,perKabP,perAlemP)

                    messages.success(request, f"Успешно! перекидка баланса")
                    try:
                        nachisleniyaOtchet = NachisleniyaOtchet.objects.get(year=current_year, month=month_word, etrap=log)
                    except:
                        nachisleniyaOtchet = NachisleniyaOtchet.objects.create(year=current_year, month=month_word, etrap=log)
                    nachisleniyaOtchet.internetM += abs(perIntM)
                    nachisleniyaOtchet.alemM += abs(perAlemM)
                    nachisleniyaOtchet.telefonM += abs(perTelefonM)
                    nachisleniyaOtchet.slrM += abs(perSlrM)
                    nachisleniyaOtchet.kodM += abs(perKodM)
                    nachisleniyaOtchet.zakazM += abs(perZakazM)
                    nachisleniyaOtchet.procheeM += abs(perProcheeM)
                    nachisleniyaOtchet.dop_uslugiM += abs(perUslugiM)

                    nachisleniyaOtchet.internetP += perIntP
                    nachisleniyaOtchet.alemP += perAlemP
                    nachisleniyaOtchet.telefonP += perTelefonP
                    nachisleniyaOtchet.slrP += perSlrP
                    nachisleniyaOtchet.kodP += perKodP
                    nachisleniyaOtchet.zakazP += perZakazP
                    nachisleniyaOtchet.procheeP += perProcheeP
                    nachisleniyaOtchet.dop_uslugiP += perUslugiP
                    nachisleniyaOtchet.save()
            
                    
                    StaffAction.objects.create(action='Перекидка',comment=f"{request.POST.get('comment')}\n\n {mes}", user=request.user)

    # Если нажал на удалить платеж (всю квитанцию)
    if request.method == 'POST' and 'cancelPayComment' in request.POST:
        if request.POST.get('cancelPayComment') == '':
            messages.error(request, 'Оставьте комментарий')
        else:
            # Удаление платежа (в interpay тоже удаляется автоматически)
            payHistoryCancelPay = PayHistory.objects.get(pk=request.POST.get('payPkCancelPay'))

            telefon1 = payHistoryCancelPay.telefon
            slr1 = payHistoryCancelPay.slr
            kod1 = payHistoryCancelPay.kod
            zakaz1 = payHistoryCancelPay.zakaz
            prochee1 = payHistoryCancelPay.prochee
            dop_uslugi1 = payHistoryCancelPay.dop_uslugi
            internet1 = payHistoryCancelPay.internet
            kabel1 = payHistoryCancelPay.kabel
            alem1 = payHistoryCancelPay.alem

            # Удалени с баланса тоже
            user = UserTable.objects.get(pk=payHistoryCancelPay.abonent.pk)
            user.b_telefon -= telefon1
            user.b_slr -= slr1
            user.b_kod -= kod1
            user.b_zakaz -= zakaz1
            user.b_prochee -= prochee1
            user.b_dop_uslugi -= dop_uslugi1
            user.b_internet -= internet1
            user.b_kabel -= kabel1
            user.b_alem -= alem1
            user.save()

            if payHistoryCancelPay.telefon != 0 or payHistoryCancelPay.slr != 0 or payHistoryCancelPay.kod != 0 or payHistoryCancelPay.zakaz != 0 or payHistoryCancelPay.prochee != 0 or payHistoryCancelPay.dop_uslugi != 0 or payHistoryCancelPay.internet != 0 or payHistoryCancelPay.alem != 0 or payHistoryCancelPay.kabel != 0:
                # хз зачем нужно создавать InterpayPerekidkaBilling.objects.create (закаментирую пока)
                # а все понял это будут показывать минусы и Interpay чтобы ejesh удалила платеж с билинг
                InterpayPerekidkaBilling.objects.create(
                    number1 = payHistoryCancelPay.abonent.number,
                    etrap1 = payHistoryCancelPay.abonent.etrap,
                    surname1 = payHistoryCancelPay.abonent.surname,
                    name1 = payHistoryCancelPay.abonent.name,
                    date = datetime.now(),


                    telefon1 = -payHistoryCancelPay.telefon,
                    slr1 = -payHistoryCancelPay.slr,
                    kod1 = -payHistoryCancelPay.kod,
                    zakaz1 = -payHistoryCancelPay.zakaz,
                    prochee1 = -payHistoryCancelPay.prochee,
                    dop_uslugi1 = -payHistoryCancelPay.dop_uslugi,
                    internet1 = -payHistoryCancelPay.internet,
                    kabel1 = -payHistoryCancelPay.kabel,
                    alem1 = -payHistoryCancelPay.alem,

                    mtbUsername = request.user.username,
                    mtbEtrap = log
                )

            mes = f'Удаление платежа абонента {payHistoryCancelPay.abonent.number}, etrap {payHistoryCancelPay.abonent.etrap}, {payHistoryCancelPay.abonent.surname} {payHistoryCancelPay.abonent.name}\n Информация о платеже: \nинтернет: {payHistoryCancelPay.internet}; кабель: {payHistoryCancelPay.kabel}; аlem TV: {payHistoryCancelPay.alem}; абонплата: {payHistoryCancelPay.telefon}; слр: {payHistoryCancelPay.slr}; код: {payHistoryCancelPay.kod}; заказ: {payHistoryCancelPay.zakaz}; прочее: {payHistoryCancelPay.prochee}; доп. услуги: {payHistoryCancelPay.dop_uslugi}; всего: {payHistoryCancelPay.total}; карт?: {payHistoryCancelPay.is_card}; кассир: {payHistoryCancelPay.kassir}; дата оплаты: {payHistoryCancelPay.date};'
            PayHistory.objects.get(pk=request.POST.get('payPkCancelPay')).delete()
            StaffAction.objects.create(action='Перекидка',comment=f"{request.POST.get('cancelPayComment')}\n\n {mes}", user=request.user)
            messages.success(request, 'Платеж удален')


    if request.method == 'POST' and 'perekidkaComment' in request.POST:
        if request.POST.get('perekidkaComment') == '':
            messages.error(request, 'Оставьте комментарий')
        else:
            # перекидка платежа (квитанции)
            payHistoryCancelPay = PayHistory.objects.get(pk=request.POST.get('payPkPerekidka'))

            if payHistoryCancelPay.telefon != 0 or payHistoryCancelPay.slr != 0 or payHistoryCancelPay.kod != 0 or payHistoryCancelPay.zakaz != 0 or payHistoryCancelPay.prochee != 0 or payHistoryCancelPay.dop_uslugi != 0 or payHistoryCancelPay.internet != 0 or payHistoryCancelPay.alem != 0 or payHistoryCancelPay.kabel:
                mes = f'Перекидка платежа с абонента {payHistoryCancelPay.abonent.number}, etrap {payHistoryCancelPay.abonent.etrap}, {payHistoryCancelPay.abonent.surname} {payHistoryCancelPay.abonent.name}\n На абонента {abonent2.number}, etrap {abonent2.etrap}, ФИО {abonent2.surname} {abonent2.name}\nИнформация о платеже: \nинтернет: {payHistoryCancelPay.internet}; кабель: {payHistoryCancelPay.kabel}; аlem TV: {payHistoryCancelPay.alem}; абонплата: {payHistoryCancelPay.telefon}; слр: {payHistoryCancelPay.slr}; код: {payHistoryCancelPay.kod}; заказ: {payHistoryCancelPay.zakaz}; прочее: {payHistoryCancelPay.prochee}; доп. услуги: {payHistoryCancelPay.dop_uslugi}; всего: {payHistoryCancelPay.total}; карт?: {payHistoryCancelPay.is_card}; кассир: {payHistoryCancelPay.kassir}; дата оплаты: {payHistoryCancelPay.date};'
                InterpayPerekidkaBilling.objects.create(
                    number1 = payHistoryCancelPay.abonent.number,
                    etrap1 = payHistoryCancelPay.abonent.etrap,
                    surname1 = payHistoryCancelPay.abonent.surname,
                    name1 = payHistoryCancelPay.abonent.name,
                    date = datetime.now(),

                    telefon1 = -payHistoryCancelPay.telefon,
                    slr1 = -payHistoryCancelPay.slr,
                    kod1 = -payHistoryCancelPay.kod,
                    zakaz1 = -payHistoryCancelPay.zakaz,
                    prochee1 = -payHistoryCancelPay.prochee,
                    dop_uslugi1 = -payHistoryCancelPay.dop_uslugi,
                    internet1 = -payHistoryCancelPay.internet,
                    kabel1 = -payHistoryCancelPay.kabel,
                    alem1 = -payHistoryCancelPay.alem,


                    number2 = abonent2.number,
                    etrap2 = abonent2.etrap,
                    surname2 = abonent2.surname,
                    name2 = abonent2.name,

                    telefon2 = payHistoryCancelPay.telefon,
                    slr2 = payHistoryCancelPay.slr,
                    kod2 = payHistoryCancelPay.kod,
                    zakaz2 = payHistoryCancelPay.zakaz,
                    prochee2 = payHistoryCancelPay.prochee,
                    dop_uslugi2 = payHistoryCancelPay.dop_uslugi,
                    internet2 = payHistoryCancelPay.internet,
                    kabel2 = payHistoryCancelPay.kabel,
                    alem2 = payHistoryCancelPay.alem,

                    mtbUsername = request.user.username,
                    mtbEtrap = log
                )

                if payHistoryCancelPay.telefon > 0:
                    abonent1.b_telefon -= payHistoryCancelPay.telefon
                    abonent2.b_telefon += payHistoryCancelPay.telefon

                if payHistoryCancelPay.slr > 0:
                    abonent1.b_slr -= payHistoryCancelPay.slr
                    abonent2.b_slr += payHistoryCancelPay.slr

                if payHistoryCancelPay.kod > 0:
                    abonent1.b_kod -= payHistoryCancelPay.kod
                    abonent2.b_kod += payHistoryCancelPay.kod

                if payHistoryCancelPay.zakaz > 0:
                    abonent1.b_zakaz -= payHistoryCancelPay.zakaz
                    abonent2.b_zakaz += payHistoryCancelPay.zakaz

                if payHistoryCancelPay.prochee > 0:
                    abonent1.b_prochee -= payHistoryCancelPay.prochee
                    abonent2.b_prochee += payHistoryCancelPay.prochee

                if payHistoryCancelPay.dop_uslugi > 0:
                    abonent1.b_dop_uslugi -= payHistoryCancelPay.dop_uslugi
                    abonent2.b_dop_uslugi += payHistoryCancelPay.dop_uslugi

                if payHistoryCancelPay.internet > 0:
                    abonent1.b_internet -= payHistoryCancelPay.internet
                    abonent2.b_internet += payHistoryCancelPay.internet

                if payHistoryCancelPay.kabel > 0:
                    abonent1.b_kabel -= payHistoryCancelPay.kabel
                    abonent2.b_kabel += payHistoryCancelPay.kabel

                if payHistoryCancelPay.alem > 0:
                    abonent1.b_alem -= payHistoryCancelPay.alem
                    abonent2.b_alem += payHistoryCancelPay.alem

                payHistoryCancelPay.abonent = abonent2
                abonent1.save()
                abonent2.save()
                payHistoryCancelPay.save()
                
                StaffAction.objects.create(action='Перекидка',comment=f"{request.POST.get('cancelPayComment')}\n\n {mes}", user=request.user)
                messages.success(request, 'Платеж перекинут')


    if request.method == 'POST' and 'cancelPerekidkaID' in request.POST:
        print('dada')
    return render(request, 'telekom/MATB/perekidka/perekidka.html', context)
