from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
# Объединение несколюко queryset
# https://sky.pro/media/kak-obedinit-neskolko-queryset-v-django/
from itertools import chain


from django.contrib.auth.models import Group


from datetime import date
import datetime

from telekom.models import InterpayBilling, PayHistory, UserTable
from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup


def internetBolum(request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'Internet' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Вход Только для соотрудников интернет отдела')
        return redirect('user-login')
  
    
    context = {}
    current_date = date.today()
    current_date = str(current_date)
    context['internetBilling'] = True
    context['payBilling'] = True
    context['current_date'] = current_date

    start = request.GET.get('start') if request.GET.get('start') != None else current_date
    end = request.GET.get('end') if request.GET.get('end') != None else current_date
    context['start'] = start
    context['end'] = end

    users = User.objects.all()

    

    dzKassirs = []
    akKassirs = []
    gorKassirs = []
    ruhKassirs = []
    nyyazKassirs = []
    turKassirs = []
    bolKassirs = []
    koneKassirs = []

    for user in Group.objects.get(name="Dashoguz_Kassa").user_set.all():
        if user.username not in dzKassirs:
            dzKassirs.append(user.username)
    for user in Group.objects.get(name="Akdepe_Kassa").user_set.all():
        if user.username not in akKassirs:
            akKassirs.append(user.username)
    for user in Group.objects.get(name="Gorogly_Kassa").user_set.all():
        if user.username not in gorKassirs:
            gorKassirs.append(user.username)
    for user in Group.objects.get(name="Ruhubelent_Kassa").user_set.all():
        if user.username not in ruhKassirs:
            ruhKassirs.append(user.username)
    for user in Group.objects.get(name="S.A.Nyyazow_Kassa").user_set.all():
        if user.username not in nyyazKassirs:
            nyyazKassirs.append(user.username)
    for user in Group.objects.get(name="Turkmenbashy_Kassa").user_set.all():
        if user.username not in turKassirs:
            turKassirs.append(user.username)
    for user in Group.objects.get(name="Boldumsaz_Kassa").user_set.all():
        if user.username not in bolKassirs:
            bolKassirs.append(user.username)
    for user in Group.objects.get(name="Koneurgench_Kassa").user_set.all():
        if user.username not in koneKassirs:
            koneKassirs.append(user.username)
    context['dzKassirs'] = dzKassirs
    context['akKassirs'] = akKassirs
    context['gorKassirs'] = gorKassirs
    context['ruhKassirs'] = ruhKassirs
    context['nyyazKassirs'] = nyyazKassirs
    context['turKassirs'] = turKassirs
    context['bolKassirs'] = bolKassirs
    context['koneKassirs'] = koneKassirs


    # for user in Group.objects.get(name="Dashoguz_Kassa").user_set.all():
    #     if user.username not in kassirs:
    #         kassirs.append(user.username)
    # for user in Group.objects.get(name="Akdepe_Kassa").user_set.all():
    #     if user.username not in kassirs:
    #         kassirs.append(user.username)
    # for user in Group.objects.get(name="Gorogly_Kassa").user_set.all():
    #     if user.username not in kassirs:
    #         kassirs.append(user.username)
    # for user in Group.objects.get(name="Ruhubelent_Kassa").user_set.all():
    #     if user.username not in kassirs:
    #         kassirs.append(user.username)
    # for user in Group.objects.get(name="S.A.Nyyazow_Kassa").user_set.all():
    #     if user.username not in kassirs:
    #         kassirs.append(user.username)
    # for user in Group.objects.get(name="Turkmenbashy_Kassa").user_set.all():
    #     if user.username not in kassirs:
    #         kassirs.append(user.username)
    # for user in Group.objects.get(name="Boldumsaz_Kassa").user_set.all():
    #     if user.username not in kassirs:
    #         kassirs.append(user.username)
    # for user in Group.objects.get(name="Koneurgench_Kassa").user_set.all():
    #     if user.username not in kassirs:
    #         kassirs.append(user.username)
    # context['kassirs'] = kassirs


    checkedKassirsGet = []
    noneCheckeKassirs = []

    

    for kassir in dzKassirs:
        if request.GET.get(kassir) != 'on':
            noneCheckeKassirs.append(kassir)
        else:
            checkedKassirsGet.append(kassir)

    for kassir in akKassirs:
        if request.GET.get(kassir) != 'on':
            noneCheckeKassirs.append(kassir)
        else:
            checkedKassirsGet.append(kassir)

    for kassir in gorKassirs:
        if request.GET.get(kassir) != 'on':
            noneCheckeKassirs.append(kassir)
        else:
            checkedKassirsGet.append(kassir)

    for kassir in ruhKassirs:
        if request.GET.get(kassir) != 'on':
            noneCheckeKassirs.append(kassir)
        else:
            checkedKassirsGet.append(kassir)

    for kassir in nyyazKassirs:
        if request.GET.get(kassir) != 'on':
            noneCheckeKassirs.append(kassir)
        else:
            checkedKassirsGet.append(kassir)

    for kassir in turKassirs:
        if request.GET.get(kassir) != 'on':
            noneCheckeKassirs.append(kassir)
        else:
            checkedKassirsGet.append(kassir)

    for kassir in bolKassirs:
        if request.GET.get(kassir) != 'on':
            noneCheckeKassirs.append(kassir)
        else:
            checkedKassirsGet.append(kassir)

    for kassir in koneKassirs:
        if request.GET.get(kassir) != 'on':
            noneCheckeKassirs.append(kassir)
        else:
            checkedKassirsGet.append(kassir)

    context['noneCheckeKassirs'] = noneCheckeKassirs
    context['checkedKassirsGet'] = checkedKassirsGet


    context['log'] = log


    # checkedKassirsGet = []
    # noneCheckeKassirs = []
    # for kassir in kassirs:
    #     if request.GET.get(kassir) != 'on':
    #         noneCheckeKassirs.append(kassir)
    #     else:
    #         checkedKassirsGet.append(kassir)
    # context['noneCheckeKassirs'] = noneCheckeKassirs
    # context['checkedKassirsGet'] = checkedKassirsGet
    # print(noneCheckeKassirs)



    if noneCheckeKassirs == []:
        messages.error(request, f'Вы не можете выбрать всех кассиров')
        return render(request, 'telekom/InternetBilling/internetBolum.html', context)

    count = 0
    for kassir in noneCheckeKassirs:
        count += 1
        if count == 1:
            objs = InterpayBilling.objects.filter(pay_history__date__range=[start, end]).exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 2:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 3:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 4:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 5:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 6:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 7:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 8:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 9:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 10:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 11:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 12:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 13:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 14:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 15:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 16:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 17:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 18:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 19:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 20:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 21:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 22:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 23:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 24:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 25:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 26:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 27:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 28:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 29:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        if count == 30:
            objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        

    
    context['objs'] = objs




    
    # Если нажал на сохранить
    if request.method == 'POST':
        print('tut')
        # берем id всех True чекбоксов
        telBoxes = request.POST.getlist('telefonCheckBox')
        intBoxes = request.POST.getlist('internetCheckBox')
        alemBoxes = request.POST.getlist('alemCheckBox')

        start = request.POST.get('start')
        end = request.POST.get('end')

        context['start'] = start
        context['end'] = end

        # Если есть True-шные чекбоксы Абонплат 
        if telBoxes:
            # Проходимся циклом по этим True-шным чекбоксам
            for x in telBoxes:
                obj = InterpayBilling.objects.get(pk=str(x))
                # Если был False то делаем True
                if obj.is_checked_telefon == False:
                    obj.is_checked_telefon = True
                    # Если все платежи успешно начислились то сохраняем дату начисления и логин оператора который осуществил начисления
                    abonplata = obj.pay_history.telefon + obj.pay_history.slr + obj.pay_history.kod + obj.pay_history.zakaz + obj.pay_history.prochee + obj.pay_history.dop_uslugi
                    if abonplata != 0 and obj.is_checked_telefon == False or obj.pay_history.alem != 0 and obj.is_checked_alem == False or obj.pay_history.internet != 0 and obj.is_checked_internet == False:
                        pass
                    else:
                        obj.billing_date_total = datetime.datetime.now()
                        obj.operator = request.user
                    obj.save()

        if intBoxes:
            for x in intBoxes:
                obj = InterpayBilling.objects.get(pk=str(x))
                if obj.is_checked_internet == False:
                    obj.is_checked_internet = True

                    abonplata = obj.pay_history.telefon + obj.pay_history.slr + obj.pay_history.kod + obj.pay_history.zakaz + obj.pay_history.prochee + obj.pay_history.dop_uslugi
                    if abonplata != 0 and obj.is_checked_telefon == False or obj.pay_history.alem != 0 and obj.is_checked_alem == False or obj.pay_history.internet != 0 and obj.is_checked_internet == False:
                        pass
                    else:
                        obj.billing_date_total = datetime.datetime.now()
                        obj.operator = request.user
                    obj.save()


        if alemBoxes:
            for x in alemBoxes:
                obj = InterpayBilling.objects.get(pk=str(x))
                if obj.is_checked_alem == False:
                    obj.is_checked_alem = True  

                    abonplata = obj.pay_history.telefon + obj.pay_history.slr + obj.pay_history.kod + obj.pay_history.zakaz + obj.pay_history.prochee + obj.pay_history.dop_uslugi
                    if abonplata != 0 and obj.is_checked_telefon == False or obj.pay_history.alem != 0 and obj.is_checked_alem == False or obj.pay_history.internet != 0 and obj.is_checked_internet == False:
                        pass
                    else:
                        obj.billing_date_total = datetime.datetime.now()
                        obj.operator = request.user
                    obj.save()

      
        # Обновления данных
        noneCheckeKassirs = []
        checkedKassirsPost = []
        for kassir in dzKassirs:
            if request.GET.get(kassir) != 'on':
                noneCheckeKassirs.append(kassir)
            else:
                checkedKassirsGet.append(kassir)

        for kassir in akKassirs:
            if request.GET.get(kassir) != 'on':
                noneCheckeKassirs.append(kassir)
            else:
                checkedKassirsGet.append(kassir)
        
        for kassir in gorKassirs:
            if request.GET.get(kassir) != 'on':
                noneCheckeKassirs.append(kassir)
            else:
                checkedKassirsGet.append(kassir)

        for kassir in ruhKassirs:
            if request.GET.get(kassir) != 'on':
                noneCheckeKassirs.append(kassir)
            else:
                checkedKassirsGet.append(kassir)

        for kassir in nyyazKassirs:
            if request.GET.get(kassir) != 'on':
                noneCheckeKassirs.append(kassir)
            else:
                checkedKassirsGet.append(kassir)

        for kassir in turKassirs:
            if request.GET.get(kassir) != 'on':
                noneCheckeKassirs.append(kassir)
            else:
                checkedKassirsGet.append(kassir)

        for kassir in bolKassirs:
            if request.GET.get(kassir) != 'on':
                noneCheckeKassirs.append(kassir)
            else:
                checkedKassirsGet.append(kassir)

        for kassir in koneKassirs:
            if request.GET.get(kassir) != 'on':
                noneCheckeKassirs.append(kassir)
            else:
                checkedKassirsGet.append(kassir)
        
        context['noneCheckeKassirs'] = noneCheckeKassirs
        context['checkedKassirsPost'] = checkedKassirsPost

      
        # # Обновления данных
        # noneCheckeKassirs = []
        # checkedKassirsPost = []
        # for kassir in kassirs:  
        #     if request.POST.get(kassir):
        #         checkedKassirsPost.append(kassir)
        #     else:
        #         noneCheckeKassirs.append(kassir)
        # context['noneCheckeKassirs'] = noneCheckeKassirs
        # context['checkedKassirsPost'] = checkedKassirsPost

        count = 0
        for kassir in noneCheckeKassirs:
            count += 1
            if count == 1:
                objs = InterpayBilling.objects.filter(pay_history__date__range=[start, end]).exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 2:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 3:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 4:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 5:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 6:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 7:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 8:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 9:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 10:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 11:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 12:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 13:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 14:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 15:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 16:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 17:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 18:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 19:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 20:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 21:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 22:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 23:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 24:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 25:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 26:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 27:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 28:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 29:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
            if count == 30:
                objs = objs.exclude(pay_history__kassir=kassir).order_by('-pay_history__date')
        

    
        context['objs'] = objs

    return render(request, 'telekom/InternetBilling/internetBolum.html', context)
