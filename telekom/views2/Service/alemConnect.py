from django.shortcuts import render, redirect
from django.contrib import messages


from django.db.models import Q

from datetime import date
from datetime import datetime
import re

from telekom.models import AlemCount, InternetTarif, StaffAction, UserTable

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup





def alemConnect(request):
    context = {}
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
        context['setService'] = True
        context['alemConnect'] = True
    else:
        messages.error(request, f'Доступ только соотрудникам MB')
        return redirect('user-login')
    
    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date

    context['log'] = log 
    context['etraps'] = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

    etrap = request.GET.get('etrap')
    try:
        number = re.sub('[-]', '', request.GET.get('number'))
        abonent = UserTable.objects.get(etrap=etrap, number=number)
        context['abonent'] = abonent
        if abonent.alemCount:
            current_tarif_pk = str(abonent.alemCount.pk)
        else:
            current_tarif_pk = ''

        if abonent.alem:
            current_alemOnOff = True
        else:
            current_alemOnOff = False
    except:
        abonent = False


    alems = AlemCount.objects.all().order_by('alem_count')
    context['alems'] = alems

    context['number'] = request.GET.get('number')
    context['etrap'] = etrap

    if abonent:
        staffAction =  StaffAction.objects.filter(Q(action__icontains='Alem TV действия') & Q(comment__icontains=abonent.number) & Q(comment__icontains=abonent.etrap))
        staffActionInfo = staffAction.filter(comment__icontains=abonent.number).order_by('-date')
        context['staffActionInfo'] = staffActionInfo

    if request.method == 'POST':
        print('tut', request.POST.get('alemConnectOrChangedDate'), type(request.POST.get('alemConnectOrChangedDate')))
        if request.POST.get('alemConnectOrChangedDate') == '':
            
            messages.error(request, 'Выберите дату подключения')
        else:

            if abonent:    
                mess= ''
                new_tarif_pk = request.POST.get('tarif_pk')
                if current_tarif_pk != new_tarif_pk:
                    if current_tarif_pk != '' and new_tarif_pk != '':
                        abonent.alemCount = AlemCount.objects.get(pk=new_tarif_pk) 
                        abonent.alem_connect_date = request.POST.get('alemConnectOrChangedDate')
                        mess += f'Смена точек Alem TV c {AlemCount.objects.get(pk=current_tarif_pk).alem_count} на {AlemCount.objects.get(pk=new_tarif_pk).alem_count}'

                        if request.POST.get('alemOnOff') == 'on' and current_alemOnOff == False:
                            mess += ',  Статус Включен'
                            abonent.alem = True
                            abonent.alem_on_date = datetime.now()

                        if request.POST.get('alemOnOff') == None and current_alemOnOff == True:
                            mess += ',  Статус Отключен'
                            abonent.alem = False
                            abonent.alem_off_date = datetime.now()

                    elif current_tarif_pk != '' and new_tarif_pk == '':
                        abonent.alemCount = None
                        abonent.alem = False
                        mess +=  f'Alem TV удален'
                        abonent.alem_connect_date = None
                        abonent.alem_off_date = None
                        abonent.alem_on_date = None
                        abonent.alem_disconnect_date = datetime.now()

                        # if request.POST.get('alemOnOff') == None and current_alemOnOff == True:
                        #     # mess += ',  Статус Отключен'
                        #     abonent.alem = False
                        #     abonent.alem_off_date = datetime.now()

                    elif current_tarif_pk == '' and new_tarif_pk != '':
                        abonent.alemCount = AlemCount.objects.get(pk=new_tarif_pk)
                        mess +=  f'Подключения Alem TV, точек: {AlemCount.objects.get(pk=new_tarif_pk).alem_count}'
                        if request.POST.get('alemConnectOrChangedDate'):
                            abonent.alem_connect_date = request.POST.get('alemConnectOrChangedDate')
                        else:
                            abonent.alem_connect_date = datetime.now()

                        
                        if request.POST.get('alemOnOff'):
                            mess += ',  Статус Включен'
                            abonent.alem = True
                            abonent.alem_on_date = datetime.now()
                        # else:
                        #     messages.error(request, 'Выберите дату')
                        #     return render(request, 'telekom/Service/alemConnect.html', context) 

                else:
                    if request.POST.get('alemOnOff') == 'on' and current_alemOnOff == False:
                        mess += 'Статус Включен'
                        abonent.alem = True
                        abonent.alem_on_date = datetime.now()
                        abonent.alem_off_date = None
                        

                    if request.POST.get('alemOnOff') == None and current_alemOnOff == True:
                        mess += 'Статус Отключен'
                        abonent.alem = False
                        abonent.alem_off_date = datetime.now()
                        abonent.alem_on_date = None
                        

                    if (request.POST.get('alemOnOff') == 'on' and current_alemOnOff == True) or (request.POST.get('alemOnOff') == None and current_alemOnOff == False):
                        mess += f'Изменений Нет'

                if mess != 'Изменений Нет':
                    StaffAction.objects.create(user=request.user, comment=f"{mess}\n\n\nАбонент {abonent.number} {abonent.etrap} {abonent.name} {abonent.surname}\n\nДата и время изменения:\n{datetime.now()}", action='Alem TV действия')
                    messages.success(request, mess)
                    abonent.save()
                else:
                    messages.error(request, 'Изменений нет')


                abonent = UserTable.objects.get(etrap=etrap, number=number)
                context['abonent'] = abonent
            
            else:
                messages.error(request, f'Выберите абонента')

    return render(request, 'telekom/Service/alemConnect.html', context)