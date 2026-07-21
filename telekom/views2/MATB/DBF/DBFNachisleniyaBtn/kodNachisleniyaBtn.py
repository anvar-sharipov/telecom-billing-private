from django.shortcuts import render, redirect
from django.contrib import messages

from calendar import monthrange
from datetime import datetime

from telekom.models import DontRepeatYourself, NachMinus, NonLocalCall, StaffAction, UserTable
from telekom.views2.myFunc.myFunc import monthСonvert

def kodNachisleniyaBtn(request):
    if request.method == 'POST':  
        month_word = request.POST.get('month')
        year = request.POST.get('year')
        month_numb = monthСonvert(month_word)

        # Если месяц не выбран назал
        if month_word == 'None':
            messages.error(request, f'Выберите месяц начисления') 
            return redirect('kod-nachisleniya')

        
        # Проверка не повторяется ли начисления за этот месяц
        try:
            DontRepeatYourself.objects.get(kodNachisleniyaYearMonth=f"{year}{month_word}")
            messages.error(request, f'За месяц {month_word} {year} года начисления уже было') 
            return redirect('kod-nachisleniya')
        except:
            pass

        # Проверка есть ли комментарий этого действия 
        if request.POST.get('comment') == '':
            messages.error(request, f'Пожалуйста Добавьте комментарий - комментарий не может быть пустым') 
            return redirect('kod-nachisleniya')
        

        days_in_nach_month = monthrange(int(year), int(month_numb))[1]

        first = f"{year}-{month_numb}-01"
        last = f"{year}-{month_numb}-{days_in_nach_month}"
        globalCalls = NonLocalCall.objects.filter(DATE__range=[first, last])
        
        # {20000Dashoguz: total_price}
        usersDict = {}
        users = UserTable.objects.all()
        nachMinus = NachMinus.objects.all()
        test = 0
        for call in globalCalls:
            try:
                user = users.get(number=call.SUB_A, etrap=call.SUB_A_etrap)
            except:
                continue

            if f'{call.SUB_A}{call.SUB_A_etrap}' not in usersDict:
                usersDict[f'{call.SUB_A}{call.SUB_A_etrap}'] = float(call.total_price)
            else:
                usersDict[f'{call.SUB_A}{call.SUB_A_etrap}'] += float(call.total_price)

        for key, price in usersDict.items():
            user = users.get(number=key[:5], etrap=key[5:])

            prochee = 0
            if user.b_kod < 0:
                if user.is_enterprises == True:
                    if user.hb.name == 'H':
                        prochee = price  * float(f"0.{str(user.hb.percent)}")
                else:
                    prochee = price* 0.05
            
            # Минус баланса
            user.b_kod -= price
            user.b_prochee -= prochee
            user.save()

             # сохраняем в NachMinus kod
            try:
                userNachMinus = nachMinus.get(user=user, year=year, month=month_numb)
                userNachMinus.kod += price
                userNachMinus.prochee += prochee
                userNachMinus.save()
            except:
                userNachMinus = NachMinus.objects.create(user=user, year=year, month=month_numb, kod=price, prochee=prochee)


        # Сохраняем действие чтобы в будущем запрещать повторное начисления
        DontRepeatYourself.objects.create(kodNachisleniyaYearMonth=f'{year}{month_word}')

        # Сохроняем действия данного оператора для истории
        StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')} \n\n Начисления КОД за месяц {month_word} {year} года", action='Начисления КОД')
        
        
      



        
        

            

        return redirect(request.POST.get('url_from'))