from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages

# Не работает в Apache
# from openpyxl import Workbook

from telekom.models import PayHistory, UserTable

from datetime import date

# Для минуса месяцев с даты
from dateutil.relativedelta import relativedelta

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup



def exportInternet(request, etrap):

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    
    if etrap in etraps:
        users = UserTable.objects.filter(etrap=etrap)
    else:
        users = UserTable.objects.all()

        # 1 месяц
    if request.method == 'POST' and 'internet1Month' in request.POST:

        users = users.exclude(name__exact='', surname__exact='')
        users = users.filter(b_internet__lt = 0 )
        

        start = str(date.today() - relativedelta(months=1)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        start2 = str(date.today() - relativedelta(months=2)) + ' 00:00:00'
        end2 = str(date.today() - relativedelta(months=1)) + ' 00:00:00'

        payHistory = PayHistory.objects.filter(date__range=[start, end], internet__gt=0)
        payHistory2 = PayHistory.objects.filter(date__range=[start2, end2], internet__gt=0)
        
        new_users = []
        for user in users:
            if user.b_internet < 0:
                pays = payHistory.filter(abonent=user)
                pays2 = payHistory2.filter(abonent=user)
                if len(pays) == 0 and len(pays2) > 0:
                    new_users.append(user)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="internet 1 ay minus {etrap}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'internet minus {etrap}'

        headers = ['ID', 'Etrap', 'Номер', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Кв', 'Сотовый', 'Предприятие', 'Хоз/Бюд', 'Счет', 'Баланс Интернет']
        
        ws.append(headers)
        for user in new_users:
            if user.is_enterprises:
                userIs_enterprises = 'Да'
            else:
                userIs_enterprises = ''

            if user.hb:
                userHb = user.hb.name
            else:
                userHb = ''

            if user.count_of_numbers:
                userCountOfNumber = user.count_of_numbers.count_of_numbers
            else:
                userCountOfNumber = ''

            if user.abon_length:
                userAbonLength = user.abon_length.metr
            else:
                userAbonLength = ''

            if user.beneficiary:
                userBeneficiary = user.beneficiary.beneficiary
            else:
                userBeneficiary = ''

            if user.service:
                userService = ''
                for i in user.service.all():
                    userService += f"{i.service}, "
            else:
                userService = ''

            ws.append([user.id, user.etrap, user.number, user.surname, user.name, user.street, user.home, user.flat, 
                        user.sotowyy, userIs_enterprises, userHb, user.account, "%.2f" % user.b_internet])    
        
        wb.save(response)
        return response

    # 2 месяца
    if request.method == 'POST' and 'internet2Month' in request.POST:
        users = users.exclude(name__exact='', surname__exact='')
        users = users.filter(b_internet__lt = 0 )

        start = str(date.today() - relativedelta(months=2)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        start2 = str(date.today() - relativedelta(months=3)) + ' 00:00:00'
        end2 = str(date.today() - relativedelta(months=2)) + ' 00:00:00'

        payHistory = PayHistory.objects.filter(date__range=[start, end], internet__gt=0)
        payHistory2 = PayHistory.objects.filter(date__range=[start2, end2], internet__gt=0)


        new_users = []
        for user in users:
            if user.b_internet < 0:
                pays = payHistory.filter(abonent=user)
                pays2 = payHistory2.filter(abonent=user)
                if len(pays) == 0  and len(pays2) > 0:
                    new_users.append(user)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="internet 2 ay minus {etrap}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'internet minus {etrap}'

        headers = ['ID', 'Etrap', 'Номер', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Кв', 'Сотовый', 'Предприятие', 'Хоз/Бюд', 'Счет', 'Баланс Интернет']

        
        ws.append(headers)
        for user in new_users:
            if user.is_enterprises:
                userIs_enterprises = 'Да'
            else:
                userIs_enterprises = ''

            if user.hb:
                userHb = user.hb.name
            else:
                userHb = ''

            if user.count_of_numbers:
                userCountOfNumber = user.count_of_numbers.count_of_numbers
            else:
                userCountOfNumber = ''

            if user.abon_length:
                userAbonLength = user.abon_length.metr
            else:
                userAbonLength = ''

            if user.beneficiary:
                userBeneficiary = user.beneficiary.beneficiary
            else:
                userBeneficiary = ''

            if user.service:
                userService = ''
                for i in user.service.all():
                    userService += f"{i.service}, "
            else:
                userService = ''

            ws.append([user.id, user.etrap, user.number, user.surname, user.name, user.street, user.home, user.flat, 
                user.sotowyy, userIs_enterprises, userHb, user.account, "%.2f" % user.b_internet])     

        wb.save(response)
        return response
    
    # 3 месяца
    if request.method == 'POST' and 'internet3Month' in request.POST:
        users = users.exclude(name__exact='', surname__exact='')
        users = users.filter(b_internet__lt = 0 )

        start = str(date.today() - relativedelta(months=3)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        start2 = str(date.today() - relativedelta(months=4)) + ' 00:00:00'
        end2 = str(date.today() - relativedelta(months=3)) + ' 00:00:00'

        payHistory = PayHistory.objects.filter(date__range=[start, end], internet__gt=0)
        payHistory2 = PayHistory.objects.filter(date__range=[start2, end2], internet__gt=0)


        new_users = []
        for user in users:
            if user.b_internet < 0:
                pays = payHistory.filter(abonent=user)
                pays2 = payHistory2.filter(abonent=user)
                if len(pays) == 0  and len(pays2) > 0:
                    new_users.append(user)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="internet 3 ay minus {etrap}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'internet minus {etrap}'

        headers = ['ID', 'Etrap', 'Номер', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Кв', 'Сотовый', 'Предприятие', 'Хоз/Бюд', 'Счет', 'Баланс Интернет']
        
        ws.append(headers)
        for user in new_users:
            if user.is_enterprises:
                userIs_enterprises = 'Да'
            else:
                userIs_enterprises = ''

            if user.hb:
                userHb = user.hb.name
            else:
                userHb = ''

            if user.count_of_numbers:
                userCountOfNumber = user.count_of_numbers.count_of_numbers
            else:
                userCountOfNumber = ''

            if user.abon_length:
                userAbonLength = user.abon_length.metr
            else:
                userAbonLength = ''

            if user.beneficiary:
                userBeneficiary = user.beneficiary.beneficiary
            else:
                userBeneficiary = ''

            if user.service:
                userService = ''
                for i in user.service.all():
                    userService += f"{i.service}, "
            else:
                userService = ''

            ws.append([user.id, user.etrap, user.number, user.surname, user.name, user.street, user.home, user.flat, 
                user.sotowyy, userIs_enterprises, userHb, user.account, "%.2f" % user.b_internet])    
        
        wb.save(response)
        return response
    
    # 4 месяца
    if request.method == 'POST' and 'internet4Month' in request.POST:
        users = users.exclude(name__exact='', surname__exact='')
        users = users.filter(b_internet__lt = 0 )

        start = str(date.today() - relativedelta(months=4)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        start2 = str(date.today() - relativedelta(months=5)) + ' 00:00:00'
        end2 = str(date.today() - relativedelta(months=4)) + ' 00:00:00'

        payHistory = PayHistory.objects.filter(date__range=[start, end], internet__gt=0)
        payHistory2 = PayHistory.objects.filter(date__range=[start2, end2], internet__gt=0)


        new_users = []
        for user in users:
            if user.b_internet < 0:
                pays = payHistory.filter(abonent=user)
                pays2 = payHistory2.filter(abonent=user)
                if len(pays) == 0  and len(pays2) > 0:
                    new_users.append(user)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="internet 4 ay minus {etrap}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'internet minus {etrap}'

        headers = ['ID', 'Etrap', 'Номер', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Кв', 'Сотовый', 'Предприятие', 'Хоз/Бюд', 'Счет', 'Баланс Интернет']
        
        ws.append(headers)
        for user in new_users:
            if user.is_enterprises:
                userIs_enterprises = 'Да'
            else:
                userIs_enterprises = ''

            if user.hb:
                userHb = user.hb.name
            else:
                userHb = ''

            if user.count_of_numbers:
                userCountOfNumber = user.count_of_numbers.count_of_numbers
            else:
                userCountOfNumber = ''

            if user.abon_length:
                userAbonLength = user.abon_length.metr
            else:
                userAbonLength = ''

            if user.beneficiary:
                userBeneficiary = user.beneficiary.beneficiary
            else:
                userBeneficiary = ''

            if user.service:
                userService = ''
                for i in user.service.all():
                    userService += f"{i.service}, "
            else:
                userService = ''

            ws.append([user.id, user.etrap, user.number, user.surname, user.name, user.street, user.home, user.flat, 
                                user.sotowyy, userIs_enterprises, userHb, user.account, "%.2f" % user.b_internet])  
        
        wb.save(response)
        return response
    

    # 5 месяца
    if request.method == 'POST' and 'internet5Month' in request.POST:
        users = users.exclude(name__exact='', surname__exact='')
        users = users.filter(b_internet__lt = 0 )

        start = str(date.today() - relativedelta(months=5)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        start2 = str(date.today() - relativedelta(months=6)) + ' 00:00:00'
        end2 = str(date.today() - relativedelta(months=5)) + ' 00:00:00'

        payHistory = PayHistory.objects.filter(date__range=[start, end], internet__gt=0)
        payHistory2 = PayHistory.objects.filter(date__range=[start2, end2], internet__gt=0)


        new_users = []
        for user in users:
            if user.b_internet < 0:
                pays = payHistory.filter(abonent=user)
                pays2 = payHistory2.filter(abonent=user)
                if len(pays) == 0  and len(pays2) > 0:
                    new_users.append(user)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="internet 5 ay minus {etrap}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'internet minus {etrap}'

        headers = ['ID', 'Etrap', 'Номер', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Кв', 'Сотовый', 'Предприятие', 'Хоз/Бюд', 'Счет', 'Баланс Интернет']      
        
        ws.append(headers)
        for user in new_users:
            if user.is_enterprises:
                userIs_enterprises = 'Да'
            else:
                userIs_enterprises = ''

            if user.hb:
                userHb = user.hb.name
            else:
                userHb = ''

            if user.count_of_numbers:
                userCountOfNumber = user.count_of_numbers.count_of_numbers
            else:
                userCountOfNumber = ''

            if user.abon_length:
                userAbonLength = user.abon_length.metr
            else:
                userAbonLength = ''

            if user.beneficiary:
                userBeneficiary = user.beneficiary.beneficiary
            else:
                userBeneficiary = ''

            if user.service:
                userService = ''
                for i in user.service.all():
                    userService += f"{i.service}, "
            else:
                userService = ''

            ws.append([user.id, user.etrap, user.number, user.surname, user.name, user.street, user.home, user.flat, 
                user.sotowyy, userIs_enterprises, userHb, user.account, "%.2f" % user.b_internet])   
        
        wb.save(response)
        return response
    
    # 6 месяца
    if request.method == 'POST' and 'internet6Month' in request.POST:
        users = users.exclude(name__exact='', surname__exact='')
        users = users.filter(b_internet__lt = 0 )

        start = str(date.today() - relativedelta(months=6)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        start2 = str(date.today() - relativedelta(months=7)) + ' 00:00:00'
        end2 = str(date.today() - relativedelta(months=6)) + ' 00:00:00'

        payHistory = PayHistory.objects.filter(date__range=[start, end], internet__gt=0)
        payHistory2 = PayHistory.objects.filter(date__range=[start2, end2], internet__gt=0)


        new_users = []
        for user in users:
            if user.b_internet < 0:
                pays = payHistory.filter(abonent=user)
                pays2 = payHistory2.filter(abonent=user)
                if len(pays) == 0  and len(pays2) > 0:
                    new_users.append(user)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="internet 6 ay minus {etrap}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'internet minus {etrap}'

        headers = ['ID', 'Etrap', 'Номер', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Кв', 'Сотовый', 'Предприятие', 'Хоз/Бюд', 'Счет', 'Баланс Интернет']
        
        ws.append(headers)
        for user in new_users:
            if user.is_enterprises:
                userIs_enterprises = 'Да'
            else:
                userIs_enterprises = ''

            if user.hb:
                userHb = user.hb.name
            else:
                userHb = ''

            if user.count_of_numbers:
                userCountOfNumber = user.count_of_numbers.count_of_numbers
            else:
                userCountOfNumber = ''

            if user.abon_length:
                userAbonLength = user.abon_length.metr
            else:
                userAbonLength = ''

            if user.beneficiary:
                userBeneficiary = user.beneficiary.beneficiary
            else:
                userBeneficiary = ''

            if user.service:
                userService = ''
                for i in user.service.all():
                    userService += f"{i.service}, "
            else:
                userService = ''

            ws.append([user.id, user.etrap, user.number, user.surname, user.name, user.street, user.home, user.flat, 
                user.sotowyy, userIs_enterprises, userHb, user.account, "%.2f" % user.b_internet])     
        
        wb.save(response)
        return response
