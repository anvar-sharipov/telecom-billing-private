from django.shortcuts import render,redirect
from django.contrib import messages



from tablib import Dataset
from telekom. models import DontRepeatYourself, ImportAlemNachisleniyaOFF, ImportAlemNachisleniyaON, ImportInternetNachisleniyaOFF, ImportInternetNachisleniyaON, ImportInternetPlateji, ImportInternetPlatejiOFF, MonthPlatejiFromBilling, MonthPlatejiOFFFromBilling, StaffAction

from itertools import chain
from datetime import date, datetime

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup


def importXlsx(request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        pass
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    context={}
    context['matbIndex'] = True
    context['importXlsx'] = True

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

    """######################################################
        Если нажал на добавить/проверить в Внешние Платежи ##
    """######################################################

    if request.method == 'POST' and 'internetPlateji' in request.POST:
        dataset = Dataset()
        # Если файл не выбран то ошибка
        try:
            xlsx_data = request.FILES['my_file']
        except:
            messages.error(request, f'Выберите Файл')
            return redirect('import-xlsx')

        # если формат не xlsx то Ошибка
        try:
            imported_data = dataset.load(xlsx_data.read(), format='xlsx')
        except:
            messages.error(request, f'Файл должен быть формата xlsx')
            return redirect('import-xlsx')
        
        if 'plateji' not in str(xlsx_data).lower():
            messages.error(request, f'В файле должен быть слово "plateji"')
            return redirect('import-xlsx')
        
        count = 0
        success_count = 0

        # Добавление данных в БД
        if request.POST.get('internetPlatejiTest') == None:
            try:
                DontRepeatYourself.objects.get(internetPlatejiXlsxName = str(xlsx_data))
                messages.error(request, f'ОШИБКА! Файл Уже был добавлен в БД. Файл: {str(xlsx_data)}')
                return redirect('import-xlsx')
            except:
                pass
            
            data_list = []
            for data in imported_data:
                if len(data) != 6:
                    messages.error(request, f'Ошибка! столбцов должно быть 6; 1)Способ оплаты, 2)Дата оплаты, 3)№ договора, 4)Ф.И.О, 4)Платеж, 6)Этрап')
                    return redirect('import-xlsx')

                # Если оплата нули или отрицательные то next
                try:
                    price = float(data[4].replace(",", "."))
                except:
                    try:
                        price = float(data[4])
                    except:
                        continue
                if price <= 0:
                    continue

                
                # Если в договоре есть буквы то upperCase()
                try:
                    dogowor = int(data[2])
                except:
                    dogowor = data[2].lstrip().rstrip().upper()

                if data[3] == None:
                    FAO = ''
                else:
                    FAO = data[3]

    
                success_count += 1

                data_list.append([data[0].lstrip().rstrip().upper(), data[1], dogowor, FAO, price, data[5]])

     
            # bulk_create
            if request.POST.get('off') == None:
                if 'ON' not in str(xlsx_data):
                    messages.error(request, f'В имени файла нет слова ON, а вы пытаетесь добавить в "ON" БД')
                    return redirect('import-xlsx')
                aux = []
                for item in data_list:
                    obj = ImportInternetPlateji(type=item[0], pay_date=item[1], dogowor=item[2], FAO=item[3], price=item[4], etrap=item[5])
                    aux.append(obj)
                ImportInternetPlateji.objects.bulk_create(aux)
            else:
                if 'OFF' not in str(xlsx_data):
                    messages.error(request, f'В имени файла нет слова OFF, а вы пытаетесь добавить в "OFF" БД')
                    return redirect('import-xlsx')
                aux = []
                for item in data_list:
                    obj = ImportInternetPlatejiOFF(type=item[0], pay_date=item[1], dogowor=item[2], FAO=item[3], price=item[4], etrap=item[5])
                    aux.append(obj)
                ImportInternetPlatejiOFF.objects.bulk_create(aux)

            DontRepeatYourself.objects.create(internetPlatejiXlsxName=str(xlsx_data))

            StaffAction.objects.create(user=request.user, comment=f'{request.POST.get("comment")} \n\nДабавления платежей с xlsx файла в БД \n\nНазвание файла: {str(xlsx_data)}', action='Импорт с xlsx внешние платежи в БД')

            messages.success(request, f'{success_count} Платежей Успешно Добавлено в БД. Файл: {xlsx_data}')
            return redirect('import-xlsx')

        # Проверка данных
        else:
            something_with_type = []
            something_with_date = []
            something_with_dogowor = []
            something_with_FAO = []
            something_with_price = []
            something_with_etrap = []

            lessThanNull = []

            lenSuccess = 0

            for data in imported_data:
                if len(data) != 6:
                    messages.error(request, f'Ошибка! столбцов должно быть 6; 1)Способ оплаты, 2)Дата оплаты, 3)№ договора, 4)Ф.И.О, 4)Платеж, 6)Этрап')
                    return redirect('import-xlsx')
                
                
                # Если оплата нули или отрицательные то next
                try:
                    price = float(data[4].replace(",", "."))
                except:
                    try:
                        price = float(data[4])
                    except:
                        something_with_price.append(data)
                        continue

                if price <= 0:
                    lessThanNull.append(data)
                    continue

                # Если в договоре есть буквы то upperCase()
                try:
                    dogowor = int(data[2])
                except:
                    try:
                        dogowor = data[2].lstrip().rstrip().upper()
                    except:
                        something_with_dogowor.append(data)
                        continue

                # Проверка типа платежа
                try:
                    data[0].lstrip().rstrip().upper()
                except:
                    something_with_type.append(data)
                    continue

                # Проверка даты
                if data[1] == None:
                    something_with_date.append(data)
                    continue

                # Проверка Ф.И.О
                if data[3] == None:
                    something_with_FAO.append(data)
                    continue

                # Проверка этрапа
                if data[5] not in etraps:
                    something_with_etrap.append(data)
                    continue

                lenSuccess += 1


            if something_with_type:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Способ платежа"')
                context['errors'] = something_with_type
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)
            
            if something_with_date:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Дата платежа"')
                context['errors'] = something_with_date
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)
            
            if something_with_dogowor:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "№ договора"')
                context['errors'] = something_with_dogowor
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)
            
            if something_with_price:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Сумма Платежа"')
                context['errors'] = something_with_price
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)
            
            if something_with_etrap:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке Этрап: Должен быть один из этих вариантов {etraps}')
                context['errors'] = something_with_etrap
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)
            
            if something_with_FAO and lessThanNull:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Ф.И.О" и в "Сумма платежа". Успешных: {lenSuccess}, Ошибок: {len(something_with_FAO) + len(lessThanNull)}')
                context['something_with_FAOandlessThanNull'] = True
                context['errors'] = list(chain(something_with_FAO, lessThanNull))
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)
            
            if something_with_FAO:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Ф.И.О". Успешных: {lenSuccess}, Ошибок: {len(something_with_FAO)}')
                context['something_with_FAO'] = True
                context['errors'] = something_with_FAO
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)
            
            if lessThanNull:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Сумма Платежа". Успешных: {lenSuccess}, Ошибок: {len(lessThanNull)}')
                context['errors'] = lessThanNull
                context['lessThanNull'] = True
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)


            messages.success(request, f'Проверка Файла прошла успешно! Файл: {xlsx_data}. Платежей: {lenSuccess}.')

    """##########################################################
        Если нажал на добавить/проверить в Внешние Платежи END ##
    """##########################################################
    
    """##########################################################
        Если нажал на добавить/проверить в Интернет Начисления ##
    """##########################################################
    
    if request.method == 'POST' and 'internetNachisleniya' in request.POST:
        dataset = Dataset()
        # Если файл не выбран то ошибка
        try:
            xlsx_data = request.FILES['my_file2']
        except:
            messages.error(request, f'Выберите Файл')
            return redirect('import-xlsx')
        
        # если формат не xlsx то Ошибка
        try:
            imported_data = dataset.load(xlsx_data.read(), format='xlsx')
        except:
            messages.error(request, f'Файл должен быть формата xlsx')
            return redirect('import-xlsx')
        
        if 'internet' not in str(xlsx_data).lower():
            messages.error(request, f'В файле должно быть слово "internet"')
            return redirect('import-xlsx')

        success_count = 0

        # Добавление данных в БД
        if request.POST.get('internetNachisleniyaTest') == None:
            try:
                DontRepeatYourself.objects.get(internetNachisleniyaXlsxName = str(xlsx_data))
                messages.error(request, f'ОШИБКА! Файл Уже был добавлен в БД. Файл: {str(xlsx_data)}')
                return redirect('import-xlsx')
            except:
                pass
            
            lenErrorPrice = 0
            data_list = []
            for data in imported_data:
                
                if len(data) != 7:
                    messages.error(request, f'Ошибка! столбцов должно быть 7; 1)Ф.И.О, 2)№ договора, 3)логин, 4)Платеж, 5)Этрап, 6)Год, 7)Месяц')
                    return redirect('import-xlsx')

                # в платеже может быть дата
                try:
                    price = float(data[3].replace(",", "."))
                except:
                    try:
                        price = float(data[3])
                    except:
                        try:
                            if (str(data[3])[8:10] == '01'):
                                monthPrice = int(str(data[3])[5:7])
                                yearPrice = str(data[3])[2:4]
                                price = float(f"{monthPrice}.{yearPrice}")
                            elif (str(data[3])[8:10] != '01'):
                                dayPrice = int(str(data[3])[8:10])
                                monthPrice = str(data[3])[5:7]
                                price = float(f"{dayPrice}.{monthPrice}")
                        except:
                            something_with_price.append(data)
                            continue

                # Если цена меньше или равен 0 next
                if price < 0:
                    lenErrorPrice += 1
                    continue

                month = data[6]
                year = str(data[5])
                
                # Если в договоре есть буквы то upperCase()
                try:
                    dogowor = int(data[1])
                except:
                    dogowor = data[1].lstrip().rstrip().upper()

                # Если в логине есть буквы то lowerCase()
                try:
                    login = int(data[2])
                except:
                    login = data[2].lstrip().rstrip().lower()

                if data[0] == None:
                    FAO = ''
                else:
                    FAO = data[0]
                # список для bulk_create 
                data_list.append([FAO, dogowor, login, price, data[4], year, month])
                success_count += 1

            # bulk_create
            if request.POST.get('off') == None:
                if 'ON' not in str(xlsx_data):
                    messages.error(request, f'В имени файла нет слова ON, а вы пытаетесь добавить в "ON" БД')
                    return redirect('import-xlsx')
                aux = []
                for item in data_list:
                    obj = ImportInternetNachisleniyaON(FAO=item[0], dogowor=item[1], login=item[2], price=item[3], etrap=item[4], year=item[5], month=item[6])
                    aux.append(obj)
                ImportInternetNachisleniyaON.objects.bulk_create(aux)
            else:
                if 'OFF' not in str(xlsx_data):
                    messages.error(request, f'В имени файла нет слова OFF, а вы пытаетесь добавить в "OFF" БД')
                    return redirect('import-xlsx')
                aux = []
                for item in data_list:
                    obj = ImportInternetNachisleniyaOFF(FAO=item[0], dogowor=item[1], login=item[2], price=item[3], etrap=item[4], year=item[5], month=item[6])
                    aux.append(obj)
                ImportInternetNachisleniyaOFF.objects.bulk_create(aux)

            
            DontRepeatYourself.objects.create(internetNachisleniyaXlsxName=str(xlsx_data))

            StaffAction.objects.create(user=request.user, comment=f'{request.POST.get("comment")} \n\nДабавления данных с xlsx файла в БД \n\nНазвание файла: {str(xlsx_data)}', action='Импорт с xlsx Интернет Начисления в БД')

            messages.success(request, f'Успешное добавление данных, файл: {xlsx_data}. Успешных: {success_count}, Ошибок: {lenErrorPrice} (где сумма <= 0)')
            return redirect('import-xlsx')
        
        # Проверка данных
        else:
            something_with_dogowor = []
            something_with_login = []
            something_with_price = []
            something_with_etrap = []
            something_with_FAO = []
            something_with_month = []
            something_with_year = []

            lessThanNull = []

            lenSuccess = 0

            total_sum = 0
            for data in imported_data:
                if len(data) != 7:
                    print(data)
                else:
                    pass
                if len(data) != 7:
                    messages.error(request, f'Ошибка! столбцов должно быть 7; 1)Ф.И.О, 2)№ договора, 3)логин, 4)Платеж, 5)Этрап, 6)Год, 7)Месяц')
                    return redirect('import-xlsx')
                
                # Проверка Месяца
                if data[6] not in months:
                    something_with_month.append(data)
                    continue

                # Проверка года
                try:
                    int(data[5])
                    if len(str(data[5])) != 4:
                        something_with_year.append(data)
                        continue
                except:
                    something_with_year.append(data)
                    continue

                # в оплате может быть дата
                try:
                    price = float(data[3].replace(",", "."))
                except:
                    try:
                        price = float(data[3])
                    except:
                        try:
                            if (str(data[3])[8:10] == '01'):
                                monthPrice = int(str(data[3])[5:7])
                                yearPrice = str(data[3])[2:4]
                                price = float(f"{monthPrice}.{yearPrice}")
                            elif (str(data[3])[8:10] != '01'):
                                dayPrice = int(str(data[3])[8:10])
                                monthPrice = str(data[3])[5:7]
                                price = float(f"{dayPrice}.{monthPrice}")
                        except:
                            something_with_price.append(data)
                            continue

                total_sum += price

                # Если оплата нули или отрицательные то next
                if price < 0:
                    lessThanNull.append(data)
                    continue


                # Если в договоре есть буквы то upperCase()
                try:
                    dogowor = int(data[1])
                except:
                    try:
                        dogowor = data[1].lstrip().rstrip().upper()
                    except:
                        something_with_dogowor.append(data)
                        continue


                # Если в логине есть буквы то lowerCase()
                try:
                    login = int(data[2])
                except:
                    try:
                        login = data[2].lstrip().rstrip().lower()
                    except:
                        something_with_login.append(data)
                        continue

                if data[4] not in etraps:
                    something_with_etrap.append(data)
                    continue

                # Проверка Ф.И.О
                if data[0] == None:
                    something_with_FAO.append(data)
                    continue

                lenSuccess += 1

            if something_with_dogowor:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "№ Договора"')
                context['errors'] = something_with_dogowor
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
            
            if something_with_login:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Логин"')
                context['errors'] = something_with_login
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)

            if something_with_price:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "сумма платежа"')
                context['errors'] = something_with_price
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
            
            if something_with_etrap:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Этрап": Должно быть один из этих вариантов {etraps}')
                context['errors'] = something_with_etrap
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
            
            if something_with_month:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Месяц": Должно быть один из этих вариантов {months}')
                context['errors'] = something_with_month
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
            
            if something_with_year:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Год"')
                context['errors'] = something_with_year
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
            
            if something_with_FAO and lessThanNull:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Ф.И.О" и в "Сумма платежа". Успешных: {lenSuccess}, Ошибок: {len(something_with_FAO) + len(lessThanNull)}, Общая сумма: {"%.2f" % total_sum} manat')
                context['something_with_FAOandlessThanNull'] = True
                context['errors'] = list(chain(something_with_FAO, lessThanNull))
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
            
            if something_with_FAO:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Ф.И.О". Успешных: {lenSuccess}, Ошибок: {len(something_with_FAO)}, Общая сумма: {"%.2f" % total_sum} manat')
                context['something_with_FAO'] = True
                context['errors'] = something_with_FAO
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
 
            
            if lessThanNull:
                messages.success(request, f'Ошибка! Файл: {xlsx_data} в колонке "Сумма Платежа". Успешных: {lenSuccess}, Ошибок: {len(lessThanNull)}, Общая сумма: {"%.2f" % total_sum} manat')
          
                context['errors'] = lessThanNull
                context['lessThanNull'] = True
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
            
            messages.success(request, f'Проверка Файла прошла успешно. {len(imported_data)} Платежей. Файл: {xlsx_data}, Общая сумма: {"%.2f" % total_sum} manat')
       

    """##############################################################
        Если нажал на добавить/проверить в Интернет Начисления END ##
    """##############################################################

    """######################################################
        Если нажал на добавить/проверить в Alem Начисления ##
    """######################################################

    if request.method == 'POST' and 'alemNachisleniya' in request.POST:
        dataset = Dataset()
        # Если файл не выбран то ошибка
        try:
            xlsx_data = request.FILES['my_file3']
        except:
            messages.error(request, f'Выберите Файл')
            return redirect('import-xlsx')
        
        # если формат не xlsx то Ошибка
        try:
            imported_data = dataset.load(xlsx_data.read(), format='xlsx')
        except:
            messages.error(request, f'Файл должен быть формата xlsx')
            return redirect('import-xlsx')


        if 'alem' not in str(xlsx_data).lower():
            messages.error(request, f'В файле должен быть слово "alem"')
            return redirect('import-xlsx')

        success_count = 0

        # # Добавление данных в БД
        if request.POST.get('alemNachisleniyaTest') == None:
            try:
                DontRepeatYourself.objects.get(alemNachisleniyaXlsxName = str(xlsx_data))
                messages.error(request, f'ОШИБКА! Файл Уже был добавлен в БД. Файл: {str(xlsx_data)}')
                return redirect('import-xlsx')
            except:
                pass
            
            lenErrorPrice = 0
            data_list = []
            for data in imported_data:
                if len(data) != 7:
                    messages.error(request, f'Ошибка! столбцов должно быть 7; 1)Ф.И.О, 2)№ договора, 3)логин, 4)Платеж, 5)Этрап, 6)Год, 7)Месяц')
                    return redirect('import-xlsx')

                # в оплате может быть дата
                try:
                    price = float(data[3].replace(",", "."))
                except:
                    try:
                        price = float(data[3])
                    except:
                        if (str(data[3])[8:10] == '01'):
                            monthPrice = int(str(data[3])[5:7])
                            yearPrice = str(data[3])[2:4]
                            price = float(f"{monthPrice}.{yearPrice}")
                        elif (str(data[3])[8:10] != '01'):
                            dayPrice = int(str(data[3])[8:10])
                            monthPrice = str(data[3])[5:7]
                            price = float(f"{dayPrice}.{monthPrice}")
                
                # Если цена меньше или равен 0 next
                if price <= 0:
                    lenErrorPrice += 1
                    continue

                month = data[6]
                year = str(data[5])
                
                # Если в договоре есть буквы то upperCase()
                try:
                    dogowor = int(data[1])
                except:
                    dogowor = data[1].lstrip().rstrip().upper()

                # Если в логине есть буквы то lowerCase()
                try:
                    login = int(data[2])
                except:
                    login = data[2].lstrip().rstrip().lower()

                if data[0] == None:
                    FAO = ''
                else:
                    FAO = data[0]
                # список для bulk_create 
                data_list.append([FAO, dogowor, login, price, data[4], year, month])
                success_count += 1

            # bulk_create
            if request.POST.get('off') == None :
                if 'ON' not in str(xlsx_data):
                    messages.error(request, f'В имени файла нет слова ON, а вы пытаетесь добавить в "ON" БД')
                    return redirect('import-xlsx')
                
                aux = []
                for item in data_list:
                    obj = ImportAlemNachisleniyaON(FAO=item[0], dogowor=item[1], login=item[2], price=item[3], etrap=item[4], year=item[5], month=item[6])
                    aux.append(obj)
                ImportAlemNachisleniyaON.objects.bulk_create(aux)
            else:
                if 'OFF' not in str(xlsx_data):
                    messages.error(request, f'В имени файла нет слова OFF, а вы пытаетесь добавить в "OFF" БД')
                    return redirect('import-xlsx')
                aux = []
                for item in data_list:
                    obj = ImportAlemNachisleniyaOFF(FAO=item[0], dogowor=item[1], login=item[2], price=item[3], etrap=item[4], year=item[5], month=item[6])
                    aux.append(obj)
                ImportAlemNachisleniyaOFF.objects.bulk_create(aux)

            
            DontRepeatYourself.objects.create(alemNachisleniyaXlsxName=str(xlsx_data))

            StaffAction.objects.create(user=request.user, comment=f'Дабавления данных с xlsx файла в БД \n\nНазвание файла: {str(xlsx_data)}', action='Импорт с xlsx Alem Начисления в БД')

            messages.success(request, f'Успешное добавление данных, файл: {xlsx_data}. Успешных: {success_count}, Ошибок: {lenErrorPrice} (где сумма <= 0)')
      
            return redirect('import-xlsx')
        
        # Проверка данных
        else:
            something_with_dogowor = []
            something_with_login = []
            something_with_price = []
            something_with_etrap = []
            something_with_FAO = []
            something_with_month = []
            something_with_year = []

            lessThanNull = []

            lenSuccess = 0

            total_sum = 0
            for data in imported_data:
                if len(data) != 7:
                    messages.error(request, f'Ошибка! столбцов должно быть 7; 1)Ф.И.О, 2)№ договора, 3)логин, 4)Платеж, 5)Этрап, 6)Год, 7)Месяц')
                    return redirect('import-xlsx')
                
                # Проверка Месяца
                if data[6] not in months:
                    something_with_month.append(data)
                    continue

                # Проверка года
                try:
                    int(data[5])
                    if len(str(data[5])) != 4:
                        something_with_year.append(data)
                        continue
                except:
                    something_with_year.append(data)
                    continue

                
                # в оплате может быть дата
                try:
                    price = float(data[3].replace(",", "."))
                except:
                    try:
                        price = float(data[3])
                    except:
                        try:
                            if (str(data[3])[8:10] == '01'):
                                monthPrice = int(str(data[3])[5:7])
                                yearPrice = str(data[3])[2:4]
                                price = float(f"{monthPrice}.{yearPrice}")
                            elif (str(data[3])[8:10] != '01'):
                                dayPrice = int(str(data[3])[8:10])
                                monthPrice = str(data[3])[5:7]
                                price = float(f"{dayPrice}.{monthPrice}")
                        except:
                            something_with_price.append(data)
                            continue

                total_sum += price

                # Если оплата нули или отрицательные то next
                if price <= 0:
                    lessThanNull.append(data)
                    continue


                # Если в договоре есть буквы то upperCase()
                try:
                    dogowor = int(data[1])
                except:
                    try:
                        dogowor = data[1].lstrip().rstrip().upper()
                    except:
                        something_with_dogowor.append(data)
                        continue


                # Если в логине есть буквы то lowerCase()
                try:
                    login = int(data[2])
                except:
                    try:
                        login = data[2].lstrip().rstrip().lower()
                    except:
                        something_with_login.append(data)
                        continue

                if data[4] not in etraps:
                    something_with_etrap.append(data)
                    continue

                # Проверка Ф.И.О
                if data[0] == None:
                    something_with_FAO.append(data)
                    continue

                lenSuccess += 1

            if something_with_dogowor:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "№ Договора"')
                context['errors'] = something_with_dogowor
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
            
            if something_with_login:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Логин"')
                context['errors'] = something_with_login
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)

            if something_with_price:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "сумма платежа"')
                context['errors'] = something_with_price
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
            
            if something_with_etrap:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Этрап": Должно быть один из этих вариантов {etraps}')
                context['errors'] = something_with_etrap
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
            
            if something_with_month:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Месяц": Должно быть один из этих вариантов {months}')
                context['errors'] = something_with_month
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
            
            if something_with_year:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Год"')
                context['errors'] = something_with_year
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
            
            if something_with_FAO and lessThanNull:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Ф.И.О" и в "Сумма платежа". Успешных: {lenSuccess}, Ошибок: {len(something_with_FAO) + len(lessThanNull)}, Общая сумма: {"%.2f" % total_sum} manat')
                context['something_with_FAOandlessThanNull'] = True
                context['errors'] = list(chain(something_with_FAO, lessThanNull))
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
            
            if something_with_FAO:
                messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Ф.И.О". Успешных: {lenSuccess}, Ошибок: {len(something_with_FAO)}, Общая сумма: {"%.2f" % total_sum} manat')
                context['something_with_FAO'] = True
                context['errors'] = something_with_FAO
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
 
            
            if lessThanNull:
                messages.success(request, f'Ошибка! Файл: {xlsx_data} в колонке "Сумма Платежа". Успешных: {lenSuccess}, Ошибок: {len(lessThanNull)}, Общая сумма: {"%.2f" % total_sum} manat')
      
                context['errors'] = lessThanNull
                context['lessThanNull'] = True
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
            
            messages.success(request, f'Проверка Файла прошла успешно. {len(imported_data)} Платежей. Файл: {xlsx_data}, Общая сумма: {"%.2f" % total_sum} manat')
     

    """##########################################################
        Если нажал на добавить/проверить в Alem Начисления END ##
    """##########################################################


    if request.method == 'POST' and 'platejiSbillinga' in request.POST:
        dataset = Dataset()
        # Если файл не выбран то ошибка
        try:
            xlsx_data = request.FILES['my_file4']
        except:
            messages.error(request, f'Выберите Файл')
            return redirect('import-xlsx')
        
        # если формат не xlsx то Ошибка
        try:
            imported_data = dataset.load(xlsx_data.read(), format='xlsx')
        except:
            messages.error(request, f'Файл должен быть формата xlsx')
            return redirect('import-xlsx')


        if 'billingplateji' not in str(xlsx_data).lower():
            messages.error(request, f'В файле должен быть слово "billingplateji"')
            return redirect('import-xlsx')
        count = 0
        # 2=type_pay (Внешние пл., default, оплата с картой), 3=manager, 6=datePlatej, 11=dogowor, 12=FIO, 13=yurOrFiz 14=price
        
        errorDict = {} # {row: [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]}
        if request.POST.get('platejiSbillingaTest') == None:
            total_sum = 0
            total_date_sum = 0
            bulk_create_list = []
            onOF = request.POST.get('off') # None или 'on'
            for d in imported_data:
                
                if d[10]:
                    kod_oplaty = d[10]
                else:
                    kod_oplaty = ''
                str_date = ''

                count += 1
                if count >= 8:   
                    manager = d[3]
                    date_ = d[6]
                    dogowor= d[11]
                    fio = d[12]
                    price = d[14]
                    if d[10]:
                        kod_oplaty = d[10]
                    else:
                        kod_oplaty = ''
                    type_pay = d[2].strip()
                    yurOrFiz = d[13].strip()
                    if dogowor == None:
                        errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
                        continue
                    elif date_ == None:
                        errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
                        continue
                    elif manager == None:
                        errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
                        continue
                    elif price == None:
                        errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
                        continue
                    elif isinstance(price, (date, datetime)):
                            str_date = str(price)
                            if str_date[8:10] == '01':
                                manat = str_date[5:7]
                                tenne = str_date[2:4]
                                price = float(f"{manat}.{tenne}")
                            else:
                                manat = str_date[8:10]
                                tenne = str_date[5:7]
                                price = float(f"{manat}.{tenne}")
                            total_date_sum += price
                    total_sum += float(price)
                    if onOF:
                        obj = MonthPlatejiOFFFromBilling(platejiType=type_pay, manager=manager, pay_date=date_, dogowor=dogowor, price=price, date_price=str_date, kod_oplaty=kod_oplaty, FAO=fio, YurOrFiz=yurOrFiz)
                    else:
                        obj = MonthPlatejiFromBilling(platejiType=type_pay, manager=manager, pay_date=date_, dogowor=dogowor, price=price, date_price=str_date, kod_oplaty=kod_oplaty, FAO=fio, YurOrFiz=yurOrFiz)     
                    bulk_create_list.append(obj)
            if errorDict:
                messages.error(request, f'Ошибка! Файл: {xlsx_data}')
                context['errorDict'] = errorDict
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/billingPlatejiErrors.html', context)
            else:
                if bulk_create_list:
                    if onOF: 
                        MonthPlatejiOFFFromBilling.objects.bulk_create(bulk_create_list)
                        messages.success(request, f'Добавлено успешно. Файл: {xlsx_data}, Общая сумма: {"%.2f" % total_sum} manat, количество платежей {count-7}')
            
                    else:
                        MonthPlatejiFromBilling.objects.bulk_create(bulk_create_list)
                        messages.success(request, f'Добавлено успешно. Файл: {xlsx_data}, Общая сумма: {"%.2f" % total_sum} manat, количество платежей {count-7}')
                    
                        
        else:
            # 3=manager, 6=datePlatej, 11=dogowor, 12=FIO, 14=price
            total_sum = 0
            total_date_sum = 0
            for d in imported_data:

                count += 1
                if count >= 8:
                    manager = d[3]
                    date_ = d[6]
                    dogowor= d[11]
                    fio = d[12]
                    price = d[14]
                    kod_oplaty = d[10]
                    type_pay = d[2].strip()
                    yurOrFiz = d[13].strip()  
                    if dogowor == None:
                        errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
                        continue
                    elif date_ == None:
                        errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
                        continue
                    elif manager == None:
                        errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
                        continue
                    elif price == None:
                        errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
                        continue
                    elif isinstance(price, (date, datetime)):
                            str_date = str(price)
                            if str_date[8:10] == '01':
                                manat = str_date[5:7]
                                tenne = str_date[2:4]
                                price = float(f"{manat}.{tenne}")
                            else:
                                manat = str_date[8:10]
                                tenne = str_date[5:7]
                                price = float(f"{manat}.{tenne}")
                            total_date_sum += price
                    total_sum += float(price)
            if errorDict:
                messages.error(request, f'Ошибка! Файл: {xlsx_data}')
                context['errorDict'] = errorDict
                return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/billingPlatejiErrors.html', context)
            else:
                messages.success(request, f'Проверка Файла прошла успешно. {count-7} Платежей. Файл: {xlsx_data}, Общая сумма: {"%.2f" % total_sum} manat')
       
                print('total_date_sum', total_date_sum)




    return render(request, 'telekom/MATB/xlsx/importXlsx/importXlsx.html', context)

# rabotaet no bez 2 nowyyh etrapow
# from django.shortcuts import render,redirect
# from django.contrib import messages



# from tablib import Dataset
# from telekom. models import DontRepeatYourself, ImportAlemNachisleniyaOFF, ImportAlemNachisleniyaON, ImportInternetNachisleniyaOFF, ImportInternetNachisleniyaON, ImportInternetPlateji, ImportInternetPlatejiOFF, MonthPlatejiFromBilling, MonthPlatejiOFFFromBilling, StaffAction

# from itertools import chain
# from datetime import date, datetime

# from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup


# def importXlsx(request):
#     EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
#     if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
#         pass
#     else:
#         messages.error(request, f'Доступ только соотрудникам MATB')
#         return redirect('user-login')
    
#     context={}
#     context['matbIndex'] = True
#     context['importXlsx'] = True

#     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
#     months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

#     """######################################################
#         Если нажал на добавить/проверить в Внешние Платежи ##
#     """######################################################

#     if request.method == 'POST' and 'internetPlateji' in request.POST:
#         dataset = Dataset()
#         # Если файл не выбран то ошибка
#         try:
#             xlsx_data = request.FILES['my_file']
#         except:
#             messages.error(request, f'Выберите Файл')
#             return redirect('import-xlsx')

#         # если формат не xlsx то Ошибка
#         try:
#             imported_data = dataset.load(xlsx_data.read(), format='xlsx')
#         except:
#             messages.error(request, f'Файл должен быть формата xlsx')
#             return redirect('import-xlsx')
        
#         if 'plateji' not in str(xlsx_data).lower():
#             messages.error(request, f'В файле должен быть слово "plateji"')
#             return redirect('import-xlsx')
        
#         count = 0
#         success_count = 0

#         # Добавление данных в БД
#         if request.POST.get('internetPlatejiTest') == None:
#             try:
#                 DontRepeatYourself.objects.get(internetPlatejiXlsxName = str(xlsx_data))
#                 messages.error(request, f'ОШИБКА! Файл Уже был добавлен в БД. Файл: {str(xlsx_data)}')
#                 return redirect('import-xlsx')
#             except:
#                 pass
            
#             data_list = []
#             for data in imported_data:
#                 if len(data) != 6:
#                     messages.error(request, f'Ошибка! столбцов должно быть 6; 1)Способ оплаты, 2)Дата оплаты, 3)№ договора, 4)Ф.И.О, 4)Платеж, 6)Этрап')
#                     return redirect('import-xlsx')

#                 # Если оплата нули или отрицательные то next
#                 try:
#                     price = float(data[4].replace(",", "."))
#                 except:
#                     try:
#                         price = float(data[4])
#                     except:
#                         continue
#                 if price <= 0:
#                     continue

                
#                 # Если в договоре есть буквы то upperCase()
#                 try:
#                     dogowor = int(data[2])
#                 except:
#                     dogowor = data[2].lstrip().rstrip().upper()

#                 if data[3] == None:
#                     FAO = ''
#                 else:
#                     FAO = data[3]

    
#                 success_count += 1

#                 data_list.append([data[0].lstrip().rstrip().upper(), data[1], dogowor, FAO, price, data[5]])

     
#             # bulk_create
#             if request.POST.get('off') == None:
#                 if 'ON' not in str(xlsx_data):
#                     messages.error(request, f'В имени файла нет слова ON, а вы пытаетесь добавить в "ON" БД')
#                     return redirect('import-xlsx')
#                 aux = []
#                 for item in data_list:
#                     obj = ImportInternetPlateji(type=item[0], pay_date=item[1], dogowor=item[2], FAO=item[3], price=item[4], etrap=item[5])
#                     aux.append(obj)
#                 ImportInternetPlateji.objects.bulk_create(aux)
#             else:
#                 if 'OFF' not in str(xlsx_data):
#                     messages.error(request, f'В имени файла нет слова OFF, а вы пытаетесь добавить в "OFF" БД')
#                     return redirect('import-xlsx')
#                 aux = []
#                 for item in data_list:
#                     obj = ImportInternetPlatejiOFF(type=item[0], pay_date=item[1], dogowor=item[2], FAO=item[3], price=item[4], etrap=item[5])
#                     aux.append(obj)
#                 ImportInternetPlatejiOFF.objects.bulk_create(aux)

#             DontRepeatYourself.objects.create(internetPlatejiXlsxName=str(xlsx_data))

#             StaffAction.objects.create(user=request.user, comment=f'{request.POST.get("comment")} \n\nДабавления платежей с xlsx файла в БД \n\nНазвание файла: {str(xlsx_data)}', action='Импорт с xlsx внешние платежи в БД')

#             messages.success(request, f'{success_count} Платежей Успешно Добавлено в БД. Файл: {xlsx_data}')
#             return redirect('import-xlsx')

#         # Проверка данных
#         else:
#             something_with_type = []
#             something_with_date = []
#             something_with_dogowor = []
#             something_with_FAO = []
#             something_with_price = []
#             something_with_etrap = []

#             lessThanNull = []

#             lenSuccess = 0

#             for data in imported_data:
#                 if len(data) != 6:
#                     messages.error(request, f'Ошибка! столбцов должно быть 6; 1)Способ оплаты, 2)Дата оплаты, 3)№ договора, 4)Ф.И.О, 4)Платеж, 6)Этрап')
#                     return redirect('import-xlsx')
                
                
#                 # Если оплата нули или отрицательные то next
#                 try:
#                     price = float(data[4].replace(",", "."))
#                 except:
#                     try:
#                         price = float(data[4])
#                     except:
#                         something_with_price.append(data)
#                         continue

#                 if price <= 0:
#                     lessThanNull.append(data)
#                     continue

#                 # Если в договоре есть буквы то upperCase()
#                 try:
#                     dogowor = int(data[2])
#                 except:
#                     try:
#                         dogowor = data[2].lstrip().rstrip().upper()
#                     except:
#                         something_with_dogowor.append(data)
#                         continue

#                 # Проверка типа платежа
#                 try:
#                     data[0].lstrip().rstrip().upper()
#                 except:
#                     something_with_type.append(data)
#                     continue

#                 # Проверка даты
#                 if data[1] == None:
#                     something_with_date.append(data)
#                     continue

#                 # Проверка Ф.И.О
#                 if data[3] == None:
#                     something_with_FAO.append(data)
#                     continue

#                 # Проверка этрапа
#                 if data[5] not in etraps:
#                     something_with_etrap.append(data)
#                     continue

#                 lenSuccess += 1


#             if something_with_type:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Способ платежа"')
#                 context['errors'] = something_with_type
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)
            
#             if something_with_date:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Дата платежа"')
#                 context['errors'] = something_with_date
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)
            
#             if something_with_dogowor:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "№ договора"')
#                 context['errors'] = something_with_dogowor
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)
            
#             if something_with_price:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Сумма Платежа"')
#                 context['errors'] = something_with_price
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)
            
#             if something_with_etrap:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке Этрап: Должен быть один из этих вариантов {etraps}')
#                 context['errors'] = something_with_etrap
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)
            
#             if something_with_FAO and lessThanNull:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Ф.И.О" и в "Сумма платежа". Успешных: {lenSuccess}, Ошибок: {len(something_with_FAO) + len(lessThanNull)}')
#                 context['something_with_FAOandlessThanNull'] = True
#                 context['errors'] = list(chain(something_with_FAO, lessThanNull))
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)
            
#             if something_with_FAO:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Ф.И.О". Успешных: {lenSuccess}, Ошибок: {len(something_with_FAO)}')
#                 context['something_with_FAO'] = True
#                 context['errors'] = something_with_FAO
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)
            
#             if lessThanNull:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Сумма Платежа". Успешных: {lenSuccess}, Ошибок: {len(lessThanNull)}')
#                 context['errors'] = lessThanNull
#                 context['lessThanNull'] = True
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetPlatejiErrors.html', context)


#             messages.success(request, f'Проверка Файла прошла успешно! Файл: {xlsx_data}. Платежей: {lenSuccess}.')

#     """##########################################################
#         Если нажал на добавить/проверить в Внешние Платежи END ##
#     """##########################################################
    
#     """##########################################################
#         Если нажал на добавить/проверить в Интернет Начисления ##
#     """##########################################################
    
#     if request.method == 'POST' and 'internetNachisleniya' in request.POST:
#         dataset = Dataset()
#         # Если файл не выбран то ошибка
#         try:
#             xlsx_data = request.FILES['my_file2']
#         except:
#             messages.error(request, f'Выберите Файл')
#             return redirect('import-xlsx')
        
#         # если формат не xlsx то Ошибка
#         try:
#             imported_data = dataset.load(xlsx_data.read(), format='xlsx')
#         except:
#             messages.error(request, f'Файл должен быть формата xlsx')
#             return redirect('import-xlsx')
        
#         if 'internet' not in str(xlsx_data).lower():
#             messages.error(request, f'В файле должно быть слово "internet"')
#             return redirect('import-xlsx')

#         success_count = 0

#         # Добавление данных в БД
#         if request.POST.get('internetNachisleniyaTest') == None:
#             try:
#                 DontRepeatYourself.objects.get(internetNachisleniyaXlsxName = str(xlsx_data))
#                 messages.error(request, f'ОШИБКА! Файл Уже был добавлен в БД. Файл: {str(xlsx_data)}')
#                 return redirect('import-xlsx')
#             except:
#                 pass
            
#             lenErrorPrice = 0
#             data_list = []
#             for data in imported_data:
                
#                 if len(data) != 7:
#                     messages.error(request, f'Ошибка! столбцов должно быть 7; 1)Ф.И.О, 2)№ договора, 3)логин, 4)Платеж, 5)Этрап, 6)Год, 7)Месяц')
#                     return redirect('import-xlsx')

#                 # в платеже может быть дата
#                 try:
#                     price = float(data[3].replace(",", "."))
#                 except:
#                     try:
#                         price = float(data[3])
#                     except:
#                         try:
#                             if (str(data[3])[8:10] == '01'):
#                                 monthPrice = int(str(data[3])[5:7])
#                                 yearPrice = str(data[3])[2:4]
#                                 price = float(f"{monthPrice}.{yearPrice}")
#                             elif (str(data[3])[8:10] != '01'):
#                                 dayPrice = int(str(data[3])[8:10])
#                                 monthPrice = str(data[3])[5:7]
#                                 price = float(f"{dayPrice}.{monthPrice}")
#                         except:
#                             something_with_price.append(data)
#                             continue

#                 # Если цена меньше или равен 0 next
#                 if price < 0:
#                     lenErrorPrice += 1
#                     continue

#                 month = data[6]
#                 year = str(data[5])
                
#                 # Если в договоре есть буквы то upperCase()
#                 try:
#                     dogowor = int(data[1])
#                 except:
#                     dogowor = data[1].lstrip().rstrip().upper()

#                 # Если в логине есть буквы то lowerCase()
#                 try:
#                     login = int(data[2])
#                 except:
#                     login = data[2].lstrip().rstrip().lower()

#                 if data[0] == None:
#                     FAO = ''
#                 else:
#                     FAO = data[0]
#                 # список для bulk_create 
#                 data_list.append([FAO, dogowor, login, price, data[4], year, month])
#                 success_count += 1

#             # bulk_create
#             if request.POST.get('off') == None:
#                 if 'ON' not in str(xlsx_data):
#                     messages.error(request, f'В имени файла нет слова ON, а вы пытаетесь добавить в "ON" БД')
#                     return redirect('import-xlsx')
#                 aux = []
#                 for item in data_list:
#                     obj = ImportInternetNachisleniyaON(FAO=item[0], dogowor=item[1], login=item[2], price=item[3], etrap=item[4], year=item[5], month=item[6])
#                     aux.append(obj)
#                 ImportInternetNachisleniyaON.objects.bulk_create(aux)
#             else:
#                 if 'OFF' not in str(xlsx_data):
#                     messages.error(request, f'В имени файла нет слова OFF, а вы пытаетесь добавить в "OFF" БД')
#                     return redirect('import-xlsx')
#                 aux = []
#                 for item in data_list:
#                     obj = ImportInternetNachisleniyaOFF(FAO=item[0], dogowor=item[1], login=item[2], price=item[3], etrap=item[4], year=item[5], month=item[6])
#                     aux.append(obj)
#                 ImportInternetNachisleniyaOFF.objects.bulk_create(aux)

            
#             DontRepeatYourself.objects.create(internetNachisleniyaXlsxName=str(xlsx_data))

#             StaffAction.objects.create(user=request.user, comment=f'{request.POST.get("comment")} \n\nДабавления данных с xlsx файла в БД \n\nНазвание файла: {str(xlsx_data)}', action='Импорт с xlsx Интернет Начисления в БД')

#             messages.success(request, f'Успешное добавление данных, файл: {xlsx_data}. Успешных: {success_count}, Ошибок: {lenErrorPrice} (где сумма <= 0)')
#             return redirect('import-xlsx')
        
#         # Проверка данных
#         else:
#             something_with_dogowor = []
#             something_with_login = []
#             something_with_price = []
#             something_with_etrap = []
#             something_with_FAO = []
#             something_with_month = []
#             something_with_year = []

#             lessThanNull = []

#             lenSuccess = 0

#             total_sum = 0
#             for data in imported_data:
#                 if len(data) != 7:
#                     print(data)
#                 else:
#                     pass
#                 if len(data) != 7:
#                     messages.error(request, f'Ошибка! столбцов должно быть 7; 1)Ф.И.О, 2)№ договора, 3)логин, 4)Платеж, 5)Этрап, 6)Год, 7)Месяц')
#                     return redirect('import-xlsx')
                
#                 # Проверка Месяца
#                 if data[6] not in months:
#                     something_with_month.append(data)
#                     continue

#                 # Проверка года
#                 try:
#                     int(data[5])
#                     if len(str(data[5])) != 4:
#                         something_with_year.append(data)
#                         continue
#                 except:
#                     something_with_year.append(data)
#                     continue

#                 # в оплате может быть дата
#                 try:
#                     price = float(data[3].replace(",", "."))
#                 except:
#                     try:
#                         price = float(data[3])
#                     except:
#                         try:
#                             if (str(data[3])[8:10] == '01'):
#                                 monthPrice = int(str(data[3])[5:7])
#                                 yearPrice = str(data[3])[2:4]
#                                 price = float(f"{monthPrice}.{yearPrice}")
#                             elif (str(data[3])[8:10] != '01'):
#                                 dayPrice = int(str(data[3])[8:10])
#                                 monthPrice = str(data[3])[5:7]
#                                 price = float(f"{dayPrice}.{monthPrice}")
#                         except:
#                             something_with_price.append(data)
#                             continue

#                 total_sum += price

#                 # Если оплата нули или отрицательные то next
#                 if price < 0:
#                     lessThanNull.append(data)
#                     continue


#                 # Если в договоре есть буквы то upperCase()
#                 try:
#                     dogowor = int(data[1])
#                 except:
#                     try:
#                         dogowor = data[1].lstrip().rstrip().upper()
#                     except:
#                         something_with_dogowor.append(data)
#                         continue


#                 # Если в логине есть буквы то lowerCase()
#                 try:
#                     login = int(data[2])
#                 except:
#                     try:
#                         login = data[2].lstrip().rstrip().lower()
#                     except:
#                         something_with_login.append(data)
#                         continue

#                 if data[4] not in etraps:
#                     something_with_etrap.append(data)
#                     continue

#                 # Проверка Ф.И.О
#                 if data[0] == None:
#                     something_with_FAO.append(data)
#                     continue

#                 lenSuccess += 1

#             if something_with_dogowor:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "№ Договора"')
#                 context['errors'] = something_with_dogowor
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
            
#             if something_with_login:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Логин"')
#                 context['errors'] = something_with_login
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)

#             if something_with_price:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "сумма платежа"')
#                 context['errors'] = something_with_price
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
            
#             if something_with_etrap:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Этрап": Должно быть один из этих вариантов {etraps}')
#                 context['errors'] = something_with_etrap
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
            
#             if something_with_month:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Месяц": Должно быть один из этих вариантов {months}')
#                 context['errors'] = something_with_month
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
            
#             if something_with_year:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Год"')
#                 context['errors'] = something_with_year
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
            
#             if something_with_FAO and lessThanNull:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Ф.И.О" и в "Сумма платежа". Успешных: {lenSuccess}, Ошибок: {len(something_with_FAO) + len(lessThanNull)}, Общая сумма: {"%.2f" % total_sum} manat')
#                 context['something_with_FAOandlessThanNull'] = True
#                 context['errors'] = list(chain(something_with_FAO, lessThanNull))
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
            
#             if something_with_FAO:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Ф.И.О". Успешных: {lenSuccess}, Ошибок: {len(something_with_FAO)}, Общая сумма: {"%.2f" % total_sum} manat')
#                 context['something_with_FAO'] = True
#                 context['errors'] = something_with_FAO
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
 
            
#             if lessThanNull:
#                 messages.success(request, f'Ошибка! Файл: {xlsx_data} в колонке "Сумма Платежа". Успешных: {lenSuccess}, Ошибок: {len(lessThanNull)}, Общая сумма: {"%.2f" % total_sum} manat')
          
#                 context['errors'] = lessThanNull
#                 context['lessThanNull'] = True
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/InternetNachisleniyaErrors.html', context)
            
#             messages.success(request, f'Проверка Файла прошла успешно. {len(imported_data)} Платежей. Файл: {xlsx_data}, Общая сумма: {"%.2f" % total_sum} manat')
       

#     """##############################################################
#         Если нажал на добавить/проверить в Интернет Начисления END ##
#     """##############################################################

#     """######################################################
#         Если нажал на добавить/проверить в Alem Начисления ##
#     """######################################################

#     if request.method == 'POST' and 'alemNachisleniya' in request.POST:
#         dataset = Dataset()
#         # Если файл не выбран то ошибка
#         try:
#             xlsx_data = request.FILES['my_file3']
#         except:
#             messages.error(request, f'Выберите Файл')
#             return redirect('import-xlsx')
        
#         # если формат не xlsx то Ошибка
#         try:
#             imported_data = dataset.load(xlsx_data.read(), format='xlsx')
#         except:
#             messages.error(request, f'Файл должен быть формата xlsx')
#             return redirect('import-xlsx')


#         if 'alem' not in str(xlsx_data).lower():
#             messages.error(request, f'В файле должен быть слово "alem"')
#             return redirect('import-xlsx')

#         success_count = 0

#         # # Добавление данных в БД
#         if request.POST.get('alemNachisleniyaTest') == None:
#             try:
#                 DontRepeatYourself.objects.get(alemNachisleniyaXlsxName = str(xlsx_data))
#                 messages.error(request, f'ОШИБКА! Файл Уже был добавлен в БД. Файл: {str(xlsx_data)}')
#                 return redirect('import-xlsx')
#             except:
#                 pass
            
#             lenErrorPrice = 0
#             data_list = []
#             for data in imported_data:
#                 if len(data) != 7:
#                     messages.error(request, f'Ошибка! столбцов должно быть 7; 1)Ф.И.О, 2)№ договора, 3)логин, 4)Платеж, 5)Этрап, 6)Год, 7)Месяц')
#                     return redirect('import-xlsx')

#                 # в оплате может быть дата
#                 try:
#                     price = float(data[3].replace(",", "."))
#                 except:
#                     try:
#                         price = float(data[3])
#                     except:
#                         if (str(data[3])[8:10] == '01'):
#                             monthPrice = int(str(data[3])[5:7])
#                             yearPrice = str(data[3])[2:4]
#                             price = float(f"{monthPrice}.{yearPrice}")
#                         elif (str(data[3])[8:10] != '01'):
#                             dayPrice = int(str(data[3])[8:10])
#                             monthPrice = str(data[3])[5:7]
#                             price = float(f"{dayPrice}.{monthPrice}")
                
#                 # Если цена меньше или равен 0 next
#                 if price <= 0:
#                     lenErrorPrice += 1
#                     continue

#                 month = data[6]
#                 year = str(data[5])
                
#                 # Если в договоре есть буквы то upperCase()
#                 try:
#                     dogowor = int(data[1])
#                 except:
#                     dogowor = data[1].lstrip().rstrip().upper()

#                 # Если в логине есть буквы то lowerCase()
#                 try:
#                     login = int(data[2])
#                 except:
#                     login = data[2].lstrip().rstrip().lower()

#                 if data[0] == None:
#                     FAO = ''
#                 else:
#                     FAO = data[0]
#                 # список для bulk_create 
#                 data_list.append([FAO, dogowor, login, price, data[4], year, month])
#                 success_count += 1

#             # bulk_create
#             if request.POST.get('off') == None :
#                 if 'ON' not in str(xlsx_data):
#                     messages.error(request, f'В имени файла нет слова ON, а вы пытаетесь добавить в "ON" БД')
#                     return redirect('import-xlsx')
                
#                 aux = []
#                 for item in data_list:
#                     obj = ImportAlemNachisleniyaON(FAO=item[0], dogowor=item[1], login=item[2], price=item[3], etrap=item[4], year=item[5], month=item[6])
#                     aux.append(obj)
#                 ImportAlemNachisleniyaON.objects.bulk_create(aux)
#             else:
#                 if 'OFF' not in str(xlsx_data):
#                     messages.error(request, f'В имени файла нет слова OFF, а вы пытаетесь добавить в "OFF" БД')
#                     return redirect('import-xlsx')
#                 aux = []
#                 for item in data_list:
#                     obj = ImportAlemNachisleniyaOFF(FAO=item[0], dogowor=item[1], login=item[2], price=item[3], etrap=item[4], year=item[5], month=item[6])
#                     aux.append(obj)
#                 ImportAlemNachisleniyaOFF.objects.bulk_create(aux)

            
#             DontRepeatYourself.objects.create(alemNachisleniyaXlsxName=str(xlsx_data))

#             StaffAction.objects.create(user=request.user, comment=f'Дабавления данных с xlsx файла в БД \n\nНазвание файла: {str(xlsx_data)}', action='Импорт с xlsx Alem Начисления в БД')

#             messages.success(request, f'Успешное добавление данных, файл: {xlsx_data}. Успешных: {success_count}, Ошибок: {lenErrorPrice} (где сумма <= 0)')
      
#             return redirect('import-xlsx')
        
#         # Проверка данных
#         else:
#             something_with_dogowor = []
#             something_with_login = []
#             something_with_price = []
#             something_with_etrap = []
#             something_with_FAO = []
#             something_with_month = []
#             something_with_year = []

#             lessThanNull = []

#             lenSuccess = 0

#             total_sum = 0
#             for data in imported_data:
#                 if len(data) != 7:
#                     messages.error(request, f'Ошибка! столбцов должно быть 7; 1)Ф.И.О, 2)№ договора, 3)логин, 4)Платеж, 5)Этрап, 6)Год, 7)Месяц')
#                     return redirect('import-xlsx')
                
#                 # Проверка Месяца
#                 if data[6] not in months:
#                     something_with_month.append(data)
#                     continue

#                 # Проверка года
#                 try:
#                     int(data[5])
#                     if len(str(data[5])) != 4:
#                         something_with_year.append(data)
#                         continue
#                 except:
#                     something_with_year.append(data)
#                     continue

                
#                 # в оплате может быть дата
#                 try:
#                     price = float(data[3].replace(",", "."))
#                 except:
#                     try:
#                         price = float(data[3])
#                     except:
#                         try:
#                             if (str(data[3])[8:10] == '01'):
#                                 monthPrice = int(str(data[3])[5:7])
#                                 yearPrice = str(data[3])[2:4]
#                                 price = float(f"{monthPrice}.{yearPrice}")
#                             elif (str(data[3])[8:10] != '01'):
#                                 dayPrice = int(str(data[3])[8:10])
#                                 monthPrice = str(data[3])[5:7]
#                                 price = float(f"{dayPrice}.{monthPrice}")
#                         except:
#                             something_with_price.append(data)
#                             continue

#                 total_sum += price

#                 # Если оплата нули или отрицательные то next
#                 if price <= 0:
#                     lessThanNull.append(data)
#                     continue


#                 # Если в договоре есть буквы то upperCase()
#                 try:
#                     dogowor = int(data[1])
#                 except:
#                     try:
#                         dogowor = data[1].lstrip().rstrip().upper()
#                     except:
#                         something_with_dogowor.append(data)
#                         continue


#                 # Если в логине есть буквы то lowerCase()
#                 try:
#                     login = int(data[2])
#                 except:
#                     try:
#                         login = data[2].lstrip().rstrip().lower()
#                     except:
#                         something_with_login.append(data)
#                         continue

#                 if data[4] not in etraps:
#                     something_with_etrap.append(data)
#                     continue

#                 # Проверка Ф.И.О
#                 if data[0] == None:
#                     something_with_FAO.append(data)
#                     continue

#                 lenSuccess += 1

#             if something_with_dogowor:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "№ Договора"')
#                 context['errors'] = something_with_dogowor
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
            
#             if something_with_login:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Логин"')
#                 context['errors'] = something_with_login
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)

#             if something_with_price:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "сумма платежа"')
#                 context['errors'] = something_with_price
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
            
#             if something_with_etrap:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Этрап": Должно быть один из этих вариантов {etraps}')
#                 context['errors'] = something_with_etrap
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
            
#             if something_with_month:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Месяц": Должно быть один из этих вариантов {months}')
#                 context['errors'] = something_with_month
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
            
#             if something_with_year:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Год"')
#                 context['errors'] = something_with_year
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
            
#             if something_with_FAO and lessThanNull:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Ф.И.О" и в "Сумма платежа". Успешных: {lenSuccess}, Ошибок: {len(something_with_FAO) + len(lessThanNull)}, Общая сумма: {"%.2f" % total_sum} manat')
#                 context['something_with_FAOandlessThanNull'] = True
#                 context['errors'] = list(chain(something_with_FAO, lessThanNull))
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
            
#             if something_with_FAO:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data} в колонке "Ф.И.О". Успешных: {lenSuccess}, Ошибок: {len(something_with_FAO)}, Общая сумма: {"%.2f" % total_sum} manat')
#                 context['something_with_FAO'] = True
#                 context['errors'] = something_with_FAO
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
 
            
#             if lessThanNull:
#                 messages.success(request, f'Ошибка! Файл: {xlsx_data} в колонке "Сумма Платежа". Успешных: {lenSuccess}, Ошибок: {len(lessThanNull)}, Общая сумма: {"%.2f" % total_sum} manat')
      
#                 context['errors'] = lessThanNull
#                 context['lessThanNull'] = True
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/alemNachisleniyaErrors.html', context)
            
#             messages.success(request, f'Проверка Файла прошла успешно. {len(imported_data)} Платежей. Файл: {xlsx_data}, Общая сумма: {"%.2f" % total_sum} manat')
     

#     """##########################################################
#         Если нажал на добавить/проверить в Alem Начисления END ##
#     """##########################################################


#     if request.method == 'POST' and 'platejiSbillinga' in request.POST:
#         dataset = Dataset()
#         # Если файл не выбран то ошибка
#         try:
#             xlsx_data = request.FILES['my_file4']
#         except:
#             messages.error(request, f'Выберите Файл')
#             return redirect('import-xlsx')
        
#         # если формат не xlsx то Ошибка
#         try:
#             imported_data = dataset.load(xlsx_data.read(), format='xlsx')
#         except:
#             messages.error(request, f'Файл должен быть формата xlsx')
#             return redirect('import-xlsx')


#         if 'billingplateji' not in str(xlsx_data).lower():
#             messages.error(request, f'В файле должен быть слово "billingplateji"')
#             return redirect('import-xlsx')
#         count = 0
#         # 2=type_pay (Внешние пл., default, оплата с картой), 3=manager, 6=datePlatej, 11=dogowor, 12=FIO, 13=yurOrFiz 14=price
        
#         errorDict = {} # {row: [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]}
#         if request.POST.get('platejiSbillingaTest') == None:
#             total_sum = 0
#             total_date_sum = 0
#             bulk_create_list = []
#             onOF = request.POST.get('off') # None или 'on'
#             for d in imported_data:
                
#                 if d[10]:
#                     kod_oplaty = d[10]
#                 else:
#                     kod_oplaty = ''
#                 str_date = ''

#                 count += 1
#                 if count >= 8:   
#                     manager = d[3]
#                     date_ = d[6]
#                     dogowor= d[11]
#                     fio = d[12]
#                     price = d[14]
#                     if d[10]:
#                         kod_oplaty = d[10]
#                     else:
#                         kod_oplaty = ''
#                     type_pay = d[2].strip()
#                     yurOrFiz = d[13].strip()
#                     if dogowor == None:
#                         errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
#                         continue
#                     elif date_ == None:
#                         errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
#                         continue
#                     elif manager == None:
#                         errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
#                         continue
#                     elif price == None:
#                         errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
#                         continue
#                     elif isinstance(price, (date, datetime)):
#                             str_date = str(price)
#                             if str_date[8:10] == '01':
#                                 manat = str_date[5:7]
#                                 tenne = str_date[2:4]
#                                 price = float(f"{manat}.{tenne}")
#                             else:
#                                 manat = str_date[8:10]
#                                 tenne = str_date[5:7]
#                                 price = float(f"{manat}.{tenne}")
#                             total_date_sum += price
#                     total_sum += float(price)
#                     if onOF:
#                         obj = MonthPlatejiOFFFromBilling(platejiType=type_pay, manager=manager, pay_date=date_, dogowor=dogowor, price=price, date_price=str_date, kod_oplaty=kod_oplaty, FAO=fio, YurOrFiz=yurOrFiz)
#                     else:
#                         obj = MonthPlatejiFromBilling(platejiType=type_pay, manager=manager, pay_date=date_, dogowor=dogowor, price=price, date_price=str_date, kod_oplaty=kod_oplaty, FAO=fio, YurOrFiz=yurOrFiz)     
#                     bulk_create_list.append(obj)
#             if errorDict:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data}')
#                 context['errorDict'] = errorDict
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/billingPlatejiErrors.html', context)
#             else:
#                 if bulk_create_list:
#                     if onOF: 
#                         MonthPlatejiOFFFromBilling.objects.bulk_create(bulk_create_list)
#                         messages.success(request, f'Добавлено успешно. Файл: {xlsx_data}, Общая сумма: {"%.2f" % total_sum} manat, количество платежей {count-7}')
            
#                     else:
#                         MonthPlatejiFromBilling.objects.bulk_create(bulk_create_list)
#                         messages.success(request, f'Добавлено успешно. Файл: {xlsx_data}, Общая сумма: {"%.2f" % total_sum} manat, количество платежей {count-7}')
                    
                        
#         else:
#             # 3=manager, 6=datePlatej, 11=dogowor, 12=FIO, 14=price
#             total_sum = 0
#             total_date_sum = 0
#             for d in imported_data:

#                 count += 1
#                 if count >= 8:
#                     manager = d[3]
#                     date_ = d[6]
#                     dogowor= d[11]
#                     fio = d[12]
#                     price = d[14]
#                     kod_oplaty = d[10]
#                     type_pay = d[2].strip()
#                     yurOrFiz = d[13].strip()  
#                     if dogowor == None:
#                         errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
#                         continue
#                     elif date_ == None:
#                         errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
#                         continue
#                     elif manager == None:
#                         errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
#                         continue
#                     elif price == None:
#                         errorDict[count] = [type_pay, manager, date_, dogowor, fio, yurOrFiz, price]
#                         continue
#                     elif isinstance(price, (date, datetime)):
#                             str_date = str(price)
#                             if str_date[8:10] == '01':
#                                 manat = str_date[5:7]
#                                 tenne = str_date[2:4]
#                                 price = float(f"{manat}.{tenne}")
#                             else:
#                                 manat = str_date[8:10]
#                                 tenne = str_date[5:7]
#                                 price = float(f"{manat}.{tenne}")
#                             total_date_sum += price
#                     total_sum += float(price)
#             if errorDict:
#                 messages.error(request, f'Ошибка! Файл: {xlsx_data}')
#                 context['errorDict'] = errorDict
#                 return render(request, 'telekom/MATB/xlsx/importXlsx/xlsxErrors/billingPlatejiErrors.html', context)
#             else:
#                 messages.success(request, f'Проверка Файла прошла успешно. {count-7} Платежей. Файл: {xlsx_data}, Общая сумма: {"%.2f" % total_sum} manat')
       
#                 print('total_date_sum', total_date_sum)




#     return render(request, 'telekom/MATB/xlsx/importXlsx/importXlsx.html', context)