from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from datetime import datetime
from telekom.models import *
from datetime import datetime, timedelta
import calendar
import tablib
from tablib import Dataset
from django.http import HttpResponse

import urllib.parse
from django.db import transaction

import logging

logger = logging.getLogger(__name__)




def check_pays(request):
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']

    request_user = request.user
    groups = request_user.groups.all()
    request_user_etrap = ''
    request_user_type = ''
    for g in groups:
        request_user_etrap, request_user_type = g.name.split('_')
        if request_user_type == 'MTB' or (request_user_type == 'SHB' and request.user.username == 'lenashb'):# or request.user.username == 'admin1':
            print('tut', request_user_type, request_user_etrap)
            break

    if request_user_type == 'SHB' and request.user.username != 'lenashb':
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')

    
    if request_user_type != 'MTB' and request_user_type != 'SHB' and (not request.user.is_superuser and request.user.username != 'admin1'):
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')
   
    context = {}
    context['all_new_for_mtb'] = True

    current_date = datetime.now().date()
    formatted_date = current_date.strftime('%Y-%m-%d')
    current_year, current_month, current_day = formatted_date.split('-')

    context['formatted_date'] = formatted_date
    context['current_year'] = current_year
    context['current_month'] = current_month
    context['current_day'] = current_day

    context['check_pays'] = True
    if request_user_type == 'MTB' or request_user_type == 'SHB':
        if request_user_type == 'MTB':
            context['matbIndex'] = True 
        if request_user_type == 'SHB':
            context['SHBIndex'] = True
        context['request_user_etrap'] = request_user_etrap 

    context['etraps'] = etraps

    etrap = request.GET.get('etrap')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    options = request.GET.get('options')

    context['options'] = options

    if etrap in etraps:
        allow = False
        if not request.user.is_superuser and request.user.username != 'admin1' and request.user.username != 'Gayyp':
            if etrap == request_user_etrap:
                allow = True
        else:
            allow = True
        if not allow:
            messages.error(request, f"Выберите абонента с своего этрапа")
            return render(request, 'telekom/MATB/NachislitWruchnuyu/check_pays.html', context)



    if etrap and date_from and date_to:

        # Преобразуем строки в объекты даты
        start_date = datetime.strptime(date_from, '%Y-%m-%d')
        end_date = datetime.strptime(date_to, '%Y-%m-%d')

        # Генерируем список дат
        date_list = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]
        context['len_date_list'] = len(date_list)

        managers_list = []
        managers_list_dict = {}
        closed_days = []

        # Проверяем, принадлежат ли обе даты одному году и одному месяцу (если нет то скрываем сохранения сверки)
        if start_date.year == end_date.year and start_date.month == end_date.month:
            # Получаем количество дней в месяце
            year = start_date.year
            month = start_date.month
            num_days = calendar.monthrange(year, month)[1]  # Получаем количество дней в данном месяце
            context['num_days'] = num_days
            mojno_nachislyat = True
            context['mojno_nachislyat'] = mojno_nachislyat
            print(f"Количество дней в месяце {month} {year}: {num_days}")
        else:
            mojno_nachislyat = False
            context['mojno_nachislyat'] = mojno_nachislyat
            print("Даты не принадлежат одному году и одному месяцу.")


        if request.user.username in ['intizar_gorogly', 'lenashb', 'testMTBDZ', 'AyshatGoroglyMtb', 'GuljahanAkdepeMtb', 'AzizShabatMtb', 'Saryyewa_Gozel_Shabat_MTB', 'BaharKoneurgenchKassa', 'Merjen_Yylally_MTB', 'GozelGubadagMtb', 'SelbiBoldumsazMtb', 'MahymAkdepeMtb', 'Aramedowa_Oguljemal', 'Kurbanowa_Gulnabat_Koneurgench', 'Baltabayewa_Sewara_MTB_DGE', 'Ishangulyyewa_Nurjemal_Koneurgench_kassa'] or (request.user.is_superuser and request.user.username == 'admin1'):
            context['allow_podtwerdit'] = True


        closed_days_dict = {}
        opened_days_list = []
        for d in date_list:
            get_day = CheckPaysWithKassirs.objects.filter(checked_date=d, etrap=etrap)
            for obj in get_day:
                if obj.day_is_closed:
                    closed_days_dict[d] = obj.who_close_the_day

            if d not in closed_days_dict:
                opened_days_list.append(d)
                
        context['closed_days_dict'] = closed_days_dict
        context['opened_days_list'] = opened_days_list

        
        if options == 'po_kassiram':
            pays = PayHistory.objects.filter(kassir_etrap=etrap, date__range=[date_from, f"{date_to} 23:59:59"])
        else:
            pays = PayHistory.objects.filter(abonent__etrap=etrap, date__range=[date_from, f"{date_to} 23:59:59"])

        if etrap == 'Dashoguz':
            pays_k = KabelTvPayHistory.objects.filter(pay_date__range=[date_from, f"{date_to} 23:59:59"])

        dict_ = {}
        total = {
            'telefoniya': 0,
            'internet': 0,
            'alem': 0,
            'kabel': 0,
            'umumy': 0,
        }

        for p in pays:
            pay_year = str(p.date.year)
            pay_month = str(p.date.month) if len(str(p.date.month)) == 2 else f"0{str(p.date.month)}"
            pay_day = str(p.date.day) if len(str(p.date.day)) == 2 else f"0{str(p.date.day)}"
            pay_date = f"{pay_year}-{pay_month}-{pay_day}"
            
            
            if pay_date not in managers_list_dict:
                managers_list_dict[pay_date] = [p.kassir]
            elif p.kassir not in managers_list_dict[pay_date]:
                managers_list_dict[pay_date].append(p.kassir)

            if p.kassir not in managers_list:
                managers_list.append(p.kassir)
                
                    
            telefoniya = p.prochee
            internet = p.internet
            alem = p.alem

            if p.kassir not in dict_:
                dict_[p.kassir] = {
                    'telefoniya': telefoniya,
                    'internet': internet,
                    'kabel': 0,
                    'alem': alem,
                    'total_kassir': telefoniya + internet + alem
                }
            else:
                dict_[p.kassir]['telefoniya'] += telefoniya
                dict_[p.kassir]['internet'] += internet
                dict_[p.kassir]['alem'] += alem
                dict_[p.kassir]['total_kassir'] += telefoniya + internet + alem

            
            total['telefoniya'] += telefoniya
            total['internet'] += internet
            total['alem'] += alem
            total['umumy'] += telefoniya + internet + alem
        if etrap == 'Dashoguz':
            for p in pays_k:
                pay_year = str(p.pay_date.year)
                pay_month = str(p.pay_date.month) if len(str(p.pay_date.month)) == 2 else f"0{str(p.pay_date.month)}"
                pay_day = str(p.pay_date.day) if len(str(p.pay_date.day)) == 2 else f"0{str(p.pay_date.day)}"
                pay_date = f"{pay_year}-{pay_month}-{pay_day}"
                
                if pay_date not in managers_list_dict:
                    managers_list_dict[pay_date] = [p.pay_kassir]
                elif p.pay_kassir not in managers_list_dict[pay_date]:
                    managers_list_dict[pay_date].append(p.pay_kassir)

                if p.pay_kassir not in managers_list:
                    managers_list.append(p.pay_kassir)
                kabel = p.pay
                if p.pay_kassir not in dict_:
                    dict_[p.pay_kassir] = {
                        'telefoniya': 0,
                        'internet': 0,
                        'kabel': kabel,
                        'alem': 0,
                        'total_kassir': kabel
                    }
                else:
                    dict_[p.pay_kassir]['kabel'] += kabel
                    dict_[p.pay_kassir]['total_kassir'] += kabel

                total['kabel'] += kabel
                total['umumy'] += kabel


        context['dict_'] = dict_
        context['total'] = total

        context['managers_list'] = managers_list

        cheked_days = []
        dont_cheked_days = []
        dont_cheked_days_dict = {} # {date: 'manager'}
        pks_checked_days = []
        dont_checked_managers_name = []
        day_is_closed = False
        for day_ in date_list:
            for m in managers_list:
                try:
                    obj = CheckPaysWithKassirs.objects.get(checked_date=day_, etrap=etrap, checked_kassir=m)

                    if len(date_list) == 1:
                        if obj.day_is_closed:
                            day_is_closed = True
                     

                    pks_checked_days.append(obj.pk)
                    cheked_days.append(day_)
                except:
                    dont_cheked_days.append(day_)
                    if day_ not in dont_cheked_days_dict:
                        if day_ in managers_list_dict:
                            if m in managers_list_dict[day_]:
                                dont_cheked_days_dict[day_] = {'managers_dict': [m]}
                    elif 'managers_dict' not in dont_cheked_days_dict[day_]:
                        if day_ in managers_list_dict:
                            if m in managers_list_dict[day_]:
                                dont_cheked_days_dict[day_] = {'managers_dict': [m]}
                    else:
                        if day_ in managers_list_dict:
                            if m in m in managers_list_dict[day_]:
                                dont_cheked_days_dict[day_]['managers_dict'].append(m)
                        
                    dont_checked_managers_name.append(m)
        context['cheked_days'] = cheked_days
        context['dont_cheked_days'] = dont_cheked_days
        context['dont_cheked_days_dict'] = dont_cheked_days_dict
        context['dont_checked_managers_name'] = dont_checked_managers_name
        context['closed_days'] = closed_days
        context['day_is_closed'] = day_is_closed

        if pks_checked_days:
            check_pays_obj = CheckPaysWithKassirs.objects.filter(pk__in=pks_checked_days)
        else:
            check_pays_obj = False
        context['check_pays_obj'] = check_pays_obj
        context['dontScroll'] = False

        # Если нажал на подтвердить
        if request.method == 'POST' and 'check_button' in request.POST:
            comment = request.POST.get('comment')
            kassir = request.POST.get('kassir')
            context['dontScroll'] = True
            if comment:
                if options == 'po_kassiram':
                    if mojno_nachislyat:
                        transaction_success_check = False
                        try:
                            with transaction.atomic():
                                for d in date_list:
                                    if CheckPaysWithKassirs.objects.filter(checked_date=d, etrap=etrap, checked_kassir=kassir).exists():
                                        # Уже сверено
                                        pass
                                    else:
                                        CheckPaysWithKassirs.objects.create(
                                            etrap=etrap,
                                            checked_date=d,
                                            checked_kassir=kassir,
                                            operator=request.user.username,
                                            comment=comment,
                                            total_telefon=dict_[kassir]['telefoniya'],
                                            total_alem=dict_[kassir]['alem'],
                                            total_internet=dict_[kassir]['internet'],
                                            total_kabel=dict_[kassir]['kabel'],
                                            itogo_kassir=dict_[kassir]['total_kassir']
                                        )
                                transaction_success_check = True
                        except Exception as e:
                            logger.warning(f"Не удалось подтвердить по причине {str(e)}")
                            messages.error(request, f'Не удалось подтвердить по причине {str(e)}')
                        if transaction_success_check:
                            messages.success(request, f'Подтверждено {date_list[0]}')
                        
                        # refresh
                        if etrap and date_from and date_to:

                            # Преобразуем строки в объекты даты
                            start_date = datetime.strptime(date_from, '%Y-%m-%d')
                            end_date = datetime.strptime(date_to, '%Y-%m-%d')

                            # Генерируем список дат
                            date_list = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]
                            context['len_date_list'] = len(date_list)

                            managers_list = []
                            managers_list_dict = {}
                            closed_days = []

                            # Проверяем, принадлежат ли обе даты одному году и одному месяцу (если нет то скрываем сохранения сверки)
                            if start_date.year == end_date.year and start_date.month == end_date.month:
                                # Получаем количество дней в месяце
                                year = start_date.year
                                month = start_date.month
                                num_days = calendar.monthrange(year, month)[1]  # Получаем количество дней в данном месяце
                                context['num_days'] = num_days
                                mojno_nachislyat = True
                                context['mojno_nachislyat'] = mojno_nachislyat
                                print(f"Количество дней в месяце {month} {year}: {num_days}")
                            else:
                                mojno_nachislyat = False
                                context['mojno_nachislyat'] = mojno_nachislyat
                                print("Даты не принадлежат одному году и одному месяцу.")



                            if options == 'po_kassiram':
                                pays = PayHistory.objects.filter(kassir_etrap=etrap, date__range=[date_from, f"{date_to} 23:59:59"])
                            else:
                                pays = PayHistory.objects.filter(abonent__etrap=etrap, date__range=[date_from, f"{date_to} 23:59:59"])

                            if etrap == 'Dashoguz':
                                pays_k = KabelTvPayHistory.objects.filter(pay_date__range=[date_from, f"{date_to} 23:59:59"])

                            dict_ = {}
                            total = {
                                'telefoniya': 0,
                                'internet': 0,
                                'alem': 0,
                                'kabel': 0,
                                'umumy': 0,
                            }

                            for p in pays:
                                pay_year = str(p.date.year)
                                pay_month = str(p.date.month) if len(str(p.date.month)) == 2 else f"0{str(p.date.month)}"
                                pay_day = str(p.date.day) if len(str(p.date.day)) == 2 else f"0{str(p.date.day)}"
                                pay_date = f"{pay_year}-{pay_month}-{pay_day}"
                                
                                
                                if pay_date not in managers_list_dict:
                                    managers_list_dict[pay_date] = [p.kassir]
                                elif p.kassir not in managers_list_dict[pay_date]:
                                    managers_list_dict[pay_date].append(p.kassir)

                                if p.kassir not in managers_list:
                                    managers_list.append(p.kassir)
                                    
                                        
                                telefoniya = p.prochee
                                internet = p.internet
                                alem = p.alem

                                if p.kassir not in dict_:
                                    dict_[p.kassir] = {
                                        'telefoniya': telefoniya,
                                        'internet': internet,
                                        'kabel': 0,
                                        'alem': alem,
                                        'total_kassir': telefoniya + internet + alem
                                    }
                                else:
                                    dict_[p.kassir]['telefoniya'] += telefoniya
                                    dict_[p.kassir]['internet'] += internet
                                    dict_[p.kassir]['alem'] += alem
                                    dict_[p.kassir]['total_kassir'] += telefoniya + internet + alem

                                
                                total['telefoniya'] += telefoniya
                                total['internet'] += internet
                                total['alem'] += alem
                                total['umumy'] += telefoniya + internet + alem
                            if etrap == 'Dashoguz':
                                for p in pays_k:
                                    pay_year = str(p.pay_date.year)
                                    pay_month = str(p.pay_date.month) if len(str(p.pay_date.month)) == 2 else f"0{str(p.pay_date.month)}"
                                    pay_day = str(p.pay_date.day) if len(str(p.pay_date.day)) == 2 else f"0{str(p.pay_date.day)}"
                                    pay_date = f"{pay_year}-{pay_month}-{pay_day}"
                                    
                                    if pay_date not in managers_list_dict:
                                        managers_list_dict[pay_date] = [p.pay_kassir]
                                    elif p.pay_kassir not in managers_list_dict[pay_date]:
                                        managers_list_dict[pay_date].append(p.pay_kassir)

                                    if p.pay_kassir not in managers_list:
                                        managers_list.append(p.pay_kassir)
                                    kabel = p.pay
                                    if p.pay_kassir not in dict_:
                                        dict_[p.pay_kassir] = {
                                            'telefoniya': 0,
                                            'internet': 0,
                                            'kabel': kabel,
                                            'alem': 0,
                                            'total_kassir': kabel
                                        }
                                    else:
                                        dict_[p.pay_kassir]['kabel'] += kabel
                                        dict_[p.pay_kassir]['total_kassir'] += kabel

                                    total['kabel'] += kabel
                                    total['umumy'] += kabel


                            context['dict_'] = dict_
                            context['total'] = total

                            context['managers_list'] = managers_list

                            cheked_days = []
                            dont_cheked_days = []
                            dont_cheked_days_dict = {} # {date: 'manager'}
                            pks_checked_days = []
                            dont_checked_managers_name = []
                            day_is_closed = False
                            for day_ in date_list:
                                for m in managers_list:
                                    try:
                                        obj = CheckPaysWithKassirs.objects.get(checked_date=day_, etrap=etrap, checked_kassir=m)

                                        if len(date_list) == 1:
                                            if obj.day_is_closed:
                                                day_is_closed = True
                                        

                                        pks_checked_days.append(obj.pk)
                                        cheked_days.append(day_)
                                    except:
                                        dont_cheked_days.append(day_)
                                        if day_ not in dont_cheked_days_dict:
                                            if day_ in managers_list_dict:
                                                if m in managers_list_dict[day_]:
                                                    dont_cheked_days_dict[day_] = {'managers_dict': [m]}
                                        elif 'managers_dict' not in dont_cheked_days_dict[day_]:
                                            if day_ in managers_list_dict:
                                                if m in managers_list_dict[day_]:
                                                    dont_cheked_days_dict[day_] = {'managers_dict': [m]}
                                        else:
                                            if day_ in managers_list_dict:
                                                if m in m in managers_list_dict[day_]:
                                                    dont_cheked_days_dict[day_]['managers_dict'].append(m)
                                            
                                        dont_checked_managers_name.append(m)
                            context['cheked_days'] = cheked_days
                            context['dont_cheked_days'] = dont_cheked_days
                            context['dont_cheked_days_dict'] = dont_cheked_days_dict
                            context['dont_checked_managers_name'] = dont_checked_managers_name
                            context['closed_days'] = closed_days
                            context['day_is_closed'] = day_is_closed

                            if pks_checked_days:
                                check_pays_obj = CheckPaysWithKassirs.objects.filter(pk__in=pks_checked_days)
                            else:
                                check_pays_obj = False
                            context['check_pays_obj'] = check_pays_obj
                            context['dontScroll'] = False
                    
                    else:
                        messages.error(request, 'Вы можете подтвердить только 1 день')
                else:
                    messages.error(request, 'Вы можете подтвердить только проверив по кассирам')
            else:
                messages.error(request, 'Оставьте комментарий')
        
        # Если нажал на скачать
        if request.method == 'POST' and 'download_pays' in request.POST:
            manager = request.POST.get('manager')
            ic('download_pays', manager)

            if pays:
                filtered_pays = pays.filter(kassir=manager)
            
            headers = ("number", "dogowors", "telefoniya", "internet", "alem", "kabel", "kassir", "date", "is_card")
            data = []
            data = tablib.Dataset(*data, headers=headers)
            
            if filtered_pays: 
                for i in filtered_pays:
                    dogowors = ''
                    if i.abonent.dogowor:
                        dogowors += i.abonent.dogowor
                    
                    old_dogowors = OldLoginDogowor.objects.filter(etrap=etrap, number=i.abonent.number)

                    if old_dogowors:
                        if dogowors != '':
                            for d in old_dogowors:
                                dogowors += f"{d.dogowor} "
                        else:
                            for d in old_dogowors:
                                dogowors += f" {d.dogowor} "

                    telefoniya = i.telefon + i.slr + i.kod + i.zakaz + i.dop_uslugi + i.prochee
                    is_card = ''
                    if i.is_card:
                        is_card = 'cart'
                    data.append((i.abonent.number, dogowors, telefoniya, i.internet, i.alem, 0, i.kassir, i.date, is_card))

            if etrap == 'Dashoguz':
                filtered_pays_k = pays_k.filter(pay_kassir=manager)

                if filtered_pays_k:
                    for i in filtered_pays_k:
                        is_card = ''
                        if i.card:
                            is_card = 'cart'

                        data.append((i.user.number, '', 0, 0, 0, i.pay, i.pay_kassir, i.pay_date, is_card))

            filename = f"tolegler_{manager}_{date_from}__{date_to}_{etrap}.xlsx"
            encoded_filename = urllib.parse.quote(filename.encode('utf-8'))
            
            response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
            response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
            return response 
        
        # Если нажал на закрыть
        if request.method == 'POST' and 'close_day' in request.POST:
            ic('close_day', check_pays_obj)
            count_dates = []
            for i in check_pays_obj:
                if i.checked_date not in count_dates:
                    count_dates.append(i.checked_date)

            if len(count_dates) == 1:
                transaction_success = False
                try: 
                    with transaction.atomic():
                        for i in check_pays_obj:
                            ic(i.checked_date)
                            i.day_is_closed = True
                            i.who_close_the_day = request.user.username,
                            i.total_telefon_when_closed_day = total['telefoniya']
                            i.total_alem_when_closed_day = total['alem']
                            i.total_internet_when_closed_day = total['internet']
                            i.total_kabel_when_closed_day = total['kabel']
                            i.itogo_when_closed_day = total['umumy']
                            i.save()
                        transaction_success = True
                except Exception as e:
                    logger.warning(f"Не удалось закрыть день по причине {str(e)}")
                    messages.error(request, f'Не удалось закрыть день по причине {str(e)}')

                # refresh
                if etrap and date_from and date_to:

                    # Преобразуем строки в объекты даты
                    start_date = datetime.strptime(date_from, '%Y-%m-%d')
                    end_date = datetime.strptime(date_to, '%Y-%m-%d')

                    # Генерируем список дат
                    date_list = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]
                    context['len_date_list'] = len(date_list)

                    managers_list = []
                    managers_list_dict = {}
                    closed_days = []

                    # Проверяем, принадлежат ли обе даты одному году и одному месяцу (если нет то скрываем сохранения сверки)
                    if start_date.year == end_date.year and start_date.month == end_date.month:
                        # Получаем количество дней в месяце
                        year = start_date.year
                        month = start_date.month
                        num_days = calendar.monthrange(year, month)[1]  # Получаем количество дней в данном месяце
                        context['num_days'] = num_days
                        mojno_nachislyat = True
                        context['mojno_nachislyat'] = mojno_nachislyat
                        print(f"Количество дней в месяце {month} {year}: {num_days}")
                    else:
                        mojno_nachislyat = False
                        context['mojno_nachislyat'] = mojno_nachislyat
                        print("Даты не принадлежат одному году и одному месяцу.")



                    if options == 'po_kassiram':
                        pays = PayHistory.objects.filter(kassir_etrap=etrap, date__range=[date_from, f"{date_to} 23:59:59"])
                    else:
                        pays = PayHistory.objects.filter(abonent__etrap=etrap, date__range=[date_from, f"{date_to} 23:59:59"])

                    if etrap == 'Dashoguz':
                        pays_k = KabelTvPayHistory.objects.filter(pay_date__range=[date_from, f"{date_to} 23:59:59"])

                    dict_ = {}
                    total = {
                        'telefoniya': 0,
                        'internet': 0,
                        'alem': 0,
                        'kabel': 0,
                        'umumy': 0,
                    }

                    for p in pays:
                        pay_year = str(p.date.year)
                        pay_month = str(p.date.month) if len(str(p.date.month)) == 2 else f"0{str(p.date.month)}"
                        pay_day = str(p.date.day) if len(str(p.date.day)) == 2 else f"0{str(p.date.day)}"
                        pay_date = f"{pay_year}-{pay_month}-{pay_day}"
                        
                        
                        if pay_date not in managers_list_dict:
                            managers_list_dict[pay_date] = [p.kassir]
                        elif p.kassir not in managers_list_dict[pay_date]:
                            managers_list_dict[pay_date].append(p.kassir)

                        if p.kassir not in managers_list:
                            managers_list.append(p.kassir)
                            
                                
                        telefoniya = p.prochee
                        internet = p.internet
                        alem = p.alem

                        if p.kassir not in dict_:
                            dict_[p.kassir] = {
                                'telefoniya': telefoniya,
                                'internet': internet,
                                'kabel': 0,
                                'alem': alem,
                                'total_kassir': telefoniya + internet + alem
                            }
                        else:
                            dict_[p.kassir]['telefoniya'] += telefoniya
                            dict_[p.kassir]['internet'] += internet
                            dict_[p.kassir]['alem'] += alem
                            dict_[p.kassir]['total_kassir'] += telefoniya + internet + alem

                        
                        total['telefoniya'] += telefoniya
                        total['internet'] += internet
                        total['alem'] += alem
                        total['umumy'] += telefoniya + internet + alem
                    if etrap == 'Dashoguz':
                        for p in pays_k:
                            pay_year = str(p.pay_date.year)
                            pay_month = str(p.pay_date.month) if len(str(p.pay_date.month)) == 2 else f"0{str(p.pay_date.month)}"
                            pay_day = str(p.pay_date.day) if len(str(p.pay_date.day)) == 2 else f"0{str(p.pay_date.day)}"
                            pay_date = f"{pay_year}-{pay_month}-{pay_day}"
                            
                            if pay_date not in managers_list_dict:
                                managers_list_dict[pay_date] = [p.pay_kassir]
                            elif p.pay_kassir not in managers_list_dict[pay_date]:
                                managers_list_dict[pay_date].append(p.pay_kassir)

                            if p.pay_kassir not in managers_list:
                                managers_list.append(p.pay_kassir)
                            kabel = p.pay
                            if p.pay_kassir not in dict_:
                                dict_[p.pay_kassir] = {
                                    'telefoniya': 0,
                                    'internet': 0,
                                    'kabel': kabel,
                                    'alem': 0,
                                    'total_kassir': kabel
                                }
                            else:
                                dict_[p.pay_kassir]['kabel'] += kabel
                                dict_[p.pay_kassir]['total_kassir'] += kabel

                            total['kabel'] += kabel
                            total['umumy'] += kabel


                    context['dict_'] = dict_
                    context['total'] = total

                    context['managers_list'] = managers_list

                    cheked_days = []
                    dont_cheked_days = []
                    dont_cheked_days_dict = {} # {date: 'manager'}
                    pks_checked_days = []
                    dont_checked_managers_name = []
                    day_is_closed = False
                    for day_ in date_list:
                        for m in managers_list:
                            try:
                                obj = CheckPaysWithKassirs.objects.get(checked_date=day_, etrap=etrap, checked_kassir=m)

                                if len(date_list) == 1:
                                    if obj.day_is_closed:
                                        day_is_closed = True
                                

                                pks_checked_days.append(obj.pk)
                                cheked_days.append(day_)
                            except:
                                dont_cheked_days.append(day_)
                                if day_ not in dont_cheked_days_dict:
                                    if day_ in managers_list_dict:
                                        if m in managers_list_dict[day_]:
                                            dont_cheked_days_dict[day_] = {'managers_dict': [m]}
                                elif 'managers_dict' not in dont_cheked_days_dict[day_]:
                                    if day_ in managers_list_dict:
                                        if m in managers_list_dict[day_]:
                                            dont_cheked_days_dict[day_] = {'managers_dict': [m]}
                                else:
                                    if day_ in managers_list_dict:
                                        if m in m in managers_list_dict[day_]:
                                            dont_cheked_days_dict[day_]['managers_dict'].append(m)
                                    
                                dont_checked_managers_name.append(m)
                    context['cheked_days'] = cheked_days
                    context['dont_cheked_days'] = dont_cheked_days
                    context['dont_cheked_days_dict'] = dont_cheked_days_dict
                    context['dont_checked_managers_name'] = dont_checked_managers_name
                    context['closed_days'] = closed_days
                    context['day_is_closed'] = day_is_closed

                    if pks_checked_days:
                        check_pays_obj = CheckPaysWithKassirs.objects.filter(pk__in=pks_checked_days)
                    else:
                        check_pays_obj = False
                    context['check_pays_obj'] = check_pays_obj
                    context['dontScroll'] = False
                if transaction_success:
                    messages.success(request, 'Успешное закрытие дня')    
            else:
                messages.error(request, 'Выбеите только 1 день')

        # Если нажал на удалить платеж
        if request.method == 'POST' and 'delete_pays' in request.POST and request.user.is_superuser and request.user.username == 'admin1':
            ic('delete pays')
            kassir_for_delete = request.POST.get('kassir_for_delete')
            date_delete = request.POST.get('date_delete')
            comment_for_delete = request.POST.get('comment_for_delete')

            if comment_for_delete:

                if len(date_list) == 1:
                    
                    # Ищем с PayHistory
                    pays_del = PayHistory.objects.filter(date__date=date_delete, kassir=kassir_for_delete)
                    

                    # Ищем платежи KabelTvPayHistory если Dashoguz
                    if etrap == 'Dashoguz':
                        pays_del_k = KabelTvPayHistory.objects.filter(pay_date__date=date_delete, pay_kassir=kassir_for_delete)

                    # Ищем с PlatejiWhichAddKassirsEveryDay
                    pays_from_billing = PlatejiWhichAddKassirsEveryDay.objects.filter(date=date_delete, manager=kassir_for_delete)
                    mes = ''
                    if pays_from_billing:
                        manager_names = []
                        file_names = []
                        for p in pays_from_billing:
                            if p.manager not in manager_names:
                                manager_names.append(p.manager)
                            if p.file_name not in file_names:
                                file_names.append(p.file_name)

                        if file_names:
                            print('tut0', file_names)
                            # info_obj = False
                            if len(file_names) == 1:
                                try:
                                    info_obj = SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.get(file_name=file_names[0])
                                    mes += ' file_names correct'
                                except:
                                    info_obj = False
                                    mes += ' error:file_names cant_find'
                            else:
                                mes += ' error:file_names > 1'
                        else:
                            mes += ' error:file_names пустой'
                    else:
                        mes += ' error:pays_from_billing пустой'
                    
                    
                    # тут удалять
                    try:
                        with transaction.atomic():
                            # минусуем с балансов PayHistory
                            if pays_del:
                                for i in pays_del:
                                    user = i.abonent
                                    if i.telefon != 0:
                                        user.b_telefon -= i.telefon
                                    if i.slr != 0:
                                        user.b_slr -= i.slr
                                    if i.kod != 0:
                                        user.b_kod -= i.kod
                                    if i.zakaz != 0:
                                        user.b_zakaz -= i.zakaz
                                    if i.prochee != 0:
                                        user.b_prochee -= i.prochee
                                    if i.dop_uslugi != 0:
                                        user.b_dop_uslugi -= i.dop_uslugi
                                    if i.internet != 0:
                                        user.b_internet -= i.internet
                                    if i.alem != 0:
                                        user.b_alem -= i.alem
                                    user.save()
                            
                                # Удаляем с PayHistory
                                pays_del.delete()

                            # минусуем с балансов KabelTvPayHistory (если Dashoguz)
                            if etrap == 'Dashoguz' and pays_del_k:
                                for i in pays_del_k:
                                    user_k = i.user
                                    user_k.balance -= i.pay
                                    user_k.save()
                                
                                # Удаляем с KabelTvPayHistory (если Dashoguz)
                                pays_del_k.delete()

                            # Удаляем с PlatejiWhichAddKassirsEveryDay
                            if pays_from_billing:
                                mes += ' так же удалили с PlatejiWhichAddKassirsEveryDay'
                                pays_from_billing.delete()
                                print('tut1')
                                if info_obj:
                                    info_obj.is_delete = True
                                    info_obj.comment = comment_for_delete
                                    info_obj.when_delete = datetime.now()
                                    info_obj.manager = manager_names
                                    info_obj.date_delete = date_delete
                                    info_obj.save()
                                    mes += ' есть инфа в SaveInfoAboutWhoAddAndNachPaysFromBilling'
                                else:
                                    mes += ' нет инфы в SaveInfoAboutWhoAddAndNachPaysFromBilling'
                                print('tut2')
                            else:
                                mes += ' нет платежей в PlatejiWhichAddKassirsEveryDay'

                            

                    except Exception as e:
                        messages.error(request, f'откат записей, ошибка в {str(e)}')
                        return render(request, 'telekom/MATB/NachislitWruchnuyu/check_pays.html', context)
                   
                    # refresh
                    if etrap and date_from and date_to:

                        # Преобразуем строки в объекты даты
                        start_date = datetime.strptime(date_from, '%Y-%m-%d')
                        end_date = datetime.strptime(date_to, '%Y-%m-%d')

                        # Генерируем список дат
                        date_list = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]
                        context['len_date_list'] = len(date_list)

                        managers_list = []
                        managers_list_dict = {}
                        closed_days = []

                        # Проверяем, принадлежат ли обе даты одному году и одному месяцу (если нет то скрываем сохранения сверки)
                        if start_date.year == end_date.year and start_date.month == end_date.month:
                            # Получаем количество дней в месяце
                            year = start_date.year
                            month = start_date.month
                            num_days = calendar.monthrange(year, month)[1]  # Получаем количество дней в данном месяце
                            context['num_days'] = num_days
                            mojno_nachislyat = True
                            context['mojno_nachislyat'] = mojno_nachislyat
                            print(f"Количество дней в месяце {month} {year}: {num_days}")
                        else:
                            mojno_nachislyat = False
                            context['mojno_nachislyat'] = mojno_nachislyat
                            print("Даты не принадлежат одному году и одному месяцу.")



                        if options == 'po_kassiram':
                            pays = PayHistory.objects.filter(kassir_etrap=etrap, date__range=[date_from, f"{date_to} 23:59:59"])
                        else:
                            pays = PayHistory.objects.filter(abonent__etrap=etrap, date__range=[date_from, f"{date_to} 23:59:59"])

                        if etrap == 'Dashoguz':
                            pays_k = KabelTvPayHistory.objects.filter(pay_date__range=[date_from, f"{date_to} 23:59:59"])

                        dict_ = {}
                        total = {
                            'telefoniya': 0,
                            'internet': 0,
                            'alem': 0,
                            'kabel': 0,
                            'umumy': 0,
                        }

                        for p in pays:
                            pay_year = str(p.date.year)
                            pay_month = str(p.date.month) if len(str(p.date.month)) == 2 else f"0{str(p.date.month)}"
                            pay_day = str(p.date.day) if len(str(p.date.day)) == 2 else f"0{str(p.date.day)}"
                            pay_date = f"{pay_year}-{pay_month}-{pay_day}"
                            
                            
                            if pay_date not in managers_list_dict:
                                managers_list_dict[pay_date] = [p.kassir]
                            elif p.kassir not in managers_list_dict[pay_date]:
                                managers_list_dict[pay_date].append(p.kassir)

                            if p.kassir not in managers_list:
                                managers_list.append(p.kassir)
                                
                                    
                            telefoniya = p.prochee
                            internet = p.internet
                            alem = p.alem

                            if p.kassir not in dict_:
                                dict_[p.kassir] = {
                                    'telefoniya': telefoniya,
                                    'internet': internet,
                                    'kabel': 0,
                                    'alem': alem,
                                    'total_kassir': telefoniya + internet + alem
                                }
                            else:
                                dict_[p.kassir]['telefoniya'] += telefoniya
                                dict_[p.kassir]['internet'] += internet
                                dict_[p.kassir]['alem'] += alem
                                dict_[p.kassir]['total_kassir'] += telefoniya + internet + alem

                            
                            total['telefoniya'] += telefoniya
                            total['internet'] += internet
                            total['alem'] += alem
                            total['umumy'] += telefoniya + internet + alem
                        if etrap == 'Dashoguz':
                            for p in pays_k:
                                pay_year = str(p.pay_date.year)
                                pay_month = str(p.pay_date.month) if len(str(p.pay_date.month)) == 2 else f"0{str(p.pay_date.month)}"
                                pay_day = str(p.pay_date.day) if len(str(p.pay_date.day)) == 2 else f"0{str(p.pay_date.day)}"
                                pay_date = f"{pay_year}-{pay_month}-{pay_day}"
                                
                                if pay_date not in managers_list_dict:
                                    managers_list_dict[pay_date] = [p.pay_kassir]
                                elif p.pay_kassir not in managers_list_dict[pay_date]:
                                    managers_list_dict[pay_date].append(p.pay_kassir)

                                if p.pay_kassir not in managers_list:
                                    managers_list.append(p.pay_kassir)
                                kabel = p.pay
                                if p.pay_kassir not in dict_:
                                    dict_[p.pay_kassir] = {
                                        'telefoniya': 0,
                                        'internet': 0,
                                        'kabel': kabel,
                                        'alem': 0,
                                        'total_kassir': kabel
                                    }
                                else:
                                    dict_[p.pay_kassir]['kabel'] += kabel
                                    dict_[p.pay_kassir]['total_kassir'] += kabel

                                total['kabel'] += kabel
                                total['umumy'] += kabel


                        context['dict_'] = dict_
                        context['total'] = total

                        context['managers_list'] = managers_list

                        cheked_days = []
                        dont_cheked_days = []
                        dont_cheked_days_dict = {} # {date: 'manager'}
                        pks_checked_days = []
                        dont_checked_managers_name = []
                        day_is_closed = False
                        for day_ in date_list:
                            for m in managers_list:
                                try:
                                    obj = CheckPaysWithKassirs.objects.get(checked_date=day_, etrap=etrap, checked_kassir=m)

                                    if len(date_list) == 1:
                                        if obj.day_is_closed:
                                            day_is_closed = True
                                    

                                    pks_checked_days.append(obj.pk)
                                    cheked_days.append(day_)
                                except:
                                    dont_cheked_days.append(day_)
                                    if day_ not in dont_cheked_days_dict:
                                        if day_ in managers_list_dict:
                                            if m in managers_list_dict[day_]:
                                                dont_cheked_days_dict[day_] = {'managers_dict': [m]}
                                    elif 'managers_dict' not in dont_cheked_days_dict[day_]:
                                        if day_ in managers_list_dict:
                                            if m in managers_list_dict[day_]:
                                                dont_cheked_days_dict[day_] = {'managers_dict': [m]}
                                    else:
                                        if day_ in managers_list_dict:
                                            if m in m in managers_list_dict[day_]:
                                                dont_cheked_days_dict[day_]['managers_dict'].append(m)
                                        
                                    dont_checked_managers_name.append(m)
                        context['cheked_days'] = cheked_days
                        context['dont_cheked_days'] = dont_cheked_days
                        context['dont_cheked_days_dict'] = dont_cheked_days_dict
                        context['dont_checked_managers_name'] = dont_checked_managers_name
                        context['closed_days'] = closed_days
                        context['day_is_closed'] = day_is_closed

                        if pks_checked_days:
                            check_pays_obj = CheckPaysWithKassirs.objects.filter(pk__in=pks_checked_days)
                        else:
                            check_pays_obj = False
                        context['check_pays_obj'] = check_pays_obj
                        context['dontScroll'] = False
            
                    
                        


                    
                
                    messages.success(request, f'Успешное удаление платежей {mes}')
                else:
                    messages.success(request, 'Выберите 1 день')
            else:
                messages.error(request, f'Оставьте комментарий')     
       
        # if request.method == 'POST' and 'delete_pays' in request.POST and request.user.is_superuser and request.user.username == 'admin1':
        #     ic('delete pays')
        #     kassir_for_delete = request.POST.get('kassir_for_delete')
        #     date_delete = request.POST.get('date_delete')
        #     ic(kassir_for_delete, date_delete)

        #     if len(date_list) == 1:

        #         pays_del = PayHistory.objects.filter(date__date=date_delete, kassir=kassir_for_delete)
         
        #         for i in pays_del:
        #             user = i.abonent
        #             if i.telefon != 0:
        #                 user.b_telefon -= i.telefon
        #             if i.slr != 0:
        #                 user.b_slr -= i.slr
        #             if i.kod != 0:
        #                 user.b_kod -= i.kod
        #             if i.zakaz != 0:
        #                 user.b_zakaz -= i.zakaz
        #             if i.prochee != 0:
        #                 user.b_prochee -= i.prochee
        #             if i.dop_uslugi != 0:
        #                 user.b_dop_uslugi -= i.dop_uslugi
        #             if i.internet != 0:
        #                 user.b_internet -= i.internet
        #             if i.alem != 0:
        #                 user.b_alem -= i.alem
        #             user.save()

        #         pays_del.delete()

        #         if etrap == 'Dashoguz':
        #             pays_del_k = KabelTvPayHistory.objects.filter(pay_date__date=date_delete, pay_kassir=kassir_for_delete)

        #             for i in pays_del_k:
        #                 user = i.user
        #                 user.balance -= i.pay
        #                 user.save()

        #             pays_del_k.delete()

        #         # refresh
        #         if etrap and date_from and date_to:

        #             # Преобразуем строки в объекты даты
        #             start_date = datetime.strptime(date_from, '%Y-%m-%d')
        #             end_date = datetime.strptime(date_to, '%Y-%m-%d')

        #             # Генерируем список дат
        #             date_list = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]
        #             context['len_date_list'] = len(date_list)

        #             managers_list = []
        #             managers_list_dict = {}
        #             closed_days = []

        #             # Проверяем, принадлежат ли обе даты одному году и одному месяцу (если нет то скрываем сохранения сверки)
        #             if start_date.year == end_date.year and start_date.month == end_date.month:
        #                 # Получаем количество дней в месяце
        #                 year = start_date.year
        #                 month = start_date.month
        #                 num_days = calendar.monthrange(year, month)[1]  # Получаем количество дней в данном месяце
        #                 context['num_days'] = num_days
        #                 mojno_nachislyat = True
        #                 context['mojno_nachislyat'] = mojno_nachislyat
        #                 print(f"Количество дней в месяце {month} {year}: {num_days}")
        #             else:
        #                 mojno_nachislyat = False
        #                 context['mojno_nachislyat'] = mojno_nachislyat
        #                 print("Даты не принадлежат одному году и одному месяцу.")



        #             if options == 'po_kassiram':
        #                 pays = PayHistory.objects.filter(kassir_etrap=etrap, date__range=[date_from, f"{date_to} 23:59:59"])
        #             else:
        #                 pays = PayHistory.objects.filter(abonent__etrap=etrap, date__range=[date_from, f"{date_to} 23:59:59"])

        #             if etrap == 'Dashoguz':
        #                 pays_k = KabelTvPayHistory.objects.filter(pay_date__range=[date_from, f"{date_to} 23:59:59"])

        #             dict_ = {}
        #             total = {
        #                 'telefoniya': 0,
        #                 'internet': 0,
        #                 'alem': 0,
        #                 'kabel': 0,
        #                 'umumy': 0,
        #             }

        #             for p in pays:
        #                 pay_year = str(p.date.year)
        #                 pay_month = str(p.date.month) if len(str(p.date.month)) == 2 else f"0{str(p.date.month)}"
        #                 pay_day = str(p.date.day) if len(str(p.date.day)) == 2 else f"0{str(p.date.day)}"
        #                 pay_date = f"{pay_year}-{pay_month}-{pay_day}"
                        
                        
        #                 if pay_date not in managers_list_dict:
        #                     managers_list_dict[pay_date] = [p.kassir]
        #                 elif p.kassir not in managers_list_dict[pay_date]:
        #                     managers_list_dict[pay_date].append(p.kassir)

        #                 if p.kassir not in managers_list:
        #                     managers_list.append(p.kassir)
                            
                                
        #                 telefoniya = p.prochee
        #                 internet = p.internet
        #                 alem = p.alem

        #                 if p.kassir not in dict_:
        #                     dict_[p.kassir] = {
        #                         'telefoniya': telefoniya,
        #                         'internet': internet,
        #                         'kabel': 0,
        #                         'alem': alem,
        #                         'total_kassir': telefoniya + internet + alem
        #                     }
        #                 else:
        #                     dict_[p.kassir]['telefoniya'] += telefoniya
        #                     dict_[p.kassir]['internet'] += internet
        #                     dict_[p.kassir]['alem'] += alem
        #                     dict_[p.kassir]['total_kassir'] += telefoniya + internet + alem

                        
        #                 total['telefoniya'] += telefoniya
        #                 total['internet'] += internet
        #                 total['alem'] += alem
        #                 total['umumy'] += telefoniya + internet + alem
        #             if etrap == 'Dashoguz':
        #                 for p in pays_k:
        #                     pay_year = str(p.pay_date.year)
        #                     pay_month = str(p.pay_date.month) if len(str(p.pay_date.month)) == 2 else f"0{str(p.pay_date.month)}"
        #                     pay_day = str(p.pay_date.day) if len(str(p.pay_date.day)) == 2 else f"0{str(p.pay_date.day)}"
        #                     pay_date = f"{pay_year}-{pay_month}-{pay_day}"
                            
        #                     if pay_date not in managers_list_dict:
        #                         managers_list_dict[pay_date] = [p.pay_kassir]
        #                     elif p.pay_kassir not in managers_list_dict[pay_date]:
        #                         managers_list_dict[pay_date].append(p.pay_kassir)

        #                     if p.pay_kassir not in managers_list:
        #                         managers_list.append(p.pay_kassir)
        #                     kabel = p.pay
        #                     if p.pay_kassir not in dict_:
        #                         dict_[p.pay_kassir] = {
        #                             'telefoniya': 0,
        #                             'internet': 0,
        #                             'kabel': kabel,
        #                             'alem': 0,
        #                             'total_kassir': kabel
        #                         }
        #                     else:
        #                         dict_[p.pay_kassir]['kabel'] += kabel
        #                         dict_[p.pay_kassir]['total_kassir'] += kabel

        #                     total['kabel'] += kabel
        #                     total['umumy'] += kabel


        #             context['dict_'] = dict_
        #             context['total'] = total

        #             context['managers_list'] = managers_list

        #             cheked_days = []
        #             dont_cheked_days = []
        #             dont_cheked_days_dict = {} # {date: 'manager'}
        #             pks_checked_days = []
        #             dont_checked_managers_name = []
        #             day_is_closed = False
        #             for day_ in date_list:
        #                 for m in managers_list:
        #                     try:
        #                         obj = CheckPaysWithKassirs.objects.get(checked_date=day_, etrap=etrap, checked_kassir=m)

        #                         if len(date_list) == 1:
        #                             if obj.day_is_closed:
        #                                 day_is_closed = True
                                

        #                         pks_checked_days.append(obj.pk)
        #                         cheked_days.append(day_)
        #                     except:
        #                         dont_cheked_days.append(day_)
        #                         if day_ not in dont_cheked_days_dict:
        #                             if day_ in managers_list_dict:
        #                                 if m in managers_list_dict[day_]:
        #                                     dont_cheked_days_dict[day_] = {'managers_dict': [m]}
        #                         elif 'managers_dict' not in dont_cheked_days_dict[day_]:
        #                             if day_ in managers_list_dict:
        #                                 if m in managers_list_dict[day_]:
        #                                     dont_cheked_days_dict[day_] = {'managers_dict': [m]}
        #                         else:
        #                             if day_ in managers_list_dict:
        #                                 if m in m in managers_list_dict[day_]:
        #                                     dont_cheked_days_dict[day_]['managers_dict'].append(m)
                                    
        #                         dont_checked_managers_name.append(m)
        #             context['cheked_days'] = cheked_days
        #             context['dont_cheked_days'] = dont_cheked_days
        #             context['dont_cheked_days_dict'] = dont_cheked_days_dict
        #             context['dont_checked_managers_name'] = dont_checked_managers_name
        #             context['closed_days'] = closed_days
        #             context['day_is_closed'] = day_is_closed

        #             if pks_checked_days:
        #                 check_pays_obj = CheckPaysWithKassirs.objects.filter(pk__in=pks_checked_days)
        #             else:
        #                 check_pays_obj = False
        #             context['check_pays_obj'] = check_pays_obj
        #             context['dontScroll'] = False
            
             
        #         messages.success(request, 'Успешное удаление платежей')
        #     else:
        #         messages.success(request, 'Выберите 1 день')


    return render(request, 'telekom/MATB/NachislitWruchnuyu/check_pays.html', context)