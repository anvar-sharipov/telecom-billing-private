from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from datetime import datetime
from telekom.models import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from django.db import transaction

from django.utils import timezone


import logging
logger = logging.getLogger(__name__)




def pays_with_comment(request):

    # test = UserTable.objects.get(number='99922', etrap='Dashoguz')
    # test.b_telefon = 0
    # test.b_slr = 0
    # test.b_kod = 0
    # test.b_zakaz = 0
    # test.b_prochee = 0
    # test.b_dop_uslugi = 0
    # test.b_internet = 0
    # test.b_alem = 0
    # test.b_kabel = 0
    # test.save()
    # # PayHistory.objects.filter(abonent = test).delete()
    # test2 = KabelTvNew.objects.get(number=99922)
    # test2.balance = 0
    # test2.save()
    # # KabelTvPayHistory.objects.filter(user=test2).delete()
    
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    request_user = request.user
    groups = request_user.groups.all()
    request_user_etrap = ''
    request_user_type = ''
    for g in groups:
        request_user_etrap, request_user_type = g.name.split('_')
        if request_user_type == 'MTB':# or request.user.username == 'admin1':
            break

    if request_user_type != 'MTB' and (not request.user.is_superuser and request.user.username != 'admin1') and (request.user.username != 'lenashb'):
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')

    context = {}

    context['pays_with_comment'] = True
    context['etraps'] = etraps
    context['all_new_for_mtb'] = True

    current_date = datetime.now().date()
    formatted_date = current_date.strftime('%Y-%m-%d')
    current_year, current_month, current_day = formatted_date.split('-')

    context['formatted_date'] = formatted_date
    context['current_year'] = current_year
    context['current_month'] = current_month
    context['current_day'] = current_day
    if (request.user.is_superuser and request.user.username == 'admin1') or request.user.username == 'lenashb':
        request_user_etrap = 'Dashoguz'
        context['request_user_etrap'] = request_user_etrap 
    
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
            return render(request, 'telekom/MATB/NachislitWruchnuyu/pays_with_comment.html', context)


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
            price = request.POST.get('price')
            type_ = request.POST.get('type')
            comment = request.POST.get('comment')
            customDate = request.POST.get('customDate')

            if customDate:
                pay_datetime = datetime.strptime(customDate, '%Y-%m-%d').replace(hour=15, minute=0)
                # pay_datetime = timezone.make_aware(pay_datetime) # dlya postgres
                pay_datetime = datetime.strptime(customDate, '%Y-%m-%d').replace(hour=15, minute=0) # dlya sqlite3
            else:
                messages.error(request, f"Выберите дату платежа")
                return render(request, 'telekom/MATB/NachislitWruchnuyu/pays_with_comment.html', context)
            
        
            if datetime.strptime(customDate, '%Y-%m-%d').date() > current_date:
                messages.error(request, f"Вы не можете оплатить за будущие даты")
                return render(request, 'telekom/MATB/NachislitWruchnuyu/pays_with_comment.html', context)
            

            if etrap not in etraps:
                messages.error(request, 'Введите этрап')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/pays_with_comment.html', context)
            price_float = float(price) if price != '' else 0
            if price_float == 0:
                messages.error(request, 'Введите цену')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/pays_with_comment.html', context)
            if type_ == '':
                messages.error(request, 'Введите тип')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/pays_with_comment.html', context)
            if len(comment) < 12:
                messages.error(request, 'Введите комментарий')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/pays_with_comment.html', context)
            
            save_user = False
            save_kabel = False
            if type_ != 'kabel':
                edata_ilat = 'ЮЛ' if user_table.is_enterprises else 'ФЛ'
                pay = PayHistory(abonent=user_table, **{type_:price_float}, kassir=request.user.username, kassa=request.user.username, total=price_float, date=pay_datetime, edara_ilat=edata_ilat, type='MATB', kassir_etrap=request_user_etrap)
                if type_ == 'prochee':
                    user_table.b_prochee += price_float
                elif type_ == 'internet':
                    user_table.b_internet += price_float
                elif type_ == 'alem':
                    user_table.b_alem += price_float
                save_user = True
                
            else:
                pay = KabelTvPayHistory(user=user_kabel, pay=price_float, pay_date=pay_datetime, pay_kassir=request.user.username)
                user_kabel.balance += price_float
                save_kabel = True


            

            try:
                with transaction.atomic():
                    pay.save()
                    pay_pk = pay.pk
                    if save_user:
                        user_table.save()
                    if save_kabel:
                        user_kabel.save()
                    pay_comment = PaysWithComment(number=number, etrap=etrap, operator=request.user.username, comment=comment, **{type_: price_float}, date_pay=pay_datetime, pays_pk=pay_pk)
                    pay_comment.save()
                    messages.success(request, 'Успешно')
            except Exception as e:
                    logger.warning(f"Ошибка! {str(e)}")
                    messages.error(request, f'Ошибка! {str(e)}')

    return render(request, 'telekom/MATB/NachislitWruchnuyu/pays_with_comment.html', context)
