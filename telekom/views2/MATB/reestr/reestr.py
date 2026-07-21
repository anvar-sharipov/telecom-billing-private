from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import date
from telekom.models import UserTable
from icecream import ic

from telekom.views2.myFunc.myFunc import getLoggedUserEtrap, loggedUserEtrapAndGroup, monthСonvert


def reestr (request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    context = {}
    context['matbIndex'] = True
    context['reestrMain'] =  True
    
    ic("reestr")

    # test = UserTable.objects.filter(account__isnull=True)
    # test2 = UserTable.objects.get(number='100000', etrap='Dashoguz')
    # print(test2.account, type(test2.account), test2.account == None)

    # test = UserTable.objects.get(number='76523', etrap='Dashoguz')
    # print(test.account, type(test.account))

    # from bulk_update.helper import bulk_update
    # people = UserTable.objects.all()
    # for person in people:
    #     person.account = None
    # bulk_update(people)  # updates all columns using the default db

    # UserTable.objects.all().update(account=None)

    # gg = 0
    # for i in range(250):
    #     gg += 60
    #     print(gg)

    # if len(calls) <= 60 and len(calls) != 0:
    #         sahypa = 1
    #     if len(calls) > 60 and len(calls) <= 120:
    #         sahypa = 2
    #     if len(calls) > 120 and len(calls) <= 180:
    #         sahypa = 3
    #     if len(calls) > 180 and len(calls) <= 240:
    #         sahypa = 4
    #     if len(calls) > 240 and len(calls) <= 300:
    #         sahypa = 5
    #     if len(calls) > 300 and len(calls) <= 360:
    #         sahypa = 6

    # gg = 60
    # for i in range(3, 1000):
    #     gg += 60
    #     print(f"if len(calls) > {gg} and len(calls) <= {gg+60}:")
    #     print(f"    sahypa={i}")


    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date

    # log = getLoggedUserEtrap(request.user.username)
    context['log'] = log
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    context['etraps'] = etraps

    context['etrap'] = request.GET.get('etrap')
    context['get_month'] = request.GET.get('month')
    context['get_year'] = request.GET.get('year')

    month_word = request.GET.get('month')
    year = request.GET.get('year')
    month_numb = monthСonvert(month_word)
    etrap = request.GET.get('etrap')
    context['etrap'] = etrap

    if month_word == '':
        messages.error(request, f'Ошибка! Выберите месяц')
        return redirect('reestr-main')


    if etrap in etraps:
        users = UserTable.objects.filter(is_enterprises = True, etrap=etrap)
    elif etrap == 'all':
        users = UserTable.objects.filter(is_enterprises = True)
    else:
        users = False


 
    return render(request, 'telekom/MATB/reestr/reestr.html', context)

# rabotaet no pered razdeleniem etrapow
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from datetime import date
# from telekom.models import UserTable

# from telekom.views2.myFunc.myFunc import getLoggedUserEtrap, loggedUserEtrapAndGroup, monthСonvert


# def reestr (request):
#     EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
#     if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
#         log = EtrapAndGroup[0]
#     else:
#         messages.error(request, f'Доступ только соотрудникам MATB')
#         return redirect('user-login')
#     context = {}
#     context['matbIndex'] = True
#     context['reestrMain'] =  True

#     # test = UserTable.objects.filter(account__isnull=True)
#     # test2 = UserTable.objects.get(number='100000', etrap='Dashoguz')
#     # print(test2.account, type(test2.account), test2.account == None)

#     # test = UserTable.objects.get(number='76523', etrap='Dashoguz')
#     # print(test.account, type(test.account))

#     # from bulk_update.helper import bulk_update
#     # people = UserTable.objects.all()
#     # for person in people:
#     #     person.account = None
#     # bulk_update(people)  # updates all columns using the default db

#     # UserTable.objects.all().update(account=None)

#     # gg = 0
#     # for i in range(250):
#     #     gg += 60
#     #     print(gg)

#     # if len(calls) <= 60 and len(calls) != 0:
#     #         sahypa = 1
#     #     if len(calls) > 60 and len(calls) <= 120:
#     #         sahypa = 2
#     #     if len(calls) > 120 and len(calls) <= 180:
#     #         sahypa = 3
#     #     if len(calls) > 180 and len(calls) <= 240:
#     #         sahypa = 4
#     #     if len(calls) > 240 and len(calls) <= 300:
#     #         sahypa = 5
#     #     if len(calls) > 300 and len(calls) <= 360:
#     #         sahypa = 6

#     # gg = 60
#     # for i in range(3, 1000):
#     #     gg += 60
#     #     print(f"if len(calls) > {gg} and len(calls) <= {gg+60}:")
#     #     print(f"    sahypa={i}")


#     current_date = date.today()
#     current_date = str(current_date)
#     context['current_date'] = current_date

#     # log = getLoggedUserEtrap(request.user.username)
#     context['log'] = log
#     context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
#     context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']
#     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
#     context['etraps'] = etraps

#     context['etrap'] = request.GET.get('etrap')
#     context['get_month'] = request.GET.get('month')
#     context['get_year'] = request.GET.get('year')

#     month_word = request.GET.get('month')
#     year = request.GET.get('year')
#     month_numb = monthСonvert(month_word)
#     etrap = request.GET.get('etrap')
#     context['etrap'] = etrap

#     if month_word == '':
#         messages.error(request, f'Ошибка! Выберите месяц')
#         return redirect('reestr-main')


#     if etrap in etraps:
#         users = UserTable.objects.filter(is_enterprises = True, etrap=etrap)
#     elif etrap == 'all':
#         users = UserTable.objects.filter(is_enterprises = True)
#     else:
#         users = False


 
#     return render(request, 'telekom/MATB/reestr/reestr.html', context)