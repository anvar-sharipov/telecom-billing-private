from django.shortcuts import render, redirect
from telekom.models import PayHistory, UserTable, AccountBalance

from telekom.views2.myFunc.myFunc import get_etrap_and_types
from django.contrib import messages
from django.db.models import Sum

def kassaAccount(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            log = 'Dashoguz'
            context['kassaIndex'] = True
            context['kassaAccount'] = True
        else:
            etrap_types = get_etrap_and_types(request.user)
            etraps = etrap_types['etraps']
            log = etraps[0]
            types = etrap_types['types']
            if 'Kassa' in types:
                context['kassaIndex'] = True
                context['kassaAccount'] = True
            if 'SHB' in types:
                context['SHBIndex'] = True
            else:
                messages.error(request, f'Вход только для кассиров')
                return redirect('user-login')
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')
   

    accountNumber = request.GET.get('accountNumber')
    etrap = request.GET.get('etrap')

    context['accountNumber'] = accountNumber
    context['etrap'] = etrap

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['etraps'] = etraps

    if request.method == 'POST':
        account_new = request.POST.get('account_new')
        account_balance = request.POST.get('accountBalanceNew')
        account_name_new = request.POST.get('account_name_new')

        print('dada', account_new, account_balance)   

        if account_new and account_balance and account_name_new:
            try:
                obj_new = AccountBalance.objects.get(account=int(account_new))
                obj_new.balance = account_balance
                obj_new.name = account_name_new
                obj_new.save()
            except:
                obj_new = AccountBalance.objects.create(account=account_new, name=account_name_new, balance=account_balance)
        else:
            messages.error(request, f"Ошибка")


    if accountNumber and etrap:
        users = UserTable.objects.filter(account=accountNumber, etrap=etrap)
        if len(users) > 0:

            try:
                acc_bal = AccountBalance.objects.get(account=accountNumber)
                new_balance = acc_bal.balance
                acc_name = acc_bal.name
                context['acc_name'] = acc_name
            except:
                new_balance = 0

            context['new_balance'] = new_balance



            pays = PayHistory.objects.filter(abonent__in=users)
            context['pays'] = pays


            context['users'] = users
            # Book.objects.aggregate(average_price=Avg('price'))
            sum_b_abon = users.aggregate(b_prochee=Sum('b_prochee'))['b_prochee']
            sum_b_int = users.aggregate(b_internet=Sum('b_internet'))['b_internet']
            sum_b_kab = users.aggregate(b_kabel=Sum('b_kabel'))['b_kabel']
            sum_b_alem = users.aggregate(b_alem=Sum('b_alem'))['b_alem']

            context['sum_b_abon'] = sum_b_abon
            context['sum_b_int'] = sum_b_int
            context['sum_b_kab'] = sum_b_kab
            context['sum_b_alem'] = sum_b_alem

            context['total_balance'] = sum_b_abon + sum_b_int + sum_b_kab + sum_b_alem

            
            context['accountName'] = f"{users[0].name} {users[0].surname}"

            total_debit = 0
            for user in users:
                if user.b_prochee < 0:
                    total_debit += user.b_prochee
                if user.b_internet < 0:
                    total_debit += user.b_internet
                if user.b_alem < 0:
                    total_debit += user.b_alem
                if user.b_kabel < 0:
                    total_debit += user.b_kabel

            context['total_debit'] = total_debit

    

        


         
    
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['columns'] = ['Номер', 'Абон', 'Интернет', 'Кабель TV', 'Alem TV', 'Дебет', 'Итого']
    return render(request, 'telekom/Kassa/kassaAccount.html', context)