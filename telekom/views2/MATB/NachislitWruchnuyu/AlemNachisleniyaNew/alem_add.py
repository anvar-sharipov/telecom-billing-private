from django.shortcuts import render, redirect
from telekom.models import *
from django.db.models import Sum
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
import tablib

from datetime import date
from calendar import monthrange
from tablib import Dataset
from icecream import ic
from telekom.views2.myFunc.myFunc import monthСonvert

from datetime import datetime, date
import calendar
import re
from decimal import Decimal

from django.db import transaction
import logging
logger = logging.getLogger(__name__)

def alem_add(request):
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    months = [
        ('01', 'Январь'), ('02', 'Февраль'), ('03', 'Март'), ('04', 'Апрель'),
        ('05', 'Май'), ('06', 'Июнь'), ('07', 'Июль'), ('08', 'Август'),
        ('09', 'Сентябрь'), ('10', 'Октябрь'), ('11', 'Ноябрь'), ('12', 'Декабрь'),
    ]
    current_date = datetime.now()
    

    context = {
        'alem_add': True,
        'etraps': etraps,
        'month_choices': months,
        'current_year': current_date.year,
        'current_month': f"{current_date.month:02d}",
    }
    
    # AlemNachFileNames.objects.all().delete()
    # AlemNachData.objects.all().delete()
    # NachMinus.objects.all().update(alem=0)
    # UserTable.objects.all().update(b_telefon=0, b_slr=0, b_kod=0, b_zakaz=0, b_prochee=0, b_dop_uslugi=0, b_internet=0, b_alem=0, b_kabel=0)
    
    

        
    now = datetime.now()
    year_str = request.GET.get("history_year") if request.GET.get("history_year") != None else now.strftime("%Y")  # '2025'
    month_str = request.GET.get("history_month") if request.GET.get("history_month") != None else now.strftime("%m")  # '08'
    
    context['year_str'] = year_str
    context['month_str'] = month_str
    
 
    # ON history
    last_added = AlemNachFileNames.objects.filter(year=year_str, month=month_str, on_off="ON").order_by('-add_date')
    ic(last_added)
    last_added_info = {}
    for l in last_added:
        added = False
        if l.add_date:
            added = True
        
        nached = False
        if l.nach_date:
            nached = True
            
        if l.etrap not in last_added_info:     
            last_added_info[l.etrap] = [[added, nached, l.file_name]]
        else:
            last_added_info[l.etrap].append([added, nached, l.file_name])
            
    context['last_added_info'] = last_added_info
    
    
    # off history
    last_added_off = AlemNachFileNames.objects.filter(year=year_str, month=month_str, on_off="OFF").order_by('-add_date')
    ic(last_added_off)
    last_added_info_off = []
    for l in last_added_off:
        added = False
        if l.add_date:
            added = True
        
        nached = False
        if l.nach_date:
            nached = True
            
        last_added_info_off.append([l.file_name, added, nached])
    context['last_added_info_off'] = last_added_info_off

    
    
    
    context['import_disabled'] = True

    # Обработка формы при GET-запросе
    if request.method == 'POST':
        dataset = Dataset()
        
        year = request.POST.get('year')
        month = request.POST.get('month')
        etrap = request.POST.get('etrap')
        action_type = request.POST.get('action_type')
        on_or_off = request.POST.get('on_or_off')
        chekPriceDateItogo = True if request.POST.get('priceCheck') == "checkWithDate" else False 
        
        context['selected_month'] = month
        context['selected_year'] = year
        context['selected_etrap'] = etrap
        context['selected_action'] = action_type
        context['selected_on_or_off'] = on_or_off
        
        try:
            xlsx_data = request.FILES['file']
            context['file_name'] = str(xlsx_data)
        except:
            messages.error(request, f'Выберите Файл')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
        
        try:
            imported_data = dataset.load(xlsx_data.read(), format='xlsx', headers=False)
        except:
            messages.error(request, f'Файл должен быть формата xlsx')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
        
        
        
        # head = imported_data[0][0].lower()
        # ic(month)
        
        month_word = monthСonvert(month)
        text = str(xlsx_data)
        
        if f"{str(month)} {str(year)}" not in text:
            messages.error(request, f'месяц или год в названии excel не совпадает с выбранным месяцем или годом')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
    
        
        if on_or_off == "OFF" and "OFF." not in text:
            messages.error(request, f'Файл не OFF')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
        
        
        if on_or_off == "ON" and "ON." not in text:
            messages.error(request, f'Файл не ON')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
        
        if "ON." in text and "OFF." in text:
            messages.error(request, 'Файл содержит и "ON.", и "OFF.". Нужно оставить только одно.')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
            
        
        
            
        
        
        test_count = 0
        test_total_price = 0
        
        check_etrap = []
        error_list = []
        error_count = 0
        error_data_price = []
        
        ##################################################################################################################################################################################################################
        ##################################################################################################################################################################################################################
        ##################################################################################################################################################################################################################
        ##################################################################################################################################################################################################################
        if on_or_off == "ON":
            
            # proweryaem etrap i dogowory
            users = UserTable.objects.filter(etrap=etrap)
            number_pk = {}
            for u in users:
                number_pk[u.number] = u.pk
                
            
                
            for idx, d in enumerate(imported_data):
                # if idx < 3:
                #     continue  # Пропускаем первые 2 строки
                # if idx == len(imported_data) - 1 and 'Всего' in d[0]:
                #     break  # Прерываемся перед последней строкой
                # ic(d[1])
                
                
                
                # ic(d[0])
                
                
                
                if d[0]:
                    check_shift_to_the_left = d[0].lower().strip()
   
                
                    if 'iptv' in check_shift_to_the_left:
                        # ic(d)
                        error_count += 1
                        error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Сдвиг влево"])
                        continue
                    
                    
                
                    
                    
                try:
                    dogowor = d[1].strip()
                except:
                    error_count += 1
                    error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная строка в Excel"])
                    continue
                
                
                
                
                
                if "IPTV" in dogowor:  
                    test_count += 1
                    
                    try:
                        tarif = d[3].upper()
                        if "IPTV" not in tarif:
                            error_count += 1
                            error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Колонка 'Тариф' не IPTV"])
                    except:
                        error_count += 1
                        error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Колонка 'Тариф' не IPTV"])
                    
                    try:
                        # print(d[6], type(d[6]))
                        price = Decimal(str(d[6]).strip().replace(',', '.'))
                        # price = Decimal(d[6])
                    except:
                        
                        error_count += 1
                        error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (В списание)"])
                        continue
                    
                    
                    test_total_price += price
                    
                    # в платеже может быть дата
                    
                    if d[8]:
                        try:
                            price = Decimal(str(d[8]).replace(",", "."))
                        except (ValueError, TypeError):
                            try:
                                value = str(d[8])
                                if len(value) >= 10 and value[8:10] == '01':
                                    month_d = int(value[5:7])
                                    year_d = value[2:4]
                                    price = Decimal(f"{month_d}.{year_d}")
                                elif len(value) >= 10 and value[8:10] != '01':
                                    day = int(value[8:10])
                                    month_d = value[5:7]
                                    price = Decimal(f"{day}.{month_d}")
                                    if chekPriceDateItogo:
                                        error_data_price.append([d[0], d[1], d[2], d[6], d[8], price, "Цена-дата (Itogo)"])
                                else:
                                    error_count += 1
                                    error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
                            except Exception:
                                error_count += 1
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
                                
                    else:
                        error_count += 1
                        error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
                    
                        
                        
                        
                  
                    number = str(re.sub(r'\D', '', dogowor))
                    if len(number) == 11:
                        if number[6:] not in number_pk:
                            error_count += 1
                            error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                            
                        elif number[3:6] == "322":
                            if len(check_etrap) == 1 and "Dashoguz" not in check_etrap:
                                error_count += 1
                                check_etrap.append("Dashoguz")
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
                            if "Dashoguz" not in check_etrap:
                                check_etrap.append("Dashoguz")
    
                        elif number[3:6] == "344":
                            if len(check_etrap) == 1 and "Akdepe" not in check_etrap:
                                error_count += 1
                                check_etrap.append("Akdepe")
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
                            if "Akdepe" not in check_etrap:
                                check_etrap.append("Akdepe")
                                
                        elif number[3:6] == "343":
                            if len(check_etrap) == 1 and "Garashsyzlyk" not in check_etrap:
                                error_count += 1
                                check_etrap.append("Garashsyzlyk")
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
                            if "Garashsyzlyk" not in check_etrap:
                                check_etrap.append("Garashsyzlyk")
                                
                        elif number[3:6] == "346":
                            if len(check_etrap) == 1 and "Boldumsaz" not in check_etrap:
                                error_count += 1
                                check_etrap.append("Boldumsaz")
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
                            if "Boldumsaz" not in check_etrap:
                                check_etrap.append("Boldumsaz")
                                
                        elif number[3:6] == "345":
                            if len(check_etrap) == 1 and "Gubadag" not in check_etrap:
                                error_count += 1
                                check_etrap.append("Gubadag")
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
                            if "Gubadag" not in check_etrap:
                                check_etrap.append("Gubadag")
                                
                        elif number[3:6] == "340":
                            if len(check_etrap) == 1 and "Gorogly" not in check_etrap:
                                error_count += 1
                                check_etrap.append("Gorogly")
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
                            if "Gorogly" not in check_etrap:
                                check_etrap.append("Gorogly")
                                
                        elif number[3:6] == "347":
                            if len(check_etrap) == 1 and "Koneurgench" not in check_etrap:
                                error_count += 1
                                check_etrap.append("Koneurgench")
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
                            if "Koneurgench" not in check_etrap:
                                check_etrap.append("Koneurgench")
                                
                        elif number[3:6] == "349":
                            if len(check_etrap) == 1 and "Turkmenbashy" not in check_etrap:
                                error_count += 1
                                check_etrap.append("Turkmenbashy")
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
                            if "Turkmenbashy" not in check_etrap:
                                check_etrap.append("Turkmenbashy")
                                
                        elif number[3:6] == "348":
                            if len(check_etrap) == 1 and "S.A.Nyyazow" not in check_etrap:
                                error_count += 1
                                check_etrap.append("S.A.Nyyazow")
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
                            if "S.A.Nyyazow" not in check_etrap:
                                check_etrap.append("S.A.Nyyazow")
                                
                        elif number[3:6] == "342":
                            if len(check_etrap) == 1 and "Ruhubelent" not in check_etrap:
                                error_count += 1
                                check_etrap.append("Ruhubelent")
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
                            if "Ruhubelent" not in check_etrap:
                                check_etrap.append("Ruhubelent")
                                
                        else:
                            error_count += 1
                            error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (kod)"])         
                    else:
                        error_count += 1
                        error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (len != 16)"])
                        
                        
            
            ic(test_total_price)              
            ic(test_count)              
            if len(error_list) > 0:
                error_context  = {}
                error_context['error_file_name'] = str(xlsx_data)
                error_context['error_list'] = error_list
                messages.error(request, f'Ошибка')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/error_alem.html', error_context )
            
            
            
            
            else:
                if check_etrap[0] != etrap:
                    messages.error(request, f'Вы выбрали не тот этрап')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
                
                if len(error_data_price) and action_type == "check":
                    error_data  = {}
                    error_data['error_file_name'] = str(xlsx_data)
                    error_data['error_data_price'] = error_data_price
                    messages.error(request, f'Ошибка')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/error_alem.html', error_data )
                
                
                if AlemNachData.objects.filter(year=year, month=month, etrap=etrap, on_off="ON").exists():
                    messages.error(request, f"Импорт для '{etrap}' за {month}-{year} уже был выполнен")
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
                    
                
                context['test_count'] = test_count
                context['test_total_price'] = test_total_price

                if AlemNachFileNames.objects.filter(file_name=text).exists():
                    messages.error(request, f'Файл {text} уже импортирован')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
                
                if action_type == "import":
                    bulk_create_objs = []
                    for idx, d in enumerate(imported_data):
                        # if idx < 3:
                        #     continue  # Пропускаем первые 3 строки
                        # if idx == len(imported_data) - 1 and 'Всего' in d[0]:
                        #     break  # Прерываемся перед последней строкой
                        
                        dogowor = d[1].strip()
                        if dogowor[:4].upper() == "IPTV":
                            
                            # в платеже может быть дата
                            if d[8]:
                                try:
                                    price = Decimal(str(d[8]).replace(",", "."))
                                except (ValueError, TypeError):
                                        value = str(d[8])
                                        if len(value) >= 10 and value[8:10] == '01':
                                            month_d = int(value[5:7])
                                            year_d = value[2:4]
                                            price = Decimal(f"{month_d}.{year_d}")
                                        elif len(value) >= 10 and value[8:10] != '01':
                                            day = int(value[8:10])
                                            month_d = value[5:7]
                                            price = Decimal(f"{day}.{month_d}")
                                        else:
                                            print(d)
                                            # raise ValueError("Недостаточно символов в d[8]")
                                            error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Недостаточно символов в (Itogo)"])


                            else:
                                error_count += 1
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
                                
                            if len(error_list) > 0:
                                error_context  = {}
                                error_context['error_file_name'] = str(xlsx_data)
                                error_context['error_list'] = error_list
                                messages.error(request, f'Ошибка')
                                return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/error_alem.html', error_context )
                      
                            number = re.sub(r'\D', '', dogowor)
                            name = d[0]
                            account_name = d[2]
                            tariff = d[3]
                            service = d[4]
                            tariff_charge = Decimal(str(d[5]).strip().replace(',', '.'))
                            service_charge = Decimal(str(d[6]).strip().replace(',', '.'))
                            quantity = Decimal(str(d[7]).strip().replace(',', '.'))
                            currency = d[9]
                            # ic(month)

                            obj = AlemNachData(
                                number=number[6:],
                                etrap=etrap,
                                dogowor=dogowor,
                                name=name,
                                account_name=account_name,
                                tariff=tariff,
                                service=service,
                                tariff_charge=tariff_charge,
                                service_charge=service_charge,
                                quantity=quantity,
                                total=price,
                                currency=currency,
                                on_off="ON",
                                month=month, 
                                year=year,
                                file_name=str(xlsx_data),
                            )
                            bulk_create_objs.append(obj)
                            
                    try:
                        with transaction.atomic():
                            if bulk_create_objs:
                                AlemNachData.objects.bulk_create(bulk_create_objs)
                                AlemNachFileNames.objects.create(file_name=str(xlsx_data), add_date=datetime.now(), who_add=request.user.username, month=month, year=year, on_off="ON", etrap=etrap)
                                messages.success(request, f'Импорт успешно: {len(bulk_create_objs)} строк добавлено')
                                return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
                            else:
                                messages.warning(request, 'Нет данных для импорта')
                    except Exception as e:
                        messages.error(request, f'ошибка с transaction == {e}')
                        logger.error(f'ошибка с transaction == {e}')
                    
                else:
                    ic(test_count)
                    ic(test_total_price)
                    messages.success(request, f'Проверка ON прошла успешно')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
         
        ################################################################################################################################################################################# 
        ################################################################################################################################################################################# 
        ################################################################################################################################################################################# 
        ################################################################################################################################################################################# 
        elif on_or_off == "OFF":
            info_ = {}
            # etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
            # proweryaem dogowory  
            for idx, d in enumerate(imported_data):
                # if idx < 3:
                #     continue  # Пропускаем первые 2 строки
                # if idx == len(imported_data) - 1 and 'Всего' in d[0]:
                #     break  # Прерываемся перед последней строкой
                
                if d[0]:
                    check_shift_to_the_left = d[0].lower().strip()
                    if 'iptv' in check_shift_to_the_left:
                        # ic(d)
                        error_count += 1
                        error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Сдвиг влево"])
                        continue
                    
                    
                try:
                    dogowor = d[1].strip()
                except:
                    error_count += 1
                    error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная строка в Excel"])
                    continue
                
                
                if "IPTV" in dogowor:
                    test_count += 1
                    
                    try:
                        tarif = d[3].upper()
                        if "IPTV" not in tarif:
                            error_count += 1
                            error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Колонка 'Тариф' не IPTV"])
                    except:
                        error_count += 1
                        error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Колонка 'Тариф' не IPTV"])
                        
                    try:
                        # float(d[6])
                        Decimal(str(d[6]).strip().replace(',', '.'))
                    except:
                        error_count += 1
                        error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (В списании)"])
                        
                        
                    # в платеже может быть дата
                    if d[8]:
                        try:
                            price = Decimal(str(d[8]).replace(",", "."))
                        except (ValueError, TypeError):
                            try:
                                value = str(d[8])
                                if len(value) >= 10 and value[8:10] == '01':
                                    month_d = int(value[5:7])
                                    year_d = value[2:4]
                                    price = Decimal(f"{month_d}.{year_d}")
                                elif len(value) >= 10 and value[8:10] != '01':
                                    day = int(value[8:10])
                                    month_d = value[5:7]
                                    price = Decimal(f"{day}.{month_d}")
                                    if chekPriceDateItogo:
                                        error_data_price.append([d[0], d[1], d[2], d[6], d[8], price, "Цена-дата (Itogo)"])
                                else:
                                    error_count += 1
                                    error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
                            except Exception:
                                error_count += 1
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
                                
                    else:
                        error_count += 1
                        error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
                        
                    test_total_price += price
                  
                    number = str(re.sub(r'\D', '', dogowor))
                    if len(number) == 11:             
   
                        if number[3:6] == "322":
                            try:
                                UserTable.objects.get(etrap="Dashoguz", number=number[6:])
                                if 'Dashoguz' not in info_:
                                    info_['Dashoguz'] = [1, price ]
                                else:
                                    info_['Dashoguz'][0] += 1
                                    info_['Dashoguz'][1] += price  
                            except:
                                error_count += 1
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
                        elif number[3:6] == "344":
                            try:
                                UserTable.objects.get(etrap="Akdepe", number=number[6:])
                                if 'Akdepe' not in info_:
                                    info_['Akdepe'] = [1, price ]
                                else:
                                    info_['Akdepe'][0] += 1
                                    info_['Akdepe'][1] += price 
                            except:
                                error_count += 1
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
                        elif number[3:6] == "343":
                            try:
                                UserTable.objects.get(etrap="Garashsyzlyk", number=number[6:])
                                if 'Garashsyzlyk' not in info_:
                                    info_['Garashsyzlyk'] = [1, price ]
                                else:
                                    info_['Garashsyzlyk'][0] += 1
                                    info_['Garashsyzlyk'][1] += price 
                            except:
                                error_count += 1
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
                        elif number[3:6] == "346":
                            try:
                                UserTable.objects.get(etrap="Boldumsaz", number=number[6:])
                                if 'Boldumsaz' not in info_:
                                    info_['Boldumsaz'] = [1, price ]
                                else:
                                    info_['Boldumsaz'][0] += 1
                                    info_['Boldumsaz'][1] += price 
                            except:
                                error_count += 1
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                          
                                
                        elif number[3:6] == "345":
                            try:
                                UserTable.objects.get(etrap="Gubadag", number=number[6:])
                                if 'Gubadag' not in info_:
                                    info_['Gubadag'] = [1, price ]
                                else:
                                    info_['Gubadag'][0] += 1
                                    info_['Gubadag'][1] += price 
                            except:
                                error_count += 1
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
                        elif number[3:6] == "340":
                            try:
                                UserTable.objects.get(etrap="Gorogly", number=number[6:])
                                if 'Gorogly' not in info_:
                                    info_['Gorogly'] = [1, price ]
                                else:
                                    info_['Gorogly'][0] += 1
                                    info_['Gorogly'][1] += price 
                            except:
                                error_count += 1
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
                        elif number[3:6] == "347":
                            try:
                                UserTable.objects.get(etrap="Koneurgench", number=number[6:])
                                if 'Koneurgench' not in info_:
                                    info_['Koneurgench'] = [1, price ]
                                else:
                                    info_['Koneurgench'][0] += 1
                                    info_['Koneurgench'][1] += price 
                            except:
                                error_count += 1
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
                        elif number[3:6] == "349":
                            try:
                                UserTable.objects.get(etrap="Turkmenbashy", number=number[6:])
                                if 'Turkmenbashy' not in info_:
                                    info_['Turkmenbashy'] = [1, price ]
                                else:
                                    info_['Turkmenbashy'][0] += 1
                                    info_['Turkmenbashy'][1] += price 
                            except:
                                error_count += 1
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
                        elif number[3:6] == "348":
                            try:
                                UserTable.objects.get(etrap="S.A.Nyyazow", number=number[6:])
                                if 'Shabat' not in info_:
                                    info_['Shabat'] = [1, price ]
                                else:
                                    info_['Shabat'][0] += 1
                                    info_['Shabat'][1] += price 
                            except:
                                error_count += 1
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
                        elif number[3:6] == "342":
                            try:
                                UserTable.objects.get(etrap="Ruhubelent", number=number[6:])
                                if 'Ruhubelent' not in info_:
                                    info_['Ruhubelent'] = [1, price ]
                                else:
                                    info_['Ruhubelent'][0] += 1
                                    info_['Ruhubelent'][1] += price 
                            except:
                                error_count += 1
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                        
                        else:
                            error_count += 1
                            error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (kod)"])         
                    else:
                        error_count += 1
                        error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (len != 16)"])
                    
             
            ic(test_total_price)
            if len(error_list) > 0:
                error_context  = {}
                error_context['error_file_name'] = str(xlsx_data)
                error_context['error_list'] = error_list
                messages.error(request, f'Ошибка')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/error_alem.html', error_context )
            
            else:
                if len(error_data_price) and action_type == "check":
                    error_data  = {}
                    error_data['error_file_name'] = str(xlsx_data)
                    error_data['error_data_price'] = error_data_price
                    messages.error(request, f'Ошибка')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/error_alem.html', error_data )
            
                context['info_'] = info_
                
                if AlemNachFileNames.objects.filter(file_name=text).exists():
                    messages.error(request, f'Файл {text} уже импортирован')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
                
                if action_type == "import":
                    bulk_create_objs = []
                    for idx, d in enumerate(imported_data):
                        # if idx < 3:
                        #     continue  # Пропускаем первые 3 строки
                        # if idx == len(imported_data) - 1 and 'Всего' in d[0]:
                        #     break  # Прерываемся перед последней строкой
        
                        dogowor = d[1].strip()
                        if dogowor[:4].upper() == "IPTV":
                            
                            # в платеже может быть дата
                            if d[8]:
                                try:
                                    price = Decimal(str(d[8]).replace(",", "."))
                                except (ValueError, TypeError):
                                    value = str(d[8])
                                    if len(value) >= 10 and value[8:10] == '01':
                                        month_d = int(value[5:7])
                                        year_d = value[2:4]
                                        price = Decimal(f"{month_d}.{year_d}")
                                    elif len(value) >= 10 and value[8:10] != '01':
                                        day = int(value[8:10])
                                        month_d = value[5:7]
                                        price = Decimal(f"{day}.{month_d}")
                                        error_data_price.append([d[0], d[1], d[2], d[6], d[8], price, "Цена-дата (Itogo)"])
                                    else:
                                        raise ValueError("Недостаточно символов в d[8]")

                                        
                            else:
                                error_count += 1
                                error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
                                        
                            number = re.sub(r'\D', '', dogowor)
                            name = d[0]
                            account_name = d[2]
                            tariff = d[3]
                            service = d[4]
                            tariff_charge = Decimal(str(d[5]).strip().replace(',', '.'))
                            service_charge = Decimal(str(d[6]).strip().replace(',', '.'))
                            quantity = Decimal(str(d[7]).strip().replace(',', '.'))
                            currency = d[9]
                            
                            if number[3:6] == "322":
                                current_etrap = "Dashoguz"
                                
                            elif number[3:6] == "344":
                                current_etrap = "Akdepe"
                                
                            elif number[3:6] == "343":
                                current_etrap = "Garashsyzlyk"
                                    
                            elif number[3:6] == "346":
                                current_etrap = "Boldumsaz"
                                
                            elif number[3:6] == "345":
                                current_etrap = "Gubadag"
        
                            elif number[3:6] == "340":
                                current_etrap = "Gorogly"
  
                            elif number[3:6] == "347":
                                current_etrap = "Koneurgench"
   
                            elif number[3:6] == "349":
                                current_etrap = "Turkmenbashy"

                            elif number[3:6] == "348":
                                current_etrap = "S.A.Nyyazow"

                            elif number[3:6] == "342":
                                current_etrap = "Ruhubelent"
         
                            else:
                                messages.error(request, f'Непонятный договор {d[1]}')
                                return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)

                            obj = AlemNachData(
                                number=number[6:],
                                etrap=current_etrap,
                                dogowor=dogowor,
                                name=name,
                                account_name=account_name,
                                tariff=tariff,
                                service=service,
                                tariff_charge=tariff_charge,
                                service_charge=service_charge,
                                quantity=quantity,
                                total=price,
                                currency=currency,
                                on_off="OFF",
                                month=month,
                                year=year,
                                file_name=str(xlsx_data),
                            )
                            bulk_create_objs.append(obj)
                            
                    try:
                        with transaction.atomic():
                            if bulk_create_objs:
                                AlemNachData.objects.bulk_create(bulk_create_objs)
                                AlemNachFileNames.objects.create(file_name=str(xlsx_data), add_date=datetime.now(), who_add=request.user.username, month=month, year=year, on_off="OFF")
                                messages.success(request, f'Импорт успешно: {len(bulk_create_objs)} строк добавлено')
                                return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
                            else:
                                messages.warning(request, 'Нет данных для импорта')
                    except Exception as e:
                        messages.error(request, f'ошибка с transaction == {e}')
                        logger.error(f'ошибка с transaction == {e}')
                    
                else:
                    messages.success(request, f'Проверка OFF прошла успешно')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
        
        else:
            messages.error(request, 'В названии файла отсутствуют слова "OFF." и "ON."')
            
                                


    return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)


# RABOTAET NO BEZ RAZDELENNYH ETRAPOW
# from django.shortcuts import render, redirect
# from telekom.models import *
# from django.db.models import Sum
# from django.contrib import messages
# from django.db.models import Q
# from django.http import HttpResponse
# import tablib

# from datetime import date
# from calendar import monthrange
# from tablib import Dataset
# from icecream import ic
# from telekom.views2.myFunc.myFunc import monthСonvert

# from datetime import datetime, date
# import calendar
# import re
# from decimal import Decimal

# from django.db import transaction
# import logging
# logger = logging.getLogger(__name__)

# def alem_add(request):
#     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
#     months = [
#         ('01', 'Январь'), ('02', 'Февраль'), ('03', 'Март'), ('04', 'Апрель'),
#         ('05', 'Май'), ('06', 'Июнь'), ('07', 'Июль'), ('08', 'Август'),
#         ('09', 'Сентябрь'), ('10', 'Октябрь'), ('11', 'Ноябрь'), ('12', 'Декабрь'),
#     ]
#     current_date = datetime.now()
    

#     context = {
#         'alem_add': True,
#         'etraps': etraps,
#         'month_choices': months,
#         'current_year': current_date.year,
#         'current_month': f"{current_date.month:02d}",
#     }
    
#     # AlemNachFileNames.objects.all().delete()
#     # AlemNachData.objects.all().delete()
#     # NachMinus.objects.all().update(alem=0)
#     # UserTable.objects.all().update(b_telefon=0, b_slr=0, b_kod=0, b_zakaz=0, b_prochee=0, b_dop_uslugi=0, b_internet=0, b_alem=0, b_kabel=0)
    
    

        
#     now = datetime.now()
#     year_str = request.GET.get("history_year") if request.GET.get("history_year") != None else now.strftime("%Y")  # '2025'
#     month_str = request.GET.get("history_month") if request.GET.get("history_month") != None else now.strftime("%m")  # '08'
    
#     context['year_str'] = year_str
#     context['month_str'] = month_str
    
 
#     # ON history
#     last_added = AlemNachFileNames.objects.filter(year=year_str, month=month_str, on_off="ON").order_by('-add_date')
#     ic(last_added)
#     last_added_info = {}
#     for l in last_added:
#         added = False
#         if l.add_date:
#             added = True
        
#         nached = False
#         if l.nach_date:
#             nached = True
            
#         if l.etrap not in last_added_info:     
#             last_added_info[l.etrap] = [[added, nached, l.file_name]]
#         else:
#             last_added_info[l.etrap].append([added, nached, l.file_name])
            
#     context['last_added_info'] = last_added_info
    
    
#     # off history
#     last_added_off = AlemNachFileNames.objects.filter(year=year_str, month=month_str, on_off="OFF").order_by('-add_date')
#     ic(last_added_off)
#     last_added_info_off = []
#     for l in last_added_off:
#         added = False
#         if l.add_date:
#             added = True
        
#         nached = False
#         if l.nach_date:
#             nached = True
            
#         last_added_info_off.append([l.file_name, added, nached])
#     context['last_added_info_off'] = last_added_info_off

    
    
    
#     context['import_disabled'] = True

#     # Обработка формы при GET-запросе
#     if request.method == 'POST':
#         dataset = Dataset()
        
#         year = request.POST.get('year')
#         month = request.POST.get('month')
#         etrap = request.POST.get('etrap')
#         action_type = request.POST.get('action_type')
#         on_or_off = request.POST.get('on_or_off')
#         chekPriceDateItogo = True if request.POST.get('priceCheck') == "checkWithDate" else False 
        
#         context['selected_month'] = month
#         context['selected_year'] = year
#         context['selected_etrap'] = etrap
#         context['selected_action'] = action_type
#         context['selected_on_or_off'] = on_or_off
        
#         try:
#             xlsx_data = request.FILES['file']
#             context['file_name'] = str(xlsx_data)
#         except:
#             messages.error(request, f'Выберите Файл')
#             return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
        
#         try:
#             imported_data = dataset.load(xlsx_data.read(), format='xlsx', headers=False)
#         except:
#             messages.error(request, f'Файл должен быть формата xlsx')
#             return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
        
        
        
#         # head = imported_data[0][0].lower()
#         # ic(month)
        
#         month_word = monthСonvert(month)
#         text = str(xlsx_data)
        
#         if f"{str(month)} {str(year)}" not in text:
#             messages.error(request, f'месяц или год в названии excel не совпадает с выбранным месяцем или годом')
#             return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
    
        
#         if on_or_off == "OFF" and "OFF." not in text:
#             messages.error(request, f'Файл не OFF')
#             return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
        
        
#         if on_or_off == "ON" and "ON." not in text:
#             messages.error(request, f'Файл не ON')
#             return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
        
#         if "ON." in text and "OFF." in text:
#             messages.error(request, 'Файл содержит и "ON.", и "OFF.". Нужно оставить только одно.')
#             return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
            
        
        
            
        
        
#         test_count = 0
#         test_total_price = 0
        
#         check_etrap = []
#         error_list = []
#         error_count = 0
#         error_data_price = []
        
#         ##################################################################################################################################################################################################################
#         ##################################################################################################################################################################################################################
#         ##################################################################################################################################################################################################################
#         ##################################################################################################################################################################################################################
#         if on_or_off == "ON":
            
#             # proweryaem etrap i dogowory
#             users = UserTable.objects.filter(etrap=etrap)
#             number_pk = {}
#             for u in users:
#                 number_pk[u.number] = u.pk
                
            
                
#             for idx, d in enumerate(imported_data):
#                 # if idx < 3:
#                 #     continue  # Пропускаем первые 2 строки
#                 # if idx == len(imported_data) - 1 and 'Всего' in d[0]:
#                 #     break  # Прерываемся перед последней строкой
#                 # ic(d[1])
                
                
                
#                 # ic(d[0])
                
                
                
#                 if d[0]:
#                     check_shift_to_the_left = d[0].lower().strip()
   
                
#                     if 'iptv' in check_shift_to_the_left:
#                         # ic(d)
#                         error_count += 1
#                         error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Сдвиг влево"])
#                         continue
                    
                    
                
                    
                    
#                 try:
#                     dogowor = d[1].strip()
#                 except:
#                     error_count += 1
#                     error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная строка в Excel"])
#                     continue
                
                
                
                
                
#                 if "IPTV" in dogowor:  
#                     test_count += 1
                    
#                     try:
#                         tarif = d[3].upper()
#                         if "IPTV" not in tarif:
#                             error_count += 1
#                             error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Колонка 'Тариф' не IPTV"])
#                     except:
#                         error_count += 1
#                         error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Колонка 'Тариф' не IPTV"])
                    
#                     try:
#                         # print(d[6], type(d[6]))
#                         price = Decimal(d[6].strip().replace(',', '.'))
#                         # price = Decimal(d[6])
#                     except:
                        
#                         error_count += 1
#                         error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (В списание)"])
#                         continue
                    
                    
#                     test_total_price += price
                    
#                     # в платеже может быть дата
                    
#                     if d[8]:
#                         try:
#                             price = Decimal(str(d[8]).replace(",", "."))
#                         except (ValueError, TypeError):
#                             try:
#                                 value = str(d[8])
#                                 if len(value) >= 10 and value[8:10] == '01':
#                                     month_d = int(value[5:7])
#                                     year_d = value[2:4]
#                                     price = Decimal(f"{month_d}.{year_d}")
#                                 elif len(value) >= 10 and value[8:10] != '01':
#                                     day = int(value[8:10])
#                                     month_d = value[5:7]
#                                     price = Decimal(f"{day}.{month_d}")
#                                     if chekPriceDateItogo:
#                                         error_data_price.append([d[0], d[1], d[2], d[6], d[8], price, "Цена-дата (Itogo)"])
#                                 else:
#                                     error_count += 1
#                                     error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
#                             except Exception:
#                                 error_count += 1
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
                                
#                     else:
#                         error_count += 1
#                         error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
                    
                        
                        
                        
                  
#                     number = str(re.sub(r'\D', '', dogowor))
#                     if len(number) == 11:
#                         if number[6:] not in number_pk:
#                             error_count += 1
#                             error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                            
#                         elif number[3:6] == "322":
#                             if len(check_etrap) == 1 and "Dashoguz" not in check_etrap:
#                                 error_count += 1
#                                 check_etrap.append("Dashoguz")
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
#                             if "Dashoguz" not in check_etrap:
#                                 check_etrap.append("Dashoguz")
    
#                         elif number[3:6] == "344":
#                             if len(check_etrap) == 1 and "Akdepe" not in check_etrap:
#                                 error_count += 1
#                                 check_etrap.append("Akdepe")
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
#                             if "Akdepe" not in check_etrap:
#                                 check_etrap.append("Akdepe")
                                
#                         elif number[3:6] == "346":
#                             if len(check_etrap) == 1 and "Boldumsaz" not in check_etrap:
#                                 error_count += 1
#                                 check_etrap.append("Boldumsaz")
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
#                             if "Boldumsaz" not in check_etrap:
#                                 check_etrap.append("Boldumsaz")
                                
#                         elif number[3:6] == "340":
#                             if len(check_etrap) == 1 and "Gorogly" not in check_etrap:
#                                 error_count += 1
#                                 check_etrap.append("Gorogly")
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
#                             if "Gorogly" not in check_etrap:
#                                 check_etrap.append("Gorogly")
                                
#                         elif number[3:6] == "347":
#                             if len(check_etrap) == 1 and "Koneurgench" not in check_etrap:
#                                 error_count += 1
#                                 check_etrap.append("Koneurgench")
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
#                             if "Koneurgench" not in check_etrap:
#                                 check_etrap.append("Koneurgench")
                                
#                         elif number[3:6] == "349":
#                             if len(check_etrap) == 1 and "Turkmenbashy" not in check_etrap:
#                                 error_count += 1
#                                 check_etrap.append("Turkmenbashy")
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
#                             if "Turkmenbashy" not in check_etrap:
#                                 check_etrap.append("Turkmenbashy")
                                
#                         elif number[3:6] == "348":
#                             if len(check_etrap) == 1 and "S.A.Nyyazow" not in check_etrap:
#                                 error_count += 1
#                                 check_etrap.append("S.A.Nyyazow")
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
#                             if "S.A.Nyyazow" not in check_etrap:
#                                 check_etrap.append("S.A.Nyyazow")
                                
#                         elif number[3:6] == "342":
#                             if len(check_etrap) == 1 and "Ruhubelent" not in check_etrap:
#                                 error_count += 1
#                                 check_etrap.append("Ruhubelent")
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], f"Непонято к какому етрапу принадлежит файл (В файле есть несколько этрапов {check_etrap})"])
#                             if "Ruhubelent" not in check_etrap:
#                                 check_etrap.append("Ruhubelent")
                                
#                         else:
#                             error_count += 1
#                             error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (kod)"])         
#                     else:
#                         error_count += 1
#                         error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (len != 16)"])
                        
                        
            
#             ic(test_total_price)              
#             ic(test_count)              
#             if len(error_list) > 0:
#                 error_context  = {}
#                 error_context['error_file_name'] = str(xlsx_data)
#                 error_context['error_list'] = error_list
#                 messages.error(request, f'Ошибка')
#                 return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/error_alem.html', error_context )
            
            
            
            
#             else:
#                 if check_etrap[0] != etrap:
#                     messages.error(request, f'Вы выбрали не тот этрап')
#                     return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
                
#                 if len(error_data_price) and action_type == "check":
#                     error_data  = {}
#                     error_data['error_file_name'] = str(xlsx_data)
#                     error_data['error_data_price'] = error_data_price
#                     messages.error(request, f'Ошибка')
#                     return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/error_alem.html', error_data )
                
                
#                 if AlemNachData.objects.filter(year=year, month=month, etrap=etrap, on_off="ON").exists():
#                     messages.error(request, f"Импорт для '{etrap}' за {month}-{year} уже был выполнен")
#                     return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
                    
                
#                 context['test_count'] = test_count
#                 context['test_total_price'] = test_total_price

#                 if AlemNachFileNames.objects.filter(file_name=text).exists():
#                     messages.error(request, f'Файл {text} уже импортирован')
#                     return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
                
#                 if action_type == "import":
#                     bulk_create_objs = []
#                     for idx, d in enumerate(imported_data):
#                         # if idx < 3:
#                         #     continue  # Пропускаем первые 3 строки
#                         # if idx == len(imported_data) - 1 and 'Всего' in d[0]:
#                         #     break  # Прерываемся перед последней строкой
                        
#                         dogowor = d[1].strip()
#                         if dogowor[:4].upper() == "IPTV":
                            
#                             # в платеже может быть дата
#                             if d[8]:
#                                 try:
#                                     price = Decimal(str(d[8]).replace(",", "."))
#                                 except (ValueError, TypeError):
#                                         value = str(d[8])
#                                         if len(value) >= 10 and value[8:10] == '01':
#                                             month_d = int(value[5:7])
#                                             year_d = value[2:4]
#                                             price = Decimal(f"{month_d}.{year_d}")
#                                         elif len(value) >= 10 and value[8:10] != '01':
#                                             day = int(value[8:10])
#                                             month_d = value[5:7]
#                                             price = Decimal(f"{day}.{month_d}")
#                                         else:
#                                             print(d)
#                                             # raise ValueError("Недостаточно символов в d[8]")
#                                             error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Недостаточно символов в (Itogo)"])


#                             else:
#                                 error_count += 1
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
                                
#                             if len(error_list) > 0:
#                                 error_context  = {}
#                                 error_context['error_file_name'] = str(xlsx_data)
#                                 error_context['error_list'] = error_list
#                                 messages.error(request, f'Ошибка')
#                                 return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/error_alem.html', error_context )
                      
#                             number = re.sub(r'\D', '', dogowor)
#                             name = d[0]
#                             account_name = d[2]
#                             tariff = d[3]
#                             service = d[4]
#                             tariff_charge = Decimal(d[5].strip().replace(',', '.'))
#                             service_charge = Decimal(d[6].strip().replace(',', '.'))
#                             quantity = Decimal(d[7].strip().replace(',', '.'))
#                             currency = d[9]
#                             # ic(month)

#                             obj = AlemNachData(
#                                 number=number[6:],
#                                 etrap=etrap,
#                                 dogowor=dogowor,
#                                 name=name,
#                                 account_name=account_name,
#                                 tariff=tariff,
#                                 service=service,
#                                 tariff_charge=tariff_charge,
#                                 service_charge=service_charge,
#                                 quantity=quantity,
#                                 total=price,
#                                 currency=currency,
#                                 on_off="ON",
#                                 month=month, 
#                                 year=year,
#                                 file_name=str(xlsx_data),
#                             )
#                             bulk_create_objs.append(obj)
                            
#                     try:
#                         with transaction.atomic():
#                             if bulk_create_objs:
#                                 AlemNachData.objects.bulk_create(bulk_create_objs)
#                                 AlemNachFileNames.objects.create(file_name=str(xlsx_data), add_date=datetime.now(), who_add=request.user.username, month=month, year=year, on_off="ON", etrap=etrap)
#                                 messages.success(request, f'Импорт успешно: {len(bulk_create_objs)} строк добавлено')
#                                 return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
#                             else:
#                                 messages.warning(request, 'Нет данных для импорта')
#                     except Exception as e:
#                         messages.error(request, f'ошибка с transaction == {e}')
#                         logger.error(f'ошибка с transaction == {e}')
                    
#                 else:
#                     ic(test_count)
#                     ic(test_total_price)
#                     messages.success(request, f'Проверка ON прошла успешно')
#                     return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
         
#         ################################################################################################################################################################################# 
#         ################################################################################################################################################################################# 
#         ################################################################################################################################################################################# 
#         ################################################################################################################################################################################# 
#         elif on_or_off == "OFF":
#             info_ = {}
#             # etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
#             # proweryaem dogowory  
#             for idx, d in enumerate(imported_data):
#                 # if idx < 3:
#                 #     continue  # Пропускаем первые 2 строки
#                 # if idx == len(imported_data) - 1 and 'Всего' in d[0]:
#                 #     break  # Прерываемся перед последней строкой
                
#                 if d[0]:
#                     check_shift_to_the_left = d[0].lower().strip()
#                     if 'iptv' in check_shift_to_the_left:
#                         # ic(d)
#                         error_count += 1
#                         error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Сдвиг влево"])
#                         continue
                    
                    
#                 try:
#                     dogowor = d[1].strip()
#                 except:
#                     error_count += 1
#                     error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная строка в Excel"])
#                     continue
                
                
#                 if "IPTV" in dogowor:
#                     test_count += 1
                    
#                     try:
#                         tarif = d[3].upper()
#                         if "IPTV" not in tarif:
#                             error_count += 1
#                             error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Колонка 'Тариф' не IPTV"])
#                     except:
#                         error_count += 1
#                         error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Колонка 'Тариф' не IPTV"])
                        
#                     try:
#                         # float(d[6])
#                         Decimal(d[6].strip().replace(',', '.'))
#                     except:
#                         error_count += 1
#                         error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (В списании)"])
                        
                        
#                     # в платеже может быть дата
#                     if d[8]:
#                         try:
#                             price = Decimal(str(d[8]).replace(",", "."))
#                         except (ValueError, TypeError):
#                             try:
#                                 value = str(d[8])
#                                 if len(value) >= 10 and value[8:10] == '01':
#                                     month_d = int(value[5:7])
#                                     year_d = value[2:4]
#                                     price = Decimal(f"{month_d}.{year_d}")
#                                 elif len(value) >= 10 and value[8:10] != '01':
#                                     day = int(value[8:10])
#                                     month_d = value[5:7]
#                                     price = Decimal(f"{day}.{month_d}")
#                                     if chekPriceDateItogo:
#                                         error_data_price.append([d[0], d[1], d[2], d[6], d[8], price, "Цена-дата (Itogo)"])
#                                 else:
#                                     error_count += 1
#                                     error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
#                             except Exception:
#                                 error_count += 1
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
                                
#                     else:
#                         error_count += 1
#                         error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
                        
#                     test_total_price += price
                  
#                     number = str(re.sub(r'\D', '', dogowor))
#                     if len(number) == 11:             
   
#                         if number[3:6] == "322":
#                             try:
#                                 UserTable.objects.get(etrap="Dashoguz", number=number[6:])
#                                 if 'Dashoguz' not in info_:
#                                     info_['Dashoguz'] = [1, price ]
#                                 else:
#                                     info_['Dashoguz'][0] += 1
#                                     info_['Dashoguz'][1] += price  
#                             except:
#                                 error_count += 1
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
#                         elif number[3:6] == "344":
#                             try:
#                                 UserTable.objects.get(etrap="Akdepe", number=number[6:])
#                                 if 'Akdepe' not in info_:
#                                     info_['Akdepe'] = [1, price ]
#                                 else:
#                                     info_['Akdepe'][0] += 1
#                                     info_['Akdepe'][1] += price 
#                             except:
#                                 error_count += 1
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
#                         elif number[3:6] == "346":
#                             try:
#                                 UserTable.objects.get(etrap="Boldumsaz", number=number[6:])
#                                 if 'Boldumsaz' not in info_:
#                                     info_['Boldumsaz'] = [1, price ]
#                                 else:
#                                     info_['Boldumsaz'][0] += 1
#                                     info_['Boldumsaz'][1] += price 
#                             except:
#                                 error_count += 1
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
#                         elif number[3:6] == "340":
#                             try:
#                                 UserTable.objects.get(etrap="Gorogly", number=number[6:])
#                                 if 'Gorogly' not in info_:
#                                     info_['Gorogly'] = [1, price ]
#                                 else:
#                                     info_['Gorogly'][0] += 1
#                                     info_['Gorogly'][1] += price 
#                             except:
#                                 error_count += 1
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
#                         elif number[3:6] == "347":
#                             try:
#                                 UserTable.objects.get(etrap="Koneurgench", number=number[6:])
#                                 if 'Koneurgench' not in info_:
#                                     info_['Koneurgench'] = [1, price ]
#                                 else:
#                                     info_['Koneurgench'][0] += 1
#                                     info_['Koneurgench'][1] += price 
#                             except:
#                                 error_count += 1
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
#                         elif number[3:6] == "349":
#                             try:
#                                 UserTable.objects.get(etrap="Turkmenbashy", number=number[6:])
#                                 if 'Turkmenbashy' not in info_:
#                                     info_['Turkmenbashy'] = [1, price ]
#                                 else:
#                                     info_['Turkmenbashy'][0] += 1
#                                     info_['Turkmenbashy'][1] += price 
#                             except:
#                                 error_count += 1
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
#                         elif number[3:6] == "348":
#                             try:
#                                 UserTable.objects.get(etrap="S.A.Nyyazow", number=number[6:])
#                                 if 'Shabat' not in info_:
#                                     info_['Shabat'] = [1, price ]
#                                 else:
#                                     info_['Shabat'][0] += 1
#                                     info_['Shabat'][1] += price 
#                             except:
#                                 error_count += 1
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                
#                         elif number[3:6] == "342":
#                             try:
#                                 UserTable.objects.get(etrap="Ruhubelent", number=number[6:])
#                                 if 'Ruhubelent' not in info_:
#                                     info_['Ruhubelent'] = [1, price ]
#                                 else:
#                                     info_['Ruhubelent'][0] += 1
#                                     info_['Ruhubelent'][1] += price 
#                             except:
#                                 error_count += 1
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (net w baze)"])
                                        
#                         else:
#                             error_count += 1
#                             error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (kod)"])         
#                     else:
#                         error_count += 1
#                         error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятный договор (len != 16)"])
                    
             
#             ic(test_total_price)
#             if len(error_list) > 0:
#                 error_context  = {}
#                 error_context['error_file_name'] = str(xlsx_data)
#                 error_context['error_list'] = error_list
#                 messages.error(request, f'Ошибка')
#                 return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/error_alem.html', error_context )
            
#             else:
#                 if len(error_data_price) and action_type == "check":
#                     error_data  = {}
#                     error_data['error_file_name'] = str(xlsx_data)
#                     error_data['error_data_price'] = error_data_price
#                     messages.error(request, f'Ошибка')
#                     return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/error_alem.html', error_data )
            
#                 context['info_'] = info_
                
#                 if AlemNachFileNames.objects.filter(file_name=text).exists():
#                     messages.error(request, f'Файл {text} уже импортирован')
#                     return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
                
#                 if action_type == "import":
#                     bulk_create_objs = []
#                     for idx, d in enumerate(imported_data):
#                         # if idx < 3:
#                         #     continue  # Пропускаем первые 3 строки
#                         # if idx == len(imported_data) - 1 and 'Всего' in d[0]:
#                         #     break  # Прерываемся перед последней строкой
        
#                         dogowor = d[1].strip()
#                         if dogowor[:4].upper() == "IPTV":
                            
#                             # в платеже может быть дата
#                             if d[8]:
#                                 try:
#                                     price = Decimal(str(d[8]).replace(",", "."))
#                                 except (ValueError, TypeError):
#                                     value = str(d[8])
#                                     if len(value) >= 10 and value[8:10] == '01':
#                                         month_d = int(value[5:7])
#                                         year_d = value[2:4]
#                                         price = Decimal(f"{month_d}.{year_d}")
#                                     elif len(value) >= 10 and value[8:10] != '01':
#                                         day = int(value[8:10])
#                                         month_d = value[5:7]
#                                         price = Decimal(f"{day}.{month_d}")
#                                         error_data_price.append([d[0], d[1], d[2], d[6], d[8], price, "Цена-дата (Itogo)"])
#                                     else:
#                                         raise ValueError("Недостаточно символов в d[8]")

                                        
#                             else:
#                                 error_count += 1
#                                 error_list.append([error_count, d[0], d[1], d[2], d[3], d[6], d[8], "Непонятная цена (Itogo)"])
                                        
#                             number = re.sub(r'\D', '', dogowor)
#                             name = d[0]
#                             account_name = d[2]
#                             tariff = d[3]
#                             service = d[4]
#                             tariff_charge = Decimal(d[5].strip().replace(',', '.'))
#                             service_charge = Decimal(d[6].strip().replace(',', '.'))
#                             quantity = Decimal(d[7].strip().replace(',', '.'))
#                             currency = d[9]
                            
#                             if number[3:6] == "322":
#                                 current_etrap = "Dashoguz"
                                
#                             elif number[3:6] == "344":
#                                 current_etrap = "Akdepe"
                                    
#                             elif number[3:6] == "346":
#                                 current_etrap = "Boldumsaz"
        
#                             elif number[3:6] == "340":
#                                 current_etrap = "Gorogly"
  
#                             elif number[3:6] == "347":
#                                 current_etrap = "Koneurgench"
   
#                             elif number[3:6] == "349":
#                                 current_etrap = "Turkmenbashy"

#                             elif number[3:6] == "348":
#                                 current_etrap = "S.A.Nyyazow"

#                             elif number[3:6] == "342":
#                                 current_etrap = "Ruhubelent"
         
#                             else:
#                                 messages.error(request, f'Непонятный договор {d[1]}')
#                                 return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)

#                             obj = AlemNachData(
#                                 number=number[6:],
#                                 etrap=current_etrap,
#                                 dogowor=dogowor,
#                                 name=name,
#                                 account_name=account_name,
#                                 tariff=tariff,
#                                 service=service,
#                                 tariff_charge=tariff_charge,
#                                 service_charge=service_charge,
#                                 quantity=quantity,
#                                 total=price,
#                                 currency=currency,
#                                 on_off="OFF",
#                                 month=month,
#                                 year=year,
#                                 file_name=str(xlsx_data),
#                             )
#                             bulk_create_objs.append(obj)
                            
#                     try:
#                         with transaction.atomic():
#                             if bulk_create_objs:
#                                 AlemNachData.objects.bulk_create(bulk_create_objs)
#                                 AlemNachFileNames.objects.create(file_name=str(xlsx_data), add_date=datetime.now(), who_add=request.user.username, month=month, year=year, on_off="OFF")
#                                 messages.success(request, f'Импорт успешно: {len(bulk_create_objs)} строк добавлено')
#                                 return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
#                             else:
#                                 messages.warning(request, 'Нет данных для импорта')
#                     except Exception as e:
#                         messages.error(request, f'ошибка с transaction == {e}')
#                         logger.error(f'ошибка с transaction == {e}')
                    
#                 else:
#                     messages.success(request, f'Проверка OFF прошла успешно')
#                     return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)
        
#         else:
#             messages.error(request, 'В названии файла отсутствуют слова "OFF." и "ON."')
            
                                


#     return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_add.html', context)

