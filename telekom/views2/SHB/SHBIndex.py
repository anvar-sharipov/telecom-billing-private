from django.shortcuts import render, redirect
from django.contrib import messages

from telekom.views2.myFunc.myFunc import get_etrap_and_types, loggedUserEtrapAndGroup

def SHBBolum(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            log = 'Dashoguz'
            context['SHBIndex'] = True
            context['is_allow_to_cahnge_base'] = True
        else:
            etrap_types = get_etrap_and_types(request.user)
            etraps = etrap_types['etraps']
            log = etraps[0]
            types = etrap_types['types']
            if 'SHB' in types:
                context['SHBIndex'] = True
                context['is_allow_to_cahnge_base'] = True
                if 'Gayyp' in request.user.username:
                    context['is_allow_to_cahnge_base'] = False
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
                if '071' in types:
                    context['operator071'] = True
                    # context['Kassa071'] = True 
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')

    return render(request, 'telekom/SHB/SHBIndex.html', context)