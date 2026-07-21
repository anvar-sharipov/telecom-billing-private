from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum

# https://metanit.com/python/django/5.5.php
# Для update
from django.db.models import F

from telekom.models import DontRepeatYourself, ImportInternetNachisleniyaOFF, ImportInternetNachisleniyaON, NachMinus, NachisleniyaOtchet, OldLoginDogowor, StaffAction, UserTable

from telekom.views2.myFunc.myFunc import getEtrapCode, loggedUserEtrapAndGroup, monthСonvert
from django.db import transaction

import logging

logger = logging.getLogger(__name__)


def internetNachisleniyaBtn(request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    context = {}
    context['matbIndex'] = True
    context['internetNachisleniyaBtn'] = True

    

    # log = getLoggedUserEtrap(request.user.username)
    context['log'] = log
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    context['etraps'] = etraps
    
    context['etrap'] = request.GET.get('etrap')
    context['get_month'] = request.GET.get('month')
    context['get_year'] = request.GET.get('year')
    off = "True" if request.GET.get('off') != None else "False"



    month_word = request.GET.get('month')
    year = request.GET.get('year')
    month_numb = monthСonvert(month_word)
    etrap = request.GET.get('etrap')
    context['off'] = 'True' if request.GET.get('off') != None else 'False'

    if month_word == '':
        messages.error(request, f'Ошибка! Выберите месяц начисления')
        return redirect('internet-nachisleniya-btn')


    
    
    
    if month_word and year and etrap:
    
        if request.GET.get('off') == None:
            if etrap in etraps:
                internetNachisleniya = ImportInternetNachisleniyaON.objects.filter(month=month_word, year=year, etrap=etrap)

                # Проверяем было ли начисление этого QuerySet (для отключения кнопки начислить)
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}ON")
                    context['alreadyNach'] = True
                except:
                    try:
                        DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allON")
                        context['alreadyNach'] = True
                    except:
                        context['alreadyNach'] = False


            elif etrap == 'all':
                internetNachisleniya = ImportInternetNachisleniyaON.objects.filter(month=month_word, year=year)
                # Были ли частичные начисления (другие этрапы)
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allON")
                    context['alreadyNach'] = True
                except:
                    pass
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzON")
                    Dashoguz = 'Dashoguz'
                except:
                    Dashoguz = ''
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeON")
                    Akdepe = 'Akdepe'
                except:
                    Akdepe = ''
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazON")
                    Boldumsaz = 'Boldumsaz'
                except:
                    Boldumsaz = ''
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyON")
                    Gorogly = 'Gorogly'
                except:
                    Gorogly = ''
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchON")
                    Koneurgench = 'Koneurgench'
                except:
                    Koneurgench = ''
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyON")
                    Turkmenbashy = 'Turkmenbashy'
                except:
                    Turkmenbashy = ''
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowON")
                    Nyyazow = 'Nyyazow'
                except:
                    Nyyazow = ''
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentON")
                    Ruhubelent = 'Ruhubelent'
                except:
                    Ruhubelent = ''

                if Dashoguz and Akdepe and Boldumsaz and Gorogly and Koneurgench and Turkmenbashy and Nyyazow and Ruhubelent:
                    context['alreadyallNach'] = True
                elif Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
                    context['alreadySeparateNach'] = True


        elif request.GET.get('off') == 'on':
            if etrap in etraps:
                internetNachisleniya = ImportInternetNachisleniyaOFF.objects.filter(month=month_word, year=year, etrap=etrap)
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}OFF")
                    context['alreadyNach'] = True
                except:
                    try:
                        DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allOFF")
                        context['alreadyNach'] = True
                    except:
                        context['alreadyNach'] = False
            elif etrap == 'all':
                internetNachisleniya = ImportInternetNachisleniyaOFF.objects.filter(month=month_word, year=year)

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allOFF")
                    context['alreadyNach'] = True
                except:
                    pass

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzOFF")
                    Dashoguz = 'Dashoguz'
                except:
                    Dashoguz = ''
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeOFF")
                    Akdepe = 'Akdepe'
                except:
                    Akdepe = ''
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazOFF")
                    Boldumsaz = 'Boldumsaz'
                except:
                    Boldumsaz = ''
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyOFF")
                    Gorogly = 'Gorogly'
                except:
                    Gorogly = ''
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchOFF")
                    Koneurgench = 'Koneurgench'
                except:
                    Koneurgench = ''
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyOFF")
                    Turkmenbashy = 'Turkmenbashy'
                except:
                    Turkmenbashy = ''
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowOFF")
                    Nyyazow = 'Nyyazow'
                except:
                    Nyyazow = ''
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentOFF")
                    Ruhubelent = 'Ruhubelent'
                except:
                    Ruhubelent = ''
                if Dashoguz and Akdepe and Boldumsaz and Gorogly and Koneurgench and Turkmenbashy and Nyyazow and Ruhubelent:
                    context['alreadyallNach'] = True
                elif Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
                    context['alreadySeparateNach'] = True

        if len(internetNachisleniya) == 0:
            context['nothingNach'] = True

        context['totalPayCount'] = len(internetNachisleniya)
        context['totalPayPrice'] = internetNachisleniya.aggregate(Sum('price'))['price__sum']

        
        if etrap == 'all':
            dogoworLogin = UserTable.objects.values('dogowor', 'login')
        elif etrap in etraps:
            dogoworLogin = UserTable.objects.filter(etrap=etrap).values('dogowor', 'login')


        ###
        oldLoginDogowor = OldLoginDogowor.objects.all()
        # {Dashoguz: {number: [login, login]}, Akdepe: {number: [login, login]}, ...}
        # {login: [etrap, number]}
        old_logins = {}
        old_dogowors = {}

        # old_logins = []
        # old_dogowors = []

        for logDog in oldLoginDogowor:
            if logDog.login:
                old_logins[logDog.login] = [logDog.etrap, logDog.number]
            if logDog.dogowor:
                old_dogowors[logDog.dogowor] = [logDog.etrap, logDog.number]


        ####

        dogowors = []
        logins = []

        for item_ in dogoworLogin:
            for col, val in item_.items():
                if col == 'dogowor' and val != '':
                    dogowors.append(item_['dogowor'])
                elif col == 'login' and val != '':
                    logins.append(item_['login'])

        dogoworSuccess = 0
        dogoworSuccessPrice = 0

        loginSuccess = 0
        loginSuccessPrice = 0

        ###
        oldDogoworSuccess = 0
        oldDogoworSuccessPrice = 0

        oldLoginSuccess = 0
        oldLoginSuccessPrice = 0
        ####

        error = 0
        errorPrice = 0
        ###
        for nach in internetNachisleniya:
            if nach.dogowor in dogowors:
                dogoworSuccess += 1
                dogoworSuccessPrice += nach.price
                continue
            elif nach.login in logins:
                loginSuccess += 1
                loginSuccessPrice += nach.price
                continue
            elif nach.dogowor in old_dogowors:
                oldDogoworSuccess += 1
                oldDogoworSuccessPrice += nach.price
                continue
            elif nach.login in old_logins:
                oldLoginSuccess += 1
                oldLoginSuccessPrice += nach.price
                continue
            else:
                # print('errorcccccccccccc', nach)
                print('EEEEEEE', nach)
                error += 1
                errorPrice += nach.price
        ####


        context['dogoworSuccess'] = dogoworSuccess
        context['dogoworSuccessPrice'] = dogoworSuccessPrice

        context['loginSuccess'] = loginSuccess
        context['loginSuccessPrice'] = loginSuccessPrice

        ##№
        context['oldLoginSuccess'] = oldLoginSuccess
        context['oldLoginSuccessPrice'] = oldLoginSuccessPrice
        context['oldDogoworSuccess'] = oldDogoworSuccess
        context['oldDogoworSuccessPrice'] = oldDogoworSuccessPrice
        ###№

        context['error'] = error
        context['errorPrice'] = errorPrice

    poDogoworuCount = 0
    poDogoworuPrice = 0
    poLoginCount = 0
    poLoginPrice = 0

    poOldDogoworuCount = 0
    poOldDogoworuPrice = 0
    poOldLoginCount = 0
    poOldLoginPrice = 0

    # Если нажал на начислить
    if request.method == 'POST' and 'comment' in request.POST:
        if etrap != 'all':
            if off == 'False':
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allON")
                    messages.error(request, f'Ошибка за месяц {month_word} {year} года интернет начислений ON было сделано на все Этрапы')
                    return redirect(request.POST.get('url_from'))
                except:
                    pass
            else:
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allOFF")
                    messages.error(request, f'Ошибка за месяц {month_word} {year} года интернет начислений OFF было сделано на все Этрапы')
                    return redirect(request.POST.get('url_from'))
                except:
                    pass
        else:
            if off == 'False':
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzON")
                    Dashoguz = 'Dashoguz'
                except:
                    Dashoguz = ''

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeON")
                    Akdepe = 'Akdepe'
                except:
                    Akdepe = ''

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazON")
                    Boldumsaz = 'Boldumsaz'
                except:
                    Boldumsaz = ''

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyON")
                    Gorogly = 'Gorogly'
                except:
                    Gorogly = ''

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchON")
                    Koneurgench = 'Koneurgench'
                except:
                    Koneurgench = ''

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyON")
                    Turkmenbashy = 'Turkmenbashy'
                except:
                    Turkmenbashy = ''

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowON")
                    Nyyazow = 'Nyyazow'
                except:
                    Nyyazow = ''

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentON")
                    Ruhubelent = 'Ruhubelent'
                except:
                    Ruhubelent = ''

                if Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
                    messages.error(request, f'Ошибка за месяц {month_word} {year} Вы не можете начислить ON на все этрапы так как некоторые этрапы уже были начислены ({Dashoguz} {Akdepe} {Boldumsaz} {Gorogly} {Koneurgench} {Turkmenbashy} {Nyyazow} {Ruhubelent})')
                    return redirect(request.POST.get('url_from'))
            
        
            else:
                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzOFF")
                    Dashoguz = 'Dashoguz'
                except:
                    Dashoguz = ''

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeOFF")
                    Akdepe = 'Akdepe'
                except:
                    Akdepe = ''

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazOFF")
                    Boldumsaz = 'Boldumsaz'
                except:
                    Boldumsaz = ''

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyOFF")
                    Gorogly = 'Gorogly'
                except:
                    Gorogly = ''

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchOFF")
                    Koneurgench = 'Koneurgench'
                except:
                    Koneurgench = ''

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyOFF")
                    Turkmenbashy = 'Turkmenbashy'
                except:
                    Turkmenbashy = ''

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowOFF")
                    Nyyazow = 'Nyyazow'
                except:
                    Nyyazow = ''

                try:
                    DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentOFF")
                    Ruhubelent = 'Ruhubelent'
                except:
                    Ruhubelent = ''

                if Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
                    messages.error(request, f'Ошибка за месяц {month_word} {year} Вы не можете начислить OFF на все этрапы так как некоторые этрапы уже были начислены ({Dashoguz} {Akdepe} {Boldumsaz} {Gorogly} {Koneurgench} {Turkmenbashy} {Nyyazow} {Ruhubelent})')
                    return redirect(request.POST.get('url_from'))
                
        try:
            if off == 'False':
                DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}ON")
                messages.error(request, f'Ошибка за месяц {month_word} {year} года {etrap} интернет начисления ON уже начислено')
                return redirect(request.POST.get('url_from'))  
            else:
                DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}OFF")
                messages.error(request, f'Ошибка за месяц {month_word} {year} года {etrap} интернет начисления OFF уже начислено')
                return redirect(request.POST.get('url_from'))  
        except:
            pass

        if request.POST.get('comment') == '':
            messages.error(request, f'Комментарий не может быть пустым')  
            return redirect(request.POST.get('url_from'))
        else:
            if internetNachisleniya == {}:
                messages.error(request, f'Ошибка! за месяц {month_word} {year} года нет ни одного начислений для начисления')
                return redirect(request.POST.get('url_from'))
        
        
        
        if etrap == 'all':
            code = None
            users = UserTable.objects.all()
            nachMinus = NachMinus.objects.filter(year=year, month=month_numb)
        else:
            code = getEtrapCode(etrap)
            users = UserTable.objects.filter(etrap=request.GET.get('etrap'))
            nachMinus = NachMinus.objects.filter(year=year, month=month_numb, user__etrap=request.GET.get('etrap'))


        # Сохранения начислений с договором
        userDogoworPk = {}
        for user in users:
            if user.dogowor != '':
                userDogoworPk[user.dogowor] = user.pk

        nachDogoworPrice = {}
        
        for n in internetNachisleniya:
            if n.dogowor not in nachDogoworPrice:
                nachDogoworPrice[n.dogowor] = n.price
            else:
                nachDogoworPrice[n.dogowor] += n.price
        
        DBNachDogoworPK = {}
        for n in nachMinus:
            DBNachDogoworPK[n.user.dogowor] = n.pk
        
        list_bulk_create = []
        succes = 0
        try:
            with transaction.atomic():
                for dogowor, price in nachDogoworPrice.items():
                    if dogowor in userDogoworPk:
                        user = UserTable.objects.get(pk=userDogoworPk[dogowor])
                        poDogoworuCount += 1
                        poDogoworuPrice += price
                        print('Начислений по договору', poDogoworuCount)
                        user.b_internet -= price

                        if dogowor not in DBNachDogoworPK:
                            list_bulk_create.append([user, month_numb, year, price])
                        else:
                            newNachMinus = NachMinus.objects.get(pk=DBNachDogoworPK[dogowor])
                            newNachMinus.internet += price
                            newNachMinus.save()
                    
                        user.save()
                        succes += 1

                        # Если выбрано 'all' (все этрапы)
                        if etrap == 'all':
                            try:
                                nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=user.etrap, year=year, month=month_word)
                                nachisleniyaOtchet.intetnetNachisleniya += price
                                nachisleniyaOtchet.save()
                            except:
                                NachisleniyaOtchet.objects.create(etrap=user.etrap, year=year, month=month_word, intetnetNachisleniya = price)

                if list_bulk_create:
                    aux=[]
                    for item in list_bulk_create:
                        obj = NachMinus(user=item[0], month=item[1], year=item[2], internet=item[3])
                        aux.append(obj)
                    NachMinus.objects.bulk_create(aux)


                # Сохранения начислений с логином
                userLoginPk = {}
                for user in users:
                    if user.login:
                        userLoginPk[user.login] = user.pk

                

                nachLoginPrice = {}

                for n in internetNachisleniya:
                    if n.login not in nachLoginPrice and n.dogowor not in dogowors:
                        nachLoginPrice[n.login] = n.price
                    elif n.login in nachLoginPrice and n.dogowor not in dogowors:
                        nachLoginPrice[n.login] += n.price
                

                DBNachLoginPK = {}
                for n in nachMinus:
                    if n.user.login:
                        DBNachLoginPK[n.user.login] = n.pk


                list_bulk_create = []
                succes2 = 0
                for login, price in nachLoginPrice.items():
                    if login in userLoginPk:

                        user = UserTable.objects.get(pk=userLoginPk[login])
                        poLoginCount += 1
                        poLoginPrice += price
                        print('Начислений по логину', poLoginCount)
                        user.b_internet -= price

                        if login not in DBNachLoginPK:
                            list_bulk_create.append([user, month_numb, year, price])
                        else:
                            newNachMinus = NachMinus.objects.get(pk=DBNachLoginPK[login])
                            newNachMinus.internet += price
                            newNachMinus.save()
                        user.save()
                        succes2 += 1

                        # Если выбрано 'all' (все этрапы)
                        if etrap == 'all':
                            try:
                                nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=user.etrap, year=year, month=month_word)
                                nachisleniyaOtchet.intetnetNachisleniya += price
                                nachisleniyaOtchet.save()
                            except:
                                NachisleniyaOtchet.objects.create(etrap=user.etrap, year=year, month=month_word, intetnetNachisleniya = price)
                if list_bulk_create:
                    aux=[]
                    for item in list_bulk_create:
                        obj = NachMinus(user=item[0], month=item[1], year=item[2], internet=item[3])
                        aux.append(obj)
                    NachMinus.objects.bulk_create(aux)

                ###
                # начисляем Login, Dogowor начисления которые нет в UserTable (по причине изменения), но есть в OldLoginDogowor
                for n in internetNachisleniya:
                    if n.login not in logins and n.dogowor not in dogowors:
                        if n.login in old_logins:
                            
                            # print(n.logins, old_logins[n.login])
                            print(n.login)
                            old_login_user = UserTable.objects.get(etrap=old_logins[n.login][0], number=old_logins[n.login][1])
                            old_login_user.b_internet -= n.price
                            poOldLoginCount += 1
                            poOldLoginPrice += n.price
                            print('Начислений по old логину', poOldLoginCount)
                            old_login_user.save()


                            try:
                                old_login_nachMinus = NachMinus.objects.get(user=old_login_user, year=year, month=month_numb)
                                old_login_nachMinus.internet += n.price
                                old_login_nachMinus.save()
                            except:
                                NachMinus.objects.create(user=old_login_user, year=year, month=month_numb, internet=n.price)

                            try:
                                nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=old_logins[n.login][0], year=year, month=month_word)
                                nachisleniyaOtchet.intetnetNachisleniya += n.price
                                nachisleniyaOtchet.save()
                            except:
                                NachisleniyaOtchet.objects.create(etrap=old_logins[n.login][0], year=year, month=month_word, intetnetNachisleniya=n.price)

                        elif n.dogowor in old_dogowors:
                            old_dogowor_user = UserTable.objects.get(etrap=old_dogowors[n.dogowor][0], number=old_dogowors[n.dogowor][1])
                            old_dogowor_user.b_internet -= n.price
                            poOldDogoworuCount += 1
                            poOldDogoworuPrice += n.price
                            print('Начислений по old договору', poOldDogoworuCount)
                            old_dogowor_user.save()


                            try:
                                old_dogowor_nachMinus = NachMinus.objects.get(user=old_dogowor_user, year=year, month=month_numb)
                                old_dogowor_nachMinus.internet += n.price
                                old_dogowor_nachMinus.save()
                            except:
                                NachMinus.objects.create(user=old_dogowor_user, year=year, month=month_numb, internet=n.price)

                            try:
                                nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=old_dogowors[n.dogowor][0], year=year, month=month_word)
                                nachisleniyaOtchet.intetnetNachisleniya += n.price
                                nachisleniyaOtchet.save()
                            except:
                                NachisleniyaOtchet.objects.create(etrap=old_dogowors[n.dogowor][0], year=year, month=month_word, intetnetNachisleniya=n.price)
                    
                ####


                # Сохранение инфы о начисленном месяце и того кто начисли и т.п.
                if off == 'False':
                    DontRepeatYourself.objects.create(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}ON")  
                else:
                    DontRepeatYourself.objects.create(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}OFF")

                if off == 'False':
                    StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')} \n\n Интернет Начисления ON за месяц {month_word} {year} года для этрапа {etrap}", action='Начисления Интернет')  
                else:
                    StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')} \n\n Интернет Начисления OFF за месяц {month_word} {year} года для этрапа {etrap}", action='Начисления Интернет')  

                if off == 'False':
                    messages.success(request, f'Успешное Интернет начисления ON для {etrap} за месяц {month_word} {year} года')
                else:
                    messages.success(request, f'Успешное Интернет начисления OFF для {etrap} - за месяц {month_word} {year} года')  
                    

                print('Начислено по договору абонентов',poDogoworuCount)
                print('Начислено по договору Цена',poDogoworuPrice)
                print('Начислено по логину абонентов',poLoginCount)
                print('Начислено по логину цена',poLoginPrice)
                print('Начислено по old договору абонентов',poOldDogoworuCount)
                print('Начислено по old договору цена',poOldDogoworuPrice)
                print('Начислено по old логину абонентов',poOldLoginCount)
                print('Начислено по old логину цена',poOldLoginPrice)
                # ##################################################
                # Сохраняем сумму начисления для месячного отчета ##
                #  #################################################
                if etrap in etraps:
                    try:
                        NachisleniyaOtchet.objects.get(year=year, month=month_word, etrap=etrap)
                        NachisleniyaOtchet.objects.filter(year=year, month=month_word, etrap=etrap).update(
                        intetnetNachisleniya=F('intetnetNachisleniya') + (dogoworSuccessPrice + loginSuccessPrice))
                    except:
                        NachisleniyaOtchet.objects.create(
                            etrap=etrap,
                            year=year, 
                            month=month_word, 
                            intetnetNachisleniya= (dogoworSuccessPrice + loginSuccessPrice))

                # ######################################################
                # Сохраняем сумму начисления для месячного отчета END ##
                #  #####################################################
              
                UserTable.objects.filter(is_enterprises=True).update(b_telefon=0, b_slr=0, b_kod=0, b_zakaz=0, b_prochee=0, b_dop_uslugi=0, b_internet=0, b_alem=0)
        except Exception as e:
            logger.warning(f"Ошибка (Откат)! {str(e)}")
            messages.error(request, f'Ошибка (Откат)! {str(e)}')

    return render(request, 'telekom/MATB/xlsx/XlsxNachisleniya/internetNachisleniyaBtn.html', context)


# rabotaet no bez razdelennymi etrapami
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.db.models import Sum

# # https://metanit.com/python/django/5.5.php
# # Для update
# from django.db.models import F

# from telekom.models import DontRepeatYourself, ImportInternetNachisleniyaOFF, ImportInternetNachisleniyaON, NachMinus, NachisleniyaOtchet, OldLoginDogowor, StaffAction, UserTable

# from telekom.views2.myFunc.myFunc import getEtrapCode, loggedUserEtrapAndGroup, monthСonvert
# from django.db import transaction

# import logging

# logger = logging.getLogger(__name__)


# def internetNachisleniyaBtn(request):
#     EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
#     if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
#         log = EtrapAndGroup[0]
#     else:
#         messages.error(request, f'Доступ только соотрудникам MATB')
#         return redirect('user-login')
    
#     context = {}
#     context['matbIndex'] = True
#     context['internetNachisleniyaBtn'] = True

    

#     # log = getLoggedUserEtrap(request.user.username)
#     context['log'] = log
#     context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
#     context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']
#     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
#     context['etraps'] = etraps
    
#     context['etrap'] = request.GET.get('etrap')
#     context['get_month'] = request.GET.get('month')
#     context['get_year'] = request.GET.get('year')
#     off = "True" if request.GET.get('off') != None else "False"



#     month_word = request.GET.get('month')
#     year = request.GET.get('year')
#     month_numb = monthСonvert(month_word)
#     etrap = request.GET.get('etrap')
#     context['off'] = 'True' if request.GET.get('off') != None else 'False'

#     if month_word == '':
#         messages.error(request, f'Ошибка! Выберите месяц начисления')
#         return redirect('internet-nachisleniya-btn')


    
    
    
#     if month_word and year and etrap:
    
#         if request.GET.get('off') == None:
#             if etrap in etraps:
#                 internetNachisleniya = ImportInternetNachisleniyaON.objects.filter(month=month_word, year=year, etrap=etrap)

#                 # Проверяем было ли начисление этого QuerySet (для отключения кнопки начислить)
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}ON")
#                     context['alreadyNach'] = True
#                 except:
#                     try:
#                         DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allON")
#                         context['alreadyNach'] = True
#                     except:
#                         context['alreadyNach'] = False


#             elif etrap == 'all':
#                 internetNachisleniya = ImportInternetNachisleniyaON.objects.filter(month=month_word, year=year)
#                 # Были ли частичные начисления (другие этрапы)
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allON")
#                     context['alreadyNach'] = True
#                 except:
#                     pass
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzON")
#                     Dashoguz = 'Dashoguz'
#                 except:
#                     Dashoguz = ''
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeON")
#                     Akdepe = 'Akdepe'
#                 except:
#                     Akdepe = ''
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazON")
#                     Boldumsaz = 'Boldumsaz'
#                 except:
#                     Boldumsaz = ''
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyON")
#                     Gorogly = 'Gorogly'
#                 except:
#                     Gorogly = ''
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchON")
#                     Koneurgench = 'Koneurgench'
#                 except:
#                     Koneurgench = ''
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyON")
#                     Turkmenbashy = 'Turkmenbashy'
#                 except:
#                     Turkmenbashy = ''
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowON")
#                     Nyyazow = 'Nyyazow'
#                 except:
#                     Nyyazow = ''
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentON")
#                     Ruhubelent = 'Ruhubelent'
#                 except:
#                     Ruhubelent = ''

#                 if Dashoguz and Akdepe and Boldumsaz and Gorogly and Koneurgench and Turkmenbashy and Nyyazow and Ruhubelent:
#                     context['alreadyallNach'] = True
#                 elif Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
#                     context['alreadySeparateNach'] = True


#         elif request.GET.get('off') == 'on':
#             if etrap in etraps:
#                 internetNachisleniya = ImportInternetNachisleniyaOFF.objects.filter(month=month_word, year=year, etrap=etrap)
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}OFF")
#                     context['alreadyNach'] = True
#                 except:
#                     try:
#                         DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allOFF")
#                         context['alreadyNach'] = True
#                     except:
#                         context['alreadyNach'] = False
#             elif etrap == 'all':
#                 internetNachisleniya = ImportInternetNachisleniyaOFF.objects.filter(month=month_word, year=year)

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allOFF")
#                     context['alreadyNach'] = True
#                 except:
#                     pass

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzOFF")
#                     Dashoguz = 'Dashoguz'
#                 except:
#                     Dashoguz = ''
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeOFF")
#                     Akdepe = 'Akdepe'
#                 except:
#                     Akdepe = ''
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazOFF")
#                     Boldumsaz = 'Boldumsaz'
#                 except:
#                     Boldumsaz = ''
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyOFF")
#                     Gorogly = 'Gorogly'
#                 except:
#                     Gorogly = ''
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchOFF")
#                     Koneurgench = 'Koneurgench'
#                 except:
#                     Koneurgench = ''
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyOFF")
#                     Turkmenbashy = 'Turkmenbashy'
#                 except:
#                     Turkmenbashy = ''
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowOFF")
#                     Nyyazow = 'Nyyazow'
#                 except:
#                     Nyyazow = ''
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentOFF")
#                     Ruhubelent = 'Ruhubelent'
#                 except:
#                     Ruhubelent = ''
#                 if Dashoguz and Akdepe and Boldumsaz and Gorogly and Koneurgench and Turkmenbashy and Nyyazow and Ruhubelent:
#                     context['alreadyallNach'] = True
#                 elif Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
#                     context['alreadySeparateNach'] = True

#         if len(internetNachisleniya) == 0:
#             context['nothingNach'] = True

#         context['totalPayCount'] = len(internetNachisleniya)
#         context['totalPayPrice'] = internetNachisleniya.aggregate(Sum('price'))['price__sum']

        
#         if etrap == 'all':
#             dogoworLogin = UserTable.objects.values('dogowor', 'login')
#         elif etrap in etraps:
#             dogoworLogin = UserTable.objects.filter(etrap=etrap).values('dogowor', 'login')


#         ###
#         oldLoginDogowor = OldLoginDogowor.objects.all()
#         # {Dashoguz: {number: [login, login]}, Akdepe: {number: [login, login]}, ...}
#         # {login: [etrap, number]}
#         old_logins = {}
#         old_dogowors = {}

#         # old_logins = []
#         # old_dogowors = []

#         for logDog in oldLoginDogowor:
#             if logDog.login:
#                 old_logins[logDog.login] = [logDog.etrap, logDog.number]
#             if logDog.dogowor:
#                 old_dogowors[logDog.dogowor] = [logDog.etrap, logDog.number]


#         ####

#         dogowors = []
#         logins = []

#         for item_ in dogoworLogin:
#             for col, val in item_.items():
#                 if col == 'dogowor' and val != '':
#                     dogowors.append(item_['dogowor'])
#                 elif col == 'login' and val != '':
#                     logins.append(item_['login'])

#         dogoworSuccess = 0
#         dogoworSuccessPrice = 0

#         loginSuccess = 0
#         loginSuccessPrice = 0

#         ###
#         oldDogoworSuccess = 0
#         oldDogoworSuccessPrice = 0

#         oldLoginSuccess = 0
#         oldLoginSuccessPrice = 0
#         ####

#         error = 0
#         errorPrice = 0
#         ###
#         for nach in internetNachisleniya:
#             if nach.dogowor in dogowors:
#                 dogoworSuccess += 1
#                 dogoworSuccessPrice += nach.price
#                 continue
#             elif nach.login in logins:
#                 loginSuccess += 1
#                 loginSuccessPrice += nach.price
#                 continue
#             elif nach.dogowor in old_dogowors:
#                 oldDogoworSuccess += 1
#                 oldDogoworSuccessPrice += nach.price
#                 continue
#             elif nach.login in old_logins:
#                 oldLoginSuccess += 1
#                 oldLoginSuccessPrice += nach.price
#                 continue
#             else:
#                 # print('errorcccccccccccc', nach)
#                 print('EEEEEEE', nach)
#                 error += 1
#                 errorPrice += nach.price
#         ####


#         context['dogoworSuccess'] = dogoworSuccess
#         context['dogoworSuccessPrice'] = dogoworSuccessPrice

#         context['loginSuccess'] = loginSuccess
#         context['loginSuccessPrice'] = loginSuccessPrice

#         ##№
#         context['oldLoginSuccess'] = oldLoginSuccess
#         context['oldLoginSuccessPrice'] = oldLoginSuccessPrice
#         context['oldDogoworSuccess'] = oldDogoworSuccess
#         context['oldDogoworSuccessPrice'] = oldDogoworSuccessPrice
#         ###№

#         context['error'] = error
#         context['errorPrice'] = errorPrice

#     poDogoworuCount = 0
#     poDogoworuPrice = 0
#     poLoginCount = 0
#     poLoginPrice = 0

#     poOldDogoworuCount = 0
#     poOldDogoworuPrice = 0
#     poOldLoginCount = 0
#     poOldLoginPrice = 0

#     # Если нажал на начислить
#     if request.method == 'POST' and 'comment' in request.POST:
#         if etrap != 'all':
#             if off == 'False':
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allON")
#                     messages.error(request, f'Ошибка за месяц {month_word} {year} года интернет начислений ON было сделано на все Этрапы')
#                     return redirect(request.POST.get('url_from'))
#                 except:
#                     pass
#             else:
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allOFF")
#                     messages.error(request, f'Ошибка за месяц {month_word} {year} года интернет начислений OFF было сделано на все Этрапы')
#                     return redirect(request.POST.get('url_from'))
#                 except:
#                     pass
#         else:
#             if off == 'False':
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzON")
#                     Dashoguz = 'Dashoguz'
#                 except:
#                     Dashoguz = ''

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeON")
#                     Akdepe = 'Akdepe'
#                 except:
#                     Akdepe = ''

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazON")
#                     Boldumsaz = 'Boldumsaz'
#                 except:
#                     Boldumsaz = ''

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyON")
#                     Gorogly = 'Gorogly'
#                 except:
#                     Gorogly = ''

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchON")
#                     Koneurgench = 'Koneurgench'
#                 except:
#                     Koneurgench = ''

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyON")
#                     Turkmenbashy = 'Turkmenbashy'
#                 except:
#                     Turkmenbashy = ''

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowON")
#                     Nyyazow = 'Nyyazow'
#                 except:
#                     Nyyazow = ''

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentON")
#                     Ruhubelent = 'Ruhubelent'
#                 except:
#                     Ruhubelent = ''

#                 if Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
#                     messages.error(request, f'Ошибка за месяц {month_word} {year} Вы не можете начислить ON на все этрапы так как некоторые этрапы уже были начислены ({Dashoguz} {Akdepe} {Boldumsaz} {Gorogly} {Koneurgench} {Turkmenbashy} {Nyyazow} {Ruhubelent})')
#                     return redirect(request.POST.get('url_from'))
            
        
#             else:
#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzOFF")
#                     Dashoguz = 'Dashoguz'
#                 except:
#                     Dashoguz = ''

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeOFF")
#                     Akdepe = 'Akdepe'
#                 except:
#                     Akdepe = ''

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazOFF")
#                     Boldumsaz = 'Boldumsaz'
#                 except:
#                     Boldumsaz = ''

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyOFF")
#                     Gorogly = 'Gorogly'
#                 except:
#                     Gorogly = ''

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchOFF")
#                     Koneurgench = 'Koneurgench'
#                 except:
#                     Koneurgench = ''

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyOFF")
#                     Turkmenbashy = 'Turkmenbashy'
#                 except:
#                     Turkmenbashy = ''

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowOFF")
#                     Nyyazow = 'Nyyazow'
#                 except:
#                     Nyyazow = ''

#                 try:
#                     DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentOFF")
#                     Ruhubelent = 'Ruhubelent'
#                 except:
#                     Ruhubelent = ''

#                 if Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
#                     messages.error(request, f'Ошибка за месяц {month_word} {year} Вы не можете начислить OFF на все этрапы так как некоторые этрапы уже были начислены ({Dashoguz} {Akdepe} {Boldumsaz} {Gorogly} {Koneurgench} {Turkmenbashy} {Nyyazow} {Ruhubelent})')
#                     return redirect(request.POST.get('url_from'))
                
#         try:
#             if off == 'False':
#                 DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}ON")
#                 messages.error(request, f'Ошибка за месяц {month_word} {year} года {etrap} интернет начисления ON уже начислено')
#                 return redirect(request.POST.get('url_from'))  
#             else:
#                 DontRepeatYourself.objects.get(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}OFF")
#                 messages.error(request, f'Ошибка за месяц {month_word} {year} года {etrap} интернет начисления OFF уже начислено')
#                 return redirect(request.POST.get('url_from'))  
#         except:
#             pass

#         if request.POST.get('comment') == '':
#             messages.error(request, f'Комментарий не может быть пустым')  
#             return redirect(request.POST.get('url_from'))
#         else:
#             if internetNachisleniya == {}:
#                 messages.error(request, f'Ошибка! за месяц {month_word} {year} года нет ни одного начислений для начисления')
#                 return redirect(request.POST.get('url_from'))
        
        
        
#         if etrap == 'all':
#             code = None
#             users = UserTable.objects.all()
#             nachMinus = NachMinus.objects.filter(year=year, month=month_numb)
#         else:
#             code = getEtrapCode(etrap)
#             users = UserTable.objects.filter(etrap=request.GET.get('etrap'))
#             nachMinus = NachMinus.objects.filter(year=year, month=month_numb, user__etrap=request.GET.get('etrap'))


#         # Сохранения начислений с договором
#         userDogoworPk = {}
#         for user in users:
#             if user.dogowor != '':
#                 userDogoworPk[user.dogowor] = user.pk

#         nachDogoworPrice = {}
        
#         for n in internetNachisleniya:
#             if n.dogowor not in nachDogoworPrice:
#                 nachDogoworPrice[n.dogowor] = n.price
#             else:
#                 nachDogoworPrice[n.dogowor] += n.price
        
#         DBNachDogoworPK = {}
#         for n in nachMinus:
#             DBNachDogoworPK[n.user.dogowor] = n.pk
        
#         list_bulk_create = []
#         succes = 0
#         try:
#             with transaction.atomic():
#                 for dogowor, price in nachDogoworPrice.items():
#                     if dogowor in userDogoworPk:
#                         user = UserTable.objects.get(pk=userDogoworPk[dogowor])
#                         poDogoworuCount += 1
#                         poDogoworuPrice += price
#                         print('Начислений по договору', poDogoworuCount)
#                         user.b_internet -= price

#                         if dogowor not in DBNachDogoworPK:
#                             list_bulk_create.append([user, month_numb, year, price])
#                         else:
#                             newNachMinus = NachMinus.objects.get(pk=DBNachDogoworPK[dogowor])
#                             newNachMinus.internet += price
#                             newNachMinus.save()
                    
#                         user.save()
#                         succes += 1

#                         # Если выбрано 'all' (все этрапы)
#                         if etrap == 'all':
#                             try:
#                                 nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=user.etrap, year=year, month=month_word)
#                                 nachisleniyaOtchet.intetnetNachisleniya += price
#                                 nachisleniyaOtchet.save()
#                             except:
#                                 NachisleniyaOtchet.objects.create(etrap=user.etrap, year=year, month=month_word, intetnetNachisleniya = price)

#                 if list_bulk_create:
#                     aux=[]
#                     for item in list_bulk_create:
#                         obj = NachMinus(user=item[0], month=item[1], year=item[2], internet=item[3])
#                         aux.append(obj)
#                     NachMinus.objects.bulk_create(aux)


#                 # Сохранения начислений с логином
#                 userLoginPk = {}
#                 for user in users:
#                     if user.login:
#                         userLoginPk[user.login] = user.pk

                

#                 nachLoginPrice = {}

#                 for n in internetNachisleniya:
#                     if n.login not in nachLoginPrice and n.dogowor not in dogowors:
#                         nachLoginPrice[n.login] = n.price
#                     elif n.login in nachLoginPrice and n.dogowor not in dogowors:
#                         nachLoginPrice[n.login] += n.price
                

#                 DBNachLoginPK = {}
#                 for n in nachMinus:
#                     if n.user.login:
#                         DBNachLoginPK[n.user.login] = n.pk


#                 list_bulk_create = []
#                 succes2 = 0
#                 for login, price in nachLoginPrice.items():
#                     if login in userLoginPk:

#                         user = UserTable.objects.get(pk=userLoginPk[login])
#                         poLoginCount += 1
#                         poLoginPrice += price
#                         print('Начислений по логину', poLoginCount)
#                         user.b_internet -= price

#                         if login not in DBNachLoginPK:
#                             list_bulk_create.append([user, month_numb, year, price])
#                         else:
#                             newNachMinus = NachMinus.objects.get(pk=DBNachLoginPK[login])
#                             newNachMinus.internet += price
#                             newNachMinus.save()
#                         user.save()
#                         succes2 += 1

#                         # Если выбрано 'all' (все этрапы)
#                         if etrap == 'all':
#                             try:
#                                 nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=user.etrap, year=year, month=month_word)
#                                 nachisleniyaOtchet.intetnetNachisleniya += price
#                                 nachisleniyaOtchet.save()
#                             except:
#                                 NachisleniyaOtchet.objects.create(etrap=user.etrap, year=year, month=month_word, intetnetNachisleniya = price)
#                 if list_bulk_create:
#                     aux=[]
#                     for item in list_bulk_create:
#                         obj = NachMinus(user=item[0], month=item[1], year=item[2], internet=item[3])
#                         aux.append(obj)
#                     NachMinus.objects.bulk_create(aux)

#                 ###
#                 # начисляем Login, Dogowor начисления которые нет в UserTable (по причине изменения), но есть в OldLoginDogowor
#                 for n in internetNachisleniya:
#                     if n.login not in logins and n.dogowor not in dogowors:
#                         if n.login in old_logins:
                            
#                             # print(n.logins, old_logins[n.login])
#                             print(n.login)
#                             old_login_user = UserTable.objects.get(etrap=old_logins[n.login][0], number=old_logins[n.login][1])
#                             old_login_user.b_internet -= n.price
#                             poOldLoginCount += 1
#                             poOldLoginPrice += n.price
#                             print('Начислений по old логину', poOldLoginCount)
#                             old_login_user.save()


#                             try:
#                                 old_login_nachMinus = NachMinus.objects.get(user=old_login_user, year=year, month=month_numb)
#                                 old_login_nachMinus.internet += n.price
#                                 old_login_nachMinus.save()
#                             except:
#                                 NachMinus.objects.create(user=old_login_user, year=year, month=month_numb, internet=n.price)

#                             try:
#                                 nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=old_logins[n.login][0], year=year, month=month_word)
#                                 nachisleniyaOtchet.intetnetNachisleniya += n.price
#                                 nachisleniyaOtchet.save()
#                             except:
#                                 NachisleniyaOtchet.objects.create(etrap=old_logins[n.login][0], year=year, month=month_word, intetnetNachisleniya=n.price)

#                         elif n.dogowor in old_dogowors:
#                             old_dogowor_user = UserTable.objects.get(etrap=old_dogowors[n.dogowor][0], number=old_dogowors[n.dogowor][1])
#                             old_dogowor_user.b_internet -= n.price
#                             poOldDogoworuCount += 1
#                             poOldDogoworuPrice += n.price
#                             print('Начислений по old договору', poOldDogoworuCount)
#                             old_dogowor_user.save()


#                             try:
#                                 old_dogowor_nachMinus = NachMinus.objects.get(user=old_dogowor_user, year=year, month=month_numb)
#                                 old_dogowor_nachMinus.internet += n.price
#                                 old_dogowor_nachMinus.save()
#                             except:
#                                 NachMinus.objects.create(user=old_dogowor_user, year=year, month=month_numb, internet=n.price)

#                             try:
#                                 nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=old_dogowors[n.dogowor][0], year=year, month=month_word)
#                                 nachisleniyaOtchet.intetnetNachisleniya += n.price
#                                 nachisleniyaOtchet.save()
#                             except:
#                                 NachisleniyaOtchet.objects.create(etrap=old_dogowors[n.dogowor][0], year=year, month=month_word, intetnetNachisleniya=n.price)
                    
#                 ####


#                 # Сохранение инфы о начисленном месяце и того кто начисли и т.п.
#                 if off == 'False':
#                     DontRepeatYourself.objects.create(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}ON")  
#                 else:
#                     DontRepeatYourself.objects.create(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}OFF")

#                 if off == 'False':
#                     StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')} \n\n Интернет Начисления ON за месяц {month_word} {year} года для этрапа {etrap}", action='Начисления Интернет')  
#                 else:
#                     StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')} \n\n Интернет Начисления OFF за месяц {month_word} {year} года для этрапа {etrap}", action='Начисления Интернет')  

#                 if off == 'False':
#                     messages.success(request, f'Успешное Интернет начисления ON для {etrap} за месяц {month_word} {year} года')
#                 else:
#                     messages.success(request, f'Успешное Интернет начисления OFF для {etrap} - за месяц {month_word} {year} года')  
                    

#                 print('Начислено по договору абонентов',poDogoworuCount)
#                 print('Начислено по договору Цена',poDogoworuPrice)
#                 print('Начислено по логину абонентов',poLoginCount)
#                 print('Начислено по логину цена',poLoginPrice)
#                 print('Начислено по old договору абонентов',poOldDogoworuCount)
#                 print('Начислено по old договору цена',poOldDogoworuPrice)
#                 print('Начислено по old логину абонентов',poOldLoginCount)
#                 print('Начислено по old логину цена',poOldLoginPrice)
#                 # ##################################################
#                 # Сохраняем сумму начисления для месячного отчета ##
#                 #  #################################################
#                 if etrap in etraps:
#                     try:
#                         NachisleniyaOtchet.objects.get(year=year, month=month_word, etrap=etrap)
#                         NachisleniyaOtchet.objects.filter(year=year, month=month_word, etrap=etrap).update(
#                         intetnetNachisleniya=F('intetnetNachisleniya') + (dogoworSuccessPrice + loginSuccessPrice))
#                     except:
#                         NachisleniyaOtchet.objects.create(
#                             etrap=etrap,
#                             year=year, 
#                             month=month_word, 
#                             intetnetNachisleniya= (dogoworSuccessPrice + loginSuccessPrice))

#                 # ######################################################
#                 # Сохраняем сумму начисления для месячного отчета END ##
#                 #  #####################################################
              
#                 UserTable.objects.filter(is_enterprises=True).update(b_telefon=0, b_slr=0, b_kod=0, b_zakaz=0, b_prochee=0, b_dop_uslugi=0, b_internet=0, b_alem=0)
#         except Exception as e:
#             logger.warning(f"Ошибка (Откат)! {str(e)}")
#             messages.error(request, f'Ошибка (Откат)! {str(e)}')

#     return render(request, 'telekom/MATB/xlsx/XlsxNachisleniya/internetNachisleniyaBtn.html', context)