from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q

import re
from datetime import datetime
from datetime import date
from telekom.models import AbonentService, InterpayBilling, NachMinus, PayHistory, StaffAction, UserTable, UserTableArhiw, UstanowkaSnyatieDopUslugHistory
from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup




def showArhiw(request):
    context = {}
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
        context['log'] = log
        context['matbIndex'] = True
        context['showArhiw'] = True
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    

    
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['etraps'] = etraps
    
    current_date = str(date.today())
    context['current_date'] = current_date
    current_year = current_date[0:4]
    context['current_year'] = current_year
    current_month = current_date[5:7]
    current_day = current_date[8:]

    # if current_month == '01':
    #     last_year = int(current_year) - 1
    #     last_month = '12'
    # else:
    #     last_year = current_year
    #     if current_month == '02':
    #         last_month = '01'
    #     if current_month == '03':
    #         last_month = '02'
    #     if current_month == '04':
    #         last_month = '03'
    #     if current_month == '05':
    #         last_month = '04'
    #     if current_month == '06':
    #         last_month = '05'
    #     if current_month == '07':
    #         last_month = '06'
    #     if current_month == '08':
    #         last_month = '07'
    #     if current_month == '09':
    #         last_month = '08'
    #     if current_month == '10':
    #         last_month = '09'
    #     if current_month == '11':
    #         last_month = '10'
    #     if current_month == '12':
    #         last_month = '11'


    
    # Если нажал на поиск по номеру
    if request.method == 'POST' and 'search_number' in request.POST:
        

        # Если нашлось абонентов больше 1-го и ты выбрал нужного
        if 'choosedUserPk' in request.POST:
            abonent = UserTableArhiw.objects.get(pk=request.POST.get('choosedUserPk'))


        else:
            number = re.sub('[-]', '', request.POST.get('search_number'))
            context['serach_number'] = request.POST.get('search_number')
            context['etrap'] = request.POST.get('etrap')

            # если обычнй поиск (без фильтра кабеля)
            if 'kabelDropdownFilter' not in request.POST and 'choosedUserPk' not in request.POST:
                # Посик по id kabel Tv (номер меньше 5-ти знаков)
                if len(number) <= 4:
                    try:
                        abonentget = UserTableArhiw.objects.get(ids=number, etrap=request.POST.get('etrap'))
                        abonentfilter = False
                    except:
                        abonentget = False
                        abonent = False
                        abonentfilter = UserTableArhiw.objects.filter(ids=number, etrap=request.POST.get('etrap'))

                    if abonentget != False:
                        abonent = abonentget
                        
                    if abonentfilter:
                        if len(abonentfilter) > 1:
                            context['abonentfilter'] = abonentfilter.order_by('-snyat_date')
                            context['serach_number'] = request.POST.get('search_number')
                            context['etrap'] = request.POST.get('etrap')
                            return render(request, 'telekom/MATB/Arhiw/showArhiw.html', context)
                        else:
                            messages.error(request, f'Ошибка! {request.POST.get("search_number")}, нет такого номера')
                        
                # Классический поиск по номеру (если 5-ти значный и больше номер)
                else:
                    try:
                        print('tututu', number, request.POST.get('etrap'))
                        abonentget = UserTableArhiw.objects.get(number=number, etrap=request.POST.get('etrap'))
                        print('tututu2', number, request.POST.get('etrap'))
                        abonentfilter = False
                    except:
                        abonentget = False
                        abonent = False
                        abonentfilter = UserTableArhiw.objects.filter(number=number, etrap=request.POST.get('etrap'))
                        print('tututu3', number, request.POST.get('etrap'), abonentget)

                    if abonentget != False:
                        print('tututu4', number, request.POST.get('etrap'), abonentget)
                        abonent = abonentget

                    if abonentfilter:
                        if len(abonentfilter) > 1:
                            context['abonentfilter'] = abonentfilter.order_by('-snyat_date')
                            context['serach_number'] = request.POST.get('search_number')
                            context['etrap'] = request.POST.get('etrap')
                            return render(request, 'telekom/MATB/Arhiw/showArhiw.html', context)
                        else:
                            messages.error(request, f'Ошибка! {request.POST.get("search_number")}, нет такого номера')


            # Если нажал на поиск по Q для оплаты Кабель TV
            if request.method == 'POST' and 'kabelDropdownFilter' in request.POST:

                surname = request.POST.get('surname') if request.POST.get('surname') != None else ''
                name = request.POST.get('name') if request.POST.get('name') != None else ''
                street = request.POST.get('street') if request.POST.get('street') != None else ''
                home = request.POST.get('home') if request.POST.get('home') != None else ''
                flat = request.POST.get('flat') if request.POST.get('flat') != None else ''
                sotowyy = request.POST.get('sotowyy') if request.POST.get('sotowyy') != None else ''

                context['kabelFilterSurname'] = surname
                context['kabelFilterName'] = name
                context['kabelFilterStreet'] = street
                context['kabelFilterHome'] = home
                context['kabelFilterFlat'] = flat
                context['kabelFilterSotowyy'] = sotowyy
                context['kabelFilterEtrap'] = request.POST.get('etrap') if request.POST.get('etrap') != None else log

                # print(surname, name, street, home, flat, sotowyy)

                abonentfilter = UserTableArhiw.objects.filter(
                    Q(etrap=request.POST.get('etrap')),
                    Q(surname__icontains=surname) &
                    Q(name__icontains=name) &
                    Q(street__icontains=street) &
                    Q(home__icontains=home) &
                    Q(flat__icontains=flat) &
                    Q(sotowyy__icontains=sotowyy)
                )

                if abonentfilter:
                    if len(abonentfilter) == 1:
                        for user in abonentfilter:
                            abonent = UserTableArhiw.objects.get(pk=user.pk)
                    else:
                        context['abonentfilter'] = abonentfilter
                        context['serach_number'] = request.POST.get('search_number')
                        context['etrap'] = request.POST.get('etrap')
                        return render(request, 'telekom/MATB/Arhiw/showArhiw.html', context)
                else:
                    abonent = False
                    messages.error(request, f'Ошибка! {request.POST.get("search_number")}, нет такого номера')
                        
                    #     context['abonent'] = abonent
                    #     context['abonentfilter'] = abonentfilter
                    #     context['serach_number'] = request.POST.get('search_number')
                    #     context['etrap'] = request.POST.get('etrap')
                    #     return render(request, 'telekom/MATB/Arhiw/showArhiw.html', context)
                    # else:
                    #     messages.error(request, f'Ошибка! {request.POST.get("search_number")}, нет такого номера')
        print('abonentFGGGG', abonent)
        if abonent:
            context['abonent'] = abonent
            context['serach_number'] = f"{abonent.number[0]}-{abonent.number[1:3]}-{abonent.number[3:5]}"
            context['etrap'] = request.POST.get('etrap')
            # Находим общую сумму услуг если есть

            if abonent.service:
                service_total_sum = 0
                for service in abonent.service.all():
                    service_total_sum += service.price
            context['service_total_sum'] = service_total_sum

            # nachMinus = NachMinusArhiw.objects.filter(user=abonent)
            # try:
            #     context['jan'] = nachMinus.get(user=abonent, year=current_year, month='01')
            #     if nachMinus.get(user=abonent, year=current_year, month='01').dop_usligi_added_Pk:
            #         added = eval(nachMinus.get(user=abonent, year=current_year, month='01').dop_usligi_added_Pk)
            #         end_list = []
            #         for i in range(len(added['added'])):
            #             start_list = []
            #             date_ = added['added'][i][-2]
            #             nach = added['added'][i][-1]
            #             start_list.append(date_)
            #             start_list.append(nach)
            #             start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
            #             end_list.append(start_list)
            #         context['end_list_jan'] = end_list
            # except: 
            #     pass

            # try:
            #     context['feb'] = nachMinus.get(user=abonent, year=current_year, month='02')
            #     if nachMinus.get(user=abonent, year=current_year, month='02').dop_usligi_added_Pk:
            #         added = eval(nachMinus.get(user=abonent, year=current_year, month='02').dop_usligi_added_Pk)
            #         end_list = []
            #         for i in range(len(added['added'])):
            #             start_list = []
            #             date_ = added['added'][i][-2]
            #             nach = added['added'][i][-1]
            #             start_list.append(date_)
            #             start_list.append(nach)
            #             start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
            #             end_list.append(start_list)
            #         context['end_list_feb'] = end_list
            # except:
            #     pass
            # try:
            #     context['mar'] = nachMinus.get(user=abonent, year=current_year, month='03')
            #     if nachMinus.get(user=abonent, year=current_year, month='03').dop_usligi_added_Pk:
            #         added = eval(nachMinus.get(user=abonent, year=current_year, month='03').dop_usligi_added_Pk)
            #         end_list = []
            #         for i in range(len(added['added'])):
            #             start_list = []
            #             date_ = added['added'][i][-2]
            #             nach = added['added'][i][-1]
            #             start_list.append(date_)
            #             start_list.append(nach)
            #             start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
            #             end_list.append(start_list)
            #         context['end_list_mar'] = end_list
            # except:
            #     pass
            # try:
            #     context['apr'] = nachMinus.get(user=abonent, year=current_year, month='04')
            #     if nachMinus.get(user=abonent, year=current_year, month='04').dop_usligi_added_Pk:
            #         added = eval(nachMinus.get(user=abonent, year=current_year, month='04').dop_usligi_added_Pk)
            #         end_list = []
            #         for i in range(len(added['added'])):
            #             start_list = []
            #             date_ = added['added'][i][-2]
            #             nach = added['added'][i][-1]
            #             start_list.append(date_)
            #             start_list.append(nach)
            #             start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
            #             end_list.append(start_list)
            #         context['end_list_apr'] = end_list
            # except:
            #     pass
            # try:
            #     context['may'] = nachMinus.get(user=abonent, year=current_year, month='05')
            #     if nachMinus.get(user=abonent, year=current_year, month='05').dop_usligi_added_Pk:
            #         added = eval(nachMinus.get(user=abonent, year=current_year, month='05').dop_usligi_added_Pk)
            #         end_list = []
            #         for i in range(len(added['added'])):
            #             start_list = []
            #             date_ = added['added'][i][-2]
            #             nach = added['added'][i][-1]
            #             start_list.append(date_)
            #             start_list.append(nach)
            #             start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
            #             end_list.append(start_list)
            #         context['end_list_may'] = end_list
            # except:
            #     pass
            # try:
            #     context['jun'] = nachMinus.get(user=abonent, year=current_year, month='06')
            #     if nachMinus.get(user=abonent, year=current_year, month='06').dop_usligi_added_Pk:
            #         added = eval(nachMinus.get(user=abonent, year=current_year, month='06').dop_usligi_added_Pk)
            #         end_list = []
            #         for i in range(len(added['added'])):
            #             start_list = []
            #             date_ = added['added'][i][-2]
            #             nach = added['added'][i][-1]
            #             start_list.append(date_)
            #             start_list.append(nach)
            #             start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
            #             end_list.append(start_list)
            #         context['end_list_jun'] = end_list
            # except:
            #     pass
            # try:
            #     context['jul'] = nachMinus.get(user=abonent, year=current_year, month='07')
            #     if nachMinus.get(user=abonent, year=current_year, month='07').dop_usligi_added_Pk:
            #         added = eval(nachMinus.get(user=abonent, year=current_year, month='07').dop_usligi_added_Pk)
            #         end_list = []
            #         for i in range(len(added['added'])):
            #             start_list = []
            #             date_ = added['added'][i][-2]
            #             nach = added['added'][i][-1]
            #             start_list.append(date_)
            #             start_list.append(nach)
            #             start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
            #             end_list.append(start_list)
            #         context['end_list_jul'] = end_list
            # except: 
            #     pass
            # try:
            #     context['aug'] = nachMinus.get(user=abonent, year=current_year, month='08')
            #     if nachMinus.get(user=abonent, year=current_year, month='08').dop_usligi_added_Pk:
            #         added = eval(nachMinus.get(user=abonent, year=current_year, month='08').dop_usligi_added_Pk)
            #         end_list = []
            #         for i in range(len(added['added'])):
            #             start_list = []
            #             date_ = added['added'][i][-2]
            #             nach = added['added'][i][-1]
            #             start_list.append(date_)
            #             start_list.append(nach)
            #             start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
            #             end_list.append(start_list)
            #         context['end_list_aug'] = end_list
            # except: 
            #     pass
            # try:
            #     context['sep'] = nachMinus.get(user=abonent, year=current_year, month='09')
            #     if nachMinus.get(user=abonent, year=current_year, month='09').dop_usligi_added_Pk:
            #         added = eval(nachMinus.get(user=abonent, year=current_year, month='09').dop_usligi_added_Pk)
            #         end_list = []
            #         for i in range(len(added['added'])):
            #             start_list = []
            #             date_ = added['added'][i][-2]
            #             nach = added['added'][i][-1]
            #             start_list.append(date_)
            #             start_list.append(nach)
            #             start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
            #             end_list.append(start_list)
            #         context['end_list_sep'] = end_list
            # except: 
            #     pass
            # try:
            #     context['oct'] = nachMinus.get(user=abonent, year=current_year, month='10')
            #     if nachMinus.get(user=abonent, year=current_year, month='10').dop_usligi_added_Pk:
            #         added = eval(nachMinus.get(user=abonent, year=current_year, month='10').dop_usligi_added_Pk)
            #         end_list = []
            #         for i in range(len(added['added'])):
            #             start_list = []
            #             date_ = added['added'][i][-2]
            #             nach = added['added'][i][-1]
            #             start_list.append(date_)
            #             start_list.append(nach)
            #             start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
            #             end_list.append(start_list)
            #         context['end_list_oct'] = end_list
            # except: 
            #     pass
            # try:
            #     context['nov'] = nachMinus.get(user=abonent, year=current_year, month='11')
            #     if nachMinus.get(user=abonent, year=current_year, month='11').dop_usligi_added_Pk:
            #         added = eval(nachMinus.get(user=abonent, year=current_year, month='11').dop_usligi_added_Pk)
            #         end_list = []
            #         for i in range(len(added['added'])):
            #             start_list = []
            #             date_ = added['added'][i][-2]
            #             nach = added['added'][i][-1]
            #             start_list.append(date_)
            #             start_list.append(nach)
            #             start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
            #             end_list.append(start_list)
            #         context['end_list_nov'] = end_list
            # except:
            #     pass
            # try:
            #     context['dec'] = nachMinus.get(user=abonent, year=current_year, month='12')
            #     if nachMinus.get(user=abonent, year=current_year, month='12').dop_usligi_added_Pk:
            #         added = eval(nachMinus.get(user=abonent, year=current_year, month='12').dop_usligi_added_Pk)
            #         end_list = []
            #         for i in range(len(added['added'])):
            #             start_list = []
            #             date_ = added['added'][i][-2]
            #             nach = added['added'][i][-1]
            #             start_list.append(date_)
            #             start_list.append(nach)
            #             start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
            #             end_list.append(start_list)
            #         context['end_list_dec'] = end_list
            # except:
            #     pass


    # Если нажал на востановить
    if request.method == 'POST' and 'wost' in request.POST or 'Another' in request.POST:

        if 'Another' in request.POST:
            abonentArhiw = UserTableArhiw.objects.get(pk=request.POST.get('Another'))
            if request.POST.get('numberToWost'):
                try:
                    abonentBase = UserTable.objects.get(number=request.POST.get('numberToWost'), etrap=request.POST.get('etrapToWost'))
                except:
                    abonentBase = 'Нет такого номера'         
            else:
                abonentBase = 'Выберите номер'     
        else:
            abonentArhiw = UserTableArhiw.objects.get(pk=request.POST.get('wost'))
            abonentBase = UserTable.objects.get(number=abonentArhiw.number, etrap=abonentArhiw.etrap)

        context['abonent'] = abonentArhiw

        context['serach_number'] = f"{abonentArhiw.number[0]}-{abonentArhiw.number[1:3]}-{abonentArhiw.number[3:5]}"
        context['etrap'] = request.POST.get('etrap')

        if request.POST.get('comment') == '':
            messages.error(request, f"Оставьте комментарий")
        else:

            if abonentBase == 'Нет такого номера':
                messages.error(request, f"Номер ({request.POST.get('numberToWost')}) на который вы хотите востановить абонента не существует")
            elif abonentBase == 'Выберите номер':
                messages.error(request, f"Выберите номер на который хотите востановить абонента")
            elif abonentBase.name != '' or abonentBase.surname != '':
                context['abonent'] = abonentArhiw
                context['serach_number'] = f"{abonentArhiw.number[0]}-{abonentArhiw.number[1:3]}-{abonentArhiw.number[3:5]}"
                context['etrap'] = request.POST.get('etrap')
                messages.error(request, f"Ошибка! {abonentBase.etrap} {abonentBase.number[0]}-{abonentBase.number[1:3]}-{abonentBase.number[3:5]} не свободен")
            else:
                abonentBase.surname = abonentArhiw.surname
                abonentBase.name = abonentArhiw.name
                abonentBase.street = abonentArhiw.street
                abonentBase.home = abonentArhiw.home
                abonentBase.flat = abonentArhiw.flat
                abonentBase.sotowyy = abonentArhiw.sotowyy
                abonentBase.is_enterprises = abonentArhiw.is_enterprises


                abonentBase.account = abonentArhiw.account
                abonentBase.hb = abonentArhiw.hb
       
                abonentBase.internet_connect_date = abonentArhiw.internet_connect_date
                abonentBase.internet_disconnect_date = abonentArhiw.internet_disconnect_date


                abonentBase.abonplata = abonentArhiw.abonplata
                abonentBase.snyat_date = None
                abonentBase.beneficiary = abonentArhiw.beneficiary

                if abonentArhiw.service.exists():
                    mess_set_serv = ""
                    mess_set_serv_count = 0
                    for i in abonentArhiw.service.all():
                        mess_set_serv_count += 1
                        mess_set_serv += f"""{mess_set_serv_count}) {i.service}
    """
                        abonentBase.service.add(i)

                    # сохраняем информацию о том что услуги были востановлены (установлены) для StaffAction
                    StaffAction.objects.create(user=request.user, comment=f"""Востановлены(установлены) услуг при востановлении с архива.
Востановление абонента {abonentArhiw.number} {abonentArhiw.etrap}.
Востановлено услуг:
    {mess_set_serv}
""", 
                    action='Изменение Услуг')

                    # Сохраняем (Устанавливаем) услуги в UstanowkaSnyatieDopUslugHistory
                    UstanowkaSnyatieDopUslugHistory.objects.create(
                        user=request.user.username,
                        which_action='при востановлении с архива',
                        which_type='установлено',
                        number=abonentArhiw.number,
                        etrap=abonentArhiw.etrap,
                        comment = f"""Установка услуг при востановлении абонента с архива {abonentArhiw.number} {abonentArhiw.etrap}
Установлено услуг:
    {mess_set_serv
}"""
                )

                abonentBase.login = abonentArhiw.login
                abonentBase.dogowor = abonentArhiw.dogowor
                abonentBase.wost_date = datetime.now()

                abonentBase.save()

       

                abonentArhiw.wost_date = datetime.now()
                abonentArhiw.save()

                context['abonent'] = abonentArhiw

                context['serach_number'] = f"{abonentArhiw.number[0]}-{abonentArhiw.number[1:3]}-{abonentArhiw.number[3:5]}"
                context['etrap'] = request.POST.get('etrap')

                if 'Another' in request.POST:
                    StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')}\n\nВостановления номера {abonentArhiw.number} etrap {abonentArhiw.etrap} pk номер: {abonentArhiw.pk} \nна другой номер: {abonentBase.number} {abonentBase.etrap}\n\nДата востановления {datetime.now()}", action='Востановление номера')
                    messages.success(request, f"Успешное востановления номера {abonentArhiw.number} {abonentArhiw.etrap}")
                else:
                    StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')}\n\nВостановления номера {abonentArhiw.number} etrap {abonentArhiw.etrap} pk номер: {abonentArhiw.pk}\n\nДата востановления {datetime.now()}", action='Востановление номера')
                    messages.success(request, f"Успешное востановления номера {abonentArhiw.number} {abonentArhiw.etrap}")
         
                
    return render(request, 'telekom/MATB/Arhiw/showArhiw.html', context)
