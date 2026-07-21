from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group

from datetime import date
import datetime
from telekom.models import InterpayPerekidkaBilling, UserTable

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup


def interpayPerekidka(request):
    context = {}
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'Internet' or request.user.is_superuser:
        log = EtrapAndGroup[0]
        print(log)
        context['log'] = log
        context['internetBilling'] = True
        context['interpayPerekidka'] = True
    else:
        messages.error(request, f'Вход Только для соотрудников интернет отдела')
        return redirect('user-login')
    
    current_date = str(date.today())
    context['current_date'] = current_date
    

    start = request.GET.get('start') if request.GET.get('start') != None else current_date
    end = request.GET.get('end') if request.GET.get('end') != None else current_date
    context['start'] = start
    context['end'] = end


    # etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

    totalCheckedNameList = []
    ####### Для Dashoguz #######
    dzGroup = Group.objects.get(name="Dashoguz_MTB").user_set.all()
    dzUsers = []
    checkedDz = []
    for user in dzGroup:
        dzUsers.append(user)
        if request.GET.get(str(user.pk)) == 'on':
            checkedDz.append(user.pk)
            totalCheckedNameList.append(user.username)
    if len(checkedDz) != 0:
        context['checkedDz'] = checkedDz
    else:
        context['checkedDz'] = None
    context['dzUsers'] = dzUsers

    ####### Для Akdepe #######
    akGroup = Group.objects.get(name="Akdepe_MTB").user_set.all()
    akUsers = []
    checkedAk = []
    for user in akGroup:
        akUsers.append(user)
        if request.GET.get(str(user.pk)) == 'on':
            checkedAk.append(user.pk)
            totalCheckedNameList.append(user.username)
    if len(checkedAk) != 0:
        context['checkedAk'] = checkedAk
    else:
        context['checkedAk'] = None
    context['akUsers'] = akUsers

    ####### Для Gorogly #######
    gorGroup = Group.objects.get(name="Gorogly_MTB").user_set.all()
    gorUsers = []
    checkedGor = []
    for user in gorGroup:
        gorUsers.append(user)
        if request.GET.get(str(user.pk)) == 'on':
            checkedGor.append(user.pk)
            totalCheckedNameList.append(user.username)
    if len(checkedGor) != 0:
        context['checkedGor'] = checkedGor
    else:
        context['checkedGor'] = None
    context['gorUsers'] = gorUsers

    ####### Для Ruhubelent #######
    ruhGroup = Group.objects.get(name="Ruhubelent_MTB").user_set.all()
    ruhUsers = []
    checkedRuh = []
    for user in ruhGroup:
        ruhUsers.append(user)
        if request.GET.get(str(user.pk)) == 'on':
            checkedRuh.append(user.pk)
            totalCheckedNameList.append(user.username)
    if len(checkedRuh) != 0:
        context['checkedRuh'] = checkedRuh
    else:
        context['checkedRuh'] = None
    context['ruhUsers'] = ruhUsers

    ####### Для S.A.Nyyazow #######
    nyGroup = Group.objects.get(name="S.A.Nyyazow_MTB").user_set.all()
    nyUsers = []
    checkedNy = []
    for user in nyGroup:
        nyUsers.append(user)
        if request.GET.get(str(user.pk)) == 'on':
            checkedNy.append(user.pk)
            totalCheckedNameList.append(user.username)
    if len(checkedNy) != 0:
        context['checkedNy'] = checkedNy
    else:
        context['checkedNy'] = None
    context['nyUsers'] = nyUsers

    ####### Для Turkmenbashy #######
    tuGroup = Group.objects.get(name="Turkmenbashy_MTB").user_set.all()
    tuUsers = []
    checkedTu = []
    for user in tuGroup:
        tuUsers.append(user)
        if request.GET.get(str(user.pk)) == 'on':
            checkedTu.append(user.pk)
            totalCheckedNameList.append(user.username)
    if len(checkedTu) != 0:
        context['checkedTu'] = checkedTu
    else:
        context['checkedTu'] = None
    context['tuUsers'] = tuUsers

    ####### Для Boldumsaz #######
    bolGroup = Group.objects.get(name="Boldumsaz_MTB").user_set.all()
    bolUsers = []
    checkedBol = []
    for user in bolGroup:
        bolUsers.append(user)
        if request.GET.get(str(user.pk)) == 'on':
            checkedBol.append(user.pk)
            totalCheckedNameList.append(user.username)
    if len(checkedBol) != 0:
        context['checkedBol'] = checkedBol
    else:
        context['checkedBol'] = None
    context['bolUsers'] = bolUsers

    ####### Для Koneurgench #######
    koGroup = Group.objects.get(name="Koneurgench_MTB").user_set.all()
    koUsers = []
    checkedKo = []
    for user in koGroup:
        koUsers.append(user)
        if request.GET.get(str(user.pk)) == 'on':
            checkedKo.append(user.pk)
            totalCheckedNameList.append(user.username)
    if len(checkedKo) != 0:
        context['checkedKo'] = checkedKo
    else:
        context['checkedKo'] = None
    context['koUsers'] = koUsers



    objs = InterpayPerekidkaBilling.objects.filter(date__range=[start, end], mtbUsername__in=totalCheckedNameList)
    context['objs'] = objs.order_by('-date')

    if request.method == 'POST':
        abonplata1 = request.POST.getlist('abonplata1')
        abonplata2 = request.POST.getlist('abonplata2')

        internet1 = request.POST.getlist('internet1')
        internet2 = request.POST.getlist('internet2')

        alem1 = request.POST.getlist('alem1')
        alem2 = request.POST.getlist('alem2')

        for i in abonplata1:
            obj = InterpayPerekidkaBilling.objects.get(pk=i)
            obj.is_checked_abonplata1 = True
            if obj.operator == '' or obj.operator == None:
                obj.operator = request.user.username
                obj.perekidka_date = datetime.datetime.now()
            obj.save()

        for i in abonplata2:
            obj = InterpayPerekidkaBilling.objects.get(pk=i)
            obj.is_checked_abonplata2 = True
            if obj.operator == '' or obj.operator == None:
                obj.operator = request.user.username
                obj.perekidka_date = datetime.datetime.now()
            obj.save()

        for i in internet1:
            obj = InterpayPerekidkaBilling.objects.get(pk=i)
            obj.is_checked_internet1 = True
            if obj.operator == '' or obj.operator == None:
                obj.operator = request.user.username
                obj.perekidka_date = datetime.datetime.now()
            obj.save()
        
        for i in internet2:
            obj = InterpayPerekidkaBilling.objects.get(pk=i)
            obj.is_checked_internet2 = True
            if obj.operator == '' or obj.operator == None:
                obj.operator = request.user.username
                obj.perekidka_date = datetime.datetime.now()
            obj.save()

        for i in alem1:
            obj = InterpayPerekidkaBilling.objects.get(pk=i)
            obj.is_checked_alem1 = True
            if obj.operator == '' or obj.operator == None:
                obj.operator = request.user.username
                obj.perekidka_date = datetime.datetime.now()
            obj.save()
            

        for i in alem2:
            obj = InterpayPerekidkaBilling.objects.get(pk=i)
            obj.is_checked_alem2 = True
            if obj.operator == '' or obj.operator == None:
                obj.operator = request.user.username
                obj.perekidka_date = datetime.datetime.now()
            obj.save()



        


        print(abonplata1, abonplata2, internet1, internet2, alem1, alem2)


    return render(request, 'telekom/InternetBilling/interpayPerekidka.html', context)
