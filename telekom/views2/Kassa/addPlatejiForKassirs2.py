from django.shortcuts import render, redirect
from django.contrib import messages

from datetime import date, datetime, timedelta
from telekom.models import KassaExcelFiles, ManagerNames, OldLoginDogowor, PayHistory, PlatejiWhichAddKassirsEveryDay, StaffAction, UserTable, KabelTvNew, SaveInfoAboutWhoAddAndNachPaysFromBilling
from tablib import Dataset

from telekom.views2.myFunc.myFunc import getEtrapNameFromCode, monthСonvert
import re

from django.db import transaction

import logging

logger = logging.getLogger(__name__)




def addPlatejiForKassirs2(request):
    # Это для лены для добавления платежей с реестре в БД одной кнопкой
    # testPays = PayHistory.objects.filter(date__range=[f"2024-02-01 00:00:00", f"2024-03-01 23:59:59"], kabel=0)
    # testPays = PayHistory.objects.filter(date__range=[f"2024-02-01 00:00:00", f"2024-03-01 23:59:59"], kabel__gt=0).update(internet=0, alem=0, prochee=0, slr=0, telefon=0, kod=0, zakaz=0, dop_uslugi=0)
    # print(len(testPays))
    context = {}
    # test_pays = PayHistory.objects.filter(date__range=[f"2024-02-01 00:00:00", f"2024-03-01 23:59:59"], abonent__etrap='Turkmenbashy')
    
    # test_total_price_alem = 0
    # test_total_price_int = 0
    # test_total_price_abon = 0
    # for p in test_pays:
    #     test_total_price_alem += p.alem
    #     test_total_price_int += p.internet
    #     test_total_price_abon += p.prochee


    # test_pays2 = PlatejiWhichAddKassirsEveryDay.objects.filter(file_name='plateji_Turkmenbashy_2024_02.xlsx')
    # test_total_price_alem2 = 0
    # test_total_price_int2 = 0
    # test_total_price_abon2 = 0
    # for p in test_pays2:
    #     if p.type_pay == 'Abonplata':
    #         test_total_price_abon2 += p.price
    #     elif p.type_pay == 'Alem':
    #         test_total_price_alem2 += p.price
    #     elif p.type_pay == 'Internet':
    #         test_total_price_int2 += p.price      


    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.username in ['intizar_gorogly', 'lenashb', 'testMTBDZ', 'AyshatGoroglyMtb', 'GuljahanAkdepeMtb', 'AzizShabatMtb', 'Saryyewa_Gozel_Shabat_MTB', 'BaharKoneurgenchKassa', 'Merjen_Yylally_MTB', 'GozelGubadagMtb', 'SelbiBoldumsazMtb', 'MahymAkdepeMtb', 'Aramedowa_Oguljemal', 'shirmamedowa_gulalek', 'Jumyazowa_Oguljemal', 'Kurbanowa_Gulnabat_Koneurgench', 'Baltabayewa_Sewara_MTB_DGE', 'Ishangulyyewa_Nurjemal_Koneurgench_kassa']:
            log = 'Dashoguz'
            context['addPlatejiForKassirs2'] = True
            if request.user.is_superuser:
                context['kassaIndex'] = True 
            else:
                context['SHBIndex'] = True 
                context['matbIndex'] = True 
        else:
            messages.error(request, f'Доступ разрешен только администратору')
            return redirect('user-login')
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')

    groups = request.user.groups.all()
    request_user_etrap = None
    for g in groups:
        request_user_etrap, request_user_type = g.name.split('_')
        # print('request_user_etrap', request_user_etrap)
        # print('request_user_type', request_user_type)

    if request.user.is_superuser and request.user.username == 'admin1':
        request_user_etrap = 'Dashoguz'

    if not request_user_etrap:
        messages.error(request, f'Не достаточно прав')
        return redirect('user-login')


    
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

    context['days'] = [i for i in range(1, 32)]
    

    current_date = str(date.today())
    context['current_date'] = current_date
    current_year = current_date[0:4]
    current_month = current_date[5:7]

    month = request.GET.get('month')
    year = request.GET.get('year')
    day = int(request.GET.get('day')) if request.GET.get('day') != None else False

    context['month'] = month
    context['year'] = year
    context['day'] = day
    context['month_digit'] = monthСonvert(month)

    
    
    
    if year and month and day:
        chossed_day = datetime(int(year), int(monthСonvert(month)), 1)
        next_date = chossed_day + timedelta(days=1)
        next_year = str(next_date.date())[0:4]
        next_month = str(next_date.date())[5:7]
        # pays = PayHistory.objects.filter(date__range=[f"{year}-{str(monthСonvert(month))}-01", f"{next_year}-{next_month}-01"])

    if request.method == 'POST' and 'platejiSKassy' in request.POST:
        if len(str(day)) == 1:
            day2 = f"0{str(day)}"
        else:
            day2 = str(day)
        need_str = [f'{year}-{monthСonvert(month)}-{day2}', f'{day2}-{monthСonvert(month)}-{year}', f'{year}.{monthСonvert(month)}.{day2}', f'{day2}.{monthСonvert(month)}.{year}', f'{year}_{monthСonvert(month)}_{day2}', f'{day2}_{monthСonvert(month)}_{year}', f'{year} {monthСonvert(month)} {day2}', f'{day2} {monthСonvert(month)} {year}']

        

        
        
        logger.info(f'==== Подготовка файлов')
        dataset = Dataset()
        try:
            xlsx_data = request.FILES['my_file2']
        except:
            messages.error(request, f'Выберите Файл')
            return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)
   
        try:
            imported_data = dataset.load(xlsx_data.read(), format='xlsx')
        except:
            messages.error(request, f'Файл должен быть формата xlsx')
            return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)


        try:
            SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.get(file_name = str(xlsx_data))
            messages.error(request, f'Файл уже добавлен в БД (2)')
            return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)
        except:
            pass

        managarNames = {}
        have_name = False
        have_date = False
        for i in ManagerNames.objects.all():
            if i.name in str(xlsx_data):
                have_name = True
            managarNames[i.name] = i.etrap

        for i in need_str:
            # print(str(xlsx_data), i)
            if i in str(xlsx_data):
                have_date = True
        
        # if have_date == False and have_name == False:
        #     messages.error(request, f'!Ошибка, в ФИО менеджера и дате платежей: {str(xlsx_data)}')
        #     return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)
        if have_date == False:
            messages.error(request, f'!Ошибка, в дате платежей:  {str(xlsx_data)}')
            return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)
        # if have_name == False:
        #     messages.error(request, f'!Ошибка, в ФИО менеджера:  {str(xlsx_data)}')
        #     return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)

       
        already_nach = False
        if len(PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=str(xlsx_data))) > 0:
            already_nach = True
        
            
        count = 0
        users = UserTable.objects.all()
        oldUsers = OldLoginDogowor.objects.all()
        code_number_pk = {}
        dogowor_pk = {}
        oldDogowor_number = {}
        for user in users:
            if user.etrap == 'Dashoguz':
                code_number_pk[f"322{user.number}"] = user.pk
            if user.etrap == 'Akdepe':
                code_number_pk[f"344{user.number}"] = user.pk
            if user.etrap == 'Boldumsaz':
                code_number_pk[f"346{user.number}"] = user.pk
            if user.etrap == 'Gorogly':
                code_number_pk[f"340{user.number}"] = user.pk
            if user.etrap == 'Koneurgench':
                code_number_pk[f"347{user.number}"] = user.pk
            if user.etrap == 'Turkmenbashy':
                code_number_pk[f"349{user.number}"] = user.pk
            if user.etrap == 'S.A.Nyyazow':
                code_number_pk[f"348{user.number}"] = user.pk
            if user.etrap == 'Ruhubelent':
                code_number_pk[f"342{user.number}"] = user.pk
            if user.etrap == 'Garashsyzlyk':
                code_number_pk[f"343{user.number}"] = user.pk
            if user.etrap == 'Gubadag':
                code_number_pk[f"345{user.number}"] = user.pk

            if user.dogowor:
                dogowor_pk[user.dogowor.lower().strip()] = [user.pk, user.number]

        for user in oldUsers:
            oldDogowor_number[user.dogowor.lower()] = user.number

        
        

        iptvCount = 0
        intCount = 0
        abonplataCount = 0
        kabelCount = 0
        total_price_iptv = 0
        total_price_internet = 0
        total_price_abonplata = 0
        total_price_kabel = 0
        errorList = []
        date_convertered_to_price = []
        bulk_create = []
        errorManager = []


        # 2 = wnPlateji, Default, Картой,       3=Manager,       4=Признак скорректированного платежа,     6=data plateja,    9= №п/п,   10=Код оплаты,   11=dogowor,  12=Ф.И.О,   13=ФЛ ЮЛ,  14=price
        # 0=Пользователь	1=Договор	2=Номер платежа	3=Сумма	4=Менеджер	5=Дата платежа	6=Платёж проведен	7=Номер счёта	8=Категория	9=Платёжное поручение	10=Комментарий	11=Оператор	12=Код оплаты

        for d in imported_data:
            # Проверка есть ли этот менеджер в ManagerNames или в ExternalPayments
            manager = d[4].strip()

            
            if manager not in managarNames and manager not in errorManager:
                errorManager.append(manager)
                try:
                    with transaction.atomic():
                        ManagerNames.objects.create(name=manager)
                except Exception as e:
                    messages.error(request, f'ошибка с transaction при сохранении нового менеджера в ManagerNames, тип ошибки == {e}')
                    logger.error(f'ошибка с transaction при сохранении нового менеджера в ManagerNames, тип ошибки == {e}')
                    return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)  
                managarNames[manager] = None
                continue
            elif managarNames[manager] == '' or managarNames[manager] == None:
                if manager not in errorManager:
                    errorManager.append(manager)
                    continue
                

            # конверт дату в цену
            if isinstance(d[3], date):
                price_date = str(d[3])
                if price_date[8:10] == '01':
                    manat = int(price_date[5:7])
                    coin = int(price_date[2:4])
                    price = float(f"{str(manat)}.{str(coin)}")
                else:
                    manat = int(price_date[8:10])
                    coin = int(price_date[5:7])
                    price = float(f"{str(manat)}.{str(coin)}")
                date_convertered_to_price.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Вместо даты будет цена {str(price)} Если вы не согласны с ценами рекомендую прописать их вручную в excel файле, а если согласны с ценами, то можно добавлять, но под вашу ответственность"])
            else:
                price = float(d[3])

            # CTV если кабель платеж
            if 'CTV' in str(d[1]):
                string = d[1].strip()
                kabelCount += 1
                total_price_kabel += price

                kod_ = re.search(r'993(\d{3})', string)
                if kod_:
                    code = kod_.group(1)
                    user_etrap = getEtrapNameFromCode(code)
                    number_ = re.search(rf'{code}(\d+)', string)
                    if number_:
                        number = number_.group(1)
                        # try:
                        #     user_pk = code_number_pk[f"{code}{number}"]
                        # except:
                        #     errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа или номер в договоре некорректный"])
                        #     continue

                        try:
                            user = KabelTvNew.objects.get(number=number)
                        except:
                            errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Не найден по PK в KabelTVNew"])
                            continue

                        # try:
                        #     user = UserTable.objects.get(pk=user_pk)
                        # except:
                        #     errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Не найден по PK в UserTable"])
                        #     continue
                    else:
                        errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Номер в договоре некорректный"])
                        continue
                else:
                    errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа в договоре некорректный"])
                    continue

                type_ = 'Kabel'
                kod_oplaty = d[12] if d[12] != None else ''
                obj = PlatejiWhichAddKassirsEveryDay(
                    number=user.number, 
                    user_etrap='Dashoguz', 
                    kassir_etrap=managarNames[manager],
                    type_pay=type_,
                    pay_category=d[8].strip(),
                    manager=manager,
                    date=d[5],
                    kodOplaty=kod_oplaty,
                    dogowor=str(d[1]),
                    name=d[0],
                    is_enterprises='ФЛ',
                    price=price,
                    file_name=str(xlsx_data),
                    who_add_file=request.user.username
                    )
                bulk_create.append(obj)

                count += 1
                continue
                # print(user_etrap, code, number, user_pk, type_)
            
            # абонплата
            elif isinstance(d[1], int):
                dogowor=d[1]
                abonplataCount += 1
                total_price_abonplata += price
                number = str(dogowor)[-5:]
                code = str(dogowor)[-8:-5]
                user_etrap = getEtrapNameFromCode(code)
                if user_etrap:
                    try:
                        user_pk = code_number_pk[f"{code}{number}"]
                    except:
                        errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа или номер в договоре некорректный"])
                        continue
                    try:
                        user = UserTable.objects.get(pk=user_pk)
                    except:
                        errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Не найден по PK"])
                        continue
                else:
                    errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа или номер в договоре некорректный"])
                    continue
                
                # if user_etrap == "Akdepe":
                #     num = int(number)
                #     if (
                #         26000 <= num <= 26991 or
                #         28000 <= num <= 28031 or
                #         58800 <= num <= 58928 or
                #         59296 <= num <= 59423 or
                #         59056 <= num <= 59183 
                #     ):
                #         user_etrap = "Garashsyzlyk"
                
                # if user_etrap == "Boldumsaz":
                #     num = int(number)
                #     if (
                #         26000 <= num <= 26991 or
                #         28000 <= num <= 28031 or
                #         58800 <= num <= 58928 or
                #         59296 <= num <= 59423 or
                #         59056 <= num <= 59183 
                #     ):
                #         user_etrap = "Gubadag"

                type_ = 'Abonplata'
            
            else:
                dogowor = d[1].lower().strip()
                if 'ikdz' in dogowor:
                    continue
                # alem
                if 'iptv' in dogowor:
                    iptvCount += 1
                    total_price_iptv += price
                    number = ''.join(filter(str.isdigit, dogowor))[-5:]
                    code = ''.join(filter(str.isdigit, dogowor))[-8:-5]
                    user_etrap = getEtrapNameFromCode(code)
                    if user_etrap:
                        try:
                            user_pk = code_number_pk[f"{code}{number}"]
                        except:
                            errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа или номер в договоре некорректный"])
                            continue
                        user = UserTable.objects.get(pk=user_pk)
                    else:
                        errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа или номер в договоре некорректный"])
                        continue
                    
                    # if user_etrap == "Akdepe":
                    #     num = int(number)
                    #     if (
                    #         26000 <= num <= 26991 or
                    #         28000 <= num <= 28031 or
                    #         58800 <= num <= 58928 or
                    #         59296 <= num <= 59423 or
                    #         59056 <= num <= 59183 
                    #     ):
                    #         user_etrap = "Garashsyzlyk"
                    
                    # if user_etrap == "Boldumsaz":
                    #     num = int(number)
                    #     if (
                    #         26000 <= num <= 26991 or
                    #         28000 <= num <= 28031 or
                    #         58800 <= num <= 58928 or
                    #         59296 <= num <= 59423 or
                    #         59056 <= num <= 59183 
                    #     ):
                    #         user_etrap = "Gubadag"
                            
                            
                    type_='Alem'
                # internet
                elif 'dza' in dogowor or 'dad' in dogowor or 'dbs' in dogowor or 'dgd' in dogowor or 'dge' in dogowor or 'dgo' in dogowor or 'dku' in dogowor or 'dnz' in dogowor or 'drb' in dogowor or 'dtb' in dogowor:
                    intCount += 1
                    total_price_internet += price
                    try:
                        user = UserTable.objects.get(pk=dogowor_pk[dogowor][0])
                    except:
                        try:
                            old_user = OldLoginDogowor.objects.get(dogowor=dogowor.upper())
                            user = UserTable.objects.get(etrap=old_user.etrap, number=old_user.number)
                        except:
                            errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Договор не найден в базе"]) 
                            continue
                    type_='Internet'
                # abonplata
                elif 'old' in dogowor:
                    dogowor = dogowor.replace('old', '')
                    if '-' in dogowor:
                        dogowor = dogowor.replace('-', '')
                    if '_' in dogowor:
                        dogowor = dogowor.replace('_', '')
                    # проверка есть ли другие символы кроме цифр в договоре
                    if any(char.isdigit() for char in dogowor):
                        # Содержит только цифры
                        abonplataCount += 1
                        total_price_abonplata += price
                        number = str(dogowor)[-5:]
                        code = str(dogowor)[-8:-5]
                        user_etrap = getEtrapNameFromCode(code)
                        if user_etrap:
                            try:
                                user_pk = code_number_pk[f"{code}{number}"]
                            except:
                                errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа или номер в договоре некорректный"])
                                continue
                            user = UserTable.objects.get(pk=user_pk)
                        else:
                            errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа или номер в договоре некорректный"])
                            continue
                    else:
                        errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Непонятный договор"])
                        continue
                    
                    # if user_etrap == "Akdepe":
                    #     num = int(number)
                    #     if (
                    #         26000 <= num <= 26991 or
                    #         28000 <= num <= 28031 or
                    #         58800 <= num <= 58928 or
                    #         59296 <= num <= 59423 or
                    #         59056 <= num <= 59183 
                    #     ):
                    #         user_etrap = "Garashsyzlyk"
                    
                    # if user_etrap == "Boldumsaz":
                    #     num = int(number)
                    #     if (
                    #         26000 <= num <= 26991 or
                    #         28000 <= num <= 28031 or
                    #         58800 <= num <= 58928 or
                    #         59296 <= num <= 59423 or
                    #         59056 <= num <= 59183 
                    #     ):
                    #         user_etrap = "Gubadag"
                    
                    type_='Abonplata'
                else:
                    errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Непонятный договор"])
                    continue
    
            # 2 = wnPlateji, Default, Картой,       3=Manager,       4=Признак скорректированного платежа,     6=data plateja,    9= №п/п,   10=Код оплаты,   11=dogowor,  12=Ф.И.О,   13=ФЛ ЮЛ,  14=price
            # 0=Пользователь	1=Договор	2=Номер платежа	3=Сумма	4=Менеджер	5=Дата платежа	6=Платёж проведен	7=Номер счёта	8=Категория	9=Платёжное поручение	10=Комментарий	11=Оператор	12=Код оплаты
            kod_oplaty = d[12] if d[12] != None else ''
            obj = PlatejiWhichAddKassirsEveryDay(
                number=user.number, 
                user_etrap=user.etrap, 
                kassir_etrap=managarNames[manager],
                type_pay=type_,
                pay_category=d[8].strip(),
                manager=manager,
                date=d[5],
                kodOplaty=kod_oplaty,
                dogowor=str(d[1]),
                name=d[0],
                is_enterprises='ФЛ',
                price=price,
                file_name=str(xlsx_data),
                who_add_file=request.user.username
                )
            bulk_create.append(obj)

            count += 1

        
        if request.POST.get('platejiTest'):
            logger.info(f'==== Проверено ==== {count}')
        else:
            logger.info(f'==== Добавлено ==== {count}')
        if errorList:
            messages.error(request, f"Ошибка")
            context['errorList'] = errorList
            context['xlsx_data'] = str(xlsx_data)
            return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/errorBillingPlatejiFromKassa.html', context)
        
        if errorManager:
            messages.error(request, f"Ошибка! есть новые менеджеры, надо определить их тип")
            context['errorManager'] = errorManager
            return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)
        
        if have_date == False and have_name == False:
            messages.error(request, f'!Ошибка, в ФИО менеджера и дате платежей: {str(xlsx_data)}')
            return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)
        if have_name == False:
            messages.error(request, f'!Ошибка, в ФИО менеджера:  {str(xlsx_data)}')
            return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)

        totalCount = abonplataCount + iptvCount + intCount + kabelCount
        totalPice = float('%.2f' % (total_price_abonplata + total_price_iptv + total_price_internet + total_price_kabel))
        context['abonplataCount'] = f"{abonplataCount:_}"
        context['total_price_abonplata'] = f"{float('%.2f' % (total_price_abonplata)):_}"
        context['iptvCount'] = f"{iptvCount:_}"
        context['total_price_iptv'] = f"{float('%.2f' % (total_price_iptv)):_}"
        context['intCount'] = f"{intCount:_}"
        context['total_price_internet'] = f"{float('%.2f' % (total_price_internet)):_}"

        context['kabelCount'] = f"{kabelCount:_}"
        context['total_price_kabel'] = f"{float('%.2f' % (total_price_kabel)):_}"

        context['totalCount'] = f"{totalCount:_}"
        context['totalPice'] = f"{totalPice:_}"

        if already_nach:
            messages.error(request, f'Этот файл "{str(xlsx_data)}" уже был добавлен в базу платежей')
            return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)

        if request.POST.get('platejiTest'):
            # Проверка
            if date_convertered_to_price:
                messages.error(request, f"Есть Ошибки! дата вместо цены")
                context['errorList'] = date_convertered_to_price
                context['xlsx_data'] = str(xlsx_data)
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/errorBillingPlatejiFromKassa.html', context)
            messages.success(request, f"Проверка прошла успешно")
        else:
            # Добавить
            try:
                with transaction.atomic():
                    if bulk_create:
                        PlatejiWhichAddKassirsEveryDay.objects.bulk_create(bulk_create)
                    StaffAction.objects.create(user=request.user, comment=f'Добавления платежей в Базу Данных, файл {str(xlsx_data)}, дата добавления {datetime.now()}, добавил {request.user.username}', action='Добавления платежей в базу')
                    SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.create(
                        file_name=str(xlsx_data),
                        etrap_add=request_user_etrap,
                        who_add=request.user.username,
                        when_add=datetime.now()
                    )
                    KassaExcelFiles.objects.create(operator=request.user, document=xlsx_data)
                    messages.success(request, f"Успешно добавлено в БД")
            except Exception as e:
                messages.error(request, f'ошибка с transaction при сохранении, тип ошибки == {e}')
                logger.error(f'ошибка с transaction при сохранении, тип ошибки == {e}')






    return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)


# rabotaet, no net Garashsyzlyk i Gubadag
# from django.shortcuts import render, redirect
# from django.contrib import messages

# from datetime import date, datetime, timedelta
# from telekom.models import KassaExcelFiles, ManagerNames, OldLoginDogowor, PayHistory, PlatejiWhichAddKassirsEveryDay, StaffAction, UserTable, KabelTvNew, SaveInfoAboutWhoAddAndNachPaysFromBilling
# from tablib import Dataset

# from telekom.views2.myFunc.myFunc import getEtrapNameFromCode, monthСonvert
# import re

# from django.db import transaction

# import logging

# logger = logging.getLogger(__name__)




# def addPlatejiForKassirs2(request):
#     # Это для лены для добавления платежей с реестре в БД одной кнопкой
#     # testPays = PayHistory.objects.filter(date__range=[f"2024-02-01 00:00:00", f"2024-03-01 23:59:59"], kabel=0)
#     # testPays = PayHistory.objects.filter(date__range=[f"2024-02-01 00:00:00", f"2024-03-01 23:59:59"], kabel__gt=0).update(internet=0, alem=0, prochee=0, slr=0, telefon=0, kod=0, zakaz=0, dop_uslugi=0)
#     # print(len(testPays))
#     context = {}
#     # test_pays = PayHistory.objects.filter(date__range=[f"2024-02-01 00:00:00", f"2024-03-01 23:59:59"], abonent__etrap='Turkmenbashy')
    
#     # test_total_price_alem = 0
#     # test_total_price_int = 0
#     # test_total_price_abon = 0
#     # for p in test_pays:
#     #     test_total_price_alem += p.alem
#     #     test_total_price_int += p.internet
#     #     test_total_price_abon += p.prochee


#     # test_pays2 = PlatejiWhichAddKassirsEveryDay.objects.filter(file_name='plateji_Turkmenbashy_2024_02.xlsx')
#     # test_total_price_alem2 = 0
#     # test_total_price_int2 = 0
#     # test_total_price_abon2 = 0
#     # for p in test_pays2:
#     #     if p.type_pay == 'Abonplata':
#     #         test_total_price_abon2 += p.price
#     #     elif p.type_pay == 'Alem':
#     #         test_total_price_alem2 += p.price
#     #     elif p.type_pay == 'Internet':
#     #         test_total_price_int2 += p.price      


#     if request.user.is_authenticated:
#         if request.user.is_superuser or request.user.username in ['lenashb', 'testMTBDZ', 'AyshatGoroglyMtb', 'GuljahanAkdepeMtb', 'AzizShabatMtb', 'Saryyewa_Gozel_Shabat_MTB', 'BaharKoneurgenchKassa', 'Merjen_Yylally_MTB', 'GozelGubadagMtb', 'SelbiBoldumsazMtb', 'MahymAkdepeMtb', 'Aramedowa_Oguljemal', 'Jumyazowa_Oguljemal', 'Kurbanowa_Gulnabat_Koneurgench']:
#             log = 'Dashoguz'
#             context['addPlatejiForKassirs2'] = True
#             if request.user.is_superuser:
#                 context['kassaIndex'] = True 
#             else:
#                 context['SHBIndex'] = True 
#                 context['matbIndex'] = True 
#         else:
#             messages.error(request, f'Доступ разрешен только администратору')
#             return redirect('user-login')
#     else:
#         messages.error(request, f'Вы не аутентифицированы')
#         return redirect('user-login')

#     groups = request.user.groups.all()
#     request_user_etrap = None
#     for g in groups:
#         request_user_etrap, request_user_type = g.name.split('_')
#         # print('request_user_etrap', request_user_etrap)
#         # print('request_user_type', request_user_type)

#     if request.user.is_superuser and request.user.username == 'admin1':
#         request_user_etrap = 'Dashoguz'

#     if not request_user_etrap:
#         messages.error(request, f'Не достаточно прав')
#         return redirect('user-login')


    
#     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
#     context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
#     context['years'] = ['2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

#     context['days'] = [i for i in range(1, 32)]
    

#     current_date = str(date.today())
#     context['current_date'] = current_date
#     current_year = current_date[0:4]
#     current_month = current_date[5:7]

#     month = request.GET.get('month')
#     year = request.GET.get('year')
#     day = int(request.GET.get('day')) if request.GET.get('day') != None else False

#     context['month'] = month
#     context['year'] = year
#     context['day'] = day
#     context['month_digit'] = monthСonvert(month)

    
    
    
#     if year and month and day:
#         chossed_day = datetime(int(year), int(monthСonvert(month)), 1)
#         next_date = chossed_day + timedelta(days=1)
#         next_year = str(next_date.date())[0:4]
#         next_month = str(next_date.date())[5:7]
#         # pays = PayHistory.objects.filter(date__range=[f"{year}-{str(monthСonvert(month))}-01", f"{next_year}-{next_month}-01"])

#     if request.method == 'POST' and 'platejiSKassy' in request.POST:
#         if len(str(day)) == 1:
#             day2 = f"0{str(day)}"
#         else:
#             day2 = str(day)
#         need_str = [f'{year}-{monthСonvert(month)}-{day2}', f'{day2}-{monthСonvert(month)}-{year}', f'{year}.{monthСonvert(month)}.{day2}', f'{day2}.{monthСonvert(month)}.{year}', f'{year}_{monthСonvert(month)}_{day2}', f'{day2}_{monthСonvert(month)}_{year}', f'{year} {monthСonvert(month)} {day2}', f'{day2} {monthСonvert(month)} {year}']

        

        
        
#         logger.info(f'==== Подготовка файлов')
#         dataset = Dataset()
#         try:
#             xlsx_data = request.FILES['my_file2']
#         except:
#             messages.error(request, f'Выберите Файл')
#             return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)
   
#         try:
#             imported_data = dataset.load(xlsx_data.read(), format='xlsx')
#         except:
#             messages.error(request, f'Файл должен быть формата xlsx')
#             return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)


#         try:
#             SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.get(file_name = str(xlsx_data))
#             messages.error(request, f'Файл уже добавлен в БД (2)')
#             return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)
#         except:
#             pass

#         managarNames = {}
#         have_name = False
#         have_date = False
#         for i in ManagerNames.objects.all():
#             if i.name in str(xlsx_data):
#                 have_name = True
#             managarNames[i.name] = i.etrap

#         for i in need_str:
#             # print(str(xlsx_data), i)
#             if i in str(xlsx_data):
#                 have_date = True
        
#         # if have_date == False and have_name == False:
#         #     messages.error(request, f'!Ошибка, в ФИО менеджера и дате платежей: {str(xlsx_data)}')
#         #     return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)
#         if have_date == False:
#             messages.error(request, f'!Ошибка, в дате платежей:  {str(xlsx_data)}')
#             return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)
#         # if have_name == False:
#         #     messages.error(request, f'!Ошибка, в ФИО менеджера:  {str(xlsx_data)}')
#         #     return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)

       
#         already_nach = False
#         if len(PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=str(xlsx_data))) > 0:
#             already_nach = True
        
            
#         count = 0
#         users = UserTable.objects.all()
#         oldUsers = OldLoginDogowor.objects.all()
#         code_number_pk = {}
#         dogowor_pk = {}
#         oldDogowor_number = {}
#         for user in users:
#             if user.etrap == 'Dashoguz':
#                 code_number_pk[f"322{user.number}"] = user.pk
#             if user.etrap == 'Akdepe':
#                 code_number_pk[f"344{user.number}"] = user.pk
#             if user.etrap == 'Boldumsaz':
#                 code_number_pk[f"346{user.number}"] = user.pk
#             if user.etrap == 'Gorogly':
#                 code_number_pk[f"340{user.number}"] = user.pk
#             if user.etrap == 'Koneurgench':
#                 code_number_pk[f"347{user.number}"] = user.pk
#             if user.etrap == 'Turkmenbashy':
#                 code_number_pk[f"349{user.number}"] = user.pk
#             if user.etrap == 'S.A.Nyyazow':
#                 code_number_pk[f"348{user.number}"] = user.pk
#             if user.etrap == 'Ruhubelent':
#                 code_number_pk[f"342{user.number}"] = user.pk

#             if user.dogowor:
#                 dogowor_pk[user.dogowor.lower().strip()] = [user.pk, user.number]

#         for user in oldUsers:
#             oldDogowor_number[user.dogowor.lower()] = user.number

        
        

#         iptvCount = 0
#         intCount = 0
#         abonplataCount = 0
#         kabelCount = 0
#         total_price_iptv = 0
#         total_price_internet = 0
#         total_price_abonplata = 0
#         total_price_kabel = 0
#         errorList = []
#         date_convertered_to_price = []
#         bulk_create = []
#         errorManager = []


#         # 2 = wnPlateji, Default, Картой,       3=Manager,       4=Признак скорректированного платежа,     6=data plateja,    9= №п/п,   10=Код оплаты,   11=dogowor,  12=Ф.И.О,   13=ФЛ ЮЛ,  14=price
#         # 0=Пользователь	1=Договор	2=Номер платежа	3=Сумма	4=Менеджер	5=Дата платежа	6=Платёж проведен	7=Номер счёта	8=Категория	9=Платёжное поручение	10=Комментарий	11=Оператор	12=Код оплаты

#         for d in imported_data:
#             # Проверка есть ли этот менеджер в ManagerNames или в ExternalPayments
#             manager = d[4].strip()

            
#             if manager not in managarNames and manager not in errorManager:
#                 errorManager.append(manager)
#                 try:
#                     with transaction.atomic():
#                         ManagerNames.objects.create(name=manager)
#                 except Exception as e:
#                     messages.error(request, f'ошибка с transaction при сохранении нового менеджера в ManagerNames, тип ошибки == {e}')
#                     logger.error(f'ошибка с transaction при сохранении нового менеджера в ManagerNames, тип ошибки == {e}')
#                     return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)  
#                 managarNames[manager] = None
#                 continue
#             elif managarNames[manager] == '' or managarNames[manager] == None:
#                 if manager not in errorManager:
#                     errorManager.append(manager)
#                     continue
                

#             # конверт дату в цену
#             if isinstance(d[3], date):
#                 price_date = str(d[3])
#                 if price_date[8:10] == '01':
#                     manat = int(price_date[5:7])
#                     coin = int(price_date[2:4])
#                     price = float(f"{str(manat)}.{str(coin)}")
#                 else:
#                     manat = int(price_date[8:10])
#                     coin = int(price_date[5:7])
#                     price = float(f"{str(manat)}.{str(coin)}")
#                 date_convertered_to_price.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Вместо даты будет цена {str(price)} Если вы не согласны с ценами рекомендую прописать их вручную в excel файле, а если согласны с ценами, то можно добавлять, но под вашу ответственность"])
#             else:
#                 price = float(d[3])

#             # CTV если кабель платеж
#             if 'CTV' in str(d[1]):
#                 string = d[1].strip()
#                 kabelCount += 1
#                 total_price_kabel += price

#                 kod_ = re.search(r'993(\d{3})', string)
#                 if kod_:
#                     code = kod_.group(1)
#                     user_etrap = getEtrapNameFromCode(code)
#                     number_ = re.search(rf'{code}(\d+)', string)
#                     if number_:
#                         number = number_.group(1)
#                         # try:
#                         #     user_pk = code_number_pk[f"{code}{number}"]
#                         # except:
#                         #     errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа или номер в договоре некорректный"])
#                         #     continue

#                         try:
#                             user = KabelTvNew.objects.get(number=number)
#                         except:
#                             errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Не найден по PK в KabelTVNew"])
#                             continue

#                         # try:
#                         #     user = UserTable.objects.get(pk=user_pk)
#                         # except:
#                         #     errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Не найден по PK в UserTable"])
#                         #     continue
#                     else:
#                         errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Номер в договоре некорректный"])
#                         continue
#                 else:
#                     errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа в договоре некорректный"])
#                     continue

#                 type_ = 'Kabel'
#                 kod_oplaty = d[12] if d[12] != None else ''
#                 obj = PlatejiWhichAddKassirsEveryDay(
#                     number=user.number, 
#                     user_etrap='Dashoguz', 
#                     kassir_etrap=managarNames[manager],
#                     type_pay=type_,
#                     pay_category=d[8].strip(),
#                     manager=manager,
#                     date=d[5],
#                     kodOplaty=kod_oplaty,
#                     dogowor=str(d[1]),
#                     name=d[0],
#                     is_enterprises='ФЛ',
#                     price=price,
#                     file_name=str(xlsx_data),
#                     who_add_file=request.user.username
#                     )
#                 bulk_create.append(obj)

#                 count += 1
#                 continue
#                 # print(user_etrap, code, number, user_pk, type_)
            
#             # абонплата
#             elif isinstance(d[1], int):
#                 dogowor=d[1]
#                 abonplataCount += 1
#                 total_price_abonplata += price
#                 number = str(dogowor)[-5:]
#                 code = str(dogowor)[-8:-5]
#                 user_etrap = getEtrapNameFromCode(code)
#                 if user_etrap:
#                     try:
#                         user_pk = code_number_pk[f"{code}{number}"]
#                     except:
#                         errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа или номер в договоре некорректный"])
#                         continue
#                     try:
#                         user = UserTable.objects.get(pk=user_pk)
#                     except:
#                         errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Не найден по PK"])
#                         continue
#                 else:
#                     errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа или номер в договоре некорректный"])
#                     continue

#                 type_ = 'Abonplata'
            
#             else:
#                 dogowor = d[1].lower().strip()
#                 if 'ikdz' in dogowor:
#                     continue
#                 # alem
#                 if 'iptv' in dogowor:
#                     iptvCount += 1
#                     total_price_iptv += price
#                     number = ''.join(filter(str.isdigit, dogowor))[-5:]
#                     code = ''.join(filter(str.isdigit, dogowor))[-8:-5]
#                     user_etrap = getEtrapNameFromCode(code)
#                     if user_etrap:
#                         try:
#                             user_pk = code_number_pk[f"{code}{number}"]
#                         except:
#                             errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа или номер в договоре некорректный"])
#                             continue
#                         user = UserTable.objects.get(pk=user_pk)
#                     else:
#                         errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа или номер в договоре некорректный"])
#                         continue
#                     type_='Alem'
#                 # internet
#                 elif 'dza' in dogowor or 'dad' in dogowor or 'dbs' in dogowor or 'dgd' in dogowor or 'dge' in dogowor or 'dgo' in dogowor or 'dku' in dogowor or 'dnz' in dogowor or 'drb' in dogowor or 'dtb' in dogowor:
#                     intCount += 1
#                     total_price_internet += price
#                     try:
#                         user = UserTable.objects.get(pk=dogowor_pk[dogowor][0])
#                     except:
#                         try:
#                             old_user = OldLoginDogowor.objects.get(dogowor=dogowor.upper())
#                             user = UserTable.objects.get(etrap=old_user.etrap, number=old_user.number)
#                         except:
#                             errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Договор не найден в базе"]) 
#                             continue
#                     type_='Internet'
#                 # abonplata
#                 elif 'old' in dogowor:
#                     dogowor = dogowor.replace('old', '')
#                     if '-' in dogowor:
#                         dogowor = dogowor.replace('-', '')
#                     if '_' in dogowor:
#                         dogowor = dogowor.replace('_', '')
#                     # проверка есть ли другие символы кроме цифр в договоре
#                     if any(char.isdigit() for char in dogowor):
#                         # Содержит только цифры
#                         abonplataCount += 1
#                         total_price_abonplata += price
#                         number = str(dogowor)[-5:]
#                         code = str(dogowor)[-8:-5]
#                         user_etrap = getEtrapNameFromCode(code)
#                         if user_etrap:
#                             try:
#                                 user_pk = code_number_pk[f"{code}{number}"]
#                             except:
#                                 errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа или номер в договоре некорректный"])
#                                 continue
#                             user = UserTable.objects.get(pk=user_pk)
#                         else:
#                             errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Код этрапа или номер в договоре некорректный"])
#                             continue
#                     else:
#                         errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Непонятный договор"])
#                         continue
#                     type_='Abonplata'
#                 else:
#                     errorList.append([d[0], d[1], d[3], d[4], d[5], d[8], f"Непонятный договор"])
#                     continue
    
#             # 2 = wnPlateji, Default, Картой,       3=Manager,       4=Признак скорректированного платежа,     6=data plateja,    9= №п/п,   10=Код оплаты,   11=dogowor,  12=Ф.И.О,   13=ФЛ ЮЛ,  14=price
#             # 0=Пользователь	1=Договор	2=Номер платежа	3=Сумма	4=Менеджер	5=Дата платежа	6=Платёж проведен	7=Номер счёта	8=Категория	9=Платёжное поручение	10=Комментарий	11=Оператор	12=Код оплаты
#             kod_oplaty = d[12] if d[12] != None else ''
#             obj = PlatejiWhichAddKassirsEveryDay(
#                 number=user.number, 
#                 user_etrap=user.etrap, 
#                 kassir_etrap=managarNames[manager],
#                 type_pay=type_,
#                 pay_category=d[8].strip(),
#                 manager=manager,
#                 date=d[5],
#                 kodOplaty=kod_oplaty,
#                 dogowor=str(d[1]),
#                 name=d[0],
#                 is_enterprises='ФЛ',
#                 price=price,
#                 file_name=str(xlsx_data),
#                 who_add_file=request.user.username
#                 )
#             bulk_create.append(obj)

#             count += 1

        
#         if request.POST.get('platejiTest'):
#             logger.info(f'==== Проверено ==== {count}')
#         else:
#             logger.info(f'==== Добавлено ==== {count}')
#         if errorList:
#             messages.error(request, f"Ошибка")
#             context['errorList'] = errorList
#             context['xlsx_data'] = str(xlsx_data)
#             return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/errorBillingPlatejiFromKassa.html', context)
        
#         if errorManager:
#             messages.error(request, f"Ошибка! есть новые менеджеры, надо определить их тип")
#             context['errorManager'] = errorManager
#             return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)
        
#         if have_date == False and have_name == False:
#             messages.error(request, f'!Ошибка, в ФИО менеджера и дате платежей: {str(xlsx_data)}')
#             return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)
#         if have_name == False:
#             messages.error(request, f'!Ошибка, в ФИО менеджера:  {str(xlsx_data)}')
#             return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)

#         totalCount = abonplataCount + iptvCount + intCount + kabelCount
#         totalPice = float('%.2f' % (total_price_abonplata + total_price_iptv + total_price_internet + total_price_kabel))
#         context['abonplataCount'] = f"{abonplataCount:_}"
#         context['total_price_abonplata'] = f"{float('%.2f' % (total_price_abonplata)):_}"
#         context['iptvCount'] = f"{iptvCount:_}"
#         context['total_price_iptv'] = f"{float('%.2f' % (total_price_iptv)):_}"
#         context['intCount'] = f"{intCount:_}"
#         context['total_price_internet'] = f"{float('%.2f' % (total_price_internet)):_}"

#         context['kabelCount'] = f"{kabelCount:_}"
#         context['total_price_kabel'] = f"{float('%.2f' % (total_price_kabel)):_}"

#         context['totalCount'] = f"{totalCount:_}"
#         context['totalPice'] = f"{totalPice:_}"

#         if already_nach:
#             messages.error(request, f'Этот файл "{str(xlsx_data)}" уже был добавлен в базу платежей')
#             return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)

#         if request.POST.get('platejiTest'):
#             # Проверка
#             if date_convertered_to_price:
#                 messages.error(request, f"Есть Ошибки! дата вместо цены")
#                 context['errorList'] = date_convertered_to_price
#                 context['xlsx_data'] = str(xlsx_data)
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/errorBillingPlatejiFromKassa.html', context)
#             messages.success(request, f"Проверка прошла успешно")
#         else:
#             # Добавить
#             try:
#                 with transaction.atomic():
#                     if bulk_create:
#                         PlatejiWhichAddKassirsEveryDay.objects.bulk_create(bulk_create)
#                     StaffAction.objects.create(user=request.user, comment=f'Добавления платежей в Базу Данных, файл {str(xlsx_data)}, дата добавления {datetime.now()}, добавил {request.user.username}', action='Добавления платежей в базу')
#                     SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.create(
#                         file_name=str(xlsx_data),
#                         etrap_add=request_user_etrap,
#                         who_add=request.user.username,
#                         when_add=datetime.now()
#                     )
#                     KassaExcelFiles.objects.create(operator=request.user, document=xlsx_data)
#                     messages.success(request, f"Успешно добавлено в БД")
#             except Exception as e:
#                 messages.error(request, f'ошибка с transaction при сохранении, тип ошибки == {e}')
#                 logger.error(f'ошибка с transaction при сохранении, тип ошибки == {e}')






#     return render(request, 'telekom/Kassa/addPlatejiForKassirs2.html', context)