from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum

# https://metanit.com/python/django/5.5.php
# Для update
from django.db.models import F

from datetime import date

from telekom.models import DontRepeatYourself, ImportAlemNachisleniyaOFF, ImportAlemNachisleniyaON, NachMinus, NachisleniyaOtchet, StaffAction, UserTable

from telekom.views2.myFunc.myFunc import getCodeEtrap, getEtrapCode, loggedUserEtrapAndGroup, monthСonvert



def alemNachisleniya(request):
    if not request.user.is_superuser and request.user.username != 'admin1':
        messages.error(request, f'Доступ только Администратору')
        return redirect('user-login')
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    
    context = {}
    context['matbIndex'] = True
    context['alemNachisleniya'] = True

    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date

    # log = getLoggedUserEtrap(request.user.username)
    context['log'] = log
    context['months'] = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['years'] = ['2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
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
        return redirect('alem-nachisleniya')


    
    
    
    if month_word and year and etrap:
    
        if request.GET.get('off') == None:
            if etrap in etraps:
                alemNachisleniya = ImportAlemNachisleniyaON.objects.filter(month=month_word, year=year, etrap=etrap)

                # Проверяем было ли начисление этого QuerySet (для отключения кнопки начислить)
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}ON")
                    context['alreadyNach'] = True
                except:
                    try:
                        DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allON")
                        context['alreadyNach'] = True
                    except:
                        context['alreadyNach'] = False


            elif etrap == 'all':
                alemNachisleniya = ImportAlemNachisleniyaON.objects.filter(month=month_word, year=year)
                # Были ли частичные начисления (другие этрапы)
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allON")
                    context['alreadyNach'] = True
                except:
                    pass
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzON")
                    Dashoguz = 'Dashoguz'
                except:
                    Dashoguz = ''
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeON")
                    Akdepe = 'Akdepe'
                except:
                    Akdepe = ''
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazON")
                    Boldumsaz = 'Boldumsaz'
                except:
                    Boldumsaz = ''
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyON")
                    Gorogly = 'Gorogly'
                except:
                    Gorogly = ''
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchON")
                    Koneurgench = 'Koneurgench'
                except:
                    Koneurgench = ''
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyON")
                    Turkmenbashy = 'Turkmenbashy'
                except:
                    Turkmenbashy = ''
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowON")
                    Nyyazow = 'Nyyazow'
                except:
                    Nyyazow = ''
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentON")
                    Ruhubelent = 'Ruhubelent'
                except:
                    Ruhubelent = ''

                if Dashoguz and Akdepe and Boldumsaz and Gorogly and Koneurgench and Turkmenbashy and Nyyazow and Ruhubelent:
                    context['alreadyallNach'] = True
                elif Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
                    context['alreadySeparateNach'] = True


        elif request.GET.get('off') == 'on':
            if etrap in etraps:
                alemNachisleniya = ImportAlemNachisleniyaOFF.objects.filter(month=month_word, year=year, etrap=etrap)
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}OFF")
                    context['alreadyNach'] = True
                except:
                    try:
                        DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allOFF")
                        context['alreadyNach'] = True
                    except:
                        context['alreadyNach'] = False
            elif etrap == 'all':
                alemNachisleniya = ImportAlemNachisleniyaOFF.objects.filter(month=month_word, year=year)

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allOFF")
                    context['alreadyNach'] = True
                except:
                    pass

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzOFF")
                    Dashoguz = 'Dashoguz'
                except:
                    Dashoguz = ''
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeOFF")
                    Akdepe = 'Akdepe'
                except:
                    Akdepe = ''
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazOFF")
                    Boldumsaz = 'Boldumsaz'
                except:
                    Boldumsaz = ''
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyOFF")
                    Gorogly = 'Gorogly'
                except:
                    Gorogly = ''
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchOFF")
                    Koneurgench = 'Koneurgench'
                except:
                    Koneurgench = ''
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyOFF")
                    Turkmenbashy = 'Turkmenbashy'
                except:
                    Turkmenbashy = ''
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowOFF")
                    Nyyazow = 'Nyyazow'
                except:
                    Nyyazow = ''
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentOFF")
                    Ruhubelent = 'Ruhubelent'
                except:
                    Ruhubelent = ''
                if Dashoguz and Akdepe and Boldumsaz and Gorogly and Koneurgench and Turkmenbashy and Nyyazow and Ruhubelent:
                    context['alreadyallNach'] = True
                elif Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
                    context['alreadySeparateNach'] = True

        if len(alemNachisleniya) == 0:
            context['nothingNach'] = True

        context['totalPayCount'] = len(alemNachisleniya)
        context['totalPayPrice'] = alemNachisleniya.aggregate(Sum('price'))['price__sum']

        


        dogoworSuccess = 0
        dogoworSuccessPrice = 0

        error = 0
        errorPrice = 0

        users = UserTable.objects.all()
        
        for n in alemNachisleniya:
            try:
                users.get(etrap=getCodeEtrap(n.dogowor[8:11]), number=n.dogowor[11:])
                dogoworSuccess += 1
                dogoworSuccessPrice += n.price
            except:
                error += 1
                errorPrice += n.price


        context['dogoworSuccess'] = dogoworSuccess
        context['dogoworSuccessPrice'] = dogoworSuccessPrice

        context['error'] = error
        context['errorPrice'] = errorPrice


    # Если нажал на начислить
    if request.method == 'POST' and 'comment' in request.POST:
        if etrap != 'all':
            if off == 'False':
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allON")
                    messages.error(request, f'Ошибка за месяц {month_word} {year} года Alem начислений ON было сделано на все Этрапы')
                    return redirect(request.POST.get('url_from'))
                except:
                    pass
            else:
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}allOFF")
                    messages.error(request, f'Ошибка за месяц {month_word} {year} года Alem начислений OFF было сделано на все Этрапы')
                    return redirect(request.POST.get('url_from'))
                except:
                    pass
        else:
            if off == 'False':
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzON")
                    Dashoguz = 'Dashoguz'
                except:
                    Dashoguz = ''

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeON")
                    Akdepe = 'Akdepe'
                except:
                    Akdepe = ''

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazON")
                    Boldumsaz = 'Boldumsaz'
                except:
                    Boldumsaz = ''

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyON")
                    Gorogly = 'Gorogly'
                except:
                    Gorogly = ''

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchON")
                    Koneurgench = 'Koneurgench'
                except:
                    Koneurgench = ''

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyON")
                    Turkmenbashy = 'Turkmenbashy'
                except:
                    Turkmenbashy = ''

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowON")
                    Nyyazow = 'Nyyazow'
                except:
                    Nyyazow = ''

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentON")
                    Ruhubelent = 'Ruhubelent'
                except:
                    Ruhubelent = ''

                if Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
                    messages.error(request, f'Ошибка за месяц {month_word} {year} Вы не можете начислить ON на все этрапы так как некоторые этрапы уже были начислены ({Dashoguz} {Akdepe} {Boldumsaz} {Gorogly} {Koneurgench} {Turkmenbashy} {Nyyazow} {Ruhubelent})')
                    return redirect(request.POST.get('url_from'))
            
        
            else:
                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}DashoguzOFF")
                    Dashoguz = 'Dashoguz'
                except:
                    Dashoguz = ''

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}AkdepeOFF")
                    Akdepe = 'Akdepe'
                except:
                    Akdepe = ''

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}BoldumsazOFF")
                    Boldumsaz = 'Boldumsaz'
                except:
                    Boldumsaz = ''

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}GoroglyOFF")
                    Gorogly = 'Gorogly'
                except:
                    Gorogly = ''

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}KoneurgenchOFF")
                    Koneurgench = 'Koneurgench'
                except:
                    Koneurgench = ''

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}TurkmenbashyOFF")
                    Turkmenbashy = 'Turkmenbashy'
                except:
                    Turkmenbashy = ''

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}S.A.NyyazowOFF")
                    Nyyazow = 'Nyyazow'
                except:
                    Nyyazow = ''

                try:
                    DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}RuhubelentOFF")
                    Ruhubelent = 'Ruhubelent'
                except:
                    Ruhubelent = ''

                if Dashoguz or Akdepe or Boldumsaz or Gorogly or Koneurgench or Turkmenbashy or Nyyazow or Ruhubelent:
                    messages.error(request, f'Ошибка за месяц {month_word} {year} Вы не можете начислить OFF на все этрапы так как некоторые этрапы уже были начислены ({Dashoguz} {Akdepe} {Boldumsaz} {Gorogly} {Koneurgench} {Turkmenbashy} {Nyyazow} {Ruhubelent})')
                    return redirect(request.POST.get('url_from'))
                
        try:
            if off == 'False':
                DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}ON")
                messages.error(request, f'Ошибка за месяц {month_word} {year} года {etrap} Alem начисления ON уже начислено')
                return redirect(request.POST.get('url_from'))  
            else:
                DontRepeatYourself.objects.get(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}OFF")
                messages.error(request, f'Ошибка за месяц {month_word} {year} года {etrap} Alem начисления OFF уже начислено')
                return redirect(request.POST.get('url_from'))  
        except:
            pass

        if request.POST.get('comment') == '':
            messages.error(request, f'Комментарий не может быть пустым')  
            return redirect(request.POST.get('url_from'))
        else:
            if alemNachisleniya == {}:
                messages.error(request, f'Ошибка! за месяц {month_word} {year} года нет начислений')
                return redirect(request.POST.get('url_from'))
        
        
        
        if etrap == 'all':
            users = UserTable.objects.all()
            nachMinus = NachMinus.objects.filter(year=year, month=month_numb)
        else:
            users = UserTable.objects.filter(etrap=request.GET.get('etrap'))
            nachMinus = NachMinus.objects.filter(year=year, month=month_numb, user__etrap=request.GET.get('etrap'))





        # Сохранения начислений с договором
        totalPrice = 0
        for n in alemNachisleniya:
            try:
                user = users.get(etrap=getCodeEtrap(n.dogowor[8:11]), number=n.dogowor[11:])
                user.b_alem -= n.price
                user.save()
                try:
                    nach = nachMinus.get(user=user, year=year, month=month_numb)
                    nach.alem += n.price
                    nach.save()
                except:
                    NachMinus.objects.create(user=user, year=year, month=month_numb, alem=n.price)

                if etrap in etraps:
                    totalPrice += n.price
                elif etrap == 'all':
                    try:
                        nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=user.etrap, year=year, month=month_word)
                        nachisleniyaOtchet.alemNachisleniya += n.price
                        nachisleniyaOtchet.save()
                    except:
                        NachisleniyaOtchet.objects.create(etrap=user.etrap, year=year, month=month_word, alemNachisleniya = n.price)
            except:
                pass 

        if etrap in etraps:
            try:
                nachisleniyaOtchet = NachisleniyaOtchet.objects.get(etrap=etrap, year=year, month=month_word)
                nachisleniyaOtchet.alemNachisleniya += totalPrice
                nachisleniyaOtchet.save()
            except:
                NachisleniyaOtchet.objects.create(etrap=etrap, year=year, month=month_word, alemNachisleniya = totalPrice)


        # Сохранение DontRepeatYourself и StaffAction.
        if off == 'False':
            DontRepeatYourself.objects.create(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}ON")  
        else:
            DontRepeatYourself.objects.create(alemNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}OFF")

        if off == 'False':
            StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')} \n\n Alem Начисления ON за месяц {month_word} {year} года для этрапа {etrap}", action='Начисления Alem')  
        else:
            StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')} \n\n alem Начисления OFF за месяц {month_word} {year} года для этрапа {etrap}", action='Начисления Alem')  

        if off == 'False':
            messages.success(request, f'Успешное Alem начисления ON для {etrap} за месяц {month_word} {year} года')  
        else:
            messages.success(request, f'Успешное Alem начисления OFF для {etrap} - за месяц {month_word} {year} года')  
            

    return render(request, 'telekom/MATB/alemNachisleniya.html', context)