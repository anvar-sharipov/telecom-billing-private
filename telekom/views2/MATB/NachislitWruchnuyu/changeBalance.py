# changeBalance
from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from datetime import datetime
from telekom.models import *
from telekom.views2.myFunc.myFunc import monthСonvert

from django.db import transaction
import logging
logger = logging.getLogger(__name__)





def changeBalance(request):
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    
    request_user = request.user
    groups = request_user.groups.all()
    request_user_etrap = ''
    request_user_type = ''
    allow_change_balance = False
    open_all_etrap = False
    for g in groups:
        request_user_etrap, request_user_type = g.name.split('_')
        if request_user_type == 'MTB':# or request.user.username == 'admin1':
            break

    if request_user_type != 'MTB' and (not request.user.is_superuser and request.user.username != 'admin1'):
        
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')
    
    for g in groups:
        ic(g.name, request_user.username)
        if g.name == "can_change_balance":
            ic("tut2")
            allow_change_balance = True
        if g.name == "open_all_etrap":
            open_all_etrap = True
            break
    allow_change_balance = True
    if request.user.is_superuser and request.user.username == "admin1":
        allow_change_balance = True
        open_all_etrap = True
        
    context = {}
    if not allow_change_balance:
        ic("tut")
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')
    
    context['allow_change_balance'] = allow_change_balance
    context['open_all_etrap'] = open_all_etrap
    context['etraps'] = etraps
    
    current_date = datetime.now().date()
    # formatted_date = current_date.strftime('%Y-%m-%d')
    # current_year, current_month, current_day = formatted_date.split('-')

    # context['formatted_date'] = formatted_date
    
    
    etrap = request.GET.get('etrap')
    number = request.GET.get('number')
    context['number'] = number
    context['etrap'] = etrap
    
    if etrap in etraps and number:
        allow = False
        if not open_all_etrap:
            if etrap == request_user_etrap:
                allow = True
        else:
            allow = True

        if not allow:
            messages.error(request, f"Выберите абонента с своего этрапа")
            return render(request, 'telekom/MATB/NachislitWruchnuyu/changeBalance.html', context)
        
        user_table_obj = False
        user_table = UserTable.objects.filter(etrap=etrap, number=number)
        if len(user_table) > 1:
            messages.error(request, f'Найдено больше 1 абонента UserTable')
        elif len(user_table) == 1 and len(number) == 5:
            user_table_obj = user_table[0]
        
        
        user_kabel_obj = False    
        user_kabel = False
        if etrap == "Dashoguz":
            user_kabel = KabelTvNew.objects.filter(number=number)
            if len(user_kabel) > 1:
                messages.error(request, f'Найдено больше 1 абонента KabelTvNew')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/changeBalance.html', context)
            elif len(user_kabel) == 1:
                user_kabel_obj = user_kabel[0]
                
        context["user_table"] = user_table
        context["user_kabel"] = user_kabel
        
        context["user_table_obj"] = user_table_obj
        context["user_kabel_obj"] = user_kabel_obj
        
        if len(number) < 5 or len(number) > 6:
            messages.error(request, f'Введите корректный номер')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/changeBalance.html', context)
        else:
            if len(number) > 5:
                context['only_kabel'] = True
    
    
    ic(etrap)
    ic(number)
    
    if request.method == 'POST' and etrap and number:
        comment = request.POST.get('comment')
        price = request.POST.get('price')
        type_ = request.POST.get('type')
        context["comment"] = comment
        context["price"] = price
        context["type_"] = type_

        
        
        if etrap not in etraps:
            messages.error(request, 'Введите этрап')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/changeBalance.html', context)
        try:
            price_float = float(price) if price != '' else 0
        except:
            messages.error(request, 'Введите цену')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/changeBalance.html', context)
           
        if type_ not in ["telefoniya", "internet", "alem", "kabel"]:
            messages.error(request, 'Введите тип')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/changeBalance.html', context)
        
        if len(comment) < 2:
            messages.error(request, 'Введите комментарий')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/changeBalance.html', context)
        
        if type_ == "kabel" and not user_kabel:
            messages.error(request, 'Абонент kabel не найден')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/changeBalance.html', context)
        
        if type_ in ["telefoniya", "internet", "alem"] and not user_table:
            messages.error(request, 'Абонент не найден')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/changeBalance.html', context)
        
        try:
            with transaction.atomic():
                if type_ == "kabel":
                    user = user_kabel[0]
                    old_balance = user.balance
                    user.balance = price_float
                    user.save()
                    ChangeBalanceWithComment.objects.create(
                        number=user.number,
                        etrap="Dashoguz",
                        surname=getattr(user, 'surname', ''),
                        name=getattr(user, 'name', ''),
                        street=getattr(user, 'street', ''),
                        home=getattr(user, 'home', ''),
                        flat=getattr(user, 'flat', ''),
                        operator=request.user.username,
                        operatorFK=request.user,
                        comment=comment,
                        old_balance=old_balance,
                        new_balance=price_float,
                        change_type="kabel",
                    )
                elif type_ in ["telefoniya", "internet", "alem"]:
                    user = user_table[0]
                    if type_ == "telefoniya":
                        old_balance = user.b_prochee + user.b_telefon + user.b_slr + user.b_kod + user.b_zakaz + user.b_dop_uslugi
                        user.b_prochee = price_float
                        user.b_telefon = 0
                        user.b_slr = 0
                        user.b_kod = 0
                        user.b_zakaz = 0
                        user.b_dop_uslugi = 0
                        user.save()
                        
                        ChangeBalanceWithComment.objects.create(
                            number=user.number,
                            etrap=etrap,
                            surname=getattr(user, 'surname', ''),
                            name=getattr(user, 'name', ''),
                            street=getattr(user, 'street', ''),
                            home=getattr(user, 'home', ''),
                            flat=getattr(user, 'flat', ''),
                            operator=request.user.username,
                            operatorFK=request.user,
                            comment=comment,
                            old_balance=old_balance,
                            new_balance=price_float,
                            change_type="telefoniya",
                        )
                    elif type_ == "internet":
                        old_balance = user.b_internet
                        user.b_internet = price_float
                        user.save()
                        
                        ChangeBalanceWithComment.objects.create(
                            number=user.number,
                            etrap=etrap,
                            surname=getattr(user, 'surname', ''),
                            name=getattr(user, 'name', ''),
                            street=getattr(user, 'street', ''),
                            home=getattr(user, 'home', ''),
                            flat=getattr(user, 'flat', ''),
                            operator=request.user.username,
                            operatorFK=request.user,
                            comment=comment,
                            old_balance=old_balance,
                            new_balance=price_float,
                            change_type="internet",
                        )
                    elif type_ == "alem":
                        old_balance = user.b_alem
                        user.b_alem = price_float
                        user.save()
                        
                        ChangeBalanceWithComment.objects.create(
                            number=user.number,
                            etrap=etrap,
                            surname=getattr(user, 'surname', ''),
                            name=getattr(user, 'name', ''),
                            street=getattr(user, 'street', ''),
                            home=getattr(user, 'home', ''),
                            flat=getattr(user, 'flat', ''),
                            operator=request.user.username,
                            operatorFK=request.user,
                            comment=comment,
                            old_balance=old_balance,
                            new_balance=price_float,
                            change_type="alem",
                        )
                        
                messages.success(request, 'Успешно')


        except Exception as e:
            messages.error(request, f'Ошибка при сохранении баланса: {e}')
            logger.error(f'Ошибка при сохранении баланса: {e}')
            
            
            
        
        
        
    
    return render(request, 'telekom/MATB/NachislitWruchnuyu/changeBalance.html', context)