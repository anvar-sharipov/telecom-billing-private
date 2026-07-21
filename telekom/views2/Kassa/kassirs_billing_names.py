from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.models import ManagerNames
from django.db.models import Q

from telekom.views2.myFunc.myFunc import get_etrap_and_types

def kassirs_billing_names(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.username == 'Gayyp':
            log = 'Dashoguz'
            context['kassaIndex'] = True
            context['kassirs_billing_names'] = True
        else:
            etrap_types = get_etrap_and_types(request.user)
            etraps = etrap_types['etraps']
            log = etraps[0]
            types = etrap_types['types']
            if 'Kassa' in types:
                context['kassaIndex'] = True
                context['kassirs_billing_names'] = True
            else:
                messages.error(request, f'Доступ только соотрудникам кассы')
                return redirect('user-login')
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')
    
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    context['etraps'] = etraps

    etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else log
    name = request.GET.get('name') if request.GET.get('name') != None else ''
    context['etrap'] = etrap
    context['name'] = name
    if etrap != 'all':
        names = ManagerNames.objects.filter(
                Q(etrap__icontains=etrap) &
                Q(name__icontains=name))
    else:
        names = ManagerNames.objects.filter(Q(name__icontains=name))
    context['names'] = names


    if request.method == 'POST' and 'manager_pk' in request.POST:
        manager_pk = request.POST.get('manager_pk')
        new_etrap = request.POST.get('new_etrap')
        if new_etrap:
            manager = ManagerNames.objects.get(pk=manager_pk)
            manager.etrap = new_etrap
            manager.save()
            messages.success(request, f"Успешно сохранено этрап {new_etrap} для кассира {manager.name}")
        else:
            messages.error(request, f"Ошибка! Выберите этрап")
        




    
    return render(request, 'telekom/Kassa/kassirs_billing_names.html', context)