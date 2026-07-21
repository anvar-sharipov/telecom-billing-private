from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from telekom.models import *
from django.db.models import Prefetch
from django.db.models import Sum, F, Q



def saldo_po_godam_save(request):
    context = {}
    if not request.user.is_superuser and not request.user.username == 'admin1':
        return redirect('HomePage')
    
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['etraps'] = etraps

    context['saldo_po_godam_save'] = True 
    context['admin_allow'] = True 

    # SaldoBalancePoGodam.objects.filter(etrap='Dashoguz').update(b_kabel=0)
    # SaldoBalancePoGodam.objects.filter(etrap='Dashoguz').update(s_kabel=0)




      

    if request.method == 'POST' and 'kabel1' in request.POST:
        ic('kabel1')
        year = int(request.POST.get('year'))
        next_year = year + 1
        save_this = request.POST.get('kabel1CheckOrSave')

        context.update({
            'kabel1': True,
            'year_kabel_1': year,
            'next_year_kabel_1': next_year,
            'save_this_kabel1': save_this,
        })

        total_kabel1_b_year = SaldoBalancePoGodam.objects.filter(
            etrap='Dashoguz', year=year
        ).aggregate(total=Sum('b_kabel'))['total'] or 0

        context['total_kabel1_b_year'] = total_kabel1_b_year
        context['savedKabel1'] = total_kabel1_b_year != 0


        # usersK = KabelTvNew.objects.all().annotate(
        #     total_payments=Sum('kabeltvpayhistory__pay', filter=Q(kabeltvpayhistory__pay_date__year__gte=next_year), distinct=True),  
        #     total_nach=Sum('kabelnach__nach', filter=Q(kabelnach__year__gte=next_year), distinct=True),
        # )

        usersK = KabelTvNew.objects.all().prefetch_related(
            Prefetch('kabeltvpayhistory_set', queryset=KabelTvPayHistory.objects.filter(pay_date__year__gte=next_year)),
            Prefetch('kabelnach_set', queryset=KabelNach.objects.filter(year__gte=next_year))
        ).annotate(
            total_payments=Sum('kabeltvpayhistory__pay', filter=Q(kabeltvpayhistory__pay_date__year__gte=next_year), distinct=True),  
            total_nach=Sum('kabelnach__nach', filter=Q(kabelnach__year__gte=next_year), distinct=True),
        )

        total_kabel1_b_year_from_user_table = 0
        obj_bulk_update = []

        dict_ = {}
        SB = SaldoBalancePoGodam.objects.filter(year=year, etrap='Dashoguz')
        ic(len(SB))
        for i in SB:
            dict_[int(i.number)] = i

        count = 0
        for user in usersK:
            # count += 1
            # print(count)
            balance_kabel = user.balance - (user.total_payments or 0) + (user.total_nach or 0)
            total_kabel1_b_year_from_user_table += balance_kabel

            if save_this:
                obj = dict_[int(user.number)]
                obj.b_kabel = balance_kabel
                obj_bulk_update.append(obj)

        if obj_bulk_update and save_this:
            SaldoBalancePoGodam.objects.bulk_update(obj_bulk_update, ['b_kabel'], batch_size=1000)
            messages.success(request, '"b_kabel" Сохранено')

        context['total_kabel1_b_year_from_user_table'] = total_kabel1_b_year_from_user_table

        if not save_this:
            messages.success(request, '"b_kabel" Проверено')
        # elif total_kabel1_b_year != 0:
        #     messages.error(request, f'"Кабельное b" за {year} уже сохранено')


    if request.method == 'POST' and 'kabel2' in request.POST:
        ic('kabel2')
        year = int(request.POST.get('year'))
        next_year = year + 1
        save_this = request.POST.get('kabel2CheckOrSave')

        context.update({
            'kabel2': True,
            'year_kabel_2': year,
            'next_year_kabel_2': next_year,
            'save_this_kabel2': save_this,
        })
        # ic(year, next_year, save_this)

        total_kabel2_s_year = SaldoBalancePoGodam.objects.filter(
            etrap='Dashoguz', year=year
        ).aggregate(total=Sum('s_kabel'))['total'] or 0

        total_kabel2_s_year_userTable = UserTable.objects.filter(
            etrap='Dashoguz'
        ).aggregate(total=Sum('s_kabel'))['total'] or 0

        context['total_kabel2_s_year'] = total_kabel2_s_year
        context['total_kabel2_s_year_userTable'] = total_kabel2_s_year_userTable
        context['savedKabel2'] = total_kabel2_s_year != 0

        dict_ = {}
        SB = SaldoBalancePoGodam.objects.filter(year=year, etrap='Dashoguz')
        for i in SB:
            dict_[int(i.number)] = i

        usersK2 = UserTable.objects.filter(etrap='Dashoguz')


        count = 0
        obj_bulk_update = []
        for i in usersK2:
            count += 1
            print(count)

            if save_this:
                obj = dict_[int(i.number)]
                obj.s_kabel = i.s_kabel
                obj_bulk_update.append(obj)

        if obj_bulk_update and save_this:
            SaldoBalancePoGodam.objects.bulk_update(obj_bulk_update, ['s_kabel'], batch_size=1000)
            messages.success(request, '"b_kabel" Сохранено')

        if not save_this:
            messages.success(request, '"b_kabel" Проверено')



    if request.method == 'POST' and 'internet_b' in request.POST:
        ic('internet_b')
        year = int(request.POST.get('year'))
        etrap = request.POST.get('etrap')
        next_year = year + 1
        save_this = request.POST.get('internet_bCheckOrSave')
        ic(etrap)

        context.update({
            'internet_b': True,
            'year_internet_b': year,
            'next_year_internet_b': next_year,
            'save_this_internet_b': save_this,
            'selected_etrap': etrap,
        })

        dict_ = {} # {number: [pay, nach, balance, objSB]}
        total_internet_b_year_from_user_table = 0
        users = UserTable.objects.filter(etrap=etrap) #.only('number', 'b_internet')
        for u in users:
            num = int(u.number)
            total_internet_b_year_from_user_table += u.b_internet
            if num not in dict_:
                dict_[num] = [0,0,u.b_internet,None]
            else:
                dict_[num][2] = u.b_internet

        pays = PayHistory.objects.filter(date__year__gte=next_year, abonent__etrap=etrap) #.select_related('abonent')
        for i in pays:
            num = int(i.abonent.number)
            if num not in dict_:
                dict_[num] = [i.internet, 0, 0, None]
            else:
                dict_[num][0] += i.internet

        nachs = NachMinus.objects.filter(year__gte=next_year, user__etrap=etrap) #.select_related('user')
        for i in nachs:
            num = int(i.user.number)
            if num not in dict_:
                dict_[num] = [0, i.internet, 0, None]
            else:
                dict_[num][1] += i.internet

        total_internet_b_year = 0
        SB = SaldoBalancePoGodam.objects.filter(year=str(year), etrap=etrap) #.only('number', 'b_internet')
        for i in SB:
            total_internet_b_year += i.b_internet
            num = int(i.number)
            if i.b_internet != (dict_[num][2] - dict_[num][0] + dict_[num][1]):
                print(i.number, i.b_internet, dict_[num][2] - dict_[num][0] + dict_[num][1])
            if num not in dict_:
                dict_[num] = [0,0,0,i]
            else:
                dict_[num][3] = i

        context['total_internet_b_year'] = total_internet_b_year
        context['total_internet_b_year_from_user_table'] = total_internet_b_year_from_user_table
        context['savedInternet_b'] = total_internet_b_year != 0
        ic(total_internet_b_year)
        ic(total_internet_b_year_from_user_table)

        
        if save_this:
            obj_bulk_update = []
            for number, (pay, nach, balance, obj) in dict_.items():
                if obj:
                    obj.b_internet = balance - pay + nach
                    obj_bulk_update.append(obj)
            if obj_bulk_update:
                SaldoBalancePoGodam.objects.bulk_update(obj_bulk_update, ['b_internet'], batch_size=1000)
                messages.success(request, '"b_internet" Сохранено')
        else:
            messages.success(request, '"b_internet" Проверено')


    




    






   



        
        

    
    return render(request, 'telekom/admin_pages/saldo_po_godam_save.html', context)








