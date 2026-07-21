from django.shortcuts import render, redirect
from django.contrib import messages

from django.db.models import Q

from datetime import date
from datetime import datetime
import re

from telekom.models import InternetTarif, StaffAction, UserTable

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup


def internetConnect(request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам MB')
        return redirect('user-login')
    
  

    context = {}
    context['setService'] = True
    context['internetConnect'] = True

    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date

    # log = getLoggedUserEtrap(request.user.username)
    context['log'] = log 
    context['etraps'] = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

    
    
    etrap = request.GET.get('etrap')
    try:
        number = re.sub('[-]', '', request.GET.get('number'))
        abonent = UserTable.objects.get(etrap=etrap, number=number)
        context['abonent'] = abonent
        if abonent.internet_tarif:
            current_tarif_pk = str(abonent.internet_tarif.pk)
        else:
            current_tarif_pk = ''
    except:
        abonent = False

    tarifs = InternetTarif.objects.all().order_by('price')
    context['tarifs'] = tarifs

    context['number'] = request.GET.get('number')
    context['etrap'] = etrap

    if abonent:
        staffAction =  StaffAction.objects.filter(Q(action__icontains='Подключения/смена интернет тарифа') & Q(comment__icontains=abonent.number) & Q(comment__icontains=abonent.etrap))
        staffActionInfo = staffAction.filter(comment__icontains=abonent.number).order_by('-date')
        context['staffActionInfo'] = staffActionInfo

        
    

    


    if request.method == 'POST':

        if abonent:
            new_tarif_pk = request.POST.get('tarif_pk')

            if current_tarif_pk != new_tarif_pk:
                if current_tarif_pk and new_tarif_pk != 'off':
                    abonent.internet_tarif = InternetTarif.objects.get(pk=new_tarif_pk)
                    abonent.internet_connect_date = request.POST.get('internetConnectOrChangedDate')     

                    messages.success(request, f'Смена Интернет тарифа c {InternetTarif.objects.get(pk=current_tarif_pk).tarif} мб/с {InternetTarif.objects.get(pk=current_tarif_pk).price} манат на {InternetTarif.objects.get(pk=new_tarif_pk).tarif} мб/с {InternetTarif.objects.get(pk=new_tarif_pk).price} манат')
                    StaffAction.objects.create(user=request.user, comment=f"Смена интернет тарифа абонента {abonent.number} {abonent.etrap} {abonent.name} {abonent.surname}:\nс\n{InternetTarif.objects.get(pk=current_tarif_pk).tarif}\nна\n{abonent.internet_tarif.tarif}\n\nДата и время смены:\n{datetime.now()}", action='Подключения/смена интернет тарифа')
                elif current_tarif_pk and new_tarif_pk == 'off':
                    abonent.internet_tarif = None
                    abonent.internet_disconnect_date = request.POST.get('internetDisConnectDate') 

                    messages.success(request, f'Отключения интернета') 
                    StaffAction.objects.create(user=request.user, comment=f"Отключения интернета\n\nабонент:\n{abonent.number} {abonent.etrap} {abonent.name} {abonent.surname}:\n\nТариф:\n{InternetTarif.objects.get(pk=current_tarif_pk)}\n\nДата и время отключения:\n{datetime.now()}", action='Подключения/смена интернет тарифа')

                elif current_tarif_pk == '':
                    abonent.internet_tarif = InternetTarif.objects.get(pk=new_tarif_pk)
                    abonent.internet_connect_date = request.POST.get('internetConnectOrChangedDate')  
                    
                    messages.success(request, f'Подключения интернета тариф: {InternetTarif.objects.get(pk=new_tarif_pk).tarif} мб/с {InternetTarif.objects.get(pk=new_tarif_pk).price} манат')
                    StaffAction.objects.create(user=request.user, comment=f"Подключения интернет тарифа абонента {abonent.number} {abonent.etrap} {abonent.name} {abonent.surname}:\n\nТариф:\n{abonent.internet_tarif}\n\nДата и время подключения:\n{datetime.now()}", action='Подключения/смена интернет тарифа')
                abonent.save()
            else:
                messages.success(request, f'Изменений Нет')

            abonent = UserTable.objects.get(etrap=etrap, number=number)
            context['abonent'] = abonent
        
        else:
            messages.error(request, f'Выберите абонента')


    

    
    

    return render(request, 'telekom/Service/internetConnect.html', context)