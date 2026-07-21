# Код с transaction и с некоторыми улучшениями
from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.models import AbonentService, DontRepeatYourself, NachMinus, NachisleniyaOtchet, StaffAction, UserTable
from django.db.models import Sum

from datetime import date

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert

from django.db import transaction

import logging

logger = logging.getLogger(__name__)


def dop_uslugiNachisleniya(request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    context = {}
    context['matbIndex'] = True
    context['dop_uslugiNachisleniya'] = True

    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date

    # log = getLoggedUserEtrap(request.user.username)
    context['log'] = log
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    context['etraps'] = etraps

    context['etrap'] = request.GET.get('etrap')
    context['get_month'] = request.GET.get('month')
    context['get_year'] = request.GET.get('year')


    month_word = request.GET.get('month')
    year = request.GET.get('year')
    month_numb = monthСonvert(month_word)
    etrap = request.GET.get('etrap')

    if month_word == '':
        messages.error(request, f'Ошибка! Выберите месяц начисления')
        return redirect('dop-uslugi-nachisleniya')

    users = UserTable.objects.filter(etrap=etrap, snyat_bool=False).exclude(service=None) 
    if users:
        context['lenSuccesCount'] = len(users)
        context['totalSum'] = users.aggregate(Sum('service__price'))['service__price__sum']
    
    try:
        DontRepeatYourself.objects.get(dopUslugiNachisleniyaYearMonthEtrap=f"{year}{month_word}{etrap}")
        context['alreadyNach'] = True
    except:
        pass
    

    if request.method == 'POST':
        if request.POST.get('comment') == '':
            messages.error(request, f'Ошибка! Комментарий не может быть пустым')     
        else:
    
            try:
                DontRepeatYourself.objects.get(dopUslugiNachisleniyaYearMonthEtrap=f"{year}{month_word}{etrap}")
                messages.error(request, f'Месяц {month_word} {year} года этрап {etrap} уже начислено')
                return render(request, 'telekom/MATB/dop_uslugiNachisleniya.html', context)
            except:
                pass

            nachMinus = NachMinus.objects.select_related("user").filter(month=month_numb, year=year, user__etrap=etrap)
            dict_nachs = {}
            for n in nachMinus:
                num = int(n.user.number)
                if num in dict_nachs:
                    messages.error(request, f"Есть дубликаты в NachMinus {num}")
                    return redirect('dop-uslugi-nachisleniya')
                dict_nachs[num] = n
            
            bulk_update_user = []
            bulk_update_nach = []
            bulk_create_nach = []

            for u in users:
                price = 0
                num = int(u.number)
                added = {'added': [[]]}
                index = 0
                for s in u.service.all():
                    price += s.price
                    added['added'][0].append(str(s.pk))
                added['added'][0].append('Начисление')
                added['added'][0].append(price)
                u.b_dop_uslugi -= price
                bulk_update_user.append(u)

                nach = dict_nachs.get(num)
                if nach:
                    nach.dop_uslugi += price
                    nach.dop_usligi_added_Pk=str(added)
                    bulk_update_nach.append(nach)
                else:
                    nach = NachMinus(user=u, year=year, month=month_numb, dop_uslugi=price, dop_usligi_added_Pk=str(added))
                    bulk_create_nach.append(nach)
            try:
                with transaction.atomic():
                    if bulk_update_nach or bulk_update_user or bulk_create_nach:
                        if bulk_update_user:
                            UserTable.objects.bulk_update(bulk_update_user, ['b_dop_uslugi'])
                        if bulk_update_nach:
                            NachMinus.objects.bulk_update(bulk_update_nach, ['dop_uslugi', 'dop_usligi_added_Pk'])
                        if bulk_create_nach:
                            NachMinus.objects.bulk_create(bulk_create_nach)

                        DontRepeatYourself.objects.create(dopUslugiNachisleniyaYearMonthEtrap=f"{year}{month_word}{etrap}")
                        StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')}\n\n Начисления Доп Услуг за {month_word} {year} года этрап {etrap}", action='Начисления Доп Услуг')
                        context['alreadyNach'] = True
                        UserTable.objects.filter(is_enterprises=True).update(b_telefon=0, b_slr=0, b_kod=0, b_zakaz=0, b_prochee=0, b_dop_uslugi=0, b_internet=0, b_alem=0)
                        messages.success(request, f'Успешное начисление за месяц {month_word} {year} года, этрап {etrap}')
            except Exception as e:
                messages.error(request, f'ошибка с transaction == {e}')
                logger.error(f'ошибка с transaction == {e}')


    return render(request, 'telekom/MATB/dop_uslugiNachisleniya.html', context)
    





































# Код работает но без Transaction

# from django.shortcuts import render, redirect
# from django.contrib import messages
# from telekom.models import AbonentService, DontRepeatYourself, NachMinus, NachisleniyaOtchet, StaffAction, UserTable
# from django.db.models import Sum

# from datetime import date

# from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert


# def dop_uslugiNachisleniya(request):
#     if not request.user.is_superuser and not request.user.username == 'admin1':
#         messages.error(request, f'Нет доступа')
#         return redirect('user-login')
        
#     EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
#     if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
#         log = EtrapAndGroup[0]
#     else:
#         messages.error(request, f'Доступ только соотрудникам MATB')
#         return redirect('user-login')
    
#     context = {}
#     context['matbIndex'] = True
#     context['dop_uslugiNachisleniya'] = True

#     current_date = date.today()
#     current_date = str(current_date)
#     context['current_date'] = current_date

#     # log = getLoggedUserEtrap(request.user.username)
#     context['log'] = log
#     context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
#     context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']
#     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
#     context['etraps'] = etraps

#     context['etrap'] = request.GET.get('etrap')
#     context['get_month'] = request.GET.get('month')
#     context['get_year'] = request.GET.get('year')


#     month_word = request.GET.get('month')
#     year = request.GET.get('year')
#     month_numb = monthСonvert(month_word)
#     etrap = request.GET.get('etrap')

#     if month_word == '':
#         messages.error(request, f'Ошибка! Выберите месяц начисления')
#         return redirect('dop-uslugi-nachisleniya')
    
#     if etrap in etraps:
#         users = UserTable.objects.filter(etrap=etrap, snyat_bool=False).exclude(service=None)
#     elif etrap == 'all':
#         users = UserTable.objects.filter().exclude(service=None)
        
#     else:
#         users = False

#     nachMinus = NachMinus.objects.filter(month=month_numb, year=year)
    
    

#     list_items = []

#     if users:
#         context['lenSuccesCount'] = len(users)
#         context['totalSum'] = users.aggregate(Sum('service__price'))['service__price__sum']

#     # Если нажал на начислить
#     if request.method == 'POST':
#         if request.POST.get('comment') == '':
#             messages.error(request, f'Ошибка! Комментарий не может быть пустым')     
#         else:

#             if etrap in etraps:
#                 try:
#                     DontRepeatYourself.objects.get(dopUslugiNachisleniyaYearMonthEtrap=f"{year}{month_word}all")
#                     messages.error(request, f'Месяц {month_word} {year} года этрап {etrap} уже начислено')
#                     return render(request, 'telekom/MATB/dop_uslugiNachisleniya.html', context)
#                 except:
#                     pass
#                 try:
#                     DontRepeatYourself.objects.get(dopUslugiNachisleniyaYearMonthEtrap=f"{year}{month_word}{etrap}")
#                     messages.error(request, f'Месяц {month_word} {year} года этрап {etrap} уже начислено')
#                     return render(request, 'telekom/MATB/dop_uslugiNachisleniya.html', context)
#                 except:
#                     pass
#             elif etrap == 'all':
#                 etr_already_nach = []
#                 for e in etraps:
#                     try:
#                         DontRepeatYourself.objects.get(dopUslugiNachisleniyaYearMonthEtrap=f"{year}{month_word}{e}")
#                         etr_already_nach.append(e)
#                     except:
#                         pass
#                 if etr_already_nach:
#                     messages.error(request, f'Вы не можете начислить На все этрапы, {month_word} {year} года некоторые этрапы уже начислены {etr_already_nach}')
#                     return render(request, 'telekom/MATB/dop_uslugiNachisleniya.html', context)

#             testTotalCount = 0
#             testTotalPrice = 0
#             total_price = 0
#             for user in users:
#                 testTotalCount += 1
#                 print('Начислено абонентов',testTotalCount)
#                 try:
#                     n = nachMinus.get(user=user, month=month_numb, year=year) 
#                     have_nach = True
#                 except:
#                     have_nach = False

#                 services = user.service.all()
#                 price = 0
#                 new_pk = []
#                 for service in services:
#                     price += service.price
#                     total_price += service.price
#                     new_pk.append(str(service.pk))

#                 new_pk.append('Начисление')
#                 new_pk.append(price)
                
#                 if have_nach:
#                     n.dop_uslugi += price

#                     if n.dop_usligi_added_Pk:
#                         added = eval(n.dop_usligi_added_Pk)
#                     else:
#                         added = {'added': []}
        
#                     added['added'].append(new_pk) 
#                     n.dop_usligi_added_Pk = str(added)
#                     n.save()

#                 else:
#                     added = {'added': []}
#                     added['added'].append(new_pk) 

#                     list_items.append([user, year, month_numb, price, str(added)])
                
#                 user.b_dop_uslugi -= price
#                 testTotalPrice += price
#                 user.save()

#                 # Код для сохранения начисления для отчета по месяцам если etrap == 'all'
#                 if etrap == 'all':
#                     try:
#                         nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=user.etrap, year=year, month=month_word) 
#                         nachisleniyaOtchet.serviceNachisleniya += price
#                         nachisleniyaOtchet.save()
#                     except:
#                         NachisleniyaOtchet.objects.create(etrap=user.etrap, year=year, month=month_word, serviceNachisleniya=price) 
                

#             if list_items:
#                 aux = []
#                 for item in list_items:
#                     obj = NachMinus(user=item[0], year=item[1], month=item[2], dop_uslugi=item[3], dop_usligi_added_Pk=item[4])
#                     aux.append(obj)

#                 NachMinus.objects.bulk_create(aux)
            


#             DontRepeatYourself.objects.create(dopUslugiNachisleniyaYearMonthEtrap=f"{year}{month_word}{etrap}")
#             StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')}\n\n Начисления Доп Услуг за {month_word} {year} года этрап {etrap}", action='Начисления Доп Услуг')
#             messages.success(request, f'Успешное начисление за месяц {month_word} {year} года, этрап {etrap}, количесво начислений: {len(users)} на сумму: {total_price}')
#             print('Всего абонентов', testTotalCount)
#             print('Общая цена ', testTotalPrice)

#             # Код для сохранения начисления для отчета по месяцам если etrap != 'all'
#             if etrap in etraps:
#                 try:
#                     nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=etrap, year=year, month=month_word) 
#                     nachisleniyaOtchet.serviceNachisleniya += total_price
#                     nachisleniyaOtchet.save()
#                 except:
#                     NachisleniyaOtchet.objects.create(etrap=etrap, year=year, month=month_word, serviceNachisleniya=total_price) 
            

#     return render(request, 'telekom/MATB/dop_uslugiNachisleniya.html', context)
    