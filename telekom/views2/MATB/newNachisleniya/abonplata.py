from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from datetime import datetime
from telekom.models import *
from telekom.views2.myFunc.myFunc import monthСonvert
from django.db import transaction

import logging

logger = logging.getLogger(__name__)


def newAbonplataNachisleniya(request):
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']

    request_user = request.user
    groups = request_user.groups.all()
    request_user_etrap = ''
    request_user_type = ''
    for g in groups:
        request_user_etrap, request_user_type = g.name.split('_')
        if request_user_type == 'MTB':# or request.user.username == 'admin1':
            break

    if request_user_type != 'MTB' and (not request.user.is_superuser and request.user.username != 'admin1'):
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')

    context = {}
    current_date = datetime.now().date()
    formatted_date = current_date.strftime('%Y-%m-%d')
    current_year, current_month, current_day = formatted_date.split('-')

    context['formatted_date'] = formatted_date
    context['current_year'] = current_year
    context['current_month'] = current_month
    context['current_day'] = current_day
    context['etraps'] = etraps
    context['newAbonplataNachisleniya'] = True

    etrap = request.GET.get('etrap')
    year = request.GET.get('year')
    month = request.GET.get('month')
    comment = request.GET.get('comment')

    context['selected_etrap'] = etrap
    context['year'] = year
    context['month'] = month
    ic(month)
    context['comment'] = comment

    if etrap and year and month:
        ic('tut')
        users = UserTable.objects.filter(etrap=etrap, snyat_bool=False, abonplata__gt=0)

        price_info_dict_edara = {}
        price_info_dict_ilat = {}

        total_edara_count = 0
        total_ilat_count = 0
        total_edara_price = 0
        total_ilat_price = 0
        umumy_count = 0
        umumy_price = 0
        for user in users:
            abonplata = float(user.abonplata.replace(',', '.')) if ',' in user.abonplata else float(user.abonplata)
            umumy_count += 1
            umumy_price += abonplata

            
            if user.is_enterprises:
                total_edara_count += 1
                total_edara_price += abonplata
                if abonplata in price_info_dict_edara:
                    price_info_dict_edara[abonplata][0] += 1
                    price_info_dict_edara[abonplata][1] += abonplata
                else:
                    price_info_dict_edara[abonplata] = [1, abonplata]

            else:
                total_ilat_count += 1
                total_ilat_price += abonplata
                if abonplata in price_info_dict_ilat:
                    price_info_dict_ilat[abonplata][0] += 1
                    price_info_dict_ilat[abonplata][1] += abonplata
                else:
                    price_info_dict_ilat[abonplata] = [1, abonplata]

            
        context['price_info_dict_ilat'] = price_info_dict_ilat
        context['price_info_dict_edara'] = price_info_dict_edara

        context['total_edara_count'] = total_edara_count
        context['total_ilat_count'] = total_ilat_count
        context['total_edara_price'] = total_edara_price
        context['total_ilat_price'] = total_ilat_price
        context['umumy_count'] = umumy_count
        context['umumy_price'] = umumy_price


        try:
            DontRepeatYourself.objects.get(abonplataNachisleniaYearMonthEtrap=f"{year}{monthСonvert(month)}{etrap}")
            context['alreadyNachs'] = True
        except:
            pass

        



        if request.method == 'POST':
        
            bulk_update_users = []
            bulk_update_nach_minus = []
            bulk_create_nach_minus = []

            nachMinus = NachMinus.objects.filter(user__etrap=etrap, year=year, month=month)
            dict_ = {}
            for n in nachMinus:
                dict_[int(n.user.number)] = n
         
            for user in users:
                abonplata = float(user.abonplata.replace(',', '.')) if ',' in user.abonplata else float(user.abonplata)
                number = int(user.number)
                
                is_enterprises = False
                hb = ''
                if user.hb:
                    hb = user.hb.name
                if user.is_enterprises:
                    is_enterprises = True
                if number in dict_:
                    user_nach = dict_[number]
                    user_nach.telefon += abonplata
                    user_nach.is_enterprises = is_enterprises
                    user_nach.hb = hb
                    bulk_update_nach_minus.append(dict_[number])
                else:
                    
                    
                    # Создание нового объекта NachMinus, если его нет
                    new_nach_minus = NachMinus(
                        user=user,
                        year=year,
                        month=month,
                        is_enterprises = is_enterprises, 
                        hb=hb,
                        telefon=abonplata  # Установка начального значения телефона
                    )
                    bulk_create_nach_minus.append(new_nach_minus) 
                
                user.b_telefon -= abonplata
                bulk_update_users.append(user)
            try:
                with transaction.atomic():
                    if bulk_update_users:
                        UserTable.objects.bulk_update(bulk_update_users, ['b_telefon'])
                    if bulk_update_nach_minus:
                        NachMinus.objects.bulk_update(bulk_update_nach_minus, ['telefon', 'is_enterprises', 'hb'])
                    if bulk_create_nach_minus:
                        NachMinus.objects.bulk_create(bulk_create_nach_minus)
                    
                    if bulk_update_users or bulk_update_nach_minus or bulk_create_nach_minus:
                        StaffAction.objects.create(user=request.user, comment=f"Начисления абонплаты new за месяц {monthСonvert(month)} {year} года Этрапа {etrap}", action='Начисления абонплата')
                        DontRepeatYourself.objects.create(abonplataNachisleniaYearMonthEtrap=f"{year}{monthСonvert(month)}{etrap}")
                        messages.success(request, f"Успешное начисление абонплата {year} {monthСonvert(month)} {etrap}")
                        UserTable.objects.filter(is_enterprises=True).update(b_telefon=0, b_slr=0, b_kod=0, b_zakaz=0, b_prochee=0, b_dop_uslugi=0, b_internet=0, b_alem=0)
                        context['alreadyNachs'] = True
            except Exception as e:
                messages.error(request, f'ошибка с transaction == {e}')
                logger.error(f'ошибка с transaction == {e}')
          

       

    return render(request, 'telekom/MATB/newNachisleniya/abonplata.html', context)