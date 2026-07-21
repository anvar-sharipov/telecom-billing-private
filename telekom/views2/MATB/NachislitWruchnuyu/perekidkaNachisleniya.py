from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from datetime import datetime
from telekom.models import *




def perekidkaNachisleniya(request):
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    
    request_user = request.user
    groups = request_user.groups.all()
    request_user_etrap = ''
    request_user_type = ''
    for g in groups:
        request_user_etrap, request_user_type = g.name.split('_')
        if request_user_type == 'MTB':# or request.user.username == 'admin1':
            break

    if request_user_type != 'MTB' and (not request.user.is_superuser and request.user.username != 'admin1'):
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')

    context = {}

    context['all_new_for_mtb'] = True
    context['etraps'] = etraps

    current_date = datetime.now().date()
    formatted_date = current_date.strftime('%Y-%m-%d')
    current_year, current_month, current_day = formatted_date.split('-')

    context['formatted_date'] = formatted_date
    context['current_year'] = current_year
    context['current_month'] = current_month
    context['current_day'] = current_day

    
    context['perekidkaNachisleniya'] = True
    if request_user_type == 'MTB':
        context['matbIndex'] = True 
        context['request_user_etrap'] = request_user_etrap

    etrap1 = request.GET.get('etrap1')
    number1 = request.GET.get('number1')
    year1 = request.GET.get('year1')
    month1 = request.GET.get('month1')

    etrap2 = request.GET.get('etrap2')
    number2 = request.GET.get('number2')
    # year2 = request.GET.get('year2')
    # month2 = request.GET.get('month2')

    allow = False
    if not request.user.is_superuser and request.user.username != 'admin1':
        if not etrap1 and not etrap2:
            allow = True
        if not etrap1 and etrap2 in etraps and etrap2 == request_user_etrap:
            allow = True
        if etrap1 and etrap1 in etraps and etrap1 == request_user_etrap and not etrap2:
            allow = True
        if etrap1 and etrap2 and etrap1 in etraps and etrap2 in etraps and etrap1 == request_user_etrap and etrap2 == request_user_etrap:
            allow = True
    else:
        allow = True

    if not allow:
        messages.error(request, f"Выберите абонента с своего этрапа")
        return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidkaNachisleniya.html', context)

    context['etrap1'] = etrap1
    context['number1'] = number1
    context['year1'] = year1
    context['month1'] = month1

    context['selected_etrap1'] = etrap1
    context['selected_year1'] = year1
    context['selected_month1'] = month1

    context['etrap2'] = etrap2
    context['number2'] = number2
    # context['year2'] = year2
    # context['month2'] = month2

    context['selected_etrap2'] = etrap2
    # context['selected_year2'] = year2
    # context['selected_month2'] = month2

    user1 = False
    user1k = False
    if etrap1 in etraps and number1 and year1 and month1:
        if int(number1) > 19999 and int(number1) < 105000:
            if int(number1) < 100000:
                try:
                    user1 = UserTable.objects.get(etrap=etrap1, number=number1)
                except:
                    pass
            try:
                user1k = KabelTvNew.objects.get(number=number1)
            except:
                pass

    user2 = False
    user2k = False
    if etrap2 in etraps and number2 and year1 and month1:
        if int(number2) > 19999 and int(number2) < 105000:
            if int(number2) < 100000:
                try:
                    user2 = UserTable.objects.get(etrap=etrap2, number=number2)
                except:
                    pass
            try:
                user2k = KabelTvNew.objects.get(number=number2)
            except:
                pass

    context['user1'] = user1
    context['user1k'] = user1k

    context['user2'] = user2
    context['user2k'] = user2k

    if user1:
        total_telefoniya_balance1 = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
        context['total_telefoniya_balance1'] = total_telefoniya_balance1
        try:
            user1_n = user1.nachminus_set.get(year=year1, month=month1)
            context['user1_n'] = user1_n
        except:
            pass


    if user2:
        total_telefoniya_balance2 = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
        context['total_telefoniya_balance2'] = total_telefoniya_balance2

        try:
            user2_n = user2.nachminus_set.get(year=year1, month=month1)
            context['user2_n'] = user2_n
            print('user2_n', user2_n)
        except:
            pass

    if user1k:
        try:
            user1k_n = user1k.kabelnach_set.get(year=year1, month=month1)
            context['user1k_n'] = user1k_n
        except:
            pass

    if user2k:
        try:
            user2k_n = user2k.kabelnach_set.get(year=year1, month=month1)
            context['user2k_n'] = user2k_n
        except:
            pass

    if request.method == 'POST':
        comment = request.POST.get('comment')
        telefon1 = float(request.POST.get('telefon1')) if request.POST.get('telefon1') != None else 0 
        telefon1CheckBox = request.POST.get('telefon1CheckBox')

        slr1 = float(request.POST.get('slr1')) if request.POST.get('slr1') != None else 0 
        slr1CheckBox = request.POST.get('slr1CheckBox')

        kod1 = float(request.POST.get('kod1')) if request.POST.get('kod1') != None else 0 
        kod1CheckBox = request.POST.get('kod1CheckBox')

        zakaz1 = float(request.POST.get('zakaz1')) if request.POST.get('zakaz1') != None else 0 
        zakaz1CheckBox = request.POST.get('zakaz1CheckBox')

        prochee1 = float(request.POST.get('prochee1')) if request.POST.get('prochee1') != None else 0
        prochee1CheckBox = request.POST.get('prochee1CheckBox')

        dop_uslugi1 = float(request.POST.get('dop_uslugi1')) if request.POST.get('dop_uslugi1') != None else 0 
        dop_uslugi1CheckBox = request.POST.get('dop_uslugi1CheckBox')

        internet1 = float(request.POST.get('internet1')) if request.POST.get('internet1') != None else 0 
        internet1CheckBox = request.POST.get('internet1CheckBox')

        alem1 = float(request.POST.get('alem1')) if request.POST.get('alem1') != None else 0 
        alem1CheckBox = request.POST.get('alem1CheckBox')

        kabel1 = float(request.POST.get('kabel1')) if request.POST.get('kabel1') != None else 0 
        kabel1CheckBox = request.POST.get('kabel1CheckBox')


        if telefon1CheckBox or slr1CheckBox or kod1CheckBox or zakaz1CheckBox or prochee1CheckBox or dop_uslugi1CheckBox or internet1CheckBox or alem1CheckBox:
            nach1 = NachMinus.objects.get(year=year1, user=user1, month=month1)
            try:
                nach2 = NachMinus.objects.get(year=year1, user=user2, month=month1)
            except:
                nach2 = NachMinus(year=year1, user=user2, month=month1)

        if kabel1CheckBox:
            nach1_k = KabelNach.objects.get(year=year1, user=user1k, month=month1)
            try:
                nach2_k = KabelNach.objects.get(year=year1, user=user2k, month=month1)
            except:
                nach2_k = KabelNach(year=year1, user=user2k, month=month1)

        


        


        mes = 'Успешная перекидка начислений: '
        comm = f"""Перекидка начислений с номера {number1} {etrap1} на номер {number2} {etrap2} год и месяц начисления {year1} {month1}:\n    """

        nach_per_history = NachPerekidkaHistory(
                operator=request.user.username,
                user1Number=number1,
                user1Etrap=etrap1,
                user2Number=number2,
                user2Etrap=etrap2
            )

        if telefon1CheckBox:
            mes += f'Абонплата: {telefon1} '
            if telefon1 > 0:
                nach1.telefon -= telefon1
                nach2.telefon += telefon1
                user1.b_telefon += telefon1
                user2.b_telefon -= telefon1
                comm += f"""с абонплата на абонплата: {telefon1}\n    """
                nach_per_history.telefon1 += telefon1
                nach_per_history.telefon2 += telefon1

        if slr1CheckBox:
            mes += f'Слр: {slr1}, '
            if slr1 > 0:
                nach1.slr -= slr1
                nach2.slr += slr1
                user1.b_slr += slr1
                user2.b_slr -= slr1
                comm += f"""с слр на слр: {slr1}\n    """
                nach_per_history.slr1 += slr1
                nach_per_history.slr2 += slr1

        if kod1CheckBox:
            mes += f'Код: {kod1}, '
            if kod1 > 0:
                nach1.kod -= kod1
                nach2.kod += kod1
                user1.b_kod += kod1
                user2.b_kod -= kod1
                comm += f"""с код на код: {kod1}\n    """
                nach_per_history.kod1 += kod1
                nach_per_history.kod2 += kod1

        if zakaz1CheckBox:
            mes += f'Заказ: {zakaz1}, '
            if zakaz1 > 0:
                nach1.zakaz -= zakaz1
                nach2.zakaz += zakaz1
                user1.b_zakaz += zakaz1
                user2.b_zakaz -= zakaz1
                comm += f"""с заказ на заказ: {zakaz1}\n    """
                nach_per_history.zakaz1 += zakaz1
                nach_per_history.zakaz2 += zakaz1

        if prochee1CheckBox:
            mes += f'Прочее: {prochee1}, '
            if prochee1 > 0:
                nach1.prochee -= prochee1
                nach2.prochee += prochee1
                user1.b_prochee += prochee1
                user2.b_prochee -= prochee1
                comm += f"""с Прочее на Прочее: {prochee1}\n    """
                nach_per_history.prochee1 += prochee1
                nach_per_history.prochee2 += prochee1

        if dop_uslugi1CheckBox:
            mes += f'Доп. услуг: {dop_uslugi1}, '
            if dop_uslugi1 > 0:
                nach1.dop_uslugi -= dop_uslugi1
                nach2.dop_uslugi += dop_uslugi1
                user1.b_dop_uslugi += dop_uslugi1
                user2.b_dop_uslugi -= dop_uslugi1
                comm += f"""с Доп. услуг на Доп. услуг: {dop_uslugi1}\n    """
                nach_per_history.dop_uslugi1 += dop_uslugi1
                nach_per_history.dop_uslugi2 += dop_uslugi1

        if internet1CheckBox:
            mes += f'Интернет {internet1}, '
            if internet1 > 0:
                nach1.internet -= internet1
                nach2.internet += internet1
                user1.b_internet += internet1
                user2.b_internet -= internet1
                comm += f"""с Интернет на Интернет: {internet1}\n    """
                nach_per_history.internet1 += internet1
                nach_per_history.internet2 += internet1

        if alem1CheckBox:
            mes += f'Alem {alem1}, '
            if alem1 > 0:
                nach1.alem -= alem1
                nach2.alem += alem1
                user1.b_alem += alem1
                user2.b_alem -= alem1
                comm += f"""с Alem на Alem: {alem1}\n    """
                nach_per_history.alem1 += alem1
                nach_per_history.alem2 += alem1

        if kabel1CheckBox:
            mes += f'Кабель {kabel1}. '
            if kabel1 > 0:
                nach1_k.nach -= kabel1
                nach2_k.nach += kabel1
                user1k.balance += kabel1
                user2k.balance -= kabel1
                comm += f"""с Кабель на Кабель: {kabel1}\n    """
                nach_per_history.kabel1 += kabel1
                nach_per_history.kabel2 += kabel1

        if telefon1CheckBox or slr1CheckBox or kod1CheckBox or zakaz1CheckBox or prochee1CheckBox or dop_uslugi1CheckBox or internet1CheckBox or alem1CheckBox or kabel1CheckBox:
            nach_per_history.comment = f"""{comm}Комментарий: {comment}"""
            nach_per_history.save()
            if telefon1CheckBox or slr1CheckBox or kod1CheckBox or zakaz1CheckBox or prochee1CheckBox or dop_uslugi1CheckBox or internet1CheckBox or alem1CheckBox:
                nach1.save()
                nach2.save()
                user1.save()
                user2.save()
                context['user1_n'] = nach1
                context['user2_n'] = nach2

                context['user1'] = user1
                context['user2'] = user2

                total_telefoniya_balance1 = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                context['total_telefoniya_balance1'] = total_telefoniya_balance1

                total_telefoniya_balance2 = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
                context['total_telefoniya_balance2'] = total_telefoniya_balance2

            if kabel1CheckBox:
                nach1_k.save()
                nach2_k.save()
                user1k.save()
                user2k.save()
                context['user1k_n'] = nach1_k
                context['user2k_n'] = nach2_k
                context['user1k'] = user1k
                context['user2k'] = user2k

            messages.success(request, f'{mes} за {year1}-{month1}')
        else:
            messages.error(request, f'Выберите что перекинуть')





        

        # ic(telefon1, telefon1CheckBox)
        # ic(slr1, slr1CheckBox)
        # ic(kod1, kod1CheckBox)
        # ic(zakaz1, zakaz1CheckBox)
        # ic(prochee1, prochee1CheckBox)
        # ic(dop_uslugi1, dop_uslugi1CheckBox)
        # ic(internet1, internet1CheckBox)
        # ic(alem1, alem1CheckBox)
        # ic(kabel1, kabel1CheckBox)


            



    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidkaNachisleniya.html', context)