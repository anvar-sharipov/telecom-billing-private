from django.shortcuts import render, redirect
from django.contrib import messages
# from telekom.models import AbonentService, DontRepeatYourself, NachMinus, NachisleniyaOtchet, StaffAction, UserTable
from django.db.models import Sum
from django.db.models import Q
from calendar import monthrange

from datetime import date
from telekom.models import DontRepeatYourself, NachMinus, NachisleniyaOtchet, PayHistory, StaffAction, UserTable

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert


def abonplataNachisleniya(request):
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == 'MTB' or request.user.is_superuser:
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам MATB')
        return redirect('user-login')
    

    
    context = {}
    context['matbIndex'] = True
    context['abonplataNachisleniya'] = True

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

    month_word = request.GET.get('month')
    year = request.GET.get('year')
    month_numb = monthСonvert(month_word)
    etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else 'Dashoguz'
    context['etrap'] = etrap
   

    if month_word == '':
        messages.error(request, f'Ошибка! Выберите месяц начисления')
        return redirect('abonplata-nachisleniya')
    
    if month_word or year:
        days_in_choosed_month = monthrange(int(year), int(monthСonvert(month_word)))[1]
        if etrap in etraps:
            usersN = UserTable.objects.filter(etrap=etrap, abonplata__gte=0, is_enterprises=False).filter(~Q(snyat_date__range=[f"{year}-{month_numb}-01", f"{year}-{month_numb}-{days_in_choosed_month}"]))
            usersE = UserTable.objects.filter(etrap=etrap, abonplata__gte=0, is_enterprises=True).filter(~Q(snyat_date__range=[f"{year}-{month_numb}-01", f"{year}-{month_numb}-{days_in_choosed_month}"]))
            # users = UserTable.objects.filter(etrap=etrap, abonplata__exact='').exclude(abonplata__isnull=True)
        elif etrap == 'all':
            usersN = UserTable.objects.filter(abonplata__gte=0, is_enterprises=False).filter(~Q(snyat_date__range=[f"{year}-{month_numb}-01", f"{year}-{month_numb}-{days_in_choosed_month}"]))
            usersE = UserTable.objects.filter(abonplata__gte=0, is_enterprises=True).filter(~Q(snyat_date__range=[f"{year}-{month_numb}-01", f"{year}-{month_numb}-{days_in_choosed_month}"]))

        context['countUserN'] = len(usersN)
        context['sumAbonplataN'] = usersN.aggregate(Sum('abonplata'))['abonplata__sum']

        context['countUserE'] = len(usersE)
        context['sumAbonplataE'] = usersE.aggregate(Sum('abonplata'))['abonplata__sum']
    else:
        usersN = []
        usersE = []

    

    context['disabled_nach'] = False
    if DontRepeatYourself.objects.filter(abonplataNachisleniaYearMonthEtrap = f"{year}{month_word}{etrap}"):
        context['disabled_nach'] = True
    if DontRepeatYourself.objects.filter(abonplataNachisleniaYearMonthEtrap = f"{year}{month_word}all"):
        context['disabled_nach'] = True
   
    if etrap == 'all':
        nach_etraps = []
        for e in etraps:
            if DontRepeatYourself.objects.filter(abonplataNachisleniaYearMonthEtrap__icontains = f"{year}{month_word}{e}"):
                nach_etraps.append(e)
            
        if nach_etraps:
            context['disabled_nach'] = True
            if len(DontRepeatYourself.objects.filter(abonplataNachisleniaYearMonthEtrap = f"{year}{month_word}all")) ==  0:
                context['ne_polnoye_nach'] = True
                context['disabled_nach'] = False
            else:
                context['ne_polnoye_nach'] = False
            
    context['totalUserCount'] = len(usersN) + len(usersE)

    totalCountE = 0
    totalCountN = 0
    totalPriceE = 0
    totalPriceN = 0

    if request.method == 'POST':
        if request.POST.get('comment') == '':
            messages.error(request, f"Комментарий не может быть пустым")
        else:
            if etrap in etraps:
                nachMinus = NachMinus.objects.filter(user__etrap=etrap, year=year, month=month_numb)
                try:
                    nachisleniyaOtchet = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap=etrap)
                except:
                    nachisleniyaOtchet = NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap=etrap)
                
                try:
                    DontRepeatYourself.objects.get(abonplataNachisleniaYearMonthEtrap = f"{year}{month_word}{etrap}")
                    messages.error(request, f"Ошибка! За месяц {month_word} {year} года этрап {etrap} уже начислено")
                    return redirect('abonplata-nachisleniya')
                except:
                    pass 

            elif etrap == 'all':
                nachMinus = NachMinus.objects.filter(year=year, month=month_numb)
                try:
                    DontRepeatYourself.objects.get(abonplataNachisleniaYearMonthEtrap = f"{year}{month_word}{etrap}")
                    messages.error(request, f"Ошибка! За месяц {month_word} {year} года все этрапы уже начислены")
                    return redirect('abonplata-nachisleniya')
                except:
                    pass
                    
                nachEtraps = []
                for e in etraps:
                    alreadyNach = DontRepeatYourself.objects.filter(abonplataNachisleniaYearMonthEtrap = f"{year}{month_word}{e}")
                    if alreadyNach:
                        nachEtraps.append(e)
                if nachEtraps:
                    messages.error(request, f"Ошибка! Вы не можете начислить на все эртапы за месяц {month_word} {year} года так-как некоторые этрапы уже начислены {nachEtraps}")
                    return redirect('abonplata-nachisleniya')
                
            if usersN:
                ak = 0
                bol = 0
                go = 0
                ko = 0
                tur = 0
                ny = 0
                ru = 0
                da = 0
                totalNach = 0

                countN = 0
                for user in usersN:
                    countN += 1
                    print('countN', countN)
                    try:
                        nach = nachMinus.get(user=user)
                    except:
                        nach = False

                    if nach:
                        nach.telefon += float(user.abonplata)
                    else:
                        NachMinus.objects.create(user=user, year=year, month=month_numb, telefon = user.abonplata)

                    if etrap == 'all':
                        if user.etrap == 'Dashoguz':
                            da += float(user.abonplata)
                        if user.etrap == 'Akdepe':
                            ak += float(user.abonplata)
                        if user.etrap == 'Gorogly':
                            go += float(user.abonplata)
                        if user.etrap == 'Ruhubelent':
                            ru += float(user.abonplata)
                        if user.etrap == 'S.A.Nyyazow':
                            ny += float(user.abonplata)
                        if user.etrap == 'Turkmenbashy':
                            tur += float(user.abonplata)
                        if user.etrap == 'Boldumsaz':
                            bol += float(user.abonplata)
                        if user.etrap == 'Koneurgench':
                            ko += float(user.abonplata)
                    else:
                        totalNach += float(user.abonplata)
                        
                    user.b_telefon -= float(user.abonplata)
                    if nach:
                        nach.save()

                    user.save()
                    totalCountN += 1
                    totalPriceN += float(user.abonplata)
                if etrap in etraps:
                    nachisleniyaOtchet.abonplataNachN += totalNach
                    nachisleniyaOtchet.save()
                else:
                    if da > 0:
                        try:
                            nachisleniyaOtchetDz = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='Dashoguz')
                            nachisleniyaOtchetDz.abonplataNachN += da
                            nachisleniyaOtchetDz.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='Dashoguz', abonplataNachN= da)
                    if ak > 0:
                        try:
                            nachisleniyaOtchetAk = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='Akdepe')
                            nachisleniyaOtchetAk.abonplataNachN += ak
                            nachisleniyaOtchetAk.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='Akdepe', abonplataNachN= ak)
                    if go > 0:
                        try:
                            nachisleniyaOtchetGo = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='Gorogly')
                            nachisleniyaOtchetGo.abonplataNachN += go
                            nachisleniyaOtchetGo.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='Gorogly', abonplataNachN= go)
                    if ru > 0:
                        try:
                            nachisleniyaOtchetRu = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='Ruhubelent')
                            nachisleniyaOtchetRu.abonplataNachN += ru
                            nachisleniyaOtchetRu.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='Ruhubelent', abonplataNachN= ru)
                    if ny > 0:
                        try:
                            nachisleniyaOtchetNy = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='S.A.Nyyazow')
                            nachisleniyaOtchetNy.abonplataNachN += ny
                            nachisleniyaOtchetNy.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='S.A.Nyyazow', abonplataNachN= ny)
                    if tur > 0:
                        try:
                            nachisleniyaOtchetTu = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='Turkmenbashy')
                            nachisleniyaOtchetTu.abonplataNachN += tur
                            nachisleniyaOtchetTu.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='Turkmenbashy', abonplataNachN= tur)
                    if bol > 0:
                        try:
                            nachisleniyaOtchetBol = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='Boldumsaz')
                            nachisleniyaOtchetBol.abonplataNachN += bol
                            nachisleniyaOtchetBol.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='Boldumsaz', abonplataNachN= bol)
                    if ko > 0:
                        try:
                            nachisleniyaOtchetKo = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='Koneurgench')
                            nachisleniyaOtchetKo.abonplataNachN += ko
                            nachisleniyaOtchetKo.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='Koneurgench', abonplataNachN= ko)
            if usersE:
                ak = 0
                bol = 0
                go = 0
                ko = 0
                tur = 0
                ny = 0
                ru = 0
                da = 0
                totalNach = 0
                countE = 0
                for user in usersE:
                    countE += 1
                    print('countE', countE)
                    try:
                        nach = nachMinus.get(user=user)
                    except:
                        nach = False

                    if nach:
                        nach.telefon += float(user.abonplata)
                    else:
                        NachMinus.objects.create(user=user, year=year, month=month_numb, telefon = user.abonplata)

                    if etrap == 'all':
                        if user.etrap == 'Dashoguz':
                            da += float(user.abonplata)
                        if user.etrap == 'Akdepe':
                            ak += float(user.abonplata)
                        if user.etrap == 'Gorogly':
                            go += float(user.abonplata)
                        if user.etrap == 'Ruhubelent':
                            ru += float(user.abonplata)
                        if user.etrap == 'S.A.Nyyazow':
                            ny += float(user.abonplata)
                        if user.etrap == 'Turkmenbashy':
                            tur += float(user.abonplata)
                        if user.etrap == 'Boldumsaz':
                            bol += float(user.abonplata)
                        if user.etrap == 'Koneurgench':
                            ko += float(user.abonplata)
                    else:
                        totalNach += float(user.abonplata)
                        
                    user.b_telefon -= float(user.abonplata)
                    if nach:
                        nach.save()
                    totalCountE += 1
                    totalPriceE += float(user.abonplata)
                    user.save()
                if etrap in etraps:
                    nachisleniyaOtchet.abonplataNachP += totalNach
                    nachisleniyaOtchet.save()
                else:
                    if da > 0:
                        try:
                            nachisleniyaOtchetDz = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='Dashoguz')
                            nachisleniyaOtchetDz.abonplataNachP += da
                            nachisleniyaOtchetDz.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='Dashoguz', abonplataNachP= da)
                    if ak > 0:
                        try:
                            nachisleniyaOtchetAk = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='Akdepe')
                            nachisleniyaOtchetAk.abonplataNachP += ak
                            nachisleniyaOtchetAk.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='Akdepe', abonplataNachP= ak)
                    if go > 0:
                        try:
                            nachisleniyaOtchetGo = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='Gorogly')
                            nachisleniyaOtchetGo.abonplataNachP += go
                            nachisleniyaOtchetGo.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='Gorogly', abonplataNachP= go)
                    if ru > 0:
                        try:
                            nachisleniyaOtchetRu = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='Ruhubelent')
                            nachisleniyaOtchetRu.abonplataNachP += ru
                            nachisleniyaOtchetRu.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='Ruhubelent', abonplataNachP= ru)
                    if ny > 0:
                        try:
                            nachisleniyaOtchetNy = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='S.A.Nyyazow')
                            nachisleniyaOtchetNy.abonplataNachP += ny
                            nachisleniyaOtchetNy.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='S.A.Nyyazow', abonplataNachP= ny)
                    if tur > 0:
                        try:
                            nachisleniyaOtchetTu = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='Turkmenbashy')
                            nachisleniyaOtchetTu.abonplataNachP += tur
                            nachisleniyaOtchetTu.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='Turkmenbashy', abonplataNachP= tur)
                    if bol > 0:
                        try:
                            nachisleniyaOtchetBol = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='Boldumsaz')
                            nachisleniyaOtchetBol.abonplataNachP += bol
                            nachisleniyaOtchetBol.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='Boldumsaz', abonplataNachP= bol)
                    if ko > 0:
                        try:
                            nachisleniyaOtchetKo = NachisleniyaOtchet.objects.get(month=month_word, year=year, etrap='Koneurgench')
                            nachisleniyaOtchetKo.abonplataNachP += ko
                            nachisleniyaOtchetKo.save()
                        except:
                            NachisleniyaOtchet.objects.create(month=month_word, year=year, etrap='Koneurgench', abonplataNachP= ko)

            StaffAction.objects.create(user=request.user, comment=f"{request.POST.get('comment')} \n\n\ Начисления абонплаты за месяц {month_word} {year} года Этрапа {etrap}", action='Начисления абонплата')

            DontRepeatYourself.objects.create(abonplataNachisleniaYearMonthEtrap=f"{year}{month_word}{etrap}")

       
            messages.success(request, f"Успешное начисление за {month_word} {year} года Этрап {etrap}")

            print('totalCountN', totalCountN)
            print('totalPriceN', totalPriceN)
            print('totalCountE', totalCountE)
            print('totalPriceE', totalPriceE)
                    

      
    return render(request, 'telekom/MATB/abonplataNachisleniya.html', context)



