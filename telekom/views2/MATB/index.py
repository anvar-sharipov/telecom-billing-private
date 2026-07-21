
from django.shortcuts import render, redirect
from django.contrib import messages

import re
from datetime import datetime
from datetime import date
from calendar import monthrange
from dateutil.relativedelta import relativedelta
from django.db.models import Q

from django.contrib.auth.models import Group
from django.db.models.functions import Cast
from django.db.models import F, IntegerField

from telekom.forms import UserTableForm
from telekom.models import DontRepeatYourself, ImportAlemNachisleniyaOFF, ImportAlemNachisleniyaON, NachisleniyaOtchet, OldLoginDogowor, UserTableArhiw, dbfNameList, ImportInternetNachisleniyaOFF, ImportInternetNachisleniyaON
from telekom.models import ImportInternetPlateji, ImportInternetPlatejiOFF, InterpayBilling, LocalCall, NachMinus, NonLocalCall, PayHistory, UserTable, HozOrBudjet, StaffAction, Zakaz, SnyatieInfo, BazaChangeInfo
from telekom.views2.myFunc.myFunc import get_etrap_and_types, getAddDict, getDelDict, getPay, loggedUserEtrapAndGroup, monthСonvert, saveDelServOnDelDict

from django.db import transaction
import logging
logger = logging.getLogger(__name__)


def matbIndex(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            log = 'Dashoguz'
            context['matbIndex'] = True
            context['is_allow_to_cahnge_base'] = True
        else:
            etrap_types = get_etrap_and_types(request.user)
            etraps = etrap_types['etraps']
            log = etraps[0]
            types = etrap_types['types']
            if 'MTB' in types:
                context['matbIndex'] = True
                context['is_allow_to_cahnge_base'] = True
                if 'Gayyp' in request.user.username:
                    context['is_allow_to_cahnge_base'] = True
            else:
                context['is_allow_to_cahnge_base'] = False
                if 'Kassa' in types:
                    context['kassaIndex'] = True
                    # context['kassa'] = True
                if 'MB' in types:
                    context['setService'] = True
                    context['KassaMB'] = True
                if 'Internet' in types:
                    context['internetBilling'] = True
                    context['dataBaseInternet'] = True
                if 'SHB' in types:
                    context['SHBIndex'] = True
                    # context['KassaSHB'] = True
                    context['dataBaseInternet'] = True
                if '071' in types:
                    context['operator071'] = True
                    # context['Kassa071'] = True 
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')
    
    # EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    # if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
    #     log = EtrapAndGroup[0]
    #     context['matbIndex'] = True
    #     context['dataBase'] = True
    # elif EtrapAndGroup[1] == 'Internet':
    #     log = EtrapAndGroup[0]
    #     context['internetBilling'] = True
    #     context['dataBaseInternet'] = True
    # else:
    #     messages.error(request, f'Доступ только соотрудникам MATB')
    #     return redirect('user-login')
    
    
    # print(type(request.META['SERVER_NAME']))

    # UserTable.objects.all().delete()

    # LocalCall.objects.all().delete()
    # NonLocalCall.objects.all().delete()
    # ImportInternetPlateji.objects.all().delete()
    # ImportInternetPlatejiOFF.objects.all().delete()
    # DontRepeatYourself.objects.all().delete()
    # ImportInternetNachisleniyaON.objects.all().delete()
    # ImportInternetNachisleniyaOFF.objects.all().delete()
    # NachMinus.objects.all().delete()
    # PayHistory.objects.all().delete()
    # InterpayBilling.objects.all().delete()
    # Zakaz.objects.all().delete()

    # dbfNameList.objects.all().delete()
    # dbf_name_list = dbfNameList.objects.all()
    # for name in dbf_name_list:
    #     name.is_nach = False
    #     name.save()

    # NachisleniyaOtchet.objects.all().delete()
    # ImportAlemNachisleniyaON.objects.all().delete()
    # ImportAlemNachisleniyaOFF.objects.all().delete()
    # StaffAction.objects.all().delete()
    
    # UserTableArhiw.objects.all().delete()
    
    # users = UserTable.objects.all()
    # count = 0
    # for user in users:
    #     if user.b_telefon or user.b_slr or user.b_kod or user.b_zakaz or user.b_prochee or user.b_dop_uslugi or user.b_internet or user.b_kabel or user.b_alem:
    #         user.b_telefon = 0
    #         user.b_slr = 0
    #         user.b_kod = 0
    #         user.b_zakaz = 0
    #         user.b_prochee = 0
    #         user.b_dop_uslugi = 0
    #         user.b_internet = 0
    #         user.b_kabel = 0
    #         user.b_alem = 0
    #         user.save()

    # n = NachMinus.objects.all()
    # for i in n:
    #     if i.zakaz != 0:
    #         i.zakaz = 0
    #         i.save()
        
        
    #     user.name = ''
    #     user.surname = ''
    #     user.street = ''
    #     user.home = ''
    #     user.flat = ''
    #     user.sotowyy = ''
    #     user.is_enterprises = False
    #     user.account = None
    #     user.hb = None
        # if user.dogowor != '':

            # count += 1
            # user.dogowor = ''
            # user.save()

    # for i in range(100):
    #     PayHistory.objects.create(abonent=UserTable.objects.get(pk=i+(50000)), kassir='kassadashoguz1', date=datetime.now(), telefon = i, internet = i, alem = i, kabel = i)
    


    # UserTable.objects.filter(number='20120', etrap='Dashoguz').update(b_alem=-1, surname='gg', name='ff')
    # UserTable.objects.filter(number='20121', etrap='Dashoguz').update(b_alem=-1, surname='gg', name='ff')
    # UserTable.objects.filter(number='20122', etrap='Dashoguz').update(b_alem=-1, surname='gg', name='ff')
    # UserTable.objects.filter(number='20123', etrap='Dashoguz').update(b_alem=-1, surname='gg', name='ff')
    # UserTable.objects.filter(number='20124', etrap='Dashoguz').update(b_alem=-1, surname='gg', name='ff')
    # UserTable.objects.filter(number='20125', etrap='Dashoguz').update(b_alem=-1, surname='gg', name='ff')
    # UserTable.objects.filter(number='20126', etrap='Dashoguz').update(b_alem=-1, surname='gg', name='ff')

    # PayHistory.objects.create(abonent=UserTable.objects.get(number='20120', etrap='Dashoguz'), kassir='kassadashoguz1', alem=2, date=datetime(2023, 9, 14, 12, 12, 12, 78915))
    # PayHistory.objects.create(abonent=UserTable.objects.get(number='20121', etrap='Dashoguz'), kassir='kassadashoguz1', alem=2, date=datetime(2023, 8, 14, 12, 12, 12, 78915))
    # PayHistory.objects.create(abonent=UserTable.objects.get(number='20122', etrap='Dashoguz'), kassir='kassadashoguz1', alem=2, date=datetime(2023, 7, 14, 12, 12, 12, 78915))
    # PayHistory.objects.create(abonent=UserTable.objects.get(number='20123', etrap='Dashoguz'), kassir='kassadashoguz1', alem=2, date=datetime(2023, 6, 14, 12, 12, 12, 78915))
    # PayHistory.objects.create(abonent=UserTable.objects.get(number='20124', etrap='Dashoguz'), kassir='kassadashoguz1', alem=2, date=datetime(2023, 5, 14, 12, 12, 12, 78915))
    # PayHistory.objects.create(abonent=UserTable.objects.get(number='20125', etrap='Dashoguz'), kassir='kassadashoguz1', alem=2, date=datetime(2023, 4, 14, 12, 12, 12, 78915))
    # payHistory = PayHistory.objects.create(abonent=UserTable.objects.get(number='20126', etrap='Dashoguz'), kassir=request.user.username, alem=2, date=datetime(2023, 3, 14, 12, 12, 12, 78915))

    # nachMinus = NachMinus.objects.get(user=UserTable.objects.get(number='20003', etrap='Dashoguz'), year='2023', month='01')
    # nachMinus.kod = 2
    # nachMinus.prochee = 2
    # nachMinus.save()

    # fast update all balnce = 0
    # UserTable.objects.filter(etrap='Dashoguz').update(b_telefon=0, b_slr=0, b_kod=0, b_zakaz=0, b_prochee=0, b_dop_uslugi=0, b_internet=0, b_alem=0, b_kabel=0)

    # InterpayBilling.objects.create(pay_history=payHistory, operator=request.user)
    current_date = str(date.today())
    context['current_date'] = current_date
    current_year = current_date[0:4]
    current_month = current_date[5:7]
    current_day = current_date[8:]
    days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]


    # log = getLoggedUserEtrap(request.user.username)
    context['log'] = log
    context['etrap'] = request.POST.get('etrap')
    context['etraps'] = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']

    if request.GET.get('akt_raport'):
        akt_raport = request.GET.get('akt_raport')
    else:
        akt_raport = current_date
    context['akt_raport'] = akt_raport

    HB = []
    for i in HozOrBudjet.objects.all():
        HB.append(i)
    context['HB'] = HB
    # Если нажал на выбрать в списке отфильтрованных данных
    if request.GET.get('user_pk'):
        abonent = UserTable.objects.get(pk=request.GET.get('user_pk'))
        number = abonent.number
        etrap = abonent.etrap
        context['num'] = f"{number[:1]}-{number[1:3]}-{number[3:5]}"
        context['etrap'] = etrap

        filter_etrap = request.GET.get('filter_etrap') if request.GET.get('filter_etrap') != None else ''
        name = request.GET.get('name') if request.GET.get('name') != None else ''
        surname = request.GET.get('surname') if request.GET.get('surname') != None else ''
        street = request.GET.get('street') if request.GET.get('street') != None else ''
        home = request.GET.get('home') if request.GET.get('home') != None else ''
        flat = request.GET.get('flat') if request.GET.get('flat') != None else ''
        login = request.GET.get('login') if request.GET.get('login') != None else ''
        dogowor = request.GET.get('dogowor') if request.GET.get('dogowor') != None else ''
        filter_Naseleniye_or_Edara = request.GET.get('filter_Naseleniye_or_Edara')
        filter_account = request.GET.get('filter_account') if request.GET.get('filter_account') != None else ''

        

        context['name'] = name
        context['surname'] = surname
        context['street'] = street
        context['home'] = home
        context['flat'] = flat
        context['login'] = login
        context['dogowor'] = dogowor
        context['filter_etrap'] = filter_etrap
        context['filter_Naseleniye_or_Edara'] = filter_Naseleniye_or_Edara
        context['filter_account'] = filter_account
       

        
        
        if filter_Naseleniye_or_Edara == 'filter_and_edara_and_naseleniye':
            if filter_account:
                filtered_objs = UserTable.objects.filter(
                Q(etrap__icontains=filter_etrap) &
                Q(surname__icontains=surname) &
                Q(name__icontains=name) &
                Q(street__icontains=street) &
                Q(login__icontains = login)&
                Q(dogowor__icontains = dogowor)&
                Q(home__icontains=home) &
                Q(flat__icontains=flat)
                ).filter(account=filter_account).order_by('number')
            else:
                filtered_objs = UserTable.objects.filter(
                Q(etrap__icontains=filter_etrap) &
                Q(surname__icontains=surname) &
                Q(name__icontains=name) &
                Q(street__icontains=street) &
                Q(login__icontains = login)&
                Q(dogowor__icontains = dogowor)&
                Q(home__icontains=home) &
                Q(flat__icontains=flat)
                ).order_by('number')
        
        elif filter_Naseleniye_or_Edara == 'filter_edara':
            if filter_account:
                filtered_objs = UserTable.objects.filter(
                Q(etrap__icontains=filter_etrap) &
                Q(surname__icontains=surname) &
                Q(name__icontains=name) &
                Q(street__icontains=street) &
                Q(login__icontains = login)&
                Q(dogowor__icontains = dogowor)&
                Q(home__icontains=home) &
                Q(flat__icontains=flat) &
                Q(is_enterprises=True)
                ).filter(account=filter_account).order_by('number')
            else:
                filtered_objs = UserTable.objects.filter(
                Q(etrap__icontains=filter_etrap) &
                Q(surname__icontains=surname) &
                Q(name__icontains=name) &
                Q(street__icontains=street) &
                Q(login__icontains = login)&
                Q(dogowor__icontains = dogowor)&
                Q(home__icontains=home) &
                Q(flat__icontains=flat) &
                Q(is_enterprises=True)
                ).order_by('account')

        elif filter_Naseleniye_or_Edara == 'filter_naseleniye':
            if filter_account:
                filtered_objs = UserTable.objects.filter(
                Q(etrap__icontains=filter_etrap) &
                Q(surname__icontains=surname) &
                Q(name__icontains=name) &
                Q(street__icontains=street) &
                Q(login__icontains = login)&
                Q(dogowor__icontains = dogowor)&
                Q(home__icontains=home) &
                Q(flat__icontains=flat) &
                Q(is_enterprises=False)
                ).filter(account=filter_account).order_by('number')
            else:
                filtered_objs = UserTable.objects.filter(
                Q(etrap__icontains=filter_etrap) &
                Q(surname__icontains=surname) &
                Q(name__icontains=name) &
                Q(street__icontains=street) &
                Q(login__icontains = login)&
                Q(dogowor__icontains = dogowor)&
                Q(home__icontains=home) &
                Q(flat__icontains=flat) &
                Q(is_enterprises=False)
                ).order_by('account')

        context['filtered_objs'] = filtered_objs
        context['len_filtered_objs'] = len(filtered_objs)

    else:
        context['num'] = request.GET.get('search_number')
        etrap = etrap=request.GET.get('etrap')
        context['etrap'] = etrap

        if request.GET.get('search_number'):
            number = re.sub('[-]', '', request.GET.get('search_number'))
            try:
                abonent = UserTable.objects.get(number=number, etrap=request.GET.get('etrap'))
            except:
                abonent = ''
        else:
            abonent = ''

        anotherName = request.GET.get('raspor')
        context['anotherName'] = anotherName




    context['abonent'] = abonent
    if abonent:
        if abonent.intOnDate:
            context['formatted_intOnDate'] = f"{str(abonent.intOnDate)[:4]}-{str(abonent.intOnDate)[5:7]}-{str(abonent.intOnDate)[-2:]}"
        if abonent.intOffDate:
            # formatted_intOffDate = abonent.intOffDate.strftime('%Y-%m-%d')
            context['formatted_intOffDate'] = f"{str(abonent.intOffDate)[:4]}-{str(abonent.intOffDate)[5:7]}-{str(abonent.intOffDate)[-2:]}"
        
    # if abonent:
    #     if abonent.addDate:
    #         formatted_addDate = abonent.addDate.strftime('%Y-%m-%d')
    #         context['formatted_addDate'] = formatted_addDate


    if request.method == 'POST' and 'filter' in request.POST:
        # Если нажал на фильтр
        context['akt_raport'] = request.POST.get('akt_filter')
        filter_etrap = request.POST.get('etrap')
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        street = request.POST.get('street')
        home = request.POST.get('home')
        flat = request.POST.get('flat')
        login = request.POST.get('login').lower().strip()
        dogowor = request.POST.get('dogowor').upper().strip()
        filter_Naseleniye_or_Edara = request.POST.get('filter_Naseleniye_or_Edara')
        filter_account = request.POST.get('filter_account') if request.POST.get('filter_account') != None else ''
        
        

        context['name'] = name
        context['surname'] = surname
        context['street'] = street
        context['home'] = home
        context['flat'] = flat
        context['login'] = login
        context['dogowor'] = dogowor
        context['filter_etrap'] = filter_etrap
        context['filter_Naseleniye_or_Edara'] = filter_Naseleniye_or_Edara
        context['filter_account'] = filter_account
        
        if filter_Naseleniye_or_Edara == 'filter_and_edara_and_naseleniye':
            if filter_account:
                filtered_objs = UserTable.objects.filter(
                Q(etrap__icontains=filter_etrap) &
                Q(surname__icontains=surname) &
                Q(name__icontains=name) &
                Q(street__icontains=street) &
                Q(login__icontains = login)&
                Q(dogowor__icontains = dogowor)&
                Q(home__icontains=home) &
                Q(flat__icontains=flat)
                ).filter(account=filter_account).order_by('number')
            else:
                filtered_objs = UserTable.objects.filter(
                Q(etrap__icontains=filter_etrap) &
                Q(surname__icontains=surname) &
                Q(name__icontains=name) &
                Q(street__icontains=street) &
                Q(login__icontains = login)&
                Q(dogowor__icontains = dogowor)&
                Q(home__icontains=home) &
                Q(flat__icontains=flat)
                ).order_by('number')

        elif filter_Naseleniye_or_Edara == 'filter_edara':
            if filter_account:
                filtered_objs = UserTable.objects.filter(
                Q(etrap__icontains=filter_etrap) &
                Q(surname__icontains=surname) &
                Q(name__icontains=name) &
                Q(street__icontains=street) &
                Q(login__icontains = login)&
                Q(dogowor__icontains = dogowor)&
                Q(home__icontains=home) &
                Q(flat__icontains=flat) &
                Q(is_enterprises=True)
                ).filter(account=filter_account).order_by('number')
            else:
                filtered_objs = UserTable.objects.filter(
                Q(etrap__icontains=filter_etrap) &
                Q(surname__icontains=surname) &
                Q(name__icontains=name) &
                Q(street__icontains=street) &
                Q(login__icontains = login)&
                Q(dogowor__icontains = dogowor)&
                Q(home__icontains=home) &
                Q(flat__icontains=flat) &
                Q(is_enterprises=True)
                ).order_by('account')

        elif filter_Naseleniye_or_Edara == 'filter_naseleniye':
            if filter_account:
                filtered_objs = UserTable.objects.filter(
                Q(etrap__icontains=filter_etrap) &
                Q(surname__icontains=surname) &
                Q(name__icontains=name) &
                Q(street__icontains=street) &
                Q(login__icontains = login)&
                Q(dogowor__icontains = dogowor)&
                Q(home__icontains=home) &
                Q(flat__icontains=flat) &
                Q(is_enterprises=False)
                ).filter(account=filter_account).order_by('number')
            else:
                filtered_objs = UserTable.objects.filter(
                Q(etrap__icontains=filter_etrap) &
                Q(surname__icontains=surname) &
                Q(name__icontains=name) &
                Q(street__icontains=street) &
                Q(login__icontains = login)&
                Q(dogowor__icontains = dogowor)&
                Q(home__icontains=home) &
                Q(flat__icontains=flat) &
                Q(is_enterprises=False)
                ).order_by('account')




        context['filtered_objs'] = filtered_objs
        context['len_filtered_objs'] = len(filtered_objs)

        






    # если нажал на сохранить Добавления/Изменения абонента
    if request.method == 'POST' and 'filter' not in request.POST:
        try:
            with transaction.atomic():

                old_name = abonent.name
                old_surname = abonent.surname
                old_street = abonent.street
                old_home = abonent.home
                old_flat = abonent.flat
                old_sotowyy = abonent.sotowyy
                old_login = abonent.login.lower().strip()
                old_dogowor = abonent.dogowor.upper().strip()
                old_account = abonent.account
                old_abonplata = abonent.abonplata

                if abonent.intOnDate:
                    old_intOnDate = abonent.intOnDate.strftime('%Y-%m-%d')
                else:
                    old_intOnDate = None
                
                if abonent.intOffDate:
                    old_intOffDate = abonent.intOffDate.strftime('%Y-%m-%d')
                else:
                    old_intOffDate = None



                
                if abonent.is_enterprises:
                    old_edara = True
                else:
                    old_edara = False

                if abonent.snyat_bool:
                    old_snyat = True
                else:
                    old_snyat = False

                if abonent.hb:
                    old_hb = str(abonent.hb.pk)
                else:
                    old_hb = ''

                if abonent.beneficiary:
                    old_beneficiary = True
                else:
                    old_beneficiary = False

                # old_addDate = str(abonent.addDate) if abonent.addDate != None else ''

                new_name = request.POST.get('name')
                new_surname = request.POST.get('surname')

                new_street = request.POST.get('street')
                new_home = request.POST.get('home')
                new_flat = request.POST.get('flat')
                new_sotowyy = re.sub('[-]', '', request.POST.get('sotowyy')) 
                new_login = request.POST.get('login').lower().strip()
                new_dogowor = request.POST.get('dogowor').upper().strip()
                new_account = None if request.POST.get('account') in ['', None] else int(request.POST.get('account'))
                new_abonplata = request.POST.get('abonplata')

                if new_dogowor and not new_login or (new_login and not new_dogowor):
                    messages.error(request, f"Неправильный логин или договор")
                    return render(request, 'telekom/MATB/matbIndex.html', context)

                new_intOnDate = request.POST.get('intOnDate') if request.POST.get('intOnDate') else None
                new_intOffDate = request.POST.get('intOffDate') if request.POST.get('intOffDate') else None
            

                ###

                forHistoryLogin = request.POST.get('reasonLogin')  
                forHistoryDogowor = request.POST.get('reasonDogowor')

                # если логин изменен но причина изменения не выбрана
                # if new_login != old_login and forHistoryLogin == 'reason':
                #     messages.error(request, f"Выберите причину изменения логина")
                #     return render(request, 'telekom/MATB/matbIndex.html', context)

                # если договор изменен но причина изменения не выбрана
                print('2222333333',new_login, new_dogowor)
                if new_dogowor and new_dogowor != old_dogowor:
                    if UserTable.objects.filter(dogowor=new_dogowor).exists():
                        messages.error(request, f"Такой договор уже есть в БД")
                        return render(request, 'telekom/MATB/matbIndex.html', context)


                    if OldLoginDogowor.objects.filter(dogowor=new_dogowor).exists() and forHistoryDogowor == 'change':
                        messages.error(request, f"Такой договор {new_dogowor} уже есть в Old")
                        return render(request, 'telekom/MATB/matbIndex.html', context)

                    if forHistoryDogowor == 'reason':
                        messages.error(request, f"Выберите сохранить или нет договор в old")
                        return render(request, 'telekom/MATB/matbIndex.html', context)

                if new_login and new_login != old_login:
                    if UserTable.objects.filter(login=new_login).exists():
                        messages.error(request, f"Такой логин уже есть в БД")
                        return render(request, 'telekom/MATB/matbIndex.html', context)

                    if OldLoginDogowor.objects.filter(login=new_login).exists() and forHistoryDogowor == 'change':
                        messages.error(request, f"Такой логин {new_login} уже есть в Old")
                        return render(request, 'telekom/MATB/matbIndex.html', context)

                    if forHistoryDogowor == 'reason':
                        messages.error(request, f"Выберите сохранить или нет логин в old")
                        return render(request, 'telekom/MATB/matbIndex.html', context)
                
                # Если логин изменен и причина это удаления или замена (сохраняем старый логин в OldLoginDogowor)
                loginChanged = True
                # if new_login != old_login and forHistoryLogin == 'change':
                #     loginChanged = True

                # Если договор изменен и причина это удаления или замена (сохраняем старый договор в OldLoginDogowor)
                dogoworChanged = False
                if new_dogowor != old_dogowor and forHistoryDogowor == 'change':
                    dogoworChanged = True

                if loginChanged or dogoworChanged:
                    if dogoworChanged == True:
                        # # Если такой логин уже есть в OldLoginDogowor то запретить
                        # try:
                        #     OldLoginDogowor.objects.get(login=abonent.login)
                        #     messages.error(request, f"Вы не можете изменить логин, так как текущий логин уже есть в Old логинах")
                        #     return render(request, 'telekom/MATB/matbIndex.html', context)
                        # except:
                        #     pass
                        # Если такой договор уже есть в OldLoginDogowor то запретить
                        try:
                            OldLoginDogowor.objects.get(dogowor=abonent.dogowor)
                            messages.error(request, f"Ошибка, не возможно сохранить в old login и dogowor")
                            return render(request, 'telekom/MATB/matbIndex.html', context)
                        except:
                            pass

                        # проверка чтобы не было один и тот же логин у 2-х абонентов
                        hb_for_old_log_dog = ''
                        if abonent.hb:
                            hb_for_old_log_dog = abonent.hb.name
                        OldLoginDogowor.objects.create(number=abonent.number, etrap=abonent.etrap, dogowor=abonent.dogowor, login=abonent.login, is_enterprises=abonent.is_enterprises, hb=hb_for_old_log_dog, operator=request.user.username, saved_in_action='База', account=abonent.account)

                    # elif dogoworChanged == False:
                        # //-//
                        # try:
                        #     OldLoginDogowor.objects.get(login=abonent.login)
                        #     messages.error(request, f"Вы не можете изменить логин, так как текущий логин уже есть в Old логинах")
                        #     return render(request, 'telekom/MATB/matbIndex.html', context)
                        # except:
                            # OldLoginDogowor.objects.create(number=abonent.number, etrap=abonent.etrap, login=old_login) 
                    # elif loginChanged == False and dogoworChanged == True:
                    #     # //-//
                    #     try:
                    #         OldLoginDogowor.objects.get(dogowor=abonent.dogowor)
                    #         messages.error(request, f"Вы не можете изменить договор, так как текущий договор уже есть в Old договорах")
                    #         return render(request, 'telekom/MATB/matbIndex.html', context)
                    #     except:
                    #         OldLoginDogowor.objects.create(number=abonent.number, etrap=abonent.etrap, dogowor=old_dogowor.upper())
                        

                ####


                if request.POST.get('edara') == 'on':
                    new_edara = True
                else:
                    new_edara = False

                if request.POST.get('snyat') == 'on':
                    new_snyat = True
                else:
                    new_snyat = False

                if request.POST.get('is_beneficiary') == 'on':
                    new_beneficiary = True
                else:
                    new_beneficiary = False

                new_hb = request.POST.get('hb')
                if new_hb == '1':
                    new_hb_name = 'H'
                elif new_hb == '2':
                    new_hb_name = 'B'
                else:
                    new_hb_name = 'None'
        

                new_addDate = str(request.POST.get('addDate')) if request.POST.get('addDate') != None else ''
                
                if (old_name == new_name and old_surname == new_surname
                    and old_street == new_street and old_home == new_home
                    and old_flat == new_flat and old_sotowyy == new_sotowyy
                    and old_login == new_login and old_dogowor == new_dogowor
                    and old_account == new_account and old_beneficiary == new_beneficiary
                    and old_abonplata == new_abonplata and old_edara == new_edara
                    and old_hb == new_hb and old_snyat == new_snyat
                    and old_intOnDate == new_intOnDate and old_intOffDate == new_intOffDate):
                    messages.error(request, f'Изменений нет')
                elif request.POST.get('comment') == '':
                    messages.error(request, f'Комментарий не может быть пустым')
                else:
                    print('gg', old_surname, new_surname)

                    mess = f'Изменение на полях: '
                    mess_for_BazaChangeInfo = f"""Изменения: 
            """
                    if len(new_sotowyy) == 8 or new_sotowyy == '':
                        pass
                    else:
                        messages.error(request, f'Сотовый номер должен быть в формате 65-11-22-33')
                    

                    if old_surname != new_surname:
                        mess += f' Фамилия,'
                        mess_for_BazaChangeInfo += f"""Фамилия изменено с {abonent.surname} на {new_surname}
            """
                        abonent.surname = new_surname

                    if old_name != new_name:
                        mess += f' Имя,'
                        mess_for_BazaChangeInfo += f"""Имя изменено с {abonent.name} на {new_name}
            """
                        abonent.name = new_name

                    if old_street != new_street:
                        mess += f' Улица,'
                        mess_for_BazaChangeInfo += f"""Улица изменено с {abonent.street} на {new_street}
            """
                        abonent.street = new_street  

                    if old_home != new_home:
                        mess += f' Дом,'
                        mess_for_BazaChangeInfo += f"""Дом изменено с {abonent.home} на {new_home}
            """
                        abonent.home = new_home

                    if old_flat != new_flat:
                        mess += f' Кв.,'
                        mess_for_BazaChangeInfo += f"""Кв. изменено с {abonent.flat} на {new_flat}
            """
                        abonent.flat = new_flat
                        
                    
                    if old_abonplata != new_abonplata:
                        mess += f'Абонплата, с {old_abonplata} на {new_abonplata}'
                        mess_for_BazaChangeInfo += f"""Абонплата изменено с {abonent.abonplata} на {new_abonplata}
            """
                        abonent.abonplata = new_abonplata

                    
                    if old_beneficiary != new_beneficiary:
                        mess += f'Льгота,'
                        mess_for_BazaChangeInfo += f"""Льгота изменено с {abonent.beneficiary} на {new_beneficiary}
            """
                        abonent.beneficiary = new_beneficiary
                    

                    if old_login != new_login:
                        mess += f' Логин c {old_login} на {new_login},'
                        mess_for_BazaChangeInfo += f"""Логин изменено с {abonent.login} на {new_login.lower()}
            """
                        abonent.login = new_login.lower()

                    if old_dogowor != new_dogowor:
                        mess += f' Договор с {old_dogowor} на {new_dogowor.upper()},'
                        mess_for_BazaChangeInfo += f"""Договор изменено с {abonent.dogowor} на {new_dogowor.upper()}
            """
                        abonent.dogowor = new_dogowor.upper()

                    if old_intOnDate != new_intOnDate:
                        mess += f' дата установки инт,'
                        mess_for_BazaChangeInfo += f"""дата установки инт изменено с {abonent.intOnDate} на {new_intOnDate}
            """
                        abonent.intOnDate = new_intOnDate
                    
                    if old_intOffDate != new_intOffDate:
                        mess += f' дата отключения инт,'
                        mess_for_BazaChangeInfo += f"""дата отключения инт изменено с {abonent.intOffDate} на {new_intOffDate}
            """
                        abonent.intOffDate = new_intOffDate

                    if old_edara != new_edara:
                        mess += f' Edara,'
                        mess_for_BazaChangeInfo += f"""Edara изменено с {abonent.is_enterprises} на {new_edara}
            """
                        abonent.is_enterprises = new_edara 

                    if old_account != new_account:
                        mess += f' Счет,'
                        mess_for_BazaChangeInfo += f"""Счет изменено с {abonent.account} на {new_account}
            """
                        abonent.account = new_account


                    if old_sotowyy != new_sotowyy:
                        abonent.sotowyy = new_sotowyy
                        mess += f' Сотовый,'

                    

                    

                    if old_snyat != new_snyat:
                        
                        if new_snyat == True:
                            abonent.snyat_date = datetime.now()
                            mess_for_BazaChangeInfo += f"""Снятие галочка поставлен в {datetime.now()}
            """
                            mess += f' Снят,'
                            abonent.wost_date = None

                            SnyatieInfo.objects.create(
                                number = abonent.number,
                                etrap = abonent.etrap,
                                operator_galochka = request.user.username,
                                date_galochka = datetime.now(),
                                namesurname1 = f"{abonent.surname} {abonent.name}",
                                comment_galochka = request.POST.get('comment')
                            )
                        else:
                            abonent.snyat_date = None
                            mess_for_BazaChangeInfo += f"""Снятие галочка убран в {datetime.now()}
            """
                            mess += f' Востановлен,'
                        
                        abonent.snyat_bool = new_snyat
                        

                    if old_hb != new_hb:
                        if abonent.hb:
                            old_hb_name = abonent.hb.name
                        else:
                            old_hb_name = 'None'
                        mess_for_BazaChangeInfo += f"""Изменения Hoz/Bud c {old_hb_name} на {new_hb_name}
            """
                        if new_hb:
                            abonent.hb = HozOrBudjet.objects.get(pk=new_hb)
                        else:
                            abonent.hb = None
                        mess += f' Hoz/Bud,'

                    # if old_addDate != new_addDate:
                    #     if new_addDate:
                    #         abonent.addDate = request.POST.get('addDate')
                    #     else:
                    #         abonent.addDate = None
                    #     mess += f' Дата добавления,'
                        
                    
                    abonent.save()
                    mess_for_BazaChangeInfo += f"""комментарий {request.POST.get('comment')}"""
                    BazaChangeInfo.objects.create(etrap=abonent.etrap, number=abonent.number, operator=request.user.username, comment=mess_for_BazaChangeInfo, akt_raport=request.GET.get('akt_raport'))

                    # Если добавил нового абонента
                    if old_name == '' and old_surname == '' and (new_name != '' or new_surname != ''):
                        StaffAction.objects.create(akt_raport=request.GET.get('akt_raport'), user=request.user, comment=f"{request.POST.get('comment')} \n\n Добавление нового абонента в базу данных \n\n {mess} \n\n дата добавления {datetime.now()}, номер {abonent.number}]", action='Добавление абонента в MATB в базе данных')

                    # Если изменил данные существующего абонента
                    else:
                        StaffAction.objects.create(akt_raport=request.GET.get('akt_raport'), user=request.user, comment=f"{request.POST.get('comment')} \n\n Изменение данных абонента {abonent.number} {abonent.etrap} {abonent.name} {abonent.surname} \n\n {mess} \n\n дата изменения {datetime.now()}", action='Изменение данных абонента в MATB в базе данных')
                        

                    messages.success(request, mess)
                # date_ = abonent.addDate
                # context['date_'] = str(date_)

                context['abonent'] = abonent


                if new_intOnDate:
                    context['formatted_intOnDate'] = new_intOnDate
                else:
                    context['formatted_intOnDate'] = None

                if new_intOffDate:
                    context['formatted_intOffDate'] = new_intOffDate
                else:
                    context['formatted_intOffDate'] = None

                # if new_intOffDate:
                #     if abonent.intOnDate:
                #         formatted_intOnDate = abonent.intOnDate.strftime('%Y-%m-%d')
                #         context['formatted_intOnDate'] = formatted_intOnDate
                    

                #     if abonent.intOffDate:
                #         print('ggggggggggggggggggggggggg', abonent.intOffDate, type(abonent.intOffDate))
                #         formatted_intOffDate = new_intOffDate.strftime('%Y-%m-%d')
                #         context['formatted_intOffDate'] = formatted_intOffDate
        except Exception as e:
            messages.error(request, f'Откат сохранения ошибка с transaction == {e}')
            logger.error(f'==== Откат сохранения ошибка с transaction при сохранении == {e}')
    try:
        objs = UserTable.objects.filter(etrap=etrap).exclude(name__exact='', surname__exact='').order_by('-number')[:1000]
        context['objs'] = objs
    except:
        pass

    return render(request, 'telekom/MATB/matbIndex.html', context)
