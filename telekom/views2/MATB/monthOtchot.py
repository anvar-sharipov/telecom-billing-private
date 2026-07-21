from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.models import MonthBalance, NachisleniyaOtchet, PayHistory, UserTable, UserTableArhiw
from django.db.models import Sum
from django.db.models import Q

from telekom.views2.myFunc.myFunc import getPreviousMonth, loggedUserEtrapAndGroup, monthСonvert

from datetime import date
from calendar import monthrange


def monthOtchot(request):
    context = {}
    current_date = str(date.today())

    current_year = current_date[0:4]

    current_month = current_date[5:7]
    month_word = monthСonvert(current_month)

    days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]
    

    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
        context['matbIndex'] = True
        context['monthOtchot'] = True
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    year = request.GET.get('year') if request.GET.get('year') != None else current_year
    month = request.GET.get('month') if request.GET.get('month') != None else month_word
    etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else log
    context['get_year'] = year
    context['get_month'] = month
    context['etrap'] = etrap
    days_in_choosed_month = monthrange(int(year), int(monthСonvert(month)))[1]


    
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['etraps'] = etraps
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

###################################################
#   Платежи (карт) за выбранный месяц PayHistory ##
###################################################

    payHistory = PayHistory.objects.filter(date__range=[f"{year}-{str(monthСonvert(month))}-01 00:00:00", f"{year}-{str(monthСonvert(month))}-{days_in_choosed_month} 23:59:59"], abonent__etrap=etrap)

    abonplataPayCard = payHistory.filter(is_card=True).aggregate(Sum('telefon'))['telefon__sum']
    abonplataPayCard = abonplataPayCard if abonplataPayCard != None else 0
    context['abonplataPayCard'] = abonplataPayCard

    slrPayCard = payHistory.filter(is_card=True).aggregate(Sum('slr'))['slr__sum']
    slrPayCard = slrPayCard if slrPayCard != None else 0
    context['slrPayCard'] = slrPayCard

    kodPayCard = payHistory.filter(is_card=True).aggregate(Sum('kod'))['kod__sum']
    kodPayCard = kodPayCard if kodPayCard != None else 0
    context['kodPayCard'] = kodPayCard

    zakazPayCard = payHistory.filter(is_card=True).aggregate(Sum('zakaz'))['zakaz__sum']
    zakazPayCard = zakazPayCard if zakazPayCard != None else 0
    context['zakazPayCard'] = zakazPayCard

    procheePayCard = payHistory.filter(is_card=True).aggregate(Sum('prochee'))['prochee__sum']
    procheePayCard = procheePayCard if procheePayCard != None else 0
    context['procheePayCard'] = procheePayCard

    dop_uslugiPayCard = payHistory.filter(is_card=True).aggregate(Sum('dop_uslugi'))['dop_uslugi__sum']
    dop_uslugiPayCard = dop_uslugiPayCard if dop_uslugiPayCard != None else 0
    context['dop_uslugiPayCard'] = dop_uslugiPayCard

    internetPayCard = payHistory.filter(is_card=True).aggregate(Sum('internet'))['internet__sum']
    internetPayCard = internetPayCard if internetPayCard != None else 0
    context['internetPayCard'] = internetPayCard

    kabelPayCard = payHistory.filter(is_card=True).aggregate(Sum('kabel'))['kabel__sum']
    kabelPayCard = kabelPayCard if kabelPayCard != None else 0
    context['kabelPayCard'] = kabelPayCard

    alemPayCard = payHistory.filter(is_card=True).aggregate(Sum('alem'))['alem__sum']
    alemPayCard = alemPayCard if alemPayCard != None else 0
    context['alemPayCard'] = alemPayCard

    context['totalPayCard'] = abonplataPayCard + slrPayCard + kodPayCard + zakazPayCard + procheePayCard + dop_uslugiPayCard + internetPayCard + kabelPayCard + alemPayCard
#######################################################
#   Платежи (карт) за выбранный месяц PayHistory END ##
#######################################################

#############################################
#   Платежи (наличными) за выбранный месяц ##
#############################################
    abonplataPay = payHistory.filter(is_card=False).aggregate(Sum('telefon'))['telefon__sum']
    abonplataPay = abonplataPay if abonplataPay != None else 0
    context['abonplataPay'] = abonplataPay

    slrPay = payHistory.filter(is_card=False).aggregate(Sum('slr'))['slr__sum']
    slrPay = slrPay if slrPay != None else 0
    context['slrPay'] = slrPay

    kodPay = payHistory.filter(is_card=False).aggregate(Sum('kod'))['kod__sum']
    kodPay = kodPay if kodPay != None else 0
    context['kodPay'] = kodPay

    zakazPay = payHistory.filter(is_card=False).aggregate(Sum('zakaz'))['zakaz__sum']
    zakazPay = zakazPay if zakazPay != None else 0
    context['zakazPay'] = zakazPay

    procheePay = payHistory.filter(is_card=False).aggregate(Sum('prochee'))['prochee__sum']
    procheePay = procheePay if procheePay != None else 0
    context['procheePay'] = procheePay

    dop_uslugiPay = payHistory.filter(is_card=False).aggregate(Sum('dop_uslugi'))['dop_uslugi__sum']
    dop_uslugiPay = dop_uslugiPay if dop_uslugiPay != None else 0
    context['dop_uslugiPay'] = dop_uslugiPay

    internetPay = payHistory.filter(is_card=False).aggregate(Sum('internet'))['internet__sum']
    internetPay = internetPay if internetPay != None else 0
    context['internetPay'] = internetPay

    kabelPay = payHistory.filter(is_card=False).aggregate(Sum('kabel'))['kabel__sum']
    kabelPay = kabelPay if kabelPay != None else 0
    context['kabelPay'] = kabelPay

    alemPay = payHistory.filter(is_card=False).aggregate(Sum('alem'))['alem__sum']
    alemPay = alemPay if alemPay != None else 0
    context['alemPay'] = alemPay

    context['totalPay'] = abonplataPay + slrPay + kodPay + zakazPay + procheePay + dop_uslugiPay + internetPay + kabelPay + alemPay
#################################################
#   Платежи (наличными) за выбранный месяц END ##
#################################################

###################################### 
#   Текущий баланс Плюс с UserTable ##
######################################
    userTable = UserTable.objects.filter(etrap=etrap)

    totalAbonplataPlus = userTable.filter(b_telefon__gte=0, etrap=etrap).aggregate(Sum('b_telefon'))['b_telefon__sum']
    totalAbonplataPlus = totalAbonplataPlus if totalAbonplataPlus != None else 0
    context['totalAbonplataPlus'] = totalAbonplataPlus

    totalSlrPlus = userTable.filter(b_slr__gte=0, etrap=etrap).aggregate(Sum('b_slr'))['b_slr__sum']
    totalSlrPlus = totalSlrPlus if totalSlrPlus != None else 0
    context['totalSlrPlus'] = totalSlrPlus

    totalKodPlus = userTable.filter(b_kod__gte=0, etrap=etrap).aggregate(Sum('b_kod'))['b_kod__sum']
    totalKodPlus = totalKodPlus if totalKodPlus != None else 0
    context['totalKodPlus'] = totalKodPlus

    totalZakazPlus = userTable.filter(b_zakaz__gte=0, etrap=etrap).aggregate(Sum('b_zakaz'))['b_zakaz__sum']
    totalZakazPlus = totalZakazPlus if totalZakazPlus != None else 0
    context['totalZakazPlus'] = totalZakazPlus

    totalProcheePlus = userTable.filter(b_prochee__gte=0, etrap=etrap).aggregate(Sum('b_prochee'))['b_prochee__sum']
    totalProcheePlus = totalProcheePlus if totalProcheePlus != None else 0
    context['totalProcheePlus'] = totalProcheePlus

    totalDop_uslugiPlus = userTable.filter(b_dop_uslugi__gte=0, etrap=etrap).aggregate(Sum('b_dop_uslugi'))['b_dop_uslugi__sum']
    totalDop_uslugiPlus = totalDop_uslugiPlus if totalDop_uslugiPlus != None else 0
    context['totalDop_uslugiPlus'] = totalDop_uslugiPlus

    totalInternetPlus = userTable.filter(b_internet__gte=0, etrap=etrap).aggregate(Sum('b_internet'))['b_internet__sum']
    totalInternetPlus = totalInternetPlus if totalInternetPlus != None else 0
    context['totalInternetPlus'] = totalInternetPlus

    totalKabelPlus = userTable.filter(b_kabel__gte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum']
    totalKabelPlus = totalKabelPlus if totalKabelPlus != None else 0
    context['totalKabelPlus'] = totalKabelPlus

    totalAlemPlus = userTable.filter(b_alem__gte=0, etrap=etrap).aggregate(Sum('b_alem'))['b_alem__sum']
    totalAlemPlus = totalAlemPlus if totalAlemPlus != None else 0
    context['totalAlemPlus'] = totalAlemPlus

    context['totalBalancePlus'] = totalAbonplataPlus + totalSlrPlus + totalKodPlus + totalZakazPlus + totalProcheePlus + totalDop_uslugiPlus + totalInternetPlus + totalKabelPlus + totalAlemPlus
########################################## 
#   Текущий баланс Плюс с UserTable END ##
##########################################

####################################### 
#   Текущий баланс Минус с UserTable ##
#######################################
    totalAbonplataMinus = userTable.filter(b_telefon__lte=0, etrap=etrap).aggregate(Sum('b_telefon'))['b_telefon__sum']
    totalAbonplataMinus = totalAbonplataMinus if totalAbonplataMinus != None else 0
    context['totalAbonplataMinus'] = totalAbonplataMinus

    totalSlrMinus = userTable.filter(b_slr__lte=0, etrap=etrap).aggregate(Sum('b_slr'))['b_slr__sum']
    totalSlrMinus = totalSlrMinus if totalSlrMinus != None else 0
    context['totalSlrMinus'] = totalSlrMinus

    totalKodMinus = userTable.filter(b_kod__lte=0, etrap=etrap).aggregate(Sum('b_kod'))['b_kod__sum']
    totalKodMinus = totalKodMinus if totalKodMinus != None else 0
    context['totalKodMinus'] = totalKodMinus

    totalZakazMinus = userTable.filter(b_zakaz__lte=0, etrap=etrap).aggregate(Sum('b_zakaz'))['b_zakaz__sum']
    totalZakazMinus = totalZakazMinus if totalZakazMinus != None else 0
    context['totalZakazMinus'] = totalZakazMinus

    totalProcheeMinus = userTable.filter(b_prochee__lte=0, etrap=etrap).aggregate(Sum('b_prochee'))['b_prochee__sum']
    totalProcheeMinus = totalProcheeMinus if totalProcheeMinus != None else 0
    context['totalProcheeMinus'] = totalProcheeMinus

    totalDop_uslugiMinus = userTable.filter(b_dop_uslugi__lte=0, etrap=etrap).aggregate(Sum('b_dop_uslugi'))['b_dop_uslugi__sum']
    totalDop_uslugiMinus = totalDop_uslugiMinus if totalDop_uslugiMinus != None else 0
    context['totalDop_uslugiMinus'] = totalDop_uslugiMinus

    totalInternetMinus = userTable.filter(b_internet__lte=0, etrap=etrap).aggregate(Sum('b_internet'))['b_internet__sum']
    totalInternetMinus = totalInternetMinus if totalInternetMinus != None else 0
    context['totalInternetMinus'] = totalInternetMinus

    totalKabelMinus = userTable.filter(b_kabel__lte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum']
    totalKabelMinus = totalKabelMinus if totalKabelMinus != None else 0
    context['totalKabelMinus'] = totalKabelMinus

    totalAlemMinus = userTable.filter(b_alem__lte=0, etrap=etrap).aggregate(Sum('b_alem'))['b_alem__sum']
    totalAlemMinus = totalAlemMinus if totalAlemMinus != None else 0
    context['totalAlemMinus'] = totalAlemMinus

    context['totalBalanceMinus'] = totalAbonplataMinus + totalSlrMinus + totalKodMinus + totalZakazMinus + totalProcheeMinus + totalDop_uslugiMinus + totalInternetMinus + totalKabelMinus + totalAlemMinus
########################################### 
#   Текущий баланс Минус с UserTable END ##
###########################################

##########################################################
#   Вся инфа с NachisleniyaOtchet для выбранного месяца ##
##########################################################
    try:
        nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=etrap, year=year, month=month)
    except:
        nachisleniyaOtchet = False
    
    if nachisleniyaOtchet:
# Инфа о внешних платежах за выбранный месяц
        internetWnPl = nachisleniyaOtchet.WneshniyePlatejiInternet if nachisleniyaOtchet.WneshniyePlatejiInternet != None else 0
        alemWnPl = nachisleniyaOtchet.WneshniyePlatejiAlem if nachisleniyaOtchet.WneshniyePlatejiAlem != None else 0
        abonplataWnPl = nachisleniyaOtchet.WneshniyePlatejiAbonplata if nachisleniyaOtchet.WneshniyePlatejiAbonplata != None else 0
        context['internetPlateji'] = internetWnPl
        context['AlemPlateji'] = alemWnPl
        context['AbonplataPlateji'] = abonplataWnPl
        context['totalWneshniePlateji'] = internetWnPl + alemWnPl + abonplataWnPl
# Инфа о начисления метры
        mss = nachisleniyaOtchet.metrNachisleniya if nachisleniyaOtchet.metrNachisleniya != None else 0
        context['mss'] = mss 
# Инфа о начислениях через Абон отдел
        serviceMonthNachMB = nachisleniyaOtchet.serviceSeparateNachisleniya
        context['serviceMonthNachMB'] = serviceMonthNachMB
        context['totalMss_seviceNach'] = serviceMonthNachMB + mss

# Инфа о начислениях за выбранный месяц
        kabelMonthNachMTB = nachisleniyaOtchet.kabelMatbNachisleniya
        context['kabelMonthNachMTB'] = kabelMonthNachMTB

        internetMonthNachMTB = nachisleniyaOtchet.intetnetNachisleniya
        context['internetMonthNachMTB'] = internetMonthNachMTB

        alemMonthNachMTB = nachisleniyaOtchet.alemNachisleniya
        context['alemMonthNachMTB'] = alemMonthNachMTB

        zakazMonthNachMTB = nachisleniyaOtchet.zakazNachisleniya
        context['zakazMonthNachMTB'] = zakazMonthNachMTB

        abonplataMonthNachMTB = nachisleniyaOtchet.abonplataNachisleniya
        context['abonplataMonthNachMTB'] = abonplataMonthNachMTB

        metrMonthNachMTB = nachisleniyaOtchet.metrNachisleniya
        context['metrMonthNachMTB'] = metrMonthNachMTB

        kodMonthNachMTB = nachisleniyaOtchet.kodNachisleniya
        context['kodMonthNachMTB'] = kodMonthNachMTB

        slrMonthNachMTB = nachisleniyaOtchet.slrNachisleniya
        context['slrMonthNachMTB'] = slrMonthNachMTB

        procheeMonthNachMTB = nachisleniyaOtchet.procheeNachisleniya
        context['procheeMonthNachMTB'] = procheeMonthNachMTB

        serviceMonthNachMTB = nachisleniyaOtchet.serviceNachisleniya
        context['serviceMonthNachMTB'] = serviceMonthNachMTB

        context['totalMTBNachisleniya'] = kabelMonthNachMTB + internetMonthNachMTB + alemMonthNachMTB + zakazMonthNachMTB + abonplataMonthNachMTB + metrMonthNachMTB+kodMonthNachMTB + slrMonthNachMTB + procheeMonthNachMTB + serviceMonthNachMTB


# ############################################################
#   Вся инфа с NachisleniyaOtchet для выбранного месяца END ##
##############################################################

# ###############################################

# ########################################
#   Берем баланс предыдущего месяца END ##
##########################################
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

# ########################################
#   Берем баланс предыдущего месяца END ##
##########################################

# ###############################################################
#   Инфа о изменениях в отчете при перекидках за текущий месяц ##
#################################################################

# Инфа о изменениях в отчете при перекидках (минус)
        internetM = nachisleniyaOtchet.internetM
        context['internetM'] = internetM

        kabelM = nachisleniyaOtchet.kabelM
        context['kabelM'] = kabelM

        alemM = nachisleniyaOtchet.alemM
        context['alemM'] = alemM

        telefonM = nachisleniyaOtchet.telefonM
        context['telefonM'] = telefonM

        slrM = nachisleniyaOtchet.slrM
        context['slrM'] = slrM

        kodM = nachisleniyaOtchet.kodM
        context['kodM'] = kodM

        zakazM = nachisleniyaOtchet.zakazM
        context['zakazM'] = zakazM

        procheeM = nachisleniyaOtchet.procheeM
        context['procheeM'] = procheeM

        dop_uslugiM = nachisleniyaOtchet.dop_uslugiM
        context['dop_uslugiM'] = dop_uslugiM

        context['totalMPerekidka'] =  + internetM + kabelM + alemM + telefonM + slrM + kodM + zakazM+procheeM + dop_uslugiM

# Инфа о изменениях в отчете при перекидках (плюс)
        internetP = nachisleniyaOtchet.internetP
        context['internetP'] = internetP
        
        kabelP = nachisleniyaOtchet.kabelP
        context['kabelP'] = kabelP

        alemP = nachisleniyaOtchet.alemP
        context['alemP'] = alemP

        telefonP = nachisleniyaOtchet.telefonP
        context['telefonP'] = telefonP

        slrP = nachisleniyaOtchet.slrP
        context['slrP'] = slrP

        kodP = nachisleniyaOtchet.kodP
        context['kodP'] = kodP

        zakazP = nachisleniyaOtchet.zakazP
        context['zakazP'] = zakazP

        procheeP = nachisleniyaOtchet.procheeP
        context['procheeP'] = procheeP

        dop_uslugiP = nachisleniyaOtchet.dop_uslugiP
        context['dop_uslugiP'] = dop_uslugiP

        context['totalPPerekidka'] =  + internetP + kabelP + alemP + telefonM + slrP + kodP + zakazM + procheeP + dop_uslugiP

# ###################################################################
#   Инфа о изменениях в отчете при перекидках за текущий месяц END ##
#####################################################################

# ##################################################################
#   Инфа о изменениях в отчете при перекидках за Предыдущий месяц ##
####################################################################
        lastNachisleniyaOtchet = NachisleniyaOtchet.objects.get(year=lastYear, month=lastMonth, etrap=etrap)

# Инфа о изменениях в отчете при перекидках (минус)
        internetMLast = lastNachisleniyaOtchet.internetM
        context['internetMLast'] = internetMLast

        kabelMLast = lastNachisleniyaOtchet.kabelM
        context['kabelMLast'] = kabelMLast

        alemMLast = lastNachisleniyaOtchet.alemM
        context['alemMLast'] = alemMLast

        telefonMLast = lastNachisleniyaOtchet.telefonM
        context['telefonMLast'] = telefonMLast

        slrMLast = lastNachisleniyaOtchet.slrM
        context['slrMLast'] = slrMLast

        kodMLast = lastNachisleniyaOtchet.kodM
        context['kodMLast'] = kodMLast

        zakazMLast = lastNachisleniyaOtchet.zakazM
        context['zakazMLast'] = zakazMLast

        procheeMLast = lastNachisleniyaOtchet.procheeM
        context['procheeMLast'] = procheeMLast

        dop_uslugiMLast = lastNachisleniyaOtchet.dop_uslugiM
        context['dop_uslugiMLast'] = dop_uslugiMLast

        context['totalMPerekidkaLast'] =  + internetMLast + kabelMLast + alemMLast + telefonMLast + slrMLast + kodMLast + zakazMLast + procheeMLast + dop_uslugiMLast

# Инфа о изменениях в отчете при перекидках (плюс)
        internetPLast = nachisleniyaOtchet.internetP
        context['internetPLast'] = internetPLast
        
        kabelPLast = nachisleniyaOtchet.kabelP
        context['kabelPLast'] = kabelPLast

        alemPLast = nachisleniyaOtchet.alemP
        context['alemPLast'] = alemPLast

        telefonPLast = nachisleniyaOtchet.telefonP
        context['telefonPLast'] = telefonPLast

        slrPLast = nachisleniyaOtchet.slrP
        context['slrPLast'] = slrPLast

        kodPLast = nachisleniyaOtchet.kodP
        context['kodPLast'] = kodPLast

        zakazPLast = nachisleniyaOtchet.zakazP
        context['zakazPLast'] = zakazPLast

        procheePLast = nachisleniyaOtchet.procheeP
        context['procheePLast'] = procheePLast

        dop_uslugiPLast = nachisleniyaOtchet.dop_uslugiP
        context['dop_uslugiPLast'] = dop_uslugiPLast

        context['totalPPerekidkaLast'] =  + internetPLast + kabelPLast + alemPLast + telefonMLast + slrPLast + kodPLast + zakazMLast + procheePLast + dop_uslugiPLast

# ####################################################@@@@##############
#   Инфа о изменениях в отчете при перекидках за Предыдущий месяц END ##
##########################################################@@@@##########

    return render(request, 'telekom/MATB/monthOtchot.html', context)