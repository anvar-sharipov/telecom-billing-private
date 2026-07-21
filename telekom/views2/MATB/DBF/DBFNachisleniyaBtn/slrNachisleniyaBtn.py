from django.shortcuts import render, redirect
from django.contrib import messages

from calendar import monthrange
from datetime import datetime

from telekom.models import DontRepeatYourself, LocalCall, NachMinus, StaffAction, UserTable
from telekom.views2.myFunc.myFunc import monthСonvert


def slrNachisleniyaBtn(request):
    # request.POST.get('url_from')
    

    if request.method == 'POST':  
        month_word = request.POST.get('month')
        year = request.POST.get('year')
        month_numb = monthСonvert(month_word)

        # Если месяц не выбран назал
        if month_word == 'None':
            messages.error(request, f'Выберите месяц начисления') 
            return redirect('slr-nachisleniya')

        
        # Проверка не повторяется ли начисления за этот месяц
        try:
            DontRepeatYourself.objects.get(slrNachisleniyaYearMonth=f"{year}{month_word}")
            messages.error(request, f'За месяц {month_word} {year} года начисления уже было') 
            return redirect('slr-nachisleniya')
        except:
            pass

        # Проверка есть ли комментарий этого действия 
        if request.POST.get('comment') == '':
            messages.error(request, f'Пожалуйста Добавьте комментарий - комментарий не может быть пустым') 
            return redirect('slr-nachisleniya')


        days_in_nach_month = monthrange(int(year), int(month_numb))[1]

        first = f"{year}-{month_numb}-01"
        last = f"{year}-{month_numb}-{days_in_nach_month}"
        localCalls = LocalCall.objects.filter(DATE__range=[first, last])

        # {20000Dashoguz: {date: total_MT, date2: total_MT}}
        usersDict = {}

        for i in range(1, days_in_nach_month+1):
            start = datetime(2023,int(month_numb),i)
            end = datetime(2023,int(month_numb),i)

            tables = localCalls.filter(DATE__range=[start, end])

            # {20000Dashoguz: {date: total_MT, date2: total_MT}}
            for table in tables:
                if f'{table.SUB_A}{table.etrap}' not in usersDict:
                    usersDict[f'{table.SUB_A}{table.etrap}'] = {f'{str(start)[:10]}': int(table.MT)}
                else:
                    if f'{str(start)[:10]}' not in usersDict[f'{table.SUB_A}{table.etrap}']:
                        usersDict[f'{table.SUB_A}{table.etrap}'][f'{str(start)[:10]}'] = int(table.MT)
                    else:
                        usersDict[f'{table.SUB_A}{table.etrap}'][f'{str(start)[:10]}'] += int(table.MT)
        
        # Убораем разговоры по датам < 6
        usersDictCopy = usersDict.copy()
        for key, value in usersDictCopy.items():
            valueCopy = value.copy()
            for date, mt in valueCopy.items():
                if mt < 6:
                    del usersDict[key][date]

        # После удаления по дата возможны пустые значения ключей usersDict (надо их удалить)
        usersDictCopy = usersDict.copy()
        for key, value in usersDictCopy.items():
            if value:
                pass
            else:
                del usersDict[key]


        users = UserTable.objects.all()
        nachMinus = NachMinus.objects.all()

        # Проццес начисления
        for key, value in usersDict.items():
            total_MT_Netto = 0

            for date, val in value.items():
                total_MT_Netto += (val - 5)
            try:
                user = users.get(number=key[:5], etrap=key[5:])
            except:
                user = None
            if user:
                # prochee
                prochee = 0
                if user.b_slr < 0:
                    if user.is_enterprises == True:
                        if user.hb.name == 'H':
                            prochee = (total_MT_Netto * 0.0006) * float(f"0.{str(user.hb.percent)}")
                    else:
                        prochee = (total_MT_Netto * 0.0006) * 0.05
                
                # Минус баланса
                user.b_slr -= (total_MT_Netto * 0.0006)
                user.b_prochee -= prochee
                user.save()

                # сохраняем в NachMinus slr
                try:
                    userNachMinus = nachMinus.get(user=user, year=year, month=month_numb)
                    userNachMinus.slr += total_MT_Netto * 0.0006
                    userNachMinus.prochee += prochee
                    userNachMinus.save()
                except:
                    userNachMinus = NachMinus.objects.create(user=user, year=year, month=month_numb, slr=(total_MT_Netto * 0.0006), prochee=prochee)


        # Сохраняем действие чтобы в будущем запрещать повторное начисления
        DontRepeatYourself.objects.create(slrNachisleniyaYearMonth=f'{year}{month_word}')

        # Сохроняем действия данного оператора для истории
        StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')} \n\n Начисления СЛР за месяц {month_word} {year} года", action='Начисления СЛР')

        
        messages.success(request, f'Успешное начисления за {month_word} {year} года') 
        return redirect('slr-nachisleniya')