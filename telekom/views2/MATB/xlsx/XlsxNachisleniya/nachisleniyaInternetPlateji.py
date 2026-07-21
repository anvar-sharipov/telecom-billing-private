from django.shortcuts import render, redirect
from django.contrib import messages

from calendar import monthrange
# Для создание даты и времени в формате DateTime
from datetime import date, time, datetime
from telekom.models import DontRepeatYourself, ImportInternetPlateji, ImportInternetPlatejiOFF, NachisleniyaOtchet, OldLoginDogowor, PayHistory, StaffAction, UserTable

# https://metanit.com/python/django/5.5.php
# Для update
from django.db.models import F


from telekom.views2.myFunc.myFunc import getEtrapCode, loggedUserEtrapAndGroup, monthСonvert

def nachisleniyaInternetPlateji(request):
    if not request.user.is_superuser and request.user.username != 'admin1':
        messages.error(request, f'Доступ только Администратору')
        return redirect('user-login')

    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    context = {}
    context['matbIndex'] = True
    context['nachisleniyaInternetPlateji'] = True

    # log = getLoggedUserEtrap(request.user.username)
    context['log'] = log
    context['etrap'] = request.GET.get('etrap')

    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date

    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']
    context['etraps'] = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

    context['get_month'] = request.GET.get('month')
    context['get_year'] = request.GET.get('year')

    off = request.GET.get('off')

    month_word = request.GET.get('month')
    year = request.GET.get('year')
    month_numb = monthСonvert(month_word)
    etrap = request.GET.get('etrap')
    context['off'] = True if request.GET.get('off') != None else False

    if month_word == '':
        messages.error(request, f'Ошибка! Выберите месяц начисления')
        return redirect('nachisleniya-internet-plateji')


    if month_numb and year:
        days_in_nach_month = monthrange(int(year), int(month_numb))[1]

        first = f"{year}-{month_numb}-01"
        last = f"{year}-{month_numb}-{days_in_nach_month}"

        if etrap == 'all':
            if request.GET.get('off') == None:
                internetPlateji = ImportInternetPlateji.objects.filter(pay_date__range=[first, last])
                 # Были ли частичные начисления (другие этрапы)
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allON")
                    context['alreadyNach'] = True
                except:
                    pass
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzON")
                    Dashoguz = 'Dashoguz'
                except:
                    Dashoguz = ''
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeON")
                    Akdepe = 'Akdepe'
                except:
                    Akdepe = ''
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazON")
                    Boldumsaz = 'Boldumsaz'
                except:
                    Boldumsaz = ''
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyON")
                    Gorogly = 'Gorogly'
                except:
                    Gorogly = ''
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchON")
                    Koneurgench = 'Koneurgench'
                except:
                    Koneurgench = ''
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyON")
                    Turkmenbashy = 'Turkmenbashy'
                except:
                    Turkmenbashy = ''
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowON")
                    Nyyazow = 'Nyyazow'
                except:
                    Nyyazow = ''
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentON")
                    Ruhubelent = 'Ruhubelent'
                except:
                    Ruhubelent = ''
                    
                if Dashoguz and Akdepe and Boldumsaz and Gorogly and Koneurgench and Turkmenbashy and Nyyazow and Ruhubelent:
                    context['alreadyallNach'] = True
                elif Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
                    context['alreadySeparateNach'] = True

            else:
                internetPlateji = ImportInternetPlatejiOFF.objects.filter(pay_date__range=[first, last])

                 # Были ли частичные начисления (другие этрапы)
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allOFF")
                    context['alreadyNach'] = True
                except:
                    pass
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzOFF")
                    Dashoguz = 'Dashoguz'
                except:
                    Dashoguz = ''
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeOFF")
                    Akdepe = 'Akdepe'
                except:
                    Akdepe = ''
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazOFF")
                    Boldumsaz = 'Boldumsaz'
                except:
                    Boldumsaz = ''
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyOFF")
                    Gorogly = 'Gorogly'
                except:
                    Gorogly = ''
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchOFF")
                    Koneurgench = 'Koneurgench'
                except:
                    Koneurgench = ''
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyOFF")
                    Turkmenbashy = 'Turkmenbashy'
                except:
                    Turkmenbashy = ''
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowOFF")
                    Nyyazow = 'Nyyazow'
                except:
                    Nyyazow = ''
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentOFF")
                    Ruhubelent = 'Ruhubelent'
                except:
                    Ruhubelent = ''

                if Dashoguz and Akdepe and Boldumsaz and Gorogly and Koneurgench and Turkmenbashy and Nyyazow and Ruhubelent:
                    context['alreadyallNach'] = True
                elif Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
                    context['alreadySeparateNach'] = True

        else:
            if request.GET.get('off') == None:
                internetPlateji = ImportInternetPlateji.objects.filter(pay_date__range=[first, last], etrap=etrap)

                # Проверяем было ли начисление этого QuerySet (для отключения кнопки начислить)
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}ON")
                    context['alreadyNach'] = True
                except:
                    try:
                        DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allON")
                        context['alreadyNach'] = True
                    except:
                        context['alreadyNach'] = False

            else:
                internetPlateji = ImportInternetPlatejiOFF.objects.filter(pay_date__range=[first, last], etrap=etrap)


                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}OFF")
                    context['alreadyNach'] = True
                except:
                    try:
                        DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allOFF")
                        context['alreadyNach'] = True
                    except:
                        context['alreadyNach'] = False
        if len(internetPlateji) == 0:
            context['nothingNach'] = True


        
        UserTableDog = []

        if etrap == 'all':
            get_dogoworsBD = UserTable.objects.values('dogowor')
        else:
            get_dogoworsBD = UserTable.objects.filter(etrap=etrap).values('dogowor')

        for i in get_dogoworsBD:
            for key, value in i.items():
                if value != '':
                    UserTableDog.append(''.join(value).upper())               

        UserNumberEtrap = []

        if etrap == 'all':
            UserNumberEtrapObj = UserTable.objects.values('number', 'etrap')
        else:
            UserNumberEtrapObj = UserTable.objects.filter(etrap=etrap).values('number', 'etrap')

        for item in UserNumberEtrapObj:
            numberEtrap = ''
            for key, value in item.items():
                # 91456Dashoguz
                numberEtrap += value
            UserNumberEtrap.append(numberEtrap)

        ###
        oldLoginsDogowors = OldLoginDogowor.objects.all()
        old_dogowors = {}
        etrapNumberDogowors = {}
        for logDog in oldLoginsDogowors:
            if logDog.dogowor:
                old_dogowors[logDog.dogowor] = [logDog.etrap, logDog.number]
            if f"{logDog.etrap}{logDog.number}" not in etrapNumberDogowors:
                etrapNumberDogowors[f"{logDog.etrap}{logDog.number}"] = [logDog.dogowor]
            else:
                etrapNumberDogowors[f"{logDog.etrap}{logDog.number}"].append([logDog.dogowor])

        platejiOldDog = {}
        platejiOldDogPayCount = 0
        platejiOldDogPayTotalPrice = 0

        ####

        PlatejiDog = {}
        platejiDogoworPayCount = 0
        platejiDogoworTotalPrice = 0

        PlatejiDogError = {}
        platejiErrorDogoworPayCount = 0
        platejiErrorDogoworTotalPrice = 0

        PlatejiTelefon = {}
        platejiTelefonPayCount = 0
        platejiTelefonTotalPrice = 0

        PlatejiTelefonError = {}
        platejiErrorTelefonPayCount = 0
        platejiErrorTelefonTotalPrice = 0

        PlatejiAlem = {}
        platejiAlemPayCount = 0
        platejiAlemTotalPrice = 0

        PlatejiAlemError = {}
        platejiErrorAlemPayCount = 0
        platejiErrorAlemTotalPrice = 0

        
        for pay in internetPlateji:
            try:
                dogoworTelefon = int(pay.dogowor)       
            except:
                dogoworTelefon = None


            # abonplata
            if dogoworTelefon:
                # f"{pay.dogowor[6:]}{pay.etrap}"
                if pay.dogowor not in PlatejiTelefon and f"{pay.dogowor[6:]}{pay.etrap}" in UserNumberEtrap:
                    PlatejiTelefon[pay.dogowor] = [pay.type, pay.pay_date, pay.FAO, pay.price, pay.etrap]
                    platejiTelefonPayCount += 1
                    platejiTelefonTotalPrice += pay.price
                elif pay.dogowor in PlatejiTelefon and f"{pay.dogowor[6:]}{pay.etrap}" in UserNumberEtrap:
                    PlatejiTelefon[pay.dogowor][3] += pay.price
                    platejiTelefonPayCount += 1 
                    platejiTelefonTotalPrice += pay.price
                elif pay.dogowor not in PlatejiTelefonError and f"{pay.dogowor[6:]}{pay.etrap}" not in UserNumberEtrap:
                    PlatejiTelefonError[pay.dogowor] = [pay.type, pay.pay_date, pay.FAO, pay.price, pay.etrap]
                    platejiErrorTelefonPayCount += 1
                    platejiErrorTelefonTotalPrice += pay.price
                elif pay.dogowor in PlatejiTelefonError and f"{pay.dogowor[6:]}{pay.etrap}" not in UserNumberEtrap:
                    PlatejiTelefonError[pay.dogowor][3] += pay.price
                    platejiErrorTelefonPayCount += 1
                    platejiErrorTelefonTotalPrice += pay.price
                continue  
        
            # alem plata
            if pay.dogowor[:4] == 'IPTV':
                if pay.dogowor not in PlatejiAlem and f"{pay.dogowor[11:]}{pay.etrap}" in UserNumberEtrap:
                    PlatejiAlem[pay.dogowor] = [pay.type, pay.pay_date, pay.FAO, pay.price, pay.etrap]
                    platejiAlemPayCount += 1
                    platejiAlemTotalPrice += pay.price
                elif pay.dogowor in PlatejiAlem and f"{pay.dogowor[11:]}{pay.etrap}" in UserNumberEtrap:
                    PlatejiAlem[pay.dogowor][3] += pay.price
                    platejiAlemPayCount += 1
                    platejiAlemTotalPrice += pay.price
                elif pay.dogowor not in PlatejiAlemError and f"{pay.dogowor[11:]}{pay.etrap}" not in UserNumberEtrap:
                    PlatejiAlemError[pay.dogowor] = [pay.type, pay.pay_date, pay.FAO, pay.price, pay.etrap]
                    platejiErrorAlemPayCount += 1
                    platejiErrorAlemTotalPrice += pay.price
                elif pay.dogowor in PlatejiAlemError and f"{pay.dogowor[11:]}{pay.etrap}" not in UserNumberEtrap:
                    PlatejiAlemError[pay.dogowor][3] += pay.price
                    platejiErrorAlemPayCount += 1
                    platejiErrorAlemTotalPrice += pay.price
                continue

            # internet plateji через dogowor
            if pay.dogowor not in PlatejiDog and pay.dogowor in UserTableDog:
                PlatejiDog[pay.dogowor] = [pay.type, pay.pay_date, pay.FAO, pay.price, pay.etrap]
                platejiDogoworPayCount += 1
                platejiDogoworTotalPrice += pay.price
            elif pay.dogowor in PlatejiDog and pay.dogowor in UserTableDog:
                PlatejiDog[pay.dogowor][3] += pay.price
                platejiDogoworPayCount += 1
                platejiDogoworTotalPrice += pay.price
            ### поиск договоров в OldLoginDogowor которых нет в UserTable
            elif pay.dogowor not in platejiOldDog and pay.dogowor in old_dogowors:
                platejiOldDog[pay.dogowor] = [pay.type, pay.pay_date, pay.FAO, pay.price, pay.etrap]
                platejiOldDogPayCount += 1
                platejiOldDogPayTotalPrice += pay.price
            elif pay.dogowor in platejiOldDog and pay.dogowor in old_dogowors:
                platejiOldDog[pay.dogowor][3] += pay.price
                platejiOldDogPayCount += 1
                platejiOldDogPayTotalPrice += pay.price
            ####
            elif pay.dogowor not in PlatejiDogError and pay.dogowor not in UserTableDog:
                PlatejiDogError[pay.dogowor] = [pay.type, pay.pay_date, pay.FAO, pay.price, pay.etrap]
                platejiErrorDogoworPayCount += 1
                platejiErrorDogoworTotalPrice += pay.price
            elif pay.dogowor in PlatejiDogError and pay.dogowor not in UserTableDog:
                PlatejiDogError[pay.dogowor][3] += pay.price
                platejiErrorDogoworPayCount += 1
                platejiErrorDogoworTotalPrice += pay.price


        # Инфа об платежах интернета если в договоре не одни цыфры и нет подтекста 'IPTV'
        context['PlatejiDogCount'] = len(PlatejiDog) + len(platejiOldDog)
        context['platejiDogoworPayCount'] = platejiDogoworPayCount + platejiOldDogPayCount
        context['platejiDogoworTotalPrice'] = platejiDogoworTotalPrice + platejiOldDogPayTotalPrice

        context['PlatejiDogError'] = len(PlatejiDogError)
        context['platejiErrorDogoworPayCount'] = platejiErrorDogoworPayCount
        context['platejiErrorDogoworTotalPrice'] = platejiErrorDogoworTotalPrice

        ###
        context['platejiOldDogCount'] = len(platejiOldDog)
        context['platejiOldDogPayCount'] = platejiOldDogPayCount
        context['platejiOldDogPayTotalPrice'] = platejiOldDogPayTotalPrice
        ####


        # Инфа об абонплатах если в договоре только одни цифры
        context['PlatejiTelefon'] = len(PlatejiTelefon)
        context['platejiTelefonPayCount'] = platejiTelefonPayCount
        context['platejiTelefonTotalPrice'] = platejiTelefonTotalPrice

        context['PlatejiTelefonError'] = len(PlatejiTelefonError)
        context['platejiErrorTelefonPayCount'] = platejiErrorTelefonPayCount
        context['platejiErrorTelefonTotalPrice'] = platejiErrorTelefonTotalPrice

        # Инфа об платежах Alem TV если в договоре есть подтекст 'IPTV'
        context['PlatejiAlem'] = len(PlatejiAlem)
        context['platejiAlemPayCount'] = platejiAlemPayCount
        context['platejiAlemTotalPrice'] = platejiAlemTotalPrice

        context['PlatejiAlemError'] = len(PlatejiAlemError)
        context['platejiErrorAlemPayCount'] = platejiErrorAlemPayCount
        context['platejiErrorAlemTotalPrice'] = platejiErrorAlemTotalPrice

        # Общая информация об успешных платежах
        context['TotalSuccessPayCount'] = platejiDogoworPayCount + platejiTelefonPayCount + platejiAlemPayCount + platejiOldDogPayCount
        context['TotalSuccessPayPrice'] = platejiDogoworTotalPrice + platejiTelefonTotalPrice + platejiAlemTotalPrice + platejiOldDogPayTotalPrice
        context['TotalSuccessAbonentCount'] = len(PlatejiDog) + len(PlatejiTelefon) + len(PlatejiAlem) + len(platejiOldDog)

        # Общая информация об ошибках
        context['TotalErrorPayCount'] = platejiErrorDogoworPayCount + platejiErrorTelefonPayCount + platejiErrorAlemPayCount
        context['TotalErrorPayPrice'] = platejiErrorDogoworTotalPrice + platejiErrorTelefonTotalPrice + platejiErrorAlemTotalPrice
        context['TotalErrorAbonentCount'] = len(PlatejiDogError) + len(PlatejiTelefonError) + len(PlatejiAlemError)
        


        # Общая информация за весь месяц платежах (тут и ошибки и успешные платежи)
        #  для Абонплаты
        context['totalAbonplataPayCount'] = platejiTelefonPayCount + platejiErrorTelefonPayCount
        context['totalAbonplataAbonentCount'] = len(PlatejiTelefon) + len(PlatejiTelefonError)
        context['totalAbonplataPrice'] = platejiTelefonTotalPrice + platejiErrorTelefonTotalPrice
        # для Alem TV
        context['totalAlemPayCount'] = platejiAlemPayCount + platejiErrorAlemPayCount
        context['totalAlemAbonentCount'] = len(PlatejiAlem) + len(PlatejiAlemError)
        context['totalAlemPrice'] = platejiAlemTotalPrice + platejiErrorAlemTotalPrice
        # для Интернета
        context['totalInternetPayCount'] = platejiDogoworPayCount + platejiErrorDogoworPayCount + platejiOldDogPayCount
        context['totalInternetAbonentCount'] = len(PlatejiDog) + len(PlatejiDogError) + len(platejiOldDog)
        context['totalInternetPrice'] = platejiDogoworTotalPrice + platejiErrorDogoworTotalPrice + platejiOldDogPayTotalPrice
        # Вся инфа за весь месяц
        context['TotalPayCount'] = platejiDogoworPayCount + platejiTelefonPayCount + platejiAlemPayCount + platejiErrorDogoworPayCount + platejiErrorTelefonPayCount + platejiErrorAlemPayCount + platejiOldDogPayCount
        context['TotalPayPrice'] = platejiDogoworTotalPrice + platejiTelefonTotalPrice + platejiAlemTotalPrice + platejiErrorDogoworTotalPrice + platejiErrorTelefonTotalPrice + platejiErrorAlemTotalPrice + platejiOldDogPayTotalPrice
        context['TotalAbonentCount'] = len(PlatejiDog) + len(PlatejiTelefon) + len(PlatejiAlem) + len(PlatejiDogError) + len(PlatejiTelefonError) + len(PlatejiAlemError) + len(platejiOldDog)
        

    # Если нажал на начислить
    if request.method == 'POST' and 'comment' in request.POST:
        if etrap != 'all':
            if off == None:
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allON")
                    messages.error(request, f'Ошибка за месяц {month_word} {year} года было начислены все Этрапы интернет платежей ON')
                    return redirect(request.POST.get('url_from'))
                except:
                    pass
            else:
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allOFF")
                    messages.error(request, f'Ошибка за месяц {month_word} {year} года было начислены все Этрапы интернет платежей OFF')
                    return redirect(request.POST.get('url_from'))
                except:
                    pass
        else:
            if off == None:
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzON")
                    Dashoguz = 'Dashoguz'
                except:
                    Dashoguz = ''

                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeON")
                    Akdepe = 'Akdepe'
                except:
                    Akdepe = ''

                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazON")
                    Boldumsaz = 'Boldumsaz'
                except:
                    Boldumsaz = ''

                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyON")
                    Gorogly = 'Gorogly'
                except:
                    Gorogly = ''

                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchON")
                    Koneurgench = 'Koneurgench'
                except:
                    Koneurgench = ''

                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyON")
                    Turkmenbashy = 'Turkmenbashy'
                except:
                    Turkmenbashy = ''

                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowON")
                    Nyyazow = 'Nyyazow'
                except:
                    Nyyazow = ''

                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentON")
                    Ruhubelent = 'Ruhubelent'
                except:
                    Ruhubelent = ''

                if Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
                    messages.error(request, f'Ошибка за месяц {month_word} {year} Вы не можете начислить ON на все этрапы так как некоторые этрапы уже начислили ({Dashoguz} {Akdepe} {Boldumsaz} {Gorogly} {Koneurgench} {Turkmenbashy} {Nyyazow} {Ruhubelent})')
                    return redirect(request.POST.get('url_from'))
            else:
                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzOFF")
                    Dashoguz = 'Dashoguz'
                except:
                    Dashoguz = ''

                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeOFF")
                    Akdepe = 'Akdepe'
                except:
                    Akdepe = ''

                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazOFF")
                    Boldumsaz = 'Boldumsaz'
                except:
                    Boldumsaz = ''

                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyOFF")
                    Gorogly = 'Gorogly'
                except:
                    Gorogly = ''

                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchOFF")
                    Koneurgench = 'Koneurgench'
                except:
                    Koneurgench = ''

                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyOFF")
                    Turkmenbashy = 'Turkmenbashy'
                except:
                    Turkmenbashy = ''

                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowOFF")
                    Nyyazow = 'Nyyazow'
                except:
                    Nyyazow = ''

                try:
                    DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentOFF")
                    Ruhubelent = 'Ruhubelent'
                except:
                    Ruhubelent = ''

                if Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
                    messages.error(request, f'Ошибка за месяц {month_word} {year} Вы не можете начислить OFF на все этрапы так как некоторые этрапы уже начислили ({Dashoguz} {Akdepe} {Boldumsaz} {Gorogly} {Koneurgench} {Turkmenbashy} {Nyyazow} {Ruhubelent})')
                    return redirect(request.POST.get('url_from'))



        try:
            if off == None:
                DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}ON")
                messages.error(request, f'Ошибка за месяц {month_word} {year} года {etrap} начисления интернет платежей ON уже было начислено')
                return redirect(request.POST.get('url_from'))  
            else:
                DontRepeatYourself.objects.get(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}OFF")
                messages.error(request, f'Ошибка за месяц {month_word} {year} года {etrap} начисления интернет платежей OFF уже было начислено')
                return redirect(request.POST.get('url_from'))  
        except:
            pass

        if request.POST.get('comment') == '':
            messages.error(request, f'Комментарий не может быть пустым')  
            return redirect(request.POST.get('url_from'))
        else:
            if PlatejiDog == {} and PlatejiAlem == {} and PlatejiTelefon == {} and platejiOldDog == {}:
                messages.error(request, f'Ошибка! за месяц {month_word} {year} года нет ни одного платежа')
                return redirect(request.POST.get('url_from'))



            if etrap == 'all':
                code = None
            else:
                code = getEtrapCode(etrap)
           
            if etrap == 'all':
                users = UserTable.objects.all()
            else:
                users = UserTable.objects.filter(etrap=request.POST.get('etrap'))

            # Сохранения Интернет платежей

            list_items_create = []
            # Сохранение internet plateji
            for user in users:
                if user.dogowor in PlatejiDog:
                    # UserTable.objects.filter(pk=user.pk).update(b_internet = F('b_internet') + PlatejiDog[user.dogowor][3])
                    user.b_internet += PlatejiDog[user.dogowor][3]
                    list_items_create.append([user, PlatejiDog[user.dogowor][3], PlatejiDog[user.dogowor][0], PlatejiDog[user.dogowor][3], PlatejiDog[user.dogowor][1]])
                    # Сохранения платежей для месячного отчета
                    try:
                        nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=user.etrap, year=str(PlatejiDog[user.dogowor][1])[:4], month=monthСonvert(str(PlatejiDog[user.dogowor][1])[5:7]))
                        nachisleniyaOtchet.WneshniyePlatejiInternet += PlatejiDog[user.dogowor][3]
                        nachisleniyaOtchet.save()
                    except:
                        NachisleniyaOtchet.objects.create(etrap=user.etrap, year=str(PlatejiDog[user.dogowor][1])[:4], month=monthСonvert(str(PlatejiDog[user.dogowor][1])[5:7]), WneshniyePlatejiInternet=PlatejiDog[user.dogowor][3])
                    user.save()
                else:
                    # Начисления платежей по старым договорам (OldLoginDogowor) которые не нашлись в UserTable
                    if f"{user.etrap}{user.number}" in etrapNumberDogowors:
                        for dog in etrapNumberDogowors[f"{user.etrap}{user.number}"]:
                            if dog in platejiOldDog:
                                user.b_internet += platejiOldDog[dog][3]
                                list_items_create.append([user, platejiOldDog[dog][3], platejiOldDog[dog][0], platejiOldDog[dog][3], platejiOldDog[dog][1]])

                                try:
                                    nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=user.etrap, year=str(platejiOldDog[dog][1])[:4], month=monthСonvert(str(platejiOldDog[dog][1])[5:7]))
                                    nachisleniyaOtchet.WneshniyePlatejiInternet += platejiOldDog[dog][3]
                                    nachisleniyaOtchet.save()
                                except:
                                    NachisleniyaOtchet.objects.create(etrap=user.etrap, year=str(platejiOldDog[dog][1])[:4], month=monthСonvert(str(platejiOldDog[dog][1])[5:7]), WneshniyePlatejiInternet=platejiOldDog[dog][3])
                                user.save()
                                continue

          
            aux_create = []
            print('111111111', list_items_create)
            for item in list_items_create:
                obj = PayHistory(abonent=item[0], internet=item[1], kassir=item[2], total=item[3], date=item[4])
                aux_create.append(obj)
            PayHistory.objects.bulk_create(aux_create)

            # Сохранения Alem TV платежей
            list_items_create = []
            for user in users:

                if code:
                    numberStr = f"IPTV-993{code}{user.number}"
                else:
                    userCode = getEtrapCode(user.etrap)
                    numberStr = f"IPTV-993{userCode}{user.number}"

                if numberStr in PlatejiAlem:
                    # UserTable.objects.filter(pk=user.pk).update(b_alem = F('b_alem') + PlatejiAlem[numberStr][3])
                    user.b_alem += PlatejiAlem[numberStr][3]
                    list_items_create.append([user,
                                            PlatejiAlem[numberStr][3], 
                                            PlatejiAlem[numberStr][0], 
                                            PlatejiAlem[numberStr][3], 
                                            PlatejiAlem[numberStr][1]])
                    
                    # Сохранения платежей для месячного отчета
                    try:
                        nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=user.etrap, year=str(PlatejiAlem[numberStr][1])[:4], month=monthСonvert(str(PlatejiAlem[numberStr][1])[5:7]))
                        nachisleniyaOtchet.WneshniyePlatejiAlem += PlatejiAlem[numberStr][3]
                        nachisleniyaOtchet.save()
                    except:
                        NachisleniyaOtchet.objects.create(etrap=user.etrap, year=str(PlatejiAlem[numberStr][1])[:4], month=monthСonvert(str(PlatejiAlem[numberStr][1])[5:7]), WneshniyePlatejiAlem=PlatejiAlem[numberStr][3])
                    user.save()
            aux_create = []
            for item in list_items_create:
                obj = PayHistory(abonent=item[0], alem=item[1], kassir=item[2], total=item[3], date=item[4])
                aux_create.append(obj)
            PayHistory.objects.bulk_create(aux_create)
        


            # Сохранения Abonplat платежей
            list_items_create = []
            for user in users:

                if code:
                    numberStr = f"993{code}{user.number}"
                else:
                    userCode = getEtrapCode(user.etrap)
                    numberStr = f"993{userCode}{user.number}"

                if numberStr in PlatejiTelefon:
                    user.b_prochee += PlatejiTelefon[numberStr][3]
                    user.save()
                                    
                    # Сохранения платежей для месячного отчета
                    try:
                        nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=user.etrap, year=str(PlatejiTelefon[numberStr][1])[:4], month=monthСonvert(str(PlatejiTelefon[numberStr][1])[5:7]))             
                        nachisleniyaOtchet.WneshniyePlatejiAbonplata += PlatejiTelefon[numberStr][3]
                        nachisleniyaOtchet.save()
                    except:
                        NachisleniyaOtchet.objects.create(etrap=user.etrap, year=str(PlatejiTelefon[numberStr][1])[:4], month=monthСonvert(str(PlatejiTelefon[numberStr][1])[5:7]), WneshniyePlatejiAbonplata = PlatejiTelefon[numberStr][3])



                    list_items_create.append([user,
                                            PlatejiTelefon[numberStr][3], 
                                            PlatejiTelefon[numberStr][0], 
                                            PlatejiTelefon[numberStr][1]
                                            ])
                    
            if list_items_create:
                aux_create = []
                for item in list_items_create:
                    obj = PayHistory(
                        abonent=item[0], 
                        kassir=item[2], 
                        total=item[1], 
                        date=item[3], 
                        prochee=item[1]
                        )
                    aux_create.append(obj)
                PayHistory.objects.bulk_create(aux_create)

            if off == None:
                DontRepeatYourself.objects.create(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}ON")  
            else:
                DontRepeatYourself.objects.create(platejiNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}OFF")

            if off == None:
                StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')} \n\n Начисления ON за месяц {month_word} {year} года для этрапа {etrap}", action='Начисления Интернет Платежей')  
            else:
                StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')} \n\n Начисления OFF за месяц {month_word} {year} года для этрапа {etrap}", action='Начисления Интернет Платежей')  

            if off == None:
                messages.success(request, f'Успешное начисления ON для {etrap} - Интернет:{len(PlatejiDog)+len(platejiOldDog)}, Alem TV:{len(PlatejiAlem)}, Абонплата:{len(PlatejiTelefon)} за месяц {month_word} {year} года')  
            else:
                messages.success(request, f'Успешное начисления OFF для {etrap} - Интернет:{len(PlatejiDog)+len(platejiOldDog)}, Alem TV:{len(PlatejiAlem)}, Абонплата:{len(PlatejiTelefon)} за месяц {month_word} {year} года')  
              

            
    return render(request, 'telekom/MATB/xlsx/XlsxNachisleniya/nachisleniyaInternetPlateji.html', context)