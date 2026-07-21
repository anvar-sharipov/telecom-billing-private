from django.shortcuts import render, redirect
from telekom.models import *
from django.contrib import messages
from decimal import Decimal

from icecream import ic

from datetime import datetime


from django.db import transaction
import logging
logger = logging.getLogger(__name__)

def alem_nach(request):
    if (not request.user.is_superuser and request.user.username != 'admin1') and request.user.username != 'Gayyp':
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')

    context = {}
    context['alem_nach'] = True
    
    alem_files = AlemNachFileNames.objects.filter(nach_date__isnull=True).order_by("-pk")
    
    context['alem_files'] = alem_files
    context['disabled'] = True
    
    
    if request.method == "POST":
        file_names = request.POST.getlist('file_names')  
        
        
            

        action = request.POST.get('action')
        
        ic(file_names)
        ic(action)
        alems = AlemNachData.objects.filter(file_name__in=file_names)
        
        total_count = 0
        total_price = 0
        
        if not alems:
            messages.error(request, 'Файл Excel пустой')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_nach.html', context)
        
        count = 0
        be_nached = []
        dont_be_nached = []
        be_nached_count = 0
        dont_be_nached_count = 0
        be_nached_price = 0
        dont_be_nached_price = 0
        for a in alems:
            if a.on_off == "OFF":
                if count == 0:
                    count += 1
                    check_alems = AlemNachFileNames.objects.filter(year=a.year, month=a.month, on_off="ON")
                    all_ON_is_nached = True
                    for c in check_alems:
                        if not c.nach_date:
                            all_ON_is_nached = False
                            
                    if len(check_alems) != 10 or not all_ON_is_nached:
                        messages.error(request, 'Перед начислением OFF сначала начислите все ON')
                        return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_nach.html', context)
                user = UserTable.objects.get(etrap=a.etrap, number=a.number)
                try:
                    nach = NachMinus.objects.get(user=user, year=a.year, month=a.month)
                    if nach.alem != a.service_charge:
                        be_nached.append([a.number, a.etrap, a.year, a.month, a.service_charge, a.dogowor])
                        be_nached_count += 1
                        be_nached_price += a.service_charge
                    else:
                        dont_be_nached.append([a.number, a.etrap, a.year, a.month, a.service_charge, a.dogowor])
                        dont_be_nached_count += 1
                        dont_be_nached_price += a.service_charge
                except NachMinus.DoesNotExist:
                    be_nached.append([a.number, a.etrap, a.year, a.month, a.service_charge, a.dogowor])
                    be_nached_count += 1
                    be_nached_price += a.service_charge
            else:       
                total_count += 1
                total_price += a.service_charge
            
            
            
        
        
        context['total_count'] = total_count
        context['total_price'] = total_price
            
        context['be_nached'] = be_nached
        context['dont_be_nached'] = dont_be_nached
        context['be_nached_count'] = be_nached_count
        context['dont_be_nached_count'] = dont_be_nached_count
        context['be_nached_price'] = be_nached_price
        context['dont_be_nached_price'] = dont_be_nached_price
        
        
        if len(file_names) != 1:
            messages.error(request, 'Выберите только один файл Excel')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_nach.html', context)
        
        
            
        
        
        
        if action == "check":
            context['file_names'] = file_names
            context['disabled'] = False
            messages.success(request, 'Проверка прошла успешно')
        
        elif action == "nach":
            try:
                with transaction.atomic():
                    for a in alems:
                        if a.on_off == "ON":
                            user = UserTable.objects.get(etrap=a.etrap, number=a.number)
                            user.b_alem = Decimal(str(user.b_alem)) - a.service_charge
                            user.save()
                            try:
                                nach = NachMinus.objects.get(user=user, year=a.year, month=a.month)
                                nach.alem = Decimal(str(nach.alem)) + a.service_charge
                                nach.save()
                            except NachMinus.DoesNotExist:
                                NachMinus.objects.create(user=user, year=a.year, month=a.month, alem=a.service_charge) 
                            a.is_nach = True
                            a.save()
                            
                        elif a.on_off == "OFF":
                            user = UserTable.objects.get(etrap=a.etrap, number=a.number)
                            try:
                                nach = NachMinus.objects.get(user=user, year=a.year, month=a.month)
                                if nach.alem != a.service_charge:
                                    nach.alem = Decimal(str(nach.alem)) + a.service_charge
                                    user.b_alem = Decimal(str(user.b_alem)) - a.service_charge
                                    user.save()
                                    nach.save()
                                    a.is_nach = True
                                    a.save()
                                else:
                                    continue
                            except NachMinus.DoesNotExist:
                                NachMinus.objects.create(user=user, year=a.year, month=a.month, alem=a.service_charge)
                                user.b_alem = Decimal(str(user.b_alem)) - a.service_charge
                                user.save()
                                a.is_nach = True
                                a.save()
                    for name in file_names:
                        a = AlemNachFileNames.objects.get(file_name=name)
                        a.nach_date = datetime.now()
                        a.who_nach = request.user.username
                        a.save()
                                
            except Exception as e:
                messages.error(request, f'ошибка с transaction == {e}')
                logger.error(f'ошибка с transaction == {e}')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_nach.html', context)
            
            context['file_names'] = file_names
            context['disabled'] = True
            messages.success(request, 'Начисления прошли успешно')
        else:
            messages.error(request, 'Выберите действие')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_nach.html', context)
            
            
            
        
    
    
    # etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    # months = [
    #     ('01', 'Январь'), ('02', 'Февраль'), ('03', 'Март'), ('04', 'Апрель'),
    #     ('05', 'Май'), ('06', 'Июнь'), ('07', 'Июль'), ('08', 'Август'),
    #     ('09', 'Сентябрь'), ('10', 'Октябрь'), ('11', 'Ноябрь'), ('12', 'Декабрь'),
    # ]
    # current_date = datetime.now()
    
    # AlemNachFileNames.objects.all().delete()
    # AlemNachData.objects.all().delete()
    

    # context = {
    #     'alem_nach': True,
    #     'etraps': etraps,
    #     'month_choices': months,
    #     'current_year': current_date.year,
    #     'current_month': f"{current_date.month:02d}",
    # }
    # context['disabled'] = True
    
    # if request.method == 'POST':
    #     context['disabled'] = False

    #     year = request.POST.get('year')
    #     month = request.POST.get('month')
    #     etrap = request.POST.get('etrap')
    #     action_type = request.POST.get('action_type')
    #     on_or_off = request.POST.get('on_or_off')
        
        
        
    #     context['selected_month'] = month
    #     context['selected_year'] = year
    #     context['selected_etrap'] = etrap
    #     context['selected_action'] = action_type
    #     context['selected_on_or_off'] = on_or_off
        
        
        
        
        
        # if on_or_off == "ON":
        #     if not etrap or not month or not year:
        #         messages.error(request, f'Wyberite etrap, god i mesyac nachisleniya')
        #         context['disabled'] = True
        #         return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_nach.html', context)
            
        #     if not AlemNachFileNames.objects.filter(etrap=etrap, month=month, year=year, on_off="ON").exists():
        #         messages.error(request, f'{etrap} za {month}/{year} ne importirowan')
        #         context['disabled'] = True
        #         return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_nach.html', context)
            
        #     if AlemNachFileNames.objects.get(etrap=etrap, month=month, year=year, on_off="ON").nach_date:
        #         messages.error(request, f'{etrap} za {month}/{year} uje nachislen')
        #         context['disabled'] = True
        #         return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_nach.html', context)
            
        #     if AlemNachData.objects.filter(etrap=etrap, month=month, year=year, on_off=).exists():
        #         messages.error(request, f'{etrap} za {month}/{year} uje est dannye')
        #         context['disabled'] = True
        #         return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_nach.html', context)
            
            
        #     messages.success(request, f'prowerka {etrap} za {month}/{year} proshla uspeshno')
            
            
            # alems = AlemNachData.objects.filter(year=year, )
                
        
        
    

    # current_date = datetime.now().date()
    # formatted_date = current_date.strftime('%Y-%m-%d')
    # current_year, current_month, current_day = formatted_date.split('-')

    # context['formatted_date'] = formatted_date
    # context['current_year'] = current_year
    # context['current_month'] = current_month
    # context['current_day'] = current_day
    # context['baza_history'] = True
    
    # if request_user_type == 'MTB':
    #     context['matbIndex'] = True 
    #     context['request_user_etrap'] = request_user_etrap 

    # context['etraps'] = etraps

    # selected_etrap = request.GET.get('etrap')
    # date_from = request.GET.get('date_from')
    # date_to = request.GET.get('date_to')
    # akt_raport = request.GET.get('akt_raport')
    # comment = request.GET.get('comment')
    # number = request.GET.get('number')

    # # Фильтрация данных на основе параметров GET
    # filter_args = {}
    
    # if selected_etrap:
    #     filter_args['etrap'] = selected_etrap
    
    # if number:
    #     filter_args['number__icontains'] = number
    
    # if comment:
    #     filter_args['comment__icontains'] = comment
    
    # if akt_raport:
    #     filter_args['akt_raport__icontains'] = akt_raport

    # if date_from:
    #     filter_args['date__gte'] = date_from  # Дата от
    
    # if date_to:
    #     filter_args['date__lte'] = date_to  # Дата до

    # # Получаем отфильтрованные данные
    # baza_changes = BazaChangeInfo.objects.filter(**filter_args).order_by('-date')[:100]

    # context['baza_changes'] = baza_changes
    # context['selected_etrap'] = selected_etrap
    # context['date_from'] = date_from
    # context['date_to'] = date_to
    # context['akt_raport'] = akt_raport
    # context['comment'] = comment
    # context['number'] = number

    return render(request, 'telekom/MATB/NachislitWruchnuyu/AlemNachisleniyaNew/alem_nach.html', context)
