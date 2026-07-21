from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

from datetime import date
from datetime import datetime
from calendar import monthrange
import re

from telekom.models import AbonentService, NachMinus, NachisleniyaOtchet, StaffAction, UserTable, UstanowkaSnyatieDopUslugHistory

from telekom.views2.myFunc.myFunc import get_etrap_and_types, loggedUserEtrapAndGroup, monthСonvert


from django.db import transaction
import logging
logger = logging.getLogger(__name__)


def serviceConnect(request):

    # EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    # if EtrapAndGroup[1] == 'MB' or request.user.is_superuser:
    #     log = EtrapAndGroup[0]
    # else:
    #     messages.error(request, f'Доступ только соотрудникам MB')
    #     return redirect('user-login')
    
    context = {}

    if request.user.is_authenticated:
        if request.user.is_superuser:
            log = 'Dashoguz'
            context['setService'] = True
            context['serviceConnect'] = True
            context['allow_to_change_service'] = True
        else:
            etrap_types = get_etrap_and_types(request.user)
            etraps = etrap_types['etraps']
            log = etraps[0]
            types = etrap_types['types']
            if 'MB' in types:
                context['setService'] = True
                context['serviceConnect'] = True
                context['allow_to_change_service'] = True
                if 'Gayyp' in request.user.username:
                    context['allow_to_change_service'] = True
            else:
                context['allow_to_change_service'] = False
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')

    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date

    current_year = current_date[0:4]
    current_month = current_date[5:7]
    current_day = current_date[8:]
    current_month_word = monthСonvert(current_month)
    days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]


    # log = getLoggedUserEtrap(request.user.username)
    context['log'] = log 
    context['etraps'] = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['months'] = months
    context['years'] = ['2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

    etrap = request.GET.get('etrap')

    try:
        number = re.sub('[-]', '', request.GET.get('number'))
        abonent = UserTable.objects.get(etrap=etrap, number=number)
        context['abonent'] = abonent
        if abonent.service:
            pass
        else:
            pass
    except:
        abonent = False

    if abonent:
        abon_services = abonent.service.all()
        # [1,3,4]
        abon_serv_pk_list = []
        for service in abon_services:
            abon_serv_pk_list.append(service.pk)
        context['abon_serv_pk_list'] = abon_serv_pk_list
        context['countOfConnectedService'] = len(abon_serv_pk_list)

    services = AbonentService.objects.all().order_by('price')
    context['services'] = services

    context['number'] = request.GET.get('number')
    context['etrap'] = etrap

    month = request.GET.get('month')
    context['month'] = month

    year = request.GET.get('year')
    context['year'] = year

    if abonent:
        staffAction =  StaffAction.objects.filter(Q(action__icontains='Изменение Услуг') & Q(comment__icontains=abonent.number) & Q(comment__icontains=abonent.etrap))
        staffActionInfo = staffAction.filter(comment__icontains=abonent.number).order_by('-date')
        context['staffActionInfo'] = staffActionInfo

    if request.method == 'POST':
        # ['1','3','4']

        try:
            with transaction.atomic():

                month = request.POST.get('month')
                context['month'] = month

                year = request.POST.get('year')
                context['year'] = year



                pkBoxes = request.POST.getlist('pkBoxes')

                if abonent:
                    mesAdd = 0
                    addedServ = ''
                    mesDel = 0
                    deletedServ = ''
                    total_nach = 0
                    new_pk = []

                    # Подключение новых услуг
                    count = 0
                    for i in pkBoxes:
                        if int(i) not in abon_serv_pk_list:
                            abonent.service.add(AbonentService.objects.get(pk=i))
                            count += 1
                            addedServ += f"""
            {count}){AbonentService.objects.get(pk=i).service}, """
                            mesAdd += 1
                            # old
                            # nach = (days_in_month - int(current_day)) * (AbonentService.objects.get(pk=i).price / days_in_month)
                            # new
                            nach = AbonentService.objects.get(pk=i).price
                            total_nach += nach
                            # abonent.b_dop_uslugi -= nach
                            new_pk.append(i)
                            abonent.save()


                    # {added: [['1','2','3','2023.04.24', 13.61], ['4','2023.04.26', 1.58]], }

                    # Отключение услуг
                    count = 0
                    for i in abon_serv_pk_list:
                        if str(i) not in pkBoxes:
                            abonent.service.remove(AbonentService.objects.get(pk=str(i)))
                            count += 1
                            deletedServ += f"""
            {count}){AbonentService.objects.get(pk=str(i)).service}, """
                            mesDel += 1
                            abonent.save()
        
                    # if total_nach:
                    #     try:
                    #         # old
                    #         # nachMinus = NachMinus.objects.get(user=abonent, month=current_month, year=current_year)  
                    #         # new
                    #         nachMinus = NachMinus.objects.get(user=abonent, month=monthСonvert(month), year=year)  
                    #     except:
                    #         # old
                    #         # nachMinus = NachMinus.objects.create(user=abonent, month=current_month, year=current_year)
                    #         # new
                    #         nachMinus = NachMinus.objects.create(user=abonent, month=monthСonvert(month), year=year)

                    #     if nachMinus.dop_usligi_added_Pk:
                    #         nachMinus.dop_uslugi += total_nach

                    #         added = eval(nachMinus.dop_usligi_added_Pk)
                    #         new_pk.append(current_date)
                    #         new_pk.append(total_nach)
                    #         added['added'].append(new_pk)
                    #         nachMinus.dop_usligi_added_Pk = str(added)
                    #         nachMinus.save()

                    #         # сохраняем начисления для месячного отчета
                    #         try:
                    #             nachisleniyaOtchet = NachisleniyaOtchet.objects.get(year=current_year, month=current_month_word, etrap=etrap)
                    #             nachisleniyaOtchet.serviceSeparateNachisleniya += total_nach
                    #             nachisleniyaOtchet.save()
                    #         except:
                    #             NachisleniyaOtchet.objects.create(year=current_year, month=current_month_word, serviceSeparateNachisleniya=total_nach, etrap=etrap)
                            
                    #     else:
                    #         nachMinus.dop_uslugi += total_nach  

                    #         new_pk.append(current_date)
                    #         new_pk.append(total_nach)
                    #         added = str({"added": [new_pk]})
                    #         nachMinus.dop_usligi_added_Pk = added
                    #         nachMinus.save()

                    #         # сохраняем начисления для месячного отчета
                    #         try:
                    #             nachisleniyaOtchet = NachisleniyaOtchet.objects.get(year=current_year, month=current_month_word, etrap=etrap)
                    #             nachisleniyaOtchet.serviceSeparateNachisleniya += total_nach
                    #             nachisleniyaOtchet.save()
                    #         except:
                    #             NachisleniyaOtchet.objects.create(year=current_year, month=current_month_word, serviceSeparateNachisleniya=total_nach, etrap=etrap)

                    abonentForMess = UserTable.objects.get(etrap=etrap, number=number)
                    abon_services_for_mes = abonent.service.all()
                    haveServices = 'Сейчас у абонента услуг:'
                    countHaveServices = 0
                    if abon_services_for_mes:
                        for service in abon_services_for_mes:
                            countHaveServices += 1
                            haveServices += f"""
            {countHaveServices}) {service.service}"""
                    else:
                        haveServices += ' нет'

                    if mesAdd and mesDel:
                        messages.success(request, f'Добавлено услуг: {mesAdd}; удалено: {mesDel}')
                        StaffAction.objects.create(user=request.user, comment=f"""Абонент: {abonent.number} {abonent.etrap},
        ФИО: {abonent.surname} {abonent.name},
        Добавлено услуг: {addedServ}
        Удалено услуг: {deletedServ}
        {haveServices}
        """, 
                    action='Изменение Услуг')
                    if mesAdd and mesDel == 0:
                        messages.success(request, f'Добавлено услуг: {mesAdd}')
                        StaffAction.objects.create(user=request.user, comment=f"""Абонент: {abonent.number} {abonent.etrap},
        ФИО: {abonent.surname} {abonent.name}
        Добавлено услуг: {addedServ}
        {haveServices}
        """, 
                    action='Изменение Услуг')
                    if mesAdd == 0 and mesDel:
                        messages.success(request, f'Удалено услуг: {mesDel}')
                        StaffAction.objects.create(user=request.user, comment=f"""Абонент: {abonent.number} {abonent.etrap},
        ФИО: {abonent.surname} {abonent.name},
        Удалено услуг: {deletedServ}
        {haveServices}
        """, 
                    action='Изменение Услуг')
                    if mesAdd == 0 and mesDel == 0:
                        messages.success(request, f'Изменений нет')


                    abonent = UserTable.objects.get(etrap=etrap, number=number)
                    abon_services = abonent.service.all()
                    # [1,3,4]
                    abon_serv_pk_list = []
                    for service in abon_services:
                        abon_serv_pk_list.append(service.pk)
                    context['abon_serv_pk_list'] = abon_serv_pk_list
                    context['countOfConnectedService'] = len(abon_serv_pk_list)
                    context['abonent'] = abonent


                    # Сохранение информации об установленных и/или снятых услугах для UstanowkaSnyatieDopUslugHistory
                    if addedServ or deletedServ:
                        if addedServ and not deletedServ:
                            which_type = 'установлено'
                            mes = f"""установлено услуг:{addedServ}"""
                        elif not addedServ and deletedServ:
                            which_type = 'снято'
                            mes = f"""снято услуг:{deletedServ}"""
                        elif addedServ and deletedServ:
                            which_type = 'снято и установлено'
                            mes = f"""снято услуг:{deletedServ}
        установлено услуг:{addedServ}"""
                        ustanowka_snyatie_dopUslug_history = UstanowkaSnyatieDopUslugHistory(
                            user=request.user.username,
                            which_action='в абон-отделе',
                            which_type=which_type,
                            number=abonent.number,
                            etrap=abonent.etrap,
                            comment = f"""{which_type} услуг абонента {abonent.number} {abonent.etrap} (в абон-отделе)
        {mes}"""
                        )
                        ustanowka_snyatie_dopUslug_history.save()

                else:
                    messages.error(request, f'Выберите абонента')

        except Exception as e:
            messages.error(request, f'Откат изменений услуг ошибка с transaction == {e}')
            logger.error(f'==== Откат изменений услуг ошибка с transaction при изменений услуг == {e}')


    return render(request, 'telekom/Service/serviceConnect.html', context)