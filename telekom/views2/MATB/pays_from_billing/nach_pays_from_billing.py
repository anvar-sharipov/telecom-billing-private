from django.shortcuts import render, redirect
from django.contrib import messages

from datetime import date, datetime, timedelta
from telekom.models import ManagerNames, OldLoginDogowor, PayHistory, PlatejiWhichAddKassirsEveryDay, StaffAction, UserTable, KabelTvNew, KabelTvPayHistory, SaveInfoAboutWhoAddAndNachPaysFromBilling
from tablib import Dataset

from telekom.views2.myFunc.myFunc import getEtrapNameFromCode, monthСonvert

from django.db import transaction

import logging

logger = logging.getLogger(__name__)


def nach_pays_from_billing(request):
    context = {}

    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.username in ['intizar_gorogly', 'lenashb', 'testMTBDZ', 'AyshatGoroglyMtb', 'GuljahanAkdepeMtb', 'AzizShabatMtb', 'Saryyewa_Gozel_Shabat_MTB', 'BaharKoneurgenchKassa', 'Merjen_Yylally_MTB', 'GozelGubadagMtb', 'SelbiBoldumsazMtb', 'MahymAkdepeMtb', 'Aramedowa_Oguljemal', 'shirmamedowa_gulalek', 'Gayyp', 'Jumyazowa_Oguljemal', 'Kurbanowa_Gulnabat_Koneurgench', 'Baltabayewa_Sewara_MTB_DGE', 'Ishangulyyewa_Nurjemal_Koneurgench_kassa']:
            log = 'Dashoguz'
            context['nach_pays_from_billing'] = True
            if request.user.is_superuser:
                context['kassaIndex'] = True
            else:
                context['SHBIndex'] = True
                context['matbIndex'] = True
        else:
            messages.error(request, f'Доступ разрешен только администратору')
            return redirect('user-login')
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')
    


    groups = request.user.groups.all()
    request_user_etrap = None
    for g in groups:
        request_user_etrap, request_user_type = g.name.split('_')
        # print('request_user_etrap', request_user_etrap)
        # print('request_user_type', request_user_type)
    if request.user.is_superuser and request.user.username == 'admin1':
        request_user_etrap = 'Dashoguz'
    if not request_user_etrap:
        messages.error(request, f'Не достаточно прав')
        return redirect('user-login')


    objs = PlatejiWhichAddKassirsEveryDay.objects.filter(file_is_nach=False).order_by('-when_added_file')

    # print(objs)
    need_nach_file_names_new = []
    file_names_list_new = {}

    for o in objs:
        if o.file_name in ['platejiP_04_2024_1_25_ne_izmenyat_balance.xlsx', 'wn_plateji_akdepe_2025_01_ON.xlsx']:
            continue
        if o.file_name not in file_names_list_new:
            file_names_list_new[o.file_name] = False

        if o.file_name not in need_nach_file_names_new:
            if request.GET.get(o.file_name):
                need_nach_file_names_new.append(o.file_name)
    
    context['file_names_list'] = file_names_list_new
    context['need_to_nach_files'] = need_nach_file_names_new
   

    

    # file_names_list = {}
    # for pay in PlatejiWhichAddKassirsEveryDay.objects.all().order_by('-when_added_file'):
    #     if pay.file_name not in file_names_list:
    #         if pay.file_is_nach:
    #             file_names_list[pay.file_name] = True
    #         else:
    #             file_names_list[pay.file_name] = False
    # context['file_names_list'] = file_names_list
  
    # need_to_nach_files = []
    # for name in file_names_list:
    #     if request.GET.get(name):
    #         need_to_nach_files.append(name)
    # context['need_to_nach_files'] = need_to_nach_files

    # context['all_new_for_mtb'] = True

    if need_nach_file_names_new:
        count_alem_kassa = 0
        price_alem_kassa = 0
        count_int_kassa = 0
        price_int_kassa = 0
        count_abon_kassa = 0
        price_abon_kassa = 0 
        count_kabel_kassa = 0
        price_kabel_kassa = 0 

        count_alem_wn = 0
        price_alem_wn = 0
        count_int_wn = 0
        price_int_wn = 0
        count_abon_wn = 0
        price_abon_wn = 0

        count_kabel_wn = 0
        price_kabel_wn = 0

        count_alem_total = 0
        price_alem_total = 0
        count_int_total = 0
        price_int_total = 0
        count_abon_total = 0
        price_abon_total = 0

        count_kabel_total = 0
        price_kabel_total = 0  

        for file_ in need_nach_file_names_new:
            pays = PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=file_)
            for p in pays:
                if p.kassir_etrap == 'Внешние платежи':
                    if p.type_pay == 'Alem':
                        count_alem_wn += 1
                        price_alem_wn += p.price
                    elif p.type_pay == 'Internet':
                        count_int_wn += 1
                        price_int_wn += p.price
                    elif p.type_pay == 'Abonplata':
                        count_abon_wn += 1
                        price_abon_wn += p.price
                    elif p.type_pay == 'Kabel':
                        count_kabel_wn += 1
                        price_kabel_wn += p.price
                else:
                    if p.type_pay == 'Alem':
                        count_alem_kassa += 1
                        price_alem_kassa += p.price
                    elif p.type_pay == 'Internet':
                        count_int_kassa += 1
                        price_int_kassa += p.price
                    elif p.type_pay == 'Abonplata':
                        count_abon_kassa += 1
                        price_abon_kassa += p.price
                    elif p.type_pay == 'Kabel':
                        count_kabel_kassa += 1
                        price_kabel_kassa += p.price

        context['count_alem'] = f"{count_alem_kassa:_}"
        context['price_alem'] = f"{float('%.2f' % (price_alem_kassa)):_}"

        context['count_int'] = f"{count_int_kassa:_}"
        context['price_int'] = f"{float('%.2f' % (price_int_kassa)):_}"

        context['count_abon'] = f"{count_abon_kassa:_}"
        context['price_abon'] = f"{float('%.2f' % (price_abon_kassa)):_}"

        context['count_kabel'] = f"{count_kabel_kassa:_}"
        context['price_kabel'] = f"{float('%.2f' % (price_kabel_kassa)):_}"

        total_price = float('%.2f' % (price_alem_kassa + price_int_kassa + price_abon_kassa + price_kabel_kassa))
        total_count = count_alem_kassa + count_int_kassa + count_abon_kassa + count_kabel_kassa

        context['total_price'] = f"{total_price:_}"
        context['total_count'] = f"{total_count:_}"




        context['count_alem_wn'] = f"{count_alem_wn:_}"
        context['price_alem_wn'] = f"{float('%.2f' % (price_alem_wn)):_}"

        context['count_int_wn'] = f"{count_int_wn:_}"
        context['price_int_wn'] = f"{float('%.2f' % (price_int_wn)):_}"

        context['count_abon_wn'] = f"{count_abon_wn:_}"
        context['price_abon_wn'] = f"{float('%.2f' % (price_abon_wn)):_}"

        context['count_kabel_wn'] = f"{count_kabel_wn:_}"
        context['price_kabel_wn'] = f"{float('%.2f' % (price_kabel_wn)):_}"

        total_price_wn = float('%.2f' % (price_alem_wn + price_int_wn + price_abon_wn + price_kabel_wn))
        total_count_wn = count_alem_wn + count_int_wn + count_abon_wn + count_kabel_wn

        context['total_price_wn'] = f"{total_price_wn:_}"
        context['total_count_wn'] = f"{total_count_wn:_}"


        count_alem_total = count_alem_wn + count_alem_kassa
        price_alem_total = price_alem_wn + price_alem_kassa
        count_int_total = count_int_wn + count_int_kassa
        price_int_total = price_int_wn + price_int_kassa
        count_abon_total = count_abon_wn + count_abon_kassa
        price_abon_total = price_abon_wn + price_abon_kassa
        
        count_kabel_total = count_kabel_wn + count_kabel_kassa
        price_kabel_total = price_kabel_wn + price_kabel_kassa

        context['count_alem_total'] = f"{count_alem_total:_}"
        context['price_alem_total'] = f"{float('%.2f' % (price_alem_total)):_}"

        context['count_int_total'] = f"{count_int_total:_}"
        context['price_int_total'] = f"{float('%.2f' % (price_int_total)):_}"

        context['count_abon_total'] = f"{count_abon_total:_}"
        context['price_abon_total'] = f"{float('%.2f' % (price_abon_total)):_}"

        context['count_kabel_total'] = f"{count_kabel_total:_}"
        context['price_kabel_total'] = f"{float('%.2f' % (price_kabel_total)):_}"

        total_price_total = float('%.2f' % (price_alem_total + price_int_total + price_abon_total + price_kabel_total))
        total_count_total = count_alem_total + count_int_total + count_abon_total + count_kabel_total

        context['total_price_total'] = f"{total_price_total:_}"
        context['total_count_total'] = f"{total_count_total:_}"

        if request.method != 'POST':
            messages.success(request, f"Есть платежи")

    else:
        messages.error(request, f"Выберите файлы которые надо начислить")

    if request.method == 'POST' and 'nachislit' in request.POST:

        if request.POST.get('comment') == '' or request.POST.get('comment') == None:
            messages.error(request, f"Оставьте комментарий! Комментарий не может быть пустым")
            return render(request, 'telekom/MATB/pays_from_billing/nach_pays_from_billing.html', context)
        
        if need_nach_file_names_new:
            user_pk_val = {} # {} {pk: [b_prochee, b_internet, b_alem, b_kabel]} # KABEL NET
            bulk_create_pay = []
            bulk_updete_user = []

            bulk_create_kabel_new_pay = []
            bulk_updete_kabel_new_user = []

            etrap_number_pk = {} # {etrap: number: pk}
            users = UserTable.objects.all()
            count2 = 0

            kabel_new_pk_balance = {} #{pk: balance}
            for user in users:
                count2 += 1
                if count2 % 50000 == 0:
                    # print('Обработка файлов ...')
                    logger.info(f'==== Обработка файлов ...')
                if user.etrap not in etrap_number_pk:
                    etrap_number_pk[user.etrap] = {user.number: user.pk}
                else:
                    etrap_number_pk[user.etrap][user.number] = user.pk

           
            count = 0
            for file_ in need_nach_file_names_new:
                pays = PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=file_)
                for p in pays:
                    if p.file_is_nach:
                        continue
                    count += 1

                    if count % 1000 == 0:
                        # print(f'Оплачено {count} из {total_count_total}')
                        logger.info(f' ==== Оплачено {count} из {total_count_total}')

                    if count == total_count_total:
                        # print(f'Оплачено {count} из {total_count_total}')
                        logger.info(f' ==== Оплачено {count} из {total_count_total}')

                    is_card = False
                    if 'картой' in p.pay_category:
                        is_card = True

                    if p.type_pay == 'Kabel':
                        # if user.pk not in user_pk_val:
                        #     user_pk_val[user.pk] = [0,0,0,p.price]
                        # else:
                        #     user_pk_val[user.pk][3] += p.price
                        # obj = PayHistory(abonent=user, kabel=p.price, is_card=is_card, kassir=p.manager, kassa=p.manager, total=p.price, date=p.date, edara_ilat=p.is_enterprises, type='Default', kassir_etrap=p.kassir_etrap)
                        user_k = KabelTvNew.objects.get(number=p.number)

                        obj_new = KabelTvPayHistory(
                            user=user_k,
                            pay=p.price,
                            pay_date=p.date,
                            pay_kassir=p.manager,
                            card=is_card
                        )
                        bulk_create_kabel_new_pay.append(obj_new)
                        if user_k.pk not in kabel_new_pk_balance:
                            kabel_new_pk_balance[user_k.pk] = p.price
                        else:
                            kabel_new_pk_balance[user_k.pk] += p.price

                        continue

                    user = UserTable.objects.get(pk=etrap_number_pk[p.user_etrap][p.number])
                    
                    if p.type_pay == 'Abonplata':
                        if user.pk not in user_pk_val:
                            user_pk_val[user.pk] = [p.price,0,0]
                        else:
                            user_pk_val[user.pk][0] += p.price
                        obj = PayHistory(abonent=user, prochee=p.price, is_card=is_card, kassir=p.manager, kassa=p.manager, total=p.price, date=p.date, edara_ilat=p.is_enterprises, type='Default', kassir_etrap=p.kassir_etrap, pays_from_billing_file_name=file_)
                    if p.type_pay == 'Internet':
                        if user.pk not in user_pk_val:
                            user_pk_val[user.pk] = [0,p.price,0]
                        else:
                            user_pk_val[user.pk][1] += p.price
                        obj = PayHistory(abonent=user, internet=p.price, is_card=is_card, kassir=p.manager, kassa=p.manager, total=p.price, date=p.date, edara_ilat=p.is_enterprises, type='Default', kassir_etrap=p.kassir_etrap, pays_from_billing_file_name=file_)
                    if p.type_pay == 'Alem':
                        if user.pk not in user_pk_val:
                            user_pk_val[user.pk] = [0,0,p.price]
                        else:
                            user_pk_val[user.pk][2] += p.price
                        obj = PayHistory(abonent=user, alem=p.price, is_card=is_card, kassir=p.manager, kassa=p.manager, total=p.price, date=p.date, edara_ilat=p.is_enterprises, type='Default', kassir_etrap=p.kassir_etrap, pays_from_billing_file_name=file_)
                    
                    
         
                   
                    bulk_create_pay.append(obj)

                
                    
         
            try:
                with transaction.atomic():
                    if user_pk_val:
                        # pass
                        for pk, v in user_pk_val.items():
                            user = UserTable.objects.get(pk=pk)
                            user.b_prochee += v[0]
                            user.b_internet += v[1]
                            user.b_alem += v[2]
                            # user.b_kabel += v[3]
                            bulk_updete_user.append(user)
                        if bulk_updete_user:
                            UserTable.objects.bulk_update(bulk_updete_user, ['b_prochee', 'b_alem', 'b_internet'])

                    if kabel_new_pk_balance:
                        for pk, balance in kabel_new_pk_balance.items():
                            user_k = KabelTvNew.objects.get(pk=pk)
                            user_k.balance += balance
                            bulk_updete_kabel_new_user.append(user_k)
                        if bulk_updete_kabel_new_user:
                            KabelTvNew.objects.bulk_update(bulk_updete_kabel_new_user, ['balance'])
                    if bulk_create_kabel_new_pay:
                        KabelTvPayHistory.objects.bulk_create(bulk_create_kabel_new_pay)
                        
                    if bulk_create_pay:
                        PayHistory.objects.bulk_create(bulk_create_pay)

                    for file_ in need_nach_file_names_new:
                        # print('gg',file_)
                        obj_save_info = SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.get(file_name=file_)
                        obj_save_info.etrap_nach=request_user_etrap
                        obj_save_info.who_nach=request.user.username
                        obj_save_info.when_nach=datetime.now()
                        obj_save_info.save()
                        file_names_list_new[file_] = True
                        PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=file_).update(file_is_nach=True)

                    # file_names_list = {}
                    # for pay in PlatejiWhichAddKassirsEveryDay.objects.all().order_by('-when_added_file'):
                    #     if pay.file_name not in file_names_list:
                    #         if pay.file_is_nach:
                    #             file_names_list[pay.file_name] = True
                    #         else:
                    #             file_names_list[pay.file_name] = False
                    # context['file_names_list'] = file_names_list
                    # context['need_to_nach_files'] = {}


                    StaffAction.objects.create(user=request.user, comment=request.POST.get('comment'), action='Пробитие платежей с базы данных')
                    messages.success(request, f"Успешное начисление файла {need_nach_file_names_new}")
            except Exception as e:
                messages.error(request, f'ошибка с transaction при сохранении, тип ошибки == {e}')
                logger.error(f'ошибка с transaction при сохранении, тип ошибки == {e}')
        else:
            messages.error(request, f"Выберите файлы которые надо начислить")


    return render(request, 'telekom/MATB/pays_from_billing/nach_pays_from_billing.html', context)



# rabotaet, no net Garashsyzlyk i Gubadag
# from django.shortcuts import render, redirect
# from django.contrib import messages

# from datetime import date, datetime, timedelta
# from telekom.models import ManagerNames, OldLoginDogowor, PayHistory, PlatejiWhichAddKassirsEveryDay, StaffAction, UserTable, KabelTvNew, KabelTvPayHistory, SaveInfoAboutWhoAddAndNachPaysFromBilling
# from tablib import Dataset

# from telekom.views2.myFunc.myFunc import getEtrapNameFromCode, monthСonvert

# from django.db import transaction

# import logging

# logger = logging.getLogger(__name__)


# def nach_pays_from_billing(request):
#     context = {}

#     if request.user.is_authenticated:
#         if request.user.is_superuser or request.user.username in ['lenashb', 'testMTBDZ', 'AyshatGoroglyMtb', 'GuljahanAkdepeMtb', 'AzizShabatMtb', 'Saryyewa_Gozel_Shabat_MTB', 'BaharKoneurgenchKassa', 'Merjen_Yylally_MTB', 'GozelGubadagMtb', 'SelbiBoldumsazMtb', 'MahymAkdepeMtb', 'Aramedowa_Oguljemal', 'Gayyp', 'Jumyazowa_Oguljemal', 'Kurbanowa_Gulnabat_Koneurgench']:
#             log = 'Dashoguz'
#             context['nach_pays_from_billing'] = True
#             if request.user.is_superuser:
#                 context['kassaIndex'] = True
#             else:
#                 context['SHBIndex'] = True
#                 context['matbIndex'] = True
#         else:
#             messages.error(request, f'Доступ разрешен только администратору')
#             return redirect('user-login')
#     else:
#         messages.error(request, f'Вы не аутентифицированы')
#         return redirect('user-login')
    


#     groups = request.user.groups.all()
#     request_user_etrap = None
#     for g in groups:
#         request_user_etrap, request_user_type = g.name.split('_')
#         # print('request_user_etrap', request_user_etrap)
#         # print('request_user_type', request_user_type)
#     if request.user.is_superuser and request.user.username == 'admin1':
#         request_user_etrap = 'Dashoguz'
#     if not request_user_etrap:
#         messages.error(request, f'Не достаточно прав')
#         return redirect('user-login')


#     objs = PlatejiWhichAddKassirsEveryDay.objects.filter(file_is_nach=False).order_by('-when_added_file')

#     # print(objs)
#     need_nach_file_names_new = []
#     file_names_list_new = {}

#     for o in objs:
#         if o.file_name in ['platejiP_04_2024_1_25_ne_izmenyat_balance.xlsx', 'wn_plateji_akdepe_2025_01_ON.xlsx']:
#             continue
#         if o.file_name not in file_names_list_new:
#             file_names_list_new[o.file_name] = False

#         if o.file_name not in need_nach_file_names_new:
#             if request.GET.get(o.file_name):
#                 need_nach_file_names_new.append(o.file_name)
    
#     context['file_names_list'] = file_names_list_new
#     context['need_to_nach_files'] = need_nach_file_names_new
   

    

#     # file_names_list = {}
#     # for pay in PlatejiWhichAddKassirsEveryDay.objects.all().order_by('-when_added_file'):
#     #     if pay.file_name not in file_names_list:
#     #         if pay.file_is_nach:
#     #             file_names_list[pay.file_name] = True
#     #         else:
#     #             file_names_list[pay.file_name] = False
#     # context['file_names_list'] = file_names_list
  
#     # need_to_nach_files = []
#     # for name in file_names_list:
#     #     if request.GET.get(name):
#     #         need_to_nach_files.append(name)
#     # context['need_to_nach_files'] = need_to_nach_files

#     # context['all_new_for_mtb'] = True

#     if need_nach_file_names_new:
#         count_alem_kassa = 0
#         price_alem_kassa = 0
#         count_int_kassa = 0
#         price_int_kassa = 0
#         count_abon_kassa = 0
#         price_abon_kassa = 0 
#         count_kabel_kassa = 0
#         price_kabel_kassa = 0 

#         count_alem_wn = 0
#         price_alem_wn = 0
#         count_int_wn = 0
#         price_int_wn = 0
#         count_abon_wn = 0
#         price_abon_wn = 0

#         count_kabel_wn = 0
#         price_kabel_wn = 0

#         count_alem_total = 0
#         price_alem_total = 0
#         count_int_total = 0
#         price_int_total = 0
#         count_abon_total = 0
#         price_abon_total = 0

#         count_kabel_total = 0
#         price_kabel_total = 0  

#         for file_ in need_nach_file_names_new:
#             pays = PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=file_)
#             for p in pays:
#                 if p.kassir_etrap == 'Внешние платежи':
#                     if p.type_pay == 'Alem':
#                         count_alem_wn += 1
#                         price_alem_wn += p.price
#                     elif p.type_pay == 'Internet':
#                         count_int_wn += 1
#                         price_int_wn += p.price
#                     elif p.type_pay == 'Abonplata':
#                         count_abon_wn += 1
#                         price_abon_wn += p.price
#                     elif p.type_pay == 'Kabel':
#                         count_kabel_wn += 1
#                         price_kabel_wn += p.price
#                 else:
#                     if p.type_pay == 'Alem':
#                         count_alem_kassa += 1
#                         price_alem_kassa += p.price
#                     elif p.type_pay == 'Internet':
#                         count_int_kassa += 1
#                         price_int_kassa += p.price
#                     elif p.type_pay == 'Abonplata':
#                         count_abon_kassa += 1
#                         price_abon_kassa += p.price
#                     elif p.type_pay == 'Kabel':
#                         count_kabel_kassa += 1
#                         price_kabel_kassa += p.price

#         context['count_alem'] = f"{count_alem_kassa:_}"
#         context['price_alem'] = f"{float('%.2f' % (price_alem_kassa)):_}"

#         context['count_int'] = f"{count_int_kassa:_}"
#         context['price_int'] = f"{float('%.2f' % (price_int_kassa)):_}"

#         context['count_abon'] = f"{count_abon_kassa:_}"
#         context['price_abon'] = f"{float('%.2f' % (price_abon_kassa)):_}"

#         context['count_kabel'] = f"{count_kabel_kassa:_}"
#         context['price_kabel'] = f"{float('%.2f' % (price_kabel_kassa)):_}"

#         total_price = float('%.2f' % (price_alem_kassa + price_int_kassa + price_abon_kassa + price_kabel_kassa))
#         total_count = count_alem_kassa + count_int_kassa + count_abon_kassa + count_kabel_kassa

#         context['total_price'] = f"{total_price:_}"
#         context['total_count'] = f"{total_count:_}"




#         context['count_alem_wn'] = f"{count_alem_wn:_}"
#         context['price_alem_wn'] = f"{float('%.2f' % (price_alem_wn)):_}"

#         context['count_int_wn'] = f"{count_int_wn:_}"
#         context['price_int_wn'] = f"{float('%.2f' % (price_int_wn)):_}"

#         context['count_abon_wn'] = f"{count_abon_wn:_}"
#         context['price_abon_wn'] = f"{float('%.2f' % (price_abon_wn)):_}"

#         context['count_kabel_wn'] = f"{count_kabel_wn:_}"
#         context['price_kabel_wn'] = f"{float('%.2f' % (price_kabel_wn)):_}"

#         total_price_wn = float('%.2f' % (price_alem_wn + price_int_wn + price_abon_wn + price_kabel_wn))
#         total_count_wn = count_alem_wn + count_int_wn + count_abon_wn + count_kabel_wn

#         context['total_price_wn'] = f"{total_price_wn:_}"
#         context['total_count_wn'] = f"{total_count_wn:_}"


#         count_alem_total = count_alem_wn + count_alem_kassa
#         price_alem_total = price_alem_wn + price_alem_kassa
#         count_int_total = count_int_wn + count_int_kassa
#         price_int_total = price_int_wn + price_int_kassa
#         count_abon_total = count_abon_wn + count_abon_kassa
#         price_abon_total = price_abon_wn + price_abon_kassa
        
#         count_kabel_total = count_kabel_wn + count_kabel_kassa
#         price_kabel_total = price_kabel_wn + price_kabel_kassa

#         context['count_alem_total'] = f"{count_alem_total:_}"
#         context['price_alem_total'] = f"{float('%.2f' % (price_alem_total)):_}"

#         context['count_int_total'] = f"{count_int_total:_}"
#         context['price_int_total'] = f"{float('%.2f' % (price_int_total)):_}"

#         context['count_abon_total'] = f"{count_abon_total:_}"
#         context['price_abon_total'] = f"{float('%.2f' % (price_abon_total)):_}"

#         context['count_kabel_total'] = f"{count_kabel_total:_}"
#         context['price_kabel_total'] = f"{float('%.2f' % (price_kabel_total)):_}"

#         total_price_total = float('%.2f' % (price_alem_total + price_int_total + price_abon_total + price_kabel_total))
#         total_count_total = count_alem_total + count_int_total + count_abon_total + count_kabel_total

#         context['total_price_total'] = f"{total_price_total:_}"
#         context['total_count_total'] = f"{total_count_total:_}"

#         if request.method != 'POST':
#             messages.success(request, f"Есть платежи")

#     else:
#         messages.error(request, f"Выберите файлы которые надо начислить")

#     if request.method == 'POST' and 'nachislit' in request.POST:

#         if request.POST.get('comment') == '' or request.POST.get('comment') == None:
#             messages.error(request, f"Оставьте комментарий! Комментарий не может быть пустым")
#             return render(request, 'telekom/MATB/pays_from_billing/nach_pays_from_billing.html', context)
        
#         if need_nach_file_names_new:
#             user_pk_val = {} # {} {pk: [b_prochee, b_internet, b_alem, b_kabel]} # KABEL NET
#             bulk_create_pay = []
#             bulk_updete_user = []

#             bulk_create_kabel_new_pay = []
#             bulk_updete_kabel_new_user = []

#             etrap_number_pk = {} # {etrap: number: pk}
#             users = UserTable.objects.all()
#             count2 = 0

#             kabel_new_pk_balance = {} #{pk: balance}
#             for user in users:
#                 count2 += 1
#                 if count2 % 50000 == 0:
#                     # print('Обработка файлов ...')
#                     logger.info(f'==== Обработка файлов ...')
#                 if user.etrap not in etrap_number_pk:
#                     etrap_number_pk[user.etrap] = {user.number: user.pk}
#                 else:
#                     etrap_number_pk[user.etrap][user.number] = user.pk

           
#             count = 0
#             for file_ in need_nach_file_names_new:
#                 pays = PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=file_)
#                 for p in pays:
#                     if p.file_is_nach:
#                         continue
#                     count += 1

#                     if count % 1000 == 0:
#                         # print(f'Оплачено {count} из {total_count_total}')
#                         logger.info(f' ==== Оплачено {count} из {total_count_total}')

#                     if count == total_count_total:
#                         # print(f'Оплачено {count} из {total_count_total}')
#                         logger.info(f' ==== Оплачено {count} из {total_count_total}')

#                     is_card = False
#                     if 'картой' in p.pay_category:
#                         is_card = True

#                     if p.type_pay == 'Kabel':
#                         # if user.pk not in user_pk_val:
#                         #     user_pk_val[user.pk] = [0,0,0,p.price]
#                         # else:
#                         #     user_pk_val[user.pk][3] += p.price
#                         # obj = PayHistory(abonent=user, kabel=p.price, is_card=is_card, kassir=p.manager, kassa=p.manager, total=p.price, date=p.date, edara_ilat=p.is_enterprises, type='Default', kassir_etrap=p.kassir_etrap)
#                         user_k = KabelTvNew.objects.get(number=p.number)

#                         obj_new = KabelTvPayHistory(
#                             user=user_k,
#                             pay=p.price,
#                             pay_date=p.date,
#                             pay_kassir=p.manager,
#                             card=is_card
#                         )
#                         bulk_create_kabel_new_pay.append(obj_new)
#                         if user_k.pk not in kabel_new_pk_balance:
#                             kabel_new_pk_balance[user_k.pk] = p.price
#                         else:
#                             kabel_new_pk_balance[user_k.pk] += p.price

#                         continue

#                     user = UserTable.objects.get(pk=etrap_number_pk[p.user_etrap][p.number])
                    
#                     if p.type_pay == 'Abonplata':
#                         if user.pk not in user_pk_val:
#                             user_pk_val[user.pk] = [p.price,0,0]
#                         else:
#                             user_pk_val[user.pk][0] += p.price
#                         obj = PayHistory(abonent=user, prochee=p.price, is_card=is_card, kassir=p.manager, kassa=p.manager, total=p.price, date=p.date, edara_ilat=p.is_enterprises, type='Default', kassir_etrap=p.kassir_etrap)
#                     if p.type_pay == 'Internet':
#                         if user.pk not in user_pk_val:
#                             user_pk_val[user.pk] = [0,p.price,0]
#                         else:
#                             user_pk_val[user.pk][1] += p.price
#                         obj = PayHistory(abonent=user, internet=p.price, is_card=is_card, kassir=p.manager, kassa=p.manager, total=p.price, date=p.date, edara_ilat=p.is_enterprises, type='Default', kassir_etrap=p.kassir_etrap)
#                     if p.type_pay == 'Alem':
#                         if user.pk not in user_pk_val:
#                             user_pk_val[user.pk] = [0,0,p.price]
#                         else:
#                             user_pk_val[user.pk][2] += p.price
#                         obj = PayHistory(abonent=user, alem=p.price, is_card=is_card, kassir=p.manager, kassa=p.manager, total=p.price, date=p.date, edara_ilat=p.is_enterprises, type='Default', kassir_etrap=p.kassir_etrap)
                    
                    
         
                   
#                     bulk_create_pay.append(obj)

                
                    
         
#             try:
#                 with transaction.atomic():
#                     if user_pk_val:
#                         # pass
#                         for pk, v in user_pk_val.items():
#                             user = UserTable.objects.get(pk=pk)
#                             user.b_prochee += v[0]
#                             user.b_internet += v[1]
#                             user.b_alem += v[2]
#                             # user.b_kabel += v[3]
#                             bulk_updete_user.append(user)
#                         if bulk_updete_user:
#                             UserTable.objects.bulk_update(bulk_updete_user, ['b_prochee', 'b_alem', 'b_internet'])

#                     if kabel_new_pk_balance:
#                         for pk, balance in kabel_new_pk_balance.items():
#                             user_k = KabelTvNew.objects.get(pk=pk)
#                             user_k.balance += balance
#                             bulk_updete_kabel_new_user.append(user_k)
#                         if bulk_updete_kabel_new_user:
#                             KabelTvNew.objects.bulk_update(bulk_updete_kabel_new_user, ['balance'])
#                     if bulk_create_kabel_new_pay:
#                         KabelTvPayHistory.objects.bulk_create(bulk_create_kabel_new_pay)
                        
#                     if bulk_create_pay:
#                         PayHistory.objects.bulk_create(bulk_create_pay)

#                     for file_ in need_nach_file_names_new:
#                         # print('gg',file_)
#                         obj_save_info = SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.get(file_name=file_)
#                         obj_save_info.etrap_nach=request_user_etrap
#                         obj_save_info.who_nach=request.user.username
#                         obj_save_info.when_nach=datetime.now()
#                         obj_save_info.save()
#                         file_names_list_new[file_] = True
#                         PlatejiWhichAddKassirsEveryDay.objects.filter(file_name=file_).update(file_is_nach=True)

#                     # file_names_list = {}
#                     # for pay in PlatejiWhichAddKassirsEveryDay.objects.all().order_by('-when_added_file'):
#                     #     if pay.file_name not in file_names_list:
#                     #         if pay.file_is_nach:
#                     #             file_names_list[pay.file_name] = True
#                     #         else:
#                     #             file_names_list[pay.file_name] = False
#                     # context['file_names_list'] = file_names_list
#                     # context['need_to_nach_files'] = {}


#                     StaffAction.objects.create(user=request.user, comment=request.POST.get('comment'), action='Пробитие платежей с базы данных')
#                     messages.success(request, f"Успешное начисление файла {need_nach_file_names_new}")
#             except Exception as e:
#                 messages.error(request, f'ошибка с transaction при сохранении, тип ошибки == {e}')
#                 logger.error(f'ошибка с transaction при сохранении, тип ошибки == {e}')
#         else:
#             messages.error(request, f"Выберите файлы которые надо начислить")


#     return render(request, 'telekom/MATB/pays_from_billing/nach_pays_from_billing.html', context)



