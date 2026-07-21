from django.shortcuts import render, redirect
from django.contrib import messages
import re
from django.db.models import Q

# import time
from datetime import datetime
from datetime import date
from calendar import monthrange
from telekom.views2.myFunc.myFunc import monthСonvert, get_etrap_and_types
from django.db.models import Sum

from telekom.models import *

from django.db import transaction
import logging
logger = logging.getLogger(__name__)





def kassaIndex(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            log = 'Dashoguz'
            context['kassaIndex'] = True
            context['kassa'] = True
            context['allow_to_pay'] = True
        else:
            etrap_types = get_etrap_and_types(request.user)
            etraps = etrap_types['etraps']
            log = etraps[0]
            types = etrap_types['types']
            if 'Kassa' in types:
                context['allow_to_pay'] = True
                context['kassaIndex'] = True
                context['kassa'] = True
            else:
                context['allow_to_pay'] = False
                if 'MTB' in types:
                    context['matbIndex'] = True
                    context['KassaMTB'] = True
                if 'MB' in types:
                    context['setService'] = True
                    context['KassaMB'] = True
                if 'Internet' in types:
                    context['internetBilling'] = True
                    context['KassaInt'] = True
                if 'SHB' in types:
                    context['SHBIndex'] = True
                    context['KassaSHB'] = True
                if '071' in types:
                    context['operator071'] = True
                    context['Kassa071'] = True 
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')


    
    # узнать последнюю дату начисления DBF файлов
    try:
        context['lastZakazDate'] = Zakaz.objects.latest('DATE')
    except:
        context['lastZakazDate'] = ''

    try:
        context['lastKodDate'] = NonLocalCall.objects.latest('DATE')
    except:
        context['lastKodDate'] = ''


    context['log'] = log
    context['PC_name'] = request.META['SERVER_NAME']

    zapretOplaty = ['operator4', 'bagt', '071dza', 'Gayyp']
    context['zapretOplaty'] = zapretOplaty

    # new 2024.12.27
    current_date_new = datetime.now().date()
    formatted_date_new = current_date_new.strftime('%Y-%m-%d')
    current_year_new, current_month_new, current_day_new = formatted_date_new.split('-')
   
    context['current_year_new'] = current_year_new
    # new end 2024.12.27



    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    context['etraps'] = etraps
    # log = getLoggedUserEtrap(request.user.username)
    # context['log'] = log

    current_date = str(date.today())
    context['current_date'] = current_date
    current_year = current_date[0:4]
    context['current_year'] = current_year
    current_month = current_date[5:7]
    current_day = current_date[8:]
    days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]
    # current_date_time = datetime.now()
    # context['current_date_time'] = current_date_time

    # Каждый месяц 1-го числа при открытии кассы платежа сохранять текущий баланс 1 раз
#################################################
## Сохоранения баланса каждый масяц 1-го числа ##
#################################################
    # if current_day == '01':
    #     for etrap in etraps:
    #         try:
    #             MonthBalance.objects.get(year=current_year, month=monthСonvert(current_month), etrap=etrap)
    #             saveMonthBalance = False
    #         except:
    #             saveMonthBalance = True

    #         # try:
    #         #     MonthBalanceRezerw.objects.get(year=current_year, month=monthСonvert(current_month), etrap=etrap)
    #         #     saveMonthBalanceRezerw = False
    #         # except:
    #         #     saveMonthBalanceRezerw = True

    #         # try:
    #         #     MonthBalanceArhiw.objects.get(year=current_year, month=monthСonvert(current_month), etrap=etrap)
    #         #     saveMonthBalanceArhiw = False
    #         # except:
    #         #     saveMonthBalanceArhiw = True

    #         if saveMonthBalance:
    #             userTable = UserTable.objects.filter(etrap=etrap)
    #             # userTableArhiw = UserTableArhiw.objects.filter(etrap=etrap, wost_date__isnull=True, close_date__isnull=True)
    #             ##########
    #             abPlus = userTable.filter(b_telefon__gte=0, etrap=etrap).aggregate(Sum('b_telefon'))['b_telefon__sum']
    #             totalAbonplataPlus =  abPlus if abPlus != None else 0
    #             abMinus = userTable.filter(b_telefon__lte=0, etrap=etrap).aggregate(Sum('b_telefon'))['b_telefon__sum']
    #             totalAbonplataMinus = abMinus if abMinus != None else 0
    #             ###########
    #             slPlus = userTable.filter(b_slr__gte=0, etrap=etrap).aggregate(Sum('b_slr'))['b_slr__sum']
    #             totalSlrPlus = slPlus  if slPlus != None else 0
    #             slMinus = userTable.filter(b_slr__lte=0, etrap=etrap).aggregate(Sum('b_slr'))['b_slr__sum']
    #             totalSlrMinus = slMinus if slMinus != None else 0
    #             ############
    #             koPlus = userTable.filter(b_kod__gte=0, etrap=etrap).aggregate(Sum('b_kod'))['b_kod__sum']
    #             totalKodPlus = koPlus if koPlus != None else 0
    #             koMinus = userTable.filter(b_kod__lte=0, etrap=etrap).aggregate(Sum('b_kod'))['b_kod__sum']
    #             totalKodMinus = koMinus if koMinus != None else 0
    #             ############
    #             zaPlus = userTable.filter(b_zakaz__gte=0, etrap=etrap).aggregate(Sum('b_zakaz'))['b_zakaz__sum']
    #             totalZakazPlus = zaPlus if zaPlus != None else 0
    #             zaMinus = userTable.filter(b_zakaz__lte=0, etrap=etrap).aggregate(Sum('b_zakaz'))['b_zakaz__sum']
    #             totalZakazMinus = zaMinus if zaMinus != None else 0
    #             ############
    #             prPlus = userTable.filter(b_prochee__gte=0, etrap=etrap).aggregate(Sum('b_prochee'))['b_prochee__sum']
    #             totalProcheePlus = prPlus if prPlus != None else 0
    #             prMinus = userTable.filter(b_prochee__lte=0, etrap=etrap).aggregate(Sum('b_prochee'))['b_prochee__sum']
    #             totalProcheeMinus = prMinus if prMinus != None else 0
    #             ############
    #             doPlus = userTable.filter(b_dop_uslugi__gte=0, etrap=etrap).aggregate(Sum('b_dop_uslugi'))['b_dop_uslugi__sum']
    #             totalDop_uslugiPlus = doPlus if doPlus != None else 0
    #             doMinus = userTable.filter(b_dop_uslugi__lte=0, etrap=etrap).aggregate(Sum('b_dop_uslugi'))['b_dop_uslugi__sum']
    #             totalDop_uslugiMinus = doMinus if doMinus != None else 0
    #             ############
    #             inPlus = userTable.filter(b_internet__gte=0, etrap=etrap).aggregate(Sum('b_internet'))['b_internet__sum']
    #             totalInternetPlus = inPlus if inPlus != None else 0
    #             inMinus = userTable.filter(b_internet__lte=0, etrap=etrap).aggregate(Sum('b_internet'))['b_internet__sum']
    #             totalInternetMinus = inMinus if inMinus != None else 0
    #             ############
    #             kaPlus = userTable.filter(b_kabel__gte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum']
    #             totalKabelPlus = kaPlus if kaPlus != None else 0
    #             kaMinus = userTable.filter(b_kabel__lte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum']
    #             totalKabelMinus = kaMinus if kaMinus != None else 0
    #             ############

    #             # totalKabelPlus = userTable.filter(b_kabel__gte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum'] if userTable.filter(b_kabel__gte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum'] != None else 0
    #             # totalKabelMinus = userTable.filter(b_kabel__lte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum'] if userTable.filter(b_kabel__lte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum'] != None else 0
    #             # totalKabelPlusArhiw = userTableArhiw.filter(b_kabel__gte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum'] if userTableArhiw.filter(b_kabel__gte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum'] != None else 0
    #             # totalKabelMinusArhiw = userTableArhiw.filter(b_kabel__lte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum'] if userTableArhiw.filter(b_kabel__lte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum'] != None else 0
    #             ############
    #             alPlus = userTable.filter(b_alem__gte=0, etrap=etrap).aggregate(Sum('b_alem'))['b_alem__sum']
    #             totalAlemPlus = alPlus if alPlus != None else 0
    #             alMinus = userTable.filter(b_alem__lte=0, etrap=etrap).aggregate(Sum('b_alem'))['b_alem__sum']
    #             totalAlemMinus = alMinus if alMinus != None else 0
                
    #             MonthBalance.objects.create(
    #                 year=current_year,
    #                 month=monthСonvert(current_month),
    #                 etrap=etrap,

    #                 internetPlus=totalInternetPlus,
    #                 kabelPlus=totalKabelPlus, 
    #                 alemPlus=totalAlemPlus,
    #                 telefonPlus=totalAbonplataPlus,
    #                 slrPlus=totalSlrPlus,
    #                 kodPlus=totalKodPlus,
    #                 zakazPlus=totalZakazPlus,
    #                 procheePlus=totalProcheePlus,
    #                 dop_uslugiPlus=totalDop_uslugiPlus,

    #                 internetMinus=totalInternetMinus,
    #                 kabelMinus=totalKabelMinus, 
    #                 alemMinus=totalAlemMinus,
    #                 telefonMinus=totalAbonplataMinus,
    #                 slrMinus=totalSlrMinus,
    #                 kodMinus=totalKodMinus,
    #                 zakazMinus=totalZakazMinus,
    #                 procheeMinus=totalProcheeMinus,
    #                 dop_uslugiMinus=totalDop_uslugiMinus,
    #                 )
#####################################################
## Сохоранения баланса каждый масяц 1-го числа END ##
#####################################################
            
            # if saveMonthBalanceRezerw:
            #     userTableRezerw = UserTableRezerw.objects.filter(etrap=etrap)
            #     if UserTableRezerw:
            #         totalAbonplataPlus = userTableRezerw.filter(b_telefon__gte=0, etrap=etrap).aggregate(Sum('b_telefon'))['b_telefon__sum']
            #         totalAbonplataMinus = userTableRezerw.filter(b_telefon__lte=0, etrap=etrap).aggregate(Sum('b_telefon'))['b_telefon__sum']
            #         context['totalAbonplataPlus'] = totalAbonplataPlus
            #         context['totalAbonplataMinus'] = totalAbonplataMinus

            #         totalSlrPlus = userTableRezerw.filter(b_slr__gte=0, etrap=etrap).aggregate(Sum('b_slr'))['b_slr__sum']
            #         totalSlrMinus = userTableRezerw.filter(b_slr__lte=0, etrap=etrap).aggregate(Sum('b_slr'))['b_slr__sum']
            #         context['totalSlrPlus'] = totalSlrPlus
            #         context['totalSlrMinus'] = totalSlrMinus

            #         totalKodPlus = userTableRezerw.filter(b_kod__gte=0, etrap=etrap).aggregate(Sum('b_kod'))['b_kod__sum']
            #         totalKodMinus = userTableRezerw.filter(b_kod__lte=0, etrap=etrap).aggregate(Sum('b_kod'))['b_kod__sum']
            #         context['totalKodPlus'] = totalKodPlus
            #         context['totalKodMinus'] = totalKodMinus

            #         totalZakazPlus = userTableRezerw.filter(b_zakaz__gte=0, etrap=etrap).aggregate(Sum('b_zakaz'))['b_zakaz__sum']
            #         totalZakazMinus = userTableRezerw.filter(b_zakaz__lte=0, etrap=etrap).aggregate(Sum('b_zakaz'))['b_zakaz__sum']
            #         context['totalZakazPlus'] = totalZakazPlus
            #         context['totalZakazMinus'] = totalZakazMinus

            #         totalProcheePlus = userTableRezerw.filter(b_prochee__gte=0, etrap=etrap).aggregate(Sum('b_prochee'))['b_prochee__sum']
            #         totalProcheeMinus = userTableRezerw.filter(b_prochee__lte=0, etrap=etrap).aggregate(Sum('b_prochee'))['b_prochee__sum']
            #         context['totalProcheePlus'] = totalProcheePlus
            #         context['totalProcheeMinus'] = totalProcheeMinus

            #         totalDop_uslugiPlus = userTableRezerw.filter(b_dop_uslugi__gte=0, etrap=etrap).aggregate(Sum('b_dop_uslugi'))['b_dop_uslugi__sum']
            #         totalDop_uslugiMinus = userTableRezerw.filter(b_dop_uslugi__lte=0, etrap=etrap).aggregate(Sum('b_dop_uslugi'))['b_dop_uslugi__sum']
            #         context['totalDop_uslugiPlus'] = totalDop_uslugiPlus
            #         context['totalDop_uslugiMinus'] = totalDop_uslugiMinus

            #         totalInternetPlus = userTableRezerw.filter(b_internet__gte=0, etrap=etrap).aggregate(Sum('b_internet'))['b_internet__sum']
            #         totalInternetMinus = userTableRezerw.filter(b_internet__lte=0, etrap=etrap).aggregate(Sum('b_internet'))['b_internet__sum']
            #         context['totalInternetPlus'] = totalInternetPlus
            #         context['totalInternetMinus'] = totalInternetMinus

            #         totalKabelPlus = userTableRezerw.filter(b_kabel__gte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum']
            #         totalKabelMinus = userTableRezerw.filter(b_kabel__lte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum']
            #         context['totalKabelPlus'] = totalKabelPlus
            #         context['totalKabelMinus'] = totalKabelMinus

            #         totalAlemPlus = userTableRezerw.filter(b_alem__gte=0, etrap=etrap).aggregate(Sum('b_alem'))['b_alem__sum']
            #         totalAlemMinus = userTableRezerw.filter(b_alem__lte=0, etrap=etrap).aggregate(Sum('b_alem'))['b_alem__sum']
            #         context['totalAlemPlus'] = totalAlemPlus
            #         context['totalAlemMinus'] = totalAlemMinus

            #         MonthBalanceRezerw.objects.create(
            #             year=current_year,
            #             month=monthСonvert(current_month),
            #             etrap=etrap,

            #             internetPlus=totalInternetPlus,
            #             kabelPlus=totalKabelPlus, 
            #             alemPlus=totalAlemPlus,
            #             telefonPlus=totalAbonplataPlus,
            #             slrPlus=totalSlrPlus,
            #             kodPlus=totalKodPlus,
            #             zakazPlus=totalZakazPlus,
            #             procheePlus=totalProcheePlus,
            #             dop_uslugiPlus=totalDop_uslugiPlus,

            #             internetMinus=totalInternetMinus,
            #             kabelMinus=totalKabelMinus, 
            #             alemMinus=totalAlemMinus,
            #             telefonMinus=totalAbonplataMinus,
            #             slrMinus=totalSlrMinus,
            #             kodMinus=totalKodMinus,
            #             zakazMinus=totalZakazMinus,
            #             procheeMinus=totalProcheeMinus,
            #             dop_uslugiMinus=totalDop_uslugiMinus,
            #             )

            # if saveMonthBalanceArhiw:
            #     userTableArhiw = UserTableArhiw.objects.filter(etrap=etrap)
                
            #     totalAbonplataPlus = userTableArhiw.filter(b_telefon__gte=0, etrap=etrap).aggregate(Sum('b_telefon'))['b_telefon__sum']
            #     totalAbonplataMinus = userTableArhiw.filter(b_telefon__lte=0, etrap=etrap).aggregate(Sum('b_telefon'))['b_telefon__sum']
            #     context['totalAbonplataPlus'] = totalAbonplataPlus
            #     context['totalAbonplataMinus'] = totalAbonplataMinus

            #     totalSlrPlus = userTableArhiw.filter(b_slr__gte=0, etrap=etrap).aggregate(Sum('b_slr'))['b_slr__sum']
            #     totalSlrMinus = userTableArhiw.filter(b_slr__lte=0, etrap=etrap).aggregate(Sum('b_slr'))['b_slr__sum']
            #     context['totalSlrPlus'] = totalSlrPlus
            #     context['totalSlrMinus'] = totalSlrMinus

            #     totalKodPlus = userTableArhiw.filter(b_kod__gte=0, etrap=etrap).aggregate(Sum('b_kod'))['b_kod__sum']
            #     totalKodMinus = userTableArhiw.filter(b_kod__lte=0, etrap=etrap).aggregate(Sum('b_kod'))['b_kod__sum']
            #     context['totalKodPlus'] = totalKodPlus
            #     context['totalKodMinus'] = totalKodMinus

            #     totalZakazPlus = userTableArhiw.filter(b_zakaz__gte=0, etrap=etrap).aggregate(Sum('b_zakaz'))['b_zakaz__sum']
            #     totalZakazMinus = userTableArhiw.filter(b_zakaz__lte=0, etrap=etrap).aggregate(Sum('b_zakaz'))['b_zakaz__sum']
            #     context['totalZakazPlus'] = totalZakazPlus
            #     context['totalZakazMinus'] = totalZakazMinus

            #     totalProcheePlus = userTableArhiw.filter(b_prochee__gte=0, etrap=etrap).aggregate(Sum('b_prochee'))['b_prochee__sum']
            #     totalProcheeMinus = userTableArhiw.filter(b_prochee__lte=0, etrap=etrap).aggregate(Sum('b_prochee'))['b_prochee__sum']
            #     context['totalProcheePlus'] = totalProcheePlus
            #     context['totalProcheeMinus'] = totalProcheeMinus

            #     totalDop_uslugiPlus = userTableArhiw.filter(b_dop_uslugi__gte=0, etrap=etrap).aggregate(Sum('b_dop_uslugi'))['b_dop_uslugi__sum']
            #     totalDop_uslugiMinus = userTableArhiw.filter(b_dop_uslugi__lte=0, etrap=etrap).aggregate(Sum('b_dop_uslugi'))['b_dop_uslugi__sum']
            #     context['totalDop_uslugiPlus'] = totalDop_uslugiPlus
            #     context['totalDop_uslugiMinus'] = totalDop_uslugiMinus

            #     totalInternetPlus = userTableArhiw.filter(b_internet__gte=0, etrap=etrap).aggregate(Sum('b_internet'))['b_internet__sum']
            #     totalInternetMinus = userTableArhiw.filter(b_internet__lte=0, etrap=etrap).aggregate(Sum('b_internet'))['b_internet__sum']
            #     context['totalInternetPlus'] = totalInternetPlus
            #     context['totalInternetMinus'] = totalInternetMinus

            #     totalKabelPlus = userTableArhiw.filter(b_kabel__gte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum']
            #     totalKabelMinus = userTableArhiw.filter(b_kabel__lte=0, etrap=etrap).aggregate(Sum('b_kabel'))['b_kabel__sum']
            #     context['totalKabelPlus'] = totalKabelPlus
            #     context['totalKabelMinus'] = totalKabelMinus

            #     totalAlemPlus = userTableArhiw.filter(b_alem__gte=0, etrap=etrap).aggregate(Sum('b_alem'))['b_alem__sum']
            #     totalAlemMinus = userTableArhiw.filter(b_alem__lte=0, etrap=etrap).aggregate(Sum('b_alem'))['b_alem__sum']
            #     context['totalAlemPlus'] = totalAlemPlus
            #     context['totalAlemMinus'] = totalAlemMinus

            #     MonthBalance.objects.create(
            #         year=current_year,
            #         month=monthСonvert(current_month),
            #         etrap=etrap,

            #         internetPlus=totalInternetPlus,
            #         kabelPlus=totalKabelPlus, 
            #         alemPlus=totalAlemPlus,
            #         telefonPlus=totalAbonplataPlus,
            #         slrPlus=totalSlrPlus,
            #         kodPlus=totalKodPlus,
            #         zakazPlus=totalZakazPlus,
            #         procheePlus=totalProcheePlus,
            #         dop_uslugiPlus=totalDop_uslugiPlus,

            #         internetMinus=totalInternetMinus,
            #         kabelMinus=totalKabelMinus, 
            #         alemMinus=totalAlemMinus,
            #         telefonMinus=totalAbonplataMinus,
            #         slrMinus=totalSlrMinus,
            #         kodMinus=totalKodMinus,
            #         zakazMinus=totalZakazMinus,
            #         procheeMinus=totalProcheeMinus,
            #         dop_uslugiMinus=totalDop_uslugiMinus,
            #         )
    # Если нажал на поиск по номеру
    if request.method == 'POST' and 'search_number' in request.POST:
        context['current_path'] = request.path
        
        number = re.sub('[-]', '', request.POST.get('search_number'))

        context['serach_number'] = request.POST.get('search_number')
        context['etrap'] = request.POST.get('etrap')

        pays_with_comment = PaysWithComment.objects.filter(number=number, etrap=request.POST.get('etrap'))
        context['pays_with_comment'] = pays_with_comment

        nach_with_comment = NachWithComment.objects.filter(number=number, etrap=request.POST.get('etrap'))
        context['nach_with_comment'] = nach_with_comment

        baza_info = BazaChangeInfo.objects.filter(number=number, etrap=request.POST.get('etrap'), date__year=request.POST.get('selected_year')).order_by('-date')
        context['baza_info'] = baza_info

        change_balance_with_comment = ChangeBalanceWithComment.objects.filter(number=number, etrap=request.POST.get('etrap'), date__year=request.POST.get('selected_year')).order_by('-date')
        context['change_balance_with_comment'] = change_balance_with_comment

        perek_nach_info = NachPerekidkaHistory.objects.filter(
            (Q(user1Etrap=request.POST.get('etrap')) & Q(user1Number=number) & Q(date__year=request.POST.get('selected_year'))) |
            (Q(user2Etrap=request.POST.get('etrap')) & Q(user2Number=number) & Q(date__year=request.POST.get('selected_year')))
            ).order_by('-date')
        context['perek_nach_info'] = perek_nach_info

        # perekidka_info = PerekidkaInfoNew.objects.filter(
        #         (Q(user1Number=number) & Q(user1Etrap=request.POST.get('etrap'))) |
        #         (Q(user2Number=number) & Q(user2Etrap=request.POST.get('etrap')))
        #     ).order_by('-date')

        selected_year = request.POST.get('selected_year')
        context['selected_year'] = selected_year

        if request.POST.get('etrap') == 'Dashoguz':

            user_kabel = False
            try:
                user_kabel = KabelTvNew.objects.get(number=number)
            except:
                pass
            if user_kabel:
                kabel_pays = user_kabel.kabeltvpayhistory_set.filter(pay_date__year=selected_year).order_by('-pay_date')
                context['kabel_pays'] = kabel_pays
                user_kabel_coment = user_kabel.kabelcomment_set.filter(comment_add_date__year=selected_year).order_by('-comment_add_date')
                print('user_kabel_coment1', kabel_pays)
                context['user_kabel_coment'] = user_kabel_coment
                if kabel_pays:
                    total_p_kabel = 0
                    for p in kabel_pays:
                        total_p_kabel += p.pay
                    context['total_p_kabel'] = total_p_kabel
                nach_history_kabel = user_kabel.kabelnach_set.filter(year=selected_year)
                if nach_history_kabel:
                    total_n_kabel = 0
                    for n in nach_history_kabel:
                        total_n_kabel += n.nach
                    context['total_n_kabel'] = total_n_kabel

            if selected_year != current_year:
                try:
                    user_kabel_sal_bal = SaldoBalancePoGodam.objects.get(year=selected_year, number=number, etrap=request.POST.get('etrap'))
                    if user_kabel_sal_bal.kabel_count > 0:
                        context['user_kabel_sal_bal'] = user_kabel_sal_bal
                except:
                    pass
            else:
                if user_kabel:
                    context['user_kabel'] = user_kabel
            
            



        # new 27.12.2024
        if selected_year != current_year:
            context['allow_to_pay'] = False
            try:
                saldo_balans = SaldoBalancePoGodam.objects.get(year=selected_year, etrap=request.POST.get('etrap'), number=number)
                context['saldo_balans'] = saldo_balans
            except:
                pass


        # new 27.12.2024 END


        # Если поиск кабельных абонентов без номеров через (ids)
        if 'kabelDropdownFilter' not in request.POST and 'kabelFilteredId' not in request.POST:
            if len(number) <= 4:
                messages.error(request, f'Ошибка {request.POST.get("search_number")}')
                return render(request, 'telekom/Kassa/kassaIndex.html', context)
                
                context['selected_year'] = request.POST.get('selected_year')
                abonent = UserTable.objects.filter(ids=number, etrap=request.POST.get('etrap'))
                try:
                    abonent = UserTable.objects.get(ids=number, etrap=request.POST.get('etrap'))
                    context['abonent'] = abonent
                except:
                    abonent = False
                    messages.error(request, f'Ошибка {request.POST.get("search_number")}')

                if abonent:

                    pay_history = abonent.payhistory_set.filter(date__year=selected_year).order_by('-date')
                    context['lastPays'] = pay_history
                    total_p_tel = 0
                    total_p_int = 0
                    total_p_alem = 0
                    for p in pay_history:
                        total_p_tel += p.telefon + p.slr + p.kod + p.zakaz + p.prochee + p.dop_uslugi
                        total_p_int += p.internet
                        total_p_alem += p.alem
                    context['total_p_tel'] = total_p_tel
                    context['total_p_int'] = total_p_int
                    context['total_p_alem'] = total_p_alem

                    nach_history = abonent.nachminus_set.filter(year=selected_year)
                    if nach_history:
                        total_n_tel = 0
                        total_n_int = 0
                        total_n_alem = 0
                        for n in nach_history:
                            total_n_tel += n.telefon + n.slr + n.kod + n.zakaz + n.prochee + n.dop_uslugi
                            total_n_int += n.internet
                            total_n_alem += n.alem
                        context['total_n_tel'] = total_n_tel
                        context['total_n_int'] = total_n_int
                        context['total_n_alem'] = total_n_alem

                    # new для показа истории оплат кабельного если есть 27.12.2024
                    if request.POST.get('etrap') == 'Dashoguz':
                        user_kabel = False
                        try:
                            user_kabel = KabelTvNew.objects.get(number=number)
                        except:
                            pass
                        if user_kabel:
                            context['user_kabel'] = user_kabel
                            kabel_pays = user_kabel.kabeltvpayhistory_set.filter(pay_date__year=selected_year).order_by('-pay_date')
                            context['kabel_pays'] = kabel_pays
                            user_kabel_coment = user_kabel.kabelcomment_set.filter(comment_add_date__year=selected_year).order_by('-comment_add_date')
                            context['user_kabel_coment'] = user_kabel_coment
                            if kabel_pays:
                                total_p_kabel = 0
                                for p in kabel_pays:
                                    total_p_kabel += p.pay
                                context['total_p_kabel'] = total_p_kabel
                            
                            nach_history_kabel = user_kabel.kabelnach_set.filter(year=selected_year)
                            if nach_history_kabel:
                                total_n_kabel = 0
                                for n in nach_history_kabel:
                                    total_n_kabel += n.nach
                                context['total_n_kabel'] = total_n_kabel



            else:

                try:
                    abonent = UserTable.objects.get(number=number, etrap=request.POST.get('etrap'))
                    context['abonent'] = abonent

                except:
                    abonent = False
                    messages.error(request, f'Ошибка {request.POST.get("search_number")}')
                if abonent:
                    # new для показа истории оплат кабельного если есть 27.12.2024
                    selected_year = request.POST.get('selected_year')

                   
                    pay_history = abonent.payhistory_set.filter(date__year=selected_year).order_by('-date')
                    context['lastPays'] = pay_history
                    total_p_tel = 0
                    total_p_int = 0
                    total_p_alem = 0
                    if pay_history:
                        for p in pay_history:
                            total_p_tel += p.telefon + p.slr + p.kod + p.zakaz + p.prochee + p.dop_uslugi
                            total_p_int += p.internet
                            total_p_alem += p.alem
                        context['total_p_tel'] = total_p_tel
                        context['total_p_int'] = total_p_int
                        context['total_p_alem'] = total_p_alem

                    nach_history = abonent.nachminus_set.filter(year=selected_year)
                    if nach_history:
                        total_n_tel = 0
                        total_n_int = 0
                        total_n_alem = 0
                        for n in nach_history:
                            total_n_tel += n.telefon + n.slr + n.kod + n.zakaz + n.prochee + n.dop_uslugi
                            total_n_int += n.internet
                            total_n_alem += n.alem
                        context['total_n_tel'] = total_n_tel
                        context['total_n_int'] = total_n_int
                        context['total_n_alem'] = total_n_alem

                    if request.POST.get('etrap') == 'Dashoguz':
                        user_kabel = False
                        try:
                            user_kabel = KabelTvNew.objects.get(number=number)
                        except:
                            pass
                        if user_kabel:
                            context['user_kabel'] = user_kabel
                            kabel_pays = user_kabel.kabeltvpayhistory_set.filter(pay_date__year=selected_year).order_by('-pay_date')
                            context['kabel_pays'] = kabel_pays
                            user_kabel_coment = user_kabel.kabelcomment_set.filter(comment_add_date__year=selected_year).order_by('-comment_add_date')
                            context['user_kabel_coment'] = user_kabel_coment
                            if kabel_pays:
                                total_p_kabel = 0
                                for p in kabel_pays:
                                    total_p_kabel += p.pay
                                context['total_p_kabel'] = total_p_kabel

                            nach_history_kabel = user_kabel.kabelnach_set.filter(year=selected_year)
                            if nach_history_kabel:
                                total_n_kabel = 0
                                for n in nach_history_kabel:
                                    total_n_kabel += n.nach
                                context['total_n_kabel'] = total_n_kabel

        # Ищем есть ли перекидки new
        # Если этрап не Dashoguz то поиск по кабелям нельзя делать
        if request.POST.get('etrap') == 'Dashoguz':
            perekidka_info = PerekidkaInfoNew.objects.filter(
                (Q(user1Number=number) & Q(user1Etrap=request.POST.get('etrap')) & Q(date__year=request.POST.get('selected_year'))) |
                (Q(user2Number=number) & Q(user2Etrap=request.POST.get('etrap')) & Q(date__year=request.POST.get('selected_year'))) |
                (Q(user2KabelNumber=number) & Q(date__year=request.POST.get('selected_year'))) |
                (Q(user1KabelNumber=number) & Q(date__year=request.POST.get('selected_year')))
            ).order_by('-date')
            context['perekidka_info'] = perekidka_info
        else:
            perekidka_info = PerekidkaInfoNew.objects.filter(
                (Q(user1Number=number) & Q(user1Etrap=request.POST.get('etrap')) & Q(date__year=request.POST.get('selected_year'))) |
                (Q(user2Number=number) & Q(user2Etrap=request.POST.get('etrap')) & Q(date__year=request.POST.get('selected_year')))
            ).order_by('-date')
            context['perekidka_info'] = perekidka_info
        ruchnoe_nach_info = NachislitWruchnuyuHistory.objects.filter(number=number, etrap=request.POST.get('etrap'), date__year=request.POST.get('selected_year'))
        context['ruchnoe_nach_info'] = ruchnoe_nach_info


        # Если нажал на поиск по Q для оплаты Кабель TV
        if request.method == 'POST' and 'kabelDropdownFilter' in request.POST:
            surname = request.POST.get('surname') if request.POST.get('surname') != None else ''
            name = request.POST.get('name') if request.POST.get('name') != None else ''
            street = request.POST.get('street') if request.POST.get('street') != None else ''
            home = request.POST.get('home') if request.POST.get('home') != None else ''
            flat = request.POST.get('flat') if request.POST.get('flat') != None else ''
            sotowyy = request.POST.get('sotowyy') if request.POST.get('sotowyy') != None else ''

            context['kabelFilterSurname'] = surname
            context['kabelFilterName'] = name
            context['kabelFilterStreet'] = street
            context['kabelFilterHome'] = home
            context['kabelFilterFlat'] = flat
            context['kabelFilterSotowyy'] = sotowyy
            context['kabelFilterEtrap'] = request.POST.get('etrap') if request.POST.get('etrap') != None else log



            abonent = UserTable.objects.filter(
                Q(etrap=request.POST.get('etrap')),
                Q(surname__icontains=surname) &
                Q(name__icontains=name) &
                Q(street__icontains=street) &
                Q(home__icontains=home) &
                Q(flat__icontains=flat) &
                Q(sotowyy__icontains=sotowyy)
            )


            if len(abonent) == 1:
                abonent = abonent[0]
                context['abonent'] = abonent
                pay_history = abonent.payhistory_set.filter(date__year=selected_year).order_by('-date')
                context['lastPays'] = pay_history
                total_p_tel = 0
                total_p_int = 0
                total_p_alem = 0
                if pay_history:
                    for p in pay_history:
                        total_p_tel += p.telefon + p.slr + p.kod + p.zakaz + p.prochee + p.dop_uslugi
                        total_p_int += p.internet
                        total_p_alem += p.alem
                    context['total_p_tel'] = total_p_tel
                    context['total_p_int'] = total_p_int
                    context['total_p_alem'] = total_p_alem
                
                nach_history = abonent.nachminus_set.filter(year=selected_year)
                if nach_history:
                    total_n_tel = 0
                    total_n_int = 0
                    total_n_alem = 0
                    for n in nach_history:
                        total_n_tel += n.telefon + n.slr + n.kod + n.zakaz + n.prochee + n.dop_uslugi
                        total_n_int += n.internet
                        total_n_alem += n.alem
                    context['total_n_tel'] = total_n_tel
                    context['total_n_int'] = total_n_int
                    context['total_n_alem'] = total_n_alem


                # new для показа истории оплат кабельного если есть 27.12.2024
                if request.POST.get('etrap') == 'Dashoguz':
                    user_kabel = False
                    try:
                        user_kabel = KabelTvNew.objects.get(number=number)
                    except:
                        pass
                    if user_kabel:
                        context['user_kabel'] = user_kabel
                        kabel_pays = user_kabel.kabeltvpayhistory_set.filter(pay_date__year=selected_year).order_by('-pay_date')
                        context['kabel_pays'] = kabel_pays
                        user_kabel_coment = user_kabel.kabelcomment_set.filter(comment_add_date__year=selected_year).order_by('-comment_add_date')
                        context['user_kabel_coment'] = user_kabel_coment
                        if kabel_pays:
                            total_p_kabel = 0
                            for p in kabel_pays:
                                total_p_kabel += p.pay
                            context['total_p_kabel'] = total_p_kabel

                        nach_history_kabel = user_kabel.kabelnach_set.filter(year=selected_year)
                        if nach_history_kabel:
                            total_n_kabel = 0
                            for n in nach_history_kabel:
                                total_n_kabel += n.nach
                            context['total_n_kabel'] = total_n_kabel

                if abonent.number:
                    context['serach_number'] = f"{abonent.number[0]}-{abonent.number[1:3]}-{abonent.number[3:]}"
            elif len(abonent) > 1:
                context['abonents'] = abonent[:100]
                return render(request, 'telekom/Kassa/kassaIndex.html', context)
            else:
                abonent = False
                messages.error(request, f'Ошибка {request.POST.get("search_number")}')

        # Если выбрал в списке фильтрованных абонентов для kabel id
        if request.method == 'POST' and 'kabelFilteredId' in request.POST:
            abonent = UserTable.objects.get(pk=request.POST.get('kabelFilteredId'))
            context['abonent'] = abonent
            pay_history = abonent.payhistory_set.filter(date__year=selected_year).order_by('-date')
            context['lastPays'] = pay_history
            total_p_tel = 0
            total_p_int = 0
            total_p_alem = 0
            if pay_history:
                for p in pay_history:
                    total_p_tel += p.telefon + p.slr + p.kod + p.zakaz + p.prochee + p.dop_uslugi
                    total_p_int += p.internet
                    total_p_alem += p.alem
                context['total_p_tel'] = total_p_tel
                context['total_p_int'] = total_p_int
                context['total_p_alem'] = total_p_alem
            
            nach_history = abonent.nachminus_set.filter(year=selected_year)
            if nach_history:
                total_n_tel = 0
                total_n_int = 0
                total_n_alem = 0
                for n in nach_history:
                    total_n_tel += n.telefon + n.slr + n.kod + n.zakaz + n.prochee + n.dop_uslugi
                    total_n_int += n.internet
                    total_n_alem += n.alem
                context['total_n_tel'] = total_n_tel
                context['total_n_int'] = total_n_int
                context['total_n_alem'] = total_n_alem
            

            # new для показа истории оплат кабельного если есть 27.12.2024
            if request.POST.get('etrap') == 'Dashoguz':
                user_kabel = False
                try:
                    user_kabel = KabelTvNew.objects.get(number=number)
                except:
                    pass
                if user_kabel:
                    context['user_kabel'] = user_kabel
                    kabel_pays = user_kabel.kabeltvpayhistory_set.filter(pay_date__year=selected_year).order_by('-pay_date')
                    context['kabel_pays'] = kabel_pays
                    user_kabel_coment = user_kabel.kabelcomment_set.filter(comment_add_date__year=selected_year).order_by('-comment_add_date')
                    context['user_kabel_coment'] = user_kabel_coment
                    if kabel_pays:
                        total_p_kabel = 0
                        for p in kabel_pays:
                            total_p_kabel += p.pay
                        context['total_p_kabel'] = total_p_kabel

                    nach_history_kabel = user_kabel.kabelnach_set.filter(year=selected_year)
                    if nach_history_kabel:
                        total_n_kabel = 0
                        for n in nach_history_kabel:
                            total_n_kabel += n.nach
                        context['total_n_kabel'] = total_n_kabel

            context['serach_number'] = f"{abonent.number[0]}-{abonent.number[1:3]}-{abonent.number[3:]}"
            context['kabelFilterSurname'] = abonent.surname
            context['kabelFilterName'] = abonent.name
            context['kabelFilterStreet'] = abonent.street
            context['kabelFilterHome'] = abonent.home
            context['kabelFilterFlat'] = abonent.flat
            context['kabelFilterSotowyy'] = abonent.sotowyy

        if abonent:
            try:
                with transaction.atomic():
                    # распределяем прочее с внешних платежей по полям у которых баланc минусовые
                    # new
                    if abonent.b_telefon != 0 or abonent.b_slr != 0 or abonent.b_kod != 0 or abonent.b_zakaz != 0 or abonent.b_dop_uslugi != 0:
                        abonent.b_prochee = abonent.b_telefon + abonent.b_slr + abonent.b_kod + abonent.b_zakaz + abonent.b_prochee + abonent.b_dop_uslugi
                        abonent.b_telefon = 0
                        abonent.b_slr = 0
                        abonent.b_kod = 0
                        abonent.b_zakaz = 0
                        abonent.b_dop_uslugi = 0

                    # # old
                    # if abonent.b_prochee > 0:
                    #     telefonAuto = 0
                    #     slrAuto = 0
                    #     kodAuto = 0
                    #     zakazAuto = 0
                    #     dop_uslugiAuto = 0
                    #     if abonent.b_telefon < 0 and abs(abonent.b_telefon) <= abonent.b_prochee:
                    #         telefonAuto = abs(abonent.b_telefon)
                    #         abonent.b_prochee -= abs(abonent.b_telefon)
                    #         abonent.b_telefon = 0
                    #     elif abonent.b_telefon < 0 and abs(abonent.b_telefon) > abonent.b_prochee:
                    #         telefonAuto = abonent.b_prochee
                    #         abonent.b_telefon += abonent.b_prochee
                    #         abonent.b_prochee = 0

                    #     if abonent.b_prochee > 0:
                    #         if abonent.b_slr < 0 and abs(abonent.b_slr) <= abonent.b_prochee:
                    #             slrAuto = abs(abonent.b_slr)
                    #             abonent.b_prochee -= abs(abonent.b_slr)
                    #             abonent.b_slr = 0
                    #         elif abonent.b_slr < 0 and abs(abonent.b_slr) > abonent.b_prochee:
                    #             slrAuto = abonent.b_prochee
                    #             abonent.b_slr += abonent.b_prochee
                    #             abonent.b_prochee = 0

                    #     if abonent.b_prochee > 0:
                    #         if abonent.b_kod < 0 and abs(abonent.b_kod) <= abonent.b_prochee:
                    #             kodAuto = abs(abonent.b_kod)
                    #             abonent.b_prochee -= abs(abonent.b_kod)
                    #             abonent.b_kod = 0  
                    #         elif abonent.b_kod < 0 and abs(abonent.b_kod) > abonent.b_prochee:
                    #             kodAuto = abonent.b_prochee
                    #             abonent.b_kod += abonent.b_prochee
                    #             abonent.b_prochee = 0

                    #     if abonent.b_prochee > 0:
                    #         if abonent.b_zakaz < 0 and abs(abonent.b_zakaz) <= abonent.b_prochee:
                    #             zakazAuto = abs(abonent.b_zakaz)
                    #             abonent.b_prochee -= abs(abonent.b_zakaz)
                    #             abonent.b_zakaz = 0
                    #         elif abonent.b_zakaz < 0 and abs(abonent.b_zakaz) > abonent.b_prochee:
                    #             zakazAuto = abonent.b_prochee
                    #             abonent.b_zakaz += abonent.b_prochee
                    #             abonent.b_prochee = 0

                    #     if abonent.b_prochee > 0:
                    #         if abonent.b_dop_uslugi < 0 and abs(abonent.b_dop_uslugi) <= abonent.b_prochee:
                    #             dop_uslugiAuto = abs(abonent.b_dop_uslugi)
                    #             abonent.b_prochee -= abs(abonent.b_dop_uslugi)
                    #             abonent.b_dop_uslugi = 0                    
                    #         elif abonent.b_dop_uslugi < 0 and abs(abonent.b_dop_uslugi) > abonent.b_prochee:
                    #             dop_uslugiAuto =  abonent.b_prochee
                    #             abonent.b_dop_uslugi += abonent.b_prochee
                    #             abonent.b_prochee = 0
                     
                        abonent.save()
            except Exception as e:
                messages.error(request, f'Откат расппределения прочее ошибка с transaction == {e}')
                logger.error(f'==== Откат расппределения прочее ошибка с transaction при перекидке баланса == {e}')






            # Находим общую сумму услуг если есть
            if current_year == selected_year:
                if abonent.service:
                    service_total_sum = 0
                    for service in abonent.service.all():
                        service_total_sum += service.price
                context['service_total_sum'] = service_total_sum
            else:
                if saldo_balans.service:
                    service_total_sum_saldo_balans = 0
                    for service in saldo_balans.service.all():
                        service_total_sum_saldo_balans += service.price
                context['service_total_sum_saldo_balans'] = service_total_sum_saldo_balans
                


            # new для показа истории начислений кабельного если есть 27.12.2024
            if request.POST.get('etrap') == 'Dashoguz':
                user_kabel = False
                try:
                    user_kabel = KabelTvNew.objects.get(number=number)
                    context['user_kabel'] = user_kabel
                except:
                    pass
                if user_kabel:
                    context['user_kabel'] = user_kabel
                    context['count_k'] = user_kabel.count

                    kabel_nachs = user_kabel.kabelnach_set.filter(year=selected_year)
                    context['kabel_nachs'] = kabel_nachs
                    for i in kabel_nachs:
                        if i.month == '01':
                            jank = i.nach
                            context['jank'] = jank
                        if i.month == '02':
                            febk = i.nach
                            context['febk'] = febk
                        if i.month == '03':
                            mark = i.nach
                            context['mark'] = mark
                        if i.month == '04':
                            aprk = i.nach
                            context['aprk'] = aprk
                        if i.month == '05':
                            mayk = i.nach
                            context['mayk'] = mayk
                        if i.month == '06':
                            junk = i.nach
                            context['junk'] = junk
                        if i.month == '07':
                            julk = i.nach
                            context['julk'] = julk
                        if i.month == '08':
                            augk = i.nach
                            context['augk'] = augk
                        if i.month == '09':
                            sepk = i.nach
                            context['sepk'] = sepk
                        if i.month == '10':
                            oktk = i.nach
                            context['oktk'] = oktk
                        if i.month == '11':
                            novk = i.nach
                            context['novk'] = novk
                        if i.month == '12':
                            deck = i.nach
                            context['deck'] = deck
                        
           

            nachMinus = NachMinus.objects.filter(user=abonent)
            try:
                context['jan'] = nachMinus.get(user=abonent, year=selected_year, month='01')
                if nachMinus.get(user=abonent, year=selected_year, month='01').dop_usligi_added_Pk:
                    added = eval(nachMinus.get(user=abonent, year=selected_year, month='01').dop_usligi_added_Pk)
                    end_list = []
                    for i in range(len(added['added'])):
                        start_list = []
                        date_ = added['added'][i][-2]
                        nach = added['added'][i][-1]
                        start_list.append(date_)
                        start_list.append(nach)
                        start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                        end_list.append(start_list)
                    context['end_list_jan'] = end_list
            except: 
                pass

            try:
                get_user =  PayHistory.objects.filter(abonent__number='61457', abonent__etrap='Dashoguz', telefon=1)
            except:
                get_user = None

            try:
                context['feb'] = nachMinus.get(user=abonent, year=selected_year, month='02')
                if nachMinus.get(user=abonent, year=selected_year, month='02').dop_usligi_added_Pk:
                    added = eval(nachMinus.get(user=abonent, year=selected_year, month='02').dop_usligi_added_Pk)
                    end_list = []
                    for i in range(len(added['added'])):
                        start_list = []
                        date_ = added['added'][i][-2]
                        nach = added['added'][i][-1]
                        start_list.append(date_)
                        start_list.append(nach)
                        start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                        end_list.append(start_list)
                    context['end_list_feb'] = end_list
            except: 
                pass
            try:
                context['mar'] = nachMinus.get(user=abonent, year=selected_year, month='03')
                if nachMinus.get(user=abonent, year=selected_year, month='03').dop_usligi_added_Pk:
                    added = eval(nachMinus.get(user=abonent, year=selected_year, month='03').dop_usligi_added_Pk)
                    end_list = []
                    for i in range(len(added['added'])):
                        start_list = []
                        date_ = added['added'][i][-2]
                        nach = added['added'][i][-1]
                        start_list.append(date_)
                        start_list.append(nach)
                        start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                        end_list.append(start_list)
                    context['end_list_mar'] = end_list
            except: 
                pass
            try:
                context['apr'] = nachMinus.get(user=abonent, year=selected_year, month='04')
                if nachMinus.get(user=abonent, year=selected_year, month='04').dop_usligi_added_Pk:
                    added = eval(nachMinus.get(user=abonent, year=selected_year, month='04').dop_usligi_added_Pk)
                    end_list = []
                    for i in range(len(added['added'])):
                        start_list = []
                        date_ = added['added'][i][-2]
                        nach = added['added'][i][-1]
                        start_list.append(date_)
                        start_list.append(nach)
                        start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                        end_list.append(start_list)
                    context['end_list_apr'] = end_list
            except: 
                pass
            try:
                context['may'] = nachMinus.get(user=abonent, year=selected_year, month='05')
                if nachMinus.get(user=abonent, year=selected_year, month='05').dop_usligi_added_Pk:
                    added = eval(nachMinus.get(user=abonent, year=selected_year, month='05').dop_usligi_added_Pk)
                    end_list = []
                    for i in range(len(added['added'])):
                        start_list = []
                        date_ = added['added'][i][-2]
                        nach = added['added'][i][-1]
                        start_list.append(date_)
                        start_list.append(nach)
                        start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                        end_list.append(start_list)
                    context['end_list_may'] = end_list
            except: 
                pass
            try:
                context['jun'] = nachMinus.get(user=abonent, year=selected_year, month='06')
                if nachMinus.get(user=abonent, year=selected_year, month='06').dop_usligi_added_Pk:
                    added = eval(nachMinus.get(user=abonent, year=selected_year, month='06').dop_usligi_added_Pk)
                    end_list = []
                    for i in range(len(added['added'])):
                        start_list = []
                        date_ = added['added'][i][-2]
                        nach = added['added'][i][-1]
                        start_list.append(date_)
                        start_list.append(nach)
                        start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                        end_list.append(start_list)
                    context['end_list_jun'] = end_list
            except: 
                pass
            try:
                context['jul'] = nachMinus.get(user=abonent, year=selected_year, month='07')
                if nachMinus.get(user=abonent, year=selected_year, month='07').dop_usligi_added_Pk:
                    added = eval(nachMinus.get(user=abonent, year=selected_year, month='07').dop_usligi_added_Pk)
                    end_list = []
                    for i in range(len(added['added'])):
                        start_list = []
                        date_ = added['added'][i][-2]
                        nach = added['added'][i][-1]
                        start_list.append(date_)
                        start_list.append(nach)
                        start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                        end_list.append(start_list)
                    context['end_list_jul'] = end_list
            except: 
                pass
            try:
                context['aug'] = nachMinus.get(user=abonent, year=selected_year, month='08')
                if nachMinus.get(user=abonent, year=selected_year, month='08').dop_usligi_added_Pk:
                    added = eval(nachMinus.get(user=abonent, year=selected_year, month='08').dop_usligi_added_Pk)
                    end_list = []
                    for i in range(len(added['added'])):
                        start_list = []
                        date_ = added['added'][i][-2]
                        nach = added['added'][i][-1]
                        start_list.append(date_)
                        start_list.append(nach)
                        start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                        end_list.append(start_list)
                    context['end_list_aug'] = end_list
            except: 
                pass
            try:
                context['sep'] = nachMinus.get(user=abonent, year=selected_year, month='09')
                if nachMinus.get(user=abonent, year=selected_year, month='09').dop_usligi_added_Pk:
                    added = eval(nachMinus.get(user=abonent, year=selected_year, month='09').dop_usligi_added_Pk)
                    end_list = []
                    for i in range(len(added['added'])):
                        start_list = []
                        date_ = added['added'][i][-2]
                        nach = added['added'][i][-1]
                        start_list.append(date_)
                        start_list.append(nach)
                        start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                        end_list.append(start_list)
                    context['end_list_sep'] = end_list
            except: 
                pass
            try:
                context['oct'] = nachMinus.get(user=abonent, year=selected_year, month='10')
                if nachMinus.get(user=abonent, year=selected_year, month='10').dop_usligi_added_Pk:
                    added = eval(nachMinus.get(user=abonent, year=selected_year, month='10').dop_usligi_added_Pk)
                    end_list = []
                    for i in range(len(added['added'])):
                        start_list = []
                        date_ = added['added'][i][-2]
                        nach = added['added'][i][-1]
                        start_list.append(date_)
                        start_list.append(nach)
                        start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                        end_list.append(start_list)
                    context['end_list_oct'] = end_list
            except: 
                pass
            try:
                context['nov'] = nachMinus.get(user=abonent, year=selected_year, month='11')
                if nachMinus.get(user=abonent, year=selected_year, month='11').dop_usligi_added_Pk:
                    added = eval(nachMinus.get(user=abonent, year=selected_year, month='11').dop_usligi_added_Pk)
                    end_list = []
                    for i in range(len(added['added'])):
                        start_list = []
                        date_ = added['added'][i][-2]
                        nach = added['added'][i][-1]
                        start_list.append(date_)
                        start_list.append(nach)
                        start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                        end_list.append(start_list)
                    context['end_list_nov'] = end_list
            except: 
                pass
            try:
                context['dec'] = nachMinus.get(user=abonent, year=selected_year, month='12')
                if nachMinus.get(user=abonent, year=selected_year, month='12').dop_usligi_added_Pk:
                    added = eval(nachMinus.get(user=abonent, year=selected_year, month='12').dop_usligi_added_Pk)
                    end_list = []
                    for i in range(len(added['added'])):
                        start_list = []
                        date_ = added['added'][i][-2]
                        nach = added['added'][i][-1]
                        start_list.append(date_)
                        start_list.append(nach)
                        start_list.append(AbonentService.objects.filter(pk__in=added['added'][i][:-2]))
                        end_list.append(start_list)
                    context['end_list_dec'] = end_list
            except: 
                pass

            if get_user:
                return redirect('kassa-index')
            else:
                allUsers = UserTable.objects.all()

    # print('dada', request.META.get('HTTP_X_FORWARDED_FOR'))
    # print('dada', request.META.get('HTTP_X_FORWARDED_HOST'))
    # print('dada', request.META.get('REMOTE_ADDR'))

    # если нажал на оплатить в oplataModal
    if request.method == 'POST' and 'oplata_serach_number' in request.POST:
        try:
            with transaction.atomic():
                number = re.sub('[-]', '', request.POST.get('oplata_serach_number'))
                context['serach_number'] = request.POST.get('oplata_serach_number')
                context['etrap'] = request.POST.get('etrap')
                abonent = UserTable.objects.get(pk=request.POST.get('user_id'))
                context['abonent'] = abonent
                selected_year = request.POST.get('selected_year')
                context['selected_year'] = selected_year

                ip_kassa = {
                    '145.9.17.63': 'kassa 6',
                    '145.9.17.61': 'kassa 1', 
                    '145.9.17.70': 'kassa 2',
                    '145.9.17.68': 'kassa 5',
                    '145.9.17.69': 'kassa 4', 
                    '145.9.17.62': 'kassa 3', 
                    '145.9.17.34': 'kassa 7',
                    '192.168.30.215': 'Bahar Nazarowa Koneurgench'
                    }
                kassa = request.META.get('REMOTE_ADDR') if request.META.get('REMOTE_ADDR') not in ip_kassa else ip_kassa[request.META.get('REMOTE_ADDR')]




                # Создаем квитанцию (чек)
                if abonent.is_enterprises:
                    edara_ilat = 'ЮЛ'
                else:
                    edara_ilat = 'ФЛ'

                # if request.POST.get('kabel') and log == 'Dashoguz':
                #     try:
                #         k_user_new = False
                #         k_user = KabelTvNew.objects.get(number=abonent.number)
                #     except:
                #         k_user_new = True
                #         k_user = KabelTvNew.objects.create(
                #             number=abonent.number,
                #             surname = abonent.surname,
                #             name = abonent.name,
                #             street = abonent.street,
                #             home = abonent.home,
                #             flat = abonent.flat,
                #             sotowyy = '',
                #             is_enterprises = False,
                #             is_active = False,
                #             count = 1
                #             )

                #     if k_user_new:    
                #         KabelComment.objects.create(
                #             user = k_user,
                #             worker = request.user.username,
                #             comment = f"Добавление абонента {datetime.now()} , Создан при оплате кассирами (Возможно ошибочный платеж)",
                #             action = 'Добавление абонента'
                #         )
                    
                #     KabelTvPayHistory.objects.create(
                #     user = k_user,
                #     pay = request.POST.get('kabel'),
                #     pay_kassir = request.user.username,
                #     card = True if request.POST.get('is_card') == 'on' else False,
                #     pay_date = datetime.now()
                #     )     
                #     k_user.balance += float(request.POST.get('kabel'))   
                #     k_user.save()

                payHistory = PayHistory.objects.create(
                    abonent=abonent, 
                    telefon=request.POST.get('abonplata') if request.POST.get('abonplata') != '' else 0,
                    slr=request.POST.get('slr') if request.POST.get('slr') != '' else 0,
                    kod=request.POST.get('kod') if request.POST.get('kod') != '' else 0,
                    zakaz=request.POST.get('zakaz') if request.POST.get('zakaz') != '' else 0,
                    prochee=request.POST.get('prochee') if request.POST.get('prochee') != '' else 0,
                    alem=request.POST.get('alem') if request.POST.get('alem') != '' else 0,
                    internet=request.POST.get('internet') if request.POST.get('internet') != '' else 0,
                    dop_uslugi=request.POST.get('dop_uslugi') if request.POST.get('dop_uslugi') != '' else 0,
                    kabel=request.POST.get('kabel') if request.POST.get('kabel') != '' else 0,
                    is_card=True if request.POST.get('is_card') == 'on' else False,
                    kassir=request.user.username,
                    total=request.POST.get('summa_w_kassu'),
                    date = datetime.now(),
                    kassa=kassa,
                    edara_ilat=edara_ilat,
                    kassir_etrap=log,
                    type='Default'
                    )
                
                # плюсуем в балансе
                UserTable.objects.filter(pk=request.POST.get('user_id')).update(
                    b_telefon=(abonent.b_telefon + float(request.POST.get('abonplata'))) if request.POST.get('abonplata') else abonent.b_telefon,
                    b_slr=(abonent.b_slr + float(request.POST.get('slr'))) if request.POST.get('slr') else abonent.b_slr,
                    b_kod=(abonent.b_kod + float(request.POST.get('kod'))) if request.POST.get('kod') else abonent.b_kod,
                    b_zakaz=(abonent.b_zakaz + float(request.POST.get('zakaz'))) if request.POST.get('zakaz') else abonent.b_zakaz,
                    b_prochee=(abonent.b_prochee + float(request.POST.get('prochee'))) if request.POST.get('prochee') else abonent.b_prochee,
                    b_alem=(abonent.b_alem + float(request.POST.get('alem'))) if request.POST.get('alem') else abonent.b_alem,
                    b_internet=(abonent.b_internet + float(request.POST.get('internet'))) if request.POST.get('internet') else abonent.b_internet,
                    b_dop_uslugi=(abonent.b_dop_uslugi + float(request.POST.get('dop_uslugi'))) if request.POST.get('dop_uslugi') else abonent.b_dop_uslugi,
                    b_kabel=(abonent.b_kabel + float(request.POST.get('kabel'))) if request.POST.get('kabel') else abonent.b_kabel,
                    )
                
                # для показа историй оплат абонента
                pay_history = abonent.payhistory_set.filter(date__year=selected_year).order_by('-date')
                context['lastPays'] = pay_history
                total_p_tel = 0
                total_p_int = 0
                total_p_alem = 0
                if pay_history:
                    for p in pay_history:
                        total_p_tel += p.telefon + p.slr + p.kod + p.zakaz + p.prochee + p.dop_uslugi
                        total_p_int += p.internet
                        total_p_alem += p.alem
                    context['total_p_tel'] = total_p_tel
                    context['total_p_int'] = total_p_int
                    context['total_p_alem'] = total_p_alem

                nach_history = abonent.nachminus_set.filter(year=selected_year)
                if nach_history:
                    total_n_tel = 0
                    total_n_int = 0
                    total_n_alem = 0
                    for n in nach_history:
                        total_n_tel += n.telefon + n.slr + n.kod + n.zakaz + n.prochee + n.dop_uslugi
                        total_n_int += n.internet
                        total_n_alem += n.alem
                    context['total_n_tel'] = total_n_tel
                    context['total_n_int'] = total_n_int
                    context['total_n_alem'] = total_n_alem

                # new для показа истории оплат кабельного если есть 27.12.2024
                if request.POST.get('etrap') == 'Dashoguz':
                    user_kabel = False
                    try:
                        user_kabel = KabelTvNew.objects.get(number=number)
                    except:
                        pass
                    if user_kabel:
                        context['user_kabel'] = user_kabel
                        kabel_pays = user_kabel.kabeltvpayhistory_set.filter(pay_date__year=selected_year).order_by('-pay_date')
                        context['kabel_pays'] = kabel_pays
                        user_kabel_coment = user_kabel.kabelcomment_set.filter(comment_add_date__year=selected_year).order_by('-comment_add_date')
                        context['user_kabel_coment'] = user_kabel_coment
                        if kabel_pays:
                            total_p_kabel = 0
                            for p in kabel_pays:
                                total_p_kabel += p.pay
                            context['total_p_kabel'] = total_p_kabel

                        nach_history_kabel = user_kabel.kabelnach_set.filter(year=selected_year)
                        if nach_history_kabel:
                            total_n_kabel = 0
                            for n in nach_history_kabel:
                                total_n_kabel += n.nach
                            context['total_n_kabel'] = total_n_kabel


                # Обновляем context абонента
                abonent = UserTable.objects.get(pk=request.POST.get('user_id'))
                context['abonent'] = abonent

                # Для быстрой печати квитанции (чека)
                context['payHistory'] = payHistory


                # сохраняем для interpay
                InterpayBilling.objects.create(pay_history=payHistory)
        except Exception as e:
            messages.error(request, f'Откат платежа в кассе ошибка с transaction == {e}')
            logger.error(f'==== Откат платежа в кассе ошибка с transaction при перекидке баланса == {e}')

        



    try:
        perekInfoMinus = PerekidkaInfo.objects.filter(createDate__range = [f'{selected_year}-01-01', f'{selected_year}-12-31'], user1Etrap = abonent.etrap, user1Number = abonent.number)
        perekInfoPlus = PerekidkaInfo.objects.filter(createDate__range = [f'{selected_year}-01-01', f'{selected_year}-12-31'], user2Etrap = abonent.etrap, user2Number = abonent.number)
        context['perekInfoMinus'] = perekInfoMinus
        context['perekInfoPlus'] = perekInfoPlus
    except:
        pass
    
    return render(request, 'telekom/Kassa/kassaIndex.html', context)
