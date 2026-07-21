from django.shortcuts import render, redirect
from django.contrib import messages

from datetime import date, datetime, timedelta
from telekom.models import ManagerNames, OldLoginDogowor, PayHistory, PlatejiWhichAddKassirsEveryDay, StaffAction, UserTable, SaveInfoAboutWhoAddAndNachPaysFromBilling
from tablib import Dataset

from telekom.views2.myFunc.myFunc import getEtrapNameFromCode, monthСonvert

from django.db import transaction

import logging

logger = logging.getLogger(__name__)


def add_month_pays_from_billing_to_my_programm(request):
    # wn_p = ['Dostluk Bank', 'E-government', 'Saray Tolegy', 'Tolleg APP TMCELL', 'Turkmen Pochta', 'TM POST Dealers']
    # PlatejiWhichAddKassirsEveryDay.objects.all().delete()
    # testPays = PayHistory.objects.filter(date__range=[f"2024-02-01 00:00:00", f"2024-03-01 23:59:59"], kabel=0)
    # testPays = PayHistory.objects.filter(date__range=[f"2024-02-01 00:00:00", f"2024-03-01 23:59:59"], kabel__gt=0).update(internet=0, alem=0, prochee=0, slr=0, telefon=0, kod=0, zakaz=0, dop_uslugi=0)
    # print(len(testPays))
    context = {}
    test_pays = PayHistory.objects.filter(date__range=[f"2024-02-01 00:00:00", f"2024-03-01 23:59:59"], abonent__etrap='Turkmenbashy')
    
    test_total_price_alem = 0
    test_total_price_int = 0
    test_total_price_abon = 0
    for p in test_pays:
        test_total_price_alem += p.alem
        test_total_price_int += p.internet
        test_total_price_abon += p.prochee
    # print('test_total_price_alem', test_total_price_alem)
    # print('test_total_price_int', test_total_price_int)
    # print('test_total_price_abon', test_total_price_abon)

    test_pays2 = PlatejiWhichAddKassirsEveryDay.objects.filter(file_name='plateji_Turkmenbashy_2024_02.xlsx')
    test_total_price_alem2 = 0
    test_total_price_int2 = 0
    test_total_price_abon2 = 0
    for p in test_pays2:
        if p.type_pay == 'Abonplata':
            test_total_price_abon2 += p.price
        elif p.type_pay == 'Alem':
            test_total_price_alem2 += p.price
        elif p.type_pay == 'Internet':
            test_total_price_int2 += p.price      
    # print('test_total_price_alem2', test_total_price_alem2)
    # print('test_total_price_int2', test_total_price_int2)
    # print('test_total_price_abon2', test_total_price_abon2)

    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.username == 'Gayyp':
            log = 'Dashoguz'
            context['matbIndex'] = True
            context['add_month_pays_from_billing_to_my_programm'] = True
        else:
            messages.error(request, f'Доступ разрешен только администратору')
            return redirect('user-login')
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')
    
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

    current_date = str(date.today())
    context['current_date'] = current_date
    current_year = current_date[0:4]
    current_month = current_date[5:7]

    month = request.GET.get('month')
    year = request.GET.get('year')

    context['month'] = month
    context['year'] = year
    context['month_digit'] = monthСonvert(month)
    
    if year and month:
        chossed_day = datetime(int(year), int(monthСonvert(month)), 1)
        next_date = chossed_day + timedelta(days=1)
        next_year = str(next_date.date())[0:4]
        next_month = str(next_date.date())[5:7]
        # pays = PayHistory.objects.filter(date__range=[f"{year}-{str(monthСonvert(month))}-01", f"{next_year}-{next_month}-01"])

    if request.method == 'POST' and 'platejiSKassy' in request.POST:
        logger.info(f'==== Подготовка файлов ...')
        # print()
        # print(f"Подготовка файлов ...")
        # print()
        dataset = Dataset()
        try:
            xlsx_data = request.FILES['my_file2']
        except:
            messages.error(request, f'Выберите Файл')
            return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)
   
        try:
            imported_data = dataset.load(xlsx_data.read(), format='xlsx')
        except:
            messages.error(request, f'Файл должен быть формата xlsx')
            return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)

        
        if monthСonvert(month) not in str(xlsx_data).lower():
            messages.error(request, f'В названии файла должен быть год и месяц Например "plateji_02_2024"')
            return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)
        
        if year not in str(xlsx_data):
            messages.error(request, f'В названии файла должен быть год и месяц Например "plateji_02_2024"')
            return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)
        
        already_nach = False
        print('str(xlsx_data)', str(xlsx_data))
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

        
 

        managarNames = {}
        for i in ManagerNames.objects.all():
            managarNames[i.name] = i.etrap

        iptvCount = 0
        tvCount = 0
        intCount = 0
        abonplataCount = 0
        total_price_iptv = 0
        total_price_tv = 0
        total_price_internet = 0
        total_price_abonplata = 0
        errorList = []
        date_convertered_to_price = []
        bulk_create = []
        errorManager = []

        total_count = 0
        umumy_total = 0

        total_off_already_payed = 0
        total_off_not_payed = 0
        # 2 = wnPlateji, Default, Картой,       3=Manager,       4=Признак скорректированного платежа,     6=data plateja,    9= №п/п,   10=Код оплаты,   11=dogowor,  12=Ф.И.О,   13=ФЛ ЮЛ,  14=price
        # test_total = 0
        test_total_plateji_kotorye_ne_dobawilis = 0
        for d in imported_data:

            fl = d[13]

            if 'ФЛ' == fl or 'ЮЛ' == fl:
      
                

                # Проверка есть ли этот менеджер в ManagerNames или в ExternalPayments
                manager = d[3].strip()

                # if manager == 'Soýunowa Aknur':
                #     continue
                if manager in ['Derýagulyýewa Jeren', 'Администратор', 'С.Сазаков']:
                    continue
                
                if manager not in managarNames and manager not in errorManager:
                    errorManager.append(manager)
                    try:
                        with transaction.atomic():
                            ManagerNames.objects.create(name=manager)
                    except Exception as e:
                        messages.error(request, f'(откат сохранений) ошибка с transaction при сохранении нового менеджера в ManagerNames, тип ошибки == {e}')
                        logger.error(f'==== (откат сохранений) ошибка с transaction при сохранении нового менеджера в ManagerNames, тип ошибки == {e}')
                        return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)
                    managarNames[manager] = None
                    continue
                elif managarNames[manager] == '' or managarNames[manager] == None:
                    if manager not in errorManager:
                        errorManager.append(manager)
                        continue
                    
                if managarNames[manager] in etraps:
                    continue

                
                total_count += 1
                # конверт дату в цену
                if isinstance(d[14], date):
                    price_date = str(d[14])
                    if price_date[8:10] == '01':
                        manat = int(price_date[5:7])
                        coin = int(price_date[2:4])
                        price = float(f"{str(manat)}.{str(coin)}")
                    else:
                        manat = int(price_date[8:10])
                        coin = int(price_date[5:7])
                        price = float(f"{str(manat)}.{str(coin)}")
                    date_convertered_to_price.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Вместо даты будет цена {str(price)} Если вы не согласны с ценами рекомендую прописать их вручную в excel файле, а если согласны с ценами, то можно добавлять, но под вашу ответственность"])
                else:
                    price = float(d[14])

                # абонплата
                if isinstance(d[11], int):
                    dogowor=d[11]
                    
                    number = str(dogowor)[-5:]
                    code = str(dogowor)[-8:-5]
                    user_etrap = getEtrapNameFromCode(code)
                    if user_etrap:
                        if 'off' in str(xlsx_data).lower():
                            try:
                                user_pk = code_number_pk[f"{code}{number}"]
                            except:
                                errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
                                continue
                            try:
                                user = UserTable.objects.get(pk=user_pk)
                            except:
                                errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Не найден по PK"])
                                continue

                            pay_off = PayHistory.objects.filter(abonent=user, prochee=price, date=d[6], kassir=d[3].strip())
                            if len(pay_off) > 0:
                                total_off_already_payed += 1
                                continue
                            else:
                                test_total_plateji_kotorye_ne_dobawilis += price
                                print(d[6], d[3], d[10], d[11], d[12], d[14])
                                type_ = 'Abonplata'
                                abonplataCount += 1
                                total_price_abonplata += price
                                umumy_total += price
                                total_off_not_payed += 1  

                        else:

                            try:
                                user_pk = code_number_pk[f"{code}{number}"]
                            except:
                                errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
                                continue
                            try:
                                user = UserTable.objects.get(pk=user_pk)
                            except:
                                errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Не найден по PK"])
                                continue
                            type_ = 'Abonplata'
                            abonplataCount += 1
                            total_price_abonplata += price
                            umumy_total += price
                    else:
                        errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
                        continue

                    # type_ = 'Abonplata'
                    
                else:
                    dogowor = d[11].lower().strip()
                    if 'ikdz' in dogowor:
                        continue
                    # alem
                    if 'iptv' in dogowor:
                        number = ''.join(filter(str.isdigit, dogowor))[-5:]
                        code = ''.join(filter(str.isdigit, dogowor))[-8:-5]
                        user_etrap = getEtrapNameFromCode(code)
                        if user_etrap:
                            if 'off' in str(xlsx_data).lower():
                                try:
                                    user_pk = code_number_pk[f"{code}{number}"]
                                except:
                                    errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
                                    continue
                                user = UserTable.objects.get(pk=user_pk)

                                pay_off = PayHistory.objects.filter(abonent=user, alem=price, date=d[6], kassir=d[3].strip())
                                if len(pay_off) > 0:
                                    total_off_already_payed += 1
                                    continue
                                else:
                                    test_total_plateji_kotorye_ne_dobawilis += price
                                    type_='Alem'
                                    iptvCount += 1
                                    total_price_iptv += price
                                    umumy_total += price
                                    total_off_not_payed += 1
                            else:
                                
                                try:
                                    user_pk = code_number_pk[f"{code}{number}"]
                                except:
                                    errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
                                    continue
                                user = UserTable.objects.get(pk=user_pk)
                                iptvCount += 1
                                total_price_iptv += price
                                umumy_total += price
                                type_='Alem'
                        else:
                            errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
                            continue
                        
                    # internet
                    elif 'dza' in dogowor or 'dad' in dogowor or 'dbs' in dogowor or 'dgd' in dogowor or 'dge' in dogowor or 'dgo' in dogowor or 'dku' in dogowor or 'dnz' in dogowor or 'drb' in dogowor or 'dtb' in dogowor:
                        
                        # Если начисляем off то многие платежи поторяются надо проверить не было ли точно такого платежа на активном чтобы небыло двойного начисления
                        if 'off' in str(xlsx_data).lower():
                            try:
                                user = UserTable.objects.get(pk=dogowor_pk[dogowor][0])
                            except:
                                try:
                                    old_user = OldLoginDogowor.objects.get(dogowor=dogowor.upper())
                                    user = UserTable.objects.get(etrap=old_user.etrap, number=old_user.number)
                                except:
                                    errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Договор не найден в базе"]) 
                                    continue
                            pay_off = PayHistory.objects.filter(abonent=user, internet=price, date=d[6], kassir=d[3].strip())
                            if len(pay_off) > 0:
                                total_off_already_payed += 1
                                continue
                            else:
                                test_total_plateji_kotorye_ne_dobawilis += price
                                type_='Internet'
                                intCount += 1
                                total_price_internet += price
                                umumy_total += price
                                total_off_not_payed += 1  

                        # если файл не off
                        else:
                            intCount += 1
                            total_price_internet += price
                            umumy_total += price
                            try:
                                user = UserTable.objects.get(pk=dogowor_pk[dogowor][0])
                            except:
                                try:
                                    old_user = OldLoginDogowor.objects.get(dogowor=dogowor.upper())
                                    user = UserTable.objects.get(etrap=old_user.etrap, number=old_user.number)
                                except:
                                    errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Договор не найден в базе"]) 
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
                            
                            number = str(dogowor)[-5:]
                            code = str(dogowor)[-8:-5]
                            user_etrap = getEtrapNameFromCode(code)
                            if user_etrap:
                                if 'off' in str(xlsx_data).lower():
                                    try:
                                        user_pk = code_number_pk[f"{code}{number}"]
                                    except:
                                        errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
                                        continue
                                    user = UserTable.objects.get(pk=user_pk)
                                    pay_off = PayHistory.objects.filter(abonent=user, prochee=price, date=d[6], kassir=d[3].strip())
                                    if len(pay_off) > 0:
                                        total_off_already_payed += 1
                                        continue
                                    else:
                                        test_total_plateji_kotorye_ne_dobawilis += price
                                        # print(user.number, )
                                        print(d[6], d[3], d[10], d[11], d[12], d[14])
                                        type_ = 'Abonplata'
                                        abonplataCount += 1
                                        total_price_abonplata += price
                                        umumy_total += price
                                else:
                                    try:
                                        user_pk = code_number_pk[f"{code}{number}"]
                                    except:
                                        errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
                                        continue
                                    user = UserTable.objects.get(pk=user_pk)
                                    type_='Abonplata'
                                    abonplataCount += 1
                                    total_price_abonplata += price
                                    umumy_total += price
                            else:
                                errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
                                continue
                        else:
                            errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Непонятный договор"])
                            continue
                        

                    elif 'ctv' in dogowor:
                        tvCount += 1
                        total_price_tv += price
                        umumy_total += price
                        if len(dogowor) == 15:
                            # print(len(dogowor))
                            number = ''.join(filter(str.isdigit, dogowor))[-5:]
                            code = ''.join(filter(str.isdigit, dogowor))[-9:-6]
                            # print(number, code)
                        elif len(dogowor) == 16:
                            # print(len(dogowor))
                            number = ''.join(filter(str.isdigit, dogowor))[-6:]
                            code = ''.join(filter(str.isdigit, dogowor))[-10:-7]
                            # print(number, code)
                        else:
                            errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Непонятный договор"])
                    else:
                        errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Непонятный договор"])
                        continue
     
                kod_oplaty = d[10] if d[10] != None else ''
                # test_total += price
                obj = PlatejiWhichAddKassirsEveryDay(
                    number=user.number, 
                    user_etrap=user.etrap, 
                    kassir_etrap=managarNames[manager],
                    type_pay=type_,
                    pay_category=d[2].strip(),
                    manager=manager,
                    date=d[6],
                    kodOplaty=kod_oplaty,
                    dogowor=str(d[11]),
                    name=d[12],
                    is_enterprises=d[13],
                    price=price,
                    file_name=str(xlsx_data),
                    who_add_file=request.user.username
                    )
                bulk_create.append(obj)

                count += 1
                # if count % 1000 == 0:
                #     if request.POST.get('platejiTest'):
                #         print(f"Проверено {count}")
                #     else:
                #         print(f"Добавлено {count}")
                        
                # elif count == len(imported_data):
                #     if request.POST.get('platejiTest'):
                #         print(f"Проверено {count}")
                #     else:
                #         print(f"Добавлено {count}")

        
        if request.POST.get('platejiTest'):
            logger.info(f'==== Проверено {count}')
            # print(f"Проверено {count}")
        else:
            logger.info(f'==== Добавлено {count}')
            # print(f"Добавлено {count}")
        if errorList:
            messages.error(request, f"Ошибка")
            context['errorList'] = errorList
            context['xlsx_data'] = str(xlsx_data)
            return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/errorBillingPlatejiFromKassa.html', context)
        
        if errorManager:
            messages.error(request, f"Ошибка! есть новые менеджеры, надо определить их тип")
            context['errorManager'] = errorManager
            return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)

        totalCount = abonplataCount + iptvCount + intCount
        totalPice = float('%.2f' % (total_price_abonplata + total_price_iptv + total_price_internet))
        context['abonplataCount'] = f"{abonplataCount:_}"
        context['total_price_abonplata'] = f"{float('%.2f' % (total_price_abonplata)):_}"
        context['iptvCount'] = f"{iptvCount:_}"
        context['total_price_iptv'] = f"{float('%.2f' % (total_price_iptv)):_}"
        context['intCount'] = f"{intCount:_}"
        context['total_price_internet'] = f"{float('%.2f' % (total_price_internet)):_}"
        context['totalCount'] = f"{totalCount:_}"
        context['totalPice'] = f"{totalPice:_}"

        if already_nach:
            messages.error(request, f'Этот файл "{str(xlsx_data)}" уже был добавлен в в базу платежей')
            return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)

        if request.POST.get('platejiTest'):
            # Проверка
            if date_convertered_to_price:
                messages.error(request, f"Есть Ошибки! дата вместо цены")
                context['errorList'] = date_convertered_to_price
                context['xlsx_data'] = str(xlsx_data)
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/errorBillingPlatejiFromKassa.html', context)
            messages.success(request, f"Проверка прошла успешно")
            # print('test_total', test_total)
        else:
            # Добавить
            try:
                with transaction.atomic():
                    if bulk_create:
                        PlatejiWhichAddKassirsEveryDay.objects.bulk_create(bulk_create)
                    StaffAction.objects.create(user=request.user, comment=f'Добавления платежей в Базу Данных, файл {str(xlsx_data)}, дата добавления {datetime.now()}, добавил {request.user.username}', action='Добавления платежей в базу')
                    SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.create(
                        file_name=str(xlsx_data),
                        etrap_add=log,
                        who_add=request.user.username,
                        when_add=datetime.now()
                    )
                    messages.success(request, f"Успешно добавлено в БД")
            except Exception as e:
                messages.error(request, f'(откат сохранений) ошибка с transaction при сохранении, тип ошибки == {e}')
                logger.error(f'(откат сохранений) ошибка с transaction при сохранении, тип ошибки == {e}')
        print('test_total_plateji_kotorye_ne_dobawilis', test_total_plateji_kotorye_ne_dobawilis)


    return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)

# Rabotaet prawilno no bez razdelennyh etrapow
# from django.shortcuts import render, redirect
# from django.contrib import messages

# from datetime import date, datetime, timedelta
# from telekom.models import ManagerNames, OldLoginDogowor, PayHistory, PlatejiWhichAddKassirsEveryDay, StaffAction, UserTable, SaveInfoAboutWhoAddAndNachPaysFromBilling
# from tablib import Dataset

# from telekom.views2.myFunc.myFunc import getEtrapNameFromCode, monthСonvert

# from django.db import transaction

# import logging

# logger = logging.getLogger(__name__)


# def add_month_pays_from_billing_to_my_programm(request):
#     # wn_p = ['Dostluk Bank', 'E-government', 'Saray Tolegy', 'Tolleg APP TMCELL', 'Turkmen Pochta', 'TM POST Dealers']
#     # PlatejiWhichAddKassirsEveryDay.objects.all().delete()
#     # testPays = PayHistory.objects.filter(date__range=[f"2024-02-01 00:00:00", f"2024-03-01 23:59:59"], kabel=0)
#     # testPays = PayHistory.objects.filter(date__range=[f"2024-02-01 00:00:00", f"2024-03-01 23:59:59"], kabel__gt=0).update(internet=0, alem=0, prochee=0, slr=0, telefon=0, kod=0, zakaz=0, dop_uslugi=0)
#     # print(len(testPays))
#     context = {}
#     test_pays = PayHistory.objects.filter(date__range=[f"2024-02-01 00:00:00", f"2024-03-01 23:59:59"], abonent__etrap='Turkmenbashy')
    
#     test_total_price_alem = 0
#     test_total_price_int = 0
#     test_total_price_abon = 0
#     for p in test_pays:
#         test_total_price_alem += p.alem
#         test_total_price_int += p.internet
#         test_total_price_abon += p.prochee
#     # print('test_total_price_alem', test_total_price_alem)
#     # print('test_total_price_int', test_total_price_int)
#     # print('test_total_price_abon', test_total_price_abon)

#     test_pays2 = PlatejiWhichAddKassirsEveryDay.objects.filter(file_name='plateji_Turkmenbashy_2024_02.xlsx')
#     test_total_price_alem2 = 0
#     test_total_price_int2 = 0
#     test_total_price_abon2 = 0
#     for p in test_pays2:
#         if p.type_pay == 'Abonplata':
#             test_total_price_abon2 += p.price
#         elif p.type_pay == 'Alem':
#             test_total_price_alem2 += p.price
#         elif p.type_pay == 'Internet':
#             test_total_price_int2 += p.price      
#     # print('test_total_price_alem2', test_total_price_alem2)
#     # print('test_total_price_int2', test_total_price_int2)
#     # print('test_total_price_abon2', test_total_price_abon2)

#     if request.user.is_authenticated:
#         if request.user.is_superuser or request.user.username == 'Gayyp':
#             log = 'Dashoguz'
#             context['matbIndex'] = True
#             context['add_month_pays_from_billing_to_my_programm'] = True
#         else:
#             messages.error(request, f'Доступ разрешен только администратору')
#             return redirect('user-login')
#     else:
#         messages.error(request, f'Вы не аутентифицированы')
#         return redirect('user-login')
    
#     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
#     context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
#     context['years'] = ['2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

#     current_date = str(date.today())
#     context['current_date'] = current_date
#     current_year = current_date[0:4]
#     current_month = current_date[5:7]

#     month = request.GET.get('month')
#     year = request.GET.get('year')

#     context['month'] = month
#     context['year'] = year
#     context['month_digit'] = monthСonvert(month)
    
#     if year and month:
#         chossed_day = datetime(int(year), int(monthСonvert(month)), 1)
#         next_date = chossed_day + timedelta(days=1)
#         next_year = str(next_date.date())[0:4]
#         next_month = str(next_date.date())[5:7]
#         # pays = PayHistory.objects.filter(date__range=[f"{year}-{str(monthСonvert(month))}-01", f"{next_year}-{next_month}-01"])

#     if request.method == 'POST' and 'platejiSKassy' in request.POST:
#         logger.info(f'==== Подготовка файлов ...')
#         # print()
#         # print(f"Подготовка файлов ...")
#         # print()
#         dataset = Dataset()
#         try:
#             xlsx_data = request.FILES['my_file2']
#         except:
#             messages.error(request, f'Выберите Файл')
#             return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)
   
#         try:
#             imported_data = dataset.load(xlsx_data.read(), format='xlsx')
#         except:
#             messages.error(request, f'Файл должен быть формата xlsx')
#             return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)

        
#         if monthСonvert(month) not in str(xlsx_data).lower():
#             messages.error(request, f'В названии файла должен быть год и месяц Например "plateji_02_2024"')
#             return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)
        
#         if year not in str(xlsx_data):
#             messages.error(request, f'В названии файла должен быть год и месяц Например "plateji_02_2024"')
#             return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)
        
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

        
 

#         managarNames = {}
#         for i in ManagerNames.objects.all():
#             managarNames[i.name] = i.etrap

#         iptvCount = 0
#         tvCount = 0
#         intCount = 0
#         abonplataCount = 0
#         total_price_iptv = 0
#         total_price_tv = 0
#         total_price_internet = 0
#         total_price_abonplata = 0
#         errorList = []
#         date_convertered_to_price = []
#         bulk_create = []
#         errorManager = []

#         total_count = 0
#         umumy_total = 0

#         total_off_already_payed = 0
#         total_off_not_payed = 0
#         # 2 = wnPlateji, Default, Картой,       3=Manager,       4=Признак скорректированного платежа,     6=data plateja,    9= №п/п,   10=Код оплаты,   11=dogowor,  12=Ф.И.О,   13=ФЛ ЮЛ,  14=price
#         # test_total = 0
#         for d in imported_data:

#             fl = d[13]

#             if 'ФЛ' == fl or 'ЮЛ' == fl:
      
                

#                 # Проверка есть ли этот менеджер в ManagerNames или в ExternalPayments
#                 manager = d[3].strip()

#                 # if manager == 'Soýunowa Aknur':
#                 #     continue
#                 if manager in ['Derýagulyýewa Jeren', 'Администратор', 'С.Сазаков']:
#                     continue
                
#                 if manager not in managarNames and manager not in errorManager:
#                     errorManager.append(manager)
#                     try:
#                         with transaction.atomic():
#                             ManagerNames.objects.create(name=manager)
#                     except Exception as e:
#                         messages.error(request, f'(откат сохранений) ошибка с transaction при сохранении нового менеджера в ManagerNames, тип ошибки == {e}')
#                         logger.error(f'==== (откат сохранений) ошибка с transaction при сохранении нового менеджера в ManagerNames, тип ошибки == {e}')
#                         return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)
#                     managarNames[manager] = None
#                     continue
#                 elif managarNames[manager] == '' or managarNames[manager] == None:
#                     if manager not in errorManager:
#                         errorManager.append(manager)
#                         continue
                    
#                 if managarNames[manager] in etraps:
#                     continue

                
#                 total_count += 1
#                 # конверт дату в цену
#                 if isinstance(d[14], date):
#                     price_date = str(d[14])
#                     if price_date[8:10] == '01':
#                         manat = int(price_date[5:7])
#                         coin = int(price_date[2:4])
#                         price = float(f"{str(manat)}.{str(coin)}")
#                     else:
#                         manat = int(price_date[8:10])
#                         coin = int(price_date[5:7])
#                         price = float(f"{str(manat)}.{str(coin)}")
#                     date_convertered_to_price.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Вместо даты будет цена {str(price)} Если вы не согласны с ценами рекомендую прописать их вручную в excel файле, а если согласны с ценами, то можно добавлять, но под вашу ответственность"])
#                 else:
#                     price = float(d[14])

#                 # абонплата
#                 if isinstance(d[11], int):
#                     dogowor=d[11]
                    
#                     number = str(dogowor)[-5:]
#                     code = str(dogowor)[-8:-5]
#                     user_etrap = getEtrapNameFromCode(code)
#                     if user_etrap:
#                         if 'off' in str(xlsx_data).lower():
#                             try:
#                                 user_pk = code_number_pk[f"{code}{number}"]
#                             except:
#                                 errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
#                                 continue
#                             try:
#                                 user = UserTable.objects.get(pk=user_pk)
#                             except:
#                                 errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Не найден по PK"])
#                                 continue

#                             pay_off = PayHistory.objects.filter(abonent=user, prochee=price, date=d[6], kassir=d[3].strip())
#                             if len(pay_off) > 0:
#                                 total_off_already_payed += 1
#                                 continue
#                             else:
#                                 type_ = 'Abonplata'
#                                 abonplataCount += 1
#                                 total_price_abonplata += price
#                                 umumy_total += price
#                                 total_off_not_payed += 1  

#                         else:

#                             try:
#                                 user_pk = code_number_pk[f"{code}{number}"]
#                             except:
#                                 errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
#                                 continue
#                             try:
#                                 user = UserTable.objects.get(pk=user_pk)
#                             except:
#                                 errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Не найден по PK"])
#                                 continue
#                             type_ = 'Abonplata'
#                             abonplataCount += 1
#                             total_price_abonplata += price
#                             umumy_total += price
#                     else:
#                         errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
#                         continue

#                     # type_ = 'Abonplata'
                    
#                 else:
#                     dogowor = d[11].lower().strip()
#                     if 'ikdz' in dogowor:
#                         continue
#                     # alem
#                     if 'iptv' in dogowor:
#                         number = ''.join(filter(str.isdigit, dogowor))[-5:]
#                         code = ''.join(filter(str.isdigit, dogowor))[-8:-5]
#                         user_etrap = getEtrapNameFromCode(code)
#                         if user_etrap:
#                             if 'off' in str(xlsx_data).lower():
#                                 try:
#                                     user_pk = code_number_pk[f"{code}{number}"]
#                                 except:
#                                     errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
#                                     continue
#                                 user = UserTable.objects.get(pk=user_pk)

#                                 pay_off = PayHistory.objects.filter(abonent=user, alem=price, date=d[6], kassir=d[3].strip())
#                                 if len(pay_off) > 0:
#                                     total_off_already_payed += 1
#                                     continue
#                                 else:
#                                     type_='Alem'
#                                     iptvCount += 1
#                                     total_price_iptv += price
#                                     umumy_total += price
#                                     total_off_not_payed += 1
#                             else:
                                
#                                 try:
#                                     user_pk = code_number_pk[f"{code}{number}"]
#                                 except:
#                                     errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
#                                     continue
#                                 user = UserTable.objects.get(pk=user_pk)
#                                 iptvCount += 1
#                                 total_price_iptv += price
#                                 umumy_total += price
#                                 type_='Alem'
#                         else:
#                             errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
#                             continue
                        
#                     # internet
#                     elif 'dza' in dogowor or 'dad' in dogowor or 'dbs' in dogowor or 'dgd' in dogowor or 'dge' in dogowor or 'dgo' in dogowor or 'dku' in dogowor or 'dnz' in dogowor or 'drb' in dogowor or 'dtb' in dogowor:
                        
#                         # Если начисляем off то многие платежи поторяются надо проверить не было ли точно такого платежа на активном чтобы небыло двойного начисления
#                         if 'off' in str(xlsx_data).lower():
#                             try:
#                                 user = UserTable.objects.get(pk=dogowor_pk[dogowor][0])
#                             except:
#                                 try:
#                                     old_user = OldLoginDogowor.objects.get(dogowor=dogowor.upper())
#                                     user = UserTable.objects.get(etrap=old_user.etrap, number=old_user.number)
#                                 except:
#                                     errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Договор не найден в базе"]) 
#                                     continue
#                             pay_off = PayHistory.objects.filter(abonent=user, internet=price, date=d[6], kassir=d[3].strip())
#                             if len(pay_off) > 0:
#                                 total_off_already_payed += 1
#                                 continue
#                             else:
#                                 type_='Internet'
#                                 intCount += 1
#                                 total_price_internet += price
#                                 umumy_total += price
#                                 total_off_not_payed += 1  

#                         # если файл не off
#                         else:
#                             intCount += 1
#                             total_price_internet += price
#                             umumy_total += price
#                             try:
#                                 user = UserTable.objects.get(pk=dogowor_pk[dogowor][0])
#                             except:
#                                 try:
#                                     old_user = OldLoginDogowor.objects.get(dogowor=dogowor.upper())
#                                     user = UserTable.objects.get(etrap=old_user.etrap, number=old_user.number)
#                                 except:
#                                     errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Договор не найден в базе"]) 
#                                     continue
#                             type_='Internet'
#                     # abonplata
#                     elif 'old' in dogowor:
#                         dogowor = dogowor.replace('old', '')
#                         if '-' in dogowor:
#                             dogowor = dogowor.replace('-', '')
#                         if '_' in dogowor:
#                             dogowor = dogowor.replace('_', '')
#                         # проверка есть ли другие символы кроме цифр в договоре
#                         if any(char.isdigit() for char in dogowor):
#                             # Содержит только цифры
                            
#                             number = str(dogowor)[-5:]
#                             code = str(dogowor)[-8:-5]
#                             user_etrap = getEtrapNameFromCode(code)
#                             if user_etrap:
#                                 if 'off' in str(xlsx_data).lower():
#                                     try:
#                                         user_pk = code_number_pk[f"{code}{number}"]
#                                     except:
#                                         errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
#                                         continue
#                                     user = UserTable.objects.get(pk=user_pk)
#                                     pay_off = PayHistory.objects.filter(abonent=user, prochee=price, date=d[6], kassir=d[3].strip())
#                                     if len(pay_off) > 0:
#                                         total_off_already_payed += 1
#                                         continue
#                                     else:
#                                         # print(user.number, )
#                                         type_ = 'Abonplata'
#                                         abonplataCount += 1
#                                         total_price_abonplata += price
#                                         umumy_total += price
#                                 else:
#                                     try:
#                                         user_pk = code_number_pk[f"{code}{number}"]
#                                     except:
#                                         errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
#                                         continue
#                                     user = UserTable.objects.get(pk=user_pk)
#                                     type_='Abonplata'
#                                     abonplataCount += 1
#                                     total_price_abonplata += price
#                                     umumy_total += price
#                             else:
#                                 errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Код этрапа или номер в договоре некорректный"])
#                                 continue
#                         else:
#                             errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Непонятный договор"])
#                             continue
                        

#                     elif 'ctv' in dogowor:
#                         tvCount += 1
#                         total_price_tv += price
#                         umumy_total += price
#                         if len(dogowor) == 15:
#                             # print(len(dogowor))
#                             number = ''.join(filter(str.isdigit, dogowor))[-5:]
#                             code = ''.join(filter(str.isdigit, dogowor))[-9:-6]
#                             # print(number, code)
#                         elif len(dogowor) == 16:
#                             # print(len(dogowor))
#                             number = ''.join(filter(str.isdigit, dogowor))[-6:]
#                             code = ''.join(filter(str.isdigit, dogowor))[-10:-7]
#                             # print(number, code)
#                         else:
#                             errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Непонятный договор"])
#                     else:
#                         errorList.append([d[12], d[11], d[14], d[3], d[6], d[2], f"Непонятный договор"])
#                         continue
     
#                 kod_oplaty = d[10] if d[10] != None else ''
#                 # test_total += price
#                 obj = PlatejiWhichAddKassirsEveryDay(
#                     number=user.number, 
#                     user_etrap=user.etrap, 
#                     kassir_etrap=managarNames[manager],
#                     type_pay=type_,
#                     pay_category=d[2].strip(),
#                     manager=manager,
#                     date=d[6],
#                     kodOplaty=kod_oplaty,
#                     dogowor=str(d[11]),
#                     name=d[12],
#                     is_enterprises=d[13],
#                     price=price,
#                     file_name=str(xlsx_data),
#                     who_add_file=request.user.username
#                     )
#                 bulk_create.append(obj)

#                 count += 1
#                 # if count % 1000 == 0:
#                 #     if request.POST.get('platejiTest'):
#                 #         print(f"Проверено {count}")
#                 #     else:
#                 #         print(f"Добавлено {count}")
                        
#                 # elif count == len(imported_data):
#                 #     if request.POST.get('platejiTest'):
#                 #         print(f"Проверено {count}")
#                 #     else:
#                 #         print(f"Добавлено {count}")

        
#         if request.POST.get('platejiTest'):
#             logger.info(f'==== Проверено {count}')
#             # print(f"Проверено {count}")
#         else:
#             logger.info(f'==== Добавлено {count}')
#             # print(f"Добавлено {count}")
#         if errorList:
#             messages.error(request, f"Ошибка")
#             context['errorList'] = errorList
#             context['xlsx_data'] = str(xlsx_data)
#             return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/errorBillingPlatejiFromKassa.html', context)
        
#         if errorManager:
#             messages.error(request, f"Ошибка! есть новые менеджеры, надо определить их тип")
#             context['errorManager'] = errorManager
#             return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)

#         totalCount = abonplataCount + iptvCount + intCount
#         totalPice = float('%.2f' % (total_price_abonplata + total_price_iptv + total_price_internet))
#         context['abonplataCount'] = f"{abonplataCount:_}"
#         context['total_price_abonplata'] = f"{float('%.2f' % (total_price_abonplata)):_}"
#         context['iptvCount'] = f"{iptvCount:_}"
#         context['total_price_iptv'] = f"{float('%.2f' % (total_price_iptv)):_}"
#         context['intCount'] = f"{intCount:_}"
#         context['total_price_internet'] = f"{float('%.2f' % (total_price_internet)):_}"
#         context['totalCount'] = f"{totalCount:_}"
#         context['totalPice'] = f"{totalPice:_}"

#         if already_nach:
#             messages.error(request, f'Этот файл "{str(xlsx_data)}" уже был добавлен в в базу платежей')
#             return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)

#         if request.POST.get('platejiTest'):
#             # Проверка
#             if date_convertered_to_price:
#                 messages.error(request, f"Есть Ошибки! дата вместо цены")
#                 context['errorList'] = date_convertered_to_price
#                 context['xlsx_data'] = str(xlsx_data)
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/errorBillingPlatejiFromKassa.html', context)
#             messages.success(request, f"Проверка прошла успешно")
#             # print('test_total', test_total)
#         else:
#             # Добавить
#             try:
#                 with transaction.atomic():
#                     if bulk_create:
#                         PlatejiWhichAddKassirsEveryDay.objects.bulk_create(bulk_create)
#                     StaffAction.objects.create(user=request.user, comment=f'Добавления платежей в Базу Данных, файл {str(xlsx_data)}, дата добавления {datetime.now()}, добавил {request.user.username}', action='Добавления платежей в базу')
#                     SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.create(
#                         file_name=str(xlsx_data),
#                         etrap_add=log,
#                         who_add=request.user.username,
#                         when_add=datetime.now()
#                     )
#                     messages.success(request, f"Успешно добавлено в БД")
#             except Exception as e:
#                 messages.error(request, f'(откат сохранений) ошибка с transaction при сохранении, тип ошибки == {e}')
#                 logger.error(f'(откат сохранений) ошибка с transaction при сохранении, тип ошибки == {e}')


#     return render(request, 'telekom/MATB/pays_from_billing/add_month_pays_from_billing_to_my_programm.html', context)