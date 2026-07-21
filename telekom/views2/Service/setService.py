from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth.models import User

# import re
# from datetime import datetime
# from datetime import date
# from calendar import monthrange

# from django.utils import timezone

# from telekom.forms import InternetTarifForm
# from telekom.models import AbonentService, UserTable, InternetTarif, AbonLength, StaffAction, AbonentNumbersCount, AbonentBeneficiary, KabelCount, NachMinus
# from telekom.views2.myFunc.myFunc import appendHistoryDict, createServiceDict, createServiceType, getAbonNachOrNone, dictHaveServiceType, loggedUserEtrapAndGroup

def setService(request):
    # if request.user.username[:7] == 'service' or request.user.username[:-1] == 'admin':
    # EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    # if EtrapAndGroup[1] == 'MB' or request.user.is_superuser:
    #     log = EtrapAndGroup[0]
    # else:
    #     messages.error(request, f'Доступ только соотрудникам Абон-отдела')
    #     return redirect('user-login')
    
    context = {}
    # current_date = date.today()
    # current_date = str(current_date)
    # context['current_date'] = current_date
    # current_year = current_date[0:4]
    # current_month = current_date[5:7]
    # current_day = current_date[8:]
    # days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]


    # # log = getLoggedUserEtrap(request.user.username)
    
    # context['setService'] = True
    # context['set_service'] = True
    # context['connectService'] = True
    # context['log'] = log 
    # context['etraps'] = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

    # # если нажал на поиск абонента POST1
    # if request.method == 'POST' and 'number' in request.POST:
    #     number = re.sub('[-]', '', request.POST.get('number'))
    #     context['number'] = request.POST.get('number')
    #     context['etrap'] = request.POST.get('etrap')
    #     context['services'] = AbonentService.objects.all()


    #     try:
    #         abonent = UserTable.objects.get(number=number, etrap=request.POST.get('etrap'))
    #         active_service = []
    #         for service in abonent.service.all():
    #             active_service.append(service.pk)
    #         context['active_service'] = active_service

    #         if abonent.name == '' and abonent.surname == '':
    #             messages.error(request, f'Свободный номер')
    #             context['abonent'] = abonent
    #         else:
    #             context['abonent'] = abonent
    #             form = InternetTarifForm(instance=abonent)
    #             context['form'] = form
    #     except:
    #         messages.error(request, f'Направильно набранный номер')
                    
    # # если нажал на сохранить абонента POST2
    # if request.method == 'POST' and 'number' not in request.POST:
    #     number = re.sub('[-]', '', request.POST.get('service_number'))
    #     context['etrap'] = request.POST.get('etrap')
    #     context['services'] = AbonentService.objects.all()


    #     abonent = UserTable.objects.get(number=number, etrap=request.POST.get('etrap'))

    #     active_service = []
    #     for service in abonent.service.all():
    #             active_service.append(str(service.pk))
    #     context['active_service'] = active_service



    #     form = InternetTarifForm(instance=abonent)

    #     context['form'] = form

    #     context['abonent'] = abonent
    #     context['number'] = request.POST.get('service_number')

    #     if abonent.internet_tarif:
    #         current_internet_tarif_pk = str(abonent.internet_tarif.pk)
    #     else:
    #         current_internet_tarif_pk = ''

        # if request.POST.get('comment') != '':
        #     count_of_changes = []
        #     # internet_tarif
        #     if request.POST.get('internet_tarif') != current_internet_tarif_pk:
        #         if request.POST.get('internet_tarif'):
        #             abonent.internet_tarif = InternetTarif.objects.get(pk=request.POST.get('internet_tarif'))
        #             nach = (int(days_in_month) - int(current_day)) * (abonent.internet_tarif.price / days_in_month)
        #             abonent.b_internet -= nach
        #             if current_internet_tarif_pk == '':
        #                 ConnectOrChangeInternetTarif.objects.create(abonent=abonent, whoChange=request.user.username, action='подключения итернета', changeFrom='', changeTo=f"{abonent.internet_tarif}")
        #                 count_of_changes.append('Поключения Интернета')
        #                 StaffAction.objects.create(user=request.user, comment=f"Подключения интернет тарифа абонента {abonent.number} {abonent.etrap} {abonent.name} {abonent.surname}:\n\nТариф:\n{abonent.internet_tarif}\n\nДата и время подключения:\n{datetime.now()}\n\nЦена начисления: {'%.2f' % nach} manat", action='Подключения/смена интернет тарифа')
        #             else:
        #                 count_of_changes.append('Смена Интернет тарифа')
        #                 ConnectOrChangeInternetTarif.objects.create(abonent=abonent, whoChange=request.user.username, action='смена интернет тарифа', changeFrom=f"{InternetTarif.objects.get(pk=current_internet_tarif_pk)}", changeTo=f"{abonent.internet_tarif}")
        #                 StaffAction.objects.create(user=request.user, comment=f"Смена интернет тарифа абонента {abonent.number} {abonent.etrap} {abonent.name} {abonent.surname}:\nс\n{InternetTarif.objects.get(pk=current_internet_tarif_pk)}\nна\n{abonent.internet_tarif}\n\nДата и время смены:\n{datetime.now()}\n\nЦена начисления: {'%.2f' % nach} manat", action='Подключения/смена интернет тарифа')
        #             try:
        #                 nachMinus = NachMinus.objects.get(user=abonent, year=current_year, month=current_month)
        #                 nachMinus.internet += nach
        #                 nachMinus.save()
        #             except:
        #                 NachMinus.objects.create(user=abonent, year=current_year, month=current_month, internet=nach)
        #         else:
        #             abonent.internet_tarif = None
        #             count_of_changes.append('Отключения Интернета')
        #             ConnectOrChangeInternetTarif.objects.create(abonent=abonent, whoChange=request.user.username, action='отключения итернета', changeFrom=f"{InternetTarif.objects.get(pk=current_internet_tarif_pk)}", changeTo=f"")
        #             StaffAction.objects.create(user=request.user, comment=f"Отключения интернета\n\nабонент:\n{abonent.number} {abonent.etrap} {abonent.name} {abonent.surname}:\n\nТариф:\n{InternetTarif.objects.get(pk=current_internet_tarif_pk)}\n\nДата и время отключения:\n{datetime.now()}", action='Подключения/смена интернет тарифа')

            
        #     abonent.save()
        #     messages.success(request, f'{count_of_changes[0]}')
        #     abonent = UserTable.objects.get(number=number, etrap=request.POST.get('etrap'))
        #     form = InternetTarifForm(instance=abonent)
        #     context['form'] = form
            


        #     nach = getAbonNachOrNone(abonent.pk)
                

        #     # abon_length ############################################################
        #     #############################################################           vv

        #     # Если abon_length нет и надо подключить
        #     if abonent.abon_length == None and request.POST.get('abon_length'):
        #         abonent.abon_length = AbonLength.objects.get(pk=request.POST.get('abon_length'))
        #         abonent.abon_length_connect_date = datetime.now()
        #         abonent.abon_length_disconnected_date = None
                

        #     # Если abon_length есть и есть новая услуга  
        #     elif abonent.abon_length != None and request.POST.get('abon_length'):

        #         # Если abon_length нужно заменить
        #         if str(abonent.abon_length.pk) != request.POST.get('abon_length'):

        #             # Если старая услуга подключена в этом месяце (денег берем не с первого числа) 
        #             if str(abonent.abon_length_connect_date)[5:7] == current_date[5:7]:
        #                 pay = (abonent.abon_length.price / days_in_month) * (int(current_date[8:10]) - int(str(abonent.abon_length_connect_date)[8:10]))
        #             else:
        #                 pay = (abonent.abon_length.price / days_in_month) * int(current_date[8:10])
                    
        #             # Если у абонента за этот месяц этого года уже создан начисления 
        #             if nach:
        #                 nach.dop_uslugi += pay

        #                 # Если есть история отключений услуг (dict_)
        #                 if nach.service_history:
        #                     dict_ = eval(nach.service_history)

        #                     # Если dict_ содержит текущую услугу
        #                     if dictHaveServiceType(dict_, 'abon_length'):
        #                         dictionary = appendHistoryDict(dict_, abonent, 'abon_length', 'Смена Тарифа', pay)
        #                     else:
        #                         dictionary = createServiceType(dict_, abonent, 'abon_length', 'Смена Тарифа', pay)

        #                 else:
        #                     dictionary = createServiceDict(abonent, 'abon_length', 'Смена Тарифа', pay)
                        
        #                 nach.service_history = str(dictionary)
        #             else:
        #                 dictionary = createServiceDict(abonent, 'abon_length', 'Смена Тарифа', pay)
        #                 nach = NachMinus.objects.create(user=abonent, year=current_year, month=current_month, dop_uslugi = pay, service_history=str(dictionary))
        #             saveServiceDaysAutoNachReport(abonent, pay, 'метры')
        #             abonent.abon_length = AbonLength.objects.get(pk=request.POST.get('abon_length'))
        #             abonent.b_dop_uslugi -= pay
        #             abonent.abon_length_connect_date = datetime.now()
        #             abonent.abon_length_disconnected_date = None
                    
        #     # Если надо отключить abon_length
        #     elif abonent.abon_length != None and request.POST.get('abon_length') == '':
        #        # проверяем установлена ли услуга в этом месяце
        #         if str(abonent.abon_length_connect_date)[5:7] == current_date[5:7]:
        #             pay = (int(current_date[8:10]) - int(str(abonent.abon_length_connect_date)[8:10])) * (abonent.abon_length.price / days_in_month)
        #         else:
        #             pay = (abonent.abon_length.price / days_in_month) * current_date[8:10]
        #         if nach:
        #             nach.dop_uslugi += pay
        #             if nach.service_history:
        #                 dict_ = eval(nach.service_history)
        #                 if dictHaveServiceType(dict_, 'abon_length'):
        #                     dictionary = appendHistoryDict(dict_, abonent, 'abon_length', 'Отключения услуги', pay)
        #                 else:
        #                     dictionary = createServiceType(dict_, abonent, 'abon_length', 'Отключения услуги', pay)

        #             else:
        #                 dictionary = createServiceDict(abonent, 'abon_length', 'Отключения услуги', pay)
                    
        #             nach.service_history = str(dictionary)
        #         else:
        #             dictionary = createServiceDict(abonent, 'abon_length', 'Отключения услуги', pay)
        #             nach = NachMinus.objects.create(user=abonent, year=current_year, month=current_month, dop_uslugi = pay, service_history=str(dictionary))
        #         saveServiceDaysAutoNachReport(abonent, pay, 'метры')
        #         abonent.b_dop_uslugi -= pay
        #         abonent.abon_length = None
        #         abonent.abon_length_connect_date = None
        #         abonent.abon_length_disconnected_date = datetime.now()

        #     # end abon_length ###########################################           ^^
        #     ##########################################################################


        #     # count_of_numbers #######################################################
        #     #############################################################           vv

        #     if abonent.count_of_numbers == None and request.POST.get('count_of_numbers'):
        #         abonent.count_of_numbers = AbonentNumbersCount.objects.get(pk=request.POST.get('count_of_numbers'))
        #         abonent.count_of_numbers_connect_date = datetime.now()
        #         abonent.count_of_numbers_disconnected_date = None

        #     elif abonent.count_of_numbers != None and request.POST.get('count_of_numbers'):

        #         if str(abonent.count_of_numbers.pk) != request.POST.get('count_of_numbers'):
        #             if str(abonent.count_of_numbers_connect_date)[5:7] == current_date[5:7]:
        #                 pay = (abonent.count_of_numbers.price / days_in_month) * (int(current_date[8:10]) - int(str(abonent.count_of_numbers_connect_date)[8:10]))
        #             else:
        #                 pay = (abonent.count_of_numbers.price / days_in_month) * int(current_date[8:10])
                    
        #             if abonent.beneficiary:
        #                 pay = pay - (pay * float('0.' + str(abonent.beneficiary.percent))) 

        #             if nach:
        #                 nach.telefon += pay

        #                 if nach.service_history:
        #                     dict_ = eval(nach.service_history)

        #                     if dictHaveServiceType(dict_, 'count_of_numbers'):
        #                         dictionary = appendHistoryDict(dict_, abonent, 'count_of_numbers', 'Смена Тарифа', pay)
        #                     else:
        #                         dictionary = createServiceType(dict_, abonent, 'count_of_numbers', 'Смена Тарифа', pay)

        #                 else:
        #                     dictionary = createServiceDict(abonent, 'count_of_numbers', 'Смена Тарифа', pay)
                        
        #                 nach.service_history = str(dictionary)

        #             else:
        #                 dictionary = createServiceDict(abonent, 'count_of_numbers', 'Смена Тарифа', pay)
        #                 nach = NachMinus.objects.create(user=abonent, year=current_year, month=current_month, telefon = pay, service_history=str(dictionary))
        #             saveServiceDaysAutoNachReport(abonent, pay, 'Кол-во номеров')
        #             abonent.count_of_numbers = AbonentNumbersCount.objects.get(pk=request.POST.get('count_of_numbers'))
        #             abonent.b_telefon -= pay
        #             abonent.count_of_numbers_connect_date = datetime.now()
        #             abonent.count_of_numbers_disconnected_date = None
                    
        #     elif abonent.count_of_numbers != None and request.POST.get('count_of_numbers') == '':

        #         if str(abonent.count_of_numbers_connect_date)[5:7] == current_date[5:7]:
        #             pay = (int(current_date[8:10]) - int(str(abonent.count_of_numbers_connect_date)[8:10])) * (abonent.count_of_numbers.price / days_in_month)
        #         else:
        #             pay = (abonent.count_of_numbers.price / days_in_month) * current_date[8:10]

        #         if nach:
        #             nach.telefon += pay

        #             if nach.service_history:
        #                 dict_ = eval(nach.service_history)

        #                 if dictHaveServiceType(dict_, 'count_of_numbers'):
        #                     dictionary = appendHistoryDict(dict_, abonent, 'count_of_numbers', 'Отключения услуги', pay)
        #                 else:
        #                     dictionary = createServiceType(dict_, abonent, 'count_of_numbers', 'Отключения услуги', pay)

        #             else:
        #                 dictionary = createServiceDict(abonent, 'count_of_numbers', 'Отключения услуги', pay)
                    
        #             nach.service_history = str(dictionary)
        #         else:
        #             dictionary = createServiceDict(abonent, 'count_of_numbers', 'Отключения услуги', pay)
        #             nach = NachMinus.objects.create(user=abonent, year=current_year, month=current_month, telefon = pay, service_history=str(dictionary))
        #         saveServiceDaysAutoNachReport(abonent, pay, 'Кол-во номеров')
        #         abonent.b_telefon -= pay
        #         abonent.count_of_numbers = None
        #         abonent.count_of_numbers_connect_date = None
        #         abonent.count_of_numbers_disconnected_date = datetime.now()

        #     # end count_of_numbers ######################################           ^^
        #     ##########################################################################
            
            
        #     if request.POST.get('beneficiary'):
        #         abonent.beneficiary = AbonentBeneficiary.objects.get(pk=request.POST.get('beneficiary'))
        #     else:
        #         abonent.beneficiary = None


        #     # kabel_count ############################################################
        #     #############################################################           vv

        #     if request.POST.get('kabel_connected'):
        #         abonent.kabel_connected = True
        #         abonent.kabel_connected_date = datetime.now()
        #         abonent.kabel_disconnected_date = None
        #     else:
        #         abonent.kabel_connected = False
        #         abonent.kabel_connected_date = None
        #         abonent.kabel_disconnected_date = datetime.now()

        #     if abonent.kabel_count == None and request.POST.get('kabel_count'):
        #         abonent.kabel_count = KabelCount.objects.get(pk=request.POST.get('kabel_count'))

        #         abonent.kabel_connected = True
        #         abonent.kabel_activated_date = datetime.now()
        #         abonent.kabel_deactivated_date = None

        #         if abonent.kabel_disconnected_date:
        #             abonent.kabel_connected_date = datetime.now()

        #     elif abonent.kabel_count != None and request.POST.get('kabel_count'):

        #         if abonent.kabel_disconnected_date:
        #             abonent.kabel_connected = True
        #             abonent.kabel_connected_date = datetime.now()

        #         if str(abonent.kabel_count.pk) != request.POST.get('kabel_count'):
        #             if str(abonent.kabel_activated_date)[5:7] == current_date[5:7]:
        #                 pay = (abonent.kabel_count.price / days_in_month) * (int(current_date[8:10]) - int(str(abonent.kabel_activated_date)[8:10]))
        #             else:
        #                 pay = (abonent.kabel_count.price / days_in_month) * int(current_date[8:10])

        #             if nach:
        #                 nach.kabel += pay

        #                 if nach.service_history:
        #                     dict_ = eval(nach.service_history)

        #                     if dictHaveServiceType(dict_, 'kabel_count'):
        #                         dictionary = appendHistoryDict(dict_, abonent, 'kabel_count', 'Смена Тарифа', pay)
        #                     else:
        #                         dictionary = createServiceType(dict_, abonent, 'kabel_count', 'Смена Тарифа', pay)

        #                 else:
        #                     dictionary = createServiceDict(abonent, 'kabel_count', 'Смена Тарифа', pay)
                        
        #                 nach.service_history = str(dictionary)

        #             else:
        #                 dictionary = createServiceDict(abonent, 'kabel_count', 'Смена Тарифа', pay)
        #                 nach = NachMinus.objects.create(user=abonent, year=current_year, month=current_month, kabel = pay, service_history=str(dictionary))
        #             saveServiceDaysAutoNachReport(abonent, pay, 'Кол-во Кабель TV')
        #             abonent.kabel_count = KabelCount.objects.get(pk=request.POST.get('kabel_count'))
        #             abonent.b_kabel -= pay
        #             abonent.kabel_activated_date = datetime.now()
        #             abonent.kabel_deactivated_date = None
                    
        #     elif abonent.kabel_count != None and request.POST.get('kabel_count') == '':

        #         abonent.kabel_connected = False
        #         abonent.kabel_connected_date = None
        #         abonent.kabel_disconnected_date = datetime.now()

        #         if str(abonent.kabel_activated_date)[5:7] == current_date[5:7]:
        #             pay = (int(current_date[8:10]) - int(str(abonent.kabel_activated_date)[8:10])) * (abonent.kabel_count.price / days_in_month)
        #         else:
        #             pay = (abonent.kabel_count.price / days_in_month) * current_date[8:10]

        #         if nach:
        #             nach.kabel += pay

        #             if nach.service_history:
        #                 dict_ = eval(nach.service_history)

        #                 if dictHaveServiceType(dict_, 'kabel_count'):
        #                     dictionary = appendHistoryDict(dict_, abonent, 'kabel_count', 'Отключения услуги', pay)
        #                 else:
        #                     dictionary = createServiceType(dict_, abonent, 'kabel_count', 'Отключения услуги', pay)

        #             else:
        #                 dictionary = createServiceDict(abonent, 'kabel_count', 'Отключения услуги', pay)
                    
        #             nach.service_history = str(dictionary)
        #         else:
        #             dictionary = createServiceDict(abonent, 'kabel_count', 'Отключения услуги', pay)
        #             nach = NachMinus.objects.create(user=abonent, year=current_year, month=current_month, kabel = pay, service_history=str(dictionary))
        #         saveServiceDaysAutoNachReport(abonent, pay, 'Кол-во Кабель TV')
        #         abonent.b_kabel -= pay
        #         abonent.kabel_count = None
        #         abonent.kabel_activated_date = None
        #         abonent.kabel_deactivated_date = datetime.now()

        #     # end kabel_count ###########################################           ^^
        #     ##########################################################################


        #     # alem
        #     if abonent.alem == False and request.POST.get('alem'):
        #         abonent.alem = True
        #         abonent.alem_connect_date = datetime.now()
        #         abonent.alem_disconnect_date = None
        #     if abonent.alem == True and request.POST.get('alem') == None:
        #         if str(abonent.alem_connect_date)[:7] == current_date[:7]:
        #             pay = (int(current_date[8:10]) - int(str(abonent.alem_connect_date)[8:10])) * (50 / days_in_month)
        #         else:
        #             pay = (50 / days_in_month) * int(current_date[8:10])
        #         saveServiceDaysAutoNachReport(abonent, pay, 'Alem TV')
        #         abonent.alem = False
        #         abonent.alem_connect_date = None
        #         abonent.alem_disconnect_date = datetime.now()
        #         if nach:
        #             nach.alem += pay
        #         else:
        #             nach = NachMinus.objects.create(user=abonent, year=current_year, month=current_month, alem = pay)
        #         abonent.b_alem -= pay


        #     # service
        #     new_serv = []
        #     for service in  AbonentService.objects.all():
        #         if request.POST.get(service.service):
        #             new_serv.append(request.POST.get(service.service))

        #     add_serv = []
        #     del_serv = []

        #     for new in new_serv:
        #         if new not in active_service:
        #             add_serv.append(new)

        #     for old in active_service:
        #         if old not in new_serv:
        #             del_serv.append(old)

        #     # нет изменений
        #     if add_serv == [] and del_serv == []:
        #         # Ничего не делаем
        #         pass

        #     # добавлена услуга  
        #     if add_serv != [] and del_serv == []:
        #         # добавляем услугу
        #         pass

        #     # удалена услуга  
        #     if add_serv == [] and del_serv != []:
        #         # сохраняем для начисления
        #         # начисляем
        #         # удаляем услугу
        #         pass

        #     # и добавлена и удалена услуга  
        #     if add_serv == [] and del_serv != []:
        #         # добавляем услугу
        #         # удаляем услугу

        #         # сохраняем для начисления
        #         # начисляем
        #         # удаляем услугу
        #         pass
            


                    




        #     StaffAction.objects.create(user=request.user, comment=request.POST.get('comment'), action='Update')

        #     messages.success(request, f'Изменения сохранены')

        #     abonent.save()

        #     if nach:
        #         nach.save()

        #     abonent = UserTable.objects.get(number=number, etrap=request.POST.get('etrap'))
        #     form = InternetTarifForm(instance=abonent)
        #     context['form'] = form

        # else:

        #     form = InternetTarifForm(request.POST)
        #     context['form'] = form
        #     messages.error(request, f'Запишите комментарий')
    
    return render(request, 'telekom/Service/setService.html', context)
