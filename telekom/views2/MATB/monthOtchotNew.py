from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.models import MonthBalance, NachisleniyaOtchet, PayHistory, UserTable, UserTableArhiw
from django.db.models import Sum
from django.db.models import Q

from telekom.views2.myFunc.myFunc import getPreviousMonth, loggedUserEtrapAndGroup, monthСonvert

from datetime import date
from calendar import monthrange


def monthOtchotNew(request):
    context = {}
    current_date = str(date.today())
    context['current_date'] = current_date

    current_year = current_date[0:4]

    current_month = current_date[5:7]
    month_word = monthСonvert(current_month)
    days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]

    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
        context['matbIndex'] = True
        context['monthOtchotNew'] = True
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['etraps'] = etraps
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']


    etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else log
    month = request.GET.get('month') if request.GET.get('month') != None else month_word
    year = request.GET.get('year') if request.GET.get('year') != None else current_year
    context['month'] = month
    context['year'] = year
    context['etrap'] = etrap
    days_in_choosed_month = monthrange(int(year), int(monthСonvert(month)))[1]

    users = UserTable.objects.filter(etrap=etrap)
    payHistory = PayHistory.objects.filter(date__range=[f"{year}-{str(monthСonvert(month))}-01 00:00:00", f"{year}-{str(monthСonvert(month))}-{days_in_choosed_month} 23:59:59"], abonent__etrap=etrap)
    try:
        nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=etrap, month=month, year=year)
    except:
        nachisleniyaOtchet = False

    ########### Текущий баланс Плюс (Население) ###########
    abonplataPlus = users.filter(is_enterprises=False, b_telefon__gt=0).aggregate(Sum('b_telefon'))['b_telefon__sum']
    if abonplataPlus == None:
        abonplataPlus = 0
    context['abonplataPlus'] = abonplataPlus

    slrPlus = users.filter(is_enterprises=False, b_slr__gt=0).aggregate(Sum('b_slr'))['b_slr__sum']
    if slrPlus == None:
        slrPlus = 0
    context['slrPlus'] = slrPlus

    kodPlus = users.filter(is_enterprises=False, b_kod__gt=0).aggregate(Sum('b_kod'))['b_kod__sum']
    if kodPlus == None:
        kodPlus = 0
    context['kodPlus'] = kodPlus

    zakazPlus = users.filter(is_enterprises=False, b_zakaz__gt=0).aggregate(Sum('b_zakaz'))['b_zakaz__sum']
    if zakazPlus == None:
        zakazPlus = 0
    context['zakazPlus'] = zakazPlus

    procheePlus = users.filter(is_enterprises=False, b_prochee__gt=0).aggregate(Sum('b_prochee'))['b_prochee__sum']
    if procheePlus == None:
        procheePlus = 0
    context['procheePlus'] = procheePlus

    dop_uslugiPlus = users.filter(is_enterprises=False, b_dop_uslugi__gt=0).aggregate(Sum('b_dop_uslugi'))['b_dop_uslugi__sum']
    if dop_uslugiPlus == None:
        dop_uslugiPlus = 0
    context['dop_uslugiPlus'] = dop_uslugiPlus

    kabelPlus = users.filter(is_enterprises=False, b_kabel__gt=0).aggregate(Sum('b_kabel'))['b_kabel__sum']
    if kabelPlus == None:
        kabelPlus = 0
    context['kabelPlus'] = kabelPlus

    internetPlus = users.filter(is_enterprises=False, b_internet__gt=0).aggregate(Sum('b_internet'))['b_internet__sum']
    if internetPlus == None:
        internetPlus = 0
    context['internetPlus'] = internetPlus

    alemPlus = users.filter(is_enterprises=False, b_alem__gt=0).aggregate(Sum('b_alem'))['b_alem__sum']
    if alemPlus == None:
        alemPlus = 0
    context['alemPlus'] = alemPlus

    context['balancePlusSum'] = abonplataPlus + slrPlus + kodPlus + zakazPlus + procheePlus + dop_uslugiPlus + internetPlus + kabelPlus + alemPlus

    ########### Текущий баланс Минус (Население) ###########
    abonplataMinus = users.filter(is_enterprises=False, b_telefon__lt=0).aggregate(Sum('b_telefon'))['b_telefon__sum']
    if abonplataMinus == None:
        abonplataMinus = 0
    context['abonplataMinus'] = abonplataMinus

    slrMinus = users.filter(is_enterprises=False, b_slr__lt=0).aggregate(Sum('b_slr'))['b_slr__sum']
    if slrMinus == None:
        slrMinus = 0
    context['slrMinus'] = slrMinus

    kodMinus = users.filter(is_enterprises=False, b_kod__lt=0).aggregate(Sum('b_kod'))['b_kod__sum']
    if kodMinus == None:
        kodMinus = 0
    context['kodMinus'] = kodMinus

    zakazMinus = users.filter(is_enterprises=False, b_zakaz__lt=0).aggregate(Sum('b_zakaz'))['b_zakaz__sum']
    if zakazMinus == None:
        zakazMinus = 0
    context['zakazMinus'] = zakazMinus

    procheeMinus = users.filter(is_enterprises=False, b_prochee__lt=0).aggregate(Sum('b_prochee'))['b_prochee__sum']
    if procheeMinus == None:
        procheeMinus = 0
    context['procheeMinus'] = procheeMinus

    dop_uslugiMinus = users.filter(is_enterprises=False, b_dop_uslugi__lt=0).aggregate(Sum('b_dop_uslugi'))['b_dop_uslugi__sum']
    if dop_uslugiMinus == None:
        dop_uslugiMinus = 0
    context['dop_uslugiMinus'] = dop_uslugiMinus

    kabelMinus = users.filter(is_enterprises=False, b_kabel__lt=0).aggregate(Sum('b_kabel'))['b_kabel__sum']
    if kabelMinus == None:
        kabelMinus = 0
    context['kabelMinus'] = kabelMinus

    internetMinus = users.filter(is_enterprises=False, b_internet__lt=0).aggregate(Sum('b_internet'))['b_internet__sum']
    if internetMinus == None:
        internetMinus = 0
    context['internetMinus'] = internetMinus

    alemMinus = users.filter(is_enterprises=False, b_alem__lt=0).aggregate(Sum('b_alem'))['b_alem__sum']
    if alemMinus == None:
        alemMinus = 0
    context['alemMinus'] = alemMinus

    context['balanceMinusSum'] = abonplataMinus + slrMinus + kodMinus + zakazMinus + procheeMinus + dop_uslugiMinus + internetMinus + kabelMinus + alemMinus

    ########### Текущий баланс Плюс (Edara) ###########
    abonplataPlusEdara = users.filter(is_enterprises=True, b_telefon__gt=0).aggregate(Sum('b_telefon'))['b_telefon__sum']
    if abonplataPlusEdara == None:
        abonplataPlusEdara = 0
    context['abonplataPlusEdara'] = abonplataPlusEdara

    slrPlusEdara = users.filter(is_enterprises=True, b_slr__gt=0).aggregate(Sum('b_slr'))['b_slr__sum']
    if slrPlusEdara == None:
        slrPlusEdara = 0
    context['slrPlusEdara'] = slrPlusEdara

    kodPlusEdara = users.filter(is_enterprises=True, b_kod__gt=0).aggregate(Sum('b_kod'))['b_kod__sum']
    if kodPlusEdara == None:
        kodPlusEdara = 0
    context['kodPlusEdara'] = kodPlusEdara

    zakazPlusEdara = users.filter(is_enterprises=True, b_zakaz__gt=0).aggregate(Sum('b_zakaz'))['b_zakaz__sum']
    if zakazPlusEdara == None:
        zakazPlusEdara = 0
    context['zakazPlusEdara'] = zakazPlusEdara

    procheePlusEdara = users.filter(is_enterprises=True, b_prochee__gt=0).aggregate(Sum('b_prochee'))['b_prochee__sum']
    if procheePlusEdara == None:
        procheePlusEdara = 0
    context['procheePlusEdara'] = procheePlusEdara

    dop_uslugiPlusEdara = users.filter(is_enterprises=True, b_dop_uslugi__gt=0).aggregate(Sum('b_dop_uslugi'))['b_dop_uslugi__sum']
    if dop_uslugiPlusEdara == None:
        dop_uslugiPlusEdara = 0
    context['dop_uslugiPlusEdara'] = dop_uslugiPlusEdara

    kabelPlusEdara = users.filter(is_enterprises=True, b_kabel__gt=0).aggregate(Sum('b_kabel'))['b_kabel__sum']
    if kabelPlusEdara == None:
        kabelPlusEdara = 0
    context['kabelPlusEdara'] = kabelPlusEdara

    internetPlusEdara = users.filter(is_enterprises=True, b_internet__gt=0).aggregate(Sum('b_internet'))['b_internet__sum']
    if internetPlusEdara == None:
        internetPlusEdara = 0
    context['internetPlusEdara'] = internetPlusEdara

    alemPlusEdara = users.filter(is_enterprises=True, b_alem__gt=0).aggregate(Sum('b_alem'))['b_alem__sum']
    if alemPlusEdara == None:
        alemPlusEdara = 0
    context['alemPlusEdara'] = alemPlusEdara

    context['balancePlusEdaraSum'] = abonplataPlusEdara + slrPlusEdara + kodPlusEdara + zakazPlusEdara + procheePlusEdara + dop_uslugiPlusEdara + internetPlusEdara + kabelPlusEdara + alemPlusEdara

    ########### Текущий баланс Минус (Edara) ###########
    abonplataMinusEdara = users.filter(is_enterprises=True, b_telefon__lt=0).aggregate(Sum('b_telefon'))['b_telefon__sum']
    if abonplataMinusEdara == None:
        abonplataMinusEdara = 0
    context['abonplataMinusEdara'] = abonplataMinusEdara

    slrMinusEdara = users.filter(is_enterprises=True, b_slr__lt=0).aggregate(Sum('b_slr'))['b_slr__sum']
    if slrMinusEdara == None:
        slrMinusEdara = 0
    context['slrMinusEdara'] = slrMinusEdara

    kodMinusEdara = users.filter(is_enterprises=True, b_kod__lt=0).aggregate(Sum('b_kod'))['b_kod__sum']
    if kodMinusEdara == None:
        kodMinusEdara = 0
    context['kodMinusEdara'] = kodMinusEdara

    zakazMinusEdara = users.filter(is_enterprises=True, b_zakaz__lt=0).aggregate(Sum('b_zakaz'))['b_zakaz__sum']
    if zakazMinusEdara == None:
        zakazMinusEdara = 0
    context['zakazMinusEdara'] = zakazMinusEdara

    procheeMinusEdara = users.filter(is_enterprises=True, b_prochee__lt=0).aggregate(Sum('b_prochee'))['b_prochee__sum']
    if procheeMinusEdara == None:
        procheeMinusEdara = 0
    context['procheeMinusEdara'] = procheeMinusEdara

    dop_uslugiMinusEdara = users.filter(is_enterprises=True, b_dop_uslugi__lt=0).aggregate(Sum('b_dop_uslugi'))['b_dop_uslugi__sum']
    if dop_uslugiMinusEdara == None:
        dop_uslugiMinusEdara = 0
    context['dop_uslugiMinusEdara'] = dop_uslugiMinusEdara

    kabelMinusEdara = users.filter(is_enterprises=True, b_kabel__lt=0).aggregate(Sum('b_kabel'))['b_kabel__sum']
    if kabelMinusEdara == None:
        kabelMinusEdara = 0
    context['kabelMinusEdara'] = kabelMinusEdara

    internetMinusEdara = users.filter(is_enterprises=True, b_internet__lt=0).aggregate(Sum('b_internet'))['b_internet__sum']
    if internetMinusEdara == None:
        internetMinusEdara = 0
    context['internetMinusEdara'] = internetMinusEdara

    alemMinusEdara = users.filter(is_enterprises=True, b_alem__lt=0).aggregate(Sum('b_alem'))['b_alem__sum']
    if alemMinusEdara == None:
        alemMinusEdara = 0
    context['alemMinusEdara'] = alemMinusEdara

    context['balanceMinusEdaraSum'] = abonplataMinusEdara + slrMinusEdara + kodMinusEdara + zakazMinusEdara + procheeMinusEdara + dop_uslugiMinusEdara + internetMinusEdara + kabelMinusEdara + alemMinusEdara

    ########### Платежи за Выбранный месяц с кассы Наличными ###########
    # payHistoryN = payHistory.exclude(kassir__icontains='APP').exclude(kassir__icontains='POCHTA').exclude(kassir__icontains='SARAY').exclude(kassir__icontains='GOVERNMENT').exclude(kassir__icontains='BANK').filter(is_card=False)
    payHistoryN = payHistory.filter(kassir__icontains='operator', is_card=False)

    abonPayNal = payHistoryN.aggregate(Sum('telefon'))['telefon__sum']
    if abonPayNal == None:
        abonPayNal = 0
    context['abonPayNal'] = abonPayNal

    slrPayNal = payHistoryN.aggregate(Sum('slr'))['slr__sum']
    if slrPayNal == None:
        slrPayNal = 0
    context['slrPayNal'] = slrPayNal

    kodPayNal = payHistoryN.aggregate(Sum('kod'))['kod__sum']
    if kodPayNal == None:
        kodPayNal = 0
    context['kodPayNal'] = kodPayNal

    zakazPayNal = payHistoryN.aggregate(Sum('zakaz'))['zakaz__sum']
    if zakazPayNal == None:
        zakazPayNal = 0
    context['zakazPayNal'] = zakazPayNal

    procheePayNal = payHistoryN.aggregate(Sum('prochee'))['prochee__sum']
    if procheePayNal == None:
        procheePayNal = 0
    context['procheePayNal'] = procheePayNal

    dop_uslugiPayNal = payHistoryN.aggregate(Sum('dop_uslugi'))['dop_uslugi__sum']
    if dop_uslugiPayNal == None:
        dop_uslugiPayNal = 0
    context['dop_uslugiPayNal'] = dop_uslugiPayNal

    internetPayNal = payHistoryN.aggregate(Sum('internet'))['internet__sum']
    if internetPayNal == None:
        internetPayNal = 0
    context['internetPayNal'] = internetPayNal

    kabelPayNal = payHistoryN.aggregate(Sum('kabel'))['kabel__sum']
    if kabelPayNal == None:
        kabelPayNal = 0
    context['kabelPayNal'] = kabelPayNal

    alemPayNal = payHistoryN.aggregate(Sum('alem'))['alem__sum']
    if alemPayNal == None:
        alemPayNal = 0
    context['alemPayNal'] = alemPayNal

    context['payNalSum'] = abonPayNal + slrPayNal + kodPayNal + zakazPayNal + procheePayNal + dop_uslugiPayNal + internetPayNal + kabelPayNal + alemPayNal

    # ########### Платежи за Выбранный месяц с кассы Картой ###########
    # payHistoryC = payHistory.exclude(kassir__icontains='APP').exclude(kassir__icontains='POCHTA').exclude(kassir__icontains='SARAY').exclude(kassir__icontains='GOVERNMENT').exclude(kassir__icontains='BANK').filter(is_card=True)
    payHistoryC = payHistory.filter(kassir__icontains='operator', is_card=True)

    abonPayCard = payHistoryC.aggregate(Sum('telefon'))['telefon__sum']
    if abonPayCard == None:
        abonPayCard = 0
    context['abonPayCard'] = abonPayCard

    slrPayCard = payHistoryC.aggregate(Sum('slr'))['slr__sum']
    if slrPayCard == None:
        slrPayCard = 0
    context['slrPayCard'] = slrPayCard

    kodPayCard = payHistoryC.aggregate(Sum('kod'))['kod__sum']
    if kodPayCard == None:
        kodPayCard = 0
    context['kodPayCard'] = kodPayCard

    zakazPayCard = payHistoryC.aggregate(Sum('zakaz'))['zakaz__sum']
    if zakazPayCard == None:
        zakazPayCard = 0
    context['zakazPayCard'] = zakazPayCard

    procheePayCard = payHistoryC.aggregate(Sum('prochee'))['prochee__sum']
    if procheePayCard == None:
        procheePayCard = 0
    context['procheePayCard'] = procheePayCard

    dop_uslugiPayCard = payHistoryC.aggregate(Sum('dop_uslugi'))['dop_uslugi__sum']
    if dop_uslugiPayCard == None:
        dop_uslugiPayCard = 0
    context['dop_uslugiPayCard'] = dop_uslugiPayCard

    internetPayCard = payHistoryC.aggregate(Sum('internet'))['internet__sum']
    if internetPayCard == None:
        internetPayCard = 0
    context['internetPayCard'] = internetPayCard

    kabelPayCard = payHistoryC.aggregate(Sum('kabel'))['kabel__sum']
    if kabelPayCard == None:
        kabelPayCard = 0
    context['kabelPayCard'] = kabelPayCard

    alemPayCard = payHistoryC.aggregate(Sum('alem'))['alem__sum']
    if alemPayCard == None:
        alemPayCard = 0
    context['alemPayCard'] = alemPayCard

    context['PayCardSum'] = abonPayCard + slrPayCard + kodPayCard + zakazPayCard + procheePayCard + dop_uslugiPayCard + internetPayCard + kabelPayCard + alemPayCard

    ########### Платежи за Выбранный месяц Внешние платежи ###########
    # payHistoryW = payHistory.filter(
    #     Q(kassir__icontains='APP')|
    #     Q(kassir__icontains='POCHTA')|
    #     Q(kassir__icontains='GOVERNMENT')|
    #     Q(kassir__icontains='BANK')
    #     )

    payHistoryW = payHistory.exclude(kassir__icontains='operator').exclude(kassir__icontains='admin')
    
    abonPayW = payHistoryW.aggregate(Sum('telefon'))['telefon__sum']
    if abonPayW == None:
        abonPayW = 0
    context['abonPayW'] = abonPayW

    slrPayW = payHistoryW.aggregate(Sum('slr'))['slr__sum']
    if slrPayW == None:
        slrPayW = 0
    context['slrPayW'] = slrPayW

    kodPayW = payHistoryW.aggregate(Sum('kod'))['kod__sum']
    if kodPayW == None:
        kodPayW = 0
    context['kodPayW'] = kodPayW

    zakazPayW = payHistoryW.aggregate(Sum('zakaz'))['zakaz__sum']
    if zakazPayW == None:
        zakazPayW = 0
    context['zakazPayW'] = zakazPayW

    procheePayW = payHistoryW.aggregate(Sum('prochee'))['prochee__sum']
    if procheePayW == None:
        procheePayW = 0
    context['procheePayW'] = procheePayW

    dop_uslugiPayW = payHistoryW.aggregate(Sum('dop_uslugi'))['dop_uslugi__sum']
    if dop_uslugiPayW == None:
        dop_uslugiPayW = 0
    context['dop_uslugiPayW'] = dop_uslugiPayW

    internetPayW = payHistoryW.aggregate(Sum('internet'))['internet__sum']
    if internetPayW == None:
        internetPayW = 0
    context['internetPayW'] = internetPayW

    kabelPayW = payHistoryW.aggregate(Sum('kabel'))['kabel__sum']
    if kabelPayW == None:
        kabelPayW = 0
    context['kabelPayW'] = kabelPayW

    alemPayW = payHistoryW.aggregate(Sum('alem'))['alem__sum']
    if alemPayW == None:
        alemPayW = 0
    context['alemPayW'] = alemPayW

    context['PayWSum'] = abonPayW + slrPayW + kodPayW + zakazPayW + procheePayW + dop_uslugiPayW + internetPayW + kabelPayW + alemPayW



    ########### Все Начисления ###########
    if nachisleniyaOtchet:
        abonNachN = nachisleniyaOtchet.abonplataNachN
        abonNachP = nachisleniyaOtchet.abonplataNachP
        
        kabelNachN = nachisleniyaOtchet.kabelNachN
        kabelNachP = nachisleniyaOtchet.kabelNachP

        intNach = nachisleniyaOtchet.intetnetNachisleniya
        alemNach = nachisleniyaOtchet.alemNachisleniya
        zakazNach = nachisleniyaOtchet.zakazNachisleniya
        kodNach = nachisleniyaOtchet.kodNachisleniya
        slrNach = nachisleniyaOtchet.slrNachisleniya
        procheeNach = nachisleniyaOtchet.procheeNachisleniya
        serviceNach = nachisleniyaOtchet.serviceNachisleniya
        serviceSepNach = nachisleniyaOtchet.serviceSeparateNachisleniya

        context['abonNachN'] = abonNachN
        context['abonNachP'] = abonNachP
        context['kabelNachN'] = kabelNachN
        context['kabelNachP'] = kabelNachP
        context['intNach'] = intNach
        context['alemNach'] = alemNach
        context['zakazNach'] = zakazNach
        context['kodNach'] = kodNach
        context['slrNach'] = slrNach
        context['procheeNach'] = procheeNach
        context['serviceNach'] = serviceNach
        context['serviceSepNach'] = serviceSepNach

        context['nachSum'] = abonNachN + abonNachP + kabelNachN + kabelNachP + intNach + alemNach + zakazNach + kodNach + slrNach + procheeNach + serviceNach + serviceSepNach

        ########### Все Перекидки ###########
        # Перекунуто с
        telefonM = nachisleniyaOtchet.telefonM
        slrM = nachisleniyaOtchet.slrM
        kodM = nachisleniyaOtchet.kodM
        zakazM = nachisleniyaOtchet.zakazM
        procheeM = nachisleniyaOtchet.procheeM
        dop_uslugiM = nachisleniyaOtchet.dop_uslugiM
        internetM = nachisleniyaOtchet.internetM
        kabelM = nachisleniyaOtchet.kabelM
        alemM = nachisleniyaOtchet.alemM

        context['telefonM'] = telefonM
        context['slrM'] = slrM
        context['kodM'] = kodM
        context['zakazM'] = zakazM
        context['procheeM'] = procheeM
        context['dop_uslugiM'] = dop_uslugiM
        context['internetM'] = internetM
        context['kabelM'] = kabelM
        context['alemM'] = alemM

        context['perekidkaMinusSum'] = telefonM + slrM + kodM + zakazM + procheeM + dop_uslugiM + internetM + kabelM + alemM

        # Перекунуто на
        telefonP = nachisleniyaOtchet.telefonP
        slrP = nachisleniyaOtchet.slrP
        kodP = nachisleniyaOtchet.kodP
        zakazP = nachisleniyaOtchet.zakazP
        procheeP = nachisleniyaOtchet.procheeP
        dop_uslugiP = nachisleniyaOtchet.dop_uslugiP
        internetP = nachisleniyaOtchet.internetP
        kabelP = nachisleniyaOtchet.kabelP
        alemP = nachisleniyaOtchet.alemP

        context['telefonP'] = telefonP
        context['slrP'] = slrP
        context['kodP'] = kodP
        context['zakazP'] = zakazP
        context['procheeP'] = procheeP
        context['dop_uslugiP'] = dop_uslugiP
        context['internetP'] = internetP
        context['kabelP'] = kabelP
        context['alemP'] = alemP

        context['perekidkaPlusSum'] = telefonP + slrP + kodP + zakazP + procheeP + dop_uslugiP + internetP + kabelP + alemP


        ########### Автоперекидки с прочего в другие минусовые колонки (abonplata, slr, kod, zakaz, dop_uslugi) абонента во время его поиска в кассе  ###########
        # Автоперекидки с прочего в  
        sProWabon = nachisleniyaOtchet.sProWabon
        sProWslr = nachisleniyaOtchet.sProWslr
        sProWkod = nachisleniyaOtchet.sProWkod
        sProWzakaz = nachisleniyaOtchet.sProWzakaz
        sProWdop_uslugi = nachisleniyaOtchet.sProWdop_uslugi


        context['sProWabon'] = sProWabon
        context['sProWslr'] = sProWslr
        context['sProWkod'] = sProWkod
        context['sProWzakaz'] = sProWzakaz
        context['sProWdop_uslugi'] = sProWdop_uslugi

        context['sProchWSum'] = sProWabon + sProWslr + sProWkod + sProWzakaz + sProWdop_uslugi

    ########### Вывод баланса предыдущего месяца  ###########
    lastMonth = getPreviousMonth(month)
    context['lastMonth'] = lastMonth

    if month == 'Январь':
        lastYear = str(int(year) - 1)
    else:
        lastYear = year
        context['lastYear'] = lastYear

    try:
        lastMonthBalance = MonthBalance.objects.get(year=lastYear, month=lastMonth, etrap=etrap)
    except:
        lastMonthBalance = False

    if lastMonthBalance:
        context['lastBalanceAbonplataPlus'] = lastMonthBalance.telefonPlus
        context['lastBalanceSlrPlus'] = lastMonthBalance.slrPlus
        context['lastBalanceKodPlus'] = lastMonthBalance.kodPlus
        context['lastBalanceZakazPlus'] = lastMonthBalance.zakazPlus
        context['lastBalanceProcheePlus'] = lastMonthBalance.procheePlus
        context['lastBalanceDop_uslugiPlus'] = lastMonthBalance.dop_uslugiPlus
        context['lastBalanceInternetPlus'] = lastMonthBalance.internetPlus
        context['lastBalanceKabelPlus'] = lastMonthBalance.kabelPlus
        context['lastBalanceAlemPlus'] = lastMonthBalance.alemPlus
        context['totalBalanceLastMonthPlus'] = lastMonthBalance.telefonPlus + lastMonthBalance.slrPlus + lastMonthBalance.kodPlus + lastMonthBalance.zakazPlus + lastMonthBalance.procheePlus + lastMonthBalance.dop_uslugiPlus + lastMonthBalance.internetPlus + lastMonthBalance.kabelPlus + lastMonthBalance.alemPlus

        context['lastBalanceAbonplataMinus'] = lastMonthBalance.telefonMinus
        context['lastBalanceSlrMinus'] = lastMonthBalance.slrMinus
        context['lastBalanceKodMinus'] = lastMonthBalance.kodMinus
        context['lastBalanceZakazMinus'] = lastMonthBalance.zakazMinus
        context['lastBalanceProcheeMinus'] = lastMonthBalance.procheeMinus
        context['lastBalanceDop_uslugiMinus'] = lastMonthBalance.dop_uslugiMinus
        context['lastBalanceInternetMinus'] = lastMonthBalance.internetMinus
        context['lastBalanceKabelMinus'] = lastMonthBalance.kabelMinus
        context['lastBalanceAlemMinus'] = lastMonthBalance.alemMinus
        context['totalBalanceLastMonthMinus'] = lastMonthBalance.telefonMinus + lastMonthBalance.slrMinus + lastMonthBalance.kodMinus + lastMonthBalance.zakazMinus + lastMonthBalance.procheeMinus + lastMonthBalance.dop_uslugiMinus + lastMonthBalance.internetMinus + lastMonthBalance.kabelMinus + lastMonthBalance.alemMinus


    

    return render(request, 'telekom/MATB/monthOtchotNew.html', context)