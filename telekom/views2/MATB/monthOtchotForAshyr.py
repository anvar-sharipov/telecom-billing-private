from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.models import ManagerNames, MonthBalance, NachMinus, NachMonthDebetKredet, NachisleniyaOtchet, NonLocalCall, PayHistory, PerekidkaInfo, SagidDecemberDebetKredet, UserTable, UserTableArhiw, KabelNach, KabelTvPayHistory
from django.db.models import Sum
from django.db.models import Q
import tablib

from telekom.views2.myFunc.myFunc import getPreviousMonth, loggedUserEtrapAndGroup, monthСonvert

from datetime import date, datetime, timedelta
from calendar import monthrange

from django.http import HttpResponse


WN_KASSIRS = ['E-government', 'Tolleg APP TMCELL', 'Saray Tolegy', 'Dostluk Bank', 'Turkmen Pochta', 'HalkBank Terminal Payments']


def monthOtchotForAshyr(request):

    context = {}
    current_date = str(date.today())
    context['current_date'] = current_date

    current_year = current_date[0:4]
    current_month = current_date[5:7]
    month_word = monthСonvert(current_month)
    days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]

    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    print('EtrapAndGroup[1]', EtrapAndGroup[1])
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
        context['matbIndex'] = True
        context['monthOtchotForAshyr'] = True
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    context['etraps'] = etraps
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

    etrap = request.GET.get('etrap')
    month = request.GET.get('month') if request.GET.get('month') != None else month_word
    year = request.GET.get('year') if request.GET.get('year') != None else current_year
    context['month'] = month
    context['year'] = year
    context['etrap'] = etrap

    days_in_choosed_month = monthrange(int(year), int(monthСonvert(month)))[1]

    if etrap and month and year:
        month_digit = monthСonvert(month)
        current_date = datetime.strptime(year + month_digit, '%Y%m')
        next_month_date = current_date + timedelta(days=days_in_choosed_month)
        nextYear = next_month_date.year
        nextMonth = next_month_date.month

        start = f"{year}-{month_digit}-01"
        end = f"{year}-{month_digit}-{days_in_choosed_month}"
        end2 = f"{nextYear}-{nextMonth}-01"

        start_for_pay_history = f"{year}-{month_digit}-01"
        end_for_pay_history = f"{year}-{month_digit}-{days_in_choosed_month} 23:59:59"

        nachMinus = NachMinus.objects.filter(year=year, month=month_digit, user__etrap=etrap, user__is_enterprises=False)

        managers = ManagerNames.objects.filter(etrap=etrap)
        wn = []
        managers_list = []
        for m in ManagerNames.objects.all():
            if m.etrap == 'Внешние платежи':
                wn.append(m.name)
            if m.etrap == etrap:
                managers_list.append(m.name)

        globalCall = NonLocalCall.objects.filter(DATE__range=[start, end2], SUB_A_etrap='Dashoguz')
        number_kod = {}
        for c in globalCall:
            if c.edara == 'I':
                if int(c.SUB_A) not in number_kod:
                    number_kod[int(c.SUB_A)] = c.total_price
                else:
                    number_kod[int(c.SUB_A)] = c.total_price

        sagitSaldoDict = {}  # {number: list[46]}

        kabelNew_number_nach = {}
        kabelNewUsersNach = KabelNach.objects.filter(year=year, month=monthСonvert(month), user__is_enterprises=False)
        for u in kabelNewUsersNach:
            kabelNew_number_nach[u.user.number] = u.nach

        # Индексы списка (46 элементов, 0..45):
        # [0]  DT
        # [1]  KT
        # [2]  telefon nach
        # [3]  slr nach
        # [4]  kod nach
        # [5]  zakaz nach
        # [6]  prochee nach (0)
        # [7]  dop_uslugi nach
        # [8]  internet nach
        # [9]  kabel nach (из KabelNach)
        # [10] alem nach
        # [11] wsego nach (не используется)
        # --- КАССА ---
        # [12] kassa_internet
        # [13] kassa_alem
        # [14] kassa_abonplata  (prochee)
        # [15] kassa_kabel_tv   (из KabelTvPayHistory, только Dashoguz)
        # [16] kassa_itogo
        # --- E-government ---
        # [17] egov_internet
        # [18] egov_alem
        # [19] egov_abonplata
        # [20] egov_itogo
        # --- Tolleg APP TMCELL ---
        # [21] tolleg_internet
        # [22] tolleg_alem
        # [23] tolleg_abonplata
        # [24] tolleg_itogo
        # --- Saray Tolegy ---
        # [25] saray_internet
        # [26] saray_alem
        # [27] saray_abonplata
        # [28] saray_itogo
        # --- Dostluk Bank ---
        # [29] dostluk_internet
        # [30] dostluk_alem
        # [31] dostluk_abonplata
        # [32] dostluk_itogo
        # --- Turkmen Pochta ---
        # [33] pochta_internet
        # [34] pochta_alem
        # [35] pochta_abonplata
        # [36] pochta_itogo
        # --- HalkBank ---
        # [37] halk_internet
        # [38] halk_alem
        # [39] halk_abonplata
        # [40] halk_itogo
        # --- Dealers ---
        # [41] dealers_internet
        # [42] dealers_alem
        # [43] dealers_abonplata
        # [44] dealers_itogo
        # --- Общий итог ---
        # [45] wsego_oplacheno

        for i in range(20000, 80000):
            if i in kabelNew_number_nach and etrap == 'Dashoguz':
                row = [0] * 46
                row[9] = kabelNew_number_nach[i]
                sagitSaldoDict[i] = row
            else:
                sagitSaldoDict[i] = [0] * 46

        for i in range(90000, 105000):
            if i in kabelNew_number_nach and etrap == 'Dashoguz':
                row = [0] * 46
                row[9] = kabelNew_number_nach[i]
                sagitSaldoDict[i] = row
            else:
                sagitSaldoDict[i] = [0] * 46

        # Начисления
        for n in nachMinus:
            lst = sagitSaldoDict[int(n.user.number)]
            lst[2] = n.telefon
            lst[3] = n.slr
            lst[4] = n.kod
            lst[5] = n.zakaz
            lst[6] = 0
            lst[7] = n.dop_uslugi
            lst[8] = n.internet
            lst[10] = n.alem

        # --- КАССА (PayHistory без внешних) ---
        pays_kassa = PayHistory.objects.filter(
            date__range=[start_for_pay_history, end_for_pay_history],
            edara_ilat='ФЛ',
            abonent__etrap=etrap
        ).exclude(kassir_etrap='Внешние платежи')

        print('len_pays_kassa', len(pays_kassa))
        for p in pays_kassa:
            if p.abonent.number == '93095':
                print('da', p.abonent.number)
            lst = sagitSaldoDict[int(p.abonent.number)]
            lst[12] += p.internet
            lst[13] += p.alem
            lst[14] += p.prochee

        # --- КАССА Кабель TV (KabelTvPayHistory, только Dashoguz, только кассовые) ---
        if etrap == 'Dashoguz':
            kabel_pays = KabelTvPayHistory.objects.filter(
                pay_date__range=[start_for_pay_history, end_for_pay_history],
                user__is_enterprises=False
            )
            for p in kabel_pays:
                lst = sagitSaldoDict[int(p.user.number)]
                is_wn = any(wn_name in p.pay_kassir for wn_name in WN_KASSIRS)
                if not is_wn:
                    lst[15] += p.pay  # kassa_kabel_tv

        # --- ВНЕШНИЕ ПЛАТЕЖИ (PayHistory с kassir_etrap='Внешние платежи') ---
        pays_wn = PayHistory.objects.filter(
            date__range=[start_for_pay_history, end_for_pay_history],
            edara_ilat='ФЛ',
            abonent__etrap=etrap,
            kassir_etrap='Внешние платежи'
        )
        print('start_for_pay_history', start_for_pay_history)
        print('end_for_pay_history', end_for_pay_history)

        for p in pays_wn:
            lst = sagitSaldoDict[int(p.abonent.number)]
            kassir_lower = p.kassir.lower()

            if 'E-government' in p.kassir:
                lst[17] += p.internet
                lst[18] += p.alem
                lst[19] += p.prochee
            elif 'Tolleg APP TMCELL' in p.kassir:
                lst[21] += p.internet
                lst[22] += p.alem
                lst[23] += p.prochee
            elif 'Saray Tolegy' in p.kassir:
                lst[25] += p.internet
                lst[26] += p.alem
                lst[27] += p.prochee
            elif 'Dostluk Bank' in p.kassir:
                lst[29] += p.internet
                lst[30] += p.alem
                lst[31] += p.prochee
            elif 'Turkmen Pochta' in p.kassir:
                lst[33] += p.internet
                lst[34] += p.alem
                lst[35] += p.prochee
            elif 'halk' in kassir_lower:
                lst[37] += p.internet
                lst[38] += p.alem
                lst[39] += p.prochee
            elif 'dealers' in kassir_lower:
                lst[41] += p.internet
                lst[42] += p.alem
                lst[43] += p.prochee
            else:
                print('ошибка внешний платёж не распознан:', p.kassir)

        # --- Считаем итоги ---
        for n, lst in sagitSaldoDict.items():
            lst[16] = lst[12] + lst[13] + lst[14] + lst[15]                                    # kassa_itogo
            lst[20] = lst[17] + lst[18] + lst[19]                                               # egov_itogo
            lst[24] = lst[21] + lst[22] + lst[23]                                               # tolleg_itogo
            lst[28] = lst[25] + lst[26] + lst[27]                                               # saray_itogo
            lst[32] = lst[29] + lst[30] + lst[31]                                               # dostluk_itogo
            lst[36] = lst[33] + lst[34] + lst[35]                                               # pochta_itogo
            lst[40] = lst[37] + lst[38] + lst[39]                                               # halk_itogo
            lst[44] = lst[41] + lst[42] + lst[43]                                               # dealers_itogo
            lst[45] = lst[16] + lst[20] + lst[24] + lst[28] + lst[32] + lst[36] + lst[40] + lst[44]  # wsego_oplacheno

        headers = (
            "Tel_Nomer", "DT", "KT",
            'AMTS_"8"', "Zakaz", "Swerh_limit", "Abonplata", "Po_razgoworny", "Prochee",
            "Internet", "Dop_Uslugi", "Kabel_TV", "Alem_TW", "Wsego_Nachisl.",
            # КАССА
            "Kassa_Internet", "Kassa_Alem", "Kassa_Abonplata", "Kassa_Kabel_TV", "Kassa_Itogo",
            # E-government
            "Egov_Internet", "Egov_Alem", "Egov_Abonplata", "Egov_Itogo",
            # Tolleg APP TMCELL
            "Tolleg_Internet", "Tolleg_Alem", "Tolleg_Abonplata", "Tolleg_Itogo",
            # Saray Tolegy
            "Saray_Internet", "Saray_Alem", "Saray_Abonplata", "Saray_Itogo",
            # Dostluk Bank
            "Dostluk_Internet", "Dostluk_Alem", "Dostluk_Abonplata", "Dostluk_Itogo",
            # Turkmen Pochta
            "Pochta_Internet", "Pochta_Alem", "Pochta_Abonplata", "Pochta_Itogo",
            # HalkBank
            "Halk_Internet", "Halk_Alem", "Halk_Abonplata", "Halk_Itogo",
            # Dealers
            "Dealers_Internet", "Dealers_Alem", "Dealers_Abonplata", "Dealers_Itogo",
            # Общий итог
            "Wsego_Oplacheno",
        )

        data = []
        data = tablib.Dataset(*data, headers=headers)

        for n, v in sagitSaldoDict.items():
            data.append((
                n, v[0], v[1],
                v[4], v[5], v[3], v[2], 0, v[6],
                v[8], v[7], v[9], v[10], v[11],
                # КАССА
                v[12], v[13], v[14], v[15], v[16],
                # E-government
                v[17], v[18], v[19], v[20],
                # Tolleg
                v[21], v[22], v[23], v[24],
                # Saray
                v[25], v[26], v[27], v[28],
                # Dostluk
                v[29], v[30], v[31], v[32],
                # Pochta
                v[33], v[34], v[35], v[36],
                # Halk
                v[37], v[38], v[39], v[40],
                # Dealers
                v[41], v[42], v[43], v[44],
                # Общий итог
                v[45],
            ))

        excel_data = data.export('xlsx')
        response = HttpResponse(excel_data, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= Debit_{etrap}.xlsx"

        return response

    return render(request, 'telekom/MATB/monthOtchotForAshyr.html', context)


# from django.shortcuts import render, redirect
# from django.contrib import messages
# from telekom.models import ManagerNames, MonthBalance, NachMinus, NachMonthDebetKredet, NachisleniyaOtchet, NonLocalCall, PayHistory, PerekidkaInfo, SagidDecemberDebetKredet, UserTable, UserTableArhiw, KabelNach, KabelTvPayHistory
# from django.db.models import Sum
# from django.db.models import Q
# import tablib

# from telekom.views2.myFunc.myFunc import getPreviousMonth, loggedUserEtrapAndGroup, monthСonvert

# from datetime import date, datetime, timedelta
# from calendar import monthrange

# from django.http import HttpResponse


# def monthOtchotForAshyr(request):

#     context = {}
#     current_date = str(date.today())
#     context['current_date'] = current_date

#     current_year = current_date[0:4]

#     current_month = current_date[5:7]
#     month_word = monthСonvert(current_month)
#     days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]

#     EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
#     print('EtrapAndGroup[1]', EtrapAndGroup[1])
#     if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
#         log = EtrapAndGroup[0]
#         context['matbIndex'] = True
#         context['monthOtchotForAshyr'] = True
#     else:
#         messages.error(request, f'Доступ только соотрудникам MATB')
#         return redirect('user-login')

#     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
#     context['etraps'] = etraps
#     context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
#     context['years'] = ['2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

#     etrap = request.GET.get('etrap')# if request.GET.get('etrap') != None else log
#     month = request.GET.get('month') if request.GET.get('month') != None else month_word
#     year = request.GET.get('year') if request.GET.get('year') != None else current_year
#     context['month'] = month
#     context['year'] = year
#     context['etrap'] = etrap
    
#     days_in_choosed_month = monthrange(int(year), int(monthСonvert(month)))[1]
    
#     if etrap and month and year:
#         month_digit = monthСonvert(month)
#         # Конвертировать строки в объект даты
#         current_date = datetime.strptime(year + month_digit, '%Y%m')
#         # Добавить один месяц
#         next_month_date = current_date + timedelta(days=days_in_choosed_month)
#         nextYear = next_month_date.year
#         nextMonth = next_month_date.month

#         start = f"{year}-{month_digit}-01"
#         end = f"{year}-{month_digit}-{days_in_choosed_month}"
#         end2 = f"{nextYear}-{nextMonth}-01"

#         start_for_pay_history = f"{year}-{month_digit}-01"
#         end_for_pay_history = f"{year}-{month_digit}-{days_in_choosed_month} 23:59:59"

  
#         nachMinus = NachMinus.objects.filter(year=year, month=month_digit, user__etrap=etrap, user__is_enterprises=False)
        

        
#         managers = ManagerNames.objects.filter(etrap=etrap)
#         # берем Внешние платежи типа wn = ['E-government', 'Tolleg APP TMCELL', 'Saray Tolegy', 'Dostluk Bank', 'Turkmen Pochta', 'HalkBank Terminal Payments']
#         wn = []
#         managers_list = []
#         for m in ManagerNames.objects.all():
#             if m.etrap == 'Внешние платежи':
#                 wn.append(m.name)
#             if m.etrap == etrap:
#                 managers_list.append(m.name)

                
#         globalCall = NonLocalCall.objects.filter(DATE__range=[start, end2], SUB_A_etrap='Dashoguz')
#         number_kod = {}
#         for c in globalCall:
#             if c.edara == 'I':
#                 if int(c.SUB_A) not in number_kod:
#                     number_kod[int(c.SUB_A)] = c.total_price
#                 else:
#                     number_kod[int(c.SUB_A)] = c.total_price

#         sagitSaldoDict = {} # {number: [debit, kredit]}
#         # sagitSaldo = SagidDecemberDebetKredet.objects.all()

#         kabelNew_number_nach = {} # {number: nach}
#         kabelNewUsersNach = KabelNach.objects.filter(year=year, month=monthСonvert(month), user__is_enterprises=False)
#         for u in kabelNewUsersNach:
#             kabelNew_number_nach[u.user.number] = u.nach
 
#         for i in range(20000, 80000):
#             #                                          sumNach 11
#             if i in kabelNew_number_nach and etrap == 'Dashoguz':
#                 sagitSaldoDict[i] = [0,0,0,0,0,0,0,0,0,kabelNew_number_nach[i],0,0,0,0,0,0,0,0,0,0]
#             else:
#                 sagitSaldoDict[i] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#         for i in range(90000, 105000):
#             # sagitSaldoDict[i] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
#             if i in kabelNew_number_nach and etrap == 'Dashoguz':
#                 sagitSaldoDict[i] = [0,0,0,0,0,0,0,0,0,kabelNew_number_nach[i],0,0,0,0,0,0,0,0,0,0]
#             else:
#                 sagitSaldoDict[i] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


#         # for s in sagitSaldo:
#         #     sagitSaldoDict[int(s.number)][0] = s.debit
#         #     sagitSaldoDict[int(s.number)][1] = s.kredit

        

#         for n in nachMinus:
#             list_2 = sagitSaldoDict[int(n.user.number)]
#             list_2[2] = n.telefon
#             list_2[3] = n.slr
#             list_2[4] = n.kod
#             list_2[5] = n.zakaz
#             list_2[6] = 0
#             list_2[7] = n.dop_uslugi
#             list_2[8] = n.internet
#             # list_2[9] = n.kabel
#             list_2[10] = n.alem
#             sagitSaldoDict[int(n.user.number)] = list_2
#         number_kassaPay = {} # {number: kassaPay}

#         pays = PayHistory.objects.filter(date__range=[start_for_pay_history, end_for_pay_history], edara_ilat='ФЛ', abonent__etrap=etrap).exclude(kassir_etrap='Внешние платежи') # тут вроде должен быть abonent__etrap=etrap, а не kassir_etrap=etrap пробую поставить abonent__etrap=etrap
#         total_kassa = 0
#         print('len_pays', len(pays))
#         for p in pays:
#             if p.abonent.number == '93095':
#                 print('da', p.abonent.number)
#             # if p.kabel == 0 and p.alem == 0:
#             sagitSaldoDict[int(p.abonent.number)][12] += p.telefon + p.slr + p.kod + p.zakaz + p.prochee + p.dop_uslugi + p.internet + p.alem

#         pays = PayHistory.objects.filter(date__range=[start_for_pay_history, end_for_pay_history], edara_ilat='ФЛ', abonent__etrap=etrap, kassir_etrap='Внешние платежи')
#         print('start_for_pay_history', start_for_pay_history)
#         print('end_for_pay_history', end_for_pay_history)
        

#         for p in pays:
#             # if p.alem > 0:
#             #     continue
#             if 'E-government' in p.kassir:
#                 sagitSaldoDict[int(p.abonent.number)][13] += p.total
#             elif 'Tolleg APP TMCELL' in p.kassir:
#                 sagitSaldoDict[int(p.abonent.number)][14] += p.total
#             elif 'Saray Tolegy' in p.kassir:
#                 sagitSaldoDict[int(p.abonent.number)][15] += p.total
#             elif 'Dostluk Bank' in p.kassir:
#                 sagitSaldoDict[int(p.abonent.number)][16] += p.total
#             elif 'Turkmen Pochta' in p.kassir:
#                 sagitSaldoDict[int(p.abonent.number)][17] += p.total
#             elif 'halk' in p.kassir.lower():
#                 sagitSaldoDict[int(p.abonent.number)][18] += p.total
#             elif 'dealers' in p.kassir.lower():
#                 sagitSaldoDict[int(p.abonent.number)][19] += p.total
#             else:
#                 print('ошибка')

        
#         if etrap == 'Dashoguz':
#             KabelTvNewPays = KabelTvPayHistory.objects.filter(pay_date__range=[start_for_pay_history, end_for_pay_history], user__is_enterprises=False)
#             for p in KabelTvNewPays:

#                 if 'E-government' in p.pay_kassir:
#                     sagitSaldoDict[int(p.user.number)][13] += p.pay
#                 elif 'Tolleg APP TMCELL' in p.pay_kassir:
#                     sagitSaldoDict[int(p.user.number)][14] += p.pay
#                 elif 'Saray Tolegy' in p.pay_kassir:
#                     sagitSaldoDict[int(p.user.number)][15] += p.pay
#                 elif 'Dostluk Bank' in p.pay_kassir:
#                     sagitSaldoDict[int(p.user.number)][16] += p.pay
#                 elif 'Turkmen Pochta' in p.pay_kassir:
#                     sagitSaldoDict[int(p.user.number)][17] += p.pay
#                 elif 'halk' in p.pay_kassir.lower():
#                     sagitSaldoDict[int(p.user.number)][18] += p.pay
#                 else:
#                     sagitSaldoDict[int(p.user.number)][12] += p.pay

               
  
     
       
#         # headers = ("Tel Nomer","DEBIT","KREDIT","NACH_ABON","NACH_SLR","NACH_KOD","NACH_ZAKAZ","NACH_PROCHEE",'NACH_USLUGI',"NACH_INT","NACH_KABEL","NACH_ALEM","WSEGO_NACH",
#                 # "TOLEG_KASSA", "E-GOV","TOLEG APP TMCELL","SARAY","DOSTLUK","POCHTA","HALKBANK")
        
#         headers = ("Tel_Nomer","DT","KT",'AMTS_"8"',"Zakaz","Swerh_limit","Abonplata","Po_razgoworny",'Prochee',"Internet","Dop_Uslugi","Kabel_TV","Alem_TW","Wsego_Nachisl.",
#                    "Kassa_toleg","Dostluk_Bank","E_gov","Toleg_APP_TM_CELL","Halk_Bank_Termonal","Saray_Toleg","Turkmen_Pochta","Prochie","TM_POST_Dealers", "Wsego_Oplacheno","DT","KT")
#         data = []
#         data = tablib.Dataset(*data, headers=headers)
#         # books = Book.objects.all()
#         # for book in books:
#         for n, v in sagitSaldoDict.items():
#             # data.append((n,v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9],v[10],v[11],v[12],v[13],v[14],v[15],v[16],v[17],v[18]))

#             data.append((n,v[0],v[1],v[4],v[5],v[3],v[2],0,v[6],v[8],v[7],v[9],v[10],v[11],   v[12],v[16],v[13],v[14],v[18],v[15],v[17], 0,v[19],0,0,0))
#         excel_data = data.export('xlsx')
#         response = HttpResponse(excel_data, content_type='application/vnd.ms-excel;charset=utf-8')
#         response['Content-Disposition'] = f"attachment; filename= Debit_{etrap}.xlsx"

#         return response
        


        







     



#     return render(request, 'telekom/MATB/monthOtchotForAshyr.html', context)


# # Rabotaet no be razdelennye etrapy Akdepe i Boldumsaz
# # from django.shortcuts import render, redirect
# # from django.contrib import messages
# # from telekom.models import ManagerNames, MonthBalance, NachMinus, NachMonthDebetKredet, NachisleniyaOtchet, NonLocalCall, PayHistory, PerekidkaInfo, SagidDecemberDebetKredet, UserTable, UserTableArhiw, KabelNach, KabelTvPayHistory
# # from django.db.models import Sum
# # from django.db.models import Q
# # import tablib

# # from telekom.views2.myFunc.myFunc import getPreviousMonth, loggedUserEtrapAndGroup, monthСonvert

# # from datetime import date, datetime, timedelta
# # from calendar import monthrange

# # from django.http import HttpResponse


# # def monthOtchotForAshyr(request):
# #     context = {}
# #     current_date = str(date.today())
# #     context['current_date'] = current_date

# #     current_year = current_date[0:4]

# #     current_month = current_date[5:7]
# #     month_word = monthСonvert(current_month)
# #     days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]

# #     EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
# #     print('EtrapAndGroup[1]', EtrapAndGroup[1])
# #     if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
# #         log = EtrapAndGroup[0]
# #         context['matbIndex'] = True
# #         context['monthOtchotForAshyr'] = True
# #     else:
# #         messages.error(request, f'Доступ только соотрудникам MATB')
# #         return redirect('user-login')

# #     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
# #     context['etraps'] = etraps
# #     context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
# #     context['years'] = ['2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

# #     etrap = request.GET.get('etrap')# if request.GET.get('etrap') != None else log
# #     month = request.GET.get('month') if request.GET.get('month') != None else month_word
# #     year = request.GET.get('year') if request.GET.get('year') != None else current_year
# #     context['month'] = month
# #     context['year'] = year
# #     context['etrap'] = etrap
    
# #     days_in_choosed_month = monthrange(int(year), int(monthСonvert(month)))[1]

    
# #     if etrap and month and year:
# #         month_digit = monthСonvert(month)
# #         # Конвертировать строки в объект даты
# #         current_date = datetime.strptime(year + month_digit, '%Y%m')
# #         # Добавить один месяц
# #         next_month_date = current_date + timedelta(days=days_in_choosed_month)
# #         nextYear = next_month_date.year
# #         nextMonth = next_month_date.month

# #         start = f"{year}-{month_digit}-01"
# #         end = f"{year}-{month_digit}-{days_in_choosed_month}"
# #         end2 = f"{nextYear}-{nextMonth}-01"

# #         start_for_pay_history = f"{year}-{month_digit}-01"
# #         end_for_pay_history = f"{year}-{month_digit}-{days_in_choosed_month} 23:59:59"

  
# #         nachMinus = NachMinus.objects.filter(year=year, month=month_digit, user__etrap=etrap, user__is_enterprises=False)
        

        
# #         managers = ManagerNames.objects.filter(etrap=etrap)
# #         # берем Внешние платежи типа wn = ['E-government', 'Tolleg APP TMCELL', 'Saray Tolegy', 'Dostluk Bank', 'Turkmen Pochta', 'HalkBank Terminal Payments']
# #         wn = []
# #         managers_list = []
# #         for m in ManagerNames.objects.all():
# #             if m.etrap == 'Внешние платежи':
# #                 wn.append(m.name)
# #             if m.etrap == etrap:
# #                 managers_list.append(m.name)

                
# #         globalCall = NonLocalCall.objects.filter(DATE__range=[start, end2], SUB_A_etrap='Dashoguz')
# #         number_kod = {}
# #         for c in globalCall:
# #             if c.edara == 'I':
# #                 if int(c.SUB_A) not in number_kod:
# #                     number_kod[int(c.SUB_A)] = c.total_price
# #                 else:
# #                     number_kod[int(c.SUB_A)] = c.total_price

# #         sagitSaldoDict = {} # {number: [debit, kredit]}
# #         # sagitSaldo = SagidDecemberDebetKredet.objects.all()

# #         kabelNew_number_nach = {} # {number: nach}
# #         kabelNewUsersNach = KabelNach.objects.filter(year=year, month=monthСonvert(month), user__is_enterprises=False)
# #         for u in kabelNewUsersNach:
# #             kabelNew_number_nach[u.user.number] = u.nach
 
# #         for i in range(20000, 80000):
# #             #                                          sumNach 11
# #             if i in kabelNew_number_nach and etrap == 'Dashoguz':
# #                 sagitSaldoDict[i] = [0,0,0,0,0,0,0,0,0,kabelNew_number_nach[i],0,0,0,0,0,0,0,0,0,0]
# #             else:
# #                 sagitSaldoDict[i] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# #         for i in range(90000, 105000):
# #             # sagitSaldoDict[i] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# #             if i in kabelNew_number_nach and etrap == 'Dashoguz':
# #                 sagitSaldoDict[i] = [0,0,0,0,0,0,0,0,0,kabelNew_number_nach[i],0,0,0,0,0,0,0,0,0,0]
# #             else:
# #                 sagitSaldoDict[i] = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


# #         # for s in sagitSaldo:
# #         #     sagitSaldoDict[int(s.number)][0] = s.debit
# #         #     sagitSaldoDict[int(s.number)][1] = s.kredit

        

# #         for n in nachMinus:
# #             list_2 = sagitSaldoDict[int(n.user.number)]
# #             list_2[2] = n.telefon
# #             list_2[3] = n.slr
# #             list_2[4] = n.kod
# #             list_2[5] = n.zakaz
# #             list_2[6] = 0
# #             list_2[7] = n.dop_uslugi
# #             list_2[8] = n.internet
# #             # list_2[9] = n.kabel
# #             list_2[10] = n.alem
# #             sagitSaldoDict[int(n.user.number)] = list_2
# #         number_kassaPay = {} # {number: kassaPay}

# #         pays = PayHistory.objects.filter(date__range=[start_for_pay_history, end_for_pay_history], edara_ilat='ФЛ', abonent__etrap=etrap).exclude(kassir_etrap='Внешние платежи') # тут вроде должен быть abonent__etrap=etrap, а не kassir_etrap=etrap пробую поставить abonent__etrap=etrap
# #         total_kassa = 0
# #         print('len_pays', len(pays))
# #         for p in pays:
# #             if p.abonent.number == '93095':
# #                 print('da', p.abonent.number)
# #             # if p.kabel == 0 and p.alem == 0:
# #             sagitSaldoDict[int(p.abonent.number)][12] += p.telefon + p.slr + p.kod + p.zakaz + p.prochee + p.dop_uslugi + p.internet + p.alem

# #         pays = PayHistory.objects.filter(date__range=[start_for_pay_history, end_for_pay_history], edara_ilat='ФЛ', abonent__etrap=etrap, kassir_etrap='Внешние платежи')
# #         print('start_for_pay_history', start_for_pay_history)
# #         print('end_for_pay_history', end_for_pay_history)
        

# #         for p in pays:
# #             # if p.alem > 0:
# #             #     continue
# #             if 'E-government' in p.kassir:
# #                 sagitSaldoDict[int(p.abonent.number)][13] += p.total
# #             elif 'Tolleg APP TMCELL' in p.kassir:
# #                 sagitSaldoDict[int(p.abonent.number)][14] += p.total
# #             elif 'Saray Tolegy' in p.kassir:
# #                 sagitSaldoDict[int(p.abonent.number)][15] += p.total
# #             elif 'Dostluk Bank' in p.kassir:
# #                 sagitSaldoDict[int(p.abonent.number)][16] += p.total
# #             elif 'Turkmen Pochta' in p.kassir:
# #                 sagitSaldoDict[int(p.abonent.number)][17] += p.total
# #             elif 'halk' in p.kassir.lower():
# #                 sagitSaldoDict[int(p.abonent.number)][18] += p.total
# #             elif 'dealers' in p.kassir.lower():
# #                 sagitSaldoDict[int(p.abonent.number)][19] += p.total
# #             else:
# #                 print('ошибка')

        
# #         if etrap == 'Dashoguz':
# #             KabelTvNewPays = KabelTvPayHistory.objects.filter(pay_date__range=[start_for_pay_history, end_for_pay_history], user__is_enterprises=False)
# #             for p in KabelTvNewPays:

# #                 if 'E-government' in p.pay_kassir:
# #                     sagitSaldoDict[int(p.user.number)][13] += p.pay
# #                 elif 'Tolleg APP TMCELL' in p.pay_kassir:
# #                     sagitSaldoDict[int(p.user.number)][14] += p.pay
# #                 elif 'Saray Tolegy' in p.pay_kassir:
# #                     sagitSaldoDict[int(p.user.number)][15] += p.pay
# #                 elif 'Dostluk Bank' in p.pay_kassir:
# #                     sagitSaldoDict[int(p.user.number)][16] += p.pay
# #                 elif 'Turkmen Pochta' in p.pay_kassir:
# #                     sagitSaldoDict[int(p.user.number)][17] += p.pay
# #                 elif 'halk' in p.pay_kassir.lower():
# #                     sagitSaldoDict[int(p.user.number)][18] += p.pay
# #                 else:
# #                     sagitSaldoDict[int(p.user.number)][12] += p.pay

               
  
     
       
# #         # headers = ("Tel Nomer","DEBIT","KREDIT","NACH_ABON","NACH_SLR","NACH_KOD","NACH_ZAKAZ","NACH_PROCHEE",'NACH_USLUGI',"NACH_INT","NACH_KABEL","NACH_ALEM","WSEGO_NACH",
# #                 # "TOLEG_KASSA", "E-GOV","TOLEG APP TMCELL","SARAY","DOSTLUK","POCHTA","HALKBANK")
        
# #         headers = ("Tel_Nomer","DT","KT",'AMTS_"8"',"Zakaz","Swerh_limit","Abonplata","Po_razgoworny",'Prochee',"Internet","Dop_Uslugi","Kabel_TV","Alem_TW","Wsego_Nachisl.",
# #                    "Kassa_toleg","Dostluk_Bank","E_gov","Toleg_APP_TM_CELL","Halk_Bank_Termonal","Saray_Toleg","Turkmen_Pochta","Prochie","TM_POST_Dealers", "Wsego_Oplacheno","DT","KT")
# #         data = []
# #         data = tablib.Dataset(*data, headers=headers)
# #         # books = Book.objects.all()
# #         # for book in books:
# #         for n, v in sagitSaldoDict.items():
# #             # data.append((n,v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9],v[10],v[11],v[12],v[13],v[14],v[15],v[16],v[17],v[18]))

# #             data.append((n,v[0],v[1],v[4],v[5],v[3],v[2],0,v[6],v[8],v[7],v[9],v[10],v[11],   v[12],v[16],v[13],v[14],v[18],v[15],v[17], 0,v[19],0,0,0))
# #         excel_data = data.export('xlsx')
# #         response = HttpResponse(excel_data, content_type='application/vnd.ms-excel;charset=utf-8')
# #         response['Content-Disposition'] = f"attachment; filename= Debit_{etrap}.xlsx"

# #         return response
        


        







     



# #     return render(request, 'telekom/MATB/monthOtchotForAshyr.html', context)