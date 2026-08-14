from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.models import ManagerNames, NachMinus, NonLocalCall, PayHistory, UserTable, KabelNach, KabelTvPayHistory
import tablib

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert

from datetime import date, datetime, timedelta
from calendar import monthrange

from django.http import HttpResponse


WN_KASSIRS = ['E-government', 'Tolleg APP TMCELL', 'Saray Tolegy', 'Dostluk Bank', 'Turkmen Pochta', 'HalkBank Terminal Payments']

# Точные имена manager/kassir для внешних платежей Milli Billing (см. vneshniePlatejiAdd.py)
MB_KASSA_MANAGERS = ['Capar', 'eGov', 'Toleg', 'Turkmenpost diller']


def monthOtchotForAshyrMB(request):

    context = {}
    current_date = str(date.today())
    context['current_date'] = current_date

    current_year = current_date[0:4]
    current_month = current_date[5:7]
    month_word = monthСonvert(current_month)

    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        context['matbIndex'] = True
        context['monthOtchotForAshyrMB'] = True
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

        start_for_pay_history = f"{year}-{month_digit}-01"
        end_for_pay_history = f"{year}-{month_digit}-{days_in_choosed_month} 23:59:59"

        nachMinus = NachMinus.objects.filter(year=year, month=month_digit, user__etrap=etrap, user__is_enterprises=False)

        sagitSaldoDict = {}  # {number: list[63]}

        kabelNew_number_nach = {}
        kabelNewUsersNach = KabelNach.objects.filter(year=year, month=monthСonvert(month), user__is_enterprises=False)
        for u in kabelNewUsersNach:
            kabelNew_number_nach[u.user.number] = u.nach

        # Индексы списка (63 элемента, 0..62) — как в monthOtchotForAshyr.py (0..45), плюс Milli Billing (46..62):
        # [0] DT  [1] KT
        # [2] telefon nach  [3] slr nach  [4] kod nach  [5] zakaz nach  [6] prochee nach (0)
        # [7] dop_uslugi nach  [8] internet nach  [9] kabel nach (KabelNach)  [10] alem nach
        # [11] wsego nach (не используется, как в оригинале)
        # --- КАССА --- [12] internet [13] alem [14] abonplata [15] kabel_tv [16] itogo
        # --- E-government (legacy) --- [17..20]
        # --- Tolleg APP TMCELL (legacy) --- [21..24]
        # --- Saray Tolegy (legacy) --- [25..28]
        # --- Dostluk Bank (legacy) --- [29..32]
        # --- Turkmen Pochta (legacy) --- [33..36]
        # --- HalkBank (legacy) --- [37..40]
        # --- Dealers (legacy) --- [41..44]
        # [45] wsego_oplacheno
        # --- NOVOE: Belet nach --- [46]
        # --- Milli Billing Capar --- [47] internet [48] alem [49] abonplata [50] itogo
        # --- Milli Billing eGov --- [51..54]
        # --- Milli Billing Toleg --- [55..58]
        # --- Milli Billing Turkmenpost diller --- [59..62]

        for i in range(20000, 80000):
            if i in kabelNew_number_nach and etrap == 'Dashoguz':
                row = [0] * 63
                row[9] = kabelNew_number_nach[i]
                sagitSaldoDict[i] = row
            else:
                sagitSaldoDict[i] = [0] * 63

        for i in range(90000, 105000):
            if i in kabelNew_number_nach and etrap == 'Dashoguz':
                row = [0] * 63
                row[9] = kabelNew_number_nach[i]
                sagitSaldoDict[i] = row
            else:
                sagitSaldoDict[i] = [0] * 63

        # Начисления (включая Belet — раньше нигде не читалось)
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
            lst[46] = n.belet

        # --- КАССА (PayHistory без внешних) ---
        # edara_ilat у части строк не заполнен (None) хотя абонент реально ФЛ - фильтруем по
        # abonent__is_enterprises, а не по edara_ilat, иначе теряем часть кассовых платежей
        pays_kassa = PayHistory.objects.filter(
            date__range=[start_for_pay_history, end_for_pay_history],
            abonent__is_enterprises=False,
            abonent__etrap=etrap
        ).exclude(kassir_etrap='Внешние платежи')

        for p in pays_kassa:
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
            abonent__is_enterprises=False,
            abonent__etrap=etrap,
            kassir_etrap='Внешние платежи'
        )

        for p in pays_wn:
            lst = sagitSaldoDict[int(p.abonent.number)]
            kassir_lower = p.kassir.lower()

            # --- Milli Billing (точное совпадение имени менеджера) ---
            if p.kassir == 'Capar':
                lst[47] += p.internet
                lst[48] += p.alem
                lst[49] += p.prochee
            elif p.kassir == 'eGov':
                lst[51] += p.internet
                lst[52] += p.alem
                lst[53] += p.prochee
            elif p.kassir == 'Toleg':
                lst[55] += p.internet
                lst[56] += p.alem
                lst[57] += p.prochee
            elif p.kassir == 'Turkmenpost diller':
                lst[59] += p.internet
                lst[60] += p.alem
                lst[61] += p.prochee
            # --- Старые (lanbilling) внешние каналы ---
            elif 'E-government' in p.kassir:
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
            lst[20] = lst[17] + lst[18] + lst[19]                                               # egov_itogo (legacy)
            lst[24] = lst[21] + lst[22] + lst[23]                                               # tolleg_itogo (legacy)
            lst[28] = lst[25] + lst[26] + lst[27]                                               # saray_itogo
            lst[32] = lst[29] + lst[30] + lst[31]                                               # dostluk_itogo
            lst[36] = lst[33] + lst[34] + lst[35]                                               # pochta_itogo
            lst[40] = lst[37] + lst[38] + lst[39]                                               # halk_itogo
            lst[44] = lst[41] + lst[42] + lst[43]                                               # dealers_itogo
            lst[50] = lst[47] + lst[48] + lst[49]                                               # capar_itogo
            lst[54] = lst[51] + lst[52] + lst[53]                                               # mb_egov_itogo
            lst[58] = lst[55] + lst[56] + lst[57]                                               # mb_toleg_itogo
            lst[62] = lst[59] + lst[60] + lst[61]                                               # tmpost_itogo
            lst[45] = (
                lst[16] + lst[20] + lst[24] + lst[28] + lst[32] + lst[36] + lst[40] + lst[44]   # старые
                + lst[50] + lst[54] + lst[58] + lst[62]                                          # Milli Billing
            )  # wsego_oplacheno

        headers = (
            "Tel_Nomer", "DT", "KT",
            'AMTS_"8"', "Zakaz", "Swerh_limit", "Abonplata", "Po_razgoworny", "Prochee",
            "Internet", "Dop_Uslugi", "Kabel_TV", "Alem_TW", "Belet", "Wsego_Nachisl.",
            # КАССА
            "Kassa_Internet", "Kassa_Alem", "Kassa_Abonplata", "Kassa_Kabel_TV", "Kassa_Itogo",
            # Milli Billing — Capar
            "Capar_Internet", "Capar_Alem", "Capar_Abonplata", "Capar_Itogo",
            # Milli Billing — eGov
            "MB_Egov_Internet", "MB_Egov_Alem", "MB_Egov_Abonplata", "MB_Egov_Itogo",
            # Milli Billing — Toleg (Tolleg APP TMCELL)
            "MB_Toleg_Internet", "MB_Toleg_Alem", "MB_Toleg_Abonplata", "MB_Toleg_Itogo",
            # Milli Billing — Turkmenpost diller
            "Turkmenpost_Diller_Internet", "Turkmenpost_Diller_Alem", "Turkmenpost_Diller_Abonplata", "Turkmenpost_Diller_Itogo",
            # Dostluk Bank (legacy)
            "Dostluk_Internet", "Dostluk_Alem", "Dostluk_Abonplata", "Dostluk_Itogo",
            # E-government (legacy)
            "Egov_Internet", "Egov_Alem", "Egov_Abonplata", "Egov_Itogo",
            # Tolleg APP TMCELL (legacy)
            "Tolleg_Internet", "Tolleg_Alem", "Tolleg_Abonplata", "Tolleg_Itogo",
            # HalkBank (legacy)
            "Halk_Internet", "Halk_Alem", "Halk_Abonplata", "Halk_Itogo",
            # Saray Tolegy (legacy)
            "Saray_Internet", "Saray_Alem", "Saray_Abonplata", "Saray_Itogo",
            # Turkmen Pochta (legacy)
            "Pochta_Internet", "Pochta_Alem", "Pochta_Abonplata", "Pochta_Itogo",
            # Dealers (legacy)
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
                v[8], v[7], v[9], v[10], v[46], v[11],
                # КАССА
                v[12], v[13], v[14], v[15], v[16],
                # Capar
                v[47], v[48], v[49], v[50],
                # eGov (Milli Billing)
                v[51], v[52], v[53], v[54],
                # Toleg (Milli Billing)
                v[55], v[56], v[57], v[58],
                # Turkmenpost diller
                v[59], v[60], v[61], v[62],
                # Dostluk
                v[29], v[30], v[31], v[32],
                # E-government (legacy)
                v[17], v[18], v[19], v[20],
                # Tolleg (legacy)
                v[21], v[22], v[23], v[24],
                # Halk
                v[37], v[38], v[39], v[40],
                # Saray
                v[25], v[26], v[27], v[28],
                # Pochta
                v[33], v[34], v[35], v[36],
                # Dealers
                v[41], v[42], v[43], v[44],
                # Общий итог
                v[45],
            ))

        excel_data = data.export('xlsx')
        response = HttpResponse(excel_data, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= Debit_MilliBilling_{etrap}.xlsx"

        return response

    return render(request, 'telekom/MATB/monthOtchotForAshyrMB.html', context)
