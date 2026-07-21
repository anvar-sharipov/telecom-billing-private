# from django.dispatch import Signal
# import django.dispatch

from django.shortcuts import render
from telekom.forms import UserTableForm
from django.contrib import messages
from telekom.models import *
from tablib import Dataset
import re
from django.db.models.functions import Length
import tablib
from icecream import ic
from collections import Counter # Поиск дублирующихся строк

###
# для использования фильтра number__gte так как number строка, а не число 
from django.db.models import F, Value, Sum
from django.db.models.functions import Cast

from datetime import datetime, timedelta
from django.db.models import Q, Count
from collections import defaultdict
import math

from telekom.views2.myFunc.myFunc import getEtrapNameFromCode, is_Akdepe, is_Garashsyzlyk, is_Boldumsaz, is_Gubadag, is_Dzk

# import pandas as pd
from django.http import HttpResponse
####
import os

from django.db import transaction, IntegrityError
import logging
logger = logging.getLogger(__name__)







def HomePage(request):
    etraps =  ['Koneurgench', 'Turkmenbashy', 'Ruhubelent', 'S.A.Nyyazow', 'Gorogly', 'Boldumsaz', 'Akdepe', 'Dashoguz', 'Garashsyzlyk', 'Gubadag']
    wn_p = ['Dostluk Bank', 'E-government', 'Saray Tolegy', 'Tolleg APP TMCELL', 'Turkmen Pochta', "TM POST Dealers"]

    context = {} 
    # importDZdogowor


    if request.user.is_superuser and 'admin1' == request.user.username:
        print('this is original')

        # actiwnye polzowateli
        # users_to_deactivate = ["Abdyewa_Yakupjemal_Turkmenbashy", "Aramedowa_Oguljemal", "Atayewa_Shemshat_Turkmenbashy", "AyshatGoroglyMtb", "aziz", "AzizShabatMtb", "bagt", "BaharKoneurgenchKassa",
        #     "Baltabayewa_Sewara_MTB_DGE", "ejeshMB", "gayyp_uniwersal", "Gayypowa_Leyli_AHM", "GozelGubadagKassa", "GozelGubadagMtb", "GuljahanAkdepeKassa", "GuljahanAkdepeMB", "GuljahanAkdepeMtb", "hoz2", "Jumyazowa_Oguljemal", "KakamyratKoneurgenchMtb", 
        #     "KakamyratKoneurgenchUsluga", "Kurbanowa_Gulnabat_Koneurgench", "MahymAkdepeMtb", "Meredowa_Leyla", "mtbeva", "oraznazarowa_gozel", "Saryyewa_Gozel_Shabat_MTB", "tawushb", "Toylyyewa_Gurbangul", "Umyt_Kerimow"]
        # User.objects.filter(username__in=users_to_deactivate).update(is_active=False)

        # for u in UserTable.objects.filter(etrap="Boldumsaz"):
        #     if is_Gubadag(u.number):
        #         u.hb = None
        #         u.save()
        # for u in UserTable.objects.filter(etrap="Akdepe"):
        #     if is_Garashsyzlyk(u.number):
        #         u.hb = None
        #         u.save()

        # # activate - deactivate Akdepe and Boldumsaz groups User
        # off_groups = ["Akdepe_MTB", "Akdepe_Kassa", "Akdepe_MB",
        #       "Akdepe_071", "Akdepe_Internet", "Akdepe_SHB", "Boldumsaz_MTB", "Boldumsaz_Kassa", "Boldumsaz_MB",
        #       "Boldumsaz_071", "Boldumsaz_Internet", "Boldumsaz_SHB"]
        # User.objects.filter(groups__name__in=off_groups).update(is_active=False)
        # print("success deactivate users")

        # # add new etrap Garashsyzlyk and Gubadag
        # users = []
        # etrap_ranges = {
        #     "Garashsyzlyk": [
        #         (20000, 30000),
        #         (50000, 60000),
        #         (70000, 80000),
        #         (90000, 100000),
        #     ],
        #     "Gubadag": [
        #         (20000, 30000),
        #         (40000, 80000),
        #     ],
        # }
        # for etrap, ranges in etrap_ranges.items():
        #     print(etrap)
        #     for start, end in ranges:
        #         for i in range(start, end):   # end НЕ включительно
        #             users.append(UserTable(etrap=etrap, number=i))
        # UserTable.objects.bulk_create(users, batch_size=1000)

        # users = []
        # Garashsyzlyk_3_ranges = {
        #     "Garashsyzlyk": [
        #         (30000, 40000),
        #     ]
        # }  
        # for etrap, ranges in Garashsyzlyk_3_ranges.items():
        #     for start, end in ranges:
        #         for i in range(start, end):   # end НЕ включительно
        #             users.append(UserTable(etrap=etrap, number=i))
        # UserTable.objects.bulk_create(users, batch_size=1000)

        # users = []
        # for num in range(90000, 100000):
        #     users.append(UserTable(etrap="Gubadag", number=num))
        # UserTable.objects.bulk_create(users, batch_size=1000)

        # # activate - deactivate all ecxlude admin1 and Gayyp (deactivasiya wseh krome admin1 i Gayyp, Meredowa_Leyla, MahymAkdepeMtb, mahym)
        # akdepe_usernames = ["MahymAkdepeMtb", "GuljahanAkdepeKassa", "GuljahanAkdepeMtb", "mahym", "guljahan"]
        # garashsyzlyk_usernames = ["Baltabayewa_Sewara_MTB_DGE", "Merjen_Yylally_MTB", "MessaAkdepeMtb", "Kadyrowa_Guljemile_Akdepe", "Maysa_N_Yylally", "MessaAkdepeKassa", "NazikYylallyAbon-otdel", "HursantYylallyAbon-otdel", "NazikYylallyKassa", "HursantYylallyKassa", "HursantYylallyMtb"]
        # boldumsaz_usernames = ["SelbiBoldumsazAbon-otdel", "SelbiBoldumsazMtb", "SelbiBoldumsazKassa", "MayaBoldumsazMtb"]
        # gubadag_usernames = ["GozelGubadagKassa", "GozelGubadagMtb", "ShemshatGubadagAbon-otdel"]
        # exclude_usernames = ['admin1', 'Gayyp', 'lenashb', 'ejeshMB']
        # User.objects.all().exclude(username__in=exclude_usernames).update(is_active=False)

            #################################################################################################################################################################################
        #################################################################################################################################################################################
        #################################################################################################################################################################################
        ###### START gayyp oshibka (dwoynoe nachislenie), udaleniya dbf po file name, tak je otmena chach, balance kod i balance slr
        def getAnyBalance(etrap = ""):
            if etrap == "":
                totals = UserTable.objects.aggregate(
                    balance_telefon=Sum('b_telefon'),
                    balance_slr=Sum('b_slr'),
                    balance_kod=Sum('b_kod'),
                    balance_zakaz=Sum('b_zakaz'),
                    balance_prochee=Sum('b_prochee'),
                    balance_dop_uslugi=Sum('b_dop_uslugi'),
                    balance_internet=Sum('b_internet'),
                    balance_alem=Sum('b_alem'),
                )

            elif etrap in etraps:
                totals = UserTable.objects.filter(etrap=etrap).aggregate(
                    balance_telefon=Sum('b_telefon'),
                    balance_slr=Sum('b_slr'),
                    balance_kod=Sum('b_kod'),
                    balance_zakaz=Sum('b_zakaz'),
                    balance_prochee=Sum('b_prochee'),
                    balance_dop_uslugi=Sum('b_dop_uslugi'),
                    balance_internet=Sum('b_internet'),
                    balance_alem=Sum('b_alem'),
                )
            else:
                ic("choose correkt etrap")
                return
                
            balance_telefon = totals['balance_telefon'] or 0
            balance_slr = totals['balance_slr'] or 0
            balance_kod = totals['balance_kod'] or 0
            balance_zakaz = totals['balance_zakaz'] or 0
            balance_prochee = totals['balance_prochee'] or 0
            balance_dop_uslugi = totals['balance_dop_uslugi'] or 0
            balance_internet = totals['balance_internet'] or 0
            balance_alem = totals['balance_alem'] or 0
            
            if etrap in etraps:
                print(f"Balances for {etrap}")
            else:       
                print("Balancea for all")
            ic(balance_telefon)
            ic(balance_slr)
            ic(balance_kod)
            ic(balance_zakaz)
            ic(balance_prochee)
            ic(balance_dop_uslugi)
            ic(balance_internet)
            ic(balance_alem)
            
            
            
            print("balance telefoniya: ", balance_telefon + balance_slr + balance_kod + balance_zakaz + balance_prochee + balance_dop_uslugi)
            
            print()
            print()
              
        def getAnyNachs(year, month, etrap = ""):
            if not year or not month:
                ic("please set year and month")
                return
            if etrap == "":
                totals = NachMinus.objects.filter(year=year, month=month).aggregate(
                    telefon=Sum("telefon"),
                    slr=Sum("slr"),
                    kod=Sum("kod"),
                    zakaz=Sum("zakaz"),
                    prochee=Sum("prochee"),
                    dop_uslugi=Sum("dop_uslugi"),
                    internet=Sum("internet"),
                    alem=Sum("alem"),
                )
            elif etrap in etraps:
                totals = NachMinus.objects.filter(user__etrap=etrap, year=year, month=month).aggregate(
                    telefon=Sum("telefon"),
                    slr=Sum("slr"),
                    kod=Sum("kod"),
                    zakaz=Sum("zakaz"),
                    prochee=Sum("prochee"),
                    dop_uslugi=Sum("dop_uslugi"),
                    internet=Sum("internet"),
                    alem=Sum("alem"),
                )
            else:
                ic("please choose correct etrap")
            
            if etrap in etraps:
                print(f"nachs for {etrap} {year} {month}")
            else:       
                print(f"nahs for all {year} {month}")
            nach_telefon = totals["telefon"] or 0
            nach_slr = totals["slr"] or 0
            nach_kod = totals["kod"] or 0
            nach_zakaz = totals["zakaz"] or 0
            nach_prochee = totals["prochee"] or 0
            nach_dop_uslugi = totals["dop_uslugi"] or 0
            nach_internet = totals["internet"] or 0
            nach_alem = totals["alem"] or 0
            
            ic(nach_telefon)
            ic(nach_slr)
            ic(nach_kod)
            ic(nach_zakaz)
            ic(nach_prochee)
            ic(nach_dop_uslugi)
            ic(nach_internet)
            ic(nach_alem)
            print()
            print()
            
        
        # getAnyBalance("Gubadag")
        # getAnyNachs("2025", "12", "Gubadag")
        
        # getAnyBalance("Boldumsaz")
        # getAnyNachs("2025", "12", "Boldumsaz")
        
           
        # # udaleniya kod balance s UserTable i nach s NachMinus
        # calls = NonLocalCall.objects.filter(file_name__in=["01-04_12_2025hu"])      
        # count = 0
        # total_kod_price_Gubadag = 0
        # total_kod_price_Boldumsaz = 0
        # try:
        #     with transaction.atomic():
        #         for c in calls:
                    
                    
        #             number = c.SUB_A
        #             etrap = c.SUB_A_etrap
        #             price = c.total_price
                    
        #             # if etrap == "Gubadag":
        #             #     total_kod_price_Gubadag += c.total_price
        #             # elif etrap == "Boldumsaz":
        #             #     total_kod_price_Boldumsaz += c.total_price
                    
                    
        #             user = UserTable.objects.get(etrap=etrap, number=number)
        #             count += 1
        #             print(count)
        #             userNach = NachMinus.objects.get(user=user, year="2025", month="12")
                    
        #             # user.b_prochee += price
        #             # user.save()
        #             # userNach.kod -= price
        #             # userNach.save()
        # except Exception as e:
        #     print(f'Откат! ошибка с transaction == {e}')
            
        # # ic(total_kod_price_Gubadag)
        # # ic(total_kod_price_Boldumsaz)
        
        
        
        
        # # udaleniya slr balance s UserTable i nach s NachMinus
        # PRICE_PER_MINUTE = 0.0006
        # FREE_MINUTES_PER_DAY = 5
        # def calculate_local_call_prices(file_name):
        #     calls = LocalCall.objects.filter(file_name__in=file_name)

        #     # etrap -> number -> date -> minutes
        #     usage = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))

        #     for call in calls:
        #         try:
        #             minutes = float(call.MT)
        #         except (ValueError, TypeError):
        #             continue

        #         usage[call.etrap][call.SUB_A][call.DATE] += minutes

        #     # Результаты
        #     result = {}
        #     etrap_totals = defaultdict(float)

        #     for etrap, numbers in usage.items():
        #         result[etrap] = {}

        #         for number, days in numbers.items():
        #             total_cost = 0.0

        #             for date, total_minutes in days.items():
        #                 billable_minutes = max(
        #                     0,
        #                     math.ceil(total_minutes - FREE_MINUTES_PER_DAY)
        #                 )
        #                 total_cost += billable_minutes * PRICE_PER_MINUTE

        #             result[etrap][number] = round(total_cost, 6)
        #             etrap_totals[etrap] += total_cost

        #     # округлим итоги
        #     etrap_totals = {
        #         k: round(v, 6) for k, v in etrap_totals.items()
        #     }

        #     return result, etrap_totals
        
        
        # numbers_prices, etrap_prices = calculate_local_call_prices(
        #     ["01-04_12_2025hu"]
        # )

        # try:
        #     with transaction.atomic():
        #         for etrap, numbers in numbers_prices.items():
        #             print(f"\n📍 Etrap: {etrap}")
        #             for number, price in numbers.items():
        #                 if price > 0:
        #                     user = UserTable.objects.get(etrap=etrap, number=number)
        #                     nach = NachMinus.objects.get(user=user, year="2025", month="12")
        #                     # user.b_slr += price
        #                     # nach.slr -= price
        #                     # user.save()
        #                     # nach.save()
        #                     print(number, "=>", price)
                
        # except Exception as e:
        #     print(f'Откат! ошибка с transaction == {e}')

        # print("\n💰 Итоги по этрапам:")
        # for etrap, total in etrap_prices.items():
        #     print(etrap, "=>", total)



        # # udaleniya samih files
        # LocalCall.objects.filter(file_name__in=["01-04_12_2025hu"]).delete()
        # NonLocalCall.objects.filter(file_name__in=["01-04_12_2025hu"]).delete()
        
        # # udaleniya file s dbfNameList
        # dbfNameList.objects.filter(name__in=["01-04_12_2025hu"]).delete()

        ###### END gayyp oshibka (dwoynoe nachislenie), udaleniya dbf po file name, tak je otmena chach, balance kod i balance slr
        #################################################################################################################################################################################
        #################################################################################################################################################################################
        ############################################################################

        # nachs = ImportInternetNachisleniyaON.objects.filter(year="2026", month="Май", etrap="Dashoguz")
        # nachs2 = ImportInternetNachisleniyaOFF.objects.filter(year="2026", month="Май", etrap="Dashoguz")
        # ic(len(nachs))
        # ic(len(nachs2))



        
        

  

    

    return render(request, 'telekom/HomePage/HomePage.html', context)