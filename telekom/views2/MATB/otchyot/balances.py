from django.shortcuts import render, redirect
from telekom.models import ImportInternetNachisleniyaON, LocalCall, ManagerNames, MonthPlatejiFromBilling, MonthPlatejiOFFFromBilling, NachMinus, NonLocalCall, OldLoginDogowor, PayHistory, PlatejiWhichAddKassirsEveryDay, UserTable
from django.db.models import Sum
from django.contrib import messages

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert
from django.db.models import Q
from datetime import date
from datetime import time
from datetime import datetime, timedelta
from calendar import monthrange
from django.http import HttpResponse
from django.contrib.auth.models import User
import tablib
import math

from django.db.models import F, IntegerField
from django.db.models.functions import Cast


def balances(request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    

    context = {}
    context['matbIndex'] = True
    context['balances'] = True

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['etraps'] = etraps
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']


    etrap = request.GET.get('etrap')
    year = request.GET.get('year')
    month_word = request.GET.get('month')
    month_digit = monthСonvert(month_word)

    

    context['etrap'] = etrap
    context['year'] = year
    context['month'] = month_word

    if etrap and year and month_word:
        month_digit = monthСonvert(month_word)
        days_in_choosed_month = monthrange(int(year), int(month_digit))[1]
        # Конвертировать строки в объект даты
        current_date = datetime.strptime(year + month_digit, '%Y%m')
        # Добавить один месяц
        next_month_date = current_date + timedelta(days=days_in_choosed_month)
        nextYear = next_month_date.year
        nextMonth = next_month_date.month
        print(f"{year}-{month_digit}-01")
        start = f"{year}-{month_digit}-01"
        start2 = f"{year}-{month_digit}-01 00:00:00"
        end=f"{nextYear}-{nextMonth}-01"
        end2=f"{year}-{month_digit}-{days_in_choosed_month}"

  
    
    if request.method == 'POST' and 'all_balance' in request.POST:
        # NEW_N	FAM	NAME	STREET	HOME	APT	P
        # users = UserTable.objects.filter(etrap=etrap)

        # users2 = UserTable.objects.annotate()
        users = UserTable.objects.annotate(
                number_as_int=Cast('number', IntegerField())
            ).filter(etrap=etrap).exclude(number_as_int__gte=100000).order_by('number')
        
        headers = ("NEW_N","FAM","NAME","STREET","HOME","APT","P", "Abon", "Int", "Alem", "Kabel")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)
        

        for u in users:
            surname = u.surname if u.surname != None else ''
            name = u.name if u.name != None else ''
            street = u.street if u.street != None else ''
            home = u.home if u.home != None else ''
            flat = u.flat if u.flat != None else ''
            hb = 'П' if u.hb else None
            b_telfon = u.b_telefon + u.b_slr + u.b_kod + u.b_zakaz + u.b_prochee + u.b_dop_uslugi
            b_internet = u.b_internet
            b_alem = u.b_alem
            b_kabel = u.b_kabel

            data.append((u.number, surname, name, street, home, flat, hb, b_telfon, b_internet, b_alem, b_kabel))
            
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {etrap}_balances_{year}-{month_digit}_.xlsx"

        return response





    return render(request, 'telekom/MATB/otchyot/balances.html', context)