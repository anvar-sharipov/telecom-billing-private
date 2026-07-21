
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages

# Не работает в Apache
# from openpyxl import Workbook
from telekom.models import KabelCount, NachMinus, NachisleniyaOtchet, PayHistory, StaffAction, UserTable
from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert

from datetime import date, datetime

from calendar import monthrange
# Для минуса месяцев с даты
from dateutil.relativedelta import relativedelta
import re





def kabelTvInfo(request):
    context = {}
    # if request.user.username[:4] == 'matb' or request.user.username[:-1] == 'admin' or request.user.username[:7] == 'service':
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or EtrapAndGroup[1] == 'MB' or EtrapAndGroup[1] == 'SHB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
        if EtrapAndGroup[1] == 'MB' or EtrapAndGroup[1] == 'SHB':
            context['my_disabled'] = False
        else:
            context['my_disabled'] = True
    else:
        messages.error(request, f'Доступ только соотрудникам MATB и Абон-отдела')
        return redirect('user-login')
    
    

    if EtrapAndGroup[1] == 'MATB' or request.user.is_superuser:
        context['matbIndex'] = True
        context['kabelTvInfo'] = True
    if EtrapAndGroup[1] == 'MB':
        context['setService'] = True
        context['kabelTvInfo'] = True
    if EtrapAndGroup[1] == 'SHB':
        context['SHBIndex'] = True
        context['kabelTvInfo'] = True

    # if request.user.username[:4] == 'matb' or  request.user.username[:-1] == 'admin':
    #     context['matbIndex'] = True
    #     context['kabelTvInfo'] = True
    # if request.user.username[:-1] == 'admin' or request.user.username[:7] == 'service':
    #     context['setService'] = True
    #     context['kabelTvInfo'] = True


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

    ids = request.GET.get('kabelIdSearch') if request.GET.get('kabelIdSearch') != None else ''
    etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else ''
    surname = request.GET.get('kabelSurnameSearch') if request.GET.get('kabelSurnameSearch') != None else ''
    name = request.GET.get('kabelNameSearch') if request.GET.get('kabelNameSearch') != None else ''
    street = request.GET.get('kabelStreetSearch') if request.GET.get('kabelStreetSearch') != None else ''
    home = request.GET.get('kabelHomeSearch') if request.GET.get('kabelHomeSearch') != None else ''
    flat = request.GET.get('kabelFlatSearch') if request.GET.get('kabelFlatSearch') != None else ''
    kabel_count = request.GET.get('kabelCountSearch') if request.GET.get('kabelCountSearch') != None else ''

    balanceEnd = request.GET.get('kabelBalanceSearchEnd')
    balanceStart = request.GET.get('kabelBalanceSearchStart')

    number = re.sub('[-]', '', request.GET.get('kabelNumberSearch')) if request.GET.get('kabelNumberSearch') != None else ''
    sotowyy = request.GET.get('kabelSotowyySearch') if request.GET.get('kabelSotowyySearch') != None else ''
    start = request.GET.get('kabelConnect_dateSearchStart')
    end = request.GET.get('kabelConnect_dateSearchEnd')
    is_on = request.GET.get('is_on') if request.GET.get('is_on') != None else ''
    is_enterprises = request.GET.get('is_enterprises') if request.GET.get('is_enterprises') != None else ''

    # is_onSort is_enterprisesSort ids etrap surname name street home flat kabel_count balanceStart balanceEnd number sotowyy start end is_on is_enterprises


    is_onSort = request.GET.get('is_onSort') if request.GET.get('is_onSort') != None else ''
    is_enterprisesSort = request.GET.get('is_enterprisesSort') if request.GET.get('is_enterprisesSort') != None else ''


    context['is_onSort'] = is_on
    context['is_enterprisesSort'] = is_enterprises

    context['ids'] = ids
    context['etrap'] = etrap
    context['surname'] = surname
    context['name'] = name
    context['street'] = street
    context['home'] = home
    context['flat'] = flat
    context['kabel_count'] = kabel_count

    context['balanceStart'] = balanceStart
    context['balanceEnd'] = balanceEnd

    context['number'] = request.GET.get('kabelNumberSearch') if request.GET.get('kabelNumberSearch') != None else ''
    context['sotowyy'] = sotowyy
    context['start'] = start
    context['end'] = end
    context['is_on'] = is_on
    context['is_enterprises'] = is_enterprises

    users = UserTable.objects.filter(
        Q(ids__icontains=ids) &
        Q(etrap__icontains=etrap) &
        Q(surname__icontains=surname) &
        Q(name__icontains=name) &
        Q(street__icontains=street) &
        Q(home__icontains=home) &
        Q(flat__icontains=flat) &
        Q(kabel_count__kabel_count__icontains=kabel_count) &
        Q(number__icontains=number) &
        Q(sotowyy__icontains=sotowyy) 
        ).exclude(kabel_count=None)
    
    
    # Если нажал на сброс фильтров и сортировок
    if request.method == 'POST' and 'sbros' in request.POST:
        context['sort'] = False
        return redirect('kabel-tv-info')

    # Если нажал на посмотреть все
    if request.method == 'POST' and 'sort' in request.POST:
        if request.POST.get('sort'):
            users = users.order_by(request.POST.get('sort'))
        context['sort'] = request.POST.get('sort')

    # Если нажал на скачать xlsx
    if request.method == 'POST' and 'xlsx_sort' in request.POST:
        users = UserTable.objects.filter(
                Q(ids__icontains=ids) &
                Q(etrap__icontains=etrap) &
                Q(surname__icontains=surname) &
                Q(name__icontains=name) &
                Q(street__icontains=street) &
                Q(home__icontains=home) &
                Q(flat__icontains=flat) &
                Q(kabel_count__kabel_count__icontains=kabel_count) &
                Q(number__icontains=number) &
                Q(sotowyy__icontains=sotowyy) 
                ).exclude(kabel_count=None)
        
        if request.POST.get('xlsx_sort'):
            users = users.order_by(request.POST.get('xlsx_sort'))
        
        # is_onSort = request.POST.get('is_onSort')
        # is_enterprisesSort = request.POST.get('is_enterprisesSort')
        if is_onSort == 'On' and is_enterprisesSort == '':
            users = users.filter(is_on=True)
            context['is_onSort'] = 'On'
            context['is_enterprisesSort'] = ''

        if is_onSort == 'On' and is_enterprisesSort == 'Off':
            users = users.filter(is_on=True, is_enterprises=False)
            context['is_onSort'] = 'On'
            context['is_enterprisesSort'] = 'Off'

        if is_onSort == 'On' and is_enterprisesSort == 'On':
            users = users.filter(is_on=True, is_enterprises=True)
            context['is_onSort'] = 'On'
            context['is_enterprisesSort'] = 'On'
        
        if is_onSort == 'Off' and is_enterprisesSort == '':
            users = users.filter(is_on=False)
            context['is_onSort'] = 'Off'
            context['is_enterprisesSort'] = ''

        if is_onSort == 'Off' and is_enterprisesSort == 'On':
            users = users.filter(is_on=False, is_enterprises=True)
            context['is_onSort'] = 'Off'
            context['is_enterprisesSort'] = 'On'

        if is_onSort == 'Off' and is_enterprisesSort == 'Off':
            users = users.filter(is_on=False, is_enterprises=False)
            context['is_onSort'] = 'Off'
            context['is_enterprisesSort'] = 'Off'

        if is_onSort == '' and is_enterprisesSort == 'On':
            users = users.filter(is_enterprises=True)
            context['is_onSort'] = ''
            context['is_enterprisesSort'] = 'On'

        if is_onSort == '' and is_enterprisesSort == 'Off':
            users = users.filter(is_enterprises=False)
            context['is_onSort'] = ''
            context['is_enterprisesSort'] = 'Off'

        context['sort'] = request.POST.get('xlsx_sort')

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Kabel-TV-Info {current_date}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'Kabel-TV-Info {current_date}'

        # Add headers
        headers = ['ID', 'Этрап', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Квартира', 'Точки', 'Баланс', 'Номер', 'Сотовый', 'Дата Подключения', 'Вкл?', 'Предприятие?', 'Примечание']
        ws.append(headers)

        # add Data
        for user in users:
            if user.is_on:
                userIs_on = 'Вкл'
            else:
                userIs_on = ''
            
            if user.is_enterprises:
                userIs_enterprises = 'Да'
            else:
                userIs_enterprises = ''

            ws.append([user.ids, user.etrap, user.surname, user.name, user.street, user.home, user.flat, user.kabel_count.kabel_count, "%.2f" % user.b_kabel, user.number, user.sotowyy, user.connect_date, userIs_on, userIs_enterprises, user.kabel_comments])

        # save
        wb.save(response)
        return response
    
    if start and end:
        end = str(end) + f" 23:59:59"
        users = users.filter(connect_date__range=[start, end])

    if is_on == 'On' and is_enterprises == '':
        users = users.filter(is_on=True)
        context['is_onSort'] = 'On'
        context['is_enterprisesSort'] = ''
    if is_on == 'On' and is_enterprises == 'Off':
        users = users.filter(is_on=True, is_enterprises=False)
        context['is_onSort'] = 'On'
        context['is_enterprisesSort'] = 'Off'
    if is_on == 'On' and is_enterprises == 'On':
        users = users.filter(is_on=True, is_enterprises=True)
        context['is_onSort'] = 'On'
        context['is_enterprisesSort'] = 'On'
    if is_on == 'Off' and is_enterprises == '':
        users = users.filter(is_on=False)
        context['is_onSort'] = 'Off'
        context['is_enterprisesSort'] = ''
    if is_on == 'Off' and is_enterprises == 'On':
        users = users.filter(is_on=False, is_enterprises=True)
        context['is_onSort'] = 'Off'
        context['is_enterprisesSort'] = 'On'
    if is_on == 'Off' and is_enterprises == 'Off':
        users = users.filter(is_on=False, is_enterprises=False)
        context['is_onSort'] = 'Off'
        context['is_enterprisesSort'] = 'Off'
    if is_enterprises == 'On' and is_on == '':
        users = users.filter(is_enterprises=True)
        context['is_onSort'] = ''
        context['is_enterprisesSort'] = 'On'
    if is_enterprises == 'Off' and is_on == '':
        users = users.filter(is_enterprises=False)
        context['is_onSort'] = ''
        context['is_enterprisesSort'] = 'Off'

    if balanceStart and balanceEnd:
        users = users.filter(b_kabel__gte=balanceStart).filter(b_kabel__lte=balanceEnd)

    if request.method == 'POST' and 'ids' in request.POST:
        users = users.order_by(request.POST.get('ids'))
        context['sort'] = request.POST.get('ids')
    
    if request.method == 'POST' and 'surname' in request.POST:
        users = users.order_by(request.POST.get('surname'))
        context['sort'] = request.POST.get('surname')

    if request.method == 'POST' and 'name' in request.POST:
        users = users.order_by(request.POST.get('name'))
        context['sort'] = request.POST.get('name')

    if request.method == 'POST' and 'street' in request.POST:
        users = users.order_by(request.POST.get('street'))
        context['sort'] = request.POST.get('street')

    if request.method == 'POST' and 'home' in request.POST:
        users = users.order_by(request.POST.get('home'))
        context['sort'] = request.POST.get('home')

    if request.method == 'POST' and 'flat' in request.POST:
        users = users.order_by(request.POST.get('flat'))
        context['sort'] = request.POST.get('flat')

    if request.method == 'POST' and 'kabel_count' in request.POST:
        users = users.order_by(request.POST.get('kabel_count'))
        context['sort'] = request.POST.get('kabel_count')
    
    if request.method == 'POST' and 'balance' in request.POST:
        users = users.order_by(request.POST.get('balance'))
        context['sort'] = request.POST.get('balance')

    if request.method == 'POST' and 'number' in request.POST:
        users = users.order_by(request.POST.get('number'))
        context['sort'] = request.POST.get('number')

    if request.method == 'POST' and 'sotowyy' in request.POST:
        users = users.order_by(request.POST.get('sotowyy'))
        context['sort'] = request.POST.get('sotowyy')

    if request.method == 'POST' and 'connect_date' in request.POST:
        users = users.order_by(request.POST.get('connect_date'))
        context['sort'] = request.POST.get('connect_date')

    
    # else:
    #     # Если только зашел и нет никаких сортировок и фильтров
    #     users = UserTable.objects.filter(
    #             Q(ids__icontains=ids) &
    #             Q(etrap__icontains=etrap) &
    #             Q(surname__icontains=surname) &
    #             Q(name__icontains=name) &
    #             Q(street__icontains=street) &
    #             Q(home__icontains=home) &
    #             Q(flat__icontains=flat) &
    #             Q(kabel_count__kabel_count__icontains=kabel_count) &
    #             Q(number__icontains=number) &
    #             Q(sotowyy__icontains=sotowyy) 
    #             ).exclude(kabel_count=None)

    #############################################################################################################################
    # Вывод в xlsx формат всех у кого баланс в минусе и оплат небыло Месяц, 2 Месяца, 3 Месяца, 4 Месяца, 5 Месяцев, 6 Месяцев ##
    #############################################################################################################################
    if request.method == 'POST' and 'oneMonthMinus' in request.POST:
    
        start = str(date.today() - relativedelta(months=1)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        payHistory = PayHistory.objects.all()
        new_users = []
        for user in users:
            if user.b_kabel < 0:
                pays = payHistory.filter(abonent=user, date__range=[start, end], kabel__gt=0)
                if len(pays) == 0:
                    new_users.append(user)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Kabel-TV-Info {current_date}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'Kabel-TV-Info {current_date}'
        headers = ['ID', 'Этрап', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Квартира', 'Точки', 'Баланс', 'Номер', 'Сотовый', 'Дата Подключения', 'Вкл?', 'Предприятие?', 'Примечание']
        ws.append(headers)
        for user in new_users:
            if user.is_on:
                userIs_on = 'Вкл'
            else:
                userIs_on = ''
            
            if user.is_enterprises:
                userIs_enterprises = 'Да'
            else:
                userIs_enterprises = ''
            ws.append([user.ids, user.etrap, user.surname, user.name, user.street, user.home, user.flat, user.kabel_count.kabel_count, "%.2f" % user.b_kabel, user.number, user.sotowyy, user.connect_date, userIs_on, userIs_enterprises, user.kabel_comments])
        wb.save(response)
        return response

    if request.method == 'POST' and 'twoMonthMinus' in request.POST:
        
        start = str(date.today() - relativedelta(months=2)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        payHistory = PayHistory.objects.all()
        new_users = []
        for user in users:
            if user.b_kabel < 0:
                pays = payHistory.filter(abonent=user, date__range=[start, end], kabel__gt=0)
                if len(pays) == 0:
                    new_users.append(user)
        
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Kabel-TV-Info {current_date}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'Kabel-TV-Info {current_date}'
        headers = ['ID', 'Этрап', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Квартира', 'Точки', 'Баланс', 'Номер', 'Сотовый', 'Дата Подключения', 'Вкл?', 'Предприятие?', 'Примечание']
        ws.append(headers)
        for user in new_users:
            if user.is_on:
                userIs_on = 'Вкл'
            else:
                userIs_on = ''
            
            if user.is_enterprises:
                userIs_enterprises = 'Да'
            else:
                userIs_enterprises = ''
            ws.append([user.ids, user.etrap, user.surname, user.name, user.street, user.home, user.flat, user.kabel_count.kabel_count, "%.2f" % user.b_kabel, user.number, user.sotowyy, user.connect_date, userIs_on, userIs_enterprises, user.kabel_comments])
        wb.save(response)
        return response

    if request.method == 'POST' and 'threeMonthMinus' in request.POST:
        
        start = str(date.today() - relativedelta(months=3)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        payHistory = PayHistory.objects.all()
        new_users = []
        for user in users:
            if user.b_kabel < 0:
                pays = payHistory.filter(abonent=user, date__range=[start, end], kabel__gt=0)
                if len(pays) == 0:
                    new_users.append(user)
        
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Kabel-TV-Info {current_date}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'Kabel-TV-Info {current_date}'
        headers = ['ID', 'Этрап', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Квартира', 'Точки', 'Баланс', 'Номер', 'Сотовый', 'Дата Подключения', 'Вкл?', 'Предприятие?', 'Примечание']
        ws.append(headers)
        for user in new_users:
            if user.is_on:
                userIs_on = 'Вкл'
            else:
                userIs_on = ''
            
            if user.is_enterprises:
                userIs_enterprises = 'Да'
            else:
                userIs_enterprises = ''
            ws.append([user.ids, user.etrap, user.surname, user.name, user.street, user.home, user.flat, user.kabel_count.kabel_count, "%.2f" % user.b_kabel, user.number, user.sotowyy, user.connect_date, userIs_on, userIs_enterprises, user.kabel_comments])
        wb.save(response)
        return response

    if request.method == 'POST' and 'fourMonthMinus' in request.POST:
        
        start = str(date.today() - relativedelta(months=4)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        payHistory = PayHistory.objects.all()
        new_users = []
        for user in users:
            if user.b_kabel < 0:
                pays = payHistory.filter(abonent=user, date__range=[start, end], kabel__gt=0)
                if len(pays) == 0:
                    new_users.append(user)
        
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Kabel-TV-Info {current_date}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'Kabel-TV-Info {current_date}'
        headers = ['ID', 'Этрап', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Квартира', 'Точки', 'Баланс', 'Номер', 'Сотовый', 'Дата Подключения', 'Вкл?', 'Предприятие?', 'Примечание']
        ws.append(headers)
        for user in new_users:
            if user.is_on:
                userIs_on = 'Вкл'
            else:
                userIs_on = ''
            
            if user.is_enterprises:
                userIs_enterprises = 'Да'
            else:
                userIs_enterprises = ''
            ws.append([user.ids, user.etrap, user.surname, user.name, user.street, user.home, user.flat, user.kabel_count.kabel_count, "%.2f" % user.b_kabel, user.number, user.sotowyy, user.connect_date, userIs_on, userIs_enterprises, user.kabel_comments])
        wb.save(response)
        return response

    if request.method == 'POST' and 'fiveMonthMinus' in request.POST:
        
        start = str(date.today() - relativedelta(months=4)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        payHistory = PayHistory.objects.all()
        new_users = []
        for user in users:
            if user.b_kabel < 0:
                pays = payHistory.filter(abonent=user, date__range=[start, end], kabel__gt=0)
                if len(pays) == 0:
                    new_users.append(user)
        
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Kabel-TV-Info {current_date}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'Kabel-TV-Info {current_date}'
        headers = ['ID', 'Этрап', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Квартира', 'Точки', 'Баланс', 'Номер', 'Сотовый', 'Дата Подключения', 'Вкл?', 'Предприятие?', 'Примечание']
        ws.append(headers)
        for user in new_users:
            if user.is_on:
                userIs_on = 'Вкл'
            else:
                userIs_on = ''
            
            if user.is_enterprises:
                userIs_enterprises = 'Да'
            else:
                userIs_enterprises = ''
            ws.append([user.ids, user.etrap, user.surname, user.name, user.street, user.home, user.flat, user.kabel_count.kabel_count, "%.2f" % user.b_kabel, user.number, user.sotowyy, user.connect_date, userIs_on, userIs_enterprises, user.kabel_comments])
        wb.save(response)
        return response

    
    if request.method == 'POST' and 'sixMonthMinus' in request.POST:
        
        start = str(date.today() - relativedelta(months=4)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        payHistory = PayHistory.objects.all()
        new_users = []
        for user in users:
            if user.b_kabel < 0:
                pays = payHistory.filter(abonent=user, date__range=[start, end], kabel__gt=0)
                if len(pays) == 0:
                    new_users.append(user)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="Kabel-TV-Info {current_date}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'Kabel-TV-Info {current_date}'
        headers = ['ID', 'Этрап', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Квартира', 'Точки', 'Баланс', 'Номер', 'Сотовый', 'Дата Подключения', 'Вкл?', 'Предприятие?', 'Примечание']
        ws.append(headers)
        for user in new_users:
            if user.is_on:
                userIs_on = 'Вкл'
            else:
                userIs_on = ''
            
            if user.is_enterprises:
                userIs_enterprises = 'Да'
            else:
                userIs_enterprises = ''
            ws.append([user.ids, user.etrap, user.surname, user.name, user.street, user.home, user.flat, user.kabel_count.kabel_count, "%.2f" % user.b_kabel, user.number, user.sotowyy, user.connect_date, userIs_on, userIs_enterprises, user.kabel_comments])
        wb.save(response)
        return response
    #################################################################################################################################
    # Вывод в xlsx формат всех у кого баланс в минусе и оплат небыло Месяц, 2 Месяца, 3 Месяца, 4 Месяца, 5 Месяцев, 6 Месяцев END ##
    #################################################################################################################################

        

    if len(users) > 500:
        context['moreThan500'] = True



    if len(users) == 1:
        tarifs = KabelCount.objects.all()
        context['tarifs'] = tarifs
        context['oneUser'] = users[0]

        if users[0].kabel_count:
            current_tarif_pk = users[0].kabel_count.pk
        else:
            current_tarif_pk = 'off'
        context['current_tarif_pk'] = current_tarif_pk

        # Если нажал на сохранить
        if request.method == 'POST' and 'pk' in request.POST:
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


                new_tarif_pk = request.POST.get('tarif_pk')

                # Если нет изменений то нечего сохранять
                if str(new_tarif_pk) == str(current_tarif_pk) and new_is_on == current_is_on:
                    messages.error(request, f'Изменений нет')
                elif new_tarif_pk == 'off' and current_tarif_pk == 'off' and new_is_on == True:
                    messages.error(request, f'Перед включением выберите тариф')
                else:
                    # Код для изменения тарифа 1 - го числа (без начислений, будет начисляться только в MATB)
                    # Если не равны значит либо изменен либо, отключен, либо включен новый тариф (с нуля)
                    if str(new_tarif_pk) != str(current_tarif_pk): 
                        if new_tarif_pk != 'off' and current_tarif_pk != 'off':
                            # Смена тарифа
                            abonent.kabel_count = KabelCount.objects.get(pk=new_tarif_pk)

                            message += f"Смена точки с {KabelCount.objects.get(pk=str(current_tarif_pk)).kabel_count} на {KabelCount.objects.get(pk=str(new_tarif_pk)).kabel_count}, абонент {abonent.number}, {abonent.name}, {abonent.surname}, ids:{abonent.ids}"
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
                            abonent.kabel_count = None
                            message += f"Отключения тарифа {KabelCount.objects.get(pk=str(current_tarif_pk)).kabel_count} точек, абонент {abonent.number}, {abonent.name}, {abonent.surname}, ids:{abonent.ids}"

                            if current_is_on == True:
                                abonent.is_on = False
                                abonent.is_on_date = None

                            staffActionComment = message

                        if new_tarif_pk != 'off' and current_tarif_pk == 'off':
                            # подключения тарифа
                            abonent.kabel_count = KabelCount.objects.get(pk=new_tarif_pk)
                            abonent.connect_date = datetime.now()
                            message += f"Подключения {KabelCount.objects.get(pk=new_tarif_pk).kabel_count} точек, абонент {abonent.number}, {abonent.name}, {abonent.surname}, ids:{abonent.ids}"
                            
                            if new_is_on == True:
                                # Если подключил новый тариф (с нуля) и включил кабель
                                abonent.is_on = True
                                abonent.is_on_date = datetime.now()
                                message += f', Статус Включен'
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
                            message =  f'Статус включен. Тариф не изменен: {abonent.kabel_count.kabel_count} точек, абонент {abonent.number}, {abonent.name}, {abonent.surname}, ids:{abonent.ids}'
                            staffActionComment = message

                        # если тупо отключили без изменения тарифа (тариф не off)
                        if new_is_on == False and current_is_on == True:
                            # отключение
                            abonent.is_on = False
                            abonent.is_on_date = None
                            message = f'Статус отключен. Тариф не изменен: {abonent.kabel_count.kabel_count} точек, абонент {abonent.number}, {abonent.name}, {abonent.surname}, ids:{abonent.ids}'
                            staffActionComment = message

                    StaffAction.objects.create(user=request.user, comment=staffActionComment, action='Кабель TV действия')

                    context['oneUser'] = abonent

                    if abonent.kabel_count:
                        current_tarif_pk = abonent.kabel_count.pk
                    else:
                        current_tarif_pk = 'off'
                    abonent.kabel_comments = f"{request.POST.get('comment')} \n\n {staffActionComment}, изменил {request.user.username}, дата {datetime.now()}"
                    abonent.save()

                    users = UserTable.objects.filter(pk=abonent.pk)
                    
                    context['current_tarif_pk'] = current_tarif_pk
                    messages.success(request, f'{message}')

                    # # Легкий вариант (Тут код с начислениями)
                    # newNach = 0
                    # # Если не равны значит либо изменен либо, отключен, либо включен новый тариф (с нуля)
                    # if str(new_tarif_pk) != str(current_tarif_pk): 
                    #     if new_tarif_pk != 'off' and current_tarif_pk != 'off':
                    #         # Смена тарифа
                    #         abonent.kabel_count = KabelCount.objects.get(pk=new_tarif_pk)
                    #         message += f"Тариф изменен"
                    #         if new_is_on == True:
                    #             # если тариф заменен и кабель включен
                    #             # начисление до конца месяца (новый тариф)
                    #             newNach += (int(days_in_month) - int(current_day)) * (abonent.kabel_count.price / int(days_in_month))
                    #             abonent.is_on_date = datetime.now()
                    #             abonent.b_kabel -= newNach
                    #             abonent.is_on = True
                    #             staffActionComment = f'Смена с {KabelCount.objects.get(pk=str(current_tarif_pk)).kabel_count} точек на {KabelCount.objects.get(pk=str(new_tarif_pk)).kabel_count} точек Статус Включен'
                    #         else:
                    #             abonent.is_on = False
                    #             staffActionComment = f'Смена с {KabelCount.objects.get(pk=str(current_tarif_pk)).kabel_count} точек на {KabelCount.objects.get(pk=str(new_tarif_pk)).kabel_count} точек Статус Выключен'



                    #     if new_tarif_pk == 'off' and current_tarif_pk != 'off':
                    #         # Отключения тарифа
                    #         abonent.is_on = False
                    #         abonent.kabel_count = None
                    #         message += f"Отключен"
                    #         abonent.is_on = False
                    #         abonent.is_on_date = None
                    #         abonent.connect_date = None
                    #         staffActionComment = f'Отключения тарифа {KabelCount.objects.get(pk=str(current_tarif_pk)).kabel_count} точек'

                    #     if new_tarif_pk != 'off' and current_tarif_pk == 'off':
                    #         # подключения тарифа
                    #         abonent.kabel_count = KabelCount.objects.get(pk=new_tarif_pk)
                    #         abonent.connect_date = datetime.now()
                    #         message += f"Тариф подключен"
                    #         if new_is_on == True:
                    #             # Если подключил новый тариф (с нуля) и включил кабель
                    #             newNach += (int(days_in_month) - int(current_day)) * (abonent.kabel_count.price / int(days_in_month))
                    #             abonent.b_kabel -= newNach
                    #             abonent.is_on = True
                    #             staffActionComment = f'Подключение тарифа {KabelCount.objects.get(pk=new_tarif_pk).kabel_count} точек, Статус Включен'
                                
                    #         else:
                    #             abonent.is_on = False
                    #             staffActionComment = f'Подключение тарифа {KabelCount.objects.get(pk=new_tarif_pk).kabel_count} точек, Статус Выключен'

                    # # если нет изменений в тарифе (значит изменения только в отк/вкл) (тариф не off)
                    # if str(new_tarif_pk) == str(current_tarif_pk) and str(current_tarif_pk) != 'off':
                    #     # если есть изменения в отк/вкл
                    #     if new_is_on != current_is_on:
                    #         # если тупо включили без изменения тарифа (тариф не off)
                    #         if new_is_on == True and current_is_on == False:
                    #             # включение
                    #             abonent.is_on = True
                    #             abonent.is_on_date = datetime.now()
                    #             newNach += (int(days_in_month) - int(current_day)) * (abonent.kabel_count.price / int(days_in_month))
                    #             abonent.b_kabel -= newNach
                    #             staffActionComment = f'Включения статуса тарифа {abonent.kabel_count.kabel_count} точек'

                    #             if message == '':
                    #                 message += f"Статус Включен"
                    #             else:
                    #                 message += f", Статус Включен"

                    #         # если тупо отключили без изменения тарифа (тариф не off)
                    #         if new_is_on == False and current_is_on == True:
                    #             # отключение
                    #             # Просто отключения без смены
                    #             abonent.is_on = False
                    #             staffActionComment = f'Выключения статуса тарифа {abonent.kabel_count.kabel_count} точек'

                    #             if message == '':
                    #                 message += f"Статус Отключен"
                    #             else:
                    #                 message += f", Статус Отключен"
                    #             abonent.is_on_date = None
                                
                    # if newNach != 0:
                    #     try:
                    #         nachMinus = NachMinus.objects.get(user=abonent, year=current_year, month=current_month)
                    #         nachMinus.kabel += newNach
                    #         nachMinus.save()
                    #     except:
                    #         NachMinus.objects.create(user=abonent, year=current_year, month=current_month, kabel=newNach)
                    #     try:
                    #         nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=abonent.etrap, year=current_year, month=monthСonvert(current_month))
                    #         nachisleniyaOtchet.kabelServiceNachisleniya += newNach
                    #         nachisleniyaOtchet.save()
                    #     except:
                    #         NachisleniyaOtchet.objects.create(etrap=abonent.etrap, year=current_year, month=monthСonvert(current_month), kabelServiceNachisleniya=newNach)

                    # StaffAction.objects.create(user=request.user, comment=staffActionComment, action='Кабель TV действия')

                    # context['oneUser'] = abonent
                    # if abonent.kabel_count:
                    #     current_tarif_pk = abonent.kabel_count.pk
                    # else:
                    #     current_tarif_pk = 'off'
                    # abonent.kabel_comments = f"{request.POST.get('comment')} \n\n {staffActionComment}"
                    # abonent.save()

                    # users = UserTable.objects.filter(pk=abonent.pk)
                    
                    # context['current_tarif_pk'] = current_tarif_pk
                    # messages.success(request, f'{message}')

            else:
                messages.error(request, f'Комментарий не может быть пустым')
    context['users'] = users[0:500]



    return render(request, 'telekom/MATB/kabelTvInfo.html', context)

