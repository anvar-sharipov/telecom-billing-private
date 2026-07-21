from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import Group

# Не работает в Apache
# from openpyxl import Workbook

from telekom.models import PayHistory, UserTable

from datetime import date

# Для минуса месяцев с даты
from dateutil.relativedelta import relativedelta



def exportZakaz(request, etrap):

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    
    if etrap in etraps:
        users = UserTable.objects.filter(etrap=etrap)
    else:
        users = UserTable.objects.all()
        
        # 1 месяц
    if request.method == 'POST' and 'zakaz1Month' in request.POST:

        users = users.exclude(name__exact='', surname__exact='')
        users = users.filter(b_zakaz__lt = 0 )
        

        start = str(date.today() - relativedelta(months=1)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        start2 = str(date.today() - relativedelta(months=2)) + ' 00:00:00'
        end2 = str(date.today() - relativedelta(months=1)) + ' 00:00:00'

        payHistory = PayHistory.objects.filter(date__range=[start, end], zakaz__gt=0)
        payHistory2 = PayHistory.objects.filter(date__range=[start2, end2], zakaz__gt=0)
        
        new_users = []
        for user in users:
            if user.b_zakaz < 0:
                pays = payHistory.filter(abonent=user)
                pays2 = payHistory2.filter(abonent=user)
                if len(pays) == 0 and len(pays2) > 0:
                    new_users.append(user)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="zakaz 1 ay minus {etrap}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'zakaz minus {etrap}'

        headers = ['ID', 'Etrap', 'Номер', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Кв', 'Сотовый', 'Предприятие', 'Хоз/Бюд', 'Счет', 'Номер по счету', 'Метры', 'Льготник', 'Подключенные Услуги', 
                    'Баланс абонплата', 'Баланс СЛР', 'Баланс КОД', 'Баланс Заказ', 'Баланс Прочее', 'Баланс доп. услуги']
        
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
                        user.sotowyy, userIs_enterprises, userHb, user.account, userCountOfNumber, userAbonLength, userBeneficiary, userService,
                            "%.2f" % user.b_telefon, "%.2f" % user.b_slr, "%.2f" % user.b_kod, "%.2f" % user.b_zakaz, "%.2f" % user.b_prochee, "%.2f" % user.b_dop_uslugi])    
        
        wb.save(response)
        return response
    
    # 2 месяца
    if request.method == 'POST' and 'zakaz2Month' in request.POST:
        users = users.exclude(name__exact='', surname__exact='')
        users = users.filter(b_zakaz__lt = 0 )

        start = str(date.today() - relativedelta(months=2)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        start2 = str(date.today() - relativedelta(months=3)) + ' 00:00:00'
        end2 = str(date.today() - relativedelta(months=2)) + ' 00:00:00'

        payHistory = PayHistory.objects.filter(date__range=[start, end], zakaz__gt=0)
        payHistory2 = PayHistory.objects.filter(date__range=[start2, end2], zakaz__gt=0)


        new_users = []
        for user in users:
            if user.b_zakaz < 0:
                pays = payHistory.filter(abonent=user)
                pays2 = payHistory2.filter(abonent=user)
                if len(pays) == 0  and len(pays2) > 0:
                    new_users.append(user)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="zakaz 2 ay minus {etrap}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'zakaz minus {etrap}'

        headers = ['ID', 'Etrap', 'Номер', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Кв', 'Сотовый', 'Предприятие', 'Хоз/Бюд', 'Счет', 'Номер по счету', 'Метры', 'Льготник', 'Подключенные Услуги', 
                    'Баланс абонплата', 'Баланс СЛР', 'Баланс КОД', 'Баланс Заказ', 'Баланс Прочее', 'Баланс доп. услуги']
        
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
                        user.sotowyy, userIs_enterprises, userHb, user.account, userCountOfNumber, userAbonLength, userBeneficiary, userService,
                            "%.2f" % user.b_telefon, "%.2f" % user.b_slr, "%.2f" % user.b_kod, "%.2f" % user.b_zakaz, "%.2f" % user.b_prochee, "%.2f" % user.b_dop_uslugi])    
        
        wb.save(response)
        return response
    
    # 3 месяца
    if request.method == 'POST' and 'zakaz3Month' in request.POST:
        users = users.exclude(name__exact='', surname__exact='')
        users = users.filter(b_zakaz__lt = 0 )

        start = str(date.today() - relativedelta(months=3)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        start2 = str(date.today() - relativedelta(months=4)) + ' 00:00:00'
        end2 = str(date.today() - relativedelta(months=3)) + ' 00:00:00'

        payHistory = PayHistory.objects.filter(date__range=[start, end], zakaz__gt=0)
        payHistory2 = PayHistory.objects.filter(date__range=[start2, end2], zakaz__gt=0)


        new_users = []
        for user in users:
            if user.b_zakaz < 0:
                pays = payHistory.filter(abonent=user)
                pays2 = payHistory2.filter(abonent=user)
                if len(pays) == 0  and len(pays2) > 0:
                    new_users.append(user)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="zakaz 3 ay minus {etrap}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'zakaz minus {etrap}'

        headers = ['ID', 'Etrap', 'Номер', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Кв', 'Сотовый', 'Предприятие', 'Хоз/Бюд', 'Счет', 'Номер по счету', 'Метры', 'Льготник', 'Подключенные Услуги', 
                    'Баланс абонплата', 'Баланс СЛР', 'Баланс КОД', 'Баланс Заказ', 'Баланс Прочее', 'Баланс доп. услуги']
        
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
                        user.sotowyy, userIs_enterprises, userHb, user.account, userCountOfNumber, userAbonLength, userBeneficiary, userService,
                            "%.2f" % user.b_telefon, "%.2f" % user.b_slr, "%.2f" % user.b_kod, "%.2f" % user.b_zakaz, "%.2f" % user.b_prochee, "%.2f" % user.b_dop_uslugi])    
        
        wb.save(response)
        return response
    
    # 4 месяца
    if request.method == 'POST' and 'zakaz4Month' in request.POST:
        users = users.exclude(name__exact='', surname__exact='')
        users = users.filter(b_zakaz__lt = 0 )

        start = str(date.today() - relativedelta(months=4)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        start2 = str(date.today() - relativedelta(months=5)) + ' 00:00:00'
        end2 = str(date.today() - relativedelta(months=4)) + ' 00:00:00'

        payHistory = PayHistory.objects.filter(date__range=[start, end], zakaz__gt=0)
        payHistory2 = PayHistory.objects.filter(date__range=[start2, end2], zakaz__gt=0)


        new_users = []
        for user in users:
            if user.b_zakaz < 0:
                pays = payHistory.filter(abonent=user)
                pays2 = payHistory2.filter(abonent=user)
                if len(pays) == 0  and len(pays2) > 0:
                    new_users.append(user)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="zakaz 4 ay minus {etrap}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'zakaz minus {etrap}'

        headers = ['ID', 'Etrap', 'Номер', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Кв', 'Сотовый', 'Предприятие', 'Хоз/Бюд', 'Счет', 'Номер по счету', 'Метры', 'Льготник', 'Подключенные Услуги', 
                    'Баланс абонплата', 'Баланс СЛР', 'Баланс КОД', 'Баланс Заказ', 'Баланс Прочее', 'Баланс доп. услуги']
        
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
                        user.sotowyy, userIs_enterprises, userHb, user.account, userCountOfNumber, userAbonLength, userBeneficiary, userService,
                            "%.2f" % user.b_telefon, "%.2f" % user.b_slr, "%.2f" % user.b_kod, "%.2f" % user.b_zakaz, "%.2f" % user.b_prochee, "%.2f" % user.b_dop_uslugi])    
        
        wb.save(response)
        return response
    

    # 5 месяца
    if request.method == 'POST' and 'zakaz5Month' in request.POST:
        users = users.exclude(name__exact='', surname__exact='')
        users = users.filter(b_zakaz__lt = 0 )

        start = str(date.today() - relativedelta(months=5)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        start2 = str(date.today() - relativedelta(months=6)) + ' 00:00:00'
        end2 = str(date.today() - relativedelta(months=5)) + ' 00:00:00'

        payHistory = PayHistory.objects.filter(date__range=[start, end], zakaz__gt=0)
        payHistory2 = PayHistory.objects.filter(date__range=[start2, end2], zakaz__gt=0)


        new_users = []
        for user in users:
            if user.b_zakaz < 0:
                pays = payHistory.filter(abonent=user)
                pays2 = payHistory2.filter(abonent=user)
                if len(pays) == 0  and len(pays2) > 0:
                    new_users.append(user)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="zakaz 5 ay minus {etrap}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'zakaz minus {etrap}'

        headers = ['ID', 'Etrap', 'Номер', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Кв', 'Сотовый', 'Предприятие', 'Хоз/Бюд', 'Счет', 'Номер по счету', 'Метры', 'Льготник', 'Подключенные Услуги', 
                    'Баланс абонплата', 'Баланс СЛР', 'Баланс КОД', 'Баланс Заказ', 'Баланс Прочее', 'Баланс доп. услуги']
        
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
                        user.sotowyy, userIs_enterprises, userHb, user.account, userCountOfNumber, userAbonLength, userBeneficiary, userService,
                            "%.2f" % user.b_telefon, "%.2f" % user.b_slr, "%.2f" % user.b_kod, "%.2f" % user.b_zakaz, "%.2f" % user.b_prochee, "%.2f" % user.b_dop_uslugi])    
        
        wb.save(response)
        return response
    
    # 6 месяца
    if request.method == 'POST' and 'zakaz6Month' in request.POST:
        users = users.exclude(name__exact='', surname__exact='')
        users = users.filter(b_zakaz__lt = 0 )

        start = str(date.today() - relativedelta(months=6)) + ' 00:00:00'
        end = str(date.today()) + ' 23:59:59'

        start2 = str(date.today() - relativedelta(months=7)) + ' 00:00:00'
        end2 = str(date.today() - relativedelta(months=6)) + ' 00:00:00'

        payHistory = PayHistory.objects.filter(date__range=[start, end], zakaz__gt=0)
        payHistory2 = PayHistory.objects.filter(date__range=[start2, end2], zakaz__gt=0)


        new_users = []
        for user in users:
            if user.b_zakaz < 0:
                pays = payHistory.filter(abonent=user)
                pays2 = payHistory2.filter(abonent=user)
                if len(pays) == 0  and len(pays2) > 0:
                    new_users.append(user)

        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="zakaz 6 ay minus {etrap}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'zakaz minus {etrap}'

        headers = ['ID', 'Etrap', 'Номер', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Кв', 'Сотовый', 'Предприятие', 'Хоз/Бюд', 'Счет', 'Номер по счету', 'Метры', 'Льготник', 'Подключенные Услуги', 
                    'Баланс абонплата', 'Баланс СЛР', 'Баланс КОД', 'Баланс Заказ', 'Баланс Прочее', 'Баланс доп. услуги']
        
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
                        user.sotowyy, userIs_enterprises, userHb, user.account, userCountOfNumber, userAbonLength, userBeneficiary, userService,
                            "%.2f" % user.b_telefon, "%.2f" % user.b_slr, "%.2f" % user.b_kod, "%.2f" % user.b_zakaz, "%.2f" % user.b_prochee, "%.2f" % user.b_dop_uslugi])    
        
        wb.save(response)
        return response
