from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from telekom.models import *
from django.db.models import Prefetch
from django.db.models import Sum, F, Q
import tablib
from tablib import Dataset
from datetime import datetime, date
from django.http import HttpResponse

import urllib.parse

from django.db import transaction
import logging
logger = logging.getLogger(__name__)



def add_nachisleniya_from_excel(request):
    context = {}
    if not request.user.is_superuser and not request.user.username == 'admin1':
        return redirect('HomePage')
    
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['etraps'] = etraps

    context['add_nachisleniya_from_excel'] = True 
    context['admin_allow'] = True 

    current_date = datetime.now().date()
    formatted_date = current_date.strftime('%Y-%m-%d')
    current_year, current_month, current_day = formatted_date.split('-')

    context['formatted_date'] = formatted_date
    context['current_month'] = current_month
    context['current_year'] = current_year


    if request.method == 'POST':
        etrap = request.POST.get('etrap')
        column = request.POST.get('type')
        month = request.POST.get('month')
        year = request.POST.get('year')
        file = request.FILES.get('file')
        comment = request.POST.get('comment')
        action = request.POST.get('action')
        download_excel = request.POST.get('download_excel')

        ic(etrap, column, month, year, comment, action)

        context['selected_etrap'] = etrap
        context['column'] = column
        context['choosed_month'] = month
        context['choosed_year'] = year
        context['comment'] = comment
        context['action'] = action
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        if 'saldo' in column:
            if not etrap or not year or not file:
                messages.error(request, f'Заполните все поля')
                return render(request, 'telekom/admin_pages/add_nachisleniya_from_excel.html', context)
            saldo, row_column = column.split('_')
            correct_column = f"s_{row_column}"
            ic(saldo, correct_column)
            dataset = Dataset()
            xlsx_data = request.FILES['file']
            file_name = xlsx_data.name[:2]
            imported_data = dataset.load(xlsx_data.read(), format='xlsx')

            
            if year == current_year:
                users = UserTable.objects.filter(etrap=etrap)
            else:
                users = SaldoBalancePoGodam.objects.filter(etrap=etrap, year=year)

            if users:
                dict_num_saldo = {} # {num: [saldo_from_users, saldo_from_excel]}
                for u in users:
                    num = int(u.number)
                    if num not in dict_num_saldo:
                        dict_num_saldo[num] = [getattr(u, correct_column) or 0, 0]
                    else:
                        messages.error(request, f'Обнаружены повторяющиеся номера ({num}) в таблице SaldoBalancePoGodam/UserTable! Проверьте данные.')
                        return render(request, 'telekom/admin_pages/add_nachisleniya_from_excel.html', context)
                    
                for d in dataset:
                    number = d[0]
                    price = float(d[1])
                    if number in dict_num_saldo:
                        dict_num_saldo[number][1] = price
                dict2 = {}
            
                for num, (saldo_from_users, saldo_from_excel) in dict_num_saldo.items():
                        if saldo_from_users != saldo_from_excel:
                            dict2[num] = [saldo_from_users, saldo_from_excel]
                context['dict2'] = dict2
                # ic(dict2)
            

                
                if action == 'nachislit':
                    bulk_update = []
                    for u in users:
                        num = int(u.number)
                        if num in dict2:
                            setattr(u, correct_column, dict2[num][1])
                            bulk_update.append(u)
                    
                    try:
                        with transaction.atomic():
                            if bulk_update:
                                if year == current_year:
                                    # esli UserTable
                                    # if correct_column == 'prochee':
                                    #     UserTable.objects.filter(etrap=etrap).update(s_telefon=0, s_slr=0, s_kod=0, s_zakaz=0, s_dop_uslugi=0, s_prochee=0)
                                    # else:
                                    #     UserTable.objects.filter(etrap=etrap).update(**{correct_column: 0})
                                    UserTable.objects.bulk_update(bulk_update, [correct_column])
                                else:
                                    # esli SaldoBalancePoGodam
                                    # if correct_column == 'prochee':
                                    #     SaldoBalancePoGodam.objects.filter(etrap=etrap, year=year).update(s_telefon=0, s_slr=0, s_kod=0, s_zakaz=0, s_dop_uslugi=0, s_prochee=0)
                                    # else:
                                    #     SaldoBalancePoGodam.objects.filter(etrap=etrap, year=year).update(**{correct_column: 0})
                                    SaldoBalancePoGodam.objects.bulk_update(bulk_update, [correct_column])
                            else:
                                messages.warning(request, "Нет данных для обновления")
                                return
                            messages.success(request, f'success')  
                    except Exception as e:
                        messages.error(request, f"Ошибка при обновлении {correct_column} для etrap={etrap}, year={year}: {e}")
                        logger.error(f"====== Ошибка при обновлении {correct_column} для etrap={etrap}, year={year}: {e}")
                        
            

                if action == 'check':
                    if dict2:
                        messages.success(request, 'Проверено')
                    else:
                        messages.success(request, '+ Все данные верифицированы, расхождений нет')
                if action == 'download':
                    headers = ("number", "saldo_from_users", "saldo_from_excel")
                    data = []
                    data = tablib.Dataset(*data, headers=headers)
                    for num, (saldo_from_users, saldo_from_excel) in dict_num_saldo.items():
                        if saldo_from_users != saldo_from_excel:
                            data.append((num, saldo_from_users, saldo_from_excel))

                    
                    filename = f"Несовпадения saldo excel и БД за {year} для {correct_column} {etrap}.xlsx"
                    encoded_filename = urllib.parse.quote(filename.encode('utf-8'))
                    
                    response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
                    response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
                    return response 
             
            else:
                messages.error(request, f'❌ Для {year} года не создана таблица SaldoBalancePoGodam!')
                return render(request, 'telekom/admin_pages/add_nachisleniya_from_excel.html', context)
        
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        
        elif 'balance' in column:
            if not etrap or not year or not file or not month:
                messages.error(request, f'Заполните все поля')
                return render(request, 'telekom/admin_pages/add_nachisleniya_from_excel.html', context)
            saldo, row_column = column.split('_')
            correct_column = f"b_{row_column}"
            dataset = Dataset()
            xlsx_data = request.FILES['file']
            file_name = xlsx_data.name[:2]
            imported_data = dataset.load(xlsx_data.read(), format='xlsx')

            
            start_date = date(int(year), int(month), 1)
            pays = PayHistory.objects.filter(abonent__etrap=etrap, date__gte=start_date).prefetch_related('abonent')
            number_pays = {}
            for p in pays:
                num = int(p.abonent.number)
                price = getattr(p, row_column) or 0
                if num not in number_pays:
                    number_pays[num] = price
                else:
                    number_pays[num] += price

            if year == current_year:
                users = UserTable.objects.filter(etrap=etrap)
            else:
                users = SaldoBalancePoGodam.objects.filter(etrap=etrap, year=year)

            if users:
                dict_num_balance = {} # {num: [saldo_from_users, saldo_from_excel]}
                for u in users:
                    num = int(u.number)
                    if num not in dict_num_balance:
                        dict_num_balance[num] = [getattr(u, correct_column), 0]
                    else:
                        messages.error(request, f'Обнаружены повторяющиеся номера ({num}) в таблице SaldoBalancePoGodam/UserTable! Проверьте данные.')
                        return render(request, 'telekom/admin_pages/add_nachisleniya_from_excel.html', context)
                    
                for d in dataset:
                    number = int(d[0])
                    price = float(d[1])

                    if year == current_year:
                        correct_price = 0
                        if number in number_pays:
                            correct_price = price + number_pays[number]
                    else:
                        correct_price = price
                    if number in dict_num_balance:
                        dict_num_balance[number][1] = correct_price
            
                dict2 = {}
                for num, (balance_from_users, balance_from_excel) in dict_num_balance.items():
                        if balance_from_users != balance_from_excel:
                            dict2[num] = [balance_from_users, balance_from_excel]
                context['dict2'] = dict2
            

                
                if action == 'nachislit':
                    bulk_update = []
                    for u in users:
                        num = int(u.number)
                        if num in dict2:
                            setattr(u, correct_column, dict2[num][1])
                            bulk_update.append(u)
                    
                    try:
                        with transaction.atomic():
                            if bulk_update:
                                if year == current_year:
                                    UserTable.objects.bulk_update(bulk_update, [correct_column])
                                else:
                                    SaldoBalancePoGodam.objects.bulk_update(bulk_update, [correct_column])
                            else:
                                messages.error(request, "Нет данных для обновления")
                                return
                            messages.success(request, f'success')  
                    except Exception as e:
                        messages.error(request, f"Ошибка при обновлении {correct_column} для etrap={etrap}, year={year}: {e}")
                        logger.error(f"====== Ошибка при обновлении {correct_column} для etrap={etrap}, year={year}: {e}")
                        
            

                if action == 'check':
                    if dict2:
                        messages.success(request, 'Проверено')
                    else:
                        messages.success(request, '+ Все данные верифицированы, расхождений нет')
                if action == 'download':
                    headers = ("number", "balance_from_users", "balance_from_excel")
                    data = []
                    data = tablib.Dataset(*data, headers=headers)
                    for num, (balance_from_users, balance_from_excel) in dict_num_balance.items():
                        if balance_from_users != balance_from_excel:
                            data.append((num, balance_from_users, balance_from_excel))

                    
                    filename = f"Несовпадения balance excel и БД за {year} для {correct_column} {etrap}.xlsx"
                    encoded_filename = urllib.parse.quote(filename.encode('utf-8'))
                    
                    response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
                    response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
                    return response 
             
            else:
                messages.error(request, f'❌ Для {year} года не создана таблица SaldoBalancePoGodam!')
                return render(request, 'telekom/admin_pages/add_nachisleniya_from_excel.html', context) 


        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        
        elif 'ustanowka' in column:
            if not etrap or not year or not file or not month:
                messages.error(request, f'Заполните все поля')
                return render(request, 'telekom/admin_pages/add_nachisleniya_from_excel.html', context)
            saldo, row_column = column.split('_')
            correct_column = f"{row_column}"
            dataset = Dataset()
            xlsx_data = request.FILES['file']
            file_name = xlsx_data.name[:2]
            imported_data = dataset.load(xlsx_data.read(), format='xlsx')

            
            if year == current_year:
                users = UserTable.objects.filter(etrap=etrap)
            else:
                users = SaldoBalancePoGodam.objects.filter(etrap=etrap, year=year)

            if users:
                dict_telefon = {} # {num: [saldo_from_users, saldo_from_excel]}
                for u in users:
                    num = int(u.number)
                    if num not in dict_telefon:
                        if correct_column == 'abonplata':
                            if getattr(u, correct_column):
                                price = float(getattr(u, correct_column))
                            else:
                                price = 0
                        elif correct_column == 'service':
                            if u.service.all().exists():
                                price = 0
                                for s in u.service.all():
                                    price += s.price
                            else:
                                price = 0
                        dict_telefon[num] = [price, 0]
                    else:
                        messages.error(request, f'Обнаружены повторяющиеся номера ({num}) в таблице SaldoBalancePoGodam/UserTable! Проверьте данные.')
                        return render(request, 'telekom/admin_pages/add_nachisleniya_from_excel.html', context)
                    
                for d in dataset:
                    number = int(d[0])
                    abonplata = float(d[1])

                    if number in dict_telefon:
                        dict_telefon[number][1] = abonplata
                    else:
                        messages.error(request, f'W BD net номера ({number})! Проверьте данные.')
                        return render(request, 'telekom/admin_pages/add_nachisleniya_from_excel.html', context)

                dict2 = {}
                for num, (abonplata_or_service_users, abonplata_or_service_from_excel) in dict_telefon.items():
                        if abonplata_or_service_users != abonplata_or_service_from_excel:
                            dict2[num] = [abonplata_or_service_users, abonplata_or_service_from_excel]
                context['dict2'] = dict2

                if action == 'nachislit':
                    pass
                    # bulk_update = []
                    # for u in users:
                    #     num = int(u.number)
                    #     if num in dict2:
                    #         setattr(u, correct_column, dict2[num][1])
                    #         bulk_update.append(u)
                    
                    # try:
                    #     with transaction.atomic():
                    #         if bulk_update:
                    #             if year == current_year:
                    #                 UserTable.objects.bulk_update(bulk_update, [correct_column])
                    #             else:
                    #                 SaldoBalancePoGodam.objects.bulk_update(bulk_update, [correct_column])
                    #         else:
                    #             messages.error(request, "Нет данных для обновления")
                    #             return
                    #         messages.success(request, f'success')  
                    # except Exception as e:
                    #     messages.error(request, f"Ошибка при обновлении {correct_column} для etrap={etrap}, year={year}: {e}")
                    #     logger.error(f"====== Ошибка при обновлении {correct_column} для etrap={etrap}, year={year}: {e}")
                        
                if action == 'check':
                    if dict2:
                        messages.success(request, f'Проверено {column}')
                    else:
                        messages.success(request, f'+ Все данные верифицированы, расхождений нет {column}')
                
                if action == 'download':
                    headers = ("number", "abonplata_users", "abonplata_excel")
                    data = []
                    data = tablib.Dataset(*data, headers=headers)
                    for num, (abonplata_or_service_users, abonplata_or_service_from_excel) in dict_telefon.items():
                        if abonplata_or_service_users != abonplata_or_service_from_excel:
                            data.append((num, abonplata_or_service_users, abonplata_or_service_from_excel))
                    
                    filename = f"Несовпадения ustanowki excel и БД за {year} для {correct_column} {etrap}.xlsx"
                    encoded_filename = urllib.parse.quote(filename.encode('utf-8'))
                    
                    response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
                    response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
                    return response
            else:
                messages.error(request, f'❌ Для {year} года не создана таблица SaldoBalancePoGodam!')
                return render(request, 'telekom/admin_pages/add_nachisleniya_from_excel.html', context) 

        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################
        ######################################################################################################################################################################################

        else:
        
            if not etrap or not column or not month or not year or not file:
                messages.error(request, f'Заполните все поля')
                return render(request, 'telekom/admin_pages/add_nachisleniya_from_excel.html', context)

            dataset = Dataset()
            xlsx_data = request.FILES['file']
            file_name = xlsx_data.name[:2]
            imported_data = dataset.load(xlsx_data.read(), format='xlsx')

            
            nachs = NachMinus.objects.filter(year=year, month=month, user__etrap=etrap, **{f"{column}__gt": 0})

            dict_ = {} # {number: [nach_from_NachMinus, nach_from_excel] }

            total_excel = 0
            for d in dataset:
                number = d[0]
                price = float(d[1])
                if number not in dict_.items():
                    dict_[number] = [0, price]
                else:
                    dict_[number][1] = price
                total_excel += price

            total_nach = 0
            for n in nachs:
                num = int(n.user.number)
                dict_[num][0] = getattr(n, column)
                total_nach += getattr(n, column)

            
            
            
            ic(total_excel)
            ic(total_nach)
            ic(etrap, column, month, year, file, comment)

            # total_excel_test = 0
            # total_nach_test = 0
            # for num, (nach_from_NachMinus, nach_from_excel) in dict_.items():
            #     total_nach_test += nach_from_NachMinus
            #     total_excel_test += nach_from_excel
            # ic(total_excel_test)
            # ic(total_nach_test)

            dict2 = {}
            for num, (nach_from_NachMinus, nach_from_excel) in dict_.items():
                if nach_from_NachMinus != nach_from_excel:
                    dict2[num] = [nach_from_NachMinus, nach_from_excel]
            context['dict2'] = dict2

            if action == 'nachislit':
                dict_n = {}
                nachs = NachMinus.objects.filter(user__etrap=etrap, year=year, month=month).prefetch_related('user')
                for n in nachs:
                    num = int(n.user.number)
                    dict_n[num] = n
                users = UserTable.objects.filter(etrap=etrap)
                dict_users = {}
                for u in users:
                    num = int(u.number)
                    dict_users[num] = u
                bulk_update = []
                bulk_create = []
                for num, (nach_from_NachMinus, nach_from_excel) in dict_.items():
                    if nach_from_NachMinus != nach_from_excel:
                        if num in dict_n:
                            nach = dict_n[num]
                            setattr(nach, column, nach_from_excel)
                            bulk_update.append(nach)
                        else:
                            user = dict_users.get(num)
                            if user is None:
                                print(f"Пропуск: пользователь {num} не найден")
                                continue
                            nach = NachMinus(user=user, year=year, month=month, **{f"{column}": nach_from_excel})
                            bulk_create.append(nach)
                ic(column)
                try:
                    with transaction.atomic():
                        if bulk_create:
                            NachMinus.objects.bulk_create(bulk_create)
                            success_msg = f'Успешно создано {len(bulk_create)} новых записей'
                            logger.info(success_msg)
                        if bulk_update:
                            NachMinus.objects.bulk_update(bulk_update, [column])
                            success_msg = f'Успешно обновлено {len(bulk_update)} записей'
                            logger.info(success_msg)
                        if bulk_create or bulk_update:
                            final_msg = f'Начисления за {month}.{year} успешно применены. Создано: {len(bulk_create)}, обновлено: {len(bulk_update)}'
                            messages.success(request, final_msg)
                        else:
                            info_msg = 'Нет изменений для сохранения'
                            messages.info(request, info_msg)
                            logger.info(info_msg)
                except Exception as e:
                    error_msg = f'Ошибка сохранения начислений за {month}.{year}: {str(e)}'
                    logger.error(error_msg, exc_info=True)
                    messages.error(request, error_msg)

            if action == 'check':
                if dict2:
                    messages.success(request, 'Проверено')
                else:
                    messages.success(request, 'Проверено wse dannye sowpadayut')
            if action == 'download':
                headers = ("number", "nach_from_data_base", "nach_from_excel")
                data = []
                data = tablib.Dataset(*data, headers=headers)
                for num, (nach_from_NachMinus, nach_from_excel) in dict_.items():
                    if nach_from_NachMinus != nach_from_excel:
                        data.append((num, nach_from_NachMinus, nach_from_excel))

                
                filename = f"Несовпадения начислений excel и БД за {year}-{month} для {column} {etrap}.xlsx"
                encoded_filename = urllib.parse.quote(filename.encode('utf-8'))
                
                response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
                response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
                return response 
            
     
                        




    return render(request, 'telekom/admin_pages/add_nachisleniya_from_excel.html', context)