# Код с transaction
from django.shortcuts import render, redirect
from django.contrib import messages


from datetime import datetime
from datetime import date
from calendar import monthrange

from telekom.models import DontRepeatYourself, LocalCall, NachMinus, NachisleniyaOtchet, NonLocalCall, StaffAction, UserTable, dbfNameList
from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert
import sys
from bulk_update.helper import bulk_update

from django.http import HttpResponse
import tablib

from django.db import transaction

import logging

logger = logging.getLogger(__name__)



def kodSlrFileNachisleniya(request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        pass
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    context = {}
    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date

    if request.GET.get('month') == '':
        return redirect('kod-slr-file-nachisleniya')

    # if request.GET.get('month') == '':
    #     return redirect('slr-nachisleniya')

    context['matbIndex'] = True
    context['kodSlrFileNachisleniya'] = True

    dbf_name_lists = dbfNameList.objects.all().order_by('-pk')
    context["dbf_name_lists"] = dbf_name_lists

    getNameList = request.GET.getlist('getNameList')
    context['getNameList'] = getNameList

    context['get_month'] = request.GET.get('month')
    context['get_year'] = request.GET.get('year')

    usersNumEtrap = UserTable.objects.values('number', 'etrap')
    # ['20000Dashoguz', '20000Akdepe'] список из numberetrap которые есть в нашей БД
    usersNumEtrList = {}
    for dict_ in usersNumEtrap:
        for key, val in dict_.items():
            if key == 'number':
                word = val
            if key == 'etrap':
                word += val
        usersNumEtrList[word] = True
    
    if getNameList:
        users = UserTable.objects.all()
        number_pk = {} # {numberEtrap: pk}
        for user in users:
            number = user.number
            etrap = user.etrap
            number_pk[f"{number}{etrap}"] = user.pk

        nach_year_month_number_pk = {} # {yearMonth: {etrapNumber: nachPk}}
        countNach = 0
        for name in getNameList:
            countNach += 1
            logger.info(f' ==== Проверка файлов {countNach} из {len(getNameList)}, {name}')
            globalCall = NonLocalCall.objects.filter(file_name = name)
            for call in globalCall:
                etrap = call.SUB_A_etrap
                date_ = str(call.DATE)
                year = date_[:4]
                month = date_[5:7]
                number = call.SUB_A
                if f"{year}{month}" not in nach_year_month_number_pk:
                    nach_pk = {}
                    for n in NachMinus.objects.filter(year=year, month=month):
                        nach_pk[f"{n.user.etrap}{n.user.number}"] = n.pk
                    nach_year_month_number_pk[f"{year}{month}"] = nach_pk
    
        
        my_dict_global = {} #{year: {month: {etrap: {number: [kod, prochee]}}}}
        my_dict_local = {} # {year: {month: {etrap: {day: {number: MT }}}}}

        totalKodPriceEdara = 0
        totalKodPriceIlat = 0


        dbfYearMonth = []
        dbf_count = 0

        AbonentCountSuccessGlobal = 0
        totalSuccesCallsGlobal = 0
        totalMtSuccessGlobal = 0
        totalSuccessPriceGlobal = 0

        AbonentCountSuccessLocal = 0
        totalSuccesCallsLocal = 0
        totalMtBruttoSuccessLocal = 0
        totalSuccessPriceBruttoLocal = 0
        
        # for name in getNameList:
        #     # Проверка нет ли повторных разговоров (дубликатов)
        #     values_pk = {} # {f"SUB_A_etrap, SUB_A, SUB_B_locations, SUB_B, price, DATE, START, FIN, DUR, MT": pk}
        #     count = 0
        #     delete_pks = []
        #     global_ = NonLocalCall.objects.exclude(file_name=name)
        #     for c in global_:
        #         pk = c.pk
        #         SUB_A_etrap = str(c.SUB_A_etrap)
        #         SUB_A = str(c.SUB_A)
        #         SUB_B_locations = str(c.SUB_B_locations)
        #         SUB_B = str(c.SUB_B)
        #         price = str(c.price)
        #         DATE = str(c.DATE)
        #         START = str(c.START)
        #         FIN = str(c.FIN)
        #         DUR = str(c.DUR)
        #         MT = str(c.MT)
        #         file_name = str(c.file_name)

        #         if f"{SUB_A_etrap}{SUB_A}{SUB_B_locations}{SUB_B}{price}{DATE}{START}{FIN}{DUR}{MT}" not in values_pk:
        #             values_pk[f"{SUB_A_etrap}{SUB_A}{SUB_B_locations}{SUB_B}{price}{DATE}{START}{FIN}{DUR}{MT}"] = c.pk
        #         else:
        #             count += 1
        #             delete_pks.append(c.pk)
        #             print(count)
        #     print('global_', len(global_))
        #     # print('values_pk', len(values_pk))
        #     delCount = 0
        #     # for p in delete_pks:
        #     #     delCount += 1
        #     #     print('delCount', delCount)
        #     #     NonLocalCall.objects.get(pk=p).delete()
        test_total_min_slr = 0
        test_total_price_kod = 0
        for name in getNameList: 
            dbf_count += 1
            logger.info(f' ==== Подготовка файлов {dbf_count} из {len(getNameList)}, {name}')
            # global
            globalCall = NonLocalCall.objects.filter(file_name = name)
            for call in globalCall:

                
                
                totalSuccesCallsGlobal += 1
                price = float(call.price)
                MT = int(call.MT)
                totalMtSuccessGlobal += MT
                total_price = price * MT
                totalSuccessPriceGlobal += total_price
                hb = call.edara
                number = call.SUB_A
                etrap = call.SUB_A_etrap
                etrap_B = call.SUB_B_locations
                date_ = str(call.DATE)
                test_total_price_kod += price * MT


                # nach_year_months               
                year = date_[:4]
                month = date_[5:7]

                if date_ not in dbfYearMonth:
                    dbfYearMonth.append(date_)

                # if f"{monthСonvert(month)} {year}" not in dbfYearMonth:
                #     dbfYearMonth.append(f"{monthСonvert(month)} {year}")

                # Работающий код с прочее для ILAT
                # user = users.get(pk=number_pk[f"{number}{etrap}"])
                # b_prochee = user.b_prochee
                # prochee = 0
                if hb == 'H':
                    totalKodPriceEdara += total_price
                    # if b_prochee <=0: 
                    #     # prochee = total_price * 0.1
                    #     prochee = 0
                    #     totalProcheePriceHoz += prochee
                elif hb == 'I' or hb == 'E':
                    totalKodPriceIlat += total_price
                    # if b_prochee <=0:
                    #     prochee = total_price * 0.05  
                    #     totalProcheePriceIlat += prochee
                elif hb == 'B':
                    totalKodPriceEdara += total_price
                # if year not in my_dict_global:
                #     my_dict_global[year] = {month: {etrap: {number: [total_price, prochee]}}}
                # elif month not in my_dict_global[year]:
                #     my_dict_global[year][month] = {etrap: {number: [total_price, prochee]}}
                # elif etrap not in my_dict_global[year][month]:
                #     my_dict_global[year][month][etrap] = {number: [total_price, prochee]}
                # elif number not in my_dict_global[year][month][etrap]:
                #     my_dict_global[year][month][etrap][number] = [total_price, prochee]
                # else:
                #     my_dict_global[year][month][etrap][number][0] += total_price
                #     my_dict_global[year][month][etrap][number][1] += prochee

                if year not in my_dict_global:
                    my_dict_global[year] = {month: {etrap: {number: total_price}}}
                elif month not in my_dict_global[year]:
                    my_dict_global[year][month] = {etrap: {number: total_price}}
                elif etrap not in my_dict_global[year][month]:
                    my_dict_global[year][month][etrap] = {number: total_price}
                elif number not in my_dict_global[year][month][etrap]:
                    my_dict_global[year][month][etrap][number] = total_price
                    AbonentCountSuccessGlobal += 1
                else:
                    my_dict_global[year][month][etrap][number] += total_price

     

            # local
            localCalls = LocalCall.objects.filter(file_name = name).exclude(edara='B')
            for call in localCalls:
                totalSuccesCallsLocal += 1
                number = call.SUB_A
                date_ = str(call.DATE)
                MT = int(call.MT)
                etrap = call.etrap
                year = date_[:4]
                month = date_[5:7]
                day_ = date_[-2:]
                if year not in my_dict_local:
                    my_dict_local[year] = {month: {etrap: {day_: {number: MT}}}}
                elif month not in my_dict_local[year]:
                    my_dict_local[year][month] = {etrap: {day_: {number: MT}}}
                elif etrap not in my_dict_local[year][month]:
                    my_dict_local[year][month][etrap] = {day_: {number: MT}}
                elif day_ not in my_dict_local[year][month][etrap]:
                    my_dict_local[year][month][etrap][day_] = {number: MT}
                elif number not in my_dict_local[year][month][etrap][day_]:
                    my_dict_local[year][month][etrap][day_][number] = MT
                else:
                    my_dict_local[year][month][etrap][day_][number] += MT


        local_c = my_dict_local.copy()
        for year, values in local_c.items():
            values_c = values.copy()
            for month, value in values_c.items():
                value_c = value.copy()
                for etrap, val in value_c.items():
                    val_c = val.copy()
                    for day_, v in val_c.items():
                        v_c = v.copy()
                        for number, MT in v_c.items():
                            if MT <= 5:
                                del my_dict_local[year][month][etrap][day_][number]
                                if my_dict_local[year][month][etrap][day_] == {}:
                                    del my_dict_local[year][month][etrap][day_]
                                if my_dict_local[year][month][etrap] == {}:
                                    del my_dict_local[year][month][etrap]
                                if my_dict_local[year][month] == {}:
                                    del my_dict_local[year][month]
                                if my_dict_local[year] == {}:
                                    del my_dict_local[year]
                            else:
                                continue
        etrapNumberMT = {} # {year: {month: {etrap: {number: MT}}}}
        for year, values in my_dict_local.items():
            for month, value in values.items():
                for etrap, val in value.items():
                    for day_, v in val.items():
                        for number, MT in v.items():

                            if year not in etrapNumberMT:
                                etrapNumberMT[year] = {month: {etrap: {number: MT - 5}}}
                            elif month not in etrapNumberMT[year]:
                                etrapNumberMT[year][month] = {etrap: {number: MT - 5}}
                            elif etrap not in etrapNumberMT[year][month]:
                                etrapNumberMT[year][month][etrap] = {number:MT-5}
                            elif number not in  etrapNumberMT[year][month][etrap]:
                                etrapNumberMT[year][month][etrap][number] = MT-5
                                AbonentCountSuccessLocal += 1
                            else:
                                etrapNumberMT[year][month][etrap][number] += MT-5
                                
                            price = (MT - 5) * 0.0006
                            totalSuccessPriceBruttoLocal += price
                            totalMtBruttoSuccessLocal += (MT - 5)
                     
        print('test_total_price_kod', test_total_price_kod)
        context['totalKodPriceEdara'] = totalKodPriceEdara
        context['totalKodPriceIlat'] = totalKodPriceIlat
        context['dbfYearMonth'] = dbfYearMonth

        context['AbonentCountSuccessGlobal'] = AbonentCountSuccessGlobal
        context['totalSuccesCallsGlobal'] = totalSuccesCallsGlobal
        context['totalMtSuccessGlobal'] = totalMtSuccessGlobal
        context['totalSuccessPriceGlobal'] = totalSuccessPriceGlobal

        context['AbonentCountSuccessLocal'] = AbonentCountSuccessLocal
        context['totalSuccesCallsLocal'] = totalSuccesCallsLocal
        context['totalMtBruttoSuccessLocal'] = totalMtBruttoSuccessLocal
        context['totalSuccessPriceBruttoLocal'] = totalSuccessPriceBruttoLocal

        umumyAbonentCountSuccessGlobal = AbonentCountSuccessGlobal + AbonentCountSuccessLocal
        umumyTotalSuccesCallsGlobal = totalSuccesCallsGlobal + totalSuccesCallsLocal
        umumyTotalMtSuccessGlobal = totalMtSuccessGlobal + totalMtBruttoSuccessLocal
        umumyTotalSuccessPriceGlobal = totalSuccessPriceGlobal + totalSuccessPriceBruttoLocal

        context['umumyAbonentCountSuccessGlobal'] = umumyAbonentCountSuccessGlobal
        context['umumyTotalSuccesCallsGlobal'] = umumyTotalSuccesCallsGlobal
        context['umumyTotalMtSuccessGlobal'] = umumyTotalMtSuccessGlobal
        context['umumyTotalSuccessPriceGlobal'] = umumyTotalSuccessPriceGlobal


   
        


    

        if request.method != 'POST':
            messages.success(request, 'Проверено')
    # ##########################
    # Если нажал на Начислить ##
    #  #########################
    if request.method == 'POST' and 'comment' in request.POST:
        if not request.POST.get('comment'):
            messages.error(request, f'Ошибка! Оставьте Комментарий')
        else:
            alreadyNachDbfName = []
            for name in getNameList:
                dbfName = dbfNameList.objects.get(name=name)
                if dbfName.is_nach == True:
                    alreadyNachDbfName.append(dbfName.name)
            if alreadyNachDbfName:
                messages.error(request, f'Ошибка! Уже начисленный файл: {alreadyNachDbfName}')
            else:  
                bulk_update_nach = []
                bulk_create_nach = []
                nachCountLocal = 0
                bulk_update_user = []
                existing_users = set()
                nachs_update = {} # {f"{user.pk}{year}{month}": nach_obj}
                nachs_create = {} # {f"{user.pk}{year}{month}": nach_obj}
                for year, values in etrapNumberMT.items():
                    for month, value in values.items():
                        for etrap, val in value.items():
                            for number, MT in val.items():
                                nachCountLocal += 1
                                if nachCountLocal == 1:
                                    logger.info(f"Идет процесс начисления сверхлимита...")
                                user = users.get(pk=number_pk[f"{number}{etrap}"])
                                price = MT * 0.0006
                                if user.pk not in existing_users:
                                    user.b_slr -= price
                                    bulk_update_user.append(user) 
                                    existing_users.add(user.pk)
                                else:
                                    existing_user = next((u for u in bulk_update_user if u.pk == user.pk), None)
                                    if existing_user:
                                        existing_user.b_slr -= price
                                    ## for existing_user in bulk_update_user:
                                    ##     if existing_user.pk == user.pk:
                                    ##         existing_user.b_slr -= price
                                    ##         break
                                nach = nachs_update.get(f"{user.pk}{year}{month}")
                                if nach:
                                    nach.slr += price
                                else:
                                    try:
                                        nach = NachMinus.objects.get(user=user, year=year, month=month)
                                        nach.slr += price
                                        nachs_update[f"{user.pk}{year}{month}"] = nach
                                    except:
                                        nach = nachs_create.get(f"{user.pk}{year}{month}")
                                        if nach:
                                            nach.slr += price
                                        else:
                                            nach = NachMinus(user=user, year=year, month=month, slr=price)
                                            nachs_create[f"{user.pk}{year}{month}"] = nach
                logger.info(f"Начисление сверхлимита завершено, количество начислений: {nachCountLocal}")
                nachCountGlobal = 0
                for year, values in my_dict_global.items():
                    for month, value in values.items():
                        for etrap, val in value.items():
                            for number, v in val.items():
                                nachCountGlobal += 1
                                if nachCountGlobal == 1:
                                    logger.info(f"Идет процесс начисления по АМТС8...")

                                kod = v
                                
                                user = users.get(pk=number_pk[f"{number}{etrap}"])
                                if user.pk not in existing_users:
                                    user.b_kod -= kod
                                    bulk_update_user.append(user) 
                                    existing_users.add(user.pk)
                                else:
                                    existing_user = next((u for u in bulk_update_user if u.pk == user.pk), None)
                                    if existing_user:
                                        existing_user.b_kod -= kod

                                nach = nachs_update.get(f"{user.pk}{year}{month}")
                                if nach:
                                    nach.kod += kod
                                else:
                                    try:
                                        nach = NachMinus.objects.get(user=user, year=year, month=month)
                                        nach.kod += kod
                                        nachs_update[f"{user.pk}{year}{month}"] = nach
                                    except:
                                        nach = nachs_create.get(f"{user.pk}{year}{month}")
                                        if nach:
                                            nach.kod += kod
                                        else:
                                            nach = NachMinus(user=user, year=year, month=month, kod=kod)
                                            nachs_create[f"{user.pk}{year}{month}"] = nach
        
                logger.info(f"Начисления по АМТС8 завершено, кол-во начислений {nachCountGlobal}")
                bulk_update_nach = []
                bulk_create_nach = []
                for key, obj in nachs_update.items():
                    bulk_update_nach.append(obj)
                for key, obj in nachs_create.items():
                    bulk_create_nach.append(obj)
                try:
                    with transaction.atomic():
                        if bulk_update_user:
                            UserTable.objects.bulk_update(bulk_update_user, ['b_slr', 'b_kod'], batch_size=1000)
                        if bulk_update_nach:
                            NachMinus.objects.bulk_update(bulk_update_nach, ['kod', 'slr'], batch_size=1000)
                        if bulk_create_nach:
                            NachMinus.objects.bulk_create(bulk_create_nach, batch_size=1000)

                        listNameMes = []
                        for name in getNameList:
                            listNameMes.append(name)
                        dbfNameList.objects.filter(name__in=getNameList).update(is_nach=True)
                        logger.info('Готово')
                        StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')}\n\n\n начисления файлов {getNameList}", action='Начисления КОД+СЛР')
                        UserTable.objects.filter(is_enterprises=True).update(b_telefon=0, b_slr=0, b_kod=0, b_zakaz=0, b_prochee=0, b_dop_uslugi=0, b_internet=0, b_alem=0)
                        messages.success(request, f'Успешное Начисления {listNameMes}')
                except Exception as e:
                    logger.error(f'Ошибка при записи в БД (откат начислений), тип ошибки == {str(e)}', exc_info=True)
                    messages.error(request, f'Ошибка при записи в БД (откат начислений), тип ошибки == {str(e)}')



    if request.method == 'POST' and 'downloadKodLists' in request.POST:

        headers = ("Year","Month","Etrap","Number","Price")
        data = []
        data = tablib.Dataset(*data, headers=headers)




        for year, values in my_dict_global.items():
            for month, value in values.items():
                for etrap, val in value.items():
                    for number, price in val.items():
                        data.append((year, month, etrap, number, price))

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= Kod_price.xlsx"
        return response
    



    if request.method == 'POST' and 'downloadSlrLists' in request.POST:

        headers = ("Year","Month","Etrap","Number","MT", "Price")
        data = []
        data = tablib.Dataset(*data, headers=headers)




        for year, values in etrapNumberMT.items():
            for month, value in values.items():
                for etrap, val in value.items():
                    for number, MT in val.items():
                        data.append((year, month, etrap, number, MT, MT * 0.0006))

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= Slr_price.xlsx"
        return response

    return render(request, 'telekom/MATB/DBF/kodSlrFileNachisleniya.html', context)

    









# Код работает идеально но без transaction
    # from django.shortcuts import render, redirect
    # from django.contrib import messages


    # from datetime import datetime
    # from datetime import date
    # from calendar import monthrange

    # from telekom.models import DontRepeatYourself, LocalCall, NachMinus, NachisleniyaOtchet, NonLocalCall, StaffAction, UserTable, dbfNameList
    # from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert
    # import sys
    # from bulk_update.helper import bulk_update

    # from django.http import HttpResponse
    # import tablib




    # def kodSlrFileNachisleniya(request):
    #     EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    #     if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
    #         pass
    #     else:
    #         messages.error(request, f'Доступ только соотрудникам MATB')
    #         return redirect('user-login')
        
    #     context = {}
    #     current_date = date.today()
    #     current_date = str(current_date)
    #     context['current_date'] = current_date

    #     if request.GET.get('month') == '':
    #         return redirect('kod-slr-file-nachisleniya')

    #     # if request.GET.get('month') == '':
    #     #     return redirect('slr-nachisleniya')

    #     context['matbIndex'] = True
    #     context['kodSlrFileNachisleniya'] = True

    #     dbf_name_lists = dbfNameList.objects.all().order_by('-pk')
    #     context["dbf_name_lists"] = dbf_name_lists

    #     getNameList = request.GET.getlist('getNameList')
    #     context['getNameList'] = getNameList

    #     context['get_month'] = request.GET.get('month')
    #     context['get_year'] = request.GET.get('year')

    #     usersNumEtrap = UserTable.objects.values('number', 'etrap')
    #     # ['20000Dashoguz', '20000Akdepe'] список из numberetrap которые есть в нашей БД
    #     usersNumEtrList = {}
    #     for dict_ in usersNumEtrap:
    #         for key, val in dict_.items():
    #             if key == 'number':
    #                 word = val
    #             if key == 'etrap':
    #                 word += val
    #         usersNumEtrList[word] = True
        
    #     if getNameList:
    #         users = UserTable.objects.all()
    #         number_pk = {} # {numberEtrap: pk}
    #         for user in users:
    #             number = user.number
    #             etrap = user.etrap
    #             number_pk[f"{number}{etrap}"] = user.pk

    #         nach_year_month_number_pk = {} # {yearMonth: {etrapNumber: nachPk}}
    #         countNach = 0
    #         for name in getNameList:
    #             countNach += 1
    #             print(f'Проверка файлов {countNach} из {len(getNameList)}')
    #             globalCall = NonLocalCall.objects.filter(file_name = name)
    #             for call in globalCall:
    #                 etrap = call.SUB_A_etrap
    #                 date_ = str(call.DATE)
    #                 year = date_[:4]
    #                 month = date_[5:7]
    #                 number = call.SUB_A
    #                 if f"{year}{month}" not in nach_year_month_number_pk:
    #                     nach_pk = {}
    #                     for n in NachMinus.objects.filter(year=year, month=month):
    #                         nach_pk[f"{n.user.etrap}{n.user.number}"] = n.pk
    #                     nach_year_month_number_pk[f"{year}{month}"] = nach_pk
        
            
    #         my_dict_global = {} #{year: {month: {etrap: {number: [kod, prochee]}}}}
    #         my_dict_local = {} # {year: {month: {etrap: {day: {number: MT }}}}}

    #         totalKodPriceEdara = 0
    #         totalKodPriceIlat = 0



        

    #         dbfYearMonth = []
    #         dbf_count = 0

    #         AbonentCountSuccessGlobal = 0
    #         totalSuccesCallsGlobal = 0
    #         totalMtSuccessGlobal = 0
    #         totalSuccessPriceGlobal = 0

    #         AbonentCountSuccessLocal = 0
    #         totalSuccesCallsLocal = 0
    #         totalMtBruttoSuccessLocal = 0
    #         totalSuccessPriceBruttoLocal = 0
            
    #         # for name in getNameList:
    #         #     # Проверка нет ли повторных разговоров (дубликатов)
    #         #     values_pk = {} # {f"SUB_A_etrap, SUB_A, SUB_B_locations, SUB_B, price, DATE, START, FIN, DUR, MT": pk}
    #         #     count = 0
    #         #     delete_pks = []
    #         #     global_ = NonLocalCall.objects.exclude(file_name=name)
    #         #     for c in global_:
    #         #         pk = c.pk
    #         #         SUB_A_etrap = str(c.SUB_A_etrap)
    #         #         SUB_A = str(c.SUB_A)
    #         #         SUB_B_locations = str(c.SUB_B_locations)
    #         #         SUB_B = str(c.SUB_B)
    #         #         price = str(c.price)
    #         #         DATE = str(c.DATE)
    #         #         START = str(c.START)
    #         #         FIN = str(c.FIN)
    #         #         DUR = str(c.DUR)
    #         #         MT = str(c.MT)
    #         #         file_name = str(c.file_name)

    #         #         if f"{SUB_A_etrap}{SUB_A}{SUB_B_locations}{SUB_B}{price}{DATE}{START}{FIN}{DUR}{MT}" not in values_pk:
    #         #             values_pk[f"{SUB_A_etrap}{SUB_A}{SUB_B_locations}{SUB_B}{price}{DATE}{START}{FIN}{DUR}{MT}"] = c.pk
    #         #         else:
    #         #             count += 1
    #         #             delete_pks.append(c.pk)
    #         #             print(count)
    #         #     print('global_', len(global_))
    #         #     # print('values_pk', len(values_pk))
    #         #     delCount = 0
    #         #     # for p in delete_pks:
    #         #     #     delCount += 1
    #         #     #     print('delCount', delCount)
    #         #     #     NonLocalCall.objects.get(pk=p).delete()
            

    #         for name in getNameList: 
    #             dbf_count += 1
    #             print(f'Подготовка файлов {dbf_count} из {len(getNameList)}')
    #             # global
    #             globalCall = NonLocalCall.objects.filter(file_name = name)
    #             for call in globalCall:

                    
                    
    #                 totalSuccesCallsGlobal += 1
    #                 price = float(call.price)
    #                 MT = int(call.MT)
    #                 totalMtSuccessGlobal += MT
    #                 total_price = price * MT
    #                 totalSuccessPriceGlobal += total_price
    #                 hb = call.edara
    #                 number = call.SUB_A
    #                 etrap = call.SUB_A_etrap
    #                 etrap_B = call.SUB_B_locations
    #                 date_ = str(call.DATE)


    #                 # nach_year_months               
                    

    #                 year = date_[:4]
    #                 month = date_[5:7]

    #                 if date_ not in dbfYearMonth:
    #                     dbfYearMonth.append(date_)

    #                 # if f"{monthСonvert(month)} {year}" not in dbfYearMonth:
    #                 #     dbfYearMonth.append(f"{monthСonvert(month)} {year}")

    #                 # Работающий код с прочее для ILAT
    #                 # user = users.get(pk=number_pk[f"{number}{etrap}"])
    #                 # b_prochee = user.b_prochee
    #                 # prochee = 0
    #                 if hb == 'H':
    #                     totalKodPriceEdara += total_price
    #                     # if b_prochee <=0: 
    #                     #     # prochee = total_price * 0.1
    #                     #     prochee = 0
    #                     #     totalProcheePriceHoz += prochee
    #                 elif hb == 'I' or hb == 'E':
    #                     totalKodPriceIlat += total_price
    #                     # if b_prochee <=0:
    #                     #     prochee = total_price * 0.05  
    #                     #     totalProcheePriceIlat += prochee
    #                 elif hb == 'B':
    #                     totalKodPriceEdara += total_price
    #                 # if year not in my_dict_global:
    #                 #     my_dict_global[year] = {month: {etrap: {number: [total_price, prochee]}}}
    #                 # elif month not in my_dict_global[year]:
    #                 #     my_dict_global[year][month] = {etrap: {number: [total_price, prochee]}}
    #                 # elif etrap not in my_dict_global[year][month]:
    #                 #     my_dict_global[year][month][etrap] = {number: [total_price, prochee]}
    #                 # elif number not in my_dict_global[year][month][etrap]:
    #                 #     my_dict_global[year][month][etrap][number] = [total_price, prochee]
    #                 # else:
    #                 #     my_dict_global[year][month][etrap][number][0] += total_price
    #                 #     my_dict_global[year][month][etrap][number][1] += prochee

    #                 if year not in my_dict_global:
    #                     my_dict_global[year] = {month: {etrap: {number: total_price}}}
    #                 elif month not in my_dict_global[year]:
    #                     my_dict_global[year][month] = {etrap: {number: total_price}}
    #                 elif etrap not in my_dict_global[year][month]:
    #                     my_dict_global[year][month][etrap] = {number: total_price}
    #                 elif number not in my_dict_global[year][month][etrap]:
    #                     my_dict_global[year][month][etrap][number] = total_price
    #                     AbonentCountSuccessGlobal += 1
    #                 else:
    #                     my_dict_global[year][month][etrap][number] += total_price

                
                

    #             # local
    #             localCalls = LocalCall.objects.filter(file_name = name).exclude(edara='B')
    #             for call in localCalls:
    #                 totalSuccesCallsLocal += 1
    #                 number = call.SUB_A
    #                 date_ = str(call.DATE)
    #                 MT = int(call.MT)
    #                 etrap = call.etrap
    #                 year = date_[:4]
    #                 month = date_[5:7]
    #                 day_ = date_[-2:]
    #                 if year not in my_dict_local:
    #                     my_dict_local[year] = {month: {etrap: {day_: {number: MT}}}}
    #                 elif month not in my_dict_local[year]:
    #                     my_dict_local[year][month] = {etrap: {day_: {number: MT}}}
    #                 elif etrap not in my_dict_local[year][month]:
    #                     my_dict_local[year][month][etrap] = {day_: {number: MT}}
    #                 elif day_ not in my_dict_local[year][month][etrap]:
    #                     my_dict_local[year][month][etrap][day_] = {number: MT}
    #                 elif number not in my_dict_local[year][month][etrap][day_]:
    #                     my_dict_local[year][month][etrap][day_][number] = MT
    #                 else:
    #                     my_dict_local[year][month][etrap][day_][number] += MT


    #         local_c = my_dict_local.copy()
    #         for year, values in local_c.items():
    #             values_c = values.copy()
    #             for month, value in values_c.items():
    #                 value_c = value.copy()
    #                 for etrap, val in value_c.items():
    #                     val_c = val.copy()
    #                     for day_, v in val_c.items():
    #                         v_c = v.copy()
    #                         for number, MT in v_c.items():
    #                             if MT <= 5:
    #                                 del my_dict_local[year][month][etrap][day_][number]
    #                                 if my_dict_local[year][month][etrap][day_] == {}:
    #                                     del my_dict_local[year][month][etrap][day_]
    #                                 if my_dict_local[year][month][etrap] == {}:
    #                                     del my_dict_local[year][month][etrap]
    #                                 if my_dict_local[year][month] == {}:
    #                                     del my_dict_local[year][month]
    #                                 if my_dict_local[year] == {}:
    #                                     del my_dict_local[year]
    #                             else:
    #                                 continue
    #         etrapNumberMT = {} # {year: {month: {etrap: {number: MT}}}}
    #         for year, values in my_dict_local.items():
    #             for month, value in values.items():
    #                 for etrap, val in value.items():
    #                     for day_, v in val.items():
    #                         for number, MT in v.items():

    #                             if year not in etrapNumberMT:
    #                                 etrapNumberMT[year] = {month: {etrap: {number: MT - 5}}}
    #                             elif month not in etrapNumberMT[year]:
    #                                 etrapNumberMT[year][month] = {etrap: {number: MT - 5}}
    #                             elif etrap not in etrapNumberMT[year][month]:
    #                                 etrapNumberMT[year][month][etrap] = {number:MT-5}
    #                             elif number not in  etrapNumberMT[year][month][etrap]:
    #                                 etrapNumberMT[year][month][etrap][number] = MT-5
    #                                 AbonentCountSuccessLocal += 1
    #                             else:
    #                                 etrapNumberMT[year][month][etrap][number] += MT-5
                                    
    #                             price = (MT - 5) * 0.0006
    #                             totalSuccessPriceBruttoLocal += price
    #                             totalMtBruttoSuccessLocal += (MT - 5)
                        
        
    #         context['totalKodPriceEdara'] = totalKodPriceEdara
    #         context['totalKodPriceIlat'] = totalKodPriceIlat
    #         context['dbfYearMonth'] = dbfYearMonth

    #         context['AbonentCountSuccessGlobal'] = AbonentCountSuccessGlobal
    #         context['totalSuccesCallsGlobal'] = totalSuccesCallsGlobal
    #         context['totalMtSuccessGlobal'] = totalMtSuccessGlobal
    #         context['totalSuccessPriceGlobal'] = totalSuccessPriceGlobal

    #         context['AbonentCountSuccessLocal'] = AbonentCountSuccessLocal
    #         context['totalSuccesCallsLocal'] = totalSuccesCallsLocal
    #         context['totalMtBruttoSuccessLocal'] = totalMtBruttoSuccessLocal
    #         context['totalSuccessPriceBruttoLocal'] = totalSuccessPriceBruttoLocal

    #         umumyAbonentCountSuccessGlobal = AbonentCountSuccessGlobal + AbonentCountSuccessLocal
    #         umumyTotalSuccesCallsGlobal = totalSuccesCallsGlobal + totalSuccesCallsLocal
    #         umumyTotalMtSuccessGlobal = totalMtSuccessGlobal + totalMtBruttoSuccessLocal
    #         umumyTotalSuccessPriceGlobal = totalSuccessPriceGlobal + totalSuccessPriceBruttoLocal

    #         context['umumyAbonentCountSuccessGlobal'] = umumyAbonentCountSuccessGlobal
    #         context['umumyTotalSuccesCallsGlobal'] = umumyTotalSuccesCallsGlobal
    #         context['umumyTotalMtSuccessGlobal'] = umumyTotalMtSuccessGlobal
    #         context['umumyTotalSuccessPriceGlobal'] = umumyTotalSuccessPriceGlobal


    
            


        

    #         if request.method != 'POST':
    #             messages.success(request, 'Проверено')
    #     # ##########################
    #     # Если нажал на Начислить ##
    #     #  #########################
    #     if request.method == 'POST' and 'comment' in request.POST:
    #         if request.POST.get('comment') == '':
    #             messages.error(request, f'Ошибка! Оставьте Комментарий')
    #         else:
    #             alreadyNachDbfName = []

    #             for name in getNameList:
    #                 dbfName = dbfNameList.objects.get(name=name)
    #                 if dbfName.is_nach == True:
    #                     alreadyNachDbfName.append(dbfName.name)

    #             if alreadyNachDbfName:
    #                 messages.error(request, f'Ошибка! Уже начисленный файл: {alreadyNachDbfName}')
    #             else:
    #                 # #####################
    #                 # Начисления для slr ##
    #                 #  ####################
                    
    #                 bulk_update_nach_loc = []
    #                 bulk_create_nach_loc = []
    #                 nachCountLocal = 0
    #                 for year, values in etrapNumberMT.items():
    #                     for month, value in values.items():
    #                         bulk_update_user_loc = []
    #                         for etrap, val in value.items():
    #                             for number, MT in val.items():
    #                                 nachCountLocal += 1
    #                                 print(f"Идет процесс начисления сверхлимита...", nachCountLocal)
    #                                 user = users.get(pk=number_pk[f"{number}{etrap}"])
    #                                 price = MT * 0.0006
    #                                 user.b_slr -= price
    #                                 try:
    #                                     nach = NachMinus.objects.get(user=user, year=year, month = month)
    #                                     nach.slr += price
    #                                     bulk_update_nach_loc.append(nach)
    #                                 except:
    #                                     nach = NachMinus(user=user, year=year, month=month, slr=price)
    #                                     bulk_create_nach_loc.append(nach)
    #                                 bulk_update_user_loc.append(user)
    #                         if bulk_update_user_loc:
    #                             UserTable.objects.bulk_update(bulk_update_user_loc, ['b_slr'])
    #                 if bulk_update_nach_loc:
    #                     NachMinus.objects.bulk_update(bulk_update_nach_loc, ['slr'])
    #                 if bulk_create_nach_loc:
    #                     NachMinus.objects.bulk_create(bulk_create_nach_loc)    
                                        
    #                 # #########################
    #                 # Начисления для slr END ##
    #                 #  ########################                    
    #                 # #####################
    #                 # Начисления для kod ##
    #                 #  ####################
                        
    #                 ####### Работающий код с прочее для ILAT
    #                 # bulk_update_user = []
    #                 # bulk_update_nach = []
    #                 # bulk_create_nach = []
    #                 # nachCountGlobal = 0
    #                 # for year, values in my_dict_global.items():
    #                 #     for month, value in values.items():
    #                 #         for etrap, val in value.items():
    #                 #             for number, v in val.items():
    #                 #                 print(f"Идет процесс начисления по АМТС8...", nachCountGlobal)
    #                 #                 nachCountGlobal += 1
    #                 #                 kod = v[0]
    #                 #                 prochee = v[1]
    #                 #                 user = users.get(pk=number_pk[f"{number}{etrap}"])
    #                 #                 user.b_kod -= kod
    #                 #                 user.b_prochee -= prochee
    #                 #                 try:
    #                 #                     nach = NachMinus.objects.get(user=user, year=year, month=month)
    #                 #                     nach.kod += kod
    #                 #                     nach.prochee += prochee
    #                 #                     bulk_update_nach.append(nach)
    #                 #                 except:
    #                 #                     nach = NachMinus(user=user, year=year, month=month, kod=kod, prochee=prochee)
    #                 #                     bulk_create_nach.append(nach)
    #                 #                 bulk_update_user.append(user)
    #                 # if bulk_update_user:
    #                 #     UserTable.objects.bulk_update(bulk_update_user, ['b_kod', 'b_prochee'])
    #                 # if bulk_update_nach:
    #                 #     NachMinus.objects.bulk_update(bulk_update_nach, ['kod', 'prochee'])
    #                 # if bulk_create_nach:
    #                 #######    NachMinus.objects.bulk_create(bulk_create_nach) 

                    
    #                 bulk_update_nach = []
    #                 bulk_create_nach = []
    #                 nachCountGlobal = 0
    #                 for year, values in my_dict_global.items():
    #                     for month, value in values.items():
    #                         bulk_update_user = []
    #                         for etrap, val in value.items():
    #                             for number, v in val.items():
    #                                 if number == '50356' or number == 50356:
    #                                     print('50356',v)
    #                                 print(f"Идет процесс начисления по АМТС8...", nachCountGlobal)
    #                                 nachCountGlobal += 1
    #                                 kod = v
    #                                 user = users.get(pk=number_pk[f"{number}{etrap}"])
    #                                 user.b_kod -= kod
    #                                 try:
    #                                     nach = NachMinus.objects.get(user=user, year=year, month=month)
    #                                     nach.kod += kod
    #                                     bulk_update_nach.append(nach)
    #                                 except:
    #                                     nach = NachMinus(user=user, year=year, month=month, kod=kod)
    #                                     bulk_create_nach.append(nach)
    #                                 bulk_update_user.append(user) 
    #                         if bulk_update_user:
    #                             UserTable.objects.bulk_update(bulk_update_user, ['b_kod'])
    #                 if bulk_update_nach:
    #                     NachMinus.objects.bulk_update(bulk_update_nach, ['kod'])
    #                 if bulk_create_nach:
    #                     NachMinus.objects.bulk_create(bulk_create_nach)
    #                 # #########################
    #                 # Начисления для kod END ##
    #                 #  ########################
                                    
                            
                    
    #                 # Открыть объязательно этот коммент
    #                 listNameMes = []
    #                 for name in getNameList:
    #                     dbfNameList.objects.filter(name=name).update(is_nach=True)
    #                     listNameMes.append(name)
    #                 messages.success(request, f'Успешное Начисления {listNameMes}')
    #                 print('Готово')
    #                 StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')}\n\n\n начисления файлов {getNameList}", action='Начисления КОД+СЛР')


    #     if request.method == 'POST' and 'downloadKodLists' in request.POST:

    #         headers = ("Year","Month","Etrap","Number","Price")
    #         data = []
    #         data = tablib.Dataset(*data, headers=headers)




    #         for year, values in my_dict_global.items():
    #             for month, value in values.items():
    #                 for etrap, val in value.items():
    #                     for number, price in val.items():
    #                         data.append((year, month, etrap, number, price))

    #         response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
    #         response['Content-Disposition'] = f"attachment; filename= Kod_price.xlsx"
    #         return response
        



    #     if request.method == 'POST' and 'downloadSlrLists' in request.POST:

    #         headers = ("Year","Month","Etrap","Number","MT", "Price")
    #         data = []
    #         data = tablib.Dataset(*data, headers=headers)




    #         for year, values in etrapNumberMT.items():
    #             for month, value in values.items():
    #                 for etrap, val in value.items():
    #                     for number, MT in val.items():
    #                         data.append((year, month, etrap, number, MT, MT * 0.0006))

    #         response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
    #         response['Content-Disposition'] = f"attachment; filename= Slr_price.xlsx"
    #         return response

    #     return render(request, 'telekom/MATB/DBF/kodSlrFileNachisleniya.html', context)

# Код работает идеально но без transaction

    


