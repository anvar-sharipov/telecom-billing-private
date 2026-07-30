from django.shortcuts import render, redirect
# from telekom.models import ImportInternetNachisleniyaON, LocalCall, ManagerNames, MonthPlatejiFromBilling, MonthPlatejiOFFFromBilling, NachMinus, NonLocalCall, OldLoginDogowor, PayHistory, PlatejiWhichAddKassirsEveryDay, UserTable, NonLocalCall, KabelTvPayHistory
from telekom.models import *
from django.db.models import Sum
from django.contrib import messages

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert
from django.db.models import Q
from datetime import date
from datetime import time
from datetime import datetime, timedelta
from calendar import monthrange
from django.http import HttpResponse
from django.contrib.auth.models import User
import tablib
import math

from django.db.models import F, IntegerField
from django.db.models.functions import Cast
from django.db.models import Count

from itertools import chain


def prochie_otchoty(request):
    context = {}
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
        context['matbIndex'] = True
        
    elif EtrapAndGroup[1] == 'Kassa':
        context['kassaIndex'] = True
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    

    
    
    context['prochie_otchoty'] = True
    context['etrap_user'] = EtrapAndGroup[0]
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    context['etraps'] = etraps
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']


    etrap = request.GET.get('etrap')
    year = request.GET.get('year')
    month_word = request.GET.get('month')
    month_digit = monthСonvert(month_word)

    if etrap:
        if  (not request.user.is_superuser and etrap != EtrapAndGroup[0]) and (request.user.username != 'Gayyp' and etrap != EtrapAndGroup[0]):
            messages.error(request, f"Выберите свой этрап")
            return redirect('prochie-otchoty')
    context['etrap'] = etrap
    context['year'] = year
    context['month'] = month_word

    if etrap and year and month_word:
        month_digit = monthСonvert(month_word)
        days_in_choosed_month = monthrange(int(year), int(month_digit))[1]
        # Конвертировать строки в объект даты
        current_date = datetime.strptime(year + month_digit, '%Y%m')
        # Добавить один месяц
        next_month_date = current_date + timedelta(days=days_in_choosed_month)
        nextYear = next_month_date.year
        nextMonth = next_month_date.month
        print(f"{year}-{month_digit}-01")
        start = f"{year}-{month_digit}-01"
        start2 = f"{year}-{month_digit}-01 00:00:00"
        end=f"{nextYear}-{nextMonth}-01"
        end2=f"{year}-{month_digit}-{days_in_choosed_month} 23:59:59"

        now = datetime.now()
        current_month = now.month
        current_year = now.year

        # month_digit и year — это, например, '2' и '2025'
        month_digit_int = int(month_digit)
        year_int = int(year)

        # Определяем предыдущий месяц и год
        if current_month == 1:
            previous_month = 12
            previous_year = current_year - 1
        else:
            previous_month = current_month - 1
            previous_year = current_year

        # # Проверка: либо текущий месяц и год, либо прошлый месяц и соответствующий год
        # if (month_digit_int == current_month and year_int == current_year) or \
        # (month_digit_int == previous_month and year_int == previous_year):
        #     pass 



    if request.method == 'POST' and 'oplatyCardOrNo' in request.POST:

    # Это оригинал Работает норм (EXCEL)
        # pays = PlatejiWhichAddKassirsEveryDay.objects.filter(date__range=[start, f"2024-03-31"], kassir_etrap=etrap, is_enterprises='ФЛ')
        pays = PayHistory.objects.filter(date__range=[start, end2], edara_ilat='ФЛ', kassir_etrap=etrap)
        pays_from_kabel_TV = KabelTvPayHistory.objects.filter(pay_date__range=[start2, end2])
        print('len_pays', len(pays))

        my_dict = {
            'Telefoniya':{"count_nal": 0, "price_nal": 0,"count_card": 0,"price_card": 0},
            'Internet':{"count_nal": 0, "price_nal": 0,"count_card": 0,"price_card": 0},
            'Alem TV':{"count_nal": 0, "price_nal": 0,"count_card": 0,"price_card": 0},
            'Kabel TV':{"count_nal": 0, "price_nal": 0,"count_card": 0,"price_card": 0}
            }  

        headers = ("TYPE","НАЛИЧ_КОЛ","НАЛИЧ_ЦЕНА","КАРТ_КОЛ","КАРТ_ЦЕНА")
        data = []
        data = tablib.Dataset(*data, headers=headers)   

        for p in pays:
            if p.abonent.number == '93095':
                print('da', p.abonent.number)
            if p.is_card:
                if p.prochee:
                    my_dict['Telefoniya']['count_card'] += 1
                    my_dict['Telefoniya']['price_card'] += p.prochee
                if p.internet:
                    my_dict['Internet']['count_card'] += 1
                    my_dict['Internet']['price_card'] += p.internet
                if p.alem:
                    my_dict['Alem TV']['count_card'] += 1
                    my_dict['Alem TV']['price_card'] += p.alem
                # if p.kabel:
                #     my_dict['Kabel TV']['count_card'] += 1
                #     my_dict['Kabel TV']['price_card'] += p.kabel

                
                if p.telefon:
                    print('telefon', p.abonent.number)
                if p.slr:
                    print('slr', p.abonent.number)
                if p.kod:
                    print('kod', p.abonent.number)
                if p.zakaz:
                    print('zakaz', p.abonent.number)
                if p.dop_uslugi:
                    print('dop_uslugi', p.abonent.number)
            else:
                if p.prochee:
                    my_dict['Telefoniya']['count_nal'] += 1
                    my_dict['Telefoniya']['price_nal'] += p.prochee
                if p.internet:
                    my_dict['Internet']['count_nal'] += 1
                    my_dict['Internet']['price_nal'] += p.internet
                if p.alem:
                    my_dict['Alem TV']['count_nal'] += 1
                    my_dict['Alem TV']['price_nal'] += p.alem
                # if p.kabel:
                #     my_dict['Kabel TV']['count_nal'] += 1
                #     my_dict['Kabel TV']['price_nal'] += p.kabel
                
                if p.telefon:
                    print('telefon', p.abonent.number)
                if p.slr:
                    print('slr', p.abonent.number)
                if p.kod:
                    print('kod', p.abonent.number)
                if p.zakaz:
                    print('zakaz', p.abonent.number)
                if p.dop_uslugi:
                    print('dop_uslugi', p.abonent.number)

        for p in pays_from_kabel_TV:
            if p.card:
                my_dict['Kabel TV']['count_card'] += 1
                my_dict['Kabel TV']['price_card'] += p.pay
            else:
                my_dict['Kabel TV']['count_nal'] += 1
                my_dict['Kabel TV']['price_nal'] += p.pay


        # if etrap == 'Dashoguz':

        #     my_dict['Kabel TV'] = {"count_nal": 0, "price_nal": 0,"count_card": 0,"price_card": 0}
        #     managarNames = ['admin1']
        #     for i in ManagerNames.objects.filter(etrap=etrap):
        #         managarNames.append(i.name)

        #     operators = User.objects.all()
        #     for u in operators:
        #         for g in u.groups.all():
        #             if etrap in g.name:
        #                 if u.username not in managarNames:
        #                     managarNames.append(u.username)

        #     pays = PayHistory.objects.filter(date__range=[start, end2], abonent__is_enterprises=False, kabel__gt=0)

        #     for p in pays:
        #         if p.is_card:
        #             my_dict['Kabel TV']['count_card'] += 1
        #             my_dict['Kabel TV']['price_card'] += p.kabel
        #         else:
        #             my_dict['Kabel TV']['count_nal'] += 1
        #             my_dict['Kabel TV']['price_nal'] += p.kabel

        for type_, values in my_dict.items():
            data.append((type_, values['count_nal'], values['price_nal'], values['count_card'], values['price_card']))
    
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= Plateji_S_Kassy_{etrap}.xlsx"
        return response
    
###############################################################################################################################################
        # Работает но берем с payHistory
        # managarNames = ['admin1']
        # for i in ManagerNames.objects.filter(etrap=etrap):
        #     managarNames.append(i.name)

        # operators = User.objects.all()
        # for u in operators:
        #     for g in u.groups.all():
        #         if etrap in g.name:
        #             if u.username not in managarNames:
        #                 managarNames.append(u.username)

        # pays = PayHistory.objects.filter(date__range=[start, end2], abonent__is_enterprises=False, kassir__in=managarNames)

        # response = HttpResponse(content_type="text/plain")
        # txtName = f'{etrap} {year}-{monthСonvert(month_word)} oplata Ilat kassa'
        # response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
        # lines = [f"TYPE:COUNT_NALICH:PRICE_NALICH:COUNT_CART:PRICE_CART\n"]

        # my_dict = {
        #     'Abonplata':{"count_nal": 0, "price_nal": 0,"count_card": 0,"price_card": 0},
        #     'Internet':{"count_nal": 0, "price_nal": 0,"count_card": 0,"price_card": 0},
        #     'Kabel TV':{"count_nal": 0, "price_nal": 0,"count_card": 0,"price_card": 0},
        #     'Alem TV':{"count_nal": 0, "price_nal": 0,"count_card": 0,"price_card": 0},
        #     }    
        
        # for p in pays:
        #     if p.is_card:
        #         if p.prochee > 0:
        #             my_dict['Abonplata']['count_card'] += 1
        #             my_dict['Abonplata']['price_card'] += p.prochee
        #         if p.internet > 0:
        #             my_dict['Internet']['count_card'] += 1
        #             my_dict['Internet']['price_card'] += p.internet
        #         if p.alem > 0:
        #             my_dict['Alem TV']['count_card'] += 1
        #             my_dict['Alem TV']['price_card'] += p.alem
        #         if p.kabel > 0:
        #             my_dict['Kabel TV']['count_card'] += 1
        #             my_dict['Kabel TV']['price_card'] += p.kabel
        #     else:
        #         if p.prochee > 0:
        #             my_dict['Abonplata']['count_nal'] += 1
        #             my_dict['Abonplata']['price_nal'] += p.prochee
        #         if p.internet > 0:
        #             my_dict['Internet']['count_nal'] += 1
        #             my_dict['Internet']['price_nal'] += p.internet
        #         if p.alem > 0:
        #             my_dict['Alem TV']['count_nal'] += 1
        #             my_dict['Alem TV']['price_nal'] += p.alem
        #         if p.kabel > 0:
        #             my_dict['Kabel TV']['count_nal'] += 1
        #             my_dict['Kabel TV']['price_nal'] += p.kabel

        # for type_, values in my_dict.items():
        #     lines.append(f"{type_}:{values['count_nal']}:{values['price_nal']}:{values['count_card']}:{values['price_card']}\n")

        # response.writelines(lines)
        # return response
            
       
    


      

    if request.method == 'POST' and 'edaraIntNach' in request.POST:
        
        nachMinus = NachMinus.objects.filter(year=year, month=monthСonvert(month_word), internet__gt=0, user__is_enterprises=True, user__etrap=etrap).order_by('user__number')

        users = UserTable.objects.filter(etrap=etrap)
        edara_numbers = {}
        for user in users:
            if user.is_enterprises:
                edara_numbers[user.number] = True

        total_price = 0
        for n in nachMinus:
            if n.internet:
                total_price += n.internet
        
   
        impIntNach = ImportInternetNachisleniyaON.objects.filter(year=year, month=month_word, etrap=etrap)
        logins = []
        for i in impIntNach:
            logins.append(i.login)
        dogowors = []
        for i in impIntNach:
            dogowors.append(i.dogowor)

        oldLogDog = OldLoginDogowor.objects.filter(etrap=etrap)
        oldLogins = []
        for i in oldLogDog:
            oldLogins.append(i.login)
        oldDogowors = []
        for i in oldLogDog:
            oldDogowors.append(i.dogowor)

        # Old
        # response = HttpResponse(content_type="text/plain")
        # txtName = f'{etrap} {year}-{monthСonvert(month_word)} edara internet nachisleniya'
        # response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
        # lines = [f"NUMBER:LOGIN:NAME:MST:HB:SUMMA:ABONPLATA:ITOGO\n"]
            
        # new
        headers = ("NUMBER","LOGIN","NAME","MST","HB","SUMMA")
        data = []
        data = tablib.Dataset(*data, headers=headers)   
   
        test_total = 0
        test_total2 = 0
        for n in nachMinus:
            test_total += n.internet
            login=n.user.login
            dogowor=n.user.dogowor
            # if login in logins or dogowor in dogowors or login in oldLogins or login in oldDogowors:
                # test_total2 += n.internet
            number=n.user.number
            name=n.user.name + ' ' +n.user.surname
            try:
                account=int(n.user.account)
            except:
                account='None'
            price = str(n.internet).replace('.',',')
            try:
                if n.user.hb.name == 'H':
                    hb='H'
                elif n.user.hb.name == 'B':
                    hb='B'
            except:
                hb='None'
            abonplata = '0,0'
            itogo = str(n.internet).replace('.',',')

            # old
            # lines.append(f"{number}:{login}:{name}:{account}:{hb}:{price}:{abonplata}:{itogo}\n")
            # new
            data.append([number,login,name,account,hb,price])
            # else:
            #     continue
        
        print('test_total', test_total)
        print('test_total2', test_total2)

        # old
        # response.writelines(lines)
        # return response 

        # new
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap} {year}-{monthСonvert(month_word)} edara internet nachisleniya.xlsx"
        return response






        # Отлично работает этот тоже но не повазывает нули :(
        # nachMinus = NachMinus.objects.filter(year=year, month=monthСonvert(month_word), internet__gte=0, user__is_enterprises=True, user__etrap=etrap).order_by('user__number')
        # response = HttpResponse(content_type="text/plain")
        # txtName = f'{etrap} {year}-{monthСonvert(month_word)} edara internet nachisleniya'
        # response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
        # lines = [f"NUMBER:LOGIN:NAME:MST:HB:SUMMA:ABONPLATA:ITOGO\n"]

        # my_list = [] # [[number, login, name, account, hb, summaNach, abonplata, itogo ], [number, login, name, account, hb, summaNach, abonplata, itogo ]]
        # for n in nachMinus:
        #     number=n.user.number
        #     login=n.user.login
        #     name=n.user.name + ' ' +n.user.surname
        #     account=int(n.user.account)
        #     price = str(n.internet).replace('.',',')
        #     if n.user.hb.name == 'H':
        #         hb='H'
        #     elif n.user.hb.name == 'B':
        #         hb='B'
        #     abonplata = '0,0'
        #     itogo = str(n.internet).replace('.',',')

        #     lines.append(f"{number}:{login}:{name}:{account}:{hb}:{price}:{abonplata}:{itogo}\n")

        # response.writelines(lines)
        # return response 
    
    if request.method == 'POST' and 'ilatIntNach' in request.POST:
        
        nachMinus = NachMinus.objects.filter(year=year, month=monthСonvert(month_word), internet__gt=0, user__is_enterprises=False, user__etrap=etrap).order_by('user__number')

        # old
        # response = HttpResponse(content_type="text/plain")
        # txtName = f'{etrap} {year}-{monthСonvert(month_word)} Ilat internet nachisleniya'
        # response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
        # lines = [f"NUMBER:LOGIN:NAME:SUMMA:ABONPLATA:ITOGO\n"]

        headers = ("NUMBER","LOGIN","NAME","SUMMA")
        data = []
        data = tablib.Dataset(*data, headers=headers)

        my_list = [] # [[number, login, name, account, hb, summaNach, abonplata, itogo ], [number, login, name, account, hb, summaNach, abonplata, itogo ]]
        for n in nachMinus:
            number=n.user.number
            login=n.user.login
            name=n.user.name + ' ' +n.user.surname
            price = str(n.internet).replace('.',',')
            abonplata = '0,0'
            itogo = str(n.internet).replace('.',',')

            # lines.append(f"{number}:{login}:{name}:{price}:{abonplata}:{itogo}\n")
            data.append([number,login,name,price])

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap} {year}-{monthСonvert(month_word)} Ilat internet nachisleniya.xlsx"
        return response

    if request.method == 'POST' and 'edaraSlrNach' in request.POST:

        # # old
        # # response = HttpResponse(content_type="text/plain")
        # # txtName = f'edara slr {etrap} {year}-{month_digit}'
        # # response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
        # # lines = [f"ACC:NOM:MIN:MAN\n"]

        # # new
        # headers = ("ABON","MT","SUM")
        # data = []
        # data = tablib.Dataset(*data, headers=headers)
        
        # number_minut = {} # {number: minut}
        # number_day_minut = {} # {number: {day: minut}}
        # localCalls = LocalCall.objects.filter(DATE__range=[start, end], etrap=etrap)
        # for l in localCalls:
        #     DAY_ = str(l.DATE)[-2:]
        #     MT = int(l.MT)
        #     NUMBER = l.SUB_A
        #     if NUMBER not in number_day_minut:
        #         number_day_minut[NUMBER] = {DAY_:MT}
        #     else:
        #         if DAY_ not in number_day_minut[NUMBER]:
        #             number_day_minut[NUMBER][DAY_] = MT
        #         else:
        #             number_day_minut[NUMBER][DAY_] += MT

        # for number,values in number_day_minut.items():
        #     total_minuts = 0
        #     for day, minut in values.items():
        #         if minut <= 5:
        #             continue
        #         else:
        #             if number not in number_minut:
        #                 number_minut[number] = minut - 5
        #             else:
        #                 number_minut[number] += minut - 5

        
        # nachMinus = NachMinus.objects.filter(year=year, month=monthСonvert(month_word), slr__gt=0, user__is_enterprises=True, user__etrap=etrap).order_by('user__account')
        # account_val = {} # {account: {number: [minut, price]}}
        # for n in nachMinus:
        #     account = n.user.account
        #     number = n.user.number
        #     slr = float(n.slr)
        #     if account not in account_val:


        #         account_val[account] = {number: [number_minut[number], slr]}
        #     else:
        #         if number not in account_val[account]:
        #             account_val[account][number] = [number_minut[number], slr]

        # umumyPrice = 0
        # umumyNumbers = 0
        # for account, values in account_val.items():
        #     totalMinut = 0
        #     totalPrice = 0
        #     count = 0
        #     data.append(['','',''])
        #     data.append([f'Счет №: {account}', '',''])
        #     for number, val in values.items():
        #         count += 1

        #         # old
        #         # price = str(round(val[1], 4)).replace('.', ',')
        #         # totalMinut += val[0]
        #         # print(val[1])
        #         # totalPrice += val[1]
        #         # lines.append(f"{account}:{int(number)}:{val[0]}:{price}\n")

        #         # new
        #         if val[1] < 0.01:
        #             price = max(val[1], 0.01)
        #         else:
        #             price = math.ceil(val[1] * 100) / 100 
        #         totalMinut += val[0]
        #         totalPrice += price
        #         umumyPrice += price
        #         umumyNumbers += 1

        #         data.append([int(number), val[0], price])
                

        #     # old
        #     # replasedTotalPrice = str(round(totalPrice, 4)).replace('.', ',')
        #     # lines.append(f":Итог:{totalMinut}:{replasedTotalPrice}\n\n")
        #     # new
        #     replasedTotalPrice = round(totalPrice, 2)
        #     data.append([f"Итог по счет № {account}", totalMinut, replasedTotalPrice])
            
            
        # # old
        # # response.writelines(lines)
        # # return response 
    
        # # new
        # data.append(["","",""])
        # data.append(["Всего:", umumyNumbers, 'номеров'])
        # data.append(["На сумму:", round(umumyPrice, 2), 'ман'])
        # response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        # response['Content-Disposition'] = f"attachment; filename= {etrap} Slr edara.xlsx"
        # return response

        headers = (f"Сверхлимитные разговоры по подразделениям За {month_word} {year}","","", "","","", "","","", "","","")
        data = []
        data.append(["ABON","MT","SUM", "ABON","MT","SUM", "ABON","MT","SUM", "ABON","MT","SUM"])
        data = tablib.Dataset(*data, headers=headers)
        
        number_minut = {} # {number: minut}
        number_day_minut = {} # {number: {day: minut}}
        localCalls = LocalCall.objects.filter(DATE__range=[start, end], etrap=etrap)
        for l in localCalls:
            DAY_ = str(l.DATE)[-2:]
            MT = int(l.MT)
            NUMBER = l.SUB_A
            if NUMBER not in number_day_minut:
                number_day_minut[NUMBER] = {DAY_:MT}
            else:
                if DAY_ not in number_day_minut[NUMBER]:
                    number_day_minut[NUMBER][DAY_] = MT
                else:
                    number_day_minut[NUMBER][DAY_] += MT

        for number,values in number_day_minut.items():
            total_minuts = 0
            for day, minut in values.items():
                if minut <= 5:
                    continue
                else:
                    if number not in number_minut:
                        number_minut[number] = minut - 5
                    else:
                        number_minut[number] += minut - 5

        nachMinus = NachMinus.objects.filter(year=year, month=monthСonvert(month_word), slr__gt=0, user__is_enterprises=True, user__etrap=etrap).order_by('user__account')
        account_val = {} # {account: {number: [minut, price]}}
        for n in nachMinus:
            account = n.user.account
            number = n.user.number
            slr = float(n.slr)
            if account not in account_val:


                account_val[account] = {number: [number_minut[number], slr]}
            else:
                if number not in account_val[account]:
                    account_val[account][number] = [number_minut[number], slr]

        umumyPrice = 0
        umumyNumbers = 0
        for account, values in account_val.items():
            totalMinut = 0
            totalPrice = 0
            count = 0
            data.append(['','','', '', '', '', '', '', '', '', '', ''])
            data.append([f'Счет №: {account}', '','', '', '', '', '', '', '', '', '', ''])
            row_of_three = 0
            new_row = []
            for number, val in values.items():
                row_of_three += 1
                count += 1
                if val[1] < 0.01:
                    price = max(val[1], 0.01)
                else:
                    price = math.ceil(val[1] * 100) / 100 
                totalMinut += val[0]
                totalPrice += price
                umumyPrice += price
                umumyNumbers += 1
                new_row.append(int(number))
                new_row.append(val[0])
                new_row.append(price)
                if row_of_three == 4:
                    data.append([new_row[0], new_row[1], new_row[2], new_row[3], new_row[4], new_row[5], new_row[6], new_row[7], new_row[8], new_row[9], new_row[10], new_row[11]])   
                    new_row = []
                    row_of_three = 0
            if row_of_three == 1:
                data.append([new_row[0], new_row[1], new_row[2], '', '', '', '', '', '', '', '', ''])
                new_row = []
                row_of_three = 0
            if row_of_three == 2:
                data.append([new_row[0], new_row[1], new_row[2], new_row[3], new_row[4], new_row[5], '', '', '', '', '', ''])   
                new_row = []
                row_of_three = 0
            if row_of_three == 3:
                data.append([new_row[0], new_row[1], new_row[2], new_row[3], new_row[4], new_row[5], new_row[6], new_row[7], new_row[8], '', '', ''])   
                new_row = []
                row_of_three = 0

            replasedTotalPrice = round(totalPrice, 2)
            data.append([f"Итог по счет № {account}", totalMinut, replasedTotalPrice, '', '', '', '', '', '', '', '', ''])
            
        data.append(["","","", '', '', '', '', '', '', '', '', ''])
        data.append(["Всего:", umumyNumbers, 'номеров', '', '', '', '', '', '', '', '', ''])
        data.append(["На сумму:", round(umumyPrice, 2), 'ман', '', '', '', '', '', '', '', '', ''])
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap} Slr edara.xlsx"
        return response

    if request.method == 'POST' and 'IlatSlrNach' in request.POST:
        if etrap != 'Dashoguz':
            # old
            # response = HttpResponse(content_type="text/plain")
            # txtName = f'ilat slr {etrap} {year}-{month_digit}'
            # response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
            # lines = [f"ABONENET:SCHOTCHIK:SUMMA\n"]

            # new
            # headers = ("ABON","SCHOT","SUM"," ","ABON","SCHOT","SUM"," ","ABON","SCHOT","SUM")
            headers = ("№","ABON","SCHOT","SUM")
            data = []
            data = tablib.Dataset(*data, headers=headers)   

            
            number_minut = {} # {number: minut}
            number_day_minut = {} # {number: {day: minut}}
            localCalls = LocalCall.objects.filter(DATE__range=[start, end], etrap=etrap)
            for l in localCalls:
                DAY_ = str(l.DATE)[-2:]
                MT = int(l.MT)
                NUMBER = l.SUB_A
                if NUMBER not in number_day_minut:
                    number_day_minut[NUMBER] = {DAY_:MT}
                else:
                    if DAY_ not in number_day_minut[NUMBER]:
                        number_day_minut[NUMBER][DAY_] = MT
                    else:
                        number_day_minut[NUMBER][DAY_] += MT

            for number,values in number_day_minut.items():
                total_minuts = 0
                for day, minut in values.items():
                    if minut <= 5:
                        continue
                    else:
                        if number not in number_minut:
                            number_minut[number] = minut - 5
                        else:
                            number_minut[number] += minut - 5

            
            nachMinus = NachMinus.objects.filter(year=year, month=monthСonvert(month_word), slr__gt=0, user__is_enterprises=False, user__etrap=etrap)
            account_val = {} # {account: {number: [minut, price]}}
            for n in nachMinus:
                account = n.user.account
                number = n.user.number
                slr = float(n.slr)
                if account not in account_val:


                    account_val[account] = {number: [number_minut[number], slr]}
                else:
                    if number not in account_val[account] and number in number_minut:
                        account_val[account][number] = [number_minut[number], slr]
            count = 0
            for account, values in account_val.items():
                totalMinut = 0
                totalPrice = 0
                only_3 = 0
                myRow = []
                for number, val in values.items():
                    count += 1
                    
                    # old
                    # price = str(val[1]).replace('.', ',')
                    # new
                    price = val[1]
                    totalMinut += val[0]
                    totalPrice += val[1]
                    # old
                    # lines.append(f"{number}:{val[0]}:{price}\n")

                    # new
                    # if only_3 < 3:
                    #     only_3 += 1
                    #     myRow.append(number)
                    #     myRow.append(val[0])
                    #     myRow.append(price)
                    #     if only_3 <= 2:
                    #         myRow.append(" ")
                    #     continue
                    # else:
                    #     print('myRow', myRow)
                    #     data.append(myRow)
                    #     only_3 = 1
                    #     myRow = []
                    #     myRow.append(number)
                    #     myRow.append(val[0])
                    #     myRow.append(price)
                    #     myRow.append(" ")
                    data.append([count, number, val[0], price])
                # old
                # replasedTotalPrice = str(totalPrice).replace('.', ',')
                # new
                replasedTotalPrice = round(totalPrice, 2)

                # old
                # lines.append(f"Итог по счету № {account}:{totalMinut}:{replasedTotalPrice}\n")

                # new
                # data.append([f"Итог по счету № {account}", totalMinut, replasedTotalPrice,'','','','','','','',''])
                data.append([f"Итог по счету № {account}", totalMinut, replasedTotalPrice,""])

            # old
            # response.writelines(lines)
            # return response 
                
            # new
            response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
            response['Content-Disposition'] = f"attachment; filename= {etrap} Slr ilat.xlsx"
            return response
        
        else:

            ## for Атс 2 (2,6,7,3) START
            headers = (f'Сверхлимитные разговоры по населению по Атс 2 (2,6,7,3) За {month_word} {year}', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '')
            data = []
            data = tablib.Dataset(*data, headers=headers)   

            
            number_minut = {} # {number: minut}
            number_day_minut = {} # {number: {day: minut}}
            # localCalls = LocalCall.objects.filter(DATE__range=[start, end], etrap=etrap)
            
            prefixes = ['2', '6', '7', '3', '4']
            query = Q()
            for p in prefixes:
                query |= Q(SUB_A__startswith=p)

            localCalls = LocalCall.objects.filter(
                DATE__range=[start, end],
                etrap=etrap
            ).filter(query)

            for l in localCalls:
                DAY_ = str(l.DATE)[-2:]
                MT = int(l.MT)
                NUMBER = l.SUB_A
                if NUMBER not in number_day_minut:
                    number_day_minut[NUMBER] = {DAY_:MT}
                else:
                    if DAY_ not in number_day_minut[NUMBER]:
                        number_day_minut[NUMBER][DAY_] = MT
                    else:
                        number_day_minut[NUMBER][DAY_] += MT

            for number,values in number_day_minut.items():
                total_minuts = 0
                for day, minut in values.items():
                    if minut <= 5:
                        continue
                    else:
                        if number not in number_minut:
                            number_minut[number] = minut - 5
                        else:
                            number_minut[number] += minut - 5

            
            # nachMinus = NachMinus.objects.filter(year=year, month=monthСonvert(month_word), slr__gt=0, user__is_enterprises=False, user__etrap=etrap)
            prefixes = ['2', '6', '7', '3', '4']
            number_query = Q()
            for p in prefixes:
                number_query |= Q(user__number__startswith=p)

            nachMinus = NachMinus.objects.filter(
                year=year,
                month=monthСonvert(month_word),
                slr__gt=0,
                user__is_enterprises=False,
                user__etrap=etrap
            ).filter(number_query)

            data.append(["№","ABON","SCHOT","SUM","№","ABON","SCHOT","SUM","№","ABON","SCHOT","SUM","№","ABON","SCHOT","SUM"])

            account_val = {} # {account: {number: [minut, price]}}
            for n in nachMinus:
                account = n.user.account
                number = n.user.number
                slr = float(n.slr)
                if account not in account_val:

                    account_val[account] = {number: [number_minut[number], slr]}
                else:
                    if number not in account_val[account]:
                        account_val[account][number] = [number_minut[number], slr]
            count = 0
            for account, values in account_val.items():
                totalMinut = 0
                totalPrice = 0
                only_4 = 0
                myRow = []
                for number, val in values.items():
                    only_4 += 1
                    count += 1

                    price = val[1]
                    totalMinut += val[0]
                    totalPrice += val[1]

                    myRow.append(count)
                    myRow.append(number)
                    myRow.append(val[0])
                    myRow.append(price)

                    if only_4 == 4:
                        data.append([myRow[0], myRow[1], myRow[2], myRow[3], myRow[4], myRow[5], myRow[6], myRow[7], myRow[8], myRow[9], myRow[10], myRow[11], myRow[12], myRow[13], myRow[14], myRow[15]])
                        myRow=[]
                        only_4 = 0
                if only_4 == 1:
                    data.append([myRow[0], myRow[1], myRow[2], myRow[3], '', '', '', '', '', '', '', '', '', '', '', ''])
                    myRow=[]
                if only_4 == 2:
                    data.append([myRow[0], myRow[1], myRow[2], myRow[3], myRow[4], myRow[5], myRow[6], myRow[7], '', '', '', '', '', '', '', ''])
                    myRow=[]
                    only_4 = 0
                if only_4 == 3:
                    data.append([myRow[0], myRow[1], myRow[2], myRow[3], myRow[4], myRow[5], myRow[6], myRow[7], myRow[8], myRow[9], myRow[10], myRow[11], '', '', '', ''])
                    myRow=[]
                    only_4 = 0

                replasedTotalPrice = round(totalPrice, 2)
                data.append(["Jemi:", 'Ats', '2,6,7,3', '', count,'sany', '', totalMinut, 'min', '',  replasedTotalPrice, "man", '', '', '', ''])

            ## for Атс 2 (2,6,7,3) END

            ## for Атс 5 START
            data.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            data.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            data.append([f'Сверхлимитные разговоры по населению по Атс 5 За {month_word} {year}', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            

            number_minut = {} # {number: minut}
            number_day_minut = {} # {number: {day: minut}}
            # localCalls = LocalCall.objects.filter(DATE__range=[start, end], etrap=etrap)
            
            prefixes = ['5']
            query = Q()
            for p in prefixes:
                query |= Q(SUB_A__startswith=p)

            localCalls = LocalCall.objects.filter(
                DATE__range=[start, end],
                etrap=etrap
            ).filter(query)

            for l in localCalls:
                DAY_ = str(l.DATE)[-2:]
                MT = int(l.MT)
                NUMBER = l.SUB_A
                if NUMBER not in number_day_minut:
                    number_day_minut[NUMBER] = {DAY_:MT}
                else:
                    if DAY_ not in number_day_minut[NUMBER]:
                        number_day_minut[NUMBER][DAY_] = MT
                    else:
                        number_day_minut[NUMBER][DAY_] += MT

            for number,values in number_day_minut.items():
                total_minuts = 0
                for day, minut in values.items():
                    if minut <= 5:
                        continue
                    else:
                        if number not in number_minut:
                            number_minut[number] = minut - 5
                        else:
                            number_minut[number] += minut - 5

            
            # nachMinus = NachMinus.objects.filter(year=year, month=monthСonvert(month_word), slr__gt=0, user__is_enterprises=False, user__etrap=etrap)
            prefixes = ['5']
            number_query = Q()
            for p in prefixes:
                number_query |= Q(user__number__startswith=p)

            nachMinus = NachMinus.objects.filter(
                year=year,
                month=monthСonvert(month_word),
                slr__gt=0,
                user__is_enterprises=False,
                user__etrap=etrap
            ).filter(number_query)

            data.append(["№","ABON","SCHOT","SUM","№","ABON","SCHOT","SUM","№","ABON","SCHOT","SUM","№","ABON","SCHOT","SUM"])

            account_val = {} # {account: {number: [minut, price]}}
            for n in nachMinus:
                account = n.user.account
                number = n.user.number
                slr = float(n.slr)
                if account not in account_val:

                    account_val[account] = {number: [number_minut[number], slr]}
                else:
                    if number not in account_val[account]:
                        account_val[account][number] = [number_minut[number], slr]
            count = 0
            for account, values in account_val.items():
                totalMinut = 0
                totalPrice = 0
                only_4 = 0
                myRow = []
                for number, val in values.items():
                    only_4 += 1
                    count += 1

                    price = val[1]
                    totalMinut += val[0]
                    totalPrice += val[1]

                    myRow.append(count)
                    myRow.append(number)
                    myRow.append(val[0])
                    myRow.append(price)

                    if only_4 == 4:
                        data.append([myRow[0], myRow[1], myRow[2], myRow[3], myRow[4], myRow[5], myRow[6], myRow[7], myRow[8], myRow[9], myRow[10], myRow[11], myRow[12], myRow[13], myRow[14], myRow[15]])
                        myRow=[]
                        only_4 = 0
                if only_4 == 1:
                    data.append([myRow[0], myRow[1], myRow[2], myRow[3], '', '', '', '', '', '', '', '', '', '', '', ''])
                    myRow=[]
                if only_4 == 2:
                    data.append([myRow[0], myRow[1], myRow[2], myRow[3], myRow[4], myRow[5], myRow[6], myRow[7], '', '', '', '', '', '', '', ''])
                    myRow=[]
                    only_4 = 0
                if only_4 == 3:
                    data.append([myRow[0], myRow[1], myRow[2], myRow[3], myRow[4], myRow[5], myRow[6], myRow[7], myRow[8], myRow[9], myRow[10], myRow[11], '', '', '', ''])
                    myRow=[]
                    only_4 = 0

                replasedTotalPrice = round(totalPrice, 2)
                data.append(["Jemi:", 'Ats 5', '', {count}, 'sany', '', totalMinut, 'min', '',  replasedTotalPrice, "man", '', '', '', '', ''])
            ## for Атс 5 END END

            # ## for Атс 9 START
            data.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            data.append(['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            data.append([f'Сверхлимитные разговоры по населению по Атс 9 За {month_word} {year}', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
            

            number_minut = {} # {number: minut}
            number_day_minut = {} # {number: {day: minut}}
            # localCalls = LocalCall.objects.filter(DATE__range=[start, end], etrap=etrap)
            
            prefixes = ['9']
            query = Q()
            for p in prefixes:
                query |= Q(SUB_A__startswith=p)

            localCalls = LocalCall.objects.filter(
                DATE__range=[start, end],
                etrap=etrap
            ).filter(query)

            for l in localCalls:
                DAY_ = str(l.DATE)[-2:]
                MT = int(l.MT)
                NUMBER = l.SUB_A
                if NUMBER not in number_day_minut:
                    number_day_minut[NUMBER] = {DAY_:MT}
                else:
                    if DAY_ not in number_day_minut[NUMBER]:
                        number_day_minut[NUMBER][DAY_] = MT
                    else:
                        number_day_minut[NUMBER][DAY_] += MT

            for number,values in number_day_minut.items():
                total_minuts = 0
                for day, minut in values.items():
                    if minut <= 5:
                        continue
                    else:
                        if number not in number_minut:
                            number_minut[number] = minut - 5
                        else:
                            number_minut[number] += minut - 5

            
            # nachMinus = NachMinus.objects.filter(year=year, month=monthСonvert(month_word), slr__gt=0, user__is_enterprises=False, user__etrap=etrap)
            prefixes = ['9']
            number_query = Q()
            for p in prefixes:
                number_query |= Q(user__number__startswith=p)

            nachMinus = NachMinus.objects.filter(
                year=year,
                month=monthСonvert(month_word),
                slr__gt=0,
                user__is_enterprises=False,
                user__etrap=etrap
            ).filter(number_query)

            data.append(["№","ABON","SCHOT","SUM","№","ABON","SCHOT","SUM","№","ABON","SCHOT","SUM","№","ABON","SCHOT","SUM"])

            account_val = {} # {account: {number: [minut, price]}}
            for n in nachMinus:
                account = n.user.account
                number = n.user.number
                slr = float(n.slr)
                if account not in account_val:

                    account_val[account] = {number: [number_minut[number], slr]}
                else:
                    if number not in account_val[account]:
                        account_val[account][number] = [number_minut[number], slr]
            count = 0
            for account, values in account_val.items():
                totalMinut = 0
                totalPrice = 0
                only_4 = 0
                myRow = []
                for number, val in values.items():
                    only_4 += 1
                    count += 1

                    price = val[1]
                    totalMinut += val[0]
                    totalPrice += val[1]

                    myRow.append(count)
                    myRow.append(number)
                    myRow.append(val[0])
                    myRow.append(price)

                    if only_4 == 4:
                        data.append([myRow[0], myRow[1], myRow[2], myRow[3], myRow[4], myRow[5], myRow[6], myRow[7], myRow[8], myRow[9], myRow[10], myRow[11], myRow[12], myRow[13], myRow[14], myRow[15]])
                        myRow=[]
                        only_4 = 0
                if only_4 == 1:
                    data.append([myRow[0], myRow[1], myRow[2], myRow[3], '', '', '', '', '', '', '', '', '', '', '', ''])
                    myRow=[]
                if only_4 == 2:
                    data.append([myRow[0], myRow[1], myRow[2], myRow[3], myRow[4], myRow[5], myRow[6], myRow[7], '', '', '', '', '', '', '', ''])
                    myRow=[]
                    only_4 = 0
                if only_4 == 3:
                    data.append([myRow[0], myRow[1], myRow[2], myRow[3], myRow[4], myRow[5], myRow[6], myRow[7], myRow[8], myRow[9], myRow[10], myRow[11], '', '', '', ''])
                    myRow=[]
                    only_4 = 0

                replasedTotalPrice = round(totalPrice, 2)
                data.append(["Jemi:", 'Ats 9', '', count,'sany', '', totalMinut, 'min', '',  replasedTotalPrice, "man", '', '', '', '', ''])
            # ## for Атс 9 END END


            response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
            response['Content-Disposition'] = f"attachment; filename= {etrap} Slr ilat.xlsx"
            return response

    if request.method == 'POST' and 'PlatejiSKassySbazy' in request.POST:
        pays = MonthPlatejiFromBilling.objects.filter(pay_date__range=[start, end])
        wn = ['E-government', 'Tolleg APP TMCELL', 'Saray Tolegy', 'Dostluk Bank', 'Turkmen Pochta', 'HalkBank Terminal Payments']
        dzKassa = ['Ziýatowa Nasiba', 'Täjimowa Oguljan', 'Nepesowa Melewşe', 'Klyçewa Gunça', 'Kakaýewa Gurbanbagt', 'Jumaýewa Aýlar',
                    'Jumaniýazowa Şahista', 'Iskanderowa Ruhiýa', 'Ilýasowa Selbi', 'Barlyýewa Serwijan', 'Ballyýewa Aýjemal', 'Amannepesowa Jennet',
                    'Amangeldiýewa Jahan']
        dzInt = ['Soýunowa Aknur', 'Mamedowa Abadan', 'Kakaýewa Jennet', 'Derýagulyýewa Jeren', 'Baýramowa Ogultagan', 'Baýramgeldiýewa Nargiza']

        dzTazeOba = ['Gaýypowa Gözel', 'Berdiýewa Gülşat']

        dz_kassirs = []

        for i in dzKassa:
            dz_kassirs.append(i.lower())
        for i in dzInt:
            dz_kassirs.append(i.lower())
        for i in dzTazeOba:
            dz_kassirs.append(i.lower())

        if etrap == 'Dashoguz':
            dogoworSlize1 = 'dza'
            dogoworSlize2 = 'dnz'
        elif etrap == 'Akdepe':
            dogoworSlize1 = 'dad'
            dogoworSlize2 = 'dge'
        elif etrap == 'Boldumsaz':
            dogoworSlize1 = 'dbs'
            dogoworSlize2 = 'dgd'
        elif etrap == 'Gorgly':
            dogoworSlize1 = 'dgo'
            dogoworSlize2 = 'dgo'
        elif etrap == 'Koneurgench':
            dogoworSlize1 = 'dku'
            dogoworSlize2 = 'dku'
        elif etrap == 'Koneurgench':
            dogoworSlize1 = 'dnz'
            dogoworSlize2 = 'dnz'
        elif etrap == 'Ruhubelent':
            dogoworSlize1 = 'drb'
            dogoworSlize2 = 'drb'
        elif etrap == 'Turkmenbashy':
            dogoworSlize1 = 'dtb'
            dogoworSlize2 = 'dtb'
        else:
            messages.error(request, f"Выберите Этрап")
            return redirect('prochie-otchoty')

        response = HttpResponse(content_type="text/plain")
        txtName = f'ilat kassa internet tolegler {etrap} {year}-{month_digit}'
        response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
        lines = [f"NUM:LOGIN:FAM:SUM\n"]

        dogowor_number = {}
        dogowor_number2 = {}
        users = UserTable.objects.filter(etrap=etrap)
        users2 = OldLoginDogowor.objects.filter(etrap=etrap)
        for user in users:
            dogowor_number[user.dogowor]=user.number
        for user in users2:
            dogowor_number2[user.dogowor]=user.number

        totalPrice = 0
        errorList = []
        for p in pays:
            manager = p.manager.lower().strip()
            dogowor = p.dogowor.lower().strip()
            
            if dogoworSlize1 in dogowor or dogoworSlize2 in dogowor:
                if manager in dz_kassirs:
                    dogowor = p.dogowor.strip()
                    try:
                        number = dogowor_number[dogowor]
                    except:
                        try:
                            number = dogowor_number2[dogowor]
                        except:
                            if len(p.kod_oplaty) == 8:
                                number = p.kod_oplaty[3:]
                                print('ggggggg', number)
                            else:
                                number = ''
                                errorList.append([p.manager, p.pay_date, p.dogowor, p.price, p.platejiType, p.date_price, p.kod_oplaty, p.YurOrFiz, p.FAO])
                    
                    lines.append(f"{number}:{p.dogowor}:{p.FAO}:{p.price}\n")

        if errorList:
            messages.error(request, f"Не найденные договора платежей в нашей БД")
            context['errorList'] = errorList
            return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/dismatchDogowor.html', context)
        else:
            response.writelines(lines)
            return response
                    

    if request.method == 'POST' and 'oplataPlatejiSBilinga' in request.POST:
        pays = MonthPlatejiFromBilling.objects.filter(pay_date__range=['2024-01-01', '2024-01-17'])
        wn = ['E-government', 'Tolleg APP TMCELL', 'Saray Tolegy', 'Dostluk Bank', 'Turkmen Pochta', 'HalkBank Terminal Payments']
        dzKassa = ['Ziýatowa Nasiba', 'Täjimowa Oguljan', 'Nepesowa Melewşe', 'Klyçewa Gunça', 'Kakaýewa Gurbanbagt', 'Jumaýewa Aýlar',
                    'Jumaniýazowa Şahista', 'Iskanderowa Ruhiýa', 'Ilýasowa Selbi', 'Barlyýewa Serwijan', 'Ballyýewa Aýjemal', 'Amannepesowa Jennet',
                    'Amangeldiýewa Jahan']
        dzInt = ['Soýunowa Aknur', 'Mamedowa Abadan', 'Kakaýewa Jennet', 'Derýagulyýewa Jeren', 'Baýramowa Ogultagan', 'Baýramgeldiýewa Nargiza']

        dzTazeOba = ['Gaýypowa Gözel', 'Berdiýewa Gülşat']

        dz_kassirs = []

        for i in dzKassa:
            dz_kassirs.append(i.lower())
        for i in dzInt:
            dz_kassirs.append(i.lower())
        for i in dzTazeOba:
            dz_kassirs.append(i.lower())

        if etrap == 'Dashoguz':
            dogoworSlize1 = 'dza'
            dogoworSlize2 = 'dnz'
        elif etrap == 'Akdepe':
            dogoworSlize1 = 'dad'
            dogoworSlize2 = 'dge'
        elif etrap == 'Boldumsaz':
            dogoworSlize1 = 'dbs'
            dogoworSlize2 = 'dgd'
        elif etrap == 'Gorgly':
            dogoworSlize1 = 'dgo'
            dogoworSlize2 = 'dgo'
        elif etrap == 'Koneurgench':
            dogoworSlize1 = 'dku'
            dogoworSlize2 = 'dku'
        elif etrap == 'Koneurgench':
            dogoworSlize1 = 'dnz'
            dogoworSlize2 = 'dnz'
        elif etrap == 'Ruhubelent':
            dogoworSlize1 = 'drb'
            dogoworSlize2 = 'drb'
        elif etrap == 'Turkmenbashy':
            dogoworSlize1 = 'dtb'
            dogoworSlize2 = 'dtb'
        else:
            messages.error(request, f"Выберите Этрап")
            return redirect('prochie-otchoty')

        response = HttpResponse(content_type="text/plain")
        txtName = f'ilat kassa internet tolegler {etrap} {year}-{month_digit}'
        response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
        lines = [f"NUM:LOGIN:FAM:SUM\n"]

        dogowor_number = {}
        dogowor_number2 = {}
        number_pk = {}
        users = UserTable.objects.filter(etrap=etrap)
        users2 = OldLoginDogowor.objects.filter(etrap=etrap)
        for user in users:
            dogowor_number[user.dogowor.lower()]=user.number
            number_pk[user.number] = user.pk
        for user in users2:
            dogowor_number2[user.dogowor.lower()]=user.number

        totalPrice = 0
        errorList = []
        bulk_update_user = []
        bulk_create_pay = []
        count = 0
        number_pays = {} # {number: [prochee, internet, alem]}
        for p in pays:
            count += 1
            # print('Пробито платежей:', count)
            manager = p.manager.lower().strip()
            dogowor = p.dogowor.lower().strip()
    
            if dogoworSlize1 in dogowor or dogoworSlize2 in dogowor:

                try:
                    number = dogowor_number[dogowor]
                except:
                    try:
                        number = dogowor_number2[dogowor]
                        print('da',number, dogowor)
                    except:
                        if len(p.kod_oplaty) == 8:
                            number = p.kod_oplaty[3:]
                        else:
                            errorList.append([p.manager, p.pay_date, p.dogowor, p.price, p.platejiType, p.date_price, p.kod_oplaty, p.YurOrFiz, p.FAO])
                            continue
                user = users.get(pk=number_pk[number])
                if user.number not in number_pays:
                    number_pays[user.number] = [0,p.price,0]
                else:
                    number_pays[user.number][1] += p.price
                if 'картой' in p.platejiType.lower():
                    is_cart = True
                else:
                    is_cart = False
                obj = PayHistory(abonent=user, internet=p.price, kassa=p.manager, kassir=p.manager, is_card=is_cart, date=p.pay_date, total=p.price)
                bulk_create_pay.append(obj)
                totalPrice += p.price
            elif 'iptv' in dogowor:
                if 'old' in dogowor:
                    number = dogowor[11:16]
                else:
                    number = dogowor[-5:]
                try:
                    user = users.get(pk=number_pk[number])
                except:
                    errorList.append([p.manager, p.pay_date, p.dogowor, p.price, p.platejiType, p.date_price, p.kod_oplaty, p.YurOrFiz, p.FAO])
                    continue

                if user.number not in number_pays:
                    number_pays[user.number] = [0,0,p.price]
                else:
                    number_pays[user.number][2] += p.price
                if 'картой' in p.platejiType.lower():
                    is_cart = True
                else:
                    is_cart = False
                obj = PayHistory(abonent=user, alem=p.price, kassa=p.manager, kassir=p.manager, is_card=is_cart, date=p.pay_date, total=p.price)
                bulk_create_pay.append(obj)
                totalPrice += p.price
            elif 'old' in dogowor:
                number = dogowor[6:11]
                try:
                    user = users.get(pk=number_pk[number])
                except:
                    errorList.append([p.manager, p.pay_date, p.dogowor, p.price, p.platejiType, p.date_price, p.kod_oplaty, p.YurOrFiz, p.FAO])
                    continue

                if user.number not in number_pays:
                    number_pays[user.number] = [p.price,0,0]
                else:
                    number_pays[user.number][0] += p.price
                if 'картой' in p.platejiType.lower():
                    is_cart = True
                else:
                    is_cart = False
                obj = PayHistory(abonent=user, prochee=p.price, kassa=p.manager, kassir=p.manager, is_card=is_cart, date=p.pay_date, total=p.price)
                bulk_create_pay.append(obj)
                totalPrice += p.price
            else:
                if "ikdz" in dogowor:
                    continue
                try:
                    int(dogowor)
                    number = dogowor[-5:]
                    user = users.get(pk=number_pk[number])
                except:
                    errorList.append([p.manager, p.pay_date, p.dogowor, p.price, p.platejiType, p.date_price, p.kod_oplaty, p.YurOrFiz, p.FAO])
                    continue

                if 'картой' in p.platejiType.lower():
                    is_cart = True
                else:
                    is_cart = False
                    
                if user.number not in number_pays:
                    number_pays[user.number] = [p.price,0,0]
                else:
                    number_pays[user.number][0] += p.price
                if 'картой' in p.platejiType.lower():
                    is_cart = True
                else:
                    is_cart = False
                obj = PayHistory(abonent=user, prochee=p.price, kassa=p.manager, kassir=p.manager, is_card=is_cart, date=p.pay_date, total=p.price)
                bulk_create_pay.append(obj)
                totalPrice += p.price



        # for number, values in  number_pays.items():
        #     user = users.get(pk=number_pk[number])
        #     user.b_prochee += values[0]
        #     user.b_internet += values[1]
        #     user.b_alem += values[2]
        #     bulk_update_user.append(user)

        if errorList:
            messages.error(request, f"Не найденные договора платежей в нашей БД")
            context['errorList'] = errorList
            return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/dismatchDogowor.html', context)
        else:
            print('totalPrice', totalPrice)
            
            # if bulk_update_user:
            #     print('tut1')
            #     UserTable.objects.bulk_update(bulk_update_user, ['b_internet', 'b_alem', 'b_prochee'])
            if bulk_create_pay:
                print('tut2')
                PayHistory.objects.bulk_create(bulk_create_pay)

    if request.method == 'POST' and 'oplataOFFPlatejiSBilinga' in request.POST:
        pays = MonthPlatejiOFFFromBilling.objects.filter(pay_date__range=['2024-01-18', '2024-02-01'])
        wn = ['E-government', 'Tolleg APP TMCELL', 'Saray Tolegy', 'Dostluk Bank', 'Turkmen Pochta', 'HalkBank Terminal Payments']
        dzKassa = ['Ziýatowa Nasiba', 'Täjimowa Oguljan', 'Nepesowa Melewşe', 'Klyçewa Gunça', 'Kakaýewa Gurbanbagt', 'Jumaýewa Aýlar',
                    'Jumaniýazowa Şahista', 'Iskanderowa Ruhiýa', 'Ilýasowa Selbi', 'Barlyýewa Serwijan', 'Ballyýewa Aýjemal', 'Amannepesowa Jennet',
                    'Amangeldiýewa Jahan']
        dzInt = ['Soýunowa Aknur', 'Mamedowa Abadan', 'Kakaýewa Jennet', 'Derýagulyýewa Jeren', 'Baýramowa Ogultagan', 'Baýramgeldiýewa Nargiza']

        dzTazeOba = ['Gaýypowa Gözel', 'Berdiýewa Gülşat']

        dz_kassirs = []

        for i in dzKassa:
            dz_kassirs.append(i.lower())
        for i in dzInt:
            dz_kassirs.append(i.lower())
        for i in dzTazeOba:
            dz_kassirs.append(i.lower())

        if etrap == 'Dashoguz':
            dogoworSlize1 = 'dza'
            dogoworSlize2 = 'dnz'
        elif etrap == 'Akdepe':
            dogoworSlize1 = 'dad'
            dogoworSlize2 = 'dge'
        elif etrap == 'Boldumsaz':
            dogoworSlize1 = 'dbs'
            dogoworSlize2 = 'dgd'
        elif etrap == 'Gorgly':
            dogoworSlize1 = 'dgo'
            dogoworSlize2 = 'dgo'
        elif etrap == 'Koneurgench':
            dogoworSlize1 = 'dku'
            dogoworSlize2 = 'dku'
        elif etrap == 'Koneurgench':
            dogoworSlize1 = 'dnz'
            dogoworSlize2 = 'dnz'
        elif etrap == 'Ruhubelent':
            dogoworSlize1 = 'drb'
            dogoworSlize2 = 'drb'
        elif etrap == 'Turkmenbashy':
            dogoworSlize1 = 'dtb'
            dogoworSlize2 = 'dtb'
        else:
            messages.error(request, f"Выберите Этрап")
            return redirect('prochie-otchoty')

        response = HttpResponse(content_type="text/plain")
        txtName = f'ilat kassa internet tolegler {etrap} {year}-{month_digit}'
        response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
        lines = [f"NUM:LOGIN:FAM:SUM\n"]

        dogowor_number = {}
        dogowor_number2 = {}
        number_pk = {}
        users = UserTable.objects.filter(etrap=etrap)
        users2 = OldLoginDogowor.objects.filter(etrap=etrap)
        for user in users:
            dogowor_number[user.dogowor.lower()]=user.number
            number_pk[user.number] = user.pk
        for user in users2:
            dogowor_number2[user.dogowor.lower()]=user.number

        totalPrice = 0
        errorList = []
        bulk_update_user = []
        bulk_create_pay = []
        count = 0
        number_pays = {} # {number: [prochee, internet, alem]}
        for p in pays:
            count += 1
            # print('Пробито платежей:', count)
            manager = p.manager.lower().strip()
            dogowor = p.dogowor.lower().strip()
    
            if dogoworSlize1 in dogowor or dogoworSlize2 in dogowor:

                try:
                    number = dogowor_number[dogowor]
                except:
                    try:
                        number = dogowor_number2[dogowor]
                        print('da',number, dogowor)
                    except:
                        if len(p.kod_oplaty) == 8:
                            number = p.kod_oplaty[3:]
                        else:
                            errorList.append([p.manager, p.pay_date, p.dogowor, p.price, p.platejiType, p.date_price, p.kod_oplaty, p.YurOrFiz, p.FAO])
                            continue
                user = users.get(pk=number_pk[number])
                if user.number not in number_pays:
                    number_pays[user.number] = [0,p.price,0]
                else:
                    number_pays[user.number][1] += p.price
                if 'картой' in p.platejiType.lower():
                    is_cart = True
                else:
                    is_cart = False
                obj = PayHistory(abonent=user, internet=p.price, kassa=p.manager, kassir=p.manager, is_card=is_cart, date=p.pay_date, total=p.price)
                bulk_create_pay.append(obj)
                totalPrice += p.price
            elif 'iptv' in dogowor:
                if 'old' in dogowor:
                    number = dogowor[11:16]
                else:
                    number = dogowor[-5:]
                try:
                    user = users.get(pk=number_pk[number])
                except:
                    errorList.append([p.manager, p.pay_date, p.dogowor, p.price, p.platejiType, p.date_price, p.kod_oplaty, p.YurOrFiz, p.FAO])
                    continue

                if user.number not in number_pays:
                    number_pays[user.number] = [0,0,p.price]
                else:
                    number_pays[user.number][2] += p.price
                if 'картой' in p.platejiType.lower():
                    is_cart = True
                else:
                    is_cart = False
                obj = PayHistory(abonent=user, alem=p.price, kassa=p.manager, kassir=p.manager, is_card=is_cart, date=p.pay_date, total=p.price)
                bulk_create_pay.append(obj)
                totalPrice += p.price
            elif 'old' in dogowor:
                number = dogowor[6:11]
                try:
                    user = users.get(pk=number_pk[number])
                except:
                    errorList.append([p.manager, p.pay_date, p.dogowor, p.price, p.platejiType, p.date_price, p.kod_oplaty, p.YurOrFiz, p.FAO])
                    continue

                if user.number not in number_pays:
                    number_pays[user.number] = [p.price,0,0]
                else:
                    number_pays[user.number][0] += p.price
                if 'картой' in p.platejiType.lower():
                    is_cart = True
                else:
                    is_cart = False
                obj = PayHistory(abonent=user, prochee=p.price, kassa=p.manager, kassir=p.manager, is_card=is_cart, date=p.pay_date, total=p.price)
                bulk_create_pay.append(obj)
                totalPrice += p.price
            else:
                if "ikdz" in dogowor:
                    continue
                try:
                    int(dogowor)
                    number = dogowor[-5:]
                    user = users.get(pk=number_pk[number])
                except:
                    errorList.append([p.manager, p.pay_date, p.dogowor, p.price, p.platejiType, p.date_price, p.kod_oplaty, p.YurOrFiz, p.FAO])
                    continue

                if 'картой' in p.platejiType.lower():
                    is_cart = True
                else:
                    is_cart = False
                    
                if user.number not in number_pays:
                    number_pays[user.number] = [p.price,0,0]
                else:
                    number_pays[user.number][0] += p.price
                if 'картой' in p.platejiType.lower():
                    is_cart = True
                else:
                    is_cart = False
                obj = PayHistory(abonent=user, prochee=p.price, kassa=p.manager, kassir=p.manager, is_card=is_cart, date=p.pay_date, total=p.price)
                bulk_create_pay.append(obj)
                totalPrice += p.price



        for number, values in  number_pays.items():
            user = users.get(pk=number_pk[number])
            user.b_prochee += values[0]
            user.b_internet += values[1]
            user.b_alem += values[2]
            bulk_update_user.append(user)

        if errorList:
            messages.error(request, f"Не найденные договора платежей в нашей БД")
            context['errorList'] = errorList
            return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/dismatchDogowor.html', context)
        else:
            print('totalPrice', totalPrice)
            
            if bulk_update_user:
                print('tut1')
                UserTable.objects.bulk_update(bulk_update_user, ['b_internet', 'b_alem', 'b_prochee'])
            if bulk_create_pay:
                print('tut2')
                PayHistory.objects.bulk_create(bulk_create_pay)
 
    if request.method == 'POST' and 'SotowyOtchyot' in request.POST:
        # calls = NonLocalCall.objects.filter(DATE__range=[f"{year}-{month_digit}-01", f"{nextYear}-{nextMonth}-01"])
        calls = NonLocalCall.objects.filter(DATE__range=[f"{year}-{month_digit}-01", f"{year}-{month_digit}-{days_in_choosed_month}"])
        nachMinus = NachMinus.objects.filter(year=year, month=month_digit, user__is_enterprises = False) 
        etrap_number_prochee = {} # {etrap: {number: prochee}}
        for n in nachMinus:
            if n.prochee:
                if n.user.etrap not in etrap_number_prochee:
                    etrap_number_prochee[n.user.etrap] = {n.user.number: n.prochee}
                elif n.user.number not in etrap_number_prochee[n.user.etrap]:
                    etrap_number_prochee[n.user.etrap][n.user.number] = n.prochee
                

        headers = ("№","ABON","SCHOT","SUM")
        data = []
        data = tablib.Dataset(*data, headers=headers)   

        # old
        # response = HttpResponse(content_type="text/plain")
        # txtName = f'Altyn Asyr otchyot {etrap} {year}-{month_digit}'
        # response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
        # lines = [f"ETRAP:COUNT:MINUT:MANAT\n"]
        etrap_val_dict = {} # {etrap: [count, min, manat]}
        for c in calls:
            if c.SUB_B_locations == 'Sotowyy':
                try:
                    prochee = etrap_number_prochee[c.SUB_A_etrap][c.SUB_A]
                    del etrap_number_prochee[c.SUB_A_etrap][c.SUB_A]
                except:
                    prochee = 0

                if c.SUB_A_etrap not in etrap_val_dict:
                    etrap_val_dict[c.SUB_A_etrap] = [1, int(c.MT), float(c.total_price) + prochee]
                else:
                    etrap_val_dict[c.SUB_A_etrap][0] += 1
                    etrap_val_dict[c.SUB_A_etrap][1] += int(c.MT)
                    etrap_val_dict[c.SUB_A_etrap][2] += float(c.total_price) + prochee

        for etr, v in etrap_val_dict.items():
            data.append([etr, v[0], v[1], v[2]])
            # old
            # lines.append(f"{etr}:{v[0]}:{v[1]}:{v[2]}\n")

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= Altyn Asyr otchyot.xlsx"
        return response

        # response.writelines(lines)
        # return response


    if request.method == 'POST' and 'SpisokOtkKabel' in request.POST:
        users = UserTable.objects.filter(is_on=True, kabel_count__isnull=False, etrap=etrap, b_kabel__lte=-10)

        # old
        # response = HttpResponse(content_type="text/plain")
        # txtName = f'Kabel TV okl {etrap} {year}-{month_digit}'
        # response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
        # lines = [f"Фамилия=Имя=Улица=Дом=Кв=Кол=Баланс=Тел.=Сотовый=id=Примечание=Дата=Вкл=Предпр\n"]

        headers = ("Фамилия","Имя","Улица","Дом","Кв","Кол","Баланс","Тел","Сотовый","id","Вкл","Предпр")
        data = []
        data = tablib.Dataset(*data, headers=headers)   

        
        for u in users:
            # old
            # surname=str(u.surname) if u.surname != None else ''
            # name=str(u.name) if u.name != None else ''
            # street=str(u.street) if u.street != None else ''
            # home=str(u.home) if u.home != None else ''
            # flat=str(u.flat) if u.flat != None else ''
            # kabel_count=str(u.kabel_count.kabel_count) if u.kabel_count.kabel_count != None else ''
            # balance=str(int(u.b_kabel))
            # number=str(u.number) if u.number != None else ''
            # sotowyy=str(u.sotowyy) if u.sotowyy != None else ''
            # ids=str(u.ids) if u.ids != None else ''
            # comments=str(u.kabel_comments) if u.kabel_comments != None else ''
            # connect_date = str(u.connect_date)[:10] if u.connect_date != None else ''
            # is_on=str(u.is_on)
            # is_enterprises=str(u.is_enterprises)
            
            # old 
            # lines.append(f"{surname}={name}={street}={home}={flat}={kabel_count}={balance}={number}={sotowyy}={ids}={comments}={connect_date}={is_on}={is_enterprises}\n")

            data.append([u.surname,u.name,u.street,u.home,u.flat,u.kabel_count.kabel_count,u.b_kabel,u.number,u.sotowyy,u.ids,u.is_on,u.is_enterprises])

        # old
        # response.writelines(lines)
        # return response 
            
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= Spisok_Otkl_kabel_TV.xlsx"
        return response





    if request.method == 'POST' and 'internetKassaTolegleri' in request.POST:
        # for i in ManagerNames.objects.filter(etrap=etrap):
        #     managarNames.append(i.name)

        # operators = User.objects.all()
        # for u in operators:
        #     for g in u.groups.all():
        #         if etrap in g.name:
        #             if u.username not in managarNames:
        #                 managarNames.append(u.username)

        # Этот код тоже работает но чуть чуть другая сумма но имена и фамили абонентов четкие взятые с биллинга
        # pays = PlatejiWhichAddKassirsEveryDay.objects.filter(date__range=[start, end2], type_pay='Internet', kassir_etrap=etrap, is_enterprises='ФЛ')
        pays = PayHistory.objects.filter(date__range=[start, end2], edara_ilat='ФЛ', kassir_etrap=etrap)

        # response = HttpResponse(content_type="text/plain")
        # txtName = f'{etrap} {year}-{monthСonvert(month_word)} oplata Internet kassa'
        # response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
        # lines = [f"NUMBER:NAME:DOGOWOR:PRICE\n"]

        headers = ("NUMBER","NAME","DOGOWOR","PRICE")
        data = []
        data = tablib.Dataset(*data, headers=headers)   


        for p in pays:
            if p.internet:
                data.append([p.abonent.number, p.abonent.name, p.abonent.dogowor, p.internet])

        # response.writelines(lines)
        # return response
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap}_{year}_{monthСonvert(month_word)}_oplata_Internet_kassa.xlsx"
        return response
    
    
    if request.method == 'POST' and 'kabelBaza' in request.POST:
        users = UserTable.objects.filter(etrap='Dashoguz', kabel_count__isnull=False)
        headers = ("Number","Surname","Name","Street","Home","Flat","Sotowy","Kabel_count",'Is_on', 'Is_enterprises', 'Balance', 'connect_date', 'comment')
        
        data = []
        data = tablib.Dataset(*data, headers=headers)
        

        for u in users:
            data.append((u.number, u.surname, u.name, u.street, u.home, u.flat, u.sotowyy, u.kabel_count.kabel_count, u.is_on, u.is_enterprises, u.b_kabel, u.connect_date, u.kabel_comments))
            
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= Kabel_TV_Baza.xlsx"

        return response
    
    if request.method == 'POST' and 'edaraBaza' in request.POST:

        users = UserTable.objects.filter(etrap=etrap, is_enterprises=True)
        headers = ("Number","Surname","Name","Street","Home","Flat","Account",'Abonplata',"HB", "Beneficiary")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)
        

        for u in users:
            surname = u.surname if u.surname != None else ''
            name = u.name if u.name != None else ''
            street = u.street if u.street != None else ''
            home = u.home if u.home != None else ''
            flat = u.flat if u.flat != None else ''
            account = u.account if u.account != None else 0
            abonplata = u.abonplata if u.abonplata != None else 0
            hb = u.hb.name if u.hb != None else 0
            data.append((u.number, surname, name, street, home, flat, account, abonplata, hb, u.beneficiary))
            
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= Edara_Baza{etrap}.xlsx"

        return response
    
    if request.method == 'POST' and 'dop_09' in request.POST:
        # NEW_N	FAM	NAME	STREET	HOME	APT	P
        # users = UserTable.objects.filter(etrap=etrap)

        # users2 = UserTable.objects.annotate()
        users = UserTable.objects.annotate(
                number_as_int=Cast('number', IntegerField())
            ).filter(etrap=etrap).exclude(number_as_int__gte=100000).order_by('number')
        
        headers = ("NEW_N","FAM","NAME","STREET","HOME","APT","P")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)
        

        for u in users:
            surname = u.surname if u.surname != None else ''
            name = u.name if u.name != None else ''
            street = u.street if u.street != None else ''
            home = u.home if u.home != None else ''
            flat = u.flat if u.flat != None else ''
            account = u.account if u.account != None else 0
            hb = 'П' if u.hb else None
            data.append((u.number, surname, name, street, home, flat, hb))
            
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap}_DOP9_{year}-{month_digit}_.xlsx"

        return response
    

    if request.method == 'POST' and 'dop_uslugi_list' in request.POST:

        users = UserTable.objects.annotate(service_count=Count('service')).filter(service_count__gt=0, etrap=etrap)
        
        headers = ("Nomer", "Ady", "Baha", "Edara", "Usluga")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)
        

        for u in users:

            list_of_service = []
            price = 0
            for service in u.service.all():
                list_of_service.append(service.service)
                price += service.price

            serv_str = ", ".join(map(str, list_of_service))

            if u.is_enterprises:
                edara = '+'
            else:
                edara = ''

            data.append((u.number, f"{u.surname} {u.name}", price, edara, serv_str))

            
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap}_spisok_uslug_{year}-{month_digit}_.xlsx"

        return response 


    if request.method == 'POST' and 'lena_plateji' in request.POST:

        pays = PayHistory.objects.filter(date__range=[start, end2], kassir_etrap='Dashoguz')
        pays_from_kabel_TV = KabelTvPayHistory.objects.filter(pay_date__range=[start2, end2])
        
        headers = ("NUMBER","NAME","ETRAP","EDARA_ILAT", "TYPE", "MANAGER", "DATE", "CART", "PRICE")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)
        

        for p in pays:
            number = p.abonent.number
            name = f"{p.abonent.surname} {p.abonent.name}"
            if p.internet:
                type_ = 'internet'
                price = p.internet
            elif p.alem:
                type_ = 'alem'
                price = p.alem
            elif p.prochee:
                type_ = 'abonplata'
                price = p.prochee
            elif p.kabel:
                continue
                # type_ = 'kabel'
                # price = p.kabel
            elif p.kod:
                type_ = 'kod'
                price = p.kod
            elif p.zakaz:
                type_ = 'zakaz'
                price = p.zakaz
            # elif p.abonplata:
            #     type_ = 'error_abonplata'
            #     price = p.abonplata
            elif p.dop_uslugi:
                type_ = 'dop_uslugi'
                price = p.dop_uslugi
            elif p.slr:
                type_ = 'slr'
                price = p.slr
        
            cart = 'Наличка'
            if p.is_card:
                cart = 'Карточка'

            date_ = p.date

            manager = p.kassir

            edara_ilat = 'ФЛ'
            if p.edara_ilat == 'ЮЛ':
                edara_ilat = 'ЮЛ'

        


   
            data.append((number, name, p.abonent.etrap, edara_ilat, type_, manager, date_, cart, price))

        for p in pays_from_kabel_TV:
            cart = 'Наличка'
            if p.card:
                cart = 'Карточка'

            edara_ilat = 'ФЛ'
            if p.user.is_enterprises:
                edara_ilat = 'ЮЛ'

            data.append((p.user.number, p.user.name, 'Dashoguz', edara_ilat, 'kabel', p.pay_kassir, p.pay_date, cart, p.pay))

            
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= Dashoguz_Lena_plateji_za_{year}-{month_digit}.xlsx"

        return response


    if request.method == 'POST' and 'lena_plateji_2' in request.POST:

        # В отличие от 'lena_plateji': берём платежи, где Dashoguz — этрап КАССИРА,
        # ИЛИ где Dashoguz — этрап АБОНЕНТА (объединение, без дублей, т.к. связь FK одиночная)
        pays = PayHistory.objects.filter(
            date__range=[start, end2]
        ).filter(
            Q(kassir_etrap='Dashoguz') | Q(abonent__etrap='Dashoguz')
        )
        pays_from_kabel_TV = KabelTvPayHistory.objects.filter(pay_date__range=[start2, end2])

        headers = ("NUMBER","NAME","ETRAP","ETRAP_KASSIROV","EDARA_ILAT", "TYPE", "MANAGER", "DATE", "CART", "PRICE")

        data = []
        data = tablib.Dataset(*data, headers=headers)


        for p in pays:
            number = p.abonent.number
            name = f"{p.abonent.surname} {p.abonent.name}"
            if p.internet:
                type_ = 'internet'
                price = p.internet
            elif p.alem:
                type_ = 'alem'
                price = p.alem
            elif p.prochee:
                type_ = 'abonplata'
                price = p.prochee
            elif p.kabel:
                continue
            elif p.kod:
                type_ = 'kod'
                price = p.kod
            elif p.zakaz:
                type_ = 'zakaz'
                price = p.zakaz
            elif p.dop_uslugi:
                type_ = 'dop_uslugi'
                price = p.dop_uslugi
            elif p.slr:
                type_ = 'slr'
                price = p.slr

            cart = 'Наличка'
            if p.is_card:
                cart = 'Карточка'

            date_ = p.date

            manager = p.kassir

            edara_ilat = 'ФЛ'
            if p.edara_ilat == 'ЮЛ':
                edara_ilat = 'ЮЛ'

            data.append((number, name, p.abonent.etrap, p.kassir_etrap, edara_ilat, type_, manager, date_, cart, price))

        for p in pays_from_kabel_TV:
            cart = 'Наличка'
            if p.card:
                cart = 'Карточка'

            edara_ilat = 'ФЛ'
            if p.user.is_enterprises:
                edara_ilat = 'ЮЛ'

            data.append((p.user.number, p.user.name, 'Dashoguz', 'Dashoguz', edara_ilat, 'kabel', p.pay_kassir, p.pay_date, cart, p.pay))


        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= Dashoguz_Lena_plateji_2_za_{year}-{month_digit}.xlsx"

        return response


    if request.method == 'POST' and 'kod_8_lik_10_lyk_gepleshikleri' in request.POST:

        calls = NonLocalCall.objects.filter(DATE__range=[start[:10], end2[:10]], SUB_A_etrap=etrap)
        
        headers = ("SUB_A_etrap","SUB_A_number","SUB_B_locations", "SUB_B_number", "TYPE", "1_MIN_PRICE", "DATE", "START", "FIN", "DUR", "MT", "total_price", "file_name", "edara?")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)
        

        for c in calls:

            data.append((c.SUB_A_etrap,c.SUB_A,c.SUB_B_locations,c.SUB_B,c.type,c.price,c.DATE,c.START,c.FIN,c.DUR,c.MT,c.total_price,c.file_name,c.edara))

            
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap}_8_lik_10_lyk_gepleshikler_{year}-{month_digit}_.xlsx"

        return response 




    if request.method == 'POST' and 'all_tolegler' in request.POST:

        print('start', start)
        print('end2', end2)
        print('etrap', etrap)
        pays = PayHistory.objects.filter(date__range=[start, end2], kassir_etrap__in=[etrap, 'Внешние платежи'], abonent__etrap=etrap)
        
        headers = ("number", "abonent","internet","kabel", "alem", "telefon", "slr", "kod", "zakaz", "prochee", "dop_uslugi", "is_card", "kassir", "kassa", "total", "date", "edara_ilat", "type", "kassir_etrap")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)

        for p in pays:
            data.append((
            p.abonent.number,
            f"{p.abonent.surname} {p.abonent.name}",
            p.internet,
            p.kabel,
            p.alem,
            p.telefon,
            p.slr,
            p.kod,
            p.zakaz,
            p.prochee,
            p.dop_uslugi,
            p.is_card,
            p.kassir,
            p.kassa,
            p.total,
            p.date,
            p.edara_ilat,
            p.type,
            p.kassir_etrap
            ))
        
            
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap} all pays {year}-{month_digit}_.xlsx" 
        return response 


  


    if request.method == 'POST' and 'only_alem_for_DT_KT' in request.POST:

        print('start', start)
        print('end2', end2)
        print('etrap', etrap)

        number_alem = {}
        for i in range(20000, 105000):
            if i >= 80000 and i < 90000:
                continue
            number_alem[i] = 0

        pays = PayHistory.objects.filter(date__range=[start, end2], kassir_etrap__in=[etrap, 'Внешние платежи'], abonent__etrap=etrap)

        headers = ("number","alem")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)
        
        for p in pays:
            number_alem[int(p.abonent.number)] += p.alem 

        for num, alem in number_alem.items():
            data.append((num, -alem))

        

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap} alem pays for DT KT {year}-{month_digit}_.xlsx" 
        return response 


    if request.method == 'POST' and 'plateji_s_DZ_na_etrapy' in request.POST:

        print('start', start)
        print('end2', end2)
        print('etrap', etrap)

        number_alem = {}
        for i in range(20000, 105000):
            if i >= 80000 and i < 90000:
                continue
            number_alem[i] = 0

        pays = PayHistory.objects.filter(date__range=[start, end2], kassir_etrap__in=[etrap]).exclude(abonent__etrap=etrap)

        headers = ("abonent","internet","kabel", "alem", "telefon", "slr", "kod", "zakaz", "prochee", "dop_uslugi", "is_card", "kassir", "kassa", "total", "date", "edara_ilat", "type", "kassir_etrap")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)

        for p in pays:
            data.append((
            f"{p.abonent.surname} {p.abonent.name}",
            p.internet,
            p.kabel,
            p.alem,
            p.telefon,
            p.slr,
            p.kod,
            p.zakaz,
            p.prochee,
            p.dop_uslugi,
            p.is_card,
            p.kassir,
            p.kassa,
            p.total,
            p.date,
            p.edara_ilat,
            p.type,
            p.kassir_etrap
            ))

        

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap} alem pays for DT KT {year}-{month_digit}_.xlsx" 
        return response 

    

    if request.method == 'POST' and 'plateji_s_DZ_naEtrapy2' in request.POST:

        print('start', start)
        print('end2', end2)
        print('etrap', etrap)

        number_alem = {}
        for i in range(20000, 105000):
            if i >= 80000 and i < 90000:
                continue
            number_alem[i] = [0, '']

        pays = PayHistory.objects.filter(date__range=[start, end2], kassir_etrap__in=[etrap], edara_ilat='ФЛ').exclude(abonent__etrap=etrap)
        
        headers = ("etrap", "number","total")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)
        
        for p in pays:
            if not p.alem:
                number_alem[int(p.abonent.number)][0] += p.total
                number_alem[int(p.abonent.number)][1] = p.abonent.etrap 

        for num, total_etrap in number_alem.items():
            data.append((total_etrap[1], num, -total_etrap[0]))

        

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap} alem pays for DT KT {year}-{month_digit}_.xlsx" 
        return response 


    if request.method == 'POST' and 'plateji_po_abonentam' in request.POST:

        dict_ = {}
        for i in range(20000, 105000):
            if i < 80000 or i > 89999:
                dict_[i] = {
                    'telefon': 0,
                    'slr': 0,
                    'kod': 0,
                    'zakaz': 0,
                    'prochee': 0,
                    'dop_uslugi': 0,
                    'internet': 0,
                    'kabel': 0,
                    'alem': 0,
                    'kassir_etrap': ''
                }

        pays = PayHistory.objects.filter(abonent__etrap=etrap, date__range=[start, end2])
        
        
        if etrap == 'Dashoguz':
            kabelPays = KabelTvPayHistory.objects.filter(pay_date__range=[start, end2], user__is_enterprises=False)
            for kp in kabelPays:
                dict_[kp.user.number]['kabel'] += kp.pay

        headers = ("number", "telefon","slr","kod","zakaz","prochee","dop_uslugi","internet", "kabel", "alem", "kassir_etrap")
        data = []
        data = tablib.Dataset(*data, headers=headers)
        
       
        for p in pays:
            dict_[int(p.abonent.number)]['telefon'] += p.telefon
            dict_[int(p.abonent.number)]['slr'] += p.slr
            dict_[int(p.abonent.number)]['kod'] += p.kod
            dict_[int(p.abonent.number)]['zakaz'] += p.zakaz
            dict_[int(p.abonent.number)]['prochee'] += p.prochee
            dict_[int(p.abonent.number)]['dop_uslugi'] += p.dop_uslugi
            dict_[int(p.abonent.number)]['internet'] += p.internet
            dict_[int(p.abonent.number)]['alem'] += p.alem
            dict_[int(p.abonent.number)]['kassir_etrap'] = p.kassir_etrap

        for number, val in dict_.items():
            data.append((
                number, 
                val['telefon'], 
                val['slr'],
                val['kod'],
                val['zakaz'],
                val['prochee'],
                val['dop_uslugi'],
                val['internet'],
                val['kabel'],
                val['alem'],
                val['kassir_etrap'],
                ))

        


        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap} abonent tolegleri {year}-{month_digit}_.xlsx" 
        return response 




    if request.method == 'POST' and 'nach_po_abonentam' in request.POST:

        
        year_for_nach = start[:4] 
        month_for_nach = start[5:7]

        headers = ("number", "telefon","slr","kod","zakaz","prochee","dop_uslugi","internet", "kabel","alem")
        data = []
        data = tablib.Dataset(*data, headers=headers)

        dict_ = {}
        for i in range(20000, 105000):
            if i < 80000 or i > 89999:
                dict_[i] = {
                    'telefon': 0,
                    'slr': 0,
                    'kod': 0,
                    'zakaz': 0,
                    'prochee': 0,
                    'dop_uslugi': 0,
                    'internet': 0,
                    'kabel': 0,
                    'alem': 0,
                }

        if etrap == 'Dashoguz':
            kabelNachs = KabelNach.objects.filter(year=year_for_nach, month=month_for_nach, user__is_enterprises=False)

            for kn in kabelNachs:
                dict_[kn.user.number]['kabel'] = kn.nach
          
        nachs = NachMinus.objects.filter(user__etrap=etrap, year=year_for_nach, month=month_for_nach, user__is_enterprises=False)

        for p in nachs:
            dict_[int(p.user.number)]['telefon'] = p.telefon
            dict_[int(p.user.number)]['slr'] = p.slr
            dict_[int(p.user.number)]['kod'] = p.kod
            dict_[int(p.user.number)]['zakaz'] = p.zakaz
            dict_[int(p.user.number)]['prochee'] = p.prochee
            dict_[int(p.user.number)]['dop_uslugi'] = p.dop_uslugi
            dict_[int(p.user.number)]['internet'] = p.internet
            dict_[int(p.user.number)]['alem'] = p.alem

        for number, val in dict_.items():
            data.append((
                number, 
                val['telefon'], 
                val['slr'],
                val['kod'],
                val['zakaz'],
                val['prochee'],
                val['dop_uslugi'],
                val['internet'],
                val['kabel'],
                val['alem']
                ))
        

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap} abonent nachisleniya {year}-{month_digit}_.xlsx" 
        return response 


    # Вывод сагид телефония баланс за 1 января
    if request.method == 'POST' and 'wywod_sagid_balance_za_1_yanwara' in request.POST:

        headers = ("number", "telefoniya")
        data = []
        data = tablib.Dataset(*data, headers=headers)

        users = UserTable.objects.filter(etrap='Dashoguz')
        

        dict_ = {}
        for i in range(20000, 105000):
            dict_[i] = 0
        
        for u in users:
            dict_[int(u.number)] = u.s_prochee
        
        for number, telefoniya in dict_.items():
            data.append((number, telefoniya))

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap} sagid balance za 1 yanwara 2024_.xlsx" 
        return response 



    # Вывод всех платежей этрапа по месяцам
    if request.method == 'POST' and 'all_toleg_po_month' in request.POST:

        pays = PayHistory.objects.filter(abonent__etrap=etrap, date__range=[start, end2])

        headers = ("number", "telefon","slr","kod","zakaz", "prochee", "dop_uslugi", "internet", "kabel","alem", "is_card", "kassir", "kassa", "total", "date", "edara_ilat", "type", "kassir_etrap")
        data = []
        data = tablib.Dataset(*data, headers=headers)

        dict_ = {}
        for i in range(20000, 105000):
            dict_[i] = {
                'telefon': 0,
                'slr': 0,
                'kod': 0,
                'zakaz': 0,
                'prochee': 0,
                'dop_uslugi': 0,
                'internet': 0,
                'kabel': 0,
                'alem': 0,
                'is_card': '',
                'kassir': '',
                'kassa': '',
                'total': '',
                'date': '',
                'edara_ilat': '',
                'type': '',
                'kassir_etrap': '',
            }

        if etrap == 'Dashoguz':
            k_pays = KabelTvPayHistory.objects.filter(pay_date__range=[start, end2])

            for p in k_pays:
                dict_[p.user.number]['kabel'] += p.pay
                dict_[p.user.number]['date'] = p.pay_date
                dict_[p.user.number]['kassir'] = p.pay_kassir
                dict_[p.user.number]['is_card'] = p.card
           
        
        for p in pays:
            if p.kassir != 'admin':
                dict_[int(p.abonent.number)]['telefon'] += p.telefon
                dict_[int(p.abonent.number)]['slr'] += p.slr
                dict_[int(p.abonent.number)]['kod'] += p.kod
                dict_[int(p.abonent.number)]['zakaz'] += p.zakaz
                dict_[int(p.abonent.number)]['prochee'] += p.prochee
                dict_[int(p.abonent.number)]['dop_uslugi'] += p.dop_uslugi
                dict_[int(p.abonent.number)]['internet'] += p.internet
                dict_[int(p.abonent.number)]['alem'] += p.alem
                dict_[int(p.abonent.number)]['is_card'] = p.is_card
                dict_[int(p.abonent.number)]['kassir'] = p.kassir
                dict_[int(p.abonent.number)]['kassa'] = p.kassa
                dict_[int(p.abonent.number)]['total'] = p.total
                dict_[int(p.abonent.number)]['date'] = p.date
                dict_[int(p.abonent.number)]['edara_ilat'] = p.edara_ilat
                dict_[int(p.abonent.number)]['type'] = p.type
                dict_[int(p.abonent.number)]['kassir_etrap'] = p.kassir_etrap

   
        for number, v in dict_.items():
            data.append((
                number,
                v['telefon'],
                v['slr'],
                v['kod'],
                v['zakaz'],
                v['prochee'],
                v['dop_uslugi'],
                v['internet'],
                v['kabel'],
                v['alem'],
                v['is_card'],
                v['kassir'],
                v['kassa'],
                v['total'],
                v['date'],
                v['edara_ilat'],
                v['type'],
                v['kassir_etrap'],
                ))
 

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap} abonent toleg {year}-{month_digit}_.xlsx" 
        return response 

    # Вывод всех Начислений этрапа по месяцам
    if request.method == 'POST' and 'all_nach_po_month' in request.POST:

        year_for_nach = start[:4] 
        month_for_nach = start[5:7]

        print('year_for_nach', year_for_nach, type(year_for_nach))
        print('month_for_nach', month_for_nach, type(month_for_nach))

        headers = ("number", "telefon","slr","kod","zakaz", "prochee", "dop_uslugi", "internet", "kabel","alem", "edara", "is_active")
        data = []
        data = tablib.Dataset(*data, headers=headers)
        
        if etrap == 'Koneurgench' or etrap == 'Turkmenbashy' or etrap == 'Ruhubelent':
            
            template = {
                'telefon': 0,
                'slr': 0,
                'kod': 0,
                'zakaz': 0,
                'prochee': 0,
                'dop_uslugi': 0,
                'internet': 0,
                'kabel': 0,
                'alem': 0,
                'edara': '',
                'is_active': '',
            }
            
            if etrap == 'Koneurgench':
                dict_ = {i: template.copy() for i in chain(range(30000, 50000), range(70000, 80000))}
                if (month_digit_int == current_month and year_int == current_year) or \
                (month_digit_int == previous_month and year_int == previous_year):
                    get_edara_users = UserTable.objects.filter(etrap='Koneurgench', is_enterprises=True)
                    for u in get_edara_users:
                        num = int(u.number)
                        if num in dict_:
                            dict_[num]['edara'] = '+' 
                    get_active = UserTable.objects.filter(etrap='Koneurgench').filter(Q(name__isnull=False, name__gt='') | Q(surname__isnull=False, surname__gt=''))
                    for u in get_active:
                        num = int(u.number)
                        if num in dict_:
                            dict_[num]['is_active'] = 'active'
            elif etrap == 'Turkmenbashy':
                dict_ = {i: template.copy() for i in chain(range(30000, 33334), range(40000, 50000), range(70000, 80000))}
                if (month_digit_int == current_month and year_int == current_year) or \
                    (month_digit_int == previous_month and year_int == previous_year):
                        get_edara_users = UserTable.objects.filter(etrap='Turkmenbashy', is_enterprises=True)
                        for u in get_edara_users:
                            num = int(u.number)
                            if num in dict_:
                                dict_[num]['edara'] = '+' 
                        get_active = UserTable.objects.filter(etrap='Turkmenbashy').filter(Q(name__isnull=False, name__gt='') | Q(surname__isnull=False, surname__gt=''))
                        for u in get_active:
                            num = int(u.number)
                            if num in dict_:
                                dict_[num]['is_active'] = 'active'
            else:
                dict_ = {i: template.copy() for i in chain(range(30000, 50000), range(70000, 80000))}
                if (month_digit_int == current_month and year_int == current_year) or \
                    (month_digit_int == previous_month and year_int == previous_year):
                        get_edara_users = UserTable.objects.filter(etrap='Ruhubelent', is_enterprises=True)
                        for u in get_edara_users:
                            num = int(u.number)
                            if num in dict_:
                                dict_[num]['edara'] = '+' 
                        get_active = UserTable.objects.filter(etrap='Ruhubelent').filter(Q(name__isnull=False, name__gt='') | Q(surname__isnull=False, surname__gt=''))
                        for u in get_active:
                            num = int(u.number)
                            if num in dict_:
                                dict_[num]['is_active'] = 'active'
            

        elif etrap == 'Akdepe':
            template = {
                'telefon': 0,
                'slr': 0,
                'kod': 0,
                'zakaz': 0,
                'prochee': 0,
                'dop_uslugi': 0,
                'internet': 0,
                'kabel': 0,
                'alem': 0,
                'edara': '',
                'is_active': '',
            }
            dict_ = {i: template.copy() for i in chain(range(20000, 60000), range(70000, 80000), range(90000, 100000))}
            if (month_digit_int == current_month and year_int == current_year) or \
                    (month_digit_int == previous_month and year_int == previous_year):
                        get_edara_users = UserTable.objects.filter(etrap='Akdepe', is_enterprises=True)
                        for u in get_edara_users:
                            num = int(u.number)
                            if num in dict_:
                                dict_[num]['edara'] = '+' 
                        get_active = UserTable.objects.filter(etrap='Akdepe').filter(Q(name__isnull=False, name__gt='') | Q(surname__isnull=False, surname__gt=''))
                        for u in get_active:
                            num = int(u.number)
                            if num in dict_:
                                dict_[num]['is_active'] = 'active'

        elif etrap == 'S.A.Nyyazow' or etrap == 'Gorogly':
            template = {
                'telefon': 0,
                'slr': 0,
                'kod': 0,
                'zakaz': 0,
                'prochee': 0,
                'dop_uslugi': 0,
                'internet': 0,
                'kabel': 0,
                'alem': 0,
                'edara': '',
                'is_active': '',
            }
            dict_ = {i: template.copy() for i in chain(range(30000, 60000), range(70000, 80000))}
            if etrap == 'S.A.Nyyazow':
                if (month_digit_int == current_month and year_int == current_year) or \
                    (month_digit_int == previous_month and year_int == previous_year):
                        get_edara_users = UserTable.objects.filter(etrap='S.A.Nyyazow', is_enterprises=True)
                        for u in get_edara_users:
                            num = int(u.number)
                            if num in dict_:
                                dict_[num]['edara'] = '+' 
                        get_active = UserTable.objects.filter(etrap='S.A.Nyyazow').filter(Q(name__isnull=False, name__gt='') | Q(surname__isnull=False, surname__gt=''))
                        for u in get_active:
                            num = int(u.number)
                            if num in dict_:
                                dict_[num]['is_active'] = 'active'
            else:
                if (month_digit_int == current_month and year_int == current_year) or \
                    (month_digit_int == previous_month and year_int == previous_year):
                        get_edara_users = UserTable.objects.filter(etrap='Gorogly', is_enterprises=True)
                        for u in get_edara_users:
                            num = int(u.number)
                            if num in dict_:
                                dict_[num]['edara'] = '+'
                        get_active = UserTable.objects.filter(etrap='Gorogly').filter(Q(name__isnull=False, name__gt='') | Q(surname__isnull=False, surname__gt=''))
                        for u in get_active:
                            num = int(u.number)
                            if num in dict_:
                                dict_[num]['is_active'] = 'active'

        elif etrap == 'Boldumsaz':
            template = {
                'telefon': 0,
                'slr': 0,
                'kod': 0,
                'zakaz': 0,
                'prochee': 0,
                'dop_uslugi': 0,
                'internet': 0,
                'kabel': 0,
                'alem': 0,
                'edara': '',
                'is_active': '',
            }
            dict_ = {i: template.copy() for i in chain(range(20000, 80000), range(90000, 100000))}
            if (month_digit_int == current_month and year_int == current_year) or \
                (month_digit_int == previous_month and year_int == previous_year):
                    get_edara_users = UserTable.objects.filter(etrap='Boldumsaz', is_enterprises=True)
                    for u in get_edara_users:
                        num = int(u.number)
                        if num in dict_:
                            dict_[num]['edara'] = '+' 
                    get_active = UserTable.objects.filter(etrap='Boldumsaz').filter(Q(name__isnull=False, name__gt='') | Q(surname__isnull=False, surname__gt=''))
                    for u in get_active:
                        num = int(u.number)
                        if num in dict_:
                            dict_[num]['is_active'] = 'active'

        elif etrap == 'Garashsyzlyk':
            template = {
                'telefon': 0,
                'slr': 0,
                'kod': 0,
                'zakaz': 0,
                'prochee': 0,
                'dop_uslugi': 0,
                'internet': 0,
                'kabel': 0,
                'alem': 0,
                'edara': '',
                'is_active': '',
            }
            dict_ = {i: template.copy() for i in chain(range(20000, 40000), range(50000, 60000), range(70000, 80000), range(90000, 100000))}
            if (month_digit_int == current_month and year_int == current_year) or \
                (month_digit_int == previous_month and year_int == previous_year):
                    get_edara_users = UserTable.objects.filter(etrap='Garashsyzlyk', is_enterprises=True)
                    for u in get_edara_users:
                        num = int(u.number)
                        if num in dict_:
                            dict_[num]['edara'] = '+' 
                    get_active = UserTable.objects.filter(etrap='Garashsyzlyk').filter(Q(name__isnull=False, name__gt='') | Q(surname__isnull=False, surname__gt=''))
                    for u in get_active:
                        num = int(u.number)
                        if num in dict_:
                            dict_[num]['is_active'] = 'active'

        else:
            dict_ = {}
            for i in range(20000, 105000):
                dict_[i] = {
                    'telefon': 0,
                    'slr': 0,
                    'kod': 0,
                    'zakaz': 0,
                    'prochee': 0,
                    'dop_uslugi': 0,
                    'internet': 0,
                    'kabel': 0,
                    'alem': 0,
                    'edara': '',
                    'is_active': '',
                }
            if (month_digit_int == current_month and year_int == current_year) or \
                (month_digit_int == previous_month and year_int == previous_year):
                    get_edara_users = UserTable.objects.filter(etrap='Dashoguz', is_enterprises=True)
                    for u in get_edara_users:
                        num = int(u.number)
                        if num in dict_:
                            dict_[num]['edara'] = '+' 
                    get_active = UserTable.objects.filter(etrap='Dashoguz').filter(Q(name__isnull=False, name__gt='') | Q(surname__isnull=False, surname__gt=''))
                    for u in get_active:
                        num = int(u.number)
                        if num in dict_:
                            dict_[num]['is_active'] = 'active'

        nachs = NachMinus.objects.filter(user__etrap=etrap, year=year_for_nach, month=month_for_nach) # , user__is_enterprises=False
        
        if etrap == 'Dashoguz':
            k_nachs = KabelNach.objects.filter(year=year_for_nach, month=month_for_nach)
            for n in k_nachs:
                dict_[int(n.user.number)]['kabel'] += n.nach

        for n in nachs:
            dict_[int(n.user.number)]['telefon'] += n.telefon
            dict_[int(n.user.number)]['slr'] += n.slr
            dict_[int(n.user.number)]['kod'] += n.kod
            dict_[int(n.user.number)]['zakaz'] += n.zakaz
            dict_[int(n.user.number)]['prochee'] += n.prochee
            dict_[int(n.user.number)]['dop_uslugi'] += n.dop_uslugi
            dict_[int(n.user.number)]['internet'] += n.internet
            dict_[int(n.user.number)]['alem'] += n.alem

        for number, v in dict_.items():
            data.append((
                number,
                v['telefon'],
                v['slr'],
                v['kod'],
                v['zakaz'],
                v['prochee'],
                v['dop_uslugi'],
                v['internet'],
                v['kabel'],
                v['alem'],
                v['edara'],
                v['is_active']
                ))

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap} all nach {year}-{month_digit}_.xlsx" 
        return response 

    # Вывод всех платежей этрапа по дням
    if request.method == 'POST' and 'all_toleg_po_day_telefoniya' in request.POST:
        pays = PayHistory.objects.filter(abonent__etrap=etrap, date__range=[start, end2])

        headers = ("number", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "", "jemi")
        data = []
        data = tablib.Dataset(*data, headers=headers)
        if etrap == 'Koneurgench' or etrap == 'Turkmenbashy' or etrap == 'Ruhubelent':
            template = {str(i): 0 for i in range(1, 32)}
            template['jemi'] = 0
            if etrap == 'Turkmenbashy':
                dict_ = {i: template.copy() for i in chain(range(30000, 33334), range(40000, 50000), range(70000, 80000))}
            else:
                dict_ = {i: template.copy() for i in chain(range(30000, 50000), range(70000, 80000))}
        elif etrap == 'Akdepe':
            template = {str(i): 0 for i in range(1, 32)}
            template['jemi'] = 0
            dict_ = {i: template.copy() for i in chain(range(20000, 60000), range(70000, 80000), range(90000, 100000))}
        elif etrap == 'S.A.Nyyazow' or etrap == 'Gorogly':
            template = {str(i): 0 for i in range(1, 32)}
            template['jemi'] = 0
            dict_ = {i: template.copy() for i in chain(range(30000, 60000), range(70000, 80000))}
        elif etrap == 'Boldumsaz':
            template = {str(i): 0 for i in range(1, 32)}
            template['jemi'] = 0
            dict_ = {i: template.copy() for i in chain(range(20000, 80000), range(90000, 100000))}
        elif etrap == 'Garashsyzlyk':
            template = {str(i): 0 for i in range(1, 32)}
            template['jemi'] = 0
            dict_ = {i: template.copy() for i in chain(range(20000, 40000), range(50000, 60000), range(70000, 80000), range(90000, 100000))}
            
        else:    
            dict_ = {}
            for i in range(20000, 100000):
                dict_[i] = {
                    '1': 0,
                    '2': 0,
                    '3': 0,
                    '4': 0,
                    '5': 0,
                    '6': 0,
                    '7': 0,
                    '8': 0,
                    '9': 0,
                    '10': 0,
                    '11': 0,
                    '12': 0,
                    '13': 0,
                    '14': 0,
                    '15': 0,
                    '16': 0,
                    '17': 0,
                    '18': 0,
                    '19': 0,
                    '20': 0,
                    '21': 0,
                    '22': 0,
                    '23': 0,
                    '24': 0,
                    '25': 0,
                    '26': 0,
                    '27': 0,
                    '28': 0,
                    '29': 0,
                    '30': 0,
                    '31': 0,
                    'jemi':0,
                }
        for p in pays:
            number = int(p.abonent.number)
            total = p.prochee
            jemi = 0
            if total != 0:
                dict_[number]['jemi'] += total
                if p.date.day == 1:
                    dict_[number]['1'] += total
                elif p.date.day == 2:
                    dict_[number]['2'] += total
                elif p.date.day == 3:
                    dict_[number]['3'] += total
                elif p.date.day == 4:
                    dict_[number]['4'] += total
                elif p.date.day == 5:
                    dict_[number]['5'] += total
                elif p.date.day == 6:
                    dict_[number]['6'] += total
                elif p.date.day == 7:
                    dict_[number]['7'] += total
                elif p.date.day == 8:
                    dict_[number]['8'] += total
                elif p.date.day == 9:
                    dict_[number]['9'] += total
                elif p.date.day == 10:
                    dict_[number]['10'] += total
                elif p.date.day == 11:
                    dict_[number]['11'] += total
                elif p.date.day == 12:
                    dict_[number]['12'] += total
                elif p.date.day == 13:
                    dict_[number]['13'] += total
                elif p.date.day == 14:
                    dict_[number]['14'] += total
                elif p.date.day == 15:
                    dict_[number]['15'] += total
                elif p.date.day == 16:
                    dict_[number]['16'] += total
                elif p.date.day == 17:
                    dict_[number]['17'] += total
                elif p.date.day == 18:
                    dict_[number]['18'] += total
                elif p.date.day == 19:
                    dict_[number]['19'] += total
                elif p.date.day == 20:
                    dict_[number]['20'] += total
                elif p.date.day == 21:
                    dict_[number]['21'] += total
                elif p.date.day == 22:
                    dict_[number]['22'] += total
                elif p.date.day == 23:
                    dict_[number]['23'] += total
                elif p.date.day == 24:
                    dict_[number]['24'] += total
                elif p.date.day == 25:
                    dict_[number]['25'] += total
                elif p.date.day == 26:
                    dict_[number]['26'] += total
                elif p.date.day == 27:
                    dict_[number]['27'] += total
                elif p.date.day == 28:
                    dict_[number]['28'] += total
                elif p.date.day == 29:
                    dict_[number]['29'] += total
                elif p.date.day == 30:
                    dict_[number]['30'] += total
                elif p.date.day == 31:
                    dict_[number]['31'] += total
                


    
        for number, v in dict_.items():
            data.append((
                number,
                v['1'],
                v['2'],
                v['3'],
                v['4'],
                v['5'],
                v['6'],
                v['7'],
                v['8'],
                v['9'],
                v['10'],
                v['11'],
                v['12'],
                v['13'],
                v['14'],
                v['15'],
                v['16'],
                v['17'],
                v['18'],
                v['19'],
                v['20'],
                v['21'],
                v['22'],
                v['23'],
                v['24'],
                v['25'],
                v['26'],
                v['27'],
                v['28'],
                v['29'],
                v['30'],
                v['31'],
                '', 
                v['jemi'],
            ))
        
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap} abonent toleg Po dnyam telefoniya {year}-{month_digit}_.xlsx" 
        return response
    

    if request.method == 'POST' and 'zakaz_calls' in request.POST:
        zakaz = Zakaz.objects.filter(DATE__range=[start, end2], total_price__gt=0)

        headers = ("SUB A", "SUB B", "NUMBER_LOCATIONS", "DATE", "DUR", "MT", "1 min BAHA", "Jemi baha", "Scyot")
        data = []
        data = tablib.Dataset(*data, headers=headers)
        users = UserTable.objects.filter(etrap='Dashoguz', is_enterprises=True)
        dict_ = {}
        for u in users:
            dict_[int(u.number)] = u.account

        for z in zakaz:
            try:
                account = dict_[int(z.NUMBER_A)]
            except:
                account = 0
            data.append((z.NUMBER_A, z.NUMBER_B, z.NUMBER_LOCATIONS, z.DATE, z.DUR, z.MT, z.price, z.total_price, account))
            

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= zakaz gepleshikler {year}-{month_digit}_.xlsx" 
        return response 


    
    if request.method == 'POST' and 'calls_for_k' in request.POST:

        calls = NonLocalCall.objects.filter(DATE__range=[start[:10], end2[:10]], SUB_A_etrap=etrap, edara__in=['E', 'I'])
        
        headers = ("SUB_A_etrap","SUB_A_number","SUB_B_locations", "SUB_B_number", "TYPE", "1_MIN_PRICE", "DATE", "START", "FIN", "DUR", "MT", "total_price", "file_name")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)
        

        for c in calls:

            data.append((c.SUB_A_etrap,c.SUB_A,c.SUB_B_locations,c.SUB_B,c.type,c.price,c.DATE,c.START,c.FIN,c.DUR,c.MT,c.total_price,c.file_name))

            
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap}_8_lik_10_lyk_gepleshikler_{year}-{month_digit}_.xlsx"

        return response 


    if request.method == 'POST' and 'mahri_poprosila' in request.POST:

        # users = UserTable.objects.filter(etrap=etrap)
        users = UserTable.objects.filter(etrap=etrap)\
            .select_related("hb")\
            .prefetch_related("service")
        headers = ("Number","Ady","Koche","Jay","Kwartira",'Abonplata',"HB", "balance_telefoniya", "balance_internet", "balance_alem", "Lgota", "Usluga", "kod", "slr")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)
        
        print("year", year)
        print("month_digit", month_digit)
        
        nachs = (
            NachMinus.objects
            .filter(user__etrap=etrap, year=year, month=month_digit)
            .filter(Q(kod__gt=0) | Q(slr__gt=0))
            .values("user__number")
            .annotate(
                kod_sum=Sum("kod"),
                slr_sum=Sum("slr")
            )
        )

        number_kod_slr = {}

        for i in nachs:
            number_kod_slr[int(i["user__number"])] = {
                "kod": i["kod_sum"] or 0,
                "slr": i["slr_sum"] or 0
            }
        

        for u in users:
            number = int(u.number)
            # if u.name or u.surname or u.abonplata or u.street or u.home or u.flat:
            # usluga = ''
            # if u.service.all().exists():
            # services = u.service.all()
            # if services:
            #     count = 0
            #     for s in services:
            #         count += 1
            #         if count == 1:
            #             usluga += f'{count}) {s.service} = {s.price} m'
            #         else:
            #             usluga += f', {count}) {s.service} = {s.price} m'
            services = u.service.all()

            usluga = ", ".join(
                f"{i+1}) {s.service} = {s.price} m"
                for i, s in enumerate(services)
            )
            hb = ''
            if u.hb:
                hb = u.hb.name


            surname = u.surname if u.surname != None else ''
            name = u.name if u.name != None else ''
            ady = f"{surname} {name}"
            street = u.street if u.street != None else ''
            home = u.home if u.home != None else ''
            flat = u.flat if u.flat != None else ''
            # account = u.account if u.account != None else 0
            abonplata = u.abonplata if u.abonplata != None else 0
            # hb = u.hb.name if u.hb != None else 0
            telefoniya = u.b_telefon+u.b_slr+u.b_kod+u.b_zakaz+u.b_prochee+u.b_dop_uslugi
            lgota = "+" if u.beneficiary else ""
            
            nach = number_kod_slr.get(number)
            if nach:
                kod = nach["kod"]
                slr = nach["slr"]
            else:
                kod = ""
                slr = ""
    
            data.append((u.number, ady, street, home, flat, abonplata, hb, telefoniya, u.b_internet, u.b_alem, lgota, usluga, kod, slr ))
                
            
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= Baza_{etrap}.xlsx"

        return response
    

    if request.method == 'POST' and 'export_old_logins_and_active_logins2' in request.POST:
        records = OldLoginDogowor.objects.filter(etrap=etrap)

        headers = (
            "Номер", "Этрап",
            "Login (Old)", "Dogowor (Old)",
            "Login (UserTable)", "Dogowor (UserTable)",
            "Совпадение",  # ✅ Новая колонка
            "Дата сохранения в old", "Предприятие", "H или B", "Кто сохранил", "Счет №", "Сохранено при действии"
        )

        data = tablib.Dataset(headers=headers)

        for r in records:
            created_at = r.created_at.strftime('%d.%m.%Y') if r.created_at else ''
            is_ent = 'Да' if r.is_enterprises else 'Нет'
            hb = r.hb or ''
            operator = r.operator or ''
            account = r.account if r.account is not None else ''
            saved_action = r.saved_in_action or ''

            # 👇 ищем UserTable по совпадению login или dogowor И только если etrap совпадает
            matched_users = UserTable.objects.filter(
                etrap=r.etrap
            ).filter(
                (models.Q(login=r.login) & ~models.Q(login='')) |
                (models.Q(dogowor=r.dogowor) & ~models.Q(dogowor=''))
            )

            for user in matched_users:
                # Определим по чему совпало
                match = ''
                if r.login and r.login == user.login:
                    match += 'Login '
                if r.dogowor and r.dogowor == user.dogowor:
                    match += 'Dogowor'

                data.append((
                    r.number or '', r.etrap or '',
                    r.login or '', r.dogowor or '',
                    user.login or '', user.dogowor or '',
                    match.strip() if match else '',
                    created_at, is_ent, hb, operator, account, saved_action
                ))

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="OldLogins_Match_By_LoginOrDogowor_EtrapSensitive.xlsx"'
        return response


    

    if request.method == 'POST' and 'export_users_with_slr_or_kod' in request.POST:
        # значения задаёшь сверху
        # year = 2025
        # month = 9
        # etrap = "Ашгабат"

        # фильтрация по NachMinus
        nach = NachMinus.objects.filter(
            user__etrap=etrap,
            year=year,
            month=monthСonvert(month_word)
        )

        headers = ("Номер телефона",)
        data = tablib.Dataset(headers=headers)

        for n in nach:
            u = n.user
            if not u.name and not u.surname:  # имя и фамилия пустые
                data.append((u.number,))

        response = HttpResponse(data.xlsx, content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = f'attachment; filename="Users_NachMinus_slr_kod_empty_number.xlsx"'
        return response
    
    
    if request.method == 'POST' and 'export_AlemNachData' in request.POST:
        # Заголовки для Excel
        headers = [
            "Номер телефона", "Этрап", "Год", "Месяц", "Пользователь",
            "Договор", "Учетное имя", "Тариф", "Услуга",
            "Списание по тарифу", "Списание за услугу",
            "Кол-во (шт.)", "Итого", "Валюта", "on_off", "Файл", "Начислен"
        ]
        
        dataset = tablib.Dataset(headers=headers)
        
        # Берем все объекты AlemNachData
        records = AlemNachData.objects.filter(etrap=etrap, year=year, month=monthСonvert(month_word))
        
        for r in records:
            dataset.append([
                r.number or "",
                r.etrap or "",
                r.year or "",
                r.month or "",
                r.name or "",
                r.dogowor or "",
                r.account_name or "",
                r.tariff or "",
                r.service or "",
                float(r.tariff_charge or 0),
                float(r.service_charge or 0),
                float(r.quantity or 0),
                float(r.total or 0),
                r.currency or "",
                r.on_off or "",
                r.file_name or "",
                "Да" if r.is_nach else "Нет"
            ])
        
        # Отдаем файл в формате Excel
        response = HttpResponse(dataset.export('xlsx'), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="alem_data.xlsx"'
        return response
    
    
    if request.method == 'POST' and 'export_AlemNachData_joined_numbers' in request.POST:
        headers = [
        "Номер телефона", "Этрап", "Год", "Месяц", "Пользователь",
        "Договор", "Учетное имя", "Тариф", "Услуга",
        "Списание по тарифу", "Списание за услугу",
        "Кол-во (шт.)", "Итого", "Валюта", "on_off", "Файл", "Начислен"
        ]
        
        dataset = tablib.Dataset(headers=headers)
        
        # Фильтруем записи
        records = AlemNachData.objects.filter(etrap=etrap, year=year, month=monthСonvert(month_word))
        
        # Группируем по номеру телефона
        grouped = {}
        for r in records:
            key = r.number
            if key not in grouped:
                grouped[key] = {
                    "etrap": r.etrap,
                    "year": r.year,
                    "month": r.month,
                    "name": r.name,
                    "dogowor": r.dogowor,
                    "account_name": r.account_name,
                    "tariff": r.tariff,
                    "service": r.service,
                    "tariff_charge": r.tariff_charge or 0,
                    "service_charge": r.service_charge or 0,
                    "quantity": r.quantity or 0,
                    "total": r.total or 0,
                    "currency": r.currency,
                    "on_off": r.on_off,
                    "file_name": r.file_name,
                    "is_nach": r.is_nach
                }
            else:
                # Суммируем нужные поля
                grouped[key]["tariff_charge"] += r.tariff_charge or 0
                grouped[key]["service_charge"] += r.service_charge or 0
                grouped[key]["quantity"] += r.quantity or 0
                grouped[key]["total"] += r.total or 0
        
        # Добавляем в dataset
        for number, data in grouped.items():
            dataset.append([
                number or "",
                data["etrap"] or "",
                data["year"] or "",
                data["month"] or "",
                data["name"] or "",
                data["dogowor"] or "",
                data["account_name"] or "",
                data["tariff"] or "",
                data["service"] or "",
                float(data["tariff_charge"]),
                float(data["service_charge"]),
                float(data["quantity"]),
                float(data["total"]),
                data["currency"] or "",
                data["on_off"] or "",
                data["file_name"] or "",
                "Да" if data["is_nach"] else "Нет"
            ])
        
        response = HttpResponse(
            dataset.export('xlsx'),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="alem_data.xlsx"'
        return response
    



    return render(request, 'telekom/MATB/otchyot/prochie_otchoty.html', context)