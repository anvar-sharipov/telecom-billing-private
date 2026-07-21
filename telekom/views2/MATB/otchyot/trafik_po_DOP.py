from django.shortcuts import render, redirect
from telekom.models import LocalCall, NonLocalCall, UserTable, Zakaz
from django.db.models import Sum
from django.contrib import messages

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert
from django.db.models import Q
from datetime import date
from datetime import time
from datetime import datetime, timedelta
from calendar import monthrange


def trafik_po_DOP(request):

    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    
    
    context = {}
    context['matbIndex'] = True
    context['trafik_dop'] = True
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
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
                
      

        calls = Zakaz.objects.filter(DATE__range=[f"{year}-{month_digit}-01", f"{nextYear}-{nextMonth}-01"], action='заказ подтвержден', etrap=etrap)
        test = 0
        for i in calls:
            test += float(i.total_price)

        print('total_price', test)
        print('all calls', len(calls))

        all_users = UserTable.objects.filter(etrap=etrap)

        users = all_users.filter(is_enterprises = True, hb__name='B')
        numbersBud = []
        for i in users:
            numbersBud.append(int(i.number))

        users = all_users.filter(is_enterprises = True, hb__name='H')
        numbersHoz = []
        for i in users:
            if i.account != ATSSALDO:
                numbersHoz.append(int(i.number))

        users = all_users.filter(account=ATSSALDO)
        nubersATS = []
        for i in users:
            nubersATS.append(int(i.number))
            
        users = all_users.filter(is_enterprises=False)
        nubersNaseleniye = []
        for i in users:
            nubersNaseleniye.append(int(i.number))

        users = all_users.filter(is_enterprises=True, hb=None)
        nubersUnknown = []
        for i in users:
            nubersUnknown.append(int(i.number))

        calls_day = calls.filter(DATE__hour__gt='6', DATE__hour__lte='22')
        calls_night = calls.filter(Q(DATE__hour__gt='22', DATE__hour__lte='23') | Q(DATE__hour__gte='00', DATE__hour__lte='06'))

        daysAndNightCallsBud = {} # {starna: [tarif, day_count, night_count, day_minut, night_minut, totalsum]}
        daysAndNightCallsHoz = {}
        daysAndNightCallsATS = {}
        daysAndNightCallsNaseleniya = {}
        daysAndNightUnknownEdara = {}

        daysCallCount = 0
        nightCallCount = 0
        # class Zakaz(models.Model):
        # DATE = models.DateTimeField(verbose_name='Дата и время звонка ')
        # NUMBER_A = models.CharField(max_length=32, verbose_name='NUMBER_A')
        # NUMBER_B = models.CharField(max_length=32, verbose_name='NUMBER_B')
        # NUMBER_LOCATIONS = models.CharField(max_length=32, verbose_name='Страна/Город соединяемой стороны')
        # etrap = models.CharField(max_length=32, choices= etraps, verbose_name='Этрап соединяющей стороны')
        # DUR = models.CharField(max_length=16, verbose_name='DUR')
        # MT = models.CharField(max_length=8, verbose_name='MT')
        # price = models.CharField(max_length=8, verbose_name='цена за минуту без процента')
        # total_price = models.CharField(max_length=16, verbose_name='Общая цена с процентом')
        # CALL_TYPE = models.CharField(max_length=4, verbose_name='CALL_TYPE')
        # action = models.CharField(max_length=32, choices= zakazCallType, verbose_name='бно/повторно/потдвержден')
        # agent_id = models.CharField(max_length=4, verbose_name='agent_id', blank=True)
        # День
        for c in calls_day:
            daysCallCount += 1
            # print('Дневных звонков',daysCallCount)
            # для бюд
            if int(c.NUMBER_A) in numbersBud:
                price= float(c.price)
                total_price = float(c.total_price)
                location = c.NUMBER_LOCATIONS
                MT = int(c.MT)

                if location not in daysAndNightCallsBud:
                    daysAndNightCallsBud[location] = [price, 1, 0, MT, 0, total_price]
                else:
                    daysAndNightCallsBud[location][1] += 1
                    daysAndNightCallsBud[location][3] += MT
                    daysAndNightCallsBud[location][5] += total_price
            # для хоз
            elif int(c.NUMBER_A) in numbersHoz:
                price= float(c.price)
                total_price = float(c.total_price)
                location = c.NUMBER_LOCATIONS
                MT = int(c.MT)

                if location not in daysAndNightCallsHoz:
                    daysAndNightCallsHoz[location] = [price, 1, 0, MT, 0, total_price]
                else:
                    daysAndNightCallsHoz[location][1] += 1
                    daysAndNightCallsHoz[location][3] += MT
                    daysAndNightCallsHoz[location][5] += total_price
            # для АТС
            elif int(c.NUMBER_A) in nubersATS:
                price= float(c.price)
                total_price = float(c.total_price)
                location = c.NUMBER_LOCATIONS
                MT = int(c.MT)
                if location not in daysAndNightCallsATS:
                    daysAndNightCallsATS[location] = [price, 1, 0, MT, 0, total_price]
                else:
                    daysAndNightCallsATS[location][1] += 1
                    daysAndNightCallsATS[location][3] += MT
                    daysAndNightCallsATS[location][5] += total_price
            # для Населения
            elif int(c.NUMBER_A) in nubersNaseleniye:
                price= float(c.price)
                total_price = float(c.total_price)
                location = c.NUMBER_LOCATIONS
                MT = int(c.MT)

                if location not in daysAndNightCallsNaseleniya:
                    daysAndNightCallsNaseleniya[location] = [price, 1, 0, MT, 0, total_price]
                else:
                    daysAndNightCallsNaseleniya[location][1] += 1
                    daysAndNightCallsNaseleniya[location][3] += MT
                    daysAndNightCallsNaseleniya[location][5] += total_price
            # для Неопознанных (Unknown)
            elif int(c.NUMBER_A) in nubersUnknown:
                price= float(c.price)
                total_price = float(c.total_price)
                location = c.NUMBER_LOCATIONS
                MT = int(c.MT)

                if location not in daysAndNightUnknownEdara:
                    daysAndNightUnknownEdara[location] = [price, 1, 0, MT, 0, total_price]
                else:
                    daysAndNightUnknownEdara[location][1] += 1
                    daysAndNightUnknownEdara[location][3] += MT
                    daysAndNightUnknownEdara[location][5] += total_price
        # Ночь
        for c in calls_night:
            nightCallCount += 1
            # print('Ночных звонков', nightCallCount)
            # для бюд
            if int(c.NUMBER_A) in numbersBud:
                price= float(c.price)
                total_price = float(c.total_price)
                location = c.NUMBER_LOCATIONS
                MT = int(c.MT)

                if location not in daysAndNightCallsBud:
                    daysAndNightCallsBud[location] = [price, 0, 1, 0, MT, total_price]
                else:
                    daysAndNightCallsBud[location][2] += 1
                    daysAndNightCallsBud[location][4] += MT
                    daysAndNightCallsBud[location][5] += total_price
            # для хоз
            elif int(c.NUMBER_A) in numbersHoz:
                price= float(c.price)
                total_price = float(c.total_price)
                location = c.NUMBER_LOCATIONS
                MT = int(c.MT)

                if location not in daysAndNightCallsHoz:
                    daysAndNightCallsHoz[location] = [price, 0, 1, 0, MT, total_price]
                else:
                    daysAndNightCallsHoz[location][2] += 1
                    daysAndNightCallsHoz[location][4] += MT
                    daysAndNightCallsHoz[location][5] += total_price
            # для АТС
            elif int(c.NUMBER_A) in nubersATS:
                price= float(c.price)
                total_price = float(c.total_price)
                location = c.NUMBER_LOCATIONS
                MT = int(c.MT)

                if location not in daysAndNightCallsATS:
                    daysAndNightCallsATS[location] = [price, 0, 1, 0, MT, total_price]
                else:
                    daysAndNightCallsATS[location][2] += 1
                    daysAndNightCallsATS[location][4] += MT
                    daysAndNightCallsATS[location][5] += total_price
            # для Населения
            elif int(c.NUMBER_A) in nubersNaseleniye:
                price= float(c.price)
                total_price = float(c.total_price)
                location = c.NUMBER_LOCATIONS
                MT = int(c.MT)

                if location not in daysAndNightCallsNaseleniya:
                    daysAndNightCallsNaseleniya[location] = [price, 0, 1, 0, MT, total_price]
                else:
                    daysAndNightCallsNaseleniya[location][2] += 1
                    daysAndNightCallsNaseleniya[location][4] += MT
                    daysAndNightCallsNaseleniya[location][5] += total_price
            # для Неопознанных (Unknown)
            elif int(c.NUMBER_A) in nubersUnknown:
                price= float(c.price)
                total_price = float(c.total_price)
                location = c.NUMBER_LOCATIONS
                MT = int(c.MT)

                if location not in daysAndNightUnknownEdara:
                    daysAndNightUnknownEdara[location] = [price, 0, 1, 0, MT, total_price]
                else:
                    daysAndNightUnknownEdara[location][2] += 1
                    daysAndNightUnknownEdara[location][4] += MT
                    daysAndNightUnknownEdara[location][5] += total_price
            
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
                if 'Ahal' in country:
                    if 'Ahal wel.' not in welayatDictBud:
                        welayatDictBud['Ahal wel.'] = values
                    else:
                        welayatDictBud['Ahal wel.'][1] += values[1]
                        welayatDictBud['Ahal wel.'][2] += values[2]
                        welayatDictBud['Ahal wel.'][3] += values[3]
                        welayatDictBud['Ahal wel.'][4] += values[4]
                        welayatDictBud['Ahal wel.'][5] += values[5]
                if 'Ashgabat' in country:
                    if 'Ashgabat wel.' not in welayatDictBud:
                        welayatDictBud['Ashgabat wel.'] = values
                    else:
                        welayatDictBud['Ashgabat wel.'][1] += values[1]
                        welayatDictBud['Ashgabat wel.'][2] += values[2]
                        welayatDictBud['Ashgabat wel.'][3] += values[3]
                        welayatDictBud['Ashgabat wel.'][4] += values[4]
                        welayatDictBud['Ashgabat wel.'][5] += values[5]
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
                if 'Sotowyy' in country:
                    if 'Sotowyy' not in welayatDictBud:
                        welayatDictBud['Sotowyy'] = values
                    else:
                        welayatDictBud['Sotowyy'][1] += values[1]
                        welayatDictBud['Sotowyy'][2] += values[2]
                        welayatDictBud['Sotowyy'][3] += values[3]
                        welayatDictBud['Sotowyy'][4] += values[4]
                        welayatDictBud['Sotowyy'][5] += values[5]
            
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
                if 'Ahal' in country:
                    if 'Ahal wel.' not in welayatDictHoz:
                        welayatDictHoz['Ahal wel.'] = values
                    else:
                        print('2222',values)
                        welayatDictHoz['Ahal wel.'][1] += values[1]
                        welayatDictHoz['Ahal wel.'][2] += values[2]
                        welayatDictHoz['Ahal wel.'][3] += values[3]
                        welayatDictHoz['Ahal wel.'][4] += values[4]
                        welayatDictHoz['Ahal wel.'][5] += values[5]
                if 'Ashgabat' in country:
                    if 'Ashgabat wel.' not in welayatDictHoz:
                        welayatDictHoz['Ashgabat wel.'] = values
                    else:
                        welayatDictHoz['Ashgabat wel.'][1] += values[1]
                        welayatDictHoz['Ashgabat wel.'][2] += values[2]
                        welayatDictHoz['Ashgabat wel.'][3] += values[3]
                        welayatDictHoz['Ashgabat wel.'][4] += values[4]
                        welayatDictHoz['Ashgabat wel.'][5] += values[5]
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
                if 'Sotowyy' in country:
                    if 'Sotowyy' not in welayatDictHoz:
                        welayatDictHoz['Sotowyy'] = values
                    else:
                        welayatDictHoz['Sotowyy'][1] += values[1]
                        welayatDictHoz['Sotowyy'][2] += values[2]
                        welayatDictHoz['Sotowyy'][3] += values[3]
                        welayatDictHoz['Sotowyy'][4] += values[4]
                        welayatDictHoz['Sotowyy'][5] += values[5]
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
                if 'Ahal' in country:
                    if 'Ahal wel.' not in welayatDictNaseleniya:
                        welayatDictNaseleniya['Ahal wel.'] = values
                    else:
                        print('2222',values)
                        welayatDictNaseleniya['Ahal wel.'][1] += values[1]
                        welayatDictNaseleniya['Ahal wel.'][2] += values[2]
                        welayatDictNaseleniya['Ahal wel.'][3] += values[3]
                        welayatDictNaseleniya['Ahal wel.'][4] += values[4]
                        welayatDictNaseleniya['Ahal wel.'][5] += values[5]
                if 'Ashgabat' in country:
                    if 'Ashgabat wel.' not in welayatDictNaseleniya:
                        welayatDictNaseleniya['Ashgabat wel.'] = values
                    else:
                        welayatDictNaseleniya['Ashgabat wel.'][1] += values[1]
                        welayatDictNaseleniya['Ashgabat wel.'][2] += values[2]
                        welayatDictNaseleniya['Ashgabat wel.'][3] += values[3]
                        welayatDictNaseleniya['Ashgabat wel.'][4] += values[4]
                        welayatDictNaseleniya['Ashgabat wel.'][5] += values[5]
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
                if 'Sotowyy' in country:
                    if 'Sotowyy' not in welayatDictNaseleniya:
                        welayatDictNaseleniya['Sotowyy'] = values
                    else:
                        welayatDictNaseleniya['Sotowyy'][1] += values[1]
                        welayatDictNaseleniya['Sotowyy'][2] += values[2]
                        welayatDictNaseleniya['Sotowyy'][3] += values[3]
                        welayatDictNaseleniya['Sotowyy'][4] += values[4]
                        welayatDictNaseleniya['Sotowyy'][5] += values[5]
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
                    print('test')
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
                if 'Ahal' in country:
                    if 'Ahal wel.' not in welayatDictATS:
                        welayatDictATS['Ahal wel.'] = values
                    else:
                        print('2222',values)
                        welayatDictATS['Ahal wel.'][1] += values[1]
                        welayatDictATS['Ahal wel.'][2] += values[2]
                        welayatDictATS['Ahal wel.'][3] += values[3]
                        welayatDictATS['Ahal wel.'][4] += values[4]
                        welayatDictATS['Ahal wel.'][5] += values[5]
                if 'Ashgabat' in country:
                    if 'Ashgabat wel.' not in welayatDictATS:
                        welayatDictATS['Ashgabat wel.'] = values
                    else:
                        welayatDictATS['Ashgabat wel.'][1] += values[1]
                        welayatDictATS['Ashgabat wel.'][2] += values[2]
                        welayatDictATS['Ashgabat wel.'][3] += values[3]
                        welayatDictATS['Ashgabat wel.'][4] += values[4]
                        welayatDictATS['Ashgabat wel.'][5] += values[5]
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
                if 'Sotowyy' in country:
                    if 'Sotowyy' not in welayatDictATS:
                        welayatDictATS['Sotowyy'] = values
                    else:
                        welayatDictATS['Sotowyy'][1] += values[1]
                        welayatDictATS['Sotowyy'][2] += values[2]
                        welayatDictATS['Sotowyy'][3] += values[3]
                        welayatDictATS['Sotowyy'][4] += values[4]
                        welayatDictATS['Sotowyy'][5] += values[5]

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
                    print('test3')
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
                    print('test4')
                    internationalDictATS[2] = values[2]
                    internationalDictATS[3] = values[3]
                    internationalDictATS[4] = values[4]
                    internationalDictATS[5] = values[5]
                    internationalDictATS[6] = values[6]
        for k, v in welayatDictATS.items():
            print(k,v)
   
        context['etrapDictATS'] = etrapDictATS
        context['etrapTotalATS'] = etrapTotalATS

        context['welayatDictATS'] = welayatDictATS
        context['welayatTotalATS'] = welayatTotalATS

        context['sngDictATS'] = sngDictATS
        context['sngTotalATS'] = sngTotalATS

        context['internationalDictATS'] = internationalDictATS
        context['internationalTotalATS'] = internationalTotalATS

        context['itogoTotalATS'] = itogoTotalATS

        messages.success(request, 'Трафик по ДОП готово')

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
        print('1111',daysAndNightUnknownEdara)

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
                if 'Ahal' in country:
                    if 'Ahal wel.' not in welayatDictUnknownEdara:
                        welayatDictUnknownEdara['Ahal wel.'] = values
                    else:
                        welayatDictUnknownEdara['Ahal wel.'][1] += values[1]
                        welayatDictUnknownEdara['Ahal wel.'][2] += values[2]
                        welayatDictUnknownEdara['Ahal wel.'][3] += values[3]
                        welayatDictUnknownEdara['Ahal wel.'][4] += values[4]
                        welayatDictUnknownEdara['Ahal wel.'][5] += values[5]
                if 'Ashgabat' in country:
                    if 'Ashgabat wel.' not in welayatDictUnknownEdara:
                        welayatDictUnknownEdara['Ashgabat wel.'] = values
                    else:
                        welayatDictUnknownEdara['Ashgabat wel.'][1] += values[1]
                        welayatDictUnknownEdara['Ashgabat wel.'][2] += values[2]
                        welayatDictUnknownEdara['Ashgabat wel.'][3] += values[3]
                        welayatDictUnknownEdara['Ashgabat wel.'][4] += values[4]
                        welayatDictUnknownEdara['Ashgabat wel.'][5] += values[5]
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
                if 'Sotowyy' in country:
                    if 'Sotowyy' not in welayatDictUnknownEdara:
                        welayatDictUnknownEdara['Sotowyy'] = values
                    else:
                        welayatDictUnknownEdara['Sotowyy'][1] += values[1]
                        welayatDictUnknownEdara['Sotowyy'][2] += values[2]
                        welayatDictUnknownEdara['Sotowyy'][3] += values[3]
                        welayatDictUnknownEdara['Sotowyy'][4] += values[4]
                        welayatDictUnknownEdara['Sotowyy'][5] += values[5]
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
   

    return render(request, 'telekom/MATB/otchyot/trafik_po_DOP.html', context)