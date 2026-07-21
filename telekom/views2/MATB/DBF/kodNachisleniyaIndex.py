from django.shortcuts import render, redirect
from django.contrib import messages


from datetime import date
from calendar import monthrange

from telekom.models import LocalCall, NonLocalCall, UserTable
from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert



def kodNachisleniyaIndex(request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        pass
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    context = {}
    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date

    if request.GET.get('month') == '':
        return redirect('kod-nachisleniya')

    # if request.GET.get('month') == '':
    #     return redirect('slr-nachisleniya')

    context['matbIndex'] = True
    context['kodNachisleniya'] = True

    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

    context['get_month'] = request.GET.get('month')
    context['get_year'] = request.GET.get('year')
    

    month_word = request.GET.get('month')
    year = request.GET.get('year')

    
    # print(f"{year}-{month_numb}-01")




    if year and month_word:
        month_numb = monthСonvert(month_word)
        days_in_nach_month = str(monthrange(int(year), int(month_numb))[1])







        try:
            globalCalls = NonLocalCall.objects.filter(DATE__range = [f"{year}-{month_numb}-01", f"{year}-{month_numb}-{days_in_nach_month}"])
        except:
            globalCalls = False
        users = UserTable.objects.all()

        context['get_month'] = request.GET.get('month')
        context['get_year'] = request.GET.get('year')

        # {'20000Dashoguz': [[call], [call], [call]]}
        userTable = {}
        if globalCalls:
            for call in globalCalls:
                if f"{call.SUB_A}{call.SUB_A_etrap}" not in userTable:
                    userTable[f"{call.SUB_A}{call.SUB_A_etrap}"] = [[call.SUB_B, call.SUB_B_locations, call.DATE, call.START, call.FIN, call.DUR, call.MT, call.price, call.total_price]]
                else:
                    userTable[f"{call.SUB_A}{call.SUB_A_etrap}"].append([call.SUB_B, call.SUB_B_locations, call.DATE, call.START, call.FIN, call.DUR, call.MT, call.price, call.total_price])

            countSuccess = 0
            countError = 0

            totalMtSuccess = 0
            totalMtError = 0

            totalSuccesCalls = 0
            totalErrorCalls = 0

            totalSuccessPrice = 0
            totalErrorPrice = 0

            

            for key, calls in userTable.items():
                if users.filter(number=key[:5], etrap=key[5:]):
                    countSuccess += 1
                    totalSuccesCalls += len(calls)
                    for call in calls:
                
                        totalMtSuccess += int(call[6])
                        totalSuccessPrice += float(call[8])
                else:
                    countError += 1
                    totalErrorCalls += len(calls)
                    for call in calls:
                
                        totalMtError += int(call[6])
                        totalErrorPrice += float(call[8])
            

            context['totalMtSuccess'] = totalMtSuccess
            context['totalMtError'] = totalMtError

            

            context['totalSuccessPrice'] = totalSuccessPrice
            context['totalErrorPrice'] = totalErrorPrice

            context['abonentCountSuccess'] = countSuccess
            context['abonentCountError'] = countError

            context['totalSuccesCalls'] = totalSuccesCalls
            context['totalErrorCalls'] = totalErrorCalls
            

            # userTable[f"{call.SUB_A}{call.SUB_A_etrap}"] = [[call.SUB_B, call.SUB_B_locations, call.price, call.DATE, call.START, call.FIN, call.DUR, call.MT, call.total_price]]


    # if month_numb and year:
    #     days_in_nach_month = monthrange(int(year), int(month_numb))[1]

    #     Users = UserTable.objects.all()

    #     first = f"{year}-{month_numb}-01"
    #     last = f"{year}-{month_numb}-{days_in_nach_month}"
    #     localCalls = LocalCall.objects.filter(DATE__range=[first, last])

    #     usersDict = {}

    #     for i in range(1, days_in_nach_month+1):
            
    #         start = datetime(2023,int(month_numb),i)
    #         end = datetime(2023,int(month_numb),i)

    #         tables = localCalls.filter(DATE__range=[start, end])


    #         # делаем {20000Dashoguz: total_MT}
    #         for table in tables:
    #             if (f'{str(start)[:10]}{table.SUB_A}{table.etrap}') not in usersDict:
    #                 usersDict[f'{str(start)[:10]}{table.SUB_A}{table.etrap}'] = int(table.MT)
    #             else:
    #                 usersDict[f'{str(start)[:10]}{table.SUB_A}{table.etrap}'] += int(table.MT)

    #     total_mt = 0
    #     error_count = 0

    #     successUserMt = {}
    #     errorUser = []
    #     for key, mt in usersDict.items():
    #         if mt > 5:
                
    #             try:
    #                 user = Users.get(number=key[10:15], etrap=key[15:])
    #             except:
    #                 user=False

    #             if user:
    #                 total_mt += (mt - 5)

    #                 if f'{user.number}{user.etrap}' not in successUserMt:
    #                     successUserMt[f'{user.number}{user.etrap}'] = (mt - 5)
    #                 else:
    #                     successUserMt[f'{user.number}{user.etrap}'] += (mt - 5)
    #             else:
    #                 if f'{key[10:]}' not in errorUser:
    #                     error_count += 1
    #                     errorUser.append(f'{key[10:]}')

    #     context['total_mt'] = total_mt
    #     context['total_price'] = total_mt * 0.0006
    #     context['sucess_count'] = len(successUserMt)
    #     context['error_count'] = error_count


    return render(request, 'telekom/MATB/DBF/kodNachisleniyaIndex.html', context)



