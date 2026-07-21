# Transaction + некоторые улучшения
from django.shortcuts import render, redirect
from telekom.models import DontRepeatYourself, NachMinus, NachisleniyaOtchet, StaffAction, UserTable, Zakaz
from django.db.models import Sum, F, Q
from django.db.models.functions import Cast
from django.db.models import DecimalField
from django.contrib import messages

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert
from datetime import date
from calendar import monthrange

from django.db import transaction
import logging
logger = logging.getLogger(__name__)


def zakazNachisleniya(request):

    if not ((request.user.is_superuser and request.user.username == 'admin1') or request.user.username == 'Gayyp'):
        messages.error(request, f'У вас нет доступа')
        return redirect('user-login')
    
    context = {}
    context['matbIndex'] = True
    context['zakazNachisleniya'] = True

    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']


    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date
    current_year = current_date[0:4]
    context['current_year'] = current_year
    current_month = current_date[5:7]
    current_day = current_date[8:]
   
    context['get_year'] = request.GET.get('year') if request.GET.get('year') != None else ''

    days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]

    month_word = request.GET.get('month') if request.GET.get('month') != None else monthСonvert(current_month)
    year = request.GET.get('year') if request.GET.get('year') != None else current_year
    month_numb = monthСonvert(month_word)
    etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else ''

    context['etrap'] = etrap
    context['get_month'] = month_word

    if month_word and year and etrap:
        days_in_nach_month = str(monthrange(int(year), int(month_numb))[1])
        start = f'{year}-{month_numb}-01 00:00:00'
        end = f'{year}-{month_numb}-{str(days_in_nach_month)} 23:59:59'
        
       
        zakazCalls = Zakaz.objects.filter(DATE__range=[start, end], action='заказ подтвержден', etrap=etrap)
        users = UserTable.objects.filter(etrap=etrap)
        dict_users = {}
        for u in users:
            num = int(u.number)
            if num not in dict_users:
                dict_users[num] = u
            

        didntHaveUser = 0
        success_total_price = 0

        for call in zakazCalls:
            num = int(call.NUMBER_A)
            user = dict_users.get(num)
            if user:
                success_total_price += float(call.total_price)
            else:
                didntHaveUser += 1

        context['didntHaveUser'] = didntHaveUser
        context['success_total_price'] = success_total_price

        try:
            DontRepeatYourself.objects.get(zakazNachisleniaYearMonthEtrap=f"{year}{month_word}{etrap}")
            already_nach = True
        except:
            already_nach = False
        context['already_nach'] = already_nach

        context['ZakazCalls'] = zakazCalls
        context['lenZakazCalls'] = len(zakazCalls)


        # context['totalSumProc'] =  zakazCalls.aggregate(Sum('total_price'))['total_price__sum']
        zakazCalls = zakazCalls.filter(
            Q(total_price__regex=r'^\d+\.?\d*$') | Q(total_price__isnull=True)
        )
        # Затем безопасно агрегируем
        try:
            context['totalSumProc'] = zakazCalls.annotate(
                numeric_price=Cast(
                    F('total_price'),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                )
            ).aggregate(
                sum_result=Sum('numeric_price')
            )['sum_result'] or 0  # or 0 для замены None на 0
        except Exception as e:
            messages.error(request, f"Ошибка при расчете суммы: {e}")
            context['totalSumProc'] = 0
        


    testTotalCount = 0
    testTotalPrice = 0

    if request.method == 'POST':
        if request.POST.get('comment') == '':
            messages.error(request, f"Ошибка! Оставьте комментарий")
        else:
        
            try:
                DontRepeatYourself.objects.get(zakazNachisleniaYearMonthEtrap=f"{year}{month_word}{etrap}")
                mes = f"Ошибка! Этрап {etrap} уже начислен"
                already_have = True
            except:
                already_have = False

            if already_have == False:

                    
           
                nachMinus = NachMinus.objects.select_related("user").filter(year=year, month=month_numb, user__etrap=etrap)

                dict_nachs = {}
                for n in nachMinus:
                    num = int(n.user.number)
                    if num in dict_nachs:
                        messages.error(request, f"Ошибка! Есть дубликаты в NachMinus {year}-{month_numb} {num}")
                        return render(request, 'telekom/MATB/zakazNachisleniya.html', context)
                    else:
                        dict_nachs[num] = n
                
                bulk_update_user_dict = {}
                bulk_update_nach_dict = {}
                bulk_create_nach_dict = {}
            
                for call in zakazCalls:
                    price = float(call.total_price)
                    num = int(call.NUMBER_A)
                    testTotalCount += 1
                    testTotalPrice += price
                    
                    user = dict_users.get(num)
                    if not user:
                        messages.error(request, f"Ошибка! Не найден пользователь с номером {num}")
                        return render(request, 'telekom/MATB/zakazNachisleniya.html', context)

                    if num not in bulk_update_user_dict:
                        user.b_zakaz -= price
                        bulk_update_user_dict[num] = user
                    else:
                        user = bulk_update_user_dict[num]
                        user.b_zakaz -= price

                    if num in bulk_update_nach_dict:
                        nach = bulk_update_nach_dict[num]
                        nach.zakaz += price
                    elif num in bulk_create_nach_dict:
                        nach = bulk_create_nach_dict[num]
                        nach.zakaz += price
                    else:
                        nach = dict_nachs.get(num)
                        if nach:
                            nach.zakaz += price
                            bulk_update_nach_dict[num] = nach
                        else:
                            nach = NachMinus(user=user, year=year, month=month_numb)
                            nach.zakaz += price
                            bulk_create_nach_dict[num] = nach
               
                if bulk_update_user_dict or bulk_update_nach_dict or bulk_create_nach_dict:
                    try:
                        with transaction.atomic():
                            if bulk_update_user_dict:
                                bulk_update_user = []
                                for num, obj in bulk_update_user_dict.items():
                                    bulk_update_user.append(obj) 
                                UserTable.objects.bulk_update(bulk_update_user, ['b_zakaz'])
                            if bulk_update_nach_dict:
                                bulk_update_nach = []
                                for num, obj in bulk_update_nach_dict.items():
                                    bulk_update_nach.append(obj)
                                NachMinus.objects.bulk_update(bulk_update_nach, ['zakaz'])

                            if bulk_create_nach_dict:
                                bulk_create_nach = []
                                for num, obj in bulk_create_nach_dict.items():
                                    bulk_create_nach.append(obj) 
                                NachMinus.objects.bulk_create(bulk_create_nach)
            
                        
                            StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')} \n\n\n Начисления заказ за {month_word} {year} года, этрап {etrap}", action='Начисления заказ')
                            DontRepeatYourself.objects.create(zakazNachisleniaYearMonthEtrap=f"{year}{month_word}{etrap}")   
                            logger.info(f'==== Количество Начислений {testTotalCount}')
                            logger.info(f'==== Сумма Начислений {testTotalPrice}')
                            context['already_nach'] = True
                            UserTable.objects.filter(is_enterprises=True).update(b_telefon=0, b_slr=0, b_kod=0, b_zakaz=0, b_prochee=0, b_dop_uslugi=0, b_internet=0, b_alem=0)
                            messages.success(request, f'Успешное Начисления Заказ, {month_word} {year}')  
                    except Exception as e:
                        messages.error(request, f'(откат сохранений) ошибка с transaction == {e}')
                        logger.error(f'==== (откат сохранений) ошибка с transaction == {e}')
                else:
                    messages.error(request, f'Нечего сохранять')
            
            else:
                messages.error(request, mes)
                    

            
    return render(request, 'telekom/MATB/zakazNachisleniya.html', context)






















# Работает но без transaction и нет некоторые улучшения
# from django.shortcuts import render, redirect
# from telekom.models import DontRepeatYourself, NachMinus, NachisleniyaOtchet, StaffAction, UserTable, Zakaz
# from django.db.models import Sum
# from django.contrib import messages

# from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert
# from datetime import date
# from calendar import monthrange


# def zakazNachisleniya(request):

#     EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
#     if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
#         log = EtrapAndGroup[0]
#     else:
#         messages.error(request, f'Доступ только соотрудникам MATB')
#         return redirect('user-login')
    
#     context = {}
#     context['matbIndex'] = True
#     context['zakazNachisleniya'] = True

#     # log = getLoggedUserEtrap(request.user.username)
#     context['log'] = log
#     context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
#     context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']
#     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
#     context['etraps'] = etraps


#     current_date = date.today()
#     current_date = str(current_date)
#     context['current_date'] = current_date
#     current_year = current_date[0:4]
#     context['current_year'] = current_year
#     current_month = current_date[5:7]
#     current_day = current_date[8:]

#     context['etrap'] = request.GET.get('etrap') if request.GET.get('etrap') != None else ''
#     context['get_month'] = request.GET.get('month') if request.GET.get('month') != None else monthСonvert(current_month)
#     context['get_year'] = request.GET.get('year') if request.GET.get('year') != None else ''

#     days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]

#     month_word = request.GET.get('month') if request.GET.get('month') != None else monthСonvert(current_month)
#     year = request.GET.get('year') if request.GET.get('year') != None else current_year
#     month_numb = monthСonvert(month_word)
#     etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else ''

#     if month_word and year and etrap:
#         days_in_nach_month = str(monthrange(int(year), int(month_numb))[1])
#         start = f'{year}-{month_numb}-01 00:00:00'
#         end = f'{year}-{month_numb}-{str(days_in_nach_month)} 23:59:59'
        
#         if etrap in etraps:
#             zakazCalls = Zakaz.objects.filter(DATE__range=[start, end], action='заказ подтвержден', etrap=etrap)
#             users = UserTable.objects.filter(etrap=etrap)
#         elif etrap == 'all':
#             zakazCalls = Zakaz.objects.filter(DATE__range=[start, end], action='заказ подтвержден')
#             users = UserTable.objects.all()


#         # Проверяем есть ли абоненты не найденные в БД
#         didntHaveUser = 0
#         success_total_price = 0
#         for call in zakazCalls:
#             try:
#                 users.get(number=call.NUMBER_A, etrap=call.etrap)
#                 success_total_price += float(call.total_price)
#             except:
#                 didntHaveUser += 1

#         context['didntHaveUser'] = didntHaveUser
#         context['success_total_price'] = success_total_price

#         try:
#             DontRepeatYourself.objects.get(zakazNachisleniaYearMonthEtrap=f"{year}{month_word}{etrap}")
#             already_nach = True
#         except:
#             already_nach = False
#         context['already_nach'] = already_nach







        

#         context['ZakazCalls'] = zakazCalls
        
#         context['lenZakazCalls'] = len(zakazCalls)

#         context['totalSumProc'] =  zakazCalls.aggregate(Sum('total_price'))['total_price__sum']
#         # context['totalSumProc'] =  zakazCalls.aggregate(Sum('total_priceProc'))['total_priceProc__sum']

#     testTotalCount = 0
#     testTotalPrice = 0
#     # Если нажал на начислить
#     if request.method == 'POST':
#         if request.POST.get('comment') == '':
#             messages.error(request, f"Ошибка! Оставьте комментарий")
#         else:
#             if etrap == 'all':
#                 try:
#                     DontRepeatYourself.objects.get(zakazNachisleniaYearMonthEtrap=f"{year}{month_word}all")
#                     mes = f"Ошибка! Все этрапы уже былы начислены"
#                     already_have = True
#                 except:
#                     try:
#                         DontRepeatYourself.objects.get(zakazNachisleniaYearMonthEtrap__icontains=f"{year}{month_word}")
#                         mes = f"Ошибка! Вы не можете начислить на все этрапы, так-как некоторые этрапы уже были начислены"
#                         already_have = True
#                     except:
#                         already_have = False
#             elif etrap in etraps:
#                 try:
#                     DontRepeatYourself.objects.get(zakazNachisleniaYearMonthEtrap=f"{year}{month_word}all")
#                     mes = f"Ошибка! Вы не можете начислить на этрап {etrap}, так-как все этрапы уже былы начислены"
#                     already_have = True
#                 except:
#                     try:
#                         DontRepeatYourself.objects.get(zakazNachisleniaYearMonthEtrap=f"{year}{month_word}{etrap}")
#                         mes = f"Ошибка! Этрап {etrap} уже начислен"
#                         already_have = True
#                     except:
#                         already_have = False

#             if already_have == False:

                    
#                 if etrap == 'all':
#                     nachMinus = NachMinus.objects.filter(year=year, month=month_numb)
#                 elif etrap in etraps:
#                     nachMinus = NachMinus.objects.filter(year=year, month=month_numb, user__etrap=etrap)

                
                
#                 if etrap in etraps:
#                     try:
#                         nachisleniyaOtchet = NachisleniyaOtchet.objects.get(year=year, month=month_word, etrap=etrap)
#                     except:
#                         nachisleniyaOtchet = NachisleniyaOtchet.objects.create(year=year, month=month_word, etrap=etrap)
#                     for call in zakazCalls:
#                         testTotalCount += 1
#                         testTotalPrice += float(call.total_price)
#                         print('Успешных начислений', testTotalCount)
#                         try:
#                             user = users.get(number=call.NUMBER_A)
#                         except:
#                             continue
#                         user.b_zakaz -= float(call.total_price)

#                         try:
#                             nach = nachMinus.get(user=user, year=year, month=month_numb)
#                         except:
#                             nach = nachMinus.create(user=user, year=year, month=month_numb)
                        
#                         nach.zakaz += float(call.total_price)
#                         nach.save()

#                         nachisleniyaOtchet.zakazNachisleniya += float(call.total_price)
#                         user.save()

#                     nachisleniyaOtchet.save()
                
                
                
#                 # elif etrap == 'all':

#                 #     total_nach = 0
#                 #     nach_dz = 0
#                 #     nach_ak = 0
#                 #     nach_bol = 0
#                 #     nach_gor = 0
#                 #     nach_kone = 0
#                 #     nach_turk = 0
#                 #     nach_nyyaz = 0
#                 #     nach_ruh = 0

#                 #     for call in zakazCalls:
#                 #         try:
#                 #             user = users.get(number=call.NUMBER_A, etrap=call.etrap)
#                 #         except:
#                 #             continue
#                 #         user.b_zakaz -= float(call.total_priceProc)

#                 #         try:
#                 #             nach = nachMinus.get(user=user, year=year, month=month_numb)
#                 #         except:
#                 #             nach = nachMinus.create(user=user, year=year, month=month_numb)
                        
#                 #         nach.zakaz += float(call.total_priceProc)
#                 #         nach.save()

#                 #         if user.etrap == 'Dashoguz':
#                 #             nach_dz += float(call.total_priceProc)
#                 #         if user.etrap == 'Akdepe':
#                 #             nach_ak += float(call.total_priceProc)
#                 #         if user.etrap == 'Boldumsaz':
#                 #             nach_bol += float(call.total_priceProc)
#                 #         if user.etrap == 'Gorogly':
#                 #             nach_gor += float(call.total_priceProc)
#                 #         if user.etrap == 'Koneurgench':
#                 #             nach_kone += float(call.total_priceProc)
#                 #         if user.etrap == 'Turkmenbashy':
#                 #             nach_turk += float(call.total_priceProc)
#                 #         if user.etrap == 'S.A.Nyyazow':
#                 #             nach_nyyaz += float(call.total_priceProc)
#                 #         if user.etrap == 'Ruhubelent':
#                 #             nach_ruh += float(call.total_priceProc)

#                 #         user.save()
#                 #     try:
#                 #         nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap='Dashoguz', month=month_word, year=year)
#                 #         nachisleniyaOtchet.alemNachisleniya+=nach_dz
#                 #         nachisleniyaOtchet.save()
#                 #     except:
#                 #         NachisleniyaOtchet.objects.create(etrap='Dashoguz', month=month_word, year=year, alemNachisleniya=nach_dz)
#                 #     try:
#                 #         nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap='Akdepe', month=month_word, year=year)
#                 #         nachisleniyaOtchet.alemNachisleniya+=nach_ak
#                 #         nachisleniyaOtchet.save()
#                 #     except:
#                 #         NachisleniyaOtchet.objects.create(etrap='Akdepe', month=month_word, year=year, alemNachisleniya=nach_ak)
#                 #     try:
#                 #         nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap='Boldumsaz', month=month_word, year=year)
#                 #         nachisleniyaOtchet.alemNachisleniya+=nach_bol
#                 #         nachisleniyaOtchet.save()
#                 #     except:
#                 #         NachisleniyaOtchet.objects.create(etrap='Boldumsaz', month=month_word, year=year, alemNachisleniya=nach_bol)
#                 #     try:
#                 #         nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap='Gorogly', month=month_word, year=year)
#                 #         nachisleniyaOtchet.alemNachisleniya+=nach_gor
#                 #         nachisleniyaOtchet.save()
#                 #     except:
#                 #         NachisleniyaOtchet.objects.create(etrap='Gorogly', month=month_word, year=year, alemNachisleniya=nach_gor)
#                 #     try:
#                 #         nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap='Koneurgench', month=month_word, year=year)
#                 #         nachisleniyaOtchet.alemNachisleniya+=nach_kone
#                 #         nachisleniyaOtchet.save()
#                 #     except:
#                 #         NachisleniyaOtchet.objects.create(etrap='Koneurgench', month=month_word, year=year, alemNachisleniya=nach_kone)
#                 #     try:
#                 #         nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap='Turkmenbashy', month=month_word, year=year)
#                 #         nachisleniyaOtchet.alemNachisleniya+=nach_turk
#                 #         nachisleniyaOtchet.save()
#                 #     except:
#                 #         NachisleniyaOtchet.objects.create(etrap='Turkmenbashy', month=month_word, year=year, alemNachisleniya=nach_turk)
#                 #     try:
#                 #         nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap='S.A.Nyyazow', month=month_word, year=year)
#                 #         nachisleniyaOtchet.alemNachisleniya+=nach_nyyaz
#                 #         nachisleniyaOtchet.save()
#                 #     except:
#                 #         NachisleniyaOtchet.objects.create(etrap='S.A.Nyyazow', month=month_word, year=year, alemNachisleniya=nach_nyyaz)
#                 #     try:
#                 #         nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap='Ruhubelent', month=month_word, year=year)
#                 #         nachisleniyaOtchet.alemNachisleniya+=nach_ruh
#                 #         nachisleniyaOtchet.save()
#                 #     except:
#                 #         NachisleniyaOtchet.objects.create(etrap='Ruhubelent', month=month_word, year=year, alemNachisleniya=nach_ruh)

#                 StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')} \n\n\n Начисления заказ за {month_word} {year} года, этрап {etrap}", action='Начисления заказ')

#                 DontRepeatYourself.objects.create(zakazNachisleniaYearMonthEtrap=f"{year}{month_word}{etrap}")
                        
#                 print('Количество Начислений',testTotalCount)
#                 print('Сумма Начислений',testTotalPrice)

#                 messages.success(request, f'Успешное Начисления Заказ, {month_word} {year}')  
#             else:
#                 messages.error(request, mes)
                    

            
#     return render(request, 'telekom/MATB/zakazNachisleniya.html', context)