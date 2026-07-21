from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.models import DontRepeatYourself, NachMinus, NachisleniyaOtchet, StaffAction, UserTable, KabelTvNew, KabelNach

from datetime import date, datetime
from calendar import monthrange
# Для минуса месяцев с даты
from dateutil.relativedelta import relativedelta

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert
from collections import defaultdict
from icecream import ic

from django.db import transaction

import logging

logger = logging.getLogger(__name__)




def kabelTvNachisleniya(request):

    if not request.user.is_superuser and request.user.username != 'admin1' and request.user.username != 'Gayyp':
        messages.error(request, f'Доступ только для администратора')
        return redirect('user-login')

    
    context = {}
    context['matbIndex'] = True
    context['kabelTvNachisleniya'] = True
 
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['etraps'] = etraps

    

    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date
    current_year = current_date[0:4]
    context['current_year'] = current_year
    current_month = current_date[5:7]
    current_day = current_date[8:]

    context['etrap'] = request.GET.get('etrap') if request.GET.get('etrap') != None else ''
    context['get_month'] = request.GET.get('month') if request.GET.get('month') != None else monthСonvert(current_month)
    context['get_year'] = request.GET.get('year') if request.GET.get('year') != None else ''

    days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]



    month_word = request.GET.get('month') if request.GET.get('month') != None else monthСonvert(current_month)
    year = request.GET.get('year') if request.GET.get('year') != None else current_year
    month_numb = monthСonvert(month_word)
    etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else ''

    if month_word and year and etrap:
        print(month_word, month_numb, year, etrap)

        try:
            DontRepeatYourself.objects.get(KabelNachisleniaYearMonthEtrap=f"{year}{month_word}{etrap}")
            context['alreadyNach'] = True
            # messages.error(request, f'Месяц {month_word} {year} года этрап {etrap} уже начислено')
        except:
            pass

        users = KabelTvNew.objects.filter(is_active=True, is_enterprises=False)
       

        price_mapping = {
            1: 10, 2: 15, 3: 20, 4: 25, 5: 30, 6: 35, 7: 40, 8: 45, 9: 50, 10: 55,
            11: 60, 12: 65, 13: 70, 14: 75, 15: 80, 16: 85, 17: 90, 18: 95, 19: 100, 20: 105,
            21: 110, 22: 115, 23: 120, 24: 125, 25: 130, 26: 135, 27: 140, 28: 145, 29: 150, 30: 155,
            31: 160, 32: 165, 33: 170, 34: 175, 35: 180, 36: 185, 37: 190, 38: 195, 39: 200, 40: 205,
            41: 210, 42: 215, 43: 220, 44: 225, 45: 230, 46: 235, 47: 240, 48: 245, 49: 250, 50: 255
        }
        dict_ = defaultdict(lambda: {'count': 0, 'price': 0})

        for u in users:
            if u.count in price_mapping:
                dict_[u.count]['count'] += 1
                dict_[u.count]['price'] += price_mapping[u.count]

        
        context['dict_'] = dict(sorted(dict_.items(), key=lambda item: item[1]['count'], reverse=True))

        users_edara = KabelTvNew.objects.filter(is_active=True, is_enterprises=True)
        price_mapping_edara = {
            1: 10, 2: 15, 3: 20, 4: 25, 5: 30, 6: 35, 7: 40, 8: 45, 9: 50, 10: 55,
            11: 60, 12: 65, 13: 70, 14: 75, 15: 80, 16: 85, 17: 90, 18: 95, 19: 100, 20: 105,
            21: 110, 22: 115, 23: 120, 24: 125, 25: 130, 26: 135, 27: 140, 28: 145, 29: 150, 30: 155,
            31: 160, 32: 165, 33: 170, 34: 175, 35: 180, 36: 185, 37: 190, 38: 195, 39: 200, 40: 205,
            41: 210, 42: 215, 43: 220, 44: 225, 45: 230, 46: 235, 47: 240, 48: 245, 49: 250, 50: 255
        }
        dict_edara = defaultdict(lambda: {'count': 0, 'price': 0})
        for u in users_edara:
            if u.count in price_mapping_edara:
                dict_edara[u.count]['count'] += 1
                dict_edara[u.count]['price'] += price_mapping_edara[u.count]

        context['dict_edara'] = dict(sorted(dict_edara.items(), key=lambda item: item[1]['count'], reverse=True))


       

    # Если нажал на начисления  
    testTotalCount = 0
    testTotalPrice = 0
    if request.method == 'POST':
        nachs = KabelNach.objects.select_related("user").filter(year=year, month=month_numb)
        dict_nachs = {}
        for n in nachs:
            num = n.user.number
            if num in dict_nachs:
                messages.error(request, f"Есть дубликат в KabelNach, {num}")
            else:
                dict_nachs[num] = n

        bulk_update_user = []
        bulk_update_nach = []
        bulk_create_nach = []

        users = KabelTvNew.objects.filter(is_active=True)
        get_price = {
            1: 10, 2: 15, 3: 20, 4: 25, 5: 30, 6: 35, 7: 40, 8: 45, 9: 50, 10: 55,
            11: 60, 12: 65, 13: 70, 14: 75, 15: 80, 16: 85, 17: 90, 18: 95, 19: 100, 20: 105,
            21: 110, 22: 115, 23: 120, 24: 125, 25: 130, 26: 135, 27: 140, 28: 145, 29: 150, 30: 155,
            31: 160, 32: 165, 33: 170, 34: 175, 35: 180, 36: 185, 37: 190, 38: 195, 39: 200, 40: 205,
            41: 210, 42: 215, 43: 220, 44: 225, 45: 230, 46: 235, 47: 240, 48: 245, 49: 250, 50: 255
        }
        for u in users:
            num = u.number
            price = get_price[u.count]
            u.balance -= price
            bulk_update_user.append(u)
        #    

            nach = dict_nachs.get(num)

            if nach:
                nach.nach += price
                bulk_update_nach.append(nach)
            else:
                nach = KabelNach(user=u, year=year, month=month_numb, nach=price)
                bulk_create_nach.append(nach)

 
        try:
            with transaction.atomic():
                if bulk_update_user or bulk_update_nach or bulk_create_nach:
                    if bulk_update_user:
                        KabelTvNew.objects.bulk_update(bulk_update_user, ['balance'])
                    if bulk_update_nach:
                        KabelNach.objects.bulk_update(bulk_update_nach, ['nach'])
                    if bulk_create_nach:
                        KabelNach.objects.bulk_create(bulk_create_nach)
                    
                    StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')} \n\n\n Начисления кабель TV за {month_word} {year} года, этрап {etrap}", action='Кабель TV действия')
                    DontRepeatYourself.objects.create(KabelNachisleniaYearMonthEtrap=f"{year}{month_word}{etrap}")
                    context['alreadyNach'] = True
                    messages.success(request, f'Успешное Начисления Kabel TV')  
        except Exception as e:
                messages.error(request, f'ошибка с transaction == {e}')
                logger.error(f'ошибка с transaction == {e}')
    

    
        



    return render(request, 'telekom/MATB/kabelTvNachisleniya.html', context)
