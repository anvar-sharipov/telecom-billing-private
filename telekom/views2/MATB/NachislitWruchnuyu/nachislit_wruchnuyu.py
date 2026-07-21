from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from datetime import datetime
from telekom.models import *

from django.db import transaction
import logging
logger = logging.getLogger(__name__)




def nachislit_wruchnuyu(request):
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

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
    context['all_new_for_mtb'] = True

    context['etraps'] = etraps

    current_date = datetime.now().date()
    formatted_date = current_date.strftime('%Y-%m-%d')
    current_year, current_month, current_day = formatted_date.split('-')

    context['formatted_date'] = formatted_date
    context['current_year'] = current_year
    context['current_month'] = current_month
    context['current_day'] = current_day

    
    context['nachislit_wruchnuyu'] = True
    if request_user_type == 'MTB':
        context['matbIndex'] = True 
        context['request_user_etrap'] = request_user_etrap 

    etrap = request.GET.get('etrap')
    number = request.GET.get('number')
    context['number'] = number


    if etrap in etraps and number:

        allow = False
        if not request.user.is_superuser and request.user.username != 'admin1':
            if etrap == request_user_etrap:
                allow = True
        else:
            allow = True

        if not allow:
            messages.error(request, f"Выберите абонента с своего этрапа")
            return render(request, 'telekom/MATB/NachislitWruchnuyu/nachislit_wruchnuyu.html', context)


        if len(number) < 5 or len(number) > 6:
            messages.error(request, f'Введите корректный номер')
        else:
            if len(number) == 5:
                try:
                    user_table = UserTable.objects.get(number=number, etrap=etrap)
                    context['user_table'] = user_table
                except:
                    messages.error(request, 'Абонент не найден')
            if etrap == 'Dashoguz':
                try:
                    user_kabel = KabelTvNew.objects.get(number=number)
                except:
                    user_kabel = False
                context['user_kabel'] = user_kabel

    if request.method == 'POST':
        try:
            with transaction.atomic():
                price = request.POST.get('price')
                type_ = request.POST.get('type')
                year = request.POST.get('year')
                month = request.POST.get('month')
                comment = request.POST.get('comment')

                ic(price,type_, year, month, comment, etrap, request_user_etrap)
                

                if etrap not in etraps:
                    messages.error(request, 'Введите этрап')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/nachislit_wruchnuyu.html', context)

                price_float = float(price) if price != '' else 0
                if price_float == 0:
                    messages.error(request, 'Введите цену')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/nachislit_wruchnuyu.html', context)
                        
                if type_ == '':
                    messages.error(request, 'Введите тип')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/nachislit_wruchnuyu.html', context)
                if year == '':
                    messages.error(request, 'Введите год')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/nachislit_wruchnuyu.html', context)
                if month == '':
                    messages.error(request, 'Введите месяц')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/nachislit_wruchnuyu.html', context)
                if comment == '':
                    messages.error(request, 'Введите комментарий')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/nachislit_wruchnuyu.html', context)

                
                if type_ != 'kabel':
                    mess = f"""Информация о начислении вручную абонента: {user_table.number} {user_table.etrap}, месяц: {month}, год {year}:
            """
                    try:
                        user_nach = NachMinus.objects.get(year=year, month=month, user=user_table)
                    except:
                        user_nach = NachMinus(year=year, month=month, user=user_table)
                    
                    if type_ == 'telefoniya':
                        mess += f"""начисления на телефонию: {price_float} manat
            было начислено: {user_nach.telefon}
            стало начислено: {user_nach.telefon + price_float}
            было баланс перед начислением: {user_table.b_telefon + user_table.b_slr + user_table.b_kod + user_table.b_zakaz + user_table.b_prochee + user_table.b_dop_uslugi}
            стало баланс после начисления: {user_table.b_telefon + user_table.b_slr + user_table.b_kod + user_table.b_zakaz + user_table.b_prochee + user_table.b_dop_uslugi - price_float}
            """
                        user_nach.telefon += price_float
                        user_table.b_telefon -= price_float   

                    elif type_ == 'inrternet':
                        mess += f"""начисления на интернет: {price_float} manat
            было начислено: {user_nach.internet}
            стало начислено: {user_nach.internet + price_float}
            было баланс перед начислением: {user_table.b_internet}
            стало баланс после начисления: {user_table.b_internet - price_float}
            """
                        user_nach.internet += price_float
                        user_table.b_internet -= price_float

                    elif type_ == 'alem':
                        mess += f"""начисления на alem: {price_float} manat
            было начислено: {user_nach.alem}
            стало начислено: {user_nach.alem + price_float}
            было баланс перед начислением: {user_table.b_alem}
            стало баланс после начисления: {user_table.b_alem - price_float}
            """
                        user_nach.alem += price_float
                        user_table.b_alem -= price_float

                    user_nach.save()
                    user_table.save()
                        

                    NachislitWruchnuyuHistory.objects.create(
                        user = request.user.username,
                        column = type_,
                        price = price_float,
                        number = int(user_table.number),
                        etrap = user_table.etrap,
                        comment = f"""{mess}
            Комментарий: {comment}"""
                    )
                    messages.success(request, (f'Успешное начисление на сумму {str(price_float)} абонента {user_table.number} {user_table.etrap}'))





                else:
                    if user_kabel:
                        try:
                            user_kabel_nach = KabelNach.objects.get(user=user_kabel, year=year, month=month)
                        except:
                            user_kabel_nach = KabelNach(user=user_kabel, year=year, month=month)

                        mess = f"""Информация о начислении вручную кабельного: {user_kabel.number}, месяц: {month}, год {year}:
            начисления на kabel: {price_float} manat
            было начислено: {user_kabel_nach.nach}
            стало начислено: {user_kabel_nach.nach + price_float}
            было баланс перед начислением: {user_kabel.balance}
            стало баланс после начисления: {user_kabel.balance - price_float}
            Комментарий: {comment}
            """

                        user_kabel_nach.nach += price_float
                        user_kabel.balance -= price_float
                        user_kabel_nach.save()
                        user_kabel.save()

                        
                        
                        NachislitWruchnuyuHistory.objects.create(
                        user = request.user.username,
                        column = type_,
                        price = price_float,
                        number = int(user_kabel.number),
                        etrap = etrap,
                        comment = mess
                    )
                    messages.success(request, (f'Успешное начисление на сумму {str(price_float)} абонента кабельного {user_kabel.number}'))
        except Exception as e:
            messages.error(request, f'Откат начисления ошибка с transaction == {e}')
            logger.error(f'==== Откат начисления ошибка с transaction при начислении == {e}')
                    



                
            



                
        


    return render(request, 'telekom/MATB/NachislitWruchnuyu/nachislit_wruchnuyu.html', context)