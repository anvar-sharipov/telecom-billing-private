from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.views2.myFunc.myFunc import get_etrap_and_types
from telekom.models import UserTable, KabelTvNew, KabelTvPayHistory, KabelComment, PayHistory, KabelNach, KabelTvNewDebitKredit, ManagerNames
# # from telekom.models import AbonentService, DontRepeatYourself, NachMinus, NachisleniyaOtchet, StaffAction, UserTable
# from django.db.models import Sum
from django.db.models import Q
# from calendar import monthrange
from datetime import datetime
from telekom.views2.myFunc.myFunc import monthСonvert
from django.http import HttpResponse
import tablib

from calendar import monthrange
from datetime import date
from dateutil.relativedelta import relativedelta
# from telekom.models import DontRepeatYourself, NachMinus, NachisleniyaOtchet, PayHistory, StaffAction, UserTable

# from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert




def kabelNach(request):
    context = {}
    if request.user.username not in ['admin1', 'Gayyp']:
        messages.error(request, 'Доступ только для администратора')
        return redirect('user-login')
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']
    if request.user.is_authenticated:
        if request.user.is_superuser or 'subadmin' in request.user.username:
            log = 'Dashoguz'
            context['KabelNach'] = True
            
        else:
            messages.error(request, f'У вас нет доступа в Kabel TV')
            return redirect('user-login')
          
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')


    users = KabelTvNew.objects.all()

    # p = PayHistory.objects.filter(kabel__gt=0, kassir = 'admin1')
    # for i in p:
    #     print(i.abonent.etrap, i.abonent.number)


    total_nach_manat_ilat = 0
    total_nach_manat_edara = 0
    count_manat = {
    1: 10, 
    2: 15, 
    3: 20, 
    4: 25, 
    5: 30, 
    6: 35, 
    7: 40, 
    8: 45, 
    9: 50, 
    10: 55, 
    11: 60, 
    12: 65, 
    13: 70, 
    14: 75, 
    15: 80, 
    16: 85, 
    17: 90, 
    18: 95, 
    19: 100, 
    20: 105
    }
    debitors = 0
    kreditors = 0
    for u in users:
        if u.balance < 0:
            debitors += abs(u.balance) 
        else:
            kreditors += u.balance
        if u.is_active:
            if u.is_enterprises:
                total_nach_manat_edara += count_manat[u.count]
            else:
                total_nach_manat_ilat += count_manat[u.count]



    context['total_nach_manat_ilat'] = total_nach_manat_ilat
    context['total_nach_manat_edara'] = total_nach_manat_edara
    context['debitors'] = debitors
    context['kreditors'] = kreditors
    context['total_balance'] = kreditors + (-debitors)


    if request.method == 'POST' and 'n_a_c_hisleniya' in request.POST:
        pass
        
    # Работающий код для начисления но я его сделал в группе Начисления
        # month = monthСonvert(request.POST.get('month'))
        # context['get_month'] = month
        
        # year = request.POST.get('year')
        # context['year'] = year

        # if month and year:
        #     already_nach = len(KabelNach.objects.filter(year=year, month=month)) == 0
        #     nach_count = 0
        #     if len(KabelNach.objects.filter(year=year, month=month)) == 0:
        #         for u in users:
        #             if u.is_active:
        #                 nach_count += 1
        #                 print('nach_count', nach_count)
        #                 u.balance -= count_manat[u.count]
        #                 try:
        #                     n = KabelNach.objects.get(user=u, year=year, month=month)
        #                 except:
        #                     n = KabelNach.objects.create(user=u, year=year, month=month)
                        
            
        #                 n.nach += count_manat[u.count]
        #                 u.save()
        #                 n.save()
        #         messages.success(request, f"Успешное начисление за {year} {request.POST.get('month')}")
        #     else:
        #         messages.error(request, f"Начисление за {year} {request.POST.get('month')} уже было")
        # else:
        #     messages.error(request, f"Выберите год и месяц")
    # Работающий код для начисления но я его сделал в группе Начисления



    if request.method == 'POST' and 'spisok' in request.POST:
        print('spisok')
        
        headers = ("NUMBER","SURNAME","NAME", "EDARA", "SOTOWYY", "COUNT", "BALANCE", "ACTIVE")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)
        

        for u in users:
            edara = ''
            if u.is_enterprises:
                edara = 'П'

            active = ''
            if u.is_active:
                active = '+'

            data.append((u.number, u.surname, u.name, edara, u.sotowyy, u.count, u.balance, active))

            
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= Kabel_baza_{datetime.now()}.xlsx"

        return response


    if request.method == 'POST' and 'nach_s_p_i_s_o_k' in request.POST:
        print('nach')

        month = monthСonvert(request.POST.get('month'))
        year = request.POST.get('year')
        
        headers = ("NUMBER","SURNAME","NAME","EDARA","COUNT","NACH")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)
        

        for u in KabelNach.objects.filter(year=year, month=month):
            edara = ''
            if u.user.is_enterprises:
                edara = 'П'

            data.append((u.user.number, u.user.surname, u.user.name, edara, u.user.count, u.nach))

            
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= nach_za_{year} {month}.xlsx"

        return response

    
    if request.method == 'POST' and 'kabel_tolegler' in request.POST:
        print('nach')

        

        month = monthСonvert(request.POST.get('month'))
        year = request.POST.get('year')

        days_in_choosed_month = monthrange(int(year), int(month))[1]
        
        headers = ("NUMBER","SURNAME","NAME","CART","PRICE")
        
        data = []
        data = tablib.Dataset(*data, headers=headers)
        

        for u in KabelTvPayHistory.objects.filter(pay_date__range=[f"{str(year)}-{str(month)}-01 00:00:00", f"{str(year)}-{str(month)}-{str(days_in_choosed_month)} 23:59:59"], user__is_enterprises=False):
            cart = 'Оплачено наличкой'
            if u.card:
                cart = 'Оплачено карточкой'

            data.append((u.user.number, u.user.surname, u.user.name, cart, u.pay))

            
        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= plateji_kabel_za_{year}_{month}.xlsx"

        return response



    if request.method == 'POST' and 'debit_kredit_kabel' in request.POST:
        print('debit_kredit_kabel')

        

        month = monthСonvert(request.POST.get('month'))
        year = request.POST.get('year')

        days_in_choosed_month = monthrange(int(year), int(month))[1]
        
        headers = ("NUMBER","DT","KT","NACH","TOLEG KASSA","TOLEG WN","TOLEG SUMM","DT","KT","EDARA")

        
        saldo = KabelTvNewDebitKredit.objects.filter(year=year, month=month)

        

        kabel_users = KabelTvNew.objects.all().order_by('number')

        current_date = datetime.strptime(f'{year}-{month}-01', '%Y-%m-%d')
        previous_month_date = current_date - relativedelta(months=1)

        last_year = previous_month_date.strftime('%Y')
        last_month = previous_month_date.strftime('%m')

        last_saldo = KabelTvNewDebitKredit.objects.filter(year=last_year, month=last_month)
        last_saldo_list = {} # {number [DT, KT]}
        for i in last_saldo:
            last_saldo_list[i.number] = [i.last_DT, i.last_KT]

        saldo_list = {} # {number: [DT, KT, NACH, payKassa, pyWn, paySumm, DT, KT]}
        for u in kabel_users:
            if u.number in saldo_list:
                saldo_list[u.number] = [last_saldo_list[u.number],last_saldo_list[u.number],0,0,0,0,0,0]

        for num, val in saldo_list.items():
            print(num, val)






        # Узнаем сколько типов платежей было
        # kabel_pays = KabelTvPayHistory.objects.filter(pay_date__range=[f"{str(year)}-{str(month)}-01 00:00:00", f"{str(year)}-{str(month)}-{str(days_in_choosed_month)} 23:59:59"])
        # managerNames_kassirs = ManagerNames.objects.filter(etrap='Dashoguz')
        # managerNames_wn = ManagerNames.objects.filter(etrap='Внешние платежи')
        # pay_type = []
        # for p in kabel_pays:
        #     if p.pay_kassir in managerNames_wn and p.pay_kassir not in pay_type:
        #         pay_type.append('p.pay_kassir')
        #     elif p.pay_kassir in managerNames_kassirs and 'Kassa' not in pay_type:
        #         pay_type.append('Kassa')
        #     else:
        #         if 'Unknown' not in pay_type:
        #             pay_type.append('Unknown')

        #     if 'Kassa' in pay_type:
        #         pay_type.insert(0, pay_type.pop(pay_type.index('Kassa')))
        #     if 'Unknown' in pay_type:
        #         pay_type.append(pay_type.pop(pay_type.index('Unknown')))
                

        #     if 'E-government' in p.pay_kassir and p.pay_kassir not in count_pay_type:
        #         count_pay_type.append('E-government')
        #     elif 'Tolleg APP TMCELL' in p.pay_kassir and p.pay_kassir not in count_pay_type:
        #         count_pay_type.append('Tolleg APP TMCELL')
        #     elif 'Saray Tolegy' in p.pay_kassir and p.pay_kassir not in count_pay_type:
        #         count_pay_type.append('Saray Tolegy')
        #     elif 'Dostluk Bank' in p.pay_kassir and p.pay_kassir not in count_pay_type:
        #         count_pay_type.append('Dostluk Bank')
        #     elif 'Turkmen Pochta' in p.pay_kassir and p.pay_kassir not in count_pay_type:
        #         count_pay_type.append('Turkmen Pochta')
        #     elif 'halk' in p.pay_kassir and p.pay_kassir not in count_pay_type:
        #         count_pay_type.append('Halk Bank')
        #     elif:
        #         count_pay_type.append('Kassa tolegi')

        
        data = []
        data = tablib.Dataset(*data, headers=headers)


        KabelTvNewDebitKredit.objects.filter(year=year, month=month)


        # kabel_users = KabelTvNew.objects.all().order_by('number')
        # # kabel_pays = KabelTvPayHistory.objects.filter(pay_date__range=[f"{str(year)}-{str(month)}-01 00:00:00", f"{str(year)}-{str(month)}-{str(days_in_choosed_month)} 23:59:59"], user__is_enterprises=False)
        # kabel_pays = KabelTvPayHistory.objects.filter(pay_date__range=[f"2024-06-01 00:00:00", f"2024-07-15 23:59:59"])
        # # kabel_nachs = KabelNach.objects.filter(year=year, month=month)
        # kabel_nachs = KabelNach.objects.filter(year='2024', month='06')

        # number_nach_6_7 = {} # {number: nach}
        # number_plateji_6_7 = {} # {number: pay}
        # current_balance = {} # {number: balance}
        # Balance_za_6 = {} # {number: [DT, KT]}

        # for n in kabel_nachs:
        #     if n.user.number not in number_nach_6_7:
        #         number_nach_6_7[n.user.number] = n.nach
        #     else:
        #         number_nach_6_7[n.user.number] += n.nach

        # for n in kabel_pays:
        #     if n.user.number not in number_plateji_6_7:
        #         number_plateji_6_7[n.user.number] = n.pay
        #     else:
        #         number_plateji_6_7[n.user.number] += n.pay

        # for n in kabel_users:
        #     current_balance[n.number] = n.balance

        # for n, b in current_balance.items():
        #     if n in number_nach_6_7:
        #         current_balance[n] += number_nach_6_7[n]

        #     if n in number_plateji_6_7:
        #         current_balance[n] -= number_plateji_6_7[n]

        # for n, b in current_balance.items():
        #     if b < 0:
        #         Balance_za_6[n] = [abs(b), 0]
        #     else:
        #         Balance_za_6[n] = [0, b]

        # bulkCreate = []
        # for n, dt_kt in Balance_za_6.items():
        #     edara = KabelTvNew.objects.get(number=n).is_enterprises

        #     obj = KabelTvNewDebitKredit(
        #         year = '2024',
        #         month = '06',
        #         number = n,
        #         last_KT = dt_kt[0],
        #         last_DT = dt_kt[1],
        #         is_enterprises = edara
        #     )
        #     bulkCreate.append(obj)
        # KabelTvNewDebitKredit.objects.bulk_create(bulkCreate)
        

        


        # last_DT_KT = {} # {number [DT, KT]}
        # current_DT_KT = {} # {number [DT, KT]}
        # current_balance = {} # {number: balance}
        # this_month_pays = {} # {number: pay}

        # for p in kabel_pays:
        #     if p.user.number not in current_pay:
        #         this_month_pays[p.user.number] = p.pay
        #     else:
        #         this_month_pays[p.user.number] += p.pay

        # for n in kabel_nachs:
        #     pass





        

        # for u in KabelTvPayHistory.objects.filter(pay_date__range=[f"{str(year)}-{str(month)}-01 00:00:00", f"{str(year)}-{str(month)}-{str(days_in_choosed_month)} 23:59:59"], user__is_enterprises=False):
        #     cart = 'Оплачено наличкой'
        #     if u.card:
        #         cart = 'Оплачено карточкой'

        #     data.append((u.user.number, u.user.surname, u.user.name, cart, u.pay))

            
        # response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        # response['Content-Disposition'] = f"attachment; filename= plateji_kabel_za_{year}_{month}.xlsx"

        # return response
            


    return render(request, 'telekom/MATB/KabelNew/kabelNach.html', context)