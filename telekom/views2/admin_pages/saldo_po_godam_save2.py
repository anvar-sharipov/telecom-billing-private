from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from telekom.models import *
from django.db.models import Prefetch
from django.db.models import Sum, F, Q, Value, FloatField
from django.db.models.functions import Coalesce
from collections import defaultdict
from django.db import transaction, IntegrityError
import logging
logger = logging.getLogger(__name__)
from datetime import datetime



def saldo_po_godam_save2(request):
    context = {}
    if not request.user.is_superuser and not request.user.username == 'admin1':
        return redirect('HomePage')
    
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Gubadag', 'Garashsyzlyk']
    columns = ['Перевод ф.и.о, адрес и abonplata абонента', 'Кабель перевод ф.и.о, адрес, count, is_active (Only Dashoguz)', 'set etrap, number and year to SaldoBalancePoGodam (first do it)', 'service', 'all balance and saldo (if year 2024 we set balance on year 2024 to SBPG and saldo to userTable)']
    context['etraps'] = etraps
    context['columns'] = columns

    context['saldo_po_godam_save2'] = True 
    context['admin_allow'] = True 


    if request.method == 'POST':
        check_or_save_checkbox = request.POST.get('check_or_save_checkbox')
        year = int(request.POST.get('year'))
        etrap = request.POST.get('etrap')
        column = request.POST.get('column')
        next_year = year + 1

        context['check_or_save_checkbox'] = check_or_save_checkbox
        context['selected_year'] = str(year)
        context['selected_etrap'] = etrap
        context['selected_column'] = column

   
        if column == 'b_kabel':
            if etrap == 'Dashoguz':
                SBPG = SaldoBalancePoGodam.objects.filter(etrap=etrap, year=year)
                total_b_SPG = SaldoBalancePoGodam.objects.filter(etrap='Dashoguz', year=year).aggregate(total=Sum('b_kabel'))['total'] or 0
                context['total_b_SPG'] = total_b_SPG

                num_nach = {} # {num: [nach, pay]}

                nachs = KabelNach.objects.filter(year__gt=year)
                for n in nachs:
                    num = int(n.user.number)
                    if num not in num_nach:
                        num_nach[num] = [n.nach, 0]
                    else:
                        num_nach[num][0] += n.nach
                pays = KabelTvPayHistory.objects.filter(pay_date__year__gt=year)

                for p in pays:
                    num = int(p.user.number)
                    if num not in num_nach:
                        num_nach[num] = [0, p.pay]
                    else:
                        num_nach[num][1] += p.pay
                users = KabelTvNew.objects.all()

                total_b_UT = 0
                bal_dict = {}
                for u in users:
                    num = int(u.number)
                    if num in num_nach:
                        bal = u.balance + num_nach[num][0] - num_nach[num][1]
                    else:
                        bal = u.balance 
                    total_b_UT += bal
                    bal_dict[num] = bal

                context['total_b_SPG'] = total_b_SPG
                context['total_b_UT'] = total_b_UT
                context['b_kabel'] = True
             
                if SBPG.exists():
                    messages.error(request, 'Сначало добавьте etrap, number, year в SaldoPoGodam')
                else: 

                    if check_or_save_checkbox:
                        users_spg = SaldoBalancePoGodam.objects.filter(year=year, etrap=etrap)
                        bulk_update = []
                        for u in users_spg:
                            num = int(u.number)
                            if num in bal_dict:
                                u.b_kabel = bal_dict[num]
                                bulk_update.append(u)
                        if bulk_update:
                            try:
                                with transaction.atomic():
                                    SaldoBalancePoGodam.objects.bulk_update(bulk_update, ['b_kabel'], batch_size=1000)
                                    messages.success(request, 'Успешное сохранение')
                            except Exception as e:
                                messages.error(request, f'Откат! ошибка с transaction == {e}')
                                logger.error(f'==== Откат с transaction == {e}')

                    else:
                        messages.success(request, 'Успешная проверка')
           
            else:
                messages.error(request, 'b_kabel только для этрапа Dashoguz')


        if column == 'set etrap, number and year to SaldoBalancePoGodam (first do it)':
            SBPG = SaldoBalancePoGodam.objects.filter(etrap=etrap, year=year)
            if SBPG.exists():  # Проверка на существование записей
                messages.error(request, 'Нельзя, etrap, number, year уже есть')
            else:
                if check_or_save_checkbox:
                    users = UserTable.objects.filter(etrap=etrap).order_by('-number')
                    bulk_create = []
                    for u in users:
                        obj = SaldoBalancePoGodam(number=u.number, etrap=etrap, year=year)
                        bulk_create.append(obj)
                    if bulk_create:
                        try:
                            with transaction.atomic():
                                SaldoBalancePoGodam.objects.bulk_create(bulk_create, batch_size=1000)
                            messages.success(request, 'Успешное сохранение')
                        except Exception as e:
                            messages.error(request, f'Откат! ошибка с transaction == {e}')
                            logger.error(f'==== Откат с transaction == {e}')
                else:
                    messages.success(request, 'Успешная проверка')

       
        if column == 'Перевод ф.и.о, адрес и abonplata абонента':
            SBPG = SaldoBalancePoGodam.objects.filter(etrap=etrap, year=year)

            if not SBPG.exists():
                messages.error(request, 'Сначало добавьте etrap, number, year в SaldoPoGodam')
            else:

                co = 0
                for u in SBPG:
                    if u.name or u.surname or u.street or u.home or u.flat or u.abonplata:
                        co += 1
                context['count'] = co
                if check_or_save_checkbox:
                    users = UserTable.objects.filter(etrap=etrap)
                    di = {}
                    for u in users:
                        num = int(u.number)
                        if num < 100000:
                            di[num] = {
                                'surname': u.surname,
                                'name': u.name,
                                'street': u.street,
                                'home': u.home,
                                'flat': u.flat,
                                'abonplata': u.abonplata
                            }

                    bulk_update = []
                    for i in SBPG:
                        num = int(i.number)
                        if num < 100000:
                            i.surname = di[num]['surname']
                            i.name = di[num]['name']
                            i.street = di[num]['street']
                            i.home = di[num]['home']
                            i.flat = di[num]['flat']
                            i.abonplata = di[num]['abonplata']

                            bulk_update.append(i)

                    if bulk_update:
                        try:
                            with transaction.atomic():
                                SaldoBalancePoGodam.objects.bulk_update(bulk_update, ['surname', 'name', 'street', 'home', 'flat', 'abonplata'], batch_size=1000)
                            messages.success(request, 'Успешное сохранение')
                        except Exception as e:
                            messages.error(request, f'Откат! ошибка с transaction == {e}')
                            logger.error(f'==== Откат с transaction == {e}')
                else:
                    messages.success(request, 'Успешная проверка')


        if column == 'service':
            SBPG = SaldoBalancePoGodam.objects.filter(etrap=etrap, year=year)

            if not SBPG.exists():
                messages.error(request, "Сначала добавьте etrap, number, year в SaldoPoGodam")
            else:
                users_UT = UserTable.objects.filter(etrap=etrap, service__isnull=False).prefetch_related("service")
                users_SBPG = SBPG.filter(service__isnull=False).prefetch_related("service")

                context["co_UT"] = users_UT.count()
                context["co_SBPG"] = users_SBPG.count()

                if check_or_save_checkbox:
                    BATCH_SIZE = 1000 
                    sal_bal_dict = { (s.etrap, s.number): s for s in SBPG }
                    m2m_updates = defaultdict(list)

                    for count, u in enumerate(users_UT, start=1):
                        print(count)
                        key = (u.etrap, u.number)
                        if key in sal_bal_dict:
                            sal_bal = sal_bal_dict[key]
                            sal_bal.service.clear()  # Очищаем связи
                            m2m_updates[sal_bal].extend(u.service.all())  # Подготовка новых связей

                    # Массовое добавление связей с batch_size
                    try:
                        with transaction.atomic():  # Группируем операции в транзакцию
                            for sal_bal, services in m2m_updates.items():
                                for i in range(0, len(services), BATCH_SIZE):
                                    sal_bal.service.add(*services[i : i + BATCH_SIZE])
                        messages.success(request, "Успешное сохранение")
                    except Exception as e:
                        messages.error(request, f'Откат! ошибка с transaction == {e}')
                        logger.error(f'==== Откат с transaction == {e}')
                    
                else:
                    messages.success(request, "Успешная проверка")





            # SBPG = SaldoBalancePoGodam.objects.filter(etrap=etrap, year=year)

            # if not SBPG:
            #     messages.error(request, 'Сначало добавьте etrap, number, year в SaldoPoGodam')
            # else:
            #     users_UT = UserTable.objects.filter(etrap=etrap, service__isnull=False).prefetch_related('service')
            #     users_SBPG = SaldoBalancePoGodam.objects.filter(etrap=etrap, service__isnull=False, year=year).prefetch_related('service')
            #     co_UT = 0
            #     co_SBPG = 0
            #     for u in users_UT:
            #         co_UT += 1
            #     for u in users_SBPG:
            #         print(u.number)
            #         co_SBPG += 1
            #     context['co_UT'] = co_UT
            #     context['co_SBPG'] = co_SBPG

            #     if check_or_save_checkbox:
            #         count = 0
            #         for u in users_UT:
            #             count += 1
            #             print(count)
            #             sal_bal = SaldoBalancePoGodam.objects.get(etrap=u.etrap, number=u.number, year=year)
            #             sal_bal.service.clear()
            #             for s in u.service.all():
            #                 sal_bal.service.add(s)
            #         messages.success(request, 'Успешное сохранение')
            #     else:
            #         messages.success(request, 'Успешная проверка')


        if column == 'Кабель перевод ф.и.о, адрес, count, is_active (Only Dashoguz)':
            ic('-Кабель перевод ф.и.о, адрес, count, is_active (Only Dashoguz)')
            if etrap != 'Dashoguz':
                messages.error(request, ' For kabel choose only Dashoguz')
            else:
                SBPG = SaldoBalancePoGodam.objects.filter(etrap=etrap, year=year)
                if not SBPG.exists():
                    messages.error(request, 'Сначало добавьте etrap, number, year в SaldoPoGodam')
                else:
                    dict_kabel_data = {}
                    users_k = KabelTvNew.objects.all()
                    for u in users_k:
                        number = int(u.number)
                        surname = u.surname
                        name = u.name
                        street = u.street
                        home = u.home
                        flat = u.flat
                        count = u.count
                        is_active = u.is_active
                        dict_kabel_data[number] = {'surname':surname, 'name':name, 'street':street, 'home':home, 'flat':flat, 'count':count, 'is_active':is_active}


                
                    bulk_update = []
                    for u in SBPG:
                        number = int(u.number)
                        if number in dict_kabel_data:
                            user_data = dict_kabel_data[number]
                            u.surname_k = user_data['surname']
                            u.name_k = user_data['name']
                            u.street_k = user_data['street']
                            u.home_k = user_data['home']
                            u.flat_k = user_data['flat']
                            u.kabel_count = user_data['count']
                            u.is_active = user_data['is_active']

                            bulk_update.append(u)

                    if check_or_save_checkbox:
                        if bulk_update:
                            try:
                                with transaction.atomic():
                                    SaldoBalancePoGodam.objects.bulk_update(bulk_update, ['surname_k', 'name_k', 'street_k', 'home_k', 'flat_k', 'kabel_count', 'is_active'], batch_size=1000)
                                messages.success(request, 'Успешное сохранение')
                            except Exception as e:
                                messages.error(request, f'Откат! ошибка с transaction == {e}')
                                logger.error(f'==== Откат с transaction == {e}')
                    else:
                        messages.success(request, 'Успешная проверка')


        if column == 'all balance and saldo (if year 2024 we set balance on year 2024 to SBPG and saldo to userTable)':
            ic('all balance and saldo (if year 2024 we set balance on year 2024 to SBPG and saldo to userTable)')
            # balance = total balance - pays next years and + nach next years
            SBPG = SaldoBalancePoGodam.objects.filter(etrap=etrap, year=year)
            years = [str(int(year) + 1), str(int(year) + 2), str(int(year) + 3)]
            if not SBPG.exists():
                messages.error(request, 'Сначало добавьте etrap, number, year в SaldoPoGodam')
            else:
                if etrap == 'Dashoguz':
                    perekidkaInfoNew = PerekidkaInfoNew.objects.filter(date__year__gt=int(year)).exclude(user1Etrap__in=['Koneurgench', 'Turkmenbashy', 'Ruhubelent', 'S.A.Nyyazow', 'Gorogly', 'Boldumsaz', 'Akdepe'])
                else:
                    perekidkaInfoNew = PerekidkaInfoNew.objects.filter(user1Etrap=etrap, user2Etrap=etrap, date__year__gt=int(year))
                per_info = {}
                for p in perekidkaInfoNew:
                    try:
                        num1 = int(p.user1Number)
                        num2 = int(p.user2Number)
                        # if num1 == 58684:
                        #         print('tut13', p.kabel1)
                        if num1 in per_info:
                            per_info[num1]['telefon'] += p.telefon1
                            per_info[num1]['internet'] += p.internet1
                            per_info[num1]['alem'] += p.alem1
                            per_info[num1]['kabel'] += p.kabel1
                        else:
                            # if num1 == 58684:
                            #     print('tut12', p.kabel1)
                            per_info[num1] = {'telefon': p.telefon1, 'internet': p.internet1, 'alem': p.alem1, 'kabel': p.kabel1}
                        
                        if num2 in per_info: 
                            per_info[num2]['telefon'] -= p.telefon2
                            per_info[num2]['internet'] -= p.internet2
                            per_info[num2]['alem'] -= p.alem2
                            per_info[num2]['kabel'] -= p.kabel2
                        else:
                            per_info[num2] = {'telefon': p.telefon2, 'internet': p.internet2, 'alem': p.alem2, 'kabel': p.kabel2}
                    except:
                        pass
                    

                    try:
                        num1K = int(p.user1KabelNumber)
                        num2K = int(p.user2KabelNumber)
                        if num1K in per_info:
                            per_info[num1K]['telefon'] += p.telefon1
                            per_info[num1K]['internet'] += p.internet1
                            per_info[num1K]['alem'] += p.alem1
                            per_info[num1K]['kabel'] += p.kabel1
                        else:
                            # if num1K == 58684:
                            #     print('tut12', p.kabel1)
                            per_info[num1K] = {'telefon': p.telefon1, 'internet': p.internet1, 'alem': p.alem1, 'kabel': p.kabel1}
                        
                        if num2K in per_info: 
                            per_info[num2K]['telefon'] -= p.telefon2
                            per_info[num2K]['internet'] -= p.internet2
                            per_info[num2K]['alem'] -= p.alem2
                            per_info[num2K]['kabel'] -= p.kabel2
                        else:
                            per_info[num2K] = {'telefon': p.telefon2, 'internet': p.internet2, 'alem': p.alem2, 'kabel': p.kabel2}
                    except:
                        pass
                    

                users = UserTable.objects.filter(etrap=etrap)
                balances = {}
                for u in users:
                    number = int(u.number)
                    b_telefoniya = u.b_telefon + u.b_slr + u.b_kod + u.b_zakaz + u.b_dop_uslugi + u.b_prochee
                    b_internet = u.b_internet
                    b_alem = u.b_alem
                    if number in per_info:
                        b_telefoniya += per_info[number]['telefon']
                        b_internet += per_info[number]['internet']
                        b_alem += per_info[number]['alem']

                    balances[number] = {'b_telefoniya':b_telefoniya, 'b_internet': b_internet, 'b_alem': b_alem}

                pays = PayHistory.objects.filter(date__year__gt=int(year), abonent__etrap=etrap).select_related('abonent')
                pays_dict = {}
                for p in pays:
                    number = int(p.abonent.number)
                    p_telefoniya = p.telefon + p.slr + p.kod + p.zakaz + p.prochee + p.dop_uslugi

                    if number not in pays_dict:
                        pays_dict[number] = {'p_telefoniya':p_telefoniya, 'p_internet': p.internet, 'p_alem': p.alem}
                    else:
                        pays_dict[number]['p_telefoniya'] += p_telefoniya
                        pays_dict[number]['p_internet'] += p.internet
                        pays_dict[number]['p_alem'] += p.alem

                nachs = NachMinus.objects.filter(year__in=years, user__etrap=etrap).select_related('user')
                nachs_dict = {}
                for n in nachs:
                    number = int(n.user.number)
                    n_telefoniya = n.telefon + n.slr + n.kod + n.zakaz + n.prochee + n.dop_uslugi
                    if number not in nachs_dict:
                        nachs_dict[number] = {'n_telefoniya': n_telefoniya, 'n_internet': n.internet, 'n_alem': n.alem}
                    else:
                        nachs_dict[number]['n_telefoniya'] += n_telefoniya
                        nachs_dict[number]['n_internet'] += n.internet
                        nachs_dict[number]['n_alem'] += n.alem

                correct_balances = {}
                for number, balance in balances.items():
                    # if number == 27400:
                    #     print('tut2 est')
                    telefoniya = balance['b_telefoniya']
                    internet = balance['b_internet']
                    alem = balance['b_alem']
                    if number in pays_dict:
                        telefoniya -= pays_dict[number]['p_telefoniya']
                        internet -= pays_dict[number]['p_internet']
                        alem -= pays_dict[number]['p_alem']
                    if number in nachs_dict:
                        telefoniya += nachs_dict[number]['n_telefoniya']
                        internet += nachs_dict[number]['n_internet']
                        alem += nachs_dict[number]['n_alem']
                    
                    correct_balances[number] = {'telefoniya': telefoniya, 'internet': internet, 'alem': alem}
                    # if number == 27400:
                    #     print('tut3', correct_balances[number])
                
                if etrap == 'Dashoguz':
                    users_k_dict = {}
                    users_k = KabelTvNew.objects.all()
                    for u in users_k:
                        number = int(u.number)
                        b_kabel = u.balance
                        # if number == 58684:
                        #     print('tut10')
                        if number in per_info:
                            b_kabel += per_info[number]['kabel']
                            # if number == 58684:
                            #     print('tut11', per_info[number])
                        users_k_dict[number] = {'balance':b_kabel, 'pay':0, 'nach':0}

                    pays_k = KabelTvPayHistory.objects.filter(pay_date__year__gt=int(year)).select_related('user')
                    for p in pays_k:
                        number = int(p.user.number)
                        users_k_dict[number]['pay'] += p.pay

                    nachs_k = KabelNach.objects.filter(year__in=years).select_related('user')
                    for n in nachs_k:
                        number = int(n.user.number)
                        users_k_dict[number]['nach'] += n.nach

                    corr_bal = {}
                    for number, values in users_k_dict.items():
                        correct_balance = values['balance'] - values['pay'] + values['nach']
                        corr_bal[number] = correct_balance

                     
                # print('tut4', correct_balances[27400])
                if check_or_save_checkbox:
                    bulk_update_SPBG = []
                    bulk_update_UT = []
                    for u in SBPG:
                        number = int(u.number)
                        updated = False
                        if number in correct_balances:
                            u.b_telefon = 0
                            u.b_slr = 0
                            u.b_kod = 0
                            u.b_zakaz = 0
                            u.b_dop_uslugi = 0
                            u.b_prochee = correct_balances[number]['telefoniya']
                            u.b_internet = correct_balances[number]['internet']
                            u.b_alem = correct_balances[number]['alem']
                            updated = True
                        if etrap == 'Dashoguz':
                            if number in corr_bal:
                                u.b_kabel = corr_bal[number]
                                updated = True
                        if updated:
                            bulk_update_SPBG.append(u)

                    users = UserTable.objects.filter(etrap=etrap)
                    # print('tut5', correct_balances[27400], etrap)
                    for u in users:
                        
                        number = int(u.number)
                        updated = False
                        # if number == 27400:
                        #     print('tut1')
                        if number in correct_balances:
                            u.s_telefon = 0
                            u.s_slr = 0
                            u.s_kod = 0
                            u.s_zakaz = 0
                            u.s_dop_uslugi = 0
                            u.s_prochee = correct_balances[number]['telefoniya']
                            u.s_internet = correct_balances[number]['internet']
                            u.s_alem = correct_balances[number]['alem']
                            updated = True
                        if etrap == 'Dashoguz':
                            if number in corr_bal:
                                u.s_kabel = corr_bal[number]
                                updated = True
                        if updated:
                            bulk_update_UT.append(u)

                
                    try:
                        with transaction.atomic():
                            if bulk_update_SPBG:
                                SaldoBalancePoGodam.objects.bulk_update(bulk_update_SPBG, ['b_telefon', 'b_slr', 'b_kod', 'b_zakaz', 'b_dop_uslugi', 'b_prochee', 'b_internet', 'b_alem', 'b_kabel'], batch_size=1000)
                            if bulk_update_UT:
                                UserTable.objects.bulk_update(bulk_update_UT, ['s_telefon', 's_slr', 's_kod', 's_zakaz', 's_dop_uslugi', 's_prochee', 's_internet', 's_alem', 's_kabel'], batch_size=1000)
                            if bulk_update_SPBG or bulk_update_UT:
                                messages.success(request, 'Успешное сохранение')
                            else:
                                messages.success(request, 'Net izmeneniy')
                            
                    except Exception as e:
                        messages.error(request, f'Откат! ошибка с transaction == {e}')
                        logger.error(f'==== Откат с transaction == {e}')
                else:
                    messages.success(request, 'Успешная проверка')


            
            






                




                    

                    
                    



                    
                    

                      


            


            


    return render(request, 'telekom/admin_pages/saldo_po_godam_save2.html', context)