from django.shortcuts import render, redirect
from django.contrib import messages

from django.db.models import Q

from datetime import date
from datetime import datetime
from calendar import monthrange
import re

from telekom.models import InternetTarif, KabelCount, NachMinus, NachisleniyaOtchet, StaffAction, UserTable

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert



def kabelTvAddUser(request):
    # if request.user.username[:4] == 'matb' or request.user.username[:-1] == 'admin' or request.user.username[:7] == 'service':

    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or EtrapAndGroup[1] == 'MB' or EtrapAndGroup[1] == 'SHB' or  request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам MATB и Абон-отдела')
        return redirect('user-login')


    context = {}

    if EtrapAndGroup[1] == 'MATB' or request.user.is_superuser:
        context['matbIndex'] = True
        context['kabelTvAddUser'] = True
    if EtrapAndGroup[1] == 'MB':
        context['setService'] = True
        context['kabelTvAddUser'] = True
    if EtrapAndGroup[1] == 'SHB':
        context['SHBIndex'] = True
        context['kabelTvAddUser'] = True

    # if request.user.username[:4] == 'matb' or request.user.username[:-1] == 'admin':
    #     context['matbIndex'] = True
    #     context['kabelTvAddUser'] = True
    # if request.user.username[:-1] == 'admin' or request.user.username[:7] == 'service':
    #     context['setService'] = True
        # context['kabelTvAddUser'] = True

    # log = getLoggedUserEtrap(request.user.username)
    context['log'] = log
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['etraps'] = etraps

    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date
    current_year = current_date[0:4]
    current_month = current_date[5:7]
    current_day = current_date[8:]
    days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]

    



    # log = getLoggedUserEtrap(request.user.username)
    # context['log'] = log 
    context['etraps'] = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

    if request.GET.get('etrap') != None and request.GET.get('etrap') != 'all':
        etrap = request.GET.get('etrap')
    else:
        etrap = ''

    if request.GET.get('number') != None:
        number = re.sub('[-]', '', request.GET.get('number'))
    else:
        number = ''

    old_id = request.GET.get('old_id') if request.GET.get('old_id') != None else ''
    surname = request.GET.get('surname') if request.GET.get('surname') != None else ''
    name = request.GET.get('name') if request.GET.get('name') != None else ''

    street = request.GET.get('street') if request.GET.get('street') != None else ''
    home = request.GET.get('home') if request.GET.get('home') != None else ''
    flat = request.GET.get('flat') if request.GET.get('flat') != None else ''

    sotowyy = request.GET.get('sotowyy') if request.GET.get('sotowyy') != None else ''

    # print('etrap', etrap)
    # print('number', number)
    # print('old_id', old_id)
    # print('surname', surname)
    # print('name', name)
    # print('street', street)
    # print('home', home)
    # print('flat', flat)
    # print('sotowyy', sotowyy)

    tarifs = KabelCount.objects.all()
    context['tarifs'] = tarifs




    context['etrap'] = request.GET.get('etrap')
    context['number'] = request.GET.get('number')
    context['old_id'] = old_id
    context['surname'] = surname
    context['name'] = name
    context['street'] = street
    context['home'] = home
    context['flat'] = flat
    context['sotowyy'] = sotowyy

    # users = UserTable.objects.filter(etrap=etrap).exclude(service=None)

    users = UserTable.objects.filter(
    Q(etrap__icontains=etrap) &
    Q(number__icontains=number) &
    Q(ids__icontains=old_id) &
    Q(surname__icontains=surname) &
    Q(name__icontains=name) &
    Q(street__icontains=street) &
    Q(home__icontains=home) &
    Q(flat__icontains=flat) &
    Q(sotowyy__icontains=sotowyy)
    )[:25]

    context['users'] = users

    if len(users) == 1:
        for user in users:
            oneUser = user
            context['oneUser'] = oneUser

            if user.kabel_count:
                current_tarif_pk = user.kabel_count.pk
            else:
                current_tarif_pk = 'off'
            context['current_tarif_pk'] = current_tarif_pk




    # Если нажал на сохранить
    if request.method == 'POST' and 'user_ID' not in request.POST:
        if request.POST.get('comment') != '':
            
            message = ''
            user_id = request.POST.get('pk')
            if request.POST.get('is_on') == 'on':
                new_is_on = True
            else:
                new_is_on = False

            abonent = UserTable.objects.get(pk=user_id)
            if abonent.kabel_count:
                current_tarif_pk = abonent.kabel_count.pk
                if abonent.is_on:
                    current_is_on = True
                else:
                    current_is_on = False
            else:
                current_tarif_pk = 'off'
                current_is_on = False

            old_name = abonent.name
            old_surname = abonent.surname
            old_street = abonent.street
            old_home = abonent.home
            old_flat = abonent.flat
            old_sotowyy = abonent.sotowyy
            old_is_enterprises = abonent.is_enterprises

            new_name = request.POST.get('name')
            new_surname = request.POST.get('surname')
            new_street = request.POST.get('street')
            new_home = request.POST.get('home')
            new_flat = request.POST.get('flat')
            new_sotowyy = request.POST.get('sotowyy')

            if request.POST.get('is_enterprises') == 'on':
                new_is_enterprises = True
            else:
                new_is_enterprises = False



            new_tarif_pk = request.POST.get('tarif_pk')

            # Если нет изменений то нечего сохранять
            if str(new_tarif_pk) == str(current_tarif_pk) and new_is_on == current_is_on and old_name == new_name and old_surname == new_surname and old_street == new_street and old_home == new_home and old_flat == new_flat and old_sotowyy == new_sotowyy and old_is_enterprises == new_is_enterprises:
                messages.error(request, f'Изменений нет')
            else:
                if str(new_tarif_pk) != str(current_tarif_pk) or new_is_on != current_is_on:
                    # Код для изменения тарифа 1 - го числа (без начислений, будет начисляться только в MATB)
                    # Если не равны значит либо изменен либо, отключен, либо включен новый тариф (с нуля)
                    if str(new_tarif_pk) != str(current_tarif_pk): 
                        if new_tarif_pk != 'off' and current_tarif_pk != 'off':
                            # Смена тарифа
                            abonent.kabel_count = KabelCount.objects.get(pk=new_tarif_pk)

                            message += f"Смена точки с {KabelCount.objects.get(pk=str(current_tarif_pk)).kabel_count} на {KabelCount.objects.get(pk=str(new_tarif_pk)).kabel_count}, {abonent.number}, {abonent.ids}, {abonent.street}, {abonent.home}, {abonent.flat}"
                            # Если есть изменения в вкл/выкл
                            if new_is_on != current_is_on:
                                if new_is_on == False:
                                    message += f", Статус отключен"
                                    abonent.is_on = False
                                    abonent.is_on_date = None
                                else:
                                    message += f", Статус включен"
                                    abonent.is_on = True
                                    abonent.is_on_date = datetime.now()

                            staffActionComment = message

                        if new_tarif_pk == 'off' and current_tarif_pk != 'off':
                            # Отключения тарифа
                            abonent.is_on = False
                            abonent.connect_date = None
                            message += f"Отключения тарифа {KabelCount.objects.get(pk=str(current_tarif_pk)).kabel_count} точек, , {abonent.number}, {abonent.ids}, {abonent.street}, {abonent.home}, {abonent.flat}"

                            if current_is_on == True:
                                abonent.is_on = False
                                abonent.is_on_date = None

                            staffActionComment = message

                        if new_tarif_pk != 'off' and current_tarif_pk == 'off':
                            # подключения тарифа
                            abonent.kabel_count = KabelCount.objects.get(pk=new_tarif_pk)
                            abonent.connect_date = datetime.now()
                            message += f"Подключения {KabelCount.objects.get(pk=new_tarif_pk).kabel_count} точек, {abonent.number}, {abonent.ids}, {abonent.street}, {abonent.home}, {abonent.flat}"
                            
                            if new_is_on == True:
                                # Если подключил новый тариф (с нуля) и включил кабель
                                abonent.is_on = True
                                abonent.is_on_date = datetime.now()
                                message += f', Статус Включен, , {abonent.number}, {abonent.ids}, {abonent.street}, {abonent.home}, {abonent.flat}'
                            else:
                                abonent.is_on = False

                            staffActionComment = message

                    # если нет изменений в тарифе (значит изменения только в отк/вкл) (тариф не off)
                    if str(new_tarif_pk) == str(current_tarif_pk) and str(current_tarif_pk) != 'off':
                        # если есть изменения в отк/вкл
                        if new_is_on == True:
                            # включение
                            abonent.is_on = True
                            abonent.is_on_date = datetime.now()
                            message =  f'Статус включен. Тариф не изменен: {abonent.kabel_count.kabel_count} точек, {abonent.number}, {abonent.ids}, {abonent.street}, {abonent.home}, {abonent.flat}'
                            staffActionComment = message

                        # если тупо отключили без изменения тарифа (тариф не off)
                        if new_is_on == False and current_is_on == True:
                            # отключение
                            abonent.is_on = False
                            abonent.is_on_date = None
                            message = f'Статус отключен. Тариф не изменен: {abonent.kabel_count.kabel_count} точек, {abonent.number}, {abonent.ids}, {abonent.street}, {abonent.home}, {abonent.flat}'
                            staffActionComment = message

                    StaffAction.objects.create(user=request.user, comment=staffActionComment, action='Кабель TV действия')

                    context['oneUser'] = abonent

                    if abonent.kabel_count:
                        current_tarif_pk = abonent.kabel_count.pk
                    else:
                        current_tarif_pk = 'off'
                    abonent.kabel_comments = f"{request.POST.get('comment')} \n\n {staffActionComment}, изменил {request.user.username}, дата {datetime.now()}"

                    
                    messages.success(request, f'{message}')
                

                abonent.name = new_name
                abonent.surname = new_surname
                abonent.street = new_street
                abonent.home = new_home
                abonent.flat = new_flat
                abonent.sotowyy = new_sotowyy
                abonent.is_enterprises = new_is_enterprises
                if str(new_tarif_pk) == str(current_tarif_pk) and new_is_on == current_is_on:
                    abonent.kabel_comments = f"{request.POST.get('comment')}, изменил {request.user.username}, дата {datetime.now()}, {abonent.number}, {abonent.ids}, {abonent.street}, {abonent.home}, {abonent.flat}"

                abonent.save()
                
                context['oneUser'] = abonent

        else:
            messages.error(request, f'Оставьте примечание')
    
    get_last_empty_number_dz = UserTable.objects.filter(number__gte='100000', number__lte = '110000', etrap='Dashoguz', name='', surname='').order_by('number')
    get_last_empty_number_ak = UserTable.objects.filter(number__gte='100000', number__lte = '110000', etrap='Akdepe', name='', surname='').order_by('number')
    get_last_empty_number_bol = UserTable.objects.filter(number__gte='100000', number__lte = '110000', etrap='Boldumsaz', name='', surname='').order_by('number')
    get_last_empty_number_gor = UserTable.objects.filter(number__gte='100000', number__lte = '110000', etrap='Gorogly', name='', surname='').order_by('number')
    get_last_empty_number_kone = UserTable.objects.filter(number__gte='100000', number__lte = '110000', etrap='Koneurgench', name='', surname='').order_by('number')
    get_last_empty_number_turk = UserTable.objects.filter(number__gte='100000', number__lte = '110000', etrap='Turkmenbashy', name='', surname='').order_by('number')
    get_last_empty_number_nyyaz = UserTable.objects.filter(number__gte='100000', number__lte = '110000', etrap='S.A.Nyyazow', name='', surname='').order_by('number')
    get_last_empty_number_ruh = UserTable.objects.filter(number__gte='100000', number__lte = '110000', etrap='Ruhubelent', name='', surname='').order_by('number')

    context['lastEmptyNumberDz'] = get_last_empty_number_dz[0].number 
    context['get_last_empty_number_ak'] = get_last_empty_number_ak[0].number 
    context['get_last_empty_number_bol'] = get_last_empty_number_bol[0].number 
    context['get_last_empty_number_gor'] = get_last_empty_number_gor[0].number 
    context['get_last_empty_number_kone'] = get_last_empty_number_kone[0].number 
    context['get_last_empty_number_turk'] = get_last_empty_number_turk[0].number 
    context['get_last_empty_number_nyyaz'] = get_last_empty_number_nyyaz[0].number 
    context['get_last_empty_number_ruh'] = get_last_empty_number_ruh[0].number 


    return render(request, 'telekom/MATB/kabelTvAddUser.html', context)

    # else:
    #     messages.error(request, f'Вход в MATB разрешено только соотрудникам MATB')
    #     return redirect('user-login')