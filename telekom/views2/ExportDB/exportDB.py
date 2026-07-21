
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import Group

# Не работает в Apache
# from openpyxl import Workbook

from telekom.models import KabelCount, NachMinus, NachisleniyaOtchet, PayHistory, StaffAction, UserTable
from telekom.views2.myFunc.myFunc import getLoggedUserEtrap, loggedUserEtrapAndGroup, monthСonvert

from datetime import date, datetime

from calendar import monthrange
# Для минуса месяцев с даты
from dateutil.relativedelta import relativedelta
import re




def exportDB(request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request,"Скачивать данные могут только соотрудники MTB")
        return redirect('user-login')

    context = {}

    context['log'] = log
    context['matbIndex'] = True
    context['exportDB'] = True

    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date
    current_year = current_date[0:4]
    current_month = current_date[5:7]
    current_day = current_date[8:]
    days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['etraps'] = etraps
    etrap = request.GET.get('etrap')
    context['etrap'] = etrap

    if etrap in etraps:
        users = UserTable.objects.filter(etrap=etrap)
    else:
        users = UserTable.objects.all()



    #################
    ## База Данных ##
    #################
    if request.method == 'POST' and 'allDB' in request.POST:


        users = users.exclude(name__exact='', surname__exact='')

        response = HttpResponse(content_type='application/ms-excel')

        response['Content-Disposition'] = f'attachment; filename="DB {etrap}.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = f'Data Base'

        

        # , , , , , , , , , , , , 
        # , abon_length_connect_date, count_of_numbers_connect_date, 
        # , is_on_date, , connect_date, kabel_comments, , , , 
        # , , , , , , , , , addDate

        # Add headers
        headers = ['ID', 'Etrap', 'Номер', 'Фамилия', 'Имя', 'Улица', 'Дом', 'Кв', 'Сотовый', 'Предприятие', 'Хоз/Бюд', 'Счет', 'Alem TV', 'Кабель TV', 'Кабель Id', 'Кабель подключен?', 'Логин', 
                    'Договор', 'Интернет', 'Номер по счету', 'Метры', 'Льготник', 'Подключенные Услуги', 
                    'Баланс интернет', 'Баланс кабель', 'Баланс alem', 'Баланс абонплата', 'Баланс СЛР', 'Баланс КОД', 'Баланс Заказ', 'Баланс Прочее', 'Баланс доп. услуги']

        ws.append(headers)

        # add Data
        for user in users:
            if user.is_on:
                userIs_on = 'Вкл'
            else:
                userIs_on = ''
            
            if user.is_enterprises:
                userIs_enterprises = 'Да'
            else:
                userIs_enterprises = ''

            if user.hb:
                userHb = user.hb.name
            else:
                userHb = ''

            if user.alem:
                userAlem = 'Да'
            else:
                userAlem = ''

            if user.kabel_count:
                userKabelCount = f"{user.kabel_count.kabel_count} точек"
            else:
                userKabelCount = ''

            if user.internet_tarif:
                userInternet = user.internet_tarif.tarif
            else:
                userInternet = ''

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
                        user.sotowyy, userIs_enterprises, userHb, user.account, userAlem, userKabelCount, user.ids, userIs_on, user.login, user.dogowor, 
                        userInternet, userCountOfNumber, userAbonLength, userBeneficiary, userService,
                        "%.2f" % user.b_internet, "%.2f" % user.b_kabel, "%.2f" % user.b_alem, "%.2f" % user.b_telefon, "%.2f" % user.b_slr,
                        "%.2f" % user.b_kod, "%.2f" % user.b_zakaz, "%.2f" % user.b_prochee, "%.2f" % user.b_dop_uslugi])

        # save
        wb.save(response)
        return response
    
    #####################
    ## База Данных END ##
    #####################

    return render(request, 'telekom/MATB/ExportDB/exportDB.html', context)

