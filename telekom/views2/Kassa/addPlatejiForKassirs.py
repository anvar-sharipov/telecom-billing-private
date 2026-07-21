from django.shortcuts import render, redirect
from telekom.models import DontRepeatYourself, OldLoginDogowor, PayHistory, PlatejiWhichAddKassirsEveryDay, UserTable
from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert
from django.contrib import messages
from datetime import date, datetime, timedelta
from calendar import monthrange
from tablib import Dataset






def addPlatejiForKassirs(request):
    context={}
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'Kassa' or request.user.is_superuser:
        log = EtrapAndGroup[0]
        context['kassaIndex'] = True
        context['addPlatejiForKassirs'] = True
    else:
        messages.error(request, f'Вход в кассу разрешено только соотрудникам кассы')
        return redirect('user-login')
    context['log'] = log


    current_date = str(date.today())
    context['current_date'] = current_date
    current_year = current_date[0:4]
    current_month = current_date[5:7]
    current_day = current_date[-2:]
    # days_in_choosed_month = monthrange(int(current_year), int(current_month))[1]

    days = []
    for day in range(1,32):
        days.append(day)
    context['days'] = days

    context['already_have'] = False

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['etraps'] = etraps
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

    # managers = ManagerNames
    etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else log
    month = request.GET.get('month') if request.GET.get('month') != None else monthСonvert(current_month)
    year = request.GET.get('year') if request.GET.get('year') != None else current_year
    day_ = request.GET.get('day')
    context['month'] = month
    context['year'] = year
    context['etrap'] = etrap
    context['month_digit'] = monthСonvert(month)
    if day_:
        context['day_'] = int(day_)
        chossed_day = datetime(int(year), int(monthСonvert(month)), int(day_))
        next_date = chossed_day + timedelta(days=1)
        next_year = str(next_date.date())[0:4]
        next_month = str(next_date.date())[5:7]
        next_day = str(next_date.date())[-2:]
 

    context['error'] = False
    if month and year and etrap and day_:
        try:
            pays = PayHistory.objects.filter(date__range=[f"{year}-{str(monthСonvert(month))}-{str(day_)}", f"{next_year}-{next_month}-{next_day}"])
        except:
            messages.error(request, f"Ошибка в дате")
            context['error'] = True
            return render(request, 'telekom/Kassa/addPlatejiForKassirs.html', context)
        total_sum_internet = 0
        total_sum_abonplata = 0
        total_sum_alem = 0
        total_sum_kabel = 0
        for p in pays:
            total_sum_internet += p.internet
            total_sum_abonplata += p.prochee
            total_sum_alem += p.alem
            total_sum_kabel += p.kabel

        context['total_sum_internet'] = f"{total_sum_internet:_}"
        context['total_sum_abonplata'] = f"{total_sum_abonplata:_}"
        context['total_sum_alem'] = f"{total_sum_alem:_}"
        context['total_sum_kabel'] = f"{total_sum_kabel:_}"
        total = total_sum_alem + total_sum_abonplata + total_sum_internet + total_sum_kabel
        context['summ'] = f"{total:_}"
        context['pays_'] = pays

        kassirsList = []
        for pay in pays:
            if pay.kassir not in kassirsList:
                kassirsList.append(pay.kassir)
        context['kassirsList'] = kassirsList

    # Если нажал на фильтр по кассирам
    if request.method == 'POST' and 'kassirSelect' in request.POST:
        kassirSelect = request.POST.get('kassirSelect')
        context['kassirSelect'] = kassirSelect
        if kassirSelect != 'all':
            pays = pays.filter(kassir=kassirSelect)
            context['pays_'] = pays

            total_sum_internet = 0
            total_sum_abonplata = 0
            total_sum_alem = 0
            total_sum_kabel = 0
            for p in pays:
                total_sum_internet += p.internet
                total_sum_abonplata += p.prochee
                total_sum_alem += p.alem
                total_sum_kabel += p.kabel

            context['total_sum_internet'] = f"{total_sum_internet:_}"
            context['total_sum_abonplata'] = f"{total_sum_abonplata:_}"
            context['total_sum_alem'] = f"{total_sum_alem:_}"
            context['total_sum_kabel'] = f"{total_sum_kabel:_}"
            total = total_sum_alem + total_sum_abonplata + total_sum_internet + total_sum_kabel
            context['summ'] = f"{total:_}"


    #  Если нажал на добавить или проверить
    if request.method == 'POST' and 'platejiSKassy' in request.POST:
        users = UserTable.objects.filter(etrap=etrap)
        oldUsers = OldLoginDogowor.objects.filter(etrap=etrap)
        number_pk = {}
        dogowor_number = {}
        oldDogowor_number = {}
        for user in users:
            number_pk[user.number] = user.pk
            if user.dogowor:
                dogowor_number[user.dogowor.lower()] = user.number

        for user in oldUsers:
            oldDogowor_number[user.dogowor.lower()] = user.number

        dataset = Dataset()
        try:
            xlsx_data = request.FILES['my_file2']
        except:
            messages.error(request, f'Выберите Файл')
            return render(request, 'telekom/Kassa/addPlatejiForKassirs.html', context)
   
        try:
            imported_data = dataset.load(xlsx_data.read(), format='xlsx')
        except:
            messages.error(request, f'Файл должен быть формата xlsx')
            return render(request, 'telekom/Kassa/addPlatejiForKassirs.html', context)
        
        if year not in str(xlsx_data).lower() or monthСonvert(month) not in str(xlsx_data).lower() or day_ not in str(xlsx_data).lower():
            messages.error(request, f'В имени файла должны быть "{year} {monthСonvert(month)} {day_}"')
            return render(request, 'telekom/Kassa/addPlatejiForKassirs.html', context)
        count = 0
        errorList = [] # 

        try:
            DontRepeatYourself.objects.get(platejiSkassyKassirami=f"{str(xlsx_data)}")
            context['already_have'] = True
        except:
            context['already_have'] = False
        # 0=adyFam, 1=dogowor, 2=nomerPlateja,  3=price,  4=manager,  5=datePlatej,  6=datePlatejProweden,  7=account,    8=cartOrNo,    9=platejPorucheniye,   10=comment,   11=operator,   12=kodOplaty  
        # Если нажал на проверить
        if request.POST.get('platejiTest') == 'on':
            count = 0
            countInt = 0
            countAbon = 0
            countAlem = 0
            total_priceInt = 0
            total_priceAbon = 0
            total_priceAlem = 0
            for d in imported_data:
                count += 1
                name = d[0] if d[0] != None else ''
                if d[1]:
                    if isinstance(d[1], int):
                        dogowor = d[1]
                    else:
                        dogowor = d[1].lower().strip()
                else:
                    errorList.append([name, d[1], price, manager, datePay, is_cart, 'Договор пуст'])
                    continue
                payNumber = d[2] if d[2] != None else ''
                price = d[3] if d[3] != None else ''
                manager = d[4] if d[4] != None else ''
                datePay = d[5] if d[5] != None else ''
                datePayAccept = d[6] if d[6] != None else ''
                account = d[7] if d[7] != None else ''
                is_cartStr = d[8] if d[8] != None else ''
                payPoruchenie = d[9] if d[9] != None else ''
                comment = d[10] if d[10] != None else ''
                operator = d[11] if d[11] != None else ''
                kodOplaty = d[12] if d[12] != None else ''
                
                # для абонплат платежей
                if isinstance(dogowor, int):
                    number = str(dogowor)[-5:]
                    try:
                        user = users.get(pk=number_pk[number])
                    except:
                        errorList.append([name, d[1], price, manager, datePay, is_cart, 'Нет такого номера в БД'])
                        continue

                    is_cart = True if 'картой' in is_cartStr.lower() else False
                    total_priceAbon += price
                    countAbon += 1
            
                else:
                    # для интернет платежей
                    if 'dza' in dogowor or 'dnz' in dogowor or 'dad' in dogowor or 'dge' in dogowor or 'dbs' in dogowor or 'dgd' in dogowor or 'dgo' in dogowor or 'dku' in dogowor or 'drb' in dogowor or 'dtb' in dogowor:
                        try:
                            number = dogowor_number[dogowor]
                        except:
                            try:
                                number = oldDogowor_number[dogowor]
                            except:
                                try:
                                    number = kodOplaty[-5:]
                                except:
                                    errorList.append([name, d[1], price, manager, datePay, is_cartStr, 'Ошибки по договору'])
                                    continue
                        try:
                            user = users.get(pk=number_pk[number])
                        except:
                            errorList.append([name, d[1], price, manager, datePay, is_cart, f'Нет такого номера в БД {str(number)}'])
                            continue
                        total_priceInt += price
                        countInt += 1

                    # для alem платежей
                    elif 'iptv' in dogowor:
                        number = ''.join(filter(str.isdigit, dogowor))[-5:]
           
                        try:
                            user = users.get(pk=number_pk[number])
                        except:
                            errorList.append([name, d[1], price, manager, datePay, is_cartStr, 'Нет такого номера в БД'])
                            continue
                        total_priceAlem += price
                        countAlem += 1
                    # абонплаты с old
                    else:
                        number = ''.join(filter(str.isdigit, dogowor))[-5:]
                        try:
                            user = users.get(pk=number_pk[number])
                        except:
                            errorList.append([name, d[1], price, manager, datePay, is_cartStr, 'Нет такого номера в БД'])
                            continue
                        total_priceAbon += price
                        countAbon += 1





            if errorList:
                messages.error(request, f"Ошибка")
                context['errorList'] = errorList
                context['xlsx_data'] = str(xlsx_data)
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/errorBillingPlatejiFromKassa.html', context)
            else:
                context['total_priceAbon'] = f"{total_priceAbon:,}"
                context['total_priceAlem'] = f"{total_priceAlem:,}"
                context['total_priceInt'] = f"{total_priceInt:,}"
                context['countInt'] = countInt
                context['countAbon'] = countAbon
                context['countAlem'] = countAlem
                context['totalCount'] = count
                total_umumy = total_priceAbon + total_priceAlem + total_priceInt
                context['total_umumy'] = f"{total_umumy:,}"
                
                
        else:
            # Если нажал на добавить
            count = 0
            countInt = 0
            countAbon = 0
            countAlem = 0
            total_priceInt = 0
            total_priceAbon = 0
            total_priceAlem = 0
            pk_pays = {} # {pk: [int, abon, alem]}
            bulk_update_user = []
            bulk_create_pay = []
            bulk_create_pay_in_db = []
            for d in imported_data:
                count += 1
                name = d[0] if d[0] != None else ''
                if d[1]:
                    if isinstance(d[1], int):
                        dogowor = d[1]
                    else:
                        dogowor = d[1].lower().strip()
                else:
                    errorList.append([name, d[1], price, manager, datePay, is_cart, 'Договор пуст'])
                    continue
                nomerPlateja = d[2] if d[2] != None else ''
                price = d[3] if d[3] != None else ''
                manager = d[4] if d[4] != None else ''
                datePay = d[5] if d[5] != None else ''
                datePlatejProweden = d[6] if d[6] != None else ''
                account = d[7] if d[7] != None else ''
                is_cartStr = d[8] if d[8] != None else ''
                payPorucheniye = d[9] if d[9] != None else ''
                comment = d[10] if d[10] != None else ''
                operator = d[11] if d[11] != None else ''
                kodOplaty = d[12] if d[12] != None else ''
                
                # для абонплат платежей
                if isinstance(dogowor, int):
                    number = str(dogowor)[-5:]
                    try:
                        user = users.get(pk=number_pk[number])
                    except:
                        errorList.append([name, d[1], price, manager, datePay, is_cart, 'Нет такого номера в БД'])
                        continue

                    is_cart = True if 'картой' in is_cartStr.lower() else False

                    if user.pk not in pk_pays:
                        pk_pays[user.pk] = [0,price,0]
                    else:
                        pk_pays[user.pk][1] += price
                    obj = PayHistory(abonent=user, prochee=price, date=datePay, is_card=is_cart, kassa=manager, kassir=manager, total=price)
                    bulk_create_pay.append(obj)


                    obj2 = PlatejiWhichAddKassirsEveryDay(
                        number=number, 
                        etrap=user.etrap, 
                        name=name, 
                        dogowor=dogowor, 
                        nomerPlateja=nomerPlateja, 
                        price=price, 
                        manager=manager, 
                        date=datePay,
                        datePlatejProweden=datePlatejProweden,
                        account=account, 
                        is_cart=is_cart, 
                        payPorucheniye=payPorucheniye,
                        comment=comment,
                        operator=operator,
                        kodOplaty=kodOplaty)
                    bulk_create_pay_in_db.append(obj2)

                    total_priceAbon += price
                    countAbon += 1
            
                else:
                    # для интернет платежей
                    if 'dza' in dogowor or 'dnz' in dogowor or 'dad' in dogowor or 'dge' in dogowor or 'dbs' in dogowor or 'dgd' in dogowor or 'dgo' in dogowor or 'dku' in dogowor or 'drb' in dogowor or 'dtb' in dogowor:
                        try:
                            number = dogowor_number[dogowor]
                        except:
                            try:
                                number = oldDogowor_number[dogowor]
                            except:
                                try:
                                    number = kodOplaty[-5:]
                                except:
                                    errorList.append([name, d[1], price, manager, datePay, is_cartStr, 'Ошибки по договору'])
                                    continue
                        try:
                            user = users.get(pk=number_pk[number])
                        except:
                            errorList.append([name, d[1], price, manager, datePay, is_cart, f'Нет такого номера в БД {str(number)}'])
                            continue
                        
                        is_cart = True if 'картой' in is_cartStr.lower() else False

                        if user.pk not in pk_pays:
                            pk_pays[user.pk] = [price,0,0]
                        else:
                            pk_pays[user.pk][0] += price
                        obj = PayHistory(abonent=user, internet=price, date=datePay, is_card=is_cart, kassa=manager, kassir=manager, total=price)
                        bulk_create_pay.append(obj)

                        obj2 = PlatejiWhichAddKassirsEveryDay(
                            number=number, 
                            etrap=user.etrap, 
                            name=name, 
                            dogowor=dogowor, 
                            nomerPlateja=nomerPlateja, 
                            price=price, 
                            manager=manager, 
                            date=datePay,
                            datePlatejProweden=datePlatejProweden,
                            account=account, 
                            is_cart=is_cart, 
                            payPorucheniye=payPorucheniye,
                            comment=comment,
                            operator=operator,
                            kodOplaty=kodOplaty)
                        bulk_create_pay_in_db.append(obj2)

                        total_priceInt += price
                        countInt += 1

                    # для alem платежей
                    elif 'iptv' in dogowor:
                        number = ''.join(filter(str.isdigit, dogowor))[-5:]
           
                        try:
                            user = users.get(pk=number_pk[number])
                        except:
                            errorList.append([name, d[1], price, manager, datePay, is_cartStr, 'Нет такого номера в БД'])
                            continue

                        is_cart = True if 'картой' in is_cartStr.lower() else False

                        if user.pk not in pk_pays:
                            pk_pays[user.pk] = [0,0,price]
                        else:
                            pk_pays[user.pk][2] += price
                        obj = PayHistory(abonent=user, alem=price, date=datePay, is_card=is_cart, kassa=manager, kassir=manager, total=price)
                        bulk_create_pay.append(obj)

                        obj2 = PlatejiWhichAddKassirsEveryDay(
                            number=number, 
                            etrap=user.etrap, 
                            name=name, 
                            dogowor=dogowor, 
                            nomerPlateja=nomerPlateja, 
                            price=price, 
                            manager=manager, 
                            date=datePay,
                            datePlatejProweden=datePlatejProweden,
                            account=account, 
                            is_cart=is_cart, 
                            payPorucheniye=payPorucheniye,
                            comment=comment,
                            operator=operator,
                            kodOplaty=kodOplaty)
                        bulk_create_pay_in_db.append(obj2)

                        total_priceAlem += price
                        countAlem += 1
                    # абонплаты с old
                    else:
                        number = ''.join(filter(str.isdigit, dogowor))[-5:]
                        try:
                            user = users.get(pk=number_pk[number])
                        except:
                            errorList.append([name, d[1], price, manager, datePay, is_cartStr, 'Нет такого номера в БД'])
                            continue

                        is_cart = True if 'картой' in is_cartStr.lower() else False

                        if user.pk not in pk_pays:
                            pk_pays[user.pk] = [0,price,0]
                        else:
                            pk_pays[user.pk][1] += price
                        obj = PayHistory(abonent=user, prochee=price, date=datePay, is_card=is_cart, kassa=manager, kassir=manager, total=price)
                        bulk_create_pay.append(obj)

                        obj2 = PlatejiWhichAddKassirsEveryDay(
                            number=number, 
                            etrap=user.etrap, 
                            name=name, 
                            dogowor=dogowor, 
                            nomerPlateja=nomerPlateja, 
                            price=price, 
                            manager=manager, 
                            date=datePay,
                            datePlatejProweden=datePlatejProweden,
                            account=account, 
                            is_cart=is_cart, 
                            payPorucheniye=payPorucheniye,
                            comment=comment,
                            operator=operator,
                            kodOplaty=kodOplaty)
                        bulk_create_pay_in_db.append(obj2)

                        total_priceAbon += price
                        countAbon += 1



            
                
            # Еще раз проверяем не был ли начислен этот файл раньше
            try:
                DontRepeatYourself.objects.get(platejiSkassyKassirami=f"{str(xlsx_data)}")
                context['already_have'] = True
                messages.error(request, f'ОШИБКА! Файл {str(xlsx_data)} уже был начислен')
                return render(request, 'telekom/Kassa/addPlatejiForKassirs.html', context)
                
            except:
                pass
            if errorList:
                messages.error(request, f"Ошибка")
                context['errorList'] = errorList
                context['xlsx_data'] = str(xlsx_data)
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/errorBillingPlatejiFromKassa.html', context)
            else:

                if pk_pays:
                    for pk, pays in pk_pays.items():
                        user = UserTable.objects.get(pk=pk)
                        user.b_internet += pays[0]
                        user.b_telefon += pays[1]
                        user.b_alem += pays[2]
                        bulk_update_user.append(user)
                    
                    UserTable.objects.bulk_update(bulk_update_user, ['b_internet', 'b_telefon', 'b_alem'])

                if bulk_create_pay:
                    PayHistory.objects.bulk_create(bulk_create_pay)
            
                if bulk_create_pay_in_db:
                    PlatejiWhichAddKassirsEveryDay.objects.bulk_create(bulk_create_pay_in_db)

            
                DontRepeatYourself.objects.create(platejiSkassyKassirami=f"{str(xlsx_data)}")

                messages.success(request, f"Успешное добавление платежей с файла {str(xlsx_data)} за {str(day_)} {month} {year} Года")

                pays = PayHistory.objects.filter(date__range=[f"{year}-{str(monthСonvert(month))}-{str(day_)}", f"{next_year}-{next_month}-{next_day}"])
                total_sum_internet = 0
                total_sum_abonplata = 0
                total_sum_alem = 0
                total_sum_kabel = 0
                for p in pays:
                    total_sum_internet += p.internet
                    total_sum_abonplata += p.prochee
                    total_sum_alem += p.alem
                    total_sum_kabel += p.kabel

                context['total_sum_internet'] = f"{total_sum_internet:_}"
                context['total_sum_abonplata'] = f"{total_sum_abonplata:_}"
                context['total_sum_alem'] = f"{total_sum_alem:_}"
                context['total_sum_kabel'] = f"{total_sum_kabel:_}"
                total = total_sum_alem + total_sum_abonplata + total_sum_internet + total_sum_kabel
                context['summ'] = f"{total:_}"
                context['pays_'] = pays

                kassirsList = []
                for pay in pays:
                    if pay.kassir not in kassirsList:
                        kassirsList.append(pay.kassir)
                context['kassirsList'] = kassirsList
         

                context['total_priceAbon'] = f"{total_priceAbon:,}"
                context['total_priceAlem'] = f"{total_priceAlem:,}"
                context['total_priceInt'] = f"{total_priceInt:,}"
                context['countInt'] = countInt
                context['countAbon'] = countAbon
                context['countAlem'] = countAlem
                context['totalCount'] = count
                total_umumy = total_priceAbon + total_priceAlem + total_priceInt
                context['total_umumy'] = f"{total_umumy:,}"
                context['already_have'] = True
            

    

    return render(request, 'telekom/Kassa/addPlatejiForKassirs.html', context)