from django.shortcuts import render, redirect

from telekom.forms import UserLoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate
from django.contrib import messages





def UserLogin(request):
    context = {}
    operators = User.objects.all().order_by('username').exclude(username__in=['admin1','anvar','anvar3','anvar5','MB','mtb',
    'Nurmyrat','shb','subadmin1','test071','testEmpty','testInternet','testInternetDZ','testKassa','testKassaDz',
    'testMTBKone','testSHB','testSHBDZ', 'testKassirDZ', 'testMTBAbonOtdel',
      'testMTBDZ', 'testMTBAbonOtdelKassa'])
    context['operators'] = operators
    
    if request.method == 'POST':

        
        

        user = request.POST.get('operator')
        parol = request.POST.get('parol')
        userAuth = authenticate(request, username=user, password=parol)
        if userAuth is not None:
            login(request, userAuth)
            return redirect('kassa-index')
        else:
            context['userName'] = user
            messages.error(request, f'Ошибка в пароле')


    return render(request, 'telekom/Login/UserLogin.html', context)


def userLogout (request):
    logout(request)
    return redirect('user-login')

  