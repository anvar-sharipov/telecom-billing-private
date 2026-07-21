
from django.shortcuts import render, redirect
from telekom.models import LocalCall, NachMinus, NonLocalCall, UserTable, KodSumm
from django.db.models import Sum
from django.contrib import messages

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert
from django.db.models import Q
from datetime import date
from datetime import time
from datetime import datetime, timedelta
from calendar import monthrange


def trafik(request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    
    
    context = {}
    context['matbIndex'] = True
    context['trafik'] = True
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    context['etraps'] = etraps
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

    


    etrap = request.GET.get('etrap')
    year = request.GET.get('year')
    month_word = request.GET.get('month')

    if etrap and year and month_word:
        context['etrap'] = etrap
        context['year'] = year
        context['month'] = month_word
        month_digit = monthСonvert(month_word)

        days_in_choosed_month = monthrange(int(year), int(month_digit))[1]

        # Конвертировать строки в объект даты
        current_date = datetime.strptime(year + month_digit, '%Y%m')
        # Добавить один месяц
        next_month_date = current_date + timedelta(days=days_in_choosed_month)
        nextYear = next_month_date.year
        nextMonth = next_month_date.month
        end2 = f"{nextYear}-{nextMonth}-01"

    
        turkmenistan = ['Sotowyy',
                'Ashgabat','Ahal Baharly','Ahal Gokdepe','Ahal Kaka','Ahal Seraks','Ahal Tejen','Ahal Babadayhan','Ahal Anew','Ahal Abadan','Ahal Ruhabat','Ahal Ashgabat',
                'Balkan Nebitdag','Balkan Hazar','Balkan Gumdag','Balkan Gyzyl Atr','Balkan Turkmenbashy','Balkan Gumdag','Balkan Esenguly','Balkan Serdar','Balkan Bereket',
                'Balkan Magtymguly','Lebap Turkmenabat','Lebap Magdanly','Lebap Garashsyzlyk','Lebap Gazajak','Lebap Koytendag','Lebap Halach','Lebap Hojambaz','Lebap Garabekewul',
                'Lebap Atamyrat','Lebap Birata','Lebap Galkynysh','Lebap Sayat','Lebap Farap', 'Lebap Sakar','Lebap Seydi','Lebap Turkmenbashy','Lebap Serdarabat','Lebap Serdarabat',
                'Mary','Mary Garagum','Mary Wekilbazar','Mary Oguzhan','Mary Yoleten','Mary Serhetabat','Mary Bayramaly','Mary Murgap','Mary Sakarchage','Mary Tagtabazar','Mary Turkm-gala']

        international = ['Fransiya','Germaniya','Gresiya','Wengriya','Italiya','Niderlandy','Norwegiya','Polsha','Rumyniya','Shwesiya','Shweysariya','Welikobritaniya',
                'Ispaniya','Albaniya','Andorra','Bosniya Gersogowina','Bolgariya','Horwatiya','Kipr', 'Estoniya','Finlyandiya','Gibraltar','Grenlandiya','Islandiya',
                'Latwiya','Lihtenshteyn','Litwa','Luksenburg','Makedoniya','Malta','Portugaliya','Slowakiya','Sloweniya','Yugoslawiya','Cheshskaya Respublika',
                'Gruziya','Ukraina','Afganistan','Turkiya','Iran','Awstriya',
                'Belgiya','Daniya','Awstraliya','Nowaya Zenlandiya','Fidji','Fransuskaya Polineziya','Kiribati','Nowaya Kaledoniya','Norfolkskiye ostrowa','Papua Nowaya Gwineya',
                'Tonga','Wanuatu','Hytay','Kuba','Indiya','Indoneziya','Yaponiya','Malaziya','Meksika','Myanma','Pakistan','Filipiny','Singapur','Yujnaya Koreya','Tailand','Wyetnam',
                'Bahreyn','Bangladesh','Bruney Daruesaalam','Kombodja','Kosta-Rika','Wostochnyy Timor','Gwatelama','Gaiti','Gonduras','Gonk-Kong','Irak','Izrail','Iordaniya','Kuweit',
                'Laos','Liwan','Makao (Aomyn)','Mongoliya','Nepal','Niderlandskie Antilly','Nikaragua','Sewernaya Koreya','Sewernyy Yemen','Oman','Panama' 'Katar','Saudowskaya Arawiya',
                'Yujnyy Yemen','Siriya','Taiwan','O.A.E','USA/CANADA','Argentina','Braziliya','Chili','Kolumbiya','Peru','Wenesuella','Boliwiya','Ekwador','Farerskie Ostrowa',
                'Fransuskatya Gwiana','Gayana','Martitnka','Surinam','Urugway','Egipet','UAR','Aljir','Angola','Benin','Botswana','Burkina Faso','Burundi','Kamerun','Kape Werde','SAR',
                'Chad','Kongo','Jibuti','Ekwatorialnaya gwineya','Efiopiya','Gabon','Gambiya','Gana','Gwineya','Gwineya Bissau','Keniya','Liberiya','Liviya','Madagaskar','Malawi','Mali',
                'Mawritaniya','Mawrikiy','Moroko','Mozambik','Namibiya','Niger','Nigeriya','Reonyon','Respublika Ruanda','Senegal','Seyshelskie ostrowa','Syerra Leonne','Somali','Sudan',
                'Tanzaniya','Respublika Togoleze','Tunis','Uganda','Zair','Zambiya','Zimbabwe']
            

        sng = ['Armeniya', 'Belorussiya', 'Azerbayjan', 'Kazakstan', 'Kyrgystan', 'Rossiya', 'Tajikistan', 'Uzbekistan', 'Moldowa']

        if etrap == 'Dashoguz':
            ATSSALDO = -698
        else:
            ATSSALDO = -700
                
        # print([f"{year}-{month_digit}-01", f"{nextYear}-{nextMonth}-01"])
        # calls = NonLocalCall.objects.filter(DATE__range=[f"{year}-{month_digit}-01", f"{nextYear}-{nextMonth}-01"], SUB_A_etrap=etrap)
        # calls = NonLocalCall.objects.filter(DATE__range=[f"{year}-{month_digit}-01", f"{year}-{month_digit}-{str(days_in_choosed_month)}"], SUB_A_etrap=etrap)
        # calls = NonLocalCall.objects.filter(DATE__range=[f"2024-03-01", "2024-03-31"], SUB_A_etrap=etrap)
        print('1111111111date', f"{year}-{month_digit}-01", f"{year}-{month_digit}-{days_in_choosed_month}", etrap)
        calls = NonLocalCall.objects.filter(DATE__range=[f"{year}-{month_digit}-01", f"{year}-{month_digit}-{days_in_choosed_month}"], SUB_A_etrap=etrap)
        total_test = 0
        for i in calls:
            total_test += int(i.MT) * i.price
        print('total_test_trafik', total_test)

        # test
        users_test = UserTable.objects.filter(account__isnull=False, etrap='Turkmenbashy')
        lists_my = []

        total_kod = 0
        for u in users_test:
            if u.account == -700:
                lists_my.append(u.number)
        total_price = 0
        for c in calls:
            if c.SUB_A in lists_my:
                total_price += c.total_price
        # print('total_price', total_price)

        
        nachMinus = NachMinus.objects.filter(year=year, month=month_digit, user__etrap=etrap)
        nach_number_pk = {} # {number: [nach.pk, prochee]}
        
        for n in nachMinus:
            nach_number_pk[n.user.number] = [n.pk, n.prochee]


        users = UserTable.objects.filter(account=ATSSALDO, etrap=etrap)
        numbersATS = []
        for i in users:
            numbersATS.append(int(i.number))


        times_day = []
        time = datetime.strptime("06:00:00", "%H:%M:%S")
        for j in range(1,100000):
            time += timedelta(seconds=1)
            if str(time)[-8:] == "22:00:00":
                break
            times_day.append(str(time)[-8:])



        # calls_day = calls.filter(START__in=times_day)
        # calls_night = calls.filter(START__in=times_night)

        
       


        
        daysAndNightCallsBud = {} # {starna: [tarif, day_count, night_count, day_minut, night_minut, totalsum]}
        daysAndNightCallsHoz = {}
        daysAndNightCallsATS = {}
        daysAndNightCallsNaseleniya = {}
        daysAndNightUnknownEdara = {}

        daysCallCount = 0
        nightCallCount = 0

        #####################################################################################
        # ✅ Классификация звонка на Хоз/Бюджет/Население/Неопознанный берётся из
        # c.edara — это то, чем абонент БЫЛ на момент начисления (см. dbf_a_nach.py:
        # hozUsers/budUsers/emptyNumberUsers считаются как раз в момент импорта DBF).
        # Раньше здесь заново считали numbersHoz/numbersBud/numbersIlat из ТЕКУЩЕГО
        # UserTable.hb — если у абонента после начисления поменяли hb (Хоз<->Бюджет),
        # обнулили его, сменили etrap или запись вообще пропала, его звонок (уже
        # оплаченный по 0.14 как Хоз/Бюджет) проваливался в else и попадал в
        # "Население" (там ожидается 0.08 за минуту) — итоговые суммы по разделам
        # переставали соответствовать реальным тарифам. АТС — отдельная ось (просто
        # спец. счёт), исторической метки на самом звонке для неё нет, поэтому она
        # по-прежнему берётся из текущего UserTable.account.
        test_price = 0

        def classify_call(c):
            if int(c.SUB_A) in numbersATS:
                return 'ATS'
            if c.edara == 'B':
                return 'Bud'
            if c.edara == 'H':
                return 'Hoz'
            if c.edara == 'E':
                return 'Unknown'
            return 'Naseleniya'

        buckets = {
            'Bud': daysAndNightCallsBud,
            'Hoz': daysAndNightCallsHoz,
            'ATS': daysAndNightCallsATS,
            'Unknown': daysAndNightUnknownEdara,
            'Naseleniya': daysAndNightCallsNaseleniya,
        }

        for c in calls:
            price = c.price
            total_price = c.total_price
            location = c.SUB_B_locations
            MT = int(c.MT)
            is_day = c.START in times_day

            if is_day:
                daysCallCount += 1
            else:
                nightCallCount += 1

            group = classify_call(c)
            if group == 'ATS':
                test_price += total_price
            target = buckets[group]

            if location not in target:
                target[location] = [price, 1, 0, MT, 0, total_price] if is_day else [price, 0, 1, 0, MT, total_price]
            else:
                if is_day:
                    target[location][1] += 1
                    target[location][3] += MT
                else:
                    target[location][2] += 1
                    target[location][4] += MT
                target[location][5] += total_price


        # ✅ По просьбе пользователя: "На сумму манат" в разделе "Трафик
        # междугородней связи АТС (по предприятиям (Хоз расчет))" — всегда
        # Количество минут × Тариф ((day_minut+night_minut) * price), а не
        # накопленная сумма total_price по звонкам (которая на реальных данных
        # чуть отличалась из-за разных цен/округления на отдельных звонках).
        # Только для Hoz — Bud/Население/АТС/Неопознанные не трогаем.
        for _values in daysAndNightCallsHoz.values():
            _values[5] = (_values[3] + _values[4]) * _values[0]

        context['daysAndNightCallsBud'] = daysAndNightCallsBud
        context['daysAndNightCallsHoz'] = daysAndNightCallsHoz
        context['daysAndNightCallsATS'] = daysAndNightCallsATS
        context['daysAndNightCallsNaseleniya'] = daysAndNightCallsNaseleniya
        context['daysAndNightUnknownEdara'] = daysAndNightUnknownEdara
      
        ##################################################################################################################
        ##################################################################################################################
        # для Бюджет ##############################################################################################

        etrapDictBud = {} # {starna: [tarif, day_count, night_count, day_minut, night_minut, totalsum]}
        etrapTotalBud = [0,0,0] # [totalConnect, totalMinut, totalPrice]

        welayatDictBud = {}
        welayatTotalBud = [0,0,0]

        sngDictBud = {}
        sngTotalBud = [0,0,0]

        internationalDictBud = {}
        internationalTotalBud = [0,0,0]

        itogoTotalBud = [0,0,0]

        for country, values in daysAndNightCallsBud.items():
            if country in etraps:
                etrapTotalBud[0] += values[1] + values[2]
                etrapTotalBud[1] += values[3] + values[4]
                etrapTotalBud[2] += values[5]
                itogoTotalBud[0] += values[1] + values[2]
                itogoTotalBud[1] += values[3] + values[4]
                itogoTotalBud[2] += values[5]

                if country not in etrapDictBud:
                    etrapDictBud[country] = values
                else:
                    etrapDictBud[1] = values[1]
                    etrapDictBud[2] = values[1]
                    etrapDictBud[3] = values[3]
                    etrapDictBud[4] = values[4]
                    etrapDictBud[5] = values[5]

            if country in turkmenistan:
                welayatTotalBud[0] += values[1] + values[2]
                welayatTotalBud[1] += values[3] + values[4]
                welayatTotalBud[2] += values[5]
                itogoTotalBud[0] += values[1] + values[2]
                itogoTotalBud[1] += values[3] + values[4]
                itogoTotalBud[2] += values[5]
                if 'Ahal' in country or 'Sotowyy' in country:
                    if 'Ahal wel.' not in welayatDictBud:
                        welayatDictBud['Ahal wel.'] = values
                    else:
                        welayatDictBud['Ahal wel.'][1] += values[1]
                        welayatDictBud['Ahal wel.'][2] += values[2]
                        welayatDictBud['Ahal wel.'][3] += values[3]
                        welayatDictBud['Ahal wel.'][4] += values[4]
                        welayatDictBud['Ahal wel.'][5] += values[5]
                if 'Ashgabat' in country:
                    if 'Ashgabat s.' not in welayatDictBud:
                        welayatDictBud['Ashgabat s.'] = values
                    else:
                        welayatDictBud['Ashgabat s.'][1] += values[1]
                        welayatDictBud['Ashgabat s.'][2] += values[2]
                        welayatDictBud['Ashgabat s.'][3] += values[3]
                        welayatDictBud['Ashgabat s.'][4] += values[4]
                        welayatDictBud['Ashgabat s.'][5] += values[5]
                if 'Mary' in country:
                    if 'Mary wel.' not in welayatDictBud:
                        welayatDictBud['Mary wel.'] = values
                    else:
                        welayatDictBud['Mary wel.'][1] += values[1]
                        welayatDictBud['Mary wel.'][2] += values[2]
                        welayatDictBud['Mary wel.'][3] += values[3]
                        welayatDictBud['Mary wel.'][4] += values[4]
                        welayatDictBud['Mary wel.'][5] += values[5]
                if 'Lebap' in country:
                    if 'Lebap wel.' not in welayatDictBud:
                        welayatDictBud['Lebap wel.'] = values
                    else:
                        welayatDictBud['Lebap wel.'][1] += values[1]
                        welayatDictBud['Lebap wel.'][2] += values[2]
                        welayatDictBud['Lebap wel.'][3] += values[3]
                        welayatDictBud['Lebap wel.'][4] += values[4]
                        welayatDictBud['Lebap wel.'][5] += values[5]
                if 'Balkan' in country:
                    if 'Balkan wel.' not in welayatDictBud:
                        welayatDictBud['Balkan wel.'] = values
                    else:
                        welayatDictBud['Balkan wel.'][1] += values[1]
                        welayatDictBud['Balkan wel.'][2] += values[2]
                        welayatDictBud['Balkan wel.'][3] += values[3]
                        welayatDictBud['Balkan wel.'][4] += values[4]
                        welayatDictBud['Balkan wel.'][5] += values[5]
                # if 'Sotowyy' in country:
                #     if 'Sotowyy' not in welayatDictBud:
                #         welayatDictBud['Sotowyy'] = values
                #     else:
                #         welayatDictBud['Sotowyy'][1] += values[1]
                #         welayatDictBud['Sotowyy'][2] += values[2]
                #         welayatDictBud['Sotowyy'][3] += values[3]
                #         welayatDictBud['Sotowyy'][4] += values[4]
                #         welayatDictBud['Sotowyy'][5] += values[5]
                # if country not in welayatDictBud:
                #     welayatDictBud[country] = values
                # else:
                #     welayatDictBud[2] = values[2]
                #     welayatDictBud[3] = values[3]
                #     welayatDictBud[4] = values[4]
                #     welayatDictBud[5] = values[5]
                #     welayatDictBud[6] = values[6]
            
            if country in sng:
                sngTotalBud[0] += values[1] + values[2]
                sngTotalBud[1] += values[3] + values[4]
                sngTotalBud[2] += values[5]
                itogoTotalBud[0] += values[1] + values[2]
                itogoTotalBud[1] += values[3] + values[4]
                itogoTotalBud[2] += values[5]
                if country not in sngDictBud:
                    sngDictBud[country] = values
                else:
                    sngDictBud[2] = values[2]
                    sngDictBud[3] = values[3]
                    sngDictBud[4] = values[4]
                    sngDictBud[5] = values[5]
                    sngDictBud[6] = values[6]

            if country in international:
                internationalTotalBud[0] += values[1] + values[2]
                internationalTotalBud[1] += values[3] + values[4]
                internationalTotalBud[2] += values[5]
                itogoTotalBud[0] += values[1] + values[2]
                itogoTotalBud[1] += values[3] + values[4]
                itogoTotalBud[2] += values[5]
                if country not in internationalDictBud:
                    internationalDictBud[country] = values
                else:
                    internationalDictBud[2] = values[2]
                    internationalDictBud[3] = values[3]
                    internationalDictBud[4] = values[4]
                    internationalDictBud[5] = values[5]
                    internationalDictBud[6] = values[6]

   
        context['etrapDictBud'] = etrapDictBud
        context['etrapTotalBud'] = etrapTotalBud

        context['welayatDictBud'] = welayatDictBud
        context['welayatTotalBud'] = welayatTotalBud

        context['sngDictBud'] = sngDictBud
        context['sngTotalBud'] = sngTotalBud

        context['internationalDictBud'] = internationalDictBud
        context['internationalTotalBud'] = internationalTotalBud

        context['itogoTotalBud'] = itogoTotalBud


        # для Бюджет ##############################################################################################
        ##################################################################################################################
        ##################################################################################################################

        ##################################################################################################################
        ##################################################################################################################
        # для Хоз ##############################################################################################
        etrapDictHoz = {} # {starna: [tarif, day_count, night_count, day_minut, night_minut, totalsum]}
        etrapTotalHoz = [0,0,0] # [totalConnect, totalMinut, totalPrice]

        welayatDictHoz = {}
        welayatTotalHoz = [0,0,0]

        sngDictHoz = {}
        sngTotalHoz = [0,0,0]

        internationalDictHoz = {}
        internationalTotalHoz = [0,0,0]

        itogoTotalHoz = [0,0,0]


        for country, values in daysAndNightCallsHoz.items():
            if country in etraps:
                etrapTotalHoz[0] += values[1] + values[2]
                etrapTotalHoz[1] += values[3] + values[4]
                etrapTotalHoz[2] += values[5]
                itogoTotalHoz[0] += values[1] + values[2]
                itogoTotalHoz[1] += values[3] + values[4]
                itogoTotalHoz[2] += values[5]
                if country not in etrapDictHoz:
                    etrapDictHoz[country] = values
                else:
                    etrapDictHoz[1] = values[1]
                    etrapDictHoz[2] = values[1]
                    etrapDictHoz[3] = values[3]
                    etrapDictHoz[4] = values[4]
                    etrapDictHoz[5] = values[5]

            if country in turkmenistan:
                welayatTotalHoz[0] += values[1] + values[2]
                welayatTotalHoz[1] += values[3] + values[4]
                welayatTotalHoz[2] += values[5]
                itogoTotalHoz[0] += values[1] + values[2]
                itogoTotalHoz[1] += values[3] + values[4]
                itogoTotalHoz[2] += values[5]
                if 'Ahal' in country or 'Sotowyy' in country:
                    if 'Ahal wel.' not in welayatDictHoz:
                        welayatDictHoz['Ahal wel.'] = values
                    else:
                        # print('2222',values)
                        welayatDictHoz['Ahal wel.'][1] += values[1]
                        welayatDictHoz['Ahal wel.'][2] += values[2]
                        welayatDictHoz['Ahal wel.'][3] += values[3]
                        welayatDictHoz['Ahal wel.'][4] += values[4]
                        welayatDictHoz['Ahal wel.'][5] += values[5]
                if 'Ashgabat' in country:
                    if 'Ashgabat s.' not in welayatDictHoz:
                        welayatDictHoz['Ashgabat s.'] = values
                    else:
                        welayatDictHoz['Ashgabat s.'][1] += values[1]
                        welayatDictHoz['Ashgabat s.'][2] += values[2]
                        welayatDictHoz['Ashgabat s.'][3] += values[3]
                        welayatDictHoz['Ashgabat s.'][4] += values[4]
                        welayatDictHoz['Ashgabat s.'][5] += values[5]
                if 'Mary' in country:
                    if 'Mary wel.' not in welayatDictHoz:
                        welayatDictHoz['Mary wel.'] = values
                    else:
                        welayatDictHoz['Mary wel.'][1] += values[1]
                        welayatDictHoz['Mary wel.'][2] += values[2]
                        welayatDictHoz['Mary wel.'][3] += values[3]
                        welayatDictHoz['Mary wel.'][4] += values[4]
                        welayatDictHoz['Mary wel.'][5] += values[5]
                if 'Lebap' in country:
                    if 'Lebap wel.' not in welayatDictHoz:
                        welayatDictHoz['Lebap wel.'] = values
                    else:
                        welayatDictHoz['Lebap wel.'][1] += values[1]
                        welayatDictHoz['Lebap wel.'][2] += values[2]
                        welayatDictHoz['Lebap wel.'][3] += values[3]
                        welayatDictHoz['Lebap wel.'][4] += values[4]
                        welayatDictHoz['Lebap wel.'][5] += values[5]
                if 'Balkan' in country:
                    if 'Balkan wel.' not in welayatDictHoz:
                        welayatDictHoz['Balkan wel.'] = values
                    else:
                        welayatDictHoz['Balkan wel.'][1] += values[1]
                        welayatDictHoz['Balkan wel.'][2] += values[2]
                        welayatDictHoz['Balkan wel.'][3] += values[3]
                        welayatDictHoz['Balkan wel.'][4] += values[4]
                        welayatDictHoz['Balkan wel.'][5] += values[5]
                # if 'Sotowyy' in country:
                #     if 'Sotowyy' not in welayatDictHoz:
                #         welayatDictHoz['Sotowyy'] = values
                #     else:
                #         welayatDictHoz['Sotowyy'][1] += values[1]
                #         welayatDictHoz['Sotowyy'][2] += values[2]
                #         welayatDictHoz['Sotowyy'][3] += values[3]
                #         welayatDictHoz['Sotowyy'][4] += values[4]
                #         welayatDictHoz['Sotowyy'][5] += values[5]
                # if country not in welayatDictHoz:
                #     welayatDictHoz[country] = values
                # else:
                #     welayatDictHoz[2] = values[2]
                #     welayatDictHoz[3] = values[3]
                #     welayatDictHoz[4] = values[4]
                #     welayatDictHoz[5] = values[5]
                #     welayatDictHoz[6] = values[6]
            
            if country in sng:
                sngTotalHoz[0] += values[1] + values[2]
                sngTotalHoz[1] += values[3] + values[4]
                sngTotalHoz[2] += values[5]
                itogoTotalHoz[0] += values[1] + values[2]
                itogoTotalHoz[1] += values[3] + values[4]
                itogoTotalHoz[2] += values[5]
                if country not in sngDictHoz:
                    sngDictHoz[country] = values
                else:
                    sngDictHoz[2] = values[2]
                    sngDictHoz[3] = values[3]
                    sngDictHoz[4] = values[4]
                    sngDictHoz[5] = values[5]
                    sngDictHoz[6] = values[6]

            if country in international:
                internationalTotalHoz[0] += values[1] + values[2]
                internationalTotalHoz[1] += values[3] + values[4]
                internationalTotalHoz[2] += values[5]
                itogoTotalHoz[0] += values[1] + values[2]
                itogoTotalHoz[1] += values[3] + values[4]
                itogoTotalHoz[2] += values[5]
                if country not in internationalDictHoz:
                    internationalDictHoz[country] = values
                else:
                    internationalDictHoz[2] = values[2]
                    internationalDictHoz[3] = values[3]
                    internationalDictHoz[4] = values[4]
                    internationalDictHoz[5] = values[5]
                    internationalDictHoz[6] = values[6]

   
        context['etrapDictHoz'] = etrapDictHoz
        context['etrapTotalHoz'] = etrapTotalHoz

        context['welayatDictHoz'] = welayatDictHoz
        context['welayatTotalHoz'] = welayatTotalHoz

        context['sngDictHoz'] = sngDictHoz
        context['sngTotalHoz'] = sngTotalHoz

        context['internationalDictHoz'] = internationalDictHoz
        context['internationalTotalHoz'] = internationalTotalHoz


        context['itogoTotalHoz'] = itogoTotalHoz


        # для Хоз ##############################################################################################
        ##################################################################################################################
        ##################################################################################################################


        ##################################################################################################################
        ##################################################################################################################
        # для населения ############################################################################################
        etrapDictNaseleniya = {} # {starna: [tarif, day_count, night_count, day_minut, night_minut, totalsum]}
        etrapTotalNaseleniya = [0,0,0] # [totalConnect, totalMinut, totalPrice]

        welayatDictNaseleniya = {}
        welayatTotalNaseleniya = [0,0,0]

        sngDictNaseleniya = {}
        sngTotalNaseleniya = [0,0,0]

        internationalDictNaseleniya = {}
        internationalTotalNaseleniya = [0,0,0]

        itogoTotalNaseleniya = [0,0,0]


        for country, values in daysAndNightCallsNaseleniya.items():
            if country in etraps:
                etrapTotalNaseleniya[0] += values[1] + values[2]
                etrapTotalNaseleniya[1] += values[3] + values[4]
                etrapTotalNaseleniya[2] += values[5]
                itogoTotalNaseleniya[0] += values[1] + values[2]
                itogoTotalNaseleniya[1] += values[3] + values[4]
                itogoTotalNaseleniya[2] += values[5]
                if country not in etrapDictNaseleniya:
                    etrapDictNaseleniya[country] = values
                else:
                    etrapDictNaseleniya[1] = values[1]
                    etrapDictNaseleniya[2] = values[1]
                    etrapDictNaseleniya[3] = values[3]
                    etrapDictNaseleniya[4] = values[4]
                    etrapDictNaseleniya[5] = values[5]
            if country in turkmenistan:
                welayatTotalNaseleniya[0] += values[1] + values[2]
                welayatTotalNaseleniya[1] += values[3] + values[4]
                welayatTotalNaseleniya[2] += values[5]
                itogoTotalNaseleniya[0] += values[1] + values[2]
                itogoTotalNaseleniya[1] += values[3] + values[4]
                itogoTotalNaseleniya[2] += values[5]
                if 'Ahal' in country or 'Sotowyy' in country:
                    if 'Ahal wel.' not in welayatDictNaseleniya:
                        welayatDictNaseleniya['Ahal wel.'] = values
                    else:
                        # print('2222',values)
                        welayatDictNaseleniya['Ahal wel.'][1] += values[1]
                        welayatDictNaseleniya['Ahal wel.'][2] += values[2]
                        welayatDictNaseleniya['Ahal wel.'][3] += values[3]
                        welayatDictNaseleniya['Ahal wel.'][4] += values[4]
                        welayatDictNaseleniya['Ahal wel.'][5] += values[5]
                if 'Ashgabat' in country:
                    if 'Ashgabat s.' not in welayatDictNaseleniya:
                        welayatDictNaseleniya['Ashgabat s.'] = values
                    else:
                        welayatDictNaseleniya['Ashgabat s.'][1] += values[1]
                        welayatDictNaseleniya['Ashgabat s.'][2] += values[2]
                        welayatDictNaseleniya['Ashgabat s.'][3] += values[3]
                        welayatDictNaseleniya['Ashgabat s.'][4] += values[4]
                        welayatDictNaseleniya['Ashgabat s.'][5] += values[5]
                if 'Mary' in country:
                    if 'Mary wel.' not in welayatDictNaseleniya:
                        welayatDictNaseleniya['Mary wel.'] = values
                    else:
                        welayatDictNaseleniya['Mary wel.'][1] += values[1]
                        welayatDictNaseleniya['Mary wel.'][2] += values[2]
                        welayatDictNaseleniya['Mary wel.'][3] += values[3]
                        welayatDictNaseleniya['Mary wel.'][4] += values[4]
                        welayatDictNaseleniya['Mary wel.'][5] += values[5]
                if 'Lebap' in country:
                    if 'Lebap wel.' not in welayatDictNaseleniya:
                        welayatDictNaseleniya['Lebap wel.'] = values
                    else:
                        welayatDictNaseleniya['Lebap wel.'][1] += values[1]
                        welayatDictNaseleniya['Lebap wel.'][2] += values[2]
                        welayatDictNaseleniya['Lebap wel.'][3] += values[3]
                        welayatDictNaseleniya['Lebap wel.'][4] += values[4]
                        welayatDictNaseleniya['Lebap wel.'][5] += values[5]
                if 'Balkan' in country:
                    if 'Balkan wel.' not in welayatDictNaseleniya:
                        welayatDictNaseleniya['Balkan wel.'] = values
                    else:
                        welayatDictNaseleniya['Balkan wel.'][1] += values[1]
                        welayatDictNaseleniya['Balkan wel.'][2] += values[2]
                        welayatDictNaseleniya['Balkan wel.'][3] += values[3]
                        welayatDictNaseleniya['Balkan wel.'][4] += values[4]
                        welayatDictNaseleniya['Balkan wel.'][5] += values[5]
                # if 'Sotowyy' in country:
                #     if 'Sotowyy' not in welayatDictNaseleniya:
                #         welayatDictNaseleniya['Sotowyy'] = values
                #     else:
                #         welayatDictNaseleniya['Sotowyy'][1] += values[1]
                #         welayatDictNaseleniya['Sotowyy'][2] += values[2]
                #         welayatDictNaseleniya['Sotowyy'][3] += values[3]
                #         welayatDictNaseleniya['Sotowyy'][4] += values[4]
                #         welayatDictNaseleniya['Sotowyy'][5] += values[5]
                # if country not in welayatDictNaseleniya:
                #     welayatDictNaseleniya[country] = values
                # else:
                #     welayatDictNaseleniya[2] = values[2]
                #     welayatDictNaseleniya[3] = values[3]
                #     welayatDictNaseleniya[4] = values[4]
                #     welayatDictNaseleniya[5] = values[5]
                #     welayatDictNaseleniya[6] = values[6]
            
            if country in sng:
                sngTotalNaseleniya[0] += values[1] + values[2]
                sngTotalNaseleniya[1] += values[3] + values[4]
                sngTotalNaseleniya[2] += values[5]
                itogoTotalNaseleniya[0] += values[1] + values[2]
                itogoTotalNaseleniya[1] += values[3] + values[4]
                itogoTotalNaseleniya[2] += values[5]
                if country not in sngDictNaseleniya:
                    sngDictNaseleniya[country] = values
                else:
                    sngDictNaseleniya[2] = values[2]
                    sngDictNaseleniya[3] = values[3]
                    sngDictNaseleniya[4] = values[4]
                    sngDictNaseleniya[5] = values[5]
                    sngDictNaseleniya[6] = values[6]

            if country in international:
                internationalTotalNaseleniya[0] += values[1] + values[2]
                internationalTotalNaseleniya[1] += values[3] + values[4]
                internationalTotalNaseleniya[2] += values[5]
                itogoTotalNaseleniya[0] += values[1] + values[2]
                itogoTotalNaseleniya[1] += values[3] + values[4]
                itogoTotalNaseleniya[2] += values[5]
                if country not in internationalDictNaseleniya:
                    internationalDictNaseleniya[country] = values
                else:
                    internationalDictNaseleniya[2] = values[2]
                    internationalDictNaseleniya[3] = values[3]
                    internationalDictNaseleniya[4] = values[4]
                    internationalDictNaseleniya[5] = values[5]
                    internationalDictNaseleniya[6] = values[6]

   
        context['etrapDictNaseleniya'] = etrapDictNaseleniya
        context['etrapTotalNaseleniya'] = etrapTotalNaseleniya

        context['welayatDictNaseleniya'] = welayatDictNaseleniya
        context['welayatTotalNaseleniya'] = welayatTotalNaseleniya

        context['sngDictNaseleniya'] = sngDictNaseleniya
        context['sngTotalNaseleniya'] = sngTotalNaseleniya

        context['internationalDictNaseleniya'] = internationalDictNaseleniya
        context['internationalTotalNaseleniya'] = internationalTotalNaseleniya

        context['itogoTotalNaseleniya'] = itogoTotalNaseleniya


        # для населения ############################################################################################
        ##################################################################################################################
        ##################################################################################################################


        ##################################################################################################################
        ##################################################################################################################
        # для АТС ##############################################################################################
        etrapDictATS = {} # {starna: [tarif, day_count, night_count, day_minut, night_minut, totalsum]}
        etrapTotalATS = [0,0,0] # [totalConnect, totalMinut, totalPrice]

        welayatDictATS = {}
        welayatTotalATS = [0,0,0]

        sngDictATS = {}
        sngTotalATS = [0,0,0]

        internationalDictATS = {}
        internationalTotalATS = [0,0,0]

        itogoTotalATS = [0,0,0]


        for country, values in daysAndNightCallsATS.items():
            if country in etraps:
                etrapTotalATS[0] += values[1] + values[2]
                etrapTotalATS[1] += values[3] + values[4]
                etrapTotalATS[2] += values[5]
                itogoTotalATS[0] += values[1] + values[2]
                itogoTotalATS[1] += values[3] + values[4]
                itogoTotalATS[2] += values[5]
                if country not in etrapDictATS:
                    etrapDictATS[country] = values
                else:
                    # print('test')
                    etrapDictATS[1] = values[1]
                    etrapDictATS[2] = values[1]
                    etrapDictATS[3] = values[3]
                    etrapDictATS[4] = values[4]
                    etrapDictATS[5] = values[5]

            if country in turkmenistan:
                welayatTotalATS[0] += values[1] + values[2]
                welayatTotalATS[1] += values[3] + values[4]
                welayatTotalATS[2] += values[5]
                itogoTotalATS[0] += values[1] + values[2]
                itogoTotalATS[1] += values[3] + values[4]
                itogoTotalATS[2] += values[5]
                if 'Ahal' in country or 'Sotowyy' in country:
                    if 'Ahal wel.' not in welayatDictATS:
                        welayatDictATS['Ahal wel.'] = values
                    else:
                        # print('2222',values)
                        welayatDictATS['Ahal wel.'][1] += values[1]
                        welayatDictATS['Ahal wel.'][2] += values[2]
                        welayatDictATS['Ahal wel.'][3] += values[3]
                        welayatDictATS['Ahal wel.'][4] += values[4]
                        welayatDictATS['Ahal wel.'][5] += values[5]
                if 'Ashgabat' in country:
                    if 'Ashgabat s.' not in welayatDictATS:
                        welayatDictATS['Ashgabat s.'] = values
                    else:
                        welayatDictATS['Ashgabat s.'][1] += values[1]
                        welayatDictATS['Ashgabat s.'][2] += values[2]
                        welayatDictATS['Ashgabat s.'][3] += values[3]
                        welayatDictATS['Ashgabat s.'][4] += values[4]
                        welayatDictATS['Ashgabat s.'][5] += values[5]
                if 'Mary' in country:
                    if 'Mary wel.' not in welayatDictATS:
                        welayatDictATS['Mary wel.'] = values
                    else:
                        welayatDictATS['Mary wel.'][1] += values[1]
                        welayatDictATS['Mary wel.'][2] += values[2]
                        welayatDictATS['Mary wel.'][3] += values[3]
                        welayatDictATS['Mary wel.'][4] += values[4]
                        welayatDictATS['Mary wel.'][5] += values[5]
                if 'Lebap' in country:
                    if 'Lebap wel.' not in welayatDictATS:
                        welayatDictATS['Lebap wel.'] = values
                    else:
                        welayatDictATS['Lebap wel.'][1] += values[1]
                        welayatDictATS['Lebap wel.'][2] += values[2]
                        welayatDictATS['Lebap wel.'][3] += values[3]
                        welayatDictATS['Lebap wel.'][4] += values[4]
                        welayatDictATS['Lebap wel.'][5] += values[5]
                if 'Balkan' in country:
                    if 'Balkan wel.' not in welayatDictATS:
                        welayatDictATS['Balkan wel.'] = values
                    else:
                        welayatDictATS['Balkan wel.'][1] += values[1]
                        welayatDictATS['Balkan wel.'][2] += values[2]
                        welayatDictATS['Balkan wel.'][3] += values[3]
                        welayatDictATS['Balkan wel.'][4] += values[4]
                        welayatDictATS['Balkan wel.'][5] += values[5]
                # if 'Sotowyy' in country:
                #     if 'Sotowyy' not in welayatDictATS:
                #         welayatDictATS['Sotowyy'] = values
                #     else:
                #         welayatDictATS['Sotowyy'][1] += values[1]
                #         welayatDictATS['Sotowyy'][2] += values[2]
                #         welayatDictATS['Sotowyy'][3] += values[3]
                #         welayatDictATS['Sotowyy'][4] += values[4]
                #         welayatDictATS['Sotowyy'][5] += values[5]

                # if country not in welayatDictATS:
                #     welayatDictATS[country] = values
                # else:
                #     print('test2')
                #     welayatDictATS[2] = values[2]
                #     welayatDictATS[3] = values[3]
                #     welayatDictATS[4] = values[4]
                #     welayatDictATS[5] = values[5]
                #     welayatDictATS[6] = values[6]
            
            if country in sng:
                sngTotalATS[0] += values[1] + values[2]
                sngTotalATS[1] += values[3] + values[4]
                sngTotalATS[2] += values[5]
                itogoTotalATS[0] += values[1] + values[2]
                itogoTotalATS[1] += values[3] + values[4]
                itogoTotalATS[2] += values[5]
                if country not in sngDictATS:
                    sngDictATS[country] = values
                else:
                    # print('test3')
                    sngDictATS[2] = values[2]
                    sngDictATS[3] = values[3]
                    sngDictATS[4] = values[4]
                    sngDictATS[5] = values[5]
                    sngDictATS[6] = values[6]

            if country in international:
                internationalTotalATS[0] += values[1] + values[2]
                internationalTotalATS[1] += values[3] + values[4]
                internationalTotalATS[2] += values[5]
                itogoTotalATS[0] += values[1] + values[2]
                itogoTotalATS[1] += values[3] + values[4]
                itogoTotalATS[2] += values[5]
                if country not in internationalDictATS:
                    internationalDictATS[country] = values
                else:
                    # print('test4')
                    internationalDictATS[2] = values[2]
                    internationalDictATS[3] = values[3]
                    internationalDictATS[4] = values[4]
                    internationalDictATS[5] = values[5]
                    internationalDictATS[6] = values[6]
        for k, v in welayatDictATS.items():
            pass
            # print(k,v)
   
        context['etrapDictATS'] = etrapDictATS
        context['etrapTotalATS'] = etrapTotalATS

        context['welayatDictATS'] = welayatDictATS
        context['welayatTotalATS'] = welayatTotalATS

        context['sngDictATS'] = sngDictATS
        context['sngTotalATS'] = sngTotalATS

        context['internationalDictATS'] = internationalDictATS
        context['internationalTotalATS'] = internationalTotalATS

        context['itogoTotalATS'] = itogoTotalATS

        messages.success(request, 'Трафик готов')

        # для АТС ##############################################################################################
        ##################################################################################################################
        ##################################################################################################################


        ##################################################################################################################
        ##################################################################################################################
        # для Неопознанные (unknown) #####################################################################################
        etrapDictUnknownEdara = {} # {starna: [tarif, day_count, night_count, day_minut, night_minut, totalsum]}
        etrapTotalUnknownEdara = [0,0,0] # [totalConnect, totalMinut, totalPrice]

        welayatDictUnknownEdara = {}
        welayatTotalUnknownEdara = [0,0,0]

        sngDictUnknownEdara = {}
        sngTotalUnknownEdara = [0,0,0]

        internationalDictUnknownEdara = {}
        internationalTotalUnknownEdara = [0,0,0]

        itogoTotalUnknownEdara = [0,0,0]
        # print('1111',daysAndNightUnknownEdara)

        for country, values in daysAndNightUnknownEdara.items():
            if country in etraps:
                etrapTotalUnknownEdara[0] += values[1] + values[2]
                etrapTotalUnknownEdara[1] += values[3] + values[4]
                etrapTotalUnknownEdara[2] += values[5]
                itogoTotalUnknownEdara[0] += values[1] + values[2]
                itogoTotalUnknownEdara[1] += values[3] + values[4]
                itogoTotalUnknownEdara[2] += values[5]

                if country not in etrapDictUnknownEdara:
                    etrapDictUnknownEdara[country] = values
                else:
                    etrapDictUnknownEdara[1] = values[1]
                    etrapDictUnknownEdara[2] = values[1]
                    etrapDictUnknownEdara[3] = values[3]
                    etrapDictUnknownEdara[4] = values[4]
                    etrapDictUnknownEdara[5] = values[5]

            if country in turkmenistan:
                welayatTotalUnknownEdara[0] += values[1] + values[2]
                welayatTotalUnknownEdara[1] += values[3] + values[4]
                welayatTotalUnknownEdara[2] += values[5]
                itogoTotalUnknownEdara[0] += values[1] + values[2]
                itogoTotalUnknownEdara[1] += values[3] + values[4]
                itogoTotalUnknownEdara[2] += values[5]
                if 'Ahal' in country or 'Sotowyy' in country:
                    if 'Ahal wel.' not in welayatDictUnknownEdara:
                        welayatDictUnknownEdara['Ahal wel.'] = values
                    else:
                        welayatDictUnknownEdara['Ahal wel.'][1] += values[1]
                        welayatDictUnknownEdara['Ahal wel.'][2] += values[2]
                        welayatDictUnknownEdara['Ahal wel.'][3] += values[3]
                        welayatDictUnknownEdara['Ahal wel.'][4] += values[4]
                        welayatDictUnknownEdara['Ahal wel.'][5] += values[5]
                if 'Ashgabat' in country:
                    if 'Ashgabat s.' not in welayatDictUnknownEdara:
                        welayatDictUnknownEdara['Ashgabat s.'] = values
                    else:
                        welayatDictUnknownEdara['Ashgabat s.'][1] += values[1]
                        welayatDictUnknownEdara['Ashgabat s.'][2] += values[2]
                        welayatDictUnknownEdara['Ashgabat s.'][3] += values[3]
                        welayatDictUnknownEdara['Ashgabat s.'][4] += values[4]
                        welayatDictUnknownEdara['Ashgabat s.'][5] += values[5]
                if 'Mary' in country:
                    if 'Mary wel.' not in welayatDictUnknownEdara:
                        welayatDictUnknownEdara['Mary wel.'] = values
                    else:
                        welayatDictUnknownEdara['Mary wel.'][1] += values[1]
                        welayatDictUnknownEdara['Mary wel.'][2] += values[2]
                        welayatDictUnknownEdara['Mary wel.'][3] += values[3]
                        welayatDictUnknownEdara['Mary wel.'][4] += values[4]
                        welayatDictUnknownEdara['Mary wel.'][5] += values[5]
                if 'Lebap' in country:
                    if 'Lebap wel.' not in welayatDictUnknownEdara:
                        welayatDictUnknownEdara['Lebap wel.'] = values
                    else:
                        welayatDictUnknownEdara['Lebap wel.'][1] += values[1]
                        welayatDictUnknownEdara['Lebap wel.'][2] += values[2]
                        welayatDictUnknownEdara['Lebap wel.'][3] += values[3]
                        welayatDictUnknownEdara['Lebap wel.'][4] += values[4]
                        welayatDictUnknownEdara['Lebap wel.'][5] += values[5]
                if 'Balkan' in country:
                    if 'Balkan wel.' not in welayatDictUnknownEdara:
                        welayatDictUnknownEdara['Balkan wel.'] = values
                    else:
                        welayatDictUnknownEdara['Balkan wel.'][1] += values[1]
                        welayatDictUnknownEdara['Balkan wel.'][2] += values[2]
                        welayatDictUnknownEdara['Balkan wel.'][3] += values[3]
                        welayatDictUnknownEdara['Balkan wel.'][4] += values[4]
                        welayatDictUnknownEdara['Balkan wel.'][5] += values[5]
                # if 'Sotowyy' in country:
                #     if 'Sotowyy' not in welayatDictUnknownEdara:
                #         welayatDictUnknownEdara['Sotowyy'] = values
                #     else:
                #         welayatDictUnknownEdara['Sotowyy'][1] += values[1]
                #         welayatDictUnknownEdara['Sotowyy'][2] += values[2]
                #         welayatDictUnknownEdara['Sotowyy'][3] += values[3]
                #         welayatDictUnknownEdara['Sotowyy'][4] += values[4]
                #         welayatDictUnknownEdara['Sotowyy'][5] += values[5]
                # if country not in welayatDictBud:
                #     welayatDictBud[country] = values
                # else:
                #     welayatDictBud[2] = values[2]
                #     welayatDictBud[3] = values[3]
                #     welayatDictBud[4] = values[4]
                #     welayatDictBud[5] = values[5]
                #     welayatDictBud[6] = values[6]
            
            if country in sng:
                sngTotalUnknownEdara[0] += values[1] + values[2]
                sngTotalUnknownEdara[1] += values[3] + values[4]
                sngTotalUnknownEdara[2] += values[5]
                itogoTotalUnknownEdara[0] += values[1] + values[2]
                itogoTotalUnknownEdara[1] += values[3] + values[4]
                itogoTotalUnknownEdara[2] += values[5]
                if country not in sngDictUnknownEdara:
                    sngDictUnknownEdara[country] = values
                else:
                    sngDictUnknownEdara[2] = values[2]
                    sngDictUnknownEdara[3] = values[3]
                    sngDictUnknownEdara[4] = values[4]
                    sngDictUnknownEdara[5] = values[5]
                    sngDictUnknownEdara[6] = values[6]

            if country in international:
                internationalTotalUnknownEdara[0] += values[1] + values[2]
                internationalTotalUnknownEdara[1] += values[3] + values[4]
                internationalTotalUnknownEdara[2] += values[5]
                itogoTotalUnknownEdara[0] += values[1] + values[2]
                itogoTotalUnknownEdara[1] += values[3] + values[4]
                itogoTotalUnknownEdara[2] += values[5]
                if country not in internationalDictUnknownEdara:
                    internationalDictUnknownEdara[country] = values
                else:
                    internationalDictUnknownEdara[2] = values[2]
                    internationalDictUnknownEdara[3] = values[3]
                    internationalDictUnknownEdara[4] = values[4]
                    internationalDictUnknownEdara[5] = values[5]
                    internationalDictUnknownEdara[6] = values[6]

   
        context['etrapDictUnknownEdara'] = etrapDictUnknownEdara
        context['etrapTotalUnknownEdara'] = etrapTotalUnknownEdara

        context['welayatDictUnknownEdara'] = welayatDictUnknownEdara
        context['welayatTotalUnknownEdara'] = welayatTotalUnknownEdara

        context['sngDictUnknownEdara'] = sngDictUnknownEdara
        context['sngTotalUnknownEdara'] = sngTotalUnknownEdara

        context['internationalDictUnknownEdara'] = internationalDictUnknownEdara
        context['internationalTotalUnknownEdara'] = internationalTotalUnknownEdara

        context['itogoTotalUnknownEdara'] = itogoTotalUnknownEdara


        # для Неопознанные (unknown) #####################################################################################
        ##################################################################################################################
        ##################################################################################################################
        

    # print('GGGGGGGGGGGGGG', test_price)
    return render(request, 'telekom/MATB/otchyot/trafik.html', context)




# from django.shortcuts import render, redirect
# from telekom.models import LocalCall, NachMinus, NonLocalCall, UserTable, KodSumm
# from django.db.models import Sum
# from django.contrib import messages

# from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert
# from django.db.models import Q
# from datetime import date
# from datetime import time
# from datetime import datetime, timedelta
# from calendar import monthrange


# def trafik(request):
#     EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
#     if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
#         log = EtrapAndGroup[0]
#     else:
#         messages.error(request, f'Доступ только соотрудникам MATB')
#         return redirect('user-login')
    
    
    
#     context = {}
#     context['matbIndex'] = True
#     context['trafik'] = True
#     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
#     context['etraps'] = etraps
#     context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
#     context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

    


#     etrap = request.GET.get('etrap')
#     year = request.GET.get('year')
#     month_word = request.GET.get('month')

#     if etrap and year and month_word:
#         context['etrap'] = etrap
#         context['year'] = year
#         context['month'] = month_word
#         month_digit = monthСonvert(month_word)

#         days_in_choosed_month = monthrange(int(year), int(month_digit))[1]

#         # Конвертировать строки в объект даты
#         current_date = datetime.strptime(year + month_digit, '%Y%m')
#         # Добавить один месяц
#         next_month_date = current_date + timedelta(days=days_in_choosed_month)
#         nextYear = next_month_date.year
#         nextMonth = next_month_date.month
#         end2 = f"{nextYear}-{nextMonth}-01"

    
#         turkmenistan = ['Sotowyy',
#                 'Ashgabat','Ahal Baharly','Ahal Gokdepe','Ahal Kaka','Ahal Seraks','Ahal Tejen','Ahal Babadayhan','Ahal Anew','Ahal Abadan','Ahal Ruhabat','Ahal Ashgabat',
#                 'Balkan Nebitdag','Balkan Hazar','Balkan Gumdag','Balkan Gyzyl Atr','Balkan Turkmenbashy','Balkan Gumdag','Balkan Esenguly','Balkan Serdar','Balkan Bereket',
#                 'Balkan Magtymguly','Lebap Turkmenabat','Lebap Magdanly','Lebap Garashsyzlyk','Lebap Gazajak','Lebap Koytendag','Lebap Halach','Lebap Hojambaz','Lebap Garabekewul',
#                 'Lebap Atamyrat','Lebap Birata','Lebap Galkynysh','Lebap Sayat','Lebap Farap', 'Lebap Sakar','Lebap Seydi','Lebap Turkmenbashy','Lebap Serdarabat','Lebap Serdarabat',
#                 'Mary','Mary Garagum','Mary Wekilbazar','Mary Oguzhan','Mary Yoleten','Mary Serhetabat','Mary Bayramaly','Mary Murgap','Mary Sakarchage','Mary Tagtabazar','Mary Turkm-gala']

#         international = ['Fransiya','Germaniya','Gresiya','Wengriya','Italiya','Niderlandy','Norwegiya','Polsha','Rumyniya','Shwesiya','Shweysariya','Welikobritaniya',
#                 'Ispaniya','Albaniya','Andorra','Bosniya Gersogowina','Bolgariya','Horwatiya','Kipr', 'Estoniya','Finlyandiya','Gibraltar','Grenlandiya','Islandiya',
#                 'Latwiya','Lihtenshteyn','Litwa','Luksenburg','Makedoniya','Malta','Portugaliya','Slowakiya','Sloweniya','Yugoslawiya','Cheshskaya Respublika',
#                 'Gruziya','Ukraina','Afganistan','Turkiya','Iran','Awstriya',
#                 'Belgiya','Daniya','Awstraliya','Nowaya Zenlandiya','Fidji','Fransuskaya Polineziya','Kiribati','Nowaya Kaledoniya','Norfolkskiye ostrowa','Papua Nowaya Gwineya',
#                 'Tonga','Wanuatu','Hytay','Kuba','Indiya','Indoneziya','Yaponiya','Malaziya','Meksika','Myanma','Pakistan','Filipiny','Singapur','Yujnaya Koreya','Tailand','Wyetnam',
#                 'Bahreyn','Bangladesh','Bruney Daruesaalam','Kombodja','Kosta-Rika','Wostochnyy Timor','Gwatelama','Gaiti','Gonduras','Gonk-Kong','Irak','Izrail','Iordaniya','Kuweit',
#                 'Laos','Liwan','Makao (Aomyn)','Mongoliya','Nepal','Niderlandskie Antilly','Nikaragua','Sewernaya Koreya','Sewernyy Yemen','Oman','Panama' 'Katar','Saudowskaya Arawiya',
#                 'Yujnyy Yemen','Siriya','Taiwan','O.A.E','USA/CANADA','Argentina','Braziliya','Chili','Kolumbiya','Peru','Wenesuella','Boliwiya','Ekwador','Farerskie Ostrowa',
#                 'Fransuskatya Gwiana','Gayana','Martitnka','Surinam','Urugway','Egipet','UAR','Aljir','Angola','Benin','Botswana','Burkina Faso','Burundi','Kamerun','Kape Werde','SAR',
#                 'Chad','Kongo','Jibuti','Ekwatorialnaya gwineya','Efiopiya','Gabon','Gambiya','Gana','Gwineya','Gwineya Bissau','Keniya','Liberiya','Liviya','Madagaskar','Malawi','Mali',
#                 'Mawritaniya','Mawrikiy','Moroko','Mozambik','Namibiya','Niger','Nigeriya','Reonyon','Respublika Ruanda','Senegal','Seyshelskie ostrowa','Syerra Leonne','Somali','Sudan',
#                 'Tanzaniya','Respublika Togoleze','Tunis','Uganda','Zair','Zambiya','Zimbabwe']
            

#         sng = ['Armeniya', 'Belorussiya', 'Azerbayjan', 'Kazakstan', 'Kyrgystan', 'Rossiya', 'Tajikistan', 'Uzbekistan', 'Moldowa']

#         if etrap == 'Dashoguz':
#             ATSSALDO = -698
#         else:
#             ATSSALDO = -700
                
#         # print([f"{year}-{month_digit}-01", f"{nextYear}-{nextMonth}-01"])
#         # calls = NonLocalCall.objects.filter(DATE__range=[f"{year}-{month_digit}-01", f"{nextYear}-{nextMonth}-01"], SUB_A_etrap=etrap)
#         # calls = NonLocalCall.objects.filter(DATE__range=[f"{year}-{month_digit}-01", f"{year}-{month_digit}-{str(days_in_choosed_month)}"], SUB_A_etrap=etrap)
#         # calls = NonLocalCall.objects.filter(DATE__range=[f"2024-03-01", "2024-03-31"], SUB_A_etrap=etrap)
#         print('1111111111date', f"{year}-{month_digit}-01", f"{year}-{month_digit}-{days_in_choosed_month}", etrap)
#         calls = NonLocalCall.objects.filter(DATE__range=[f"{year}-{month_digit}-01", f"{year}-{month_digit}-{days_in_choosed_month}"], SUB_A_etrap=etrap)
#         total_test = 0
#         for i in calls:
#             total_test += int(i.MT) * i.price
#         print('total_test_trafik', total_test)

#         # test
#         users_test = UserTable.objects.filter(account__isnull=False, etrap='Turkmenbashy')
#         lists_my = []

#         total_kod = 0
#         for u in users_test:
#             if u.account == -700:
#                 lists_my.append(u.number)
#         total_price = 0
#         for c in calls:
#             if c.SUB_A in lists_my:
#                 total_price += c.total_price
#         # print('total_price', total_price)

        
#         nachMinus = NachMinus.objects.filter(year=year, month=month_digit, user__etrap=etrap)
#         nach_number_pk = {} # {number: [nach.pk, prochee]}
        
#         for n in nachMinus:
#             nach_number_pk[n.user.number] = [n.pk, n.prochee]


#         users = UserTable.objects.filter(account=ATSSALDO, etrap=etrap)
#         numbersATS = []
#         for i in users:
#             numbersATS.append(int(i.number))


#         times_day = []
#         time = datetime.strptime("06:00:00", "%H:%M:%S")
#         for j in range(1,100000):
#             time += timedelta(seconds=1)
#             if str(time)[-8:] == "22:00:00":
#                 break
#             times_day.append(str(time)[-8:])



#         # calls_day = calls.filter(START__in=times_day)
#         # calls_night = calls.filter(START__in=times_night)

        
       


        
#         daysAndNightCallsBud = {} # {starna: [tarif, day_count, night_count, day_minut, night_minut, totalsum]}
#         daysAndNightCallsHoz = {}
#         daysAndNightCallsATS = {}
#         daysAndNightCallsNaseleniya = {}
#         daysAndNightUnknownEdara = {}

#         daysCallCount = 0
#         nightCallCount = 0

#         #####################################################################################
#         users = UserTable.objects.filter(etrap=etrap, is_enterprises=False)
#         numbersIlat = []
#         for i in users:
#             numbersIlat.append(int(i.number))
        

#         users = UserTable.objects.filter(etrap=etrap, is_enterprises=True, hb__name='H')
#         numbersHoz = []
#         for i in users:
#             if i.account != ATSSALDO:
#                 numbersHoz.append(int(i.number))
      

#         users = UserTable.objects.filter(etrap=etrap, is_enterprises=True, hb__name='B')
#         numbersBud = []
#         for i in users:
#             numbersBud.append(int(i.number))
#         test_price = 0
        
#         for c in calls:
#             # День
#             daysCallCount += 1
#             hbi = c.edara
#             price=c.price
#             total_price = c.total_price
#             location = c.SUB_B_locations
#             MT = int(c.MT)
#             if c.START in times_day:
                
#                 # для бюд
#                 if int(c.SUB_A) in numbersBud: # in numbersBud
#                     if location not in daysAndNightCallsBud:
#                         daysAndNightCallsBud[location] = [price, 1, 0, MT, 0, total_price]
#                     else:
#                         daysAndNightCallsBud[location][1] += 1
#                         daysAndNightCallsBud[location][3] += MT
#                         daysAndNightCallsBud[location][5] += total_price
#                 # для хоз
#                 elif int(c.SUB_A) in numbersHoz: # in numbersHoz
#                     # для Хоз
#                     if location not in daysAndNightCallsHoz:
#                         daysAndNightCallsHoz[location] = [price, 1, 0, MT, 0, total_price]
#                     else:
#                         daysAndNightCallsHoz[location][1] += 1
#                         daysAndNightCallsHoz[location][3] += MT
#                         daysAndNightCallsHoz[location][5] += total_price
#                 elif int(c.SUB_A) in numbersATS:
#                     # для АТС
#                     test_price += total_price
#                     if location not in daysAndNightCallsATS:
#                         daysAndNightCallsATS[location] = [price, 1, 0, MT, 0, total_price]
#                     else:
#                         daysAndNightCallsATS[location][1] += 1
#                         daysAndNightCallsATS[location][3] += MT
#                         daysAndNightCallsATS[location][5] += total_price
#                 # для Неопознанных (Unknown)
#                 elif hbi == 'E':
#                     if location not in daysAndNightUnknownEdara:
#                         daysAndNightUnknownEdara[location] = [price, 1, 0, MT, 0, total_price]
#                     else:
#                         daysAndNightUnknownEdara[location][1] += 1
#                         daysAndNightUnknownEdara[location][3] += MT
#                         daysAndNightUnknownEdara[location][5] += total_price
#                 # для Населения
#                 else: # in numbersIlat
#                     if location not in daysAndNightCallsNaseleniya:
#                         daysAndNightCallsNaseleniya[location] = [price, 1, 0, MT, 0, total_price]
#                     else:
#                         daysAndNightCallsNaseleniya[location][1] += 1
#                         daysAndNightCallsNaseleniya[location][3] += MT
#                         daysAndNightCallsNaseleniya[location][5] += total_price
#             # Ночь
#             else:
#                 nightCallCount += 1
#                 price=c.price
#                 total_price = c.total_price
#                 location = c.SUB_B_locations
#                 MT = int(c.MT)
#                 # для бюд
#                 if int(c.SUB_A) in numbersBud:
#                     if location not in daysAndNightCallsBud:
#                         daysAndNightCallsBud[location] = [price, 0, 1, 0, MT, total_price]
#                     else:
#                         daysAndNightCallsBud[location][2] += 1
#                         daysAndNightCallsBud[location][4] += MT
#                         daysAndNightCallsBud[location][5] += total_price
#                 # для хоз и АТС
#                 elif int(c.SUB_A) in numbersHoz:
#                     # для хоз
#                     if int(c.SUB_A) not in numbersATS:
#                         if location not in daysAndNightCallsHoz:
#                             daysAndNightCallsHoz[location] = [price, 0, 1, 0, MT, total_price]
#                         else:
#                             daysAndNightCallsHoz[location][2] += 1
#                             daysAndNightCallsHoz[location][4] += MT
#                             daysAndNightCallsHoz[location][5] += total_price
#                 elif int(c.SUB_A) in numbersATS:          
#                     # для АТС
#                     test_price += total_price
#                     if location not in daysAndNightCallsATS:
#                         daysAndNightCallsATS[location] = [price, 0, 1, 0, MT, total_price]
#                     else:
#                         daysAndNightCallsATS[location][2] += 1
#                         daysAndNightCallsATS[location][4] += MT
#                         daysAndNightCallsATS[location][5] += total_price
#                 # для Неопознанных (Unknown)
#                 elif hbi == 'E':
#                     if location not in daysAndNightUnknownEdara:
#                         daysAndNightUnknownEdara[location] = [price, 0, 1, 0, MT, total_price]
#                     else:
#                         daysAndNightUnknownEdara[location][2] += 1
#                         daysAndNightUnknownEdara[location][4] += MT
#                         daysAndNightUnknownEdara[location][5] += total_price
#                 # для Населения
#                 else:
#                     if location not in daysAndNightCallsNaseleniya:
#                         daysAndNightCallsNaseleniya[location] = [price, 0, 1, 0, MT, total_price]
#                     else:
#                         daysAndNightCallsNaseleniya[location][2] += 1
#                         daysAndNightCallsNaseleniya[location][4] += MT
#                         daysAndNightCallsNaseleniya[location][5] += total_price
                

      
#         # ✅ По просьбе пользователя: "На сумму манат" в разделе "Трафик
#         # междугородней связи АТС (по предприятиям (Хоз расчет))" — всегда
#         # Количество минут × Тариф ((day_minut+night_minut) * price), а не
#         # накопленная сумма total_price по звонкам (которая на реальных данных
#         # чуть отличалась из-за разных цен/округления на отдельных звонках —
#         # пример: Boldumsaz, июнь 2026, Dashoguz: 3030+55 мин * 0.14 = 431.90,
#         # а накопленная сумма была 427.82). Только для Hoz — Bud/Население/
#         # АТС/Неопознанные не трогаем.
#         for _values in daysAndNightCallsHoz.values():
#             _values[5] = (_values[3] + _values[4]) * _values[0]

#         context['daysAndNightCallsBud'] = daysAndNightCallsBud
#         context['daysAndNightCallsHoz'] = daysAndNightCallsHoz
#         context['daysAndNightCallsATS'] = daysAndNightCallsATS
#         context['daysAndNightCallsNaseleniya'] = daysAndNightCallsNaseleniya
#         context['daysAndNightUnknownEdara'] = daysAndNightUnknownEdara
      
#         ##################################################################################################################
#         ##################################################################################################################
#         # для Бюджет ##############################################################################################

#         etrapDictBud = {} # {starna: [tarif, day_count, night_count, day_minut, night_minut, totalsum]}
#         etrapTotalBud = [0,0,0] # [totalConnect, totalMinut, totalPrice]

#         welayatDictBud = {}
#         welayatTotalBud = [0,0,0]

#         sngDictBud = {}
#         sngTotalBud = [0,0,0]

#         internationalDictBud = {}
#         internationalTotalBud = [0,0,0]

#         itogoTotalBud = [0,0,0]

#         for country, values in daysAndNightCallsBud.items():
#             if country in etraps:
#                 etrapTotalBud[0] += values[1] + values[2]
#                 etrapTotalBud[1] += values[3] + values[4]
#                 etrapTotalBud[2] += values[5]
#                 itogoTotalBud[0] += values[1] + values[2]
#                 itogoTotalBud[1] += values[3] + values[4]
#                 itogoTotalBud[2] += values[5]

#                 if country not in etrapDictBud:
#                     etrapDictBud[country] = values
#                 else:
#                     etrapDictBud[1] = values[1]
#                     etrapDictBud[2] = values[1]
#                     etrapDictBud[3] = values[3]
#                     etrapDictBud[4] = values[4]
#                     etrapDictBud[5] = values[5]

#             if country in turkmenistan:
#                 welayatTotalBud[0] += values[1] + values[2]
#                 welayatTotalBud[1] += values[3] + values[4]
#                 welayatTotalBud[2] += values[5]
#                 itogoTotalBud[0] += values[1] + values[2]
#                 itogoTotalBud[1] += values[3] + values[4]
#                 itogoTotalBud[2] += values[5]
#                 if 'Ahal' in country or 'Sotowyy' in country:
#                     if 'Ahal wel.' not in welayatDictBud:
#                         welayatDictBud['Ahal wel.'] = values
#                     else:
#                         welayatDictBud['Ahal wel.'][1] += values[1]
#                         welayatDictBud['Ahal wel.'][2] += values[2]
#                         welayatDictBud['Ahal wel.'][3] += values[3]
#                         welayatDictBud['Ahal wel.'][4] += values[4]
#                         welayatDictBud['Ahal wel.'][5] += values[5]
#                 if 'Ashgabat' in country:
#                     if 'Ashgabat s.' not in welayatDictBud:
#                         welayatDictBud['Ashgabat s.'] = values
#                     else:
#                         welayatDictBud['Ashgabat s.'][1] += values[1]
#                         welayatDictBud['Ashgabat s.'][2] += values[2]
#                         welayatDictBud['Ashgabat s.'][3] += values[3]
#                         welayatDictBud['Ashgabat s.'][4] += values[4]
#                         welayatDictBud['Ashgabat s.'][5] += values[5]
#                 if 'Mary' in country:
#                     if 'Mary wel.' not in welayatDictBud:
#                         welayatDictBud['Mary wel.'] = values
#                     else:
#                         welayatDictBud['Mary wel.'][1] += values[1]
#                         welayatDictBud['Mary wel.'][2] += values[2]
#                         welayatDictBud['Mary wel.'][3] += values[3]
#                         welayatDictBud['Mary wel.'][4] += values[4]
#                         welayatDictBud['Mary wel.'][5] += values[5]
#                 if 'Lebap' in country:
#                     if 'Lebap wel.' not in welayatDictBud:
#                         welayatDictBud['Lebap wel.'] = values
#                     else:
#                         welayatDictBud['Lebap wel.'][1] += values[1]
#                         welayatDictBud['Lebap wel.'][2] += values[2]
#                         welayatDictBud['Lebap wel.'][3] += values[3]
#                         welayatDictBud['Lebap wel.'][4] += values[4]
#                         welayatDictBud['Lebap wel.'][5] += values[5]
#                 if 'Balkan' in country:
#                     if 'Balkan wel.' not in welayatDictBud:
#                         welayatDictBud['Balkan wel.'] = values
#                     else:
#                         welayatDictBud['Balkan wel.'][1] += values[1]
#                         welayatDictBud['Balkan wel.'][2] += values[2]
#                         welayatDictBud['Balkan wel.'][3] += values[3]
#                         welayatDictBud['Balkan wel.'][4] += values[4]
#                         welayatDictBud['Balkan wel.'][5] += values[5]
#                 # if 'Sotowyy' in country:
#                 #     if 'Sotowyy' not in welayatDictBud:
#                 #         welayatDictBud['Sotowyy'] = values
#                 #     else:
#                 #         welayatDictBud['Sotowyy'][1] += values[1]
#                 #         welayatDictBud['Sotowyy'][2] += values[2]
#                 #         welayatDictBud['Sotowyy'][3] += values[3]
#                 #         welayatDictBud['Sotowyy'][4] += values[4]
#                 #         welayatDictBud['Sotowyy'][5] += values[5]
#                 # if country not in welayatDictBud:
#                 #     welayatDictBud[country] = values
#                 # else:
#                 #     welayatDictBud[2] = values[2]
#                 #     welayatDictBud[3] = values[3]
#                 #     welayatDictBud[4] = values[4]
#                 #     welayatDictBud[5] = values[5]
#                 #     welayatDictBud[6] = values[6]
            
#             if country in sng:
#                 sngTotalBud[0] += values[1] + values[2]
#                 sngTotalBud[1] += values[3] + values[4]
#                 sngTotalBud[2] += values[5]
#                 itogoTotalBud[0] += values[1] + values[2]
#                 itogoTotalBud[1] += values[3] + values[4]
#                 itogoTotalBud[2] += values[5]
#                 if country not in sngDictBud:
#                     sngDictBud[country] = values
#                 else:
#                     sngDictBud[2] = values[2]
#                     sngDictBud[3] = values[3]
#                     sngDictBud[4] = values[4]
#                     sngDictBud[5] = values[5]
#                     sngDictBud[6] = values[6]

#             if country in international:
#                 internationalTotalBud[0] += values[1] + values[2]
#                 internationalTotalBud[1] += values[3] + values[4]
#                 internationalTotalBud[2] += values[5]
#                 itogoTotalBud[0] += values[1] + values[2]
#                 itogoTotalBud[1] += values[3] + values[4]
#                 itogoTotalBud[2] += values[5]
#                 if country not in internationalDictBud:
#                     internationalDictBud[country] = values
#                 else:
#                     internationalDictBud[2] = values[2]
#                     internationalDictBud[3] = values[3]
#                     internationalDictBud[4] = values[4]
#                     internationalDictBud[5] = values[5]
#                     internationalDictBud[6] = values[6]

   
#         context['etrapDictBud'] = etrapDictBud
#         context['etrapTotalBud'] = etrapTotalBud

#         context['welayatDictBud'] = welayatDictBud
#         context['welayatTotalBud'] = welayatTotalBud

#         context['sngDictBud'] = sngDictBud
#         context['sngTotalBud'] = sngTotalBud

#         context['internationalDictBud'] = internationalDictBud
#         context['internationalTotalBud'] = internationalTotalBud

#         context['itogoTotalBud'] = itogoTotalBud


#         # для Бюджет ##############################################################################################
#         ##################################################################################################################
#         ##################################################################################################################

#         ##################################################################################################################
#         ##################################################################################################################
#         # для Хоз ##############################################################################################
#         etrapDictHoz = {} # {starna: [tarif, day_count, night_count, day_minut, night_minut, totalsum]}
#         etrapTotalHoz = [0,0,0] # [totalConnect, totalMinut, totalPrice]

#         welayatDictHoz = {}
#         welayatTotalHoz = [0,0,0]

#         sngDictHoz = {}
#         sngTotalHoz = [0,0,0]

#         internationalDictHoz = {}
#         internationalTotalHoz = [0,0,0]

#         itogoTotalHoz = [0,0,0]


#         for country, values in daysAndNightCallsHoz.items():
#             if country in etraps:
#                 etrapTotalHoz[0] += values[1] + values[2]
#                 etrapTotalHoz[1] += values[3] + values[4]
#                 etrapTotalHoz[2] += values[5]
#                 itogoTotalHoz[0] += values[1] + values[2]
#                 itogoTotalHoz[1] += values[3] + values[4]
#                 itogoTotalHoz[2] += values[5]
#                 if country not in etrapDictHoz:
#                     etrapDictHoz[country] = values
#                 else:
#                     etrapDictHoz[1] = values[1]
#                     etrapDictHoz[2] = values[1]
#                     etrapDictHoz[3] = values[3]
#                     etrapDictHoz[4] = values[4]
#                     etrapDictHoz[5] = values[5]

#             if country in turkmenistan:
#                 welayatTotalHoz[0] += values[1] + values[2]
#                 welayatTotalHoz[1] += values[3] + values[4]
#                 welayatTotalHoz[2] += values[5]
#                 itogoTotalHoz[0] += values[1] + values[2]
#                 itogoTotalHoz[1] += values[3] + values[4]
#                 itogoTotalHoz[2] += values[5]
#                 if 'Ahal' in country or 'Sotowyy' in country:
#                     if 'Ahal wel.' not in welayatDictHoz:
#                         welayatDictHoz['Ahal wel.'] = values
#                     else:
#                         # print('2222',values)
#                         welayatDictHoz['Ahal wel.'][1] += values[1]
#                         welayatDictHoz['Ahal wel.'][2] += values[2]
#                         welayatDictHoz['Ahal wel.'][3] += values[3]
#                         welayatDictHoz['Ahal wel.'][4] += values[4]
#                         welayatDictHoz['Ahal wel.'][5] += values[5]
#                 if 'Ashgabat' in country:
#                     if 'Ashgabat s.' not in welayatDictHoz:
#                         welayatDictHoz['Ashgabat s.'] = values
#                     else:
#                         welayatDictHoz['Ashgabat s.'][1] += values[1]
#                         welayatDictHoz['Ashgabat s.'][2] += values[2]
#                         welayatDictHoz['Ashgabat s.'][3] += values[3]
#                         welayatDictHoz['Ashgabat s.'][4] += values[4]
#                         welayatDictHoz['Ashgabat s.'][5] += values[5]
#                 if 'Mary' in country:
#                     if 'Mary wel.' not in welayatDictHoz:
#                         welayatDictHoz['Mary wel.'] = values
#                     else:
#                         welayatDictHoz['Mary wel.'][1] += values[1]
#                         welayatDictHoz['Mary wel.'][2] += values[2]
#                         welayatDictHoz['Mary wel.'][3] += values[3]
#                         welayatDictHoz['Mary wel.'][4] += values[4]
#                         welayatDictHoz['Mary wel.'][5] += values[5]
#                 if 'Lebap' in country:
#                     if 'Lebap wel.' not in welayatDictHoz:
#                         welayatDictHoz['Lebap wel.'] = values
#                     else:
#                         welayatDictHoz['Lebap wel.'][1] += values[1]
#                         welayatDictHoz['Lebap wel.'][2] += values[2]
#                         welayatDictHoz['Lebap wel.'][3] += values[3]
#                         welayatDictHoz['Lebap wel.'][4] += values[4]
#                         welayatDictHoz['Lebap wel.'][5] += values[5]
#                 if 'Balkan' in country:
#                     if 'Balkan wel.' not in welayatDictHoz:
#                         welayatDictHoz['Balkan wel.'] = values
#                     else:
#                         welayatDictHoz['Balkan wel.'][1] += values[1]
#                         welayatDictHoz['Balkan wel.'][2] += values[2]
#                         welayatDictHoz['Balkan wel.'][3] += values[3]
#                         welayatDictHoz['Balkan wel.'][4] += values[4]
#                         welayatDictHoz['Balkan wel.'][5] += values[5]
#                 # if 'Sotowyy' in country:
#                 #     if 'Sotowyy' not in welayatDictHoz:
#                 #         welayatDictHoz['Sotowyy'] = values
#                 #     else:
#                 #         welayatDictHoz['Sotowyy'][1] += values[1]
#                 #         welayatDictHoz['Sotowyy'][2] += values[2]
#                 #         welayatDictHoz['Sotowyy'][3] += values[3]
#                 #         welayatDictHoz['Sotowyy'][4] += values[4]
#                 #         welayatDictHoz['Sotowyy'][5] += values[5]
#                 # if country not in welayatDictHoz:
#                 #     welayatDictHoz[country] = values
#                 # else:
#                 #     welayatDictHoz[2] = values[2]
#                 #     welayatDictHoz[3] = values[3]
#                 #     welayatDictHoz[4] = values[4]
#                 #     welayatDictHoz[5] = values[5]
#                 #     welayatDictHoz[6] = values[6]
            
#             if country in sng:
#                 sngTotalHoz[0] += values[1] + values[2]
#                 sngTotalHoz[1] += values[3] + values[4]
#                 sngTotalHoz[2] += values[5]
#                 itogoTotalHoz[0] += values[1] + values[2]
#                 itogoTotalHoz[1] += values[3] + values[4]
#                 itogoTotalHoz[2] += values[5]
#                 if country not in sngDictHoz:
#                     sngDictHoz[country] = values
#                 else:
#                     sngDictHoz[2] = values[2]
#                     sngDictHoz[3] = values[3]
#                     sngDictHoz[4] = values[4]
#                     sngDictHoz[5] = values[5]
#                     sngDictHoz[6] = values[6]

#             if country in international:
#                 internationalTotalHoz[0] += values[1] + values[2]
#                 internationalTotalHoz[1] += values[3] + values[4]
#                 internationalTotalHoz[2] += values[5]
#                 itogoTotalHoz[0] += values[1] + values[2]
#                 itogoTotalHoz[1] += values[3] + values[4]
#                 itogoTotalHoz[2] += values[5]
#                 if country not in internationalDictHoz:
#                     internationalDictHoz[country] = values
#                 else:
#                     internationalDictHoz[2] = values[2]
#                     internationalDictHoz[3] = values[3]
#                     internationalDictHoz[4] = values[4]
#                     internationalDictHoz[5] = values[5]
#                     internationalDictHoz[6] = values[6]

   
#         context['etrapDictHoz'] = etrapDictHoz
#         context['etrapTotalHoz'] = etrapTotalHoz

#         context['welayatDictHoz'] = welayatDictHoz
#         context['welayatTotalHoz'] = welayatTotalHoz

#         context['sngDictHoz'] = sngDictHoz
#         context['sngTotalHoz'] = sngTotalHoz

#         context['internationalDictHoz'] = internationalDictHoz
#         context['internationalTotalHoz'] = internationalTotalHoz


#         context['itogoTotalHoz'] = itogoTotalHoz


#         # для Хоз ##############################################################################################
#         ##################################################################################################################
#         ##################################################################################################################


#         ##################################################################################################################
#         ##################################################################################################################
#         # для населения ############################################################################################
#         etrapDictNaseleniya = {} # {starna: [tarif, day_count, night_count, day_minut, night_minut, totalsum]}
#         etrapTotalNaseleniya = [0,0,0] # [totalConnect, totalMinut, totalPrice]

#         welayatDictNaseleniya = {}
#         welayatTotalNaseleniya = [0,0,0]

#         sngDictNaseleniya = {}
#         sngTotalNaseleniya = [0,0,0]

#         internationalDictNaseleniya = {}
#         internationalTotalNaseleniya = [0,0,0]

#         itogoTotalNaseleniya = [0,0,0]


#         for country, values in daysAndNightCallsNaseleniya.items():
#             if country in etraps:
#                 etrapTotalNaseleniya[0] += values[1] + values[2]
#                 etrapTotalNaseleniya[1] += values[3] + values[4]
#                 etrapTotalNaseleniya[2] += values[5]
#                 itogoTotalNaseleniya[0] += values[1] + values[2]
#                 itogoTotalNaseleniya[1] += values[3] + values[4]
#                 itogoTotalNaseleniya[2] += values[5]
#                 if country not in etrapDictNaseleniya:
#                     etrapDictNaseleniya[country] = values
#                 else:
#                     etrapDictNaseleniya[1] = values[1]
#                     etrapDictNaseleniya[2] = values[1]
#                     etrapDictNaseleniya[3] = values[3]
#                     etrapDictNaseleniya[4] = values[4]
#                     etrapDictNaseleniya[5] = values[5]
#             if country in turkmenistan:
#                 welayatTotalNaseleniya[0] += values[1] + values[2]
#                 welayatTotalNaseleniya[1] += values[3] + values[4]
#                 welayatTotalNaseleniya[2] += values[5]
#                 itogoTotalNaseleniya[0] += values[1] + values[2]
#                 itogoTotalNaseleniya[1] += values[3] + values[4]
#                 itogoTotalNaseleniya[2] += values[5]
#                 if 'Ahal' in country or 'Sotowyy' in country:
#                     if 'Ahal wel.' not in welayatDictNaseleniya:
#                         welayatDictNaseleniya['Ahal wel.'] = values
#                     else:
#                         # print('2222',values)
#                         welayatDictNaseleniya['Ahal wel.'][1] += values[1]
#                         welayatDictNaseleniya['Ahal wel.'][2] += values[2]
#                         welayatDictNaseleniya['Ahal wel.'][3] += values[3]
#                         welayatDictNaseleniya['Ahal wel.'][4] += values[4]
#                         welayatDictNaseleniya['Ahal wel.'][5] += values[5]
#                 if 'Ashgabat' in country:
#                     if 'Ashgabat s.' not in welayatDictNaseleniya:
#                         welayatDictNaseleniya['Ashgabat s.'] = values
#                     else:
#                         welayatDictNaseleniya['Ashgabat s.'][1] += values[1]
#                         welayatDictNaseleniya['Ashgabat s.'][2] += values[2]
#                         welayatDictNaseleniya['Ashgabat s.'][3] += values[3]
#                         welayatDictNaseleniya['Ashgabat s.'][4] += values[4]
#                         welayatDictNaseleniya['Ashgabat s.'][5] += values[5]
#                 if 'Mary' in country:
#                     if 'Mary wel.' not in welayatDictNaseleniya:
#                         welayatDictNaseleniya['Mary wel.'] = values
#                     else:
#                         welayatDictNaseleniya['Mary wel.'][1] += values[1]
#                         welayatDictNaseleniya['Mary wel.'][2] += values[2]
#                         welayatDictNaseleniya['Mary wel.'][3] += values[3]
#                         welayatDictNaseleniya['Mary wel.'][4] += values[4]
#                         welayatDictNaseleniya['Mary wel.'][5] += values[5]
#                 if 'Lebap' in country:
#                     if 'Lebap wel.' not in welayatDictNaseleniya:
#                         welayatDictNaseleniya['Lebap wel.'] = values
#                     else:
#                         welayatDictNaseleniya['Lebap wel.'][1] += values[1]
#                         welayatDictNaseleniya['Lebap wel.'][2] += values[2]
#                         welayatDictNaseleniya['Lebap wel.'][3] += values[3]
#                         welayatDictNaseleniya['Lebap wel.'][4] += values[4]
#                         welayatDictNaseleniya['Lebap wel.'][5] += values[5]
#                 if 'Balkan' in country:
#                     if 'Balkan wel.' not in welayatDictNaseleniya:
#                         welayatDictNaseleniya['Balkan wel.'] = values
#                     else:
#                         welayatDictNaseleniya['Balkan wel.'][1] += values[1]
#                         welayatDictNaseleniya['Balkan wel.'][2] += values[2]
#                         welayatDictNaseleniya['Balkan wel.'][3] += values[3]
#                         welayatDictNaseleniya['Balkan wel.'][4] += values[4]
#                         welayatDictNaseleniya['Balkan wel.'][5] += values[5]
#                 # if 'Sotowyy' in country:
#                 #     if 'Sotowyy' not in welayatDictNaseleniya:
#                 #         welayatDictNaseleniya['Sotowyy'] = values
#                 #     else:
#                 #         welayatDictNaseleniya['Sotowyy'][1] += values[1]
#                 #         welayatDictNaseleniya['Sotowyy'][2] += values[2]
#                 #         welayatDictNaseleniya['Sotowyy'][3] += values[3]
#                 #         welayatDictNaseleniya['Sotowyy'][4] += values[4]
#                 #         welayatDictNaseleniya['Sotowyy'][5] += values[5]
#                 # if country not in welayatDictNaseleniya:
#                 #     welayatDictNaseleniya[country] = values
#                 # else:
#                 #     welayatDictNaseleniya[2] = values[2]
#                 #     welayatDictNaseleniya[3] = values[3]
#                 #     welayatDictNaseleniya[4] = values[4]
#                 #     welayatDictNaseleniya[5] = values[5]
#                 #     welayatDictNaseleniya[6] = values[6]
            
#             if country in sng:
#                 sngTotalNaseleniya[0] += values[1] + values[2]
#                 sngTotalNaseleniya[1] += values[3] + values[4]
#                 sngTotalNaseleniya[2] += values[5]
#                 itogoTotalNaseleniya[0] += values[1] + values[2]
#                 itogoTotalNaseleniya[1] += values[3] + values[4]
#                 itogoTotalNaseleniya[2] += values[5]
#                 if country not in sngDictNaseleniya:
#                     sngDictNaseleniya[country] = values
#                 else:
#                     sngDictNaseleniya[2] = values[2]
#                     sngDictNaseleniya[3] = values[3]
#                     sngDictNaseleniya[4] = values[4]
#                     sngDictNaseleniya[5] = values[5]
#                     sngDictNaseleniya[6] = values[6]

#             if country in international:
#                 internationalTotalNaseleniya[0] += values[1] + values[2]
#                 internationalTotalNaseleniya[1] += values[3] + values[4]
#                 internationalTotalNaseleniya[2] += values[5]
#                 itogoTotalNaseleniya[0] += values[1] + values[2]
#                 itogoTotalNaseleniya[1] += values[3] + values[4]
#                 itogoTotalNaseleniya[2] += values[5]
#                 if country not in internationalDictNaseleniya:
#                     internationalDictNaseleniya[country] = values
#                 else:
#                     internationalDictNaseleniya[2] = values[2]
#                     internationalDictNaseleniya[3] = values[3]
#                     internationalDictNaseleniya[4] = values[4]
#                     internationalDictNaseleniya[5] = values[5]
#                     internationalDictNaseleniya[6] = values[6]

   
#         context['etrapDictNaseleniya'] = etrapDictNaseleniya
#         context['etrapTotalNaseleniya'] = etrapTotalNaseleniya

#         context['welayatDictNaseleniya'] = welayatDictNaseleniya
#         context['welayatTotalNaseleniya'] = welayatTotalNaseleniya

#         context['sngDictNaseleniya'] = sngDictNaseleniya
#         context['sngTotalNaseleniya'] = sngTotalNaseleniya

#         context['internationalDictNaseleniya'] = internationalDictNaseleniya
#         context['internationalTotalNaseleniya'] = internationalTotalNaseleniya

#         context['itogoTotalNaseleniya'] = itogoTotalNaseleniya


#         # для населения ############################################################################################
#         ##################################################################################################################
#         ##################################################################################################################


#         ##################################################################################################################
#         ##################################################################################################################
#         # для АТС ##############################################################################################
#         etrapDictATS = {} # {starna: [tarif, day_count, night_count, day_minut, night_minut, totalsum]}
#         etrapTotalATS = [0,0,0] # [totalConnect, totalMinut, totalPrice]

#         welayatDictATS = {}
#         welayatTotalATS = [0,0,0]

#         sngDictATS = {}
#         sngTotalATS = [0,0,0]

#         internationalDictATS = {}
#         internationalTotalATS = [0,0,0]

#         itogoTotalATS = [0,0,0]


#         for country, values in daysAndNightCallsATS.items():
#             if country in etraps:
#                 etrapTotalATS[0] += values[1] + values[2]
#                 etrapTotalATS[1] += values[3] + values[4]
#                 etrapTotalATS[2] += values[5]
#                 itogoTotalATS[0] += values[1] + values[2]
#                 itogoTotalATS[1] += values[3] + values[4]
#                 itogoTotalATS[2] += values[5]
#                 if country not in etrapDictATS:
#                     etrapDictATS[country] = values
#                 else:
#                     # print('test')
#                     etrapDictATS[1] = values[1]
#                     etrapDictATS[2] = values[1]
#                     etrapDictATS[3] = values[3]
#                     etrapDictATS[4] = values[4]
#                     etrapDictATS[5] = values[5]

#             if country in turkmenistan:
#                 welayatTotalATS[0] += values[1] + values[2]
#                 welayatTotalATS[1] += values[3] + values[4]
#                 welayatTotalATS[2] += values[5]
#                 itogoTotalATS[0] += values[1] + values[2]
#                 itogoTotalATS[1] += values[3] + values[4]
#                 itogoTotalATS[2] += values[5]
#                 if 'Ahal' in country or 'Sotowyy' in country:
#                     if 'Ahal wel.' not in welayatDictATS:
#                         welayatDictATS['Ahal wel.'] = values
#                     else:
#                         # print('2222',values)
#                         welayatDictATS['Ahal wel.'][1] += values[1]
#                         welayatDictATS['Ahal wel.'][2] += values[2]
#                         welayatDictATS['Ahal wel.'][3] += values[3]
#                         welayatDictATS['Ahal wel.'][4] += values[4]
#                         welayatDictATS['Ahal wel.'][5] += values[5]
#                 if 'Ashgabat' in country:
#                     if 'Ashgabat s.' not in welayatDictATS:
#                         welayatDictATS['Ashgabat s.'] = values
#                     else:
#                         welayatDictATS['Ashgabat s.'][1] += values[1]
#                         welayatDictATS['Ashgabat s.'][2] += values[2]
#                         welayatDictATS['Ashgabat s.'][3] += values[3]
#                         welayatDictATS['Ashgabat s.'][4] += values[4]
#                         welayatDictATS['Ashgabat s.'][5] += values[5]
#                 if 'Mary' in country:
#                     if 'Mary wel.' not in welayatDictATS:
#                         welayatDictATS['Mary wel.'] = values
#                     else:
#                         welayatDictATS['Mary wel.'][1] += values[1]
#                         welayatDictATS['Mary wel.'][2] += values[2]
#                         welayatDictATS['Mary wel.'][3] += values[3]
#                         welayatDictATS['Mary wel.'][4] += values[4]
#                         welayatDictATS['Mary wel.'][5] += values[5]
#                 if 'Lebap' in country:
#                     if 'Lebap wel.' not in welayatDictATS:
#                         welayatDictATS['Lebap wel.'] = values
#                     else:
#                         welayatDictATS['Lebap wel.'][1] += values[1]
#                         welayatDictATS['Lebap wel.'][2] += values[2]
#                         welayatDictATS['Lebap wel.'][3] += values[3]
#                         welayatDictATS['Lebap wel.'][4] += values[4]
#                         welayatDictATS['Lebap wel.'][5] += values[5]
#                 if 'Balkan' in country:
#                     if 'Balkan wel.' not in welayatDictATS:
#                         welayatDictATS['Balkan wel.'] = values
#                     else:
#                         welayatDictATS['Balkan wel.'][1] += values[1]
#                         welayatDictATS['Balkan wel.'][2] += values[2]
#                         welayatDictATS['Balkan wel.'][3] += values[3]
#                         welayatDictATS['Balkan wel.'][4] += values[4]
#                         welayatDictATS['Balkan wel.'][5] += values[5]
#                 # if 'Sotowyy' in country:
#                 #     if 'Sotowyy' not in welayatDictATS:
#                 #         welayatDictATS['Sotowyy'] = values
#                 #     else:
#                 #         welayatDictATS['Sotowyy'][1] += values[1]
#                 #         welayatDictATS['Sotowyy'][2] += values[2]
#                 #         welayatDictATS['Sotowyy'][3] += values[3]
#                 #         welayatDictATS['Sotowyy'][4] += values[4]
#                 #         welayatDictATS['Sotowyy'][5] += values[5]

#                 # if country not in welayatDictATS:
#                 #     welayatDictATS[country] = values
#                 # else:
#                 #     print('test2')
#                 #     welayatDictATS[2] = values[2]
#                 #     welayatDictATS[3] = values[3]
#                 #     welayatDictATS[4] = values[4]
#                 #     welayatDictATS[5] = values[5]
#                 #     welayatDictATS[6] = values[6]
            
#             if country in sng:
#                 sngTotalATS[0] += values[1] + values[2]
#                 sngTotalATS[1] += values[3] + values[4]
#                 sngTotalATS[2] += values[5]
#                 itogoTotalATS[0] += values[1] + values[2]
#                 itogoTotalATS[1] += values[3] + values[4]
#                 itogoTotalATS[2] += values[5]
#                 if country not in sngDictATS:
#                     sngDictATS[country] = values
#                 else:
#                     # print('test3')
#                     sngDictATS[2] = values[2]
#                     sngDictATS[3] = values[3]
#                     sngDictATS[4] = values[4]
#                     sngDictATS[5] = values[5]
#                     sngDictATS[6] = values[6]

#             if country in international:
#                 internationalTotalATS[0] += values[1] + values[2]
#                 internationalTotalATS[1] += values[3] + values[4]
#                 internationalTotalATS[2] += values[5]
#                 itogoTotalATS[0] += values[1] + values[2]
#                 itogoTotalATS[1] += values[3] + values[4]
#                 itogoTotalATS[2] += values[5]
#                 if country not in internationalDictATS:
#                     internationalDictATS[country] = values
#                 else:
#                     # print('test4')
#                     internationalDictATS[2] = values[2]
#                     internationalDictATS[3] = values[3]
#                     internationalDictATS[4] = values[4]
#                     internationalDictATS[5] = values[5]
#                     internationalDictATS[6] = values[6]
#         for k, v in welayatDictATS.items():
#             pass
#             # print(k,v)
   
#         context['etrapDictATS'] = etrapDictATS
#         context['etrapTotalATS'] = etrapTotalATS

#         context['welayatDictATS'] = welayatDictATS
#         context['welayatTotalATS'] = welayatTotalATS

#         context['sngDictATS'] = sngDictATS
#         context['sngTotalATS'] = sngTotalATS

#         context['internationalDictATS'] = internationalDictATS
#         context['internationalTotalATS'] = internationalTotalATS

#         context['itogoTotalATS'] = itogoTotalATS

#         messages.success(request, 'Трафик готов')

#         # для АТС ##############################################################################################
#         ##################################################################################################################
#         ##################################################################################################################


#         ##################################################################################################################
#         ##################################################################################################################
#         # для Неопознанные (unknown) #####################################################################################
#         etrapDictUnknownEdara = {} # {starna: [tarif, day_count, night_count, day_minut, night_minut, totalsum]}
#         etrapTotalUnknownEdara = [0,0,0] # [totalConnect, totalMinut, totalPrice]

#         welayatDictUnknownEdara = {}
#         welayatTotalUnknownEdara = [0,0,0]

#         sngDictUnknownEdara = {}
#         sngTotalUnknownEdara = [0,0,0]

#         internationalDictUnknownEdara = {}
#         internationalTotalUnknownEdara = [0,0,0]

#         itogoTotalUnknownEdara = [0,0,0]
#         # print('1111',daysAndNightUnknownEdara)

#         for country, values in daysAndNightUnknownEdara.items():
#             if country in etraps:
#                 etrapTotalUnknownEdara[0] += values[1] + values[2]
#                 etrapTotalUnknownEdara[1] += values[3] + values[4]
#                 etrapTotalUnknownEdara[2] += values[5]
#                 itogoTotalUnknownEdara[0] += values[1] + values[2]
#                 itogoTotalUnknownEdara[1] += values[3] + values[4]
#                 itogoTotalUnknownEdara[2] += values[5]

#                 if country not in etrapDictUnknownEdara:
#                     etrapDictUnknownEdara[country] = values
#                 else:
#                     etrapDictUnknownEdara[1] = values[1]
#                     etrapDictUnknownEdara[2] = values[1]
#                     etrapDictUnknownEdara[3] = values[3]
#                     etrapDictUnknownEdara[4] = values[4]
#                     etrapDictUnknownEdara[5] = values[5]

#             if country in turkmenistan:
#                 welayatTotalUnknownEdara[0] += values[1] + values[2]
#                 welayatTotalUnknownEdara[1] += values[3] + values[4]
#                 welayatTotalUnknownEdara[2] += values[5]
#                 itogoTotalUnknownEdara[0] += values[1] + values[2]
#                 itogoTotalUnknownEdara[1] += values[3] + values[4]
#                 itogoTotalUnknownEdara[2] += values[5]
#                 if 'Ahal' in country or 'Sotowyy' in country:
#                     if 'Ahal wel.' not in welayatDictUnknownEdara:
#                         welayatDictUnknownEdara['Ahal wel.'] = values
#                     else:
#                         welayatDictUnknownEdara['Ahal wel.'][1] += values[1]
#                         welayatDictUnknownEdara['Ahal wel.'][2] += values[2]
#                         welayatDictUnknownEdara['Ahal wel.'][3] += values[3]
#                         welayatDictUnknownEdara['Ahal wel.'][4] += values[4]
#                         welayatDictUnknownEdara['Ahal wel.'][5] += values[5]
#                 if 'Ashgabat' in country:
#                     if 'Ashgabat s.' not in welayatDictUnknownEdara:
#                         welayatDictUnknownEdara['Ashgabat s.'] = values
#                     else:
#                         welayatDictUnknownEdara['Ashgabat s.'][1] += values[1]
#                         welayatDictUnknownEdara['Ashgabat s.'][2] += values[2]
#                         welayatDictUnknownEdara['Ashgabat s.'][3] += values[3]
#                         welayatDictUnknownEdara['Ashgabat s.'][4] += values[4]
#                         welayatDictUnknownEdara['Ashgabat s.'][5] += values[5]
#                 if 'Mary' in country:
#                     if 'Mary wel.' not in welayatDictUnknownEdara:
#                         welayatDictUnknownEdara['Mary wel.'] = values
#                     else:
#                         welayatDictUnknownEdara['Mary wel.'][1] += values[1]
#                         welayatDictUnknownEdara['Mary wel.'][2] += values[2]
#                         welayatDictUnknownEdara['Mary wel.'][3] += values[3]
#                         welayatDictUnknownEdara['Mary wel.'][4] += values[4]
#                         welayatDictUnknownEdara['Mary wel.'][5] += values[5]
#                 if 'Lebap' in country:
#                     if 'Lebap wel.' not in welayatDictUnknownEdara:
#                         welayatDictUnknownEdara['Lebap wel.'] = values
#                     else:
#                         welayatDictUnknownEdara['Lebap wel.'][1] += values[1]
#                         welayatDictUnknownEdara['Lebap wel.'][2] += values[2]
#                         welayatDictUnknownEdara['Lebap wel.'][3] += values[3]
#                         welayatDictUnknownEdara['Lebap wel.'][4] += values[4]
#                         welayatDictUnknownEdara['Lebap wel.'][5] += values[5]
#                 if 'Balkan' in country:
#                     if 'Balkan wel.' not in welayatDictUnknownEdara:
#                         welayatDictUnknownEdara['Balkan wel.'] = values
#                     else:
#                         welayatDictUnknownEdara['Balkan wel.'][1] += values[1]
#                         welayatDictUnknownEdara['Balkan wel.'][2] += values[2]
#                         welayatDictUnknownEdara['Balkan wel.'][3] += values[3]
#                         welayatDictUnknownEdara['Balkan wel.'][4] += values[4]
#                         welayatDictUnknownEdara['Balkan wel.'][5] += values[5]
#                 # if 'Sotowyy' in country:
#                 #     if 'Sotowyy' not in welayatDictUnknownEdara:
#                 #         welayatDictUnknownEdara['Sotowyy'] = values
#                 #     else:
#                 #         welayatDictUnknownEdara['Sotowyy'][1] += values[1]
#                 #         welayatDictUnknownEdara['Sotowyy'][2] += values[2]
#                 #         welayatDictUnknownEdara['Sotowyy'][3] += values[3]
#                 #         welayatDictUnknownEdara['Sotowyy'][4] += values[4]
#                 #         welayatDictUnknownEdara['Sotowyy'][5] += values[5]
#                 # if country not in welayatDictBud:
#                 #     welayatDictBud[country] = values
#                 # else:
#                 #     welayatDictBud[2] = values[2]
#                 #     welayatDictBud[3] = values[3]
#                 #     welayatDictBud[4] = values[4]
#                 #     welayatDictBud[5] = values[5]
#                 #     welayatDictBud[6] = values[6]
            
#             if country in sng:
#                 sngTotalUnknownEdara[0] += values[1] + values[2]
#                 sngTotalUnknownEdara[1] += values[3] + values[4]
#                 sngTotalUnknownEdara[2] += values[5]
#                 itogoTotalUnknownEdara[0] += values[1] + values[2]
#                 itogoTotalUnknownEdara[1] += values[3] + values[4]
#                 itogoTotalUnknownEdara[2] += values[5]
#                 if country not in sngDictUnknownEdara:
#                     sngDictUnknownEdara[country] = values
#                 else:
#                     sngDictUnknownEdara[2] = values[2]
#                     sngDictUnknownEdara[3] = values[3]
#                     sngDictUnknownEdara[4] = values[4]
#                     sngDictUnknownEdara[5] = values[5]
#                     sngDictUnknownEdara[6] = values[6]

#             if country in international:
#                 internationalTotalUnknownEdara[0] += values[1] + values[2]
#                 internationalTotalUnknownEdara[1] += values[3] + values[4]
#                 internationalTotalUnknownEdara[2] += values[5]
#                 itogoTotalUnknownEdara[0] += values[1] + values[2]
#                 itogoTotalUnknownEdara[1] += values[3] + values[4]
#                 itogoTotalUnknownEdara[2] += values[5]
#                 if country not in internationalDictUnknownEdara:
#                     internationalDictUnknownEdara[country] = values
#                 else:
#                     internationalDictUnknownEdara[2] = values[2]
#                     internationalDictUnknownEdara[3] = values[3]
#                     internationalDictUnknownEdara[4] = values[4]
#                     internationalDictUnknownEdara[5] = values[5]
#                     internationalDictUnknownEdara[6] = values[6]

   
#         context['etrapDictUnknownEdara'] = etrapDictUnknownEdara
#         context['etrapTotalUnknownEdara'] = etrapTotalUnknownEdara

#         context['welayatDictUnknownEdara'] = welayatDictUnknownEdara
#         context['welayatTotalUnknownEdara'] = welayatTotalUnknownEdara

#         context['sngDictUnknownEdara'] = sngDictUnknownEdara
#         context['sngTotalUnknownEdara'] = sngTotalUnknownEdara

#         context['internationalDictUnknownEdara'] = internationalDictUnknownEdara
#         context['internationalTotalUnknownEdara'] = internationalTotalUnknownEdara

#         context['itogoTotalUnknownEdara'] = itogoTotalUnknownEdara


#         # для Неопознанные (unknown) #####################################################################################
#         ##################################################################################################################
#         ##################################################################################################################
        

#     # print('GGGGGGGGGGGGGG', test_price)
#     return render(request, 'telekom/MATB/otchyot/trafik.html', context)



