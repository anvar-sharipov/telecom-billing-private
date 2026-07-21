
from xmlrpc.client import DateTime
from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.models import NachMinus, OldLoginDogowor, PayHistory, StaffAction, UserTable, UserTableArhiw

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup
from datetime import date

# from django.db.models import Q

# from telekom.models import StaffAction

# from datetime import date

def totalSnyatie(request):
    context = {}
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
        context['log'] = log
        context['matbIndex'] = True
        context['totalSnyatie'] = True
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    current_date = str(date.today())
    context['current_date'] = current_date

    start = request.GET.get('start')
    end = request.GET.get('end')
    context['start'] = start
    context['end'] = end

    objs = UserTable.objects.filter(snyat_bool=True, snyat_date__range=[start, end])

    context['objs'] = objs

    test = UserTable.objects.filter(snyat_bool=True)
    # print('tut objs', test)


    # UserTable.objects.create(number='91456', etrap='Dashoguz')
    # UserTable.objects.create(number='91455', etrap='Dashoguz')


    if request.method == 'POST':
        if request.POST.get('comment') == '':
            messages.error(request, f"Оставьте комментарий")
        else:


            # Сначала Сохраняем OldLoginDogowor
            if objs:
                for abonent in objs:
                    if abonent.login:
                        try:
                            oldLogDog = OldLoginDogowor.objects.get(login=abonent.login.lower())
                            loginEmpty = False
                            if oldLogDog.etrap == abonent.etrap and oldLogDog.number == abonent.number:
                                pass
                            else:
                                messages.error(request, f'Не11 возможно сохранить старый логин {abonent.login} так как этот логин принадлежит абоненту {oldLogDog.number} {oldLogDog.etrap}')
                                return render(request, 'telekom/MATB/totalSnyatie.html', context)

                        except:
                            loginEmpty = True

                        try:
                            oldLogDog = OldLoginDogowor.objects.get(dogowor=abonent.dogowor.upper())
                            dogoworEmpty = False
                            if oldLogDog.etrap == abonent.etrap and oldLogDog.number == abonent.number:
                                pass
                            else:
                                messages.error(request, f'Не возможно сохранить старый договор так как этот договор принадлежит абоненту {oldLogDog.number} {oldLogDog.etrap}')
                                return render(request, 'telekom/MATB/totalSnyatie.html', context)

                        except:
                            dogoworEmpty = True
                        
    

                        if loginEmpty and dogoworEmpty:
                            OldLoginDogowor.objects.create(number=abonent.number, etrap=abonent.etrap, login=abonent.login.lower(), dogowor=abonent.dogowor.upper())
                        else:
                            print(abonent.number, abonent.etrap)
                     
                            updateOldLogDog = OldLoginDogowor.objects.get(number=abonent.number, etrap=abonent.etrap)
                            updateOldLogDog.login = abonent.login.lower()
                            updateOldLogDog.dogowor = abonent.dogowor.upper()
                            updateOldLogDog.save()
                    
                             

                            

                    

            if objs:
                mes = 'Снятие номеров: '
                for abonent in objs:
                    arhiwUser = UserTableArhiw.objects.create(
                    number = abonent.number,
                    etrap = abonent.etrap,
                    surname = abonent.surname,
                    name = abonent.name,
                    street = abonent.street,
                    home = abonent.home,
                    flat = abonent.flat,
                    sotowyy = abonent.sotowyy,
                    is_enterprises = abonent.is_enterprises,
                    alem = abonent.alem,
                    alemCount = abonent.alemCount,
                    alem_connect_date = abonent.alem_connect_date,
                    alem_on_date = abonent.alem_on_date,
                    alem_off_date = abonent.alem_off_date,
                    alem_disconnect_date = abonent.alem_disconnect_date,
                    account = abonent.account,
                    accountName = abonent.accountName,
                    hb = abonent.hb,     
                    internet_tarif = abonent.internet_tarif,
                    internet_connect_date = abonent.internet_connect_date,
                    internet_disconnect_date = abonent.internet_disconnect_date,
                    abonplata = abonent.abonplata,

                    beneficiary = abonent.beneficiary,

                    is_on = abonent.is_on,
                    is_on_date = abonent.is_on_date,
                    kabel_count = abonent.kabel_count,
                    connect_date = abonent.connect_date,
                    kabel_comments = abonent.kabel_comments,
                    ids = abonent.ids,
                    login = abonent.login,
                    dogowor = abonent.dogowor,
                    
                    b_internet = abonent.b_internet,
                    b_kabel = abonent.b_kabel,
                    b_alem = abonent.b_alem,
                    b_telefon = abonent.b_telefon,
                    b_slr = abonent.b_slr,
                    b_kod = abonent.b_kod,
                    b_zakaz = abonent.b_zakaz,
                    b_prochee = abonent.b_prochee,
                    b_dop_uslugi = abonent.b_dop_uslugi,

                    s_internet = abonent.s_internet,
                    s_kabel = abonent.s_kabel,
                    s_alem = abonent.s_alem,
                    s_telefon = abonent.s_telefon,
                    s_slr = abonent.s_slr,
                    s_kod = abonent.s_kod,
                    s_zakaz = abonent.s_zakaz,
                    s_prochee = abonent.s_prochee,
                    s_dop_uslugi = abonent.s_dop_uslugi,
                    
                    addDate = abonent.addDate,
                    snyat_date = abonent.snyat_date,
                    snyat_bool = True
                    )
                    if abonent.service:
                        for i in abonent.service.all():
                            arhiwUser.service.add(i)
                        arhiwUser.save()


                    abonent.surname = ''
                    abonent.name = ''
                    abonent.street = ''
                    abonent.home = ''
                    abonent.flat = ''
                    abonent.sotowyy = ''
                    abonent.is_enterprises = False
                    abonent.alem = False
                    abonent.alemCount = None
                    abonent.alem_connect_date = None
                    abonent.alem_on_date = None
                    abonent.alem_off_date = None
                    abonent.alem_disconnect_date = None
                    abonent.account = None
                    abonent.accountName = ''
                    abonent.hb = None  
                    abonent.internet_tarif = None
                    abonent.internet_connect_date = None
                    abonent.internet_disconnect_date = None
                    abonent.abonplata = ''
                    abonent.is_on = False
                    abonent.is_on_date = None
                    abonent.kabel_count = None
                    abonent.connect_date = None
                    abonent.kabel_comments = None
                    abonent.ids = ''
                    abonent.login = ''
                    abonent.dogowor = ''
                    abonent.addDate = None
                    abonent.snyat_date = None
                    abonent.snyat_bool = False
                    if abonent.service.all():
                        abonent.service.clear()

                    mes += f'"{abonent.number} {abonent.etrap}", '
             

                    abonent.save()
                
                StaffAction.objects.create(comment=f"{request.POST.get('comment')} {mes}", user=request.user, action='Снятие Номера')
         
                messages.success(request, f'Успешное снятие {len(objs)} номеров')
            
            else:
                messages.error(request, "Нет номеров для снятия")



                    



    

    return render(request, 'telekom/MATB/totalSnyatie.html', context)