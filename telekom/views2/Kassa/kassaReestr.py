from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib import messages
from django.db.models import Sum

from datetime import date
from telekom.models import PayHistory
import datetime

from telekom.views2.myFunc.myFunc import get_etrap_and_types, getLoggedUserEtrap, loggedUserEtrapAndGroup

def kassaReestr(request):
    # EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    # if EtrapAndGroup[1] == 'Kassa' or request.user.is_superuser:
    #     log = EtrapAndGroup[0]
    # else:
    #     messages.error(request, f'Вход в кассу разрешено только соотрудникам кассы')
    #     return redirect('user-login')

  
    context={}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            log = 'Dashoguz'
            context['kassaIndex'] = True
            context['kassa'] = True
            context['allow_to_pay'] = True
        else:
            etrap_types = get_etrap_and_types(request.user)
            etraps = etrap_types['etraps']
            log = etraps[0]
            types = etrap_types['types']
            if 'Kassa' in types:
                context['kassaIndex'] = True
                context['kassaReestr'] = True
            else:
                if 'MTB' in types:
                    context['matbIndex'] = True
                    context['KassaMTB'] = True
                if 'MB' in types:
                    context['setService'] = True
                    context['KassaMB'] = True
                if 'Internet' in types:
                    context['internetBilling'] = True
                    context['KassaInt'] = True
                if 'SHB' in types:
                    context['SHBIndex'] = True
                    context['KassaSHB'] = True
                if '071' in types:
                    context['operator071'] = True
                    context['Kassa071'] = True 
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')

    context['log'] = log

    # log = getLoggedUserEtrap(request.user.username)
    # context['log'] = log
    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date
    context['current_date_time'] = datetime.datetime.now()


    context['kassaIndex'] = True
    context['kassaReestr'] = True

    # kassasObj = PayHistory.objects.all().order_by('kassa')
    # kassas = []
    # for kassa in kassasObj:
    #     if kassa.kassa not in kassas:
    #         kassas.append(kassa.kassa)
    # context['kassas'] = kassas


    kassas = list(PayHistory.objects.order_by('kassa')
            .values_list('kassa', flat=True)
            .distinct())
    context['kassas'] = kassas

    getKassaName = request.GET.get('kassa')
    context['getKassaName'] = getKassaName

    

    start = request.GET.get('start') if request.GET.get('start') != None else current_date
    end = request.GET.get('end') if request.GET.get('end') != None else current_date
    context['start'] = start
    context['end'] = end

    

    pays = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end])
    context['pays'] = pays

    totalNalT = 0
    totalNalS = 0
    totalNalKod = 0
    totalNalZ = 0
    totalNalP = 0
    totalNalD = 0
    totalNalI = 0
    totalNalK = 0
    totalNalA = 0

    totalCardT = 0
    totalCardS = 0
    totalCardKod = 0
    totalCardZ = 0
    totalCardP = 0
    totalCardD = 0
    totalCardI = 0
    totalCardK = 0
    totalCardA = 0

    totalCard = 0
    for p in pays:
        if p.is_card == False:
            totalNalT += p.telefon  
            totalNalS += p.slr  
            totalNalKod += p.kod  
            totalNalZ += p.zakaz  
            totalNalP += p.prochee  
            totalNalD += p.dop_uslugi  
            totalNalI += p.internet
            totalNalK += p.kabel 
            totalNalA += p.alem  
        else:
            totalCardT += p.telefon  
            totalCardS += p.slr  
            totalCardKod += p.kod  
            totalCardZ += p.zakaz  
            totalCardP += p.prochee  
            totalCardD += p.dop_uslugi  
            totalCardI += p.internet
            totalCardK += p.kabel 
            totalCardA += p.alem  

    context['totalNalT'] = totalNalT
    context['totalNalS'] = totalNalS
    context['totalNalKod'] = totalNalKod
    context['totalNalZ'] = totalNalZ
    context['totalNalP'] = totalNalP
    context['totalNalD'] = totalNalD
    context['totalNalI'] = totalNalI
    context['totalNalK'] = totalNalK
    context['totalNalA'] = totalNalA

    context['totalCardT'] = totalCardT
    context['totalCardS'] = totalCardS
    context['totalCardKod'] = totalCardKod
    context['totalCardZ'] = totalCardZ
    context['totalCardP'] = totalCardP
    context['totalCardD'] = totalCardD
    context['totalCardI'] = totalCardI
    context['totalCardK'] = totalCardK
    context['totalCardA'] = totalCardA

    totalNal =  totalNalT + totalNalS +totalNalKod +totalNalZ +totalNalP +totalNalD +totalNalI +totalNalK +totalNalA
    context['totalNal'] = totalNal

    totalCard =  totalCardT + totalCardS +totalCardKod +totalCardZ +totalCardP +totalCardD +totalCardI +totalCardK +totalCardA
    context['totalCard'] = totalCard

    context['umumyTotal'] = totalNal + totalCard



    paysDaNal = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='Dashoguz', is_card=False).order_by('date')
    paysAkNal = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='Akdepe', is_card=False).order_by('date')
    paysGoNal = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='Gorogly', is_card=False).order_by('date')
    paysRuNal = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='Ruhubelent', is_card=False).order_by('date')
    paysNyNal = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='S.A.Nyyazow', is_card=False).order_by('date')
    paysTuNal = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='Turkmenbashy', is_card=False).order_by('date')
    paysBoNal = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='Boldumsaz', is_card=False).order_by('date')
    paysKoNal = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='Koneurgench', is_card=False).order_by('date')

    context['paysDaNal'] = paysDaNal
    context['paysAkNal'] = paysAkNal
    context['paysGoNal'] = paysGoNal
    context['paysRuNal'] = paysRuNal
    context['paysNyNal'] = paysNyNal
    context['paysTuNal'] = paysTuNal
    context['paysBoNal'] = paysBoNal
    context['paysKoNal'] = paysKoNal


    paysDaCard = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='Dashoguz', is_card=True).order_by('date')
    paysAkCard = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='Akdepe', is_card=True).order_by('date')
    paysGoCard = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='Gorogly', is_card=True).order_by('date')
    paysRuCard = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='Ruhubelent', is_card=True).order_by('date')
    paysNyCard = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='S.A.Nyyazow', is_card=True).order_by('date')
    paysTuCard = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='Turkmenbashy', is_card=True).order_by('date')
    paysBoCard = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='Boldumsaz', is_card=True).order_by('date')
    paysKoCard = PayHistory.objects.filter(kassa=getKassaName, date__range=[start, end], abonent__etrap='Koneurgench', is_card=True).order_by('date')

    context['paysDaCard'] = paysDaCard
    context['paysAkCard'] = paysAkCard
    context['paysGoCard'] = paysGoCard
    context['paysRuCard'] = paysRuCard
    context['paysNyCard'] = paysNyCard
    context['paysTuCard'] = paysTuCard
    context['paysBoCard'] = paysBoCard
    context['paysKoCard'] = paysKoCard


    return render(request, 'telekom/Kassa/kassaReestr.html', context)
