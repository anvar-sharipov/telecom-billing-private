from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from datetime import datetime
from telekom.models import *
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from django.db import transaction
import logging
logger = logging.getLogger(__name__)




def perekidka_new(request):
# get
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']

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

    
    context['perekidka_new'] = True
    if request_user_type == 'MTB':
        context['matbIndex'] = True 
        context['request_user_etrap'] = request_user_etrap 

    etrap1 = request.GET.get('etrap1')
    number1 = request.GET.get('number1')
    etrap2 = request.GET.get('etrap2')
    number2 = request.GET.get('number2')

    # abonent1_perekidka_info_new = PerekidkaInfoNew.objects.filter(user1Number=number1, user1Etrap=etrap1)
    if len(str(number1)) > 4 and len(str(number1)) < 7:
        abonent1_perekidka_info_new = PerekidkaInfoNew.objects.filter(
            Q(user1Number=number1, user1Etrap=etrap1) |
            Q(user1KabelNumber=number1, type_perekidka='перекидка баланса')
        ).order_by('-date')
        kabel1_perekidka_info_new = PerekidkaInfoNew.objects.filter(user1KabelNumber=number1).exclude(type_perekidka='перекидка баланса').order_by('-date')
        context['abonent1_perekidka_info_new'] = abonent1_perekidka_info_new
        context['kabel1_perekidka_info_new'] = kabel1_perekidka_info_new
    

    

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
        return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)

    context['etrap1'] = etrap1
    context['number1'] = number1
    context['etrap2'] = etrap2
    context['number2'] = number2
    context['selected_etrap1'] = etrap1
    context['selected_etrap2'] = etrap2

    # search PaysWithComment
    pays_with_comment = PaysWithComment.objects.filter(etrap=etrap1, number=number1)
    context['pays_with_comment'] = pays_with_comment
    # search PaysWithComment END
    if number1:
        if len(number1) < 6:
            try:
                user1 = UserTable.objects.get(etrap=etrap1, number=number1)
            except:
                user1 = False
        else:
            user1 = False
    else:
        user1 = False
    if number2:
        if len(number2) < 6:
            try:
                user2 = UserTable.objects.get(etrap=etrap2, number=number2)
            except:
                user2 = False
        else:
            user2 = False
    else:
        user2 = False
    if etrap1 == 'Dashoguz':
        try:
            user1Kabel = KabelTvNew.objects.get(number=number1)
        except:
            user1Kabel = False

        try:
            user2Kabel = KabelTvNew.objects.get(number=number2)
        except:
            user2Kabel = False
        context['user2Kabel'] = user2Kabel
        context['user1Kabel'] = user1Kabel
    else:
        user1Kabel = False
        user2Kabel = False

    context['user1'] = user1
    context['user2'] = user2
    
    if user1:
        context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    if user2:
        context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
# get
    #################################################################################################################################################################
    #######################################################################################################################################################
    # Перекидка только баланс START
    if request.method == 'POST' and 'perekidkaBalance' in request.POST:
        try:
            with transaction.atomic():
                priceTel = float(request.POST.get('priceTel')) if request.POST.get('priceTel') not in ['', None] else 0
                priceInt = float(request.POST.get('priceInt')) if request.POST.get('priceInt') not in ['', None] else 0
                priceAlem = float(request.POST.get('priceAlem')) if request.POST.get('priceAlem') not in ['', None] else 0
                priceKabel = float(request.POST.get('priceKabel')) if request.POST.get('priceKabel') not in ['', None] else 0
                user2_column_telefoniya = request.POST.get('user2_column_telefoniya')
                user2_column_internet = request.POST.get('user2_column_internet')
                user2_column_alem = request.POST.get('user2_column_alem')
                user2_column_kabel = request.POST.get('user2_column_kabel')
                comment = request.POST.get('comment')

                if not user1Kabel and not user1 and not user2 and not user2Kabel:
                    # false false false false
                    messages.error(request, 'Введите корректные данные')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                elif not user1Kabel and not user1 and not user2 and user2Kabel:
                    # false false false true
                    messages.error(request, 'Введите корректные данные')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                elif not user1Kabel and not user1 and user2 and not user2Kabel:
                    # false false true false
                    messages.error(request, 'Введите корректные данные')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                elif not user1Kabel and not user1 and user2 and user2Kabel:
                    # false false true true
                    messages.error(request, 'Введите корректные данные')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                elif not user1Kabel and user1 and not user2 and not user2Kabel:
                    # false true false false
                    messages.error(request, 'Введите корректные данные')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                elif not user1Kabel and user1 and not user2 and user2Kabel:
                    # false true false true
                    per_info = PerekidkaInfoNew(
                        user1Number = user1.number,
                        user1Etrap = user1.etrap,
                        user1NameSurname = f"{user1.surname} {user1.name}",

                        user2KabelNumber = user2Kabel.number,
                        user2KabelNameSurname = f"{user2Kabel.surname} {user2Kabel.name}",

                        operator = request.user.username,
                        type_perekidka = 'перекидка баланса',
                    )
                elif not user1Kabel and user1 and user2 and not user2Kabel:
                    # false true true false
                    per_info = PerekidkaInfoNew(
                        user1Number = user1.number,
                        user1Etrap = user1.etrap,
                        user1NameSurname = f"{user1.surname} {user1.name}",

                        user2Number = user2.number,
                        user2Etrap = user2.etrap,
                        user2NameSurname = f"{user2.surname} {user2.name}",

                        operator = request.user.username,
                        type_perekidka = 'перекидка баланса',
                    )
                elif not user1Kabel and user1 and user2 and user2Kabel:
                    # false true true true
                    per_info = PerekidkaInfoNew(
                        user1Number = user1.number,
                        user1Etrap = user1.etrap,
                        user1NameSurname = f"{user1.surname} {user1.name}",

                        user2Number = user2.number,
                        user2Etrap = user2.etrap,
                        user2NameSurname = f"{user2.surname} {user2.name}",

                        user2KabelNumber = user2Kabel.number,
                        user2KabelNameSurname = f"{user2Kabel.surname} {user2Kabel.name}",

                        operator = request.user.username,
                        type_perekidka = 'перекидка баланса',
                    )
                elif user1Kabel and not user1 and not user2 and not user2Kabel:
                    # true false false false
                    messages.error(request, 'Введите корректные данные')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                elif user1Kabel and not user1 and not user2 and user2Kabel:
                    # true false false true
                    per_info = PerekidkaInfoNew(
                        user1KabelNumber = user1Kabel.number,
                        user1KabelNameSurname = f"{user1Kabel.surname} {user1Kabel.name}",
            
                        user2KabelNumber = user2Kabel.number,
                        user2KabelNameSurname = f"{user2Kabel.surname} {user2Kabel.name}",

                        operator = request.user.username,
                        type_perekidka = 'перекидка баланса',
                    )
                elif user1Kabel and not user1 and user2 and not user2Kabel:
                    # true false true false
                    per_info = PerekidkaInfoNew(
                        user1KabelNumber = user1Kabel.number,
                        user1KabelNameSurname = f"{user1Kabel.surname} {user1Kabel.name}",

                        user2Number = user2.number,
                        user2Etrap = user2.etrap,
                        user2NameSurname = f"{user2.surname} {user2.name}",

                        operator = request.user.username,
                        type_perekidka = 'перекидка баланса',
                    )
                elif user1Kabel and not user1 and user2 and user2Kabel:
                    # true false true true
                    per_info = PerekidkaInfoNew(
                        user1KabelNumber = user1Kabel.number,
                        user1KabelNameSurname = f"{user1Kabel.surname} {user1Kabel.name}",

                        user2Number = user2.number,
                        user2Etrap = user2.etrap,
                        user2NameSurname = f"{user2.surname} {user2.name}",

                        user2KabelNumber = user2Kabel.number,
                        user2KabelNameSurname = f"{user2Kabel.surname} {user2Kabel.name}",

                        operator = request.user.username,
                        type_perekidka = 'перекидка баланса',
                    )
                elif user1Kabel and user1 and not user2 and not user2Kabel:
                    # true true false false
                    messages.error(request, 'Введите корректные данные')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                elif user1Kabel and user1 and not user2 and user2Kabel:
                    # true true false true
                    per_info = PerekidkaInfoNew(
                        user1KabelNumber = user1Kabel.number,
                        user1KabelNameSurname = f"{user1Kabel.surname} {user1Kabel.name}",

                        user1Number = user1.number,
                        user1Etrap = user1.etrap,
                        user1NameSurname = f"{user1.surname} {user1.name}",

                        user2KabelNumber = user2Kabel.number,
                        user2KabelNameSurname = f"{user2Kabel.surname} {user2Kabel.name}",

                        operator = request.user.username,
                        type_perekidka = 'перекидка баланса',
                    )
                elif user1Kabel and user1 and user2 and not user2Kabel:
                    # true true true false
                    per_info = PerekidkaInfoNew(
                        user1KabelNumber = user1Kabel.number,
                        user1KabelNameSurname = f"{user1Kabel.surname} {user1Kabel.name}",

                        user1Number = user1.number,
                        user1Etrap = user1.etrap,
                        user1NameSurname = f"{user1.surname} {user1.name}",

                        user2Number = user2.number,
                        user2Etrap = user2.etrap,
                        user2NameSurname = f"{user2.surname} {user2.name}",

                        operator = request.user.username,
                        type_perekidka = 'перекидка баланса',
                    )
                elif user1Kabel and user1 and user2 and user2Kabel:
                    # true true true true
                    per_info = PerekidkaInfoNew(
                        user1KabelNumber = user1Kabel.number,
                        user1KabelNameSurname = f"{user1Kabel.surname} {user1Kabel.name}",

                        user1Number = user1.number,
                        user1Etrap = user1.etrap,
                        user1NameSurname = f"{user1.surname} {user1.name}",

                        user2Number = user2.number,
                        user2Etrap = user2.etrap,
                        user2NameSurname = f"{user2.surname} {user2.name}",

                        user2KabelNumber = user2Kabel.number,
                        user2KabelNameSurname = f"{user2Kabel.surname} {user2Kabel.name}",

                        operator = request.user.username,
                        type_perekidka = 'перекидка баланса',
                    )
                
                mess = f"""Перекинуто с {number1} на {number2}:
            """
                mess_kabel = f''

                ##################################################################################################################################################################
                ########################################################################################################################################################
                if not user1Kabel and not user1 and not user2 and not user2Kabel:
                    # false false false false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    pass
                elif not user1Kabel and not user1 and not user2 and user2Kabel:
                    # false false false true ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    pass
                elif not user1Kabel and not user1 and user2 and not user2Kabel:
                    # false false true false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    pass
                elif not user1Kabel and not user1 and user2 and user2Kabel:
                    # false false true true ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    pass
                elif not user1Kabel and user1 and not user2 and not user2Kabel:
                    # false true false false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    pass
                elif not user1Kabel and user1 and not user2 and user2Kabel:
                    # false true false true ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    ic('Перекидка баланса разные номера')
                    if priceTel != 0:
                        totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                        per_info.telefon1 += priceTel
                        user1.b_telefon = 0
                        user1.b_slr = 0
                        user1.b_kod = 0
                        user1.b_zakaz = 0
                        user1.b_dop_uslugi = 0
                        user1.b_prochee = totalTelefoniya - priceTel
                        if user2_column_telefoniya == 'kabel' and user2Kabel:
                            per_info.kabel2 += priceTel
                            user2Kabel.balance += priceTel
                            mess += f"""c телефония на kabel: {priceTel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c Телефония на кабель: {priceTel} manat
            """
                            else:
                                mess_kabel += f"""c Телефония на кабель: {priceTel} manat
            """
                    if priceInt != 0:
                        per_info.internet1 += priceInt
                        user1.b_internet -= priceInt
                        if user2_column_internet == 'kabel' and user2Kabel:
                            per_info.kabel2 += priceInt
                            user2Kabel.balance += priceInt
                            mess += f"""c internet на kabel: {priceInt} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c Интернет на кабель: {priceInt} manat
            """
                            else:
                                mess_kabel += f"""c Интернет на кабель: {priceInt} manat
            """
                    if priceAlem != 0:
                        per_info.alem1 += priceAlem
                        user1.b_alem -= priceAlem
                        if user2_column_alem == 'kabel' and user2Kabel:
                            per_info.kabel2 += priceAlem
                            user2Kabel.balance += priceAlem
                            mess += f"""c alem на kabel: {priceAlem} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c алем на кабель: {priceAlem} manat
            """
                            else:
                                mess_kabel += f"""c алем на кабель: {priceAlem} manat
            """      
                    if priceTel != 0 or priceInt != 0 or priceAlem != 0:
                        mess += comment
                        per_info.comment = mess
                        per_info.save()
                        if user1:
                            user1.save()
                            context['user1'] = user1
                            context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                        if user2:
                            user2.save()
                            context['user2'] = user2
                            context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
                        if user2Kabel:
                            user2Kabel.save()
                            context['user2Kabel'] = user2Kabel
                        if mess_kabel != '':
                            KabelComment.objects.create(
                                user = user2Kabel,
                                worker = request.user.username,
                                action = 'Изменения данных',
                                perekidka_info_new_pk = per_info.pk,
                                comment = f"""{mess_kabel}
            Комментарий: {comment}
            """)
                        messages.success(request, 'Успешная перекидка баланса')
                    else:
                        messages.error(request, 'Все цены перекидки 0')
                elif not user1Kabel and user1 and user2 and not user2Kabel:
                    # false true true false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    if number1 == number2:
                        ic('perekidka один и тот же номер')
                        if priceTel != 0:
                            totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                            per_info.telefon1 += priceTel
                            user1.b_telefon = 0
                            user1.b_slr = 0
                            user1.b_kod = 0
                            user1.b_zakaz = 0
                            user1.b_dop_uslugi = 0
                            user1.b_prochee = totalTelefoniya - priceTel
                            if user2_column_telefoniya == 'internet':
                                per_info.internet2 += priceTel
                                user1.b_internet += priceTel
                                mess += f"""c телефония на интернет: {priceTel} манат
            """
                            if user2_column_telefoniya == 'alem':
                                per_info.alem2 += priceTel
                                user1.b_alem += priceTel
                                mess += f"""c телефония на алем: {priceTel} манат
            """
                        # с интернета на (тут или на телефония или на алем или на кабель)
                        if priceInt != 0:
                            per_info.internet1 += priceInt
                            user1.b_internet -= priceInt
                            # Перекидываем баланс с internet на
                            if user2_column_internet == 'telefoniya':
                                # Перекидываем с internet в телефония
                                per_info.telefon2 += priceInt
                                totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                                user1.b_telefon = 0
                                user1.b_slr = 0
                                user1.b_kod = 0
                                user1.b_zakaz = 0
                                user1.b_dop_uslugi = 0
                                user1.b_prochee = totalTelefoniya + priceInt
                                mess += f"""c интернет на телефония: {priceInt} манат
            """
                            if user2_column_internet == 'alem':
                                # Перекидываем с internet в alem
                                per_info.alem2 += priceInt
                                user1.b_alem += priceInt
                                mess += f"""c интернет на алем: {priceInt} манат
            """
                        # с алем на (тут или на телефония или на интернет или на кабель)
                        if priceAlem != 0:
                            per_info.alem1 += priceAlem
                            user1.b_alem -= priceAlem
                            if user2_column_alem == 'telefoniya':
                                per_info.telefon2 += priceAlem
                                totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                                user1.b_telefon = 0
                                user1.b_slr = 0
                                user1.b_kod = 0
                                user1.b_zakaz = 0
                                user1.b_dop_uslugi = 0
                                user1.b_prochee = totalTelefoniya + priceAlem
                                mess += f"""c alem на телефония: {priceAlem} манат
            """
                            if user2_column_alem == 'internet':
                                per_info.internet2 += priceAlem
                                user1.b_internet += priceAlem
                                mess += f"""c alem на интернет: {priceAlem} манат
            """
                        if priceTel != 0 or priceInt != 0 or priceAlem != 0:
                            mess += comment
                            per_info.comment = mess
                            per_info.save()
                            if user1:
                                user1.save()
                                context['user1'] = user1
                                context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                            messages.success(request, 'Успешная перекидка баланса')
                        else:
                            messages.error(request, 'Все цены перекидки 0')
                    else:
                        ic('Перекидка баланса разные номера')
                        if priceTel != 0:
                            totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                            per_info.telefon1 += priceTel
                            user1.b_telefon = 0
                            user1.b_slr = 0
                            user1.b_kod = 0
                            user1.b_zakaz = 0
                            user1.b_dop_uslugi = 0
                            user1.b_prochee = totalTelefoniya - priceTel
                            if user2_column_telefoniya == 'telefoniya':
                                per_info.telefon2 += priceTel
                                user2.b_prochee += priceTel
                                mess += f"""c телефония на телефония: {priceTel} манат
            """             
                            if user2_column_telefoniya == 'internet':
                                per_info.internet2 += priceTel
                                user2.b_internet += priceTel
                                mess += f"""c телефония на internet: {priceTel} манат
            """
                            if user2_column_telefoniya == 'alem':
                                per_info.alem2 += priceTel
                                user2.b_alem += priceTel
                                mess += f"""c телефония на alem: {priceTel} манат
            """
                        if priceInt != 0:
                            per_info.internet1 += priceInt
                            user1.b_internet -= priceInt
                            if user2_column_internet == 'telefoniya':
                                per_info.telefon2 += priceInt
                                user2.b_prochee += priceInt
                                mess += f"""c internet на телефония: {priceInt} манат
            """
                            if user2_column_internet == 'internet':
                                per_info.internet2 += priceInt
                                user2.b_internet += priceInt
                                mess += f"""c internet на internet: {priceInt} манат
            """
                            if user2_column_internet == 'alem':
                                per_info.alem2 += priceInt
                                user2.b_alem += priceInt
                                mess += f"""c internet на alem: {priceInt} манат
            """
                        if priceAlem != 0:
                            per_info.alem1 += priceAlem
                            user1.b_alem -= priceAlem
                            if user2_column_alem == 'telefoniya':
                                per_info.telefon2 += priceAlem
                                user2.b_prochee += priceAlem
                                mess += f"""c alem на телефония: {priceAlem} манат
            """
                            if user2_column_alem == 'internet':
                                per_info.internet2 += priceAlem
                                user2.b_internet += priceAlem
                                mess += f"""c alem на internet: {priceAlem} манат
            """
                            if user2_column_alem == 'alem':
                                per_info.alem2 += priceAlem
                                user2.b_alem += priceAlem
                                mess += f"""c alem на alem: {priceAlem} манат
            """           
                        if priceTel != 0 or priceInt != 0 or priceAlem != 0:
                            mess += comment
                            per_info.comment = mess
                            per_info.save()
                            if user1:
                                user1.save()
                                context['user1'] = user1
                                context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                            if user2:
                                user2.save()
                                context['user2'] = user2
                                context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
                            messages.success(request, 'Успешная перекидка баланса')
                        else:
                            messages.error(request, 'Все цены перекидки 0')

                elif not user1Kabel and user1 and user2 and user2Kabel:
                    # false true true true (Тут не возможен вариант когда 2 номера одинаковые но у одного баланса кабель нет а у другого есть, поэтому в таких ситуациях один и тот же номер не возможен) ----------------------------
                    ic('Перекидка баланса разные номера')
                    if priceTel != 0:
                        totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                        per_info.telefon1 += priceTel
                        user1.b_telefon = 0
                        user1.b_slr = 0
                        user1.b_kod = 0
                        user1.b_zakaz = 0
                        user1.b_dop_uslugi = 0
                        user1.b_prochee = totalTelefoniya - priceTel
                        if user2_column_telefoniya == 'telefoniya':
                            per_info.telefon2 += priceTel
                            user2.b_prochee += priceTel
                            mess += f"""c телефония на телефония: {priceTel} манат
            """             
                        if user2_column_telefoniya == 'internet':
                            per_info.internet2 += priceTel
                            user2.b_internet += priceTel
                            mess += f"""c телефония на internet: {priceTel} манат
            """
                        if user2_column_telefoniya == 'alem':
                            per_info.alem2 += priceTel
                            user2.b_alem += priceTel
                            mess += f"""c телефония на alem: {priceTel} манат
            """
                        if user2_column_telefoniya == 'kabel' and user2Kabel:
                            per_info.kabel2 += priceTel
                            user2Kabel.balance += priceTel
                            mess += f"""c телефония на kabel: {priceTel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c Телефония на кабель: {priceTel} manat
            """
                            else:
                                mess_kabel += f"""c Телефония на кабель: {priceTel} manat
            """
                    if priceInt != 0:
                        per_info.internet1 += priceInt
                        user1.b_internet -= priceInt
                        if user2_column_internet == 'telefoniya':
                            per_info.telefon2 += priceInt
                            user2.b_prochee += priceInt
                            mess += f"""c internet на телефония: {priceInt} манат
            """
                        if user2_column_internet == 'internet':
                            per_info.internet2 += priceInt
                            user2.b_internet += priceInt
                            mess += f"""c internet на internet: {priceInt} манат
            """
                        if user2_column_internet == 'alem':
                            per_info.alem2 += priceInt
                            user2.b_alem += priceInt
                            mess += f"""c internet на alem: {priceInt} манат
            """
                        if user2_column_internet == 'kabel' and user2Kabel:
                            per_info.kabel2 += priceInt
                            user2Kabel.balance += priceInt
                            mess += f"""c internet на kabel: {priceInt} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c Интернет на кабель: {priceInt} manat
            """
                            else:
                                mess_kabel += f"""c Интернет на кабель: {priceInt} manat
            """
                    if priceAlem != 0:
                        per_info.alem1 += priceAlem
                        user1.b_alem -= priceAlem
                        if user2_column_alem == 'telefoniya':
                            per_info.telefon2 += priceAlem
                            user2.b_prochee += priceAlem
                            mess += f"""c alem на телефония: {priceAlem} манат
            """
                        if user2_column_alem == 'internet':
                            per_info.internet2 += priceAlem
                            user2.b_internet += priceAlem
                            mess += f"""c alem на internet: {priceAlem} манат
            """
                        if user2_column_alem == 'alem':
                            per_info.alem2 += priceAlem
                            user2.b_alem += priceAlem
                            mess += f"""c alem на alem: {priceAlem} манат
            """
                        if user2_column_alem == 'kabel' and user2Kabel:
                            per_info.kabel2 += priceAlem
                            user2Kabel.balance += priceAlem
                            mess += f"""c alem на kabel: {priceAlem} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c алем на кабель: {priceAlem} manat
            """
                            else:
                                mess_kabel += f"""c алем на кабель: {priceAlem} manat
            """
                    if priceTel != 0 or priceInt != 0 or priceAlem != 0:
                        mess += comment
                        per_info.comment = mess
                        per_info.save()
                        if user1:
                            user1.save()
                            context['user1'] = user1
                            context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                        if user2:
                            user2.save()
                            context['user2'] = user2
                            context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
                        if user2Kabel:
                            user2Kabel.save()
                            context['user2Kabel'] = user2Kabel
                        if mess_kabel != '':
                            KabelComment.objects.create(
                                user = user2Kabel,
                                worker = request.user.username,
                                action = 'Изменения данных',
                                perekidka_info_new_pk = per_info.pk,
                                comment = f"""{mess_kabel}
            Комментарий: {comment}
            """)

                        messages.success(request, 'Успешная перекидка баланса')
                    else:
                        messages.error(request, 'Все цены перекидки 0')
                elif user1Kabel and not user1 and not user2 and not user2Kabel:
                    # true false false false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    pass
                elif user1Kabel and not user1 and not user2 and user2Kabel:
                    # true false false true (Тут нельзя никак перекинуть если кабельные один и тот же номер) ------------------------------------------------------------------------------------------------------------
                    ic('Перекидка баланса разные номера')
                    if priceKabel != 0:
                        per_info.kabel1 += priceKabel
                        user1Kabel.balance -= priceKabel
                        if user2_column_kabel == 'kabel' and user2Kabel:
                            per_info.kabel2 += priceKabel
                            user2Kabel.balance += priceKabel
                            mess += f"""c kabel на kabel: {priceKabel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на кабель: {priceKabel} manat
            """
                            else:
                                mess_kabel += f"""c кабель на кабель: {priceKabel} manat
            """
                    
                    if priceKabel != 0:
                        mess += comment
                        per_info.comment = mess
                        per_info.save()
                        if user2Kabel:
                            user2Kabel.save()
                            context['user2Kabel'] = user2Kabel
                        if user1Kabel:
                            user1Kabel.save()
                            context['user1Kabel'] = user1Kabel
                        if mess_kabel != '':
                            KabelComment.objects.create(
                                user = user1Kabel,
                                worker = request.user.username,
                                action = 'Изменения данных',
                                perekidka_info_new_pk = per_info.pk,
                                comment = f"""{mess_kabel}
            Комментарий: {comment}
            """)
                            ic('tut1')
                            KabelComment.objects.create(
                                user = user2Kabel,
                                worker = request.user.username,
                                action = 'Изменения данных',
                                perekidka_info_new_pk = per_info.pk,
                                comment = f"""{mess_kabel}
            Комментарий: {comment}
            """)

                        messages.success(request, 'Успешная перекидка баланса')
                    else:
                        messages.error(request, 'Все цены перекидки 0')
                elif user1Kabel and not user1 and user2 and not user2Kabel:
                    # true false true false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    ic('Перекидка баланса разные номера')
                    if priceKabel != 0:
                        per_info.kabel1 += priceKabel
                        user1Kabel.balance -= priceKabel
                        if user2_column_kabel == 'telefoniya':
                            per_info.telefon2 += priceKabel
                            user2.b_prochee += priceKabel
                            mess += f"""c kabel на телефония: {priceKabel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на телефония: {priceKabel} manat
            """
                            else:
                                mess_kabel += f"""c кабель на телефония: {priceKabel} manat
            """
                        if user2_column_kabel == 'internet':
                            per_info.internet2 += priceKabel
                            user2.b_internet += priceKabel
                            mess += f"""c kabel на internet: {priceKabel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на интернет: {priceKabel} manat
            """
                            else:
                                mess_kabel += f"""c кабель на интернет: {priceKabel} manat
            """
                        if user2_column_kabel == 'alem':
                            per_info.alem2 += priceKabel
                            user2.b_alem += priceKabel
                            mess += f"""c kabel на alem: {priceKabel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на алем: {priceKabel} manat
            """
                            else:
                                mess_kabel += f"""c кабель на алем: {priceKabel} manat
            """
                    
                    if priceKabel != 0:
                        mess += comment
                        per_info.comment = mess
                        per_info.save()
                        if user2:
                            user2.save()
                            context['user2'] = user2
                            context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
                        if user1Kabel:
                            user1Kabel.save()
                            context['user1Kabel'] = user1Kabel
                        if mess_kabel != '':
                            KabelComment.objects.create(
                                user = user1Kabel,
                                worker = request.user.username,
                                action = 'Изменения данных',
                                perekidka_info_new_pk = per_info.pk,
                                comment = f"""{mess_kabel}
            Комментарий: {comment}
            """)
                        messages.success(request, 'Успешная перекидка баланса')
                    else:
                        messages.error(request, 'Все цены перекидки 0')
                elif user1Kabel and not user1 and user2 and user2Kabel:
                    # true false true true ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    ic('Перекидка баланса разные номера')
                    if priceKabel != 0:
                        per_info.kabel1 += priceKabel
                        user1Kabel.balance -= priceKabel
                        if user2_column_kabel == 'telefoniya':
                            per_info.telefon2 += priceKabel
                            user2.b_prochee += priceKabel
                            mess += f"""c kabel на телефония: {priceKabel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на телефония: {priceKabel} manat
            """
                            else:
                                mess_kabel += f"""c кабель на телефония: {priceKabel} manat
            """
                        if user2_column_kabel == 'internet':
                            per_info.internet2 += priceKabel
                            user2.b_internet += priceKabel
                            mess += f"""c kabel на internet: {priceKabel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на интернет: {priceKabel} manat
            """
                            else:
                                mess_kabel += f"""c кабель на интернет: {priceKabel} manat
            """
                        if user2_column_kabel == 'alem':
                            per_info.alem2 += priceKabel
                            user2.b_alem += priceKabel
                            mess += f"""c kabel на alem: {priceKabel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на алем: {priceKabel} manat
            """
                            else:
                                mess_kabel += f"""c кабель на алем: {priceKabel} manat
            """
                        if user2_column_kabel == 'kabel' and user2Kabel:
                            per_info.kabel2 += priceKabel
                            user2Kabel.balance += priceKabel
                            mess += f"""c kabel на kabel: {priceKabel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на кабель: {priceKabel} manat
            """
                            else:
                                mess_kabel += f"""c кабель на кабель: {priceKabel} manat
            """
                    
                    if priceKabel != 0:
                        mess += comment
                        per_info.comment = mess
                        per_info.save()
                        if user2:
                            user2.save()
                            context['user2'] = user2
                            context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
                        if user2Kabel:
                            user2Kabel.save()
                            context['user2Kabel'] = user2Kabel
                        if user1Kabel:
                            user1Kabel.save()
                            context['user1Kabel'] = user1Kabel
                        if mess_kabel != '':
                            KabelComment.objects.create(
                                user = user1Kabel,
                                worker = request.user.username,
                                action = 'Изменения данных',
                                perekidka_info_new_pk = per_info.pk,
                                comment = f"""{mess_kabel}
            Комментарий: {comment}
            """)
                            KabelComment.objects.create(
                                user = user2Kabel,
                                worker = request.user.username,
                                action = 'Изменения данных',
                                perekidka_info_new_pk = per_info.pk,
                                comment = f"""{mess_kabel}
            Комментарий: {comment}
            """)

                        messages.success(request, 'Успешная перекидка баланса')
                    else:
                        messages.error(request, 'Все цены перекидки 0')
                elif user1Kabel and user1 and not user2 and not user2Kabel:
                    # true true false false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    pass
                elif user1Kabel and user1 and not user2 and user2Kabel:
                    # true true false true ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    ic('Перекидка баланса разные номера')
                    if priceTel != 0:
                        totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                        per_info.telefon1 += priceTel
                        user1.b_telefon = 0
                        user1.b_slr = 0
                        user1.b_kod = 0
                        user1.b_zakaz = 0
                        user1.b_dop_uslugi = 0
                        user1.b_prochee = totalTelefoniya - priceTel
                        if user2_column_telefoniya == 'kabel' and user2Kabel:
                            per_info.kabel2 += priceTel
                            user2Kabel.balance += priceTel
                            mess += f"""c телефония на kabel: {priceTel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c Телефония на кабель: {priceTel} manat
            """
                            else:
                                mess_kabel += f"""c Телефония на кабель: {priceTel} manat
            """
                    if priceInt != 0:
                        per_info.internet1 += priceInt
                        user1.b_internet -= priceInt
                        if user2_column_internet == 'kabel' and user2Kabel:
                            per_info.kabel2 += priceInt
                            user2Kabel.balance += priceInt
                            mess += f"""c internet на kabel: {priceInt} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c Интернет на кабель: {priceInt} manat
            """
                            else:
                                mess_kabel += f"""c Интернет на кабель: {priceInt} manat
            """
                    if priceAlem != 0:
                        per_info.alem1 += priceAlem
                        user1.b_alem -= priceAlem
                        if user2_column_alem == 'kabel' and user2Kabel:
                            per_info.kabel2 += priceAlem
                            user2Kabel.balance += priceAlem
                            mess += f"""c alem на kabel: {priceAlem} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c алем на кабель: {priceAlem} manat
            """
                            else:
                                mess_kabel += f"""c алем на кабель: {priceAlem} manat
            """
                    if priceKabel != 0:
                        per_info.kabel1 += priceKabel
                        user1Kabel.balance -= priceKabel
                        if user2_column_kabel == 'alem':
                            per_info.alem2 += priceKabel
                            user2.b_alem += priceKabel
                            mess += f"""c kabel на alem: {priceKabel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на алем: {priceKabel} manat
            """
                            else:
                                mess_kabel += f"""c кабель на алем: {priceKabel} manat
            """
                        if user2_column_kabel == 'kabel' and user2Kabel:
                            per_info.kabel2 += priceKabel
                            user2Kabel.balance += priceKabel
                            mess += f"""c kabel на kabel: {priceKabel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на кабель: {priceKabel} manat
            """
                            else:
                                mess_kabel += f"""c кабель на кабель: {priceKabel} manat
            """
                    
                    if priceTel != 0 or priceInt != 0 or priceAlem != 0 or priceKabel != 0:
                        mess += comment
                        per_info.comment = mess
                        per_info.save()
                        if user1:
                            user1.save()
                            context['user1'] = user1
                            context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                        if user2:
                            user2.save()
                            context['user2'] = user2
                            context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
                        if user2Kabel:
                            user2Kabel.save()
                            context['user2Kabel'] = user2Kabel
                        if user1Kabel:
                            user1Kabel.save()
                            context['user1Kabel'] = user1Kabel
                        if mess_kabel != '':
                            KabelComment.objects.create(
                                user = user1Kabel,
                                worker = request.user.username,
                                action = 'Изменения данных',
                                perekidka_info_new_pk = per_info.pk,
                                comment = f"""{mess_kabel}
            Комментарий: {comment}
            """)
                            KabelComment.objects.create(
                                user = user2Kabel,
                                worker = request.user.username,
                                action = 'Изменения данных',
                                perekidka_info_new_pk = per_info.pk,
                                comment = f"""{mess_kabel}
            Комментарий: {comment}
            """)

                        messages.success(request, 'Успешная перекидка баланса')
                    else:
                        messages.error(request, 'Все цены перекидки 0')
                elif user1Kabel and user1 and user2 and not user2Kabel:
                    # true true true false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                    ic('Перекидка баланса разные номера')
                    if priceTel != 0:
                        totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                        per_info.telefon1 += priceTel
                        user1.b_telefon = 0
                        user1.b_slr = 0
                        user1.b_kod = 0
                        user1.b_zakaz = 0
                        user1.b_dop_uslugi = 0
                        user1.b_prochee = totalTelefoniya - priceTel
                        if user2_column_telefoniya == 'telefoniya':
                            per_info.telefon2 += priceTel
                            user2.b_prochee += priceTel
                            mess += f"""c телефония на телефония: {priceTel} манат
            """             
                        if user2_column_telefoniya == 'internet':
                            per_info.internet2 += priceTel
                            user2.b_internet += priceTel
                            mess += f"""c телефония на internet: {priceTel} манат
            """
                        if user2_column_telefoniya == 'alem':
                            per_info.alem2 += priceTel
                            user2.b_alem += priceTel
                            mess += f"""c телефония на alem: {priceTel} манат
            """
                    if priceInt != 0:
                        per_info.internet1 += priceInt
                        user1.b_internet -= priceInt
                        if user2_column_internet == 'telefoniya':
                            per_info.telefon2 += priceInt
                            user2.b_prochee += priceInt
                            mess += f"""c internet на телефония: {priceInt} манат
            """
                        if user2_column_internet == 'internet':
                            per_info.internet2 += priceInt
                            user2.b_internet += priceInt
                            mess += f"""c internet на internet: {priceInt} манат
            """
                        if user2_column_internet == 'alem':
                            per_info.alem2 += priceInt
                            user2.b_alem += priceInt
                            mess += f"""c internet на alem: {priceInt} манат
            """
                    if priceAlem != 0:
                        per_info.alem1 += priceAlem
                        user1.b_alem -= priceAlem
                        if user2_column_alem == 'telefoniya':
                            per_info.telefon2 += priceAlem
                            user2.b_prochee += priceAlem
                            mess += f"""c alem на телефония: {priceAlem} манат
            """
                        if user2_column_alem == 'internet':
                            per_info.internet2 += priceAlem
                            user2.b_internet += priceAlem
                            mess += f"""c alem на internet: {priceAlem} манат
            """
                        if user2_column_alem == 'alem':
                            per_info.alem2 += priceAlem
                            user2.b_alem += priceAlem
                            mess += f"""c alem на alem: {priceAlem} манат
            """
                    if priceKabel != 0:
                        per_info.kabel1 += priceKabel
                        user1Kabel.balance -= priceKabel
                        if user2_column_kabel == 'telefoniya':
                            per_info.telefon2 += priceKabel
                            user2.b_prochee += priceKabel
                            mess += f"""c kabel на телефония: {priceKabel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на телефония: {priceKabel} manat
            """
                            else:
                                mess_kabel += f"""c кабель на телефония: {priceKabel} manat
            """
                        if user2_column_kabel == 'internet':
                            per_info.internet2 += priceKabel
                            user2.b_internet += priceKabel
                            mess += f"""c kabel на internet: {priceKabel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на интернет: {priceKabel} manat
            """
                            else:
                                mess_kabel += f"""c кабель на интернет: {priceKabel} manat
            """
                        if user2_column_kabel == 'alem':
                            per_info.alem2 += priceKabel
                            user2.b_alem += priceKabel
                            mess += f"""c kabel на alem: {priceKabel} манат
            """
                            if mess_kabel == '':
                                mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на алем: {priceKabel} manat
            """
                            else:
                                mess_kabel += f"""c кабель на алем: {priceKabel} manat
            """         
                    if priceTel != 0 or priceInt != 0 or priceAlem != 0 or priceKabel != 0:
                        mess += comment
                        per_info.comment = mess
                        per_info.save()
                        if user1:
                            user1.save()
                            context['user1'] = user1
                            context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                        if user2:
                            user2.save()
                            context['user2'] = user2
                            context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
                        if user1Kabel:
                            user1Kabel.save()
                            context['user1Kabel'] = user1Kabel
                        if mess_kabel != '':
                            KabelComment.objects.create(
                                user = user1Kabel,
                                worker = request.user.username,
                                action = 'Изменения данных',
                                perekidka_info_new_pk = per_info.pk,
                                comment = f"""{mess_kabel}
            Комментарий: {comment}
            """)
                        messages.success(request, 'Успешная перекидка баланса')
                    else:
                        messages.error(request, 'Все цены перекидки 0')
                elif user1Kabel and user1 and user2 and user2Kabel:
                    # true true true true ------------------------------------------------------------------------------------------------------------------------------------------------------------------------           
                    if number1 == number2:
                        ic('perekidka один и тот же номер')
                        if priceTel != 0:
                            totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                            per_info.telefon1 += priceTel
                            user1.b_telefon = 0
                            user1.b_slr = 0
                            user1.b_kod = 0
                            user1.b_zakaz = 0
                            user1.b_dop_uslugi = 0
                            user1.b_prochee = totalTelefoniya - priceTel
                            if user2_column_telefoniya == 'internet':
                                per_info.internet2 += priceTel
                                user1.b_internet += priceTel
                                mess += f"""c телефония на интернет: {priceTel} манат
            """
                            if user2_column_telefoniya == 'alem':
                                per_info.alem2 += priceTel
                                user1.b_alem += priceTel
                                mess += f"""c телефония на алем: {priceTel} манат
            """
                            if user2_column_telefoniya == 'kabel' and user1Kabel:
                                if mess_kabel == '':
                                    mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c телефония на кабель: {priceTel} manat
            """
                                else:
                                    mess_kabel += f"""c телефония на кабель: {priceTel} manat
            """
                                per_info.kabel2 += priceTel
                                user1Kabel.balance += priceTel
                                mess += f"""c телефония на кабель: {priceTel} манат
            """
                        # с интернета на (тут или на телефония или на алем или на кабель)
                        if priceInt != 0:
                            per_info.internet1 += priceInt
                            user1.b_internet -= priceInt
                            # Перекидываем баланс с internet на
                            if user2_column_internet == 'telefoniya':
                                # Перекидываем с internet в телефония
                                per_info.telefon2 += priceInt
                                totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                                user1.b_telefon = 0
                                user1.b_slr = 0
                                user1.b_kod = 0
                                user1.b_zakaz = 0
                                user1.b_dop_uslugi = 0
                                user1.b_prochee = totalTelefoniya + priceInt
                                mess += f"""c интернет на телефония: {priceInt} манат
            """
                            if user2_column_internet == 'alem':
                                # Перекидываем с internet в alem
                                per_info.alem2 += priceInt
                                user1.b_alem += priceInt
                                mess += f"""c интернет на алем: {priceInt} манат
            """
                            if user2_column_internet == 'kabel' and user1Kabel:
                                # Перекидываем с internet в kabel
                                if mess_kabel == '':
                                    mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c интернет на кабель: {priceInt} manat
            """
                                else:
                                    mess_kabel += f"""c интернет на кабель: {priceInt} manat
            """
                                per_info.kabel2 += priceInt
                                user1Kabel.balance += priceInt
                                mess += f"""c интернет на kabel: {priceInt} манат
            """
                        # с алем на (тут или на телефония или на интернет или на кабель)
                        if priceAlem != 0:
                            per_info.alem1 += priceAlem
                            user1.b_alem -= priceAlem
                            if user2_column_alem == 'telefoniya':
                                per_info.telefon2 += priceAlem
                                totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                                user1.b_telefon = 0
                                user1.b_slr = 0
                                user1.b_kod = 0
                                user1.b_zakaz = 0
                                user1.b_dop_uslugi = 0
                                user1.b_prochee = totalTelefoniya + priceAlem
                                mess += f"""c alem на телефония: {priceAlem} манат
            """
                            if user2_column_alem == 'internet':
                                per_info.internet2 += priceAlem
                                user1.b_internet += priceAlem
                                mess += f"""c alem на интернет: {priceAlem} манат
            """
                            if user2_column_alem == 'kabel' and user1Kabel:
                                if mess_kabel == '':
                                    mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c alem на кабель: {priceAlem} manat
            """
                                else:
                                    mess_kabel += f"""c alem на кабель: {priceAlem} manat
            """
                                per_info.kabel2 += priceAlem
                                user1Kabel.balance += priceAlem
                                mess += f"""c alem на kabel: {priceAlem} манат
            """
                        if priceKabel != 0:
                            per_info.kabel1 += priceKabel
                            user1Kabel.balance -= priceKabel
                            if user2_column_kabel == 'telefoniya':
                                if mess_kabel == '':
                                    mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на телефония: {priceKabel} manat
            """
                                else:
                                    mess_kabel += f"""c кабель на телефония: {priceKabel} manat
            """
                                per_info.telefon2 += priceKabel
                                totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                                user1.b_telefon = 0
                                user1.b_slr = 0
                                user1.b_kod = 0
                                user1.b_zakaz = 0
                                user1.b_dop_uslugi = 0
                                user1.b_prochee = totalTelefoniya + priceKabel
                                mess += f"""c kabel на телефония: {priceKabel} манат
            """
                            if user2_column_kabel == 'internet':
                                if mess_kabel == '':
                                    mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на интернет: {priceKabel} manat
            """
                                else:
                                    mess_kabel += f"""c кабель на интернет: {priceKabel} manat
            """
                                per_info.internet2 += priceKabel
                                user1.b_internet += priceKabel
                                mess += f"""c kabel на интернет: {priceKabel} манат
            """
                            if user2_column_kabel == 'alem':
                                if mess_kabel == '':
                                    mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на alem: {priceKabel} manat
            """
                                else:
                                    mess_kabel += f"""c кабель на alem: {priceKabel} manat
            """
                                per_info.alem2 += priceKabel
                                user1.b_alem += priceKabel
                                mess += f"""c kabel на alem: {priceKabel} манат
            """

                        if priceTel != 0 or priceInt != 0 or priceAlem != 0 or priceKabel != 0:
                            mess += comment
                            per_info.comment = mess
                            per_info.save()
                            if user1:
                                user1.save()
                                context['user1'] = user1
                                context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                            if user1Kabel:
                                user1Kabel.save()
                                context['user1Kabel'] = user1Kabel
                            # теперь надо сохранить историю о перекидке в самом кабельном программе если перекидка баланса кабельного была
                            if mess_kabel != '':
                                KabelComment.objects.create(
                                    user = user1Kabel,
                                    worker = request.user.username,
                                    action = 'Изменения данных',
                                    perekidka_info_new_pk = per_info.pk,
                                    comment = f"""{mess_kabel}
            Комментарий: {comment}
            """
                                )
                            messages.success(request, 'Успешная перекидка баланса')
                        else:
                            messages.error(request, 'Все цены перекидки 0')
                    else:
                        ic('Перекидка баланса разные номера')
                        if priceTel != 0:
                            totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                            per_info.telefon1 += priceTel
                            user1.b_telefon = 0
                            user1.b_slr = 0
                            user1.b_kod = 0
                            user1.b_zakaz = 0
                            user1.b_dop_uslugi = 0
                            user1.b_prochee = totalTelefoniya - priceTel
                            if user2_column_telefoniya == 'telefoniya':
                                per_info.telefon2 += priceTel
                                user2.b_prochee += priceTel
                                mess += f"""c телефония на телефония: {priceTel} манат
            """             
                            if user2_column_telefoniya == 'internet':
                                per_info.internet2 += priceTel
                                user2.b_internet += priceTel
                                mess += f"""c телефония на internet: {priceTel} манат
            """
                            if user2_column_telefoniya == 'alem':
                                per_info.alem2 += priceTel
                                user2.b_alem += priceTel
                                mess += f"""c телефония на alem: {priceTel} манат
            """
                            if user2_column_telefoniya == 'kabel' and user2Kabel:
                                per_info.kabel2 += priceTel
                                user2Kabel.balance += priceTel
                                mess += f"""c телефония на kabel: {priceTel} манат
            """
                                if mess_kabel == '':
                                    mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c Телефония на кабель: {priceTel} manat
            """
                                else:
                                    mess_kabel += f"""c Телефония на кабель: {priceTel} manat
            """
                        if priceInt != 0:
                            per_info.internet1 += priceInt
                            user1.b_internet -= priceInt
                            if user2_column_internet == 'telefoniya':
                                per_info.telefon2 += priceInt
                                user2.b_prochee += priceInt
                                mess += f"""c internet на телефония: {priceInt} манат
            """
                            if user2_column_internet == 'internet':
                                per_info.internet2 += priceInt
                                user2.b_internet += priceInt
                                mess += f"""c internet на internet: {priceInt} манат
            """
                            if user2_column_internet == 'alem':
                                per_info.alem2 += priceInt
                                user2.b_alem += priceInt
                                mess += f"""c internet на alem: {priceInt} манат
            """
                            if user2_column_internet == 'kabel' and user2Kabel:
                                per_info.kabel2 += priceInt
                                user2Kabel.balance += priceInt
                                mess += f"""c internet на kabel: {priceInt} манат
            """
                                if mess_kabel == '':
                                    mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c Интернет на кабель: {priceInt} manat
            """
                                else:
                                    mess_kabel += f"""c Интернет на кабель: {priceInt} manat
            """
                        if priceAlem != 0:
                            per_info.alem1 += priceAlem
                            user1.b_alem -= priceAlem
                            if user2_column_alem == 'telefoniya':
                                per_info.telefon2 += priceAlem
                                user2.b_prochee += priceAlem
                                mess += f"""c alem на телефония: {priceAlem} манат
            """
                            if user2_column_alem == 'internet':
                                per_info.internet2 += priceAlem
                                user2.b_internet += priceAlem
                                mess += f"""c alem на internet: {priceAlem} манат
            """
                            if user2_column_alem == 'alem':
                                per_info.alem2 += priceAlem
                                user2.b_alem += priceAlem
                                mess += f"""c alem на alem: {priceAlem} манат
            """
                            if user2_column_alem == 'kabel' and user2Kabel:
                                per_info.kabel2 += priceAlem
                                user2Kabel.balance += priceAlem
                                mess += f"""c alem на kabel: {priceAlem} манат
            """
                                if mess_kabel == '':
                                    mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c алем на кабель: {priceAlem} manat
            """
                                else:
                                    mess_kabel += f"""c алем на кабель: {priceAlem} manat
            """
                        if priceKabel != 0:
                            per_info.kabel1 += priceKabel
                            user1Kabel.balance -= priceKabel
                            if user2_column_kabel == 'telefoniya':
                                per_info.telefon2 += priceKabel
                                user2.b_prochee += priceKabel
                                mess += f"""c kabel на телефония: {priceKabel} манат
            """
                                if mess_kabel == '':
                                    mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на телефония: {priceKabel} manat
            """
                                else:
                                    mess_kabel += f"""c кабель на телефония: {priceKabel} manat
            """
                            if user2_column_kabel == 'internet':
                                per_info.internet2 += priceKabel
                                user2.b_internet += priceKabel
                                mess += f"""c kabel на internet: {priceKabel} манат
            """
                                if mess_kabel == '':
                                    mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на интернет: {priceKabel} manat
            """
                                else:
                                    mess_kabel += f"""c кабель на интернет: {priceKabel} manat
            """
                            if user2_column_kabel == 'alem':
                                per_info.alem2 += priceKabel
                                user2.b_alem += priceKabel
                                mess += f"""c kabel на alem: {priceKabel} манат
            """
                                if mess_kabel == '':
                                    mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на алем: {priceKabel} manat
            """
                                else:
                                    mess_kabel += f"""c кабель на алем: {priceKabel} manat
            """
                            if user2_column_kabel == 'kabel' and user2Kabel:
                                per_info.kabel2 += priceKabel
                                user2Kabel.balance += priceKabel
                                mess += f"""c kabel на kabel: {priceKabel} манат
            """
                                if mess_kabel == '':
                                    mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
            c кабель на кабель: {priceKabel} manat
            """
                                else:
                                    mess_kabel += f"""c кабель на кабель: {priceKabel} manat
            """
                        
                        if priceTel != 0 or priceInt != 0 or priceAlem != 0 or priceKabel != 0:
                            mess += comment
                            per_info.comment = mess
                            per_info.save()
                            if user1:
                                user1.save()
                                context['user1'] = user1
                                context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                            if user2:
                                user2.save()
                                context['user2'] = user2
                                context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
                            if user2Kabel:
                                user2Kabel.save()
                                context['user2Kabel'] = user2Kabel
                            if user1Kabel:
                                user1Kabel.save()
                                context['user1Kabel'] = user1Kabel
                            if mess_kabel != '':
                                KabelComment.objects.create(
                                    user = user1Kabel,
                                    worker = request.user.username,
                                    action = 'Изменения данных',
                                    perekidka_info_new_pk = per_info.pk,
                                    comment = f"""{mess_kabel}
            Комментарий: {comment}
            """)
                                KabelComment.objects.create(
                                    user = user2Kabel,
                                    worker = request.user.username,
                                    action = 'Изменения данных',
                                    perekidka_info_new_pk = per_info.pk,
                                    comment = f"""{mess_kabel}
            Комментарий: {comment}
            """)

                            messages.success(request, 'Успешная перекидка баланса')
                        else:
                            messages.error(request, 'Все цены перекидки 0')
        except Exception as e:
            messages.error(request, f'Откат перекидки ошибка с transaction == {e}')
            logger.error(f'==== Откат перекидки ошибка с transaction при перекидке баланса == {e}')
    # Перекидка только баланс END
    #######################################################################################################################################################
    #################################################################################################################################################################

    
    if request.method == 'POST' and 'perekidkaAll' in request.POST:
        try:
            with transaction.atomic():
                whichPerekidka = request.POST.get('perekidkaAll')
                comment = request.POST.get('comment')
                if comment == '':
                    messages.error(request, 'Введите комментарий')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                #################################################################################################################################################################
                #######################################################################################################################################################
                # Перекидка всех данных  START
                if whichPerekidka == 'abonent' or whichPerekidka == 'kabel_and_abonent':
                    ic('perekidka s abonent na abonent')
                    s_korrect_checkbox = request.POST.get('s_korrect_checkbox')
                    if s_korrect_checkbox:
                        s_korrect_telefoniya = float(request.POST.get('s_korrect_telefoniya')) if request.POST.get('s_korrect_telefoniya') != '' else 0
                        s_korrect_internet = float(request.POST.get('s_korrect_internet')) if request.POST.get('s_korrect_internet') != '' else 0
                        s_korrect_alem = float(request.POST.get('s_korrect_alem')) if request.POST.get('s_korrect_alem') != '' else 0
                    if user1 and user2 and user1.number != user2.number:

                        

                        # Сохраняем логин и договор user2 в OldLoginDogowor если такие есть
                        hb_for_old_log_dog = ''
                        if user2.hb:
                            hb_for_old_log_dog = user2.hb.name

                        save_old_login_dogowor = False
                        if user2.dogowor and user2.login:
                            if OldLoginDogowor.objects.filter(login=user2.login, dogowor=user2.dogowor).exists():
                                messages.error(request, f'Невозможно сохранить login dogowor абонента {user2.number} в old так как такой old login dogowor уже есть')
                                return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                            else:
                                save_old_login_dogowor = True

                        save_old_dogowor_alem = False
                        if user2.dogowor_alem:
                            if OldLoginDogowor.objects.filter(dogowor_alem=user2.dogowor_alem).exists():
                                messages.error(request, f'Невозможно сохранить договор Алем ТВ абонента {user2.number} в old так как такой договор уже есть в old')
                                return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                            save_old_dogowor_alem = True

                        save_old_dogowor_telefoniya = False
                        if user2.dogowor_telefoniya:
                            if OldLoginDogowor.objects.filter(dogowor_telefoniya=user2.dogowor_telefoniya).exists():
                                messages.error(request, f'Невозможно сохранить договор Телефония абонента {user2.number} в old так как такой договор уже есть в old')
                                return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                            save_old_dogowor_telefoniya = True

                        save_old_dogowor_belet = False
                        if user2.dogowor_belet:
                            if OldLoginDogowor.objects.filter(dogowor_belet=user2.dogowor_belet).exists():
                                messages.error(request, f'Невозможно сохранить договор Белет абонента {user2.number} в old так как такой договор уже есть в old')
                                return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                            save_old_dogowor_belet = True

        # Для начало надо сохранить perekidka_info_new для того чтобы взять его id и по id искать все инфы этого изменения по всем таблицам, то нужно для того чтобы при отмене быстро найти всю инфу в таблицах и отменить их 
                        # mess Для в PerekidkaInfoNew
                        if s_korrect_checkbox:
                            totalTelefonBalance = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                            totalTelefonBalance2 = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
                            mess = f"""Перекинуто ( полная перекидка c корректировкой) с {user1.number} на {user2.number} c ({user1.name} {user1.surname}) на ({user2.name} {user2.surname}):
            с телефония на телефонию: 
                            у {user1.number} было: {totalTelefonBalance:.2f} manat
                                    перекинуто: {s_korrect_telefoniya:.2f} manat
                                    стало: {(totalTelefonBalance - s_korrect_telefoniya):.2f}  manat
                            у {user2.number} было: {totalTelefonBalance2:.2f} manat
                                    перекинуто: {s_korrect_telefoniya} manat
                                    стало: {(totalTelefonBalance2 + s_korrect_telefoniya):.2f}  manat
                
            с internet на internet:
                            у {user1.number} было: {user1.b_internet:.2f} manat
                                    перекинуто: {s_korrect_internet:.2f} manat
                                    стало: {(user1.b_internet - s_korrect_internet):.2f}  manat
                            у {user2.number} было: {user2.b_internet:.2f} manat
                                    перекинуто: {s_korrect_internet} manat
                                    стало: {(user2.b_internet + s_korrect_internet):.2f}  manat
            с alem на alem:
                        у {user1.number} было: {user1.b_alem:.2f} manat
                                    перекинуто: {s_korrect_alem:.2f} manat
                                    стало: {(user1.b_alem - s_korrect_alem):.2f}  manat
                        у {user2.number} было: {user2.b_alem:.2f} manat
                                    перекинуто: {s_korrect_alem} manat
                                    стало: {(user2.b_alem + s_korrect_alem):.2f}  manat
            комментарий: {comment}
            """
                        else:
                            totalTelefonBalance = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                            mess = f"""Перекинуто с {user1.number} на {user2.number} c ({user1.name} {user1.surname}) на ({user2.name} {user2.surname}):
            с телефония на телефонию: {totalTelefonBalance:.2f} manat
            с internet на internet: {user1.b_internet:.2f} manat
            с alem на alem: {user1.b_alem:.2f} manat
            комментарий: {comment}
            """
                        # mess Для в PerekidkaInfoNew END

                        perekidka_info_new = PerekidkaInfoNew(
                            user1Number=user1.number,
                            user1Etrap=user1.etrap,
                            user1NameSurname=f"{user1.name} {user1.surname}",
                            user2Number=user2.number,
                            user2Etrap=user2.etrap,
                            user2NameSurname=f"{user2.name} {user2.surname}",
                            operator=request.user.username,
                            comment=mess,
                        )

                        if s_korrect_checkbox:
                            perekidka_info_new.internet1 = s_korrect_internet
                            perekidka_info_new.alem1 = s_korrect_alem
                            perekidka_info_new.telefon1 = s_korrect_telefoniya
                            perekidka_info_new.internet2 = s_korrect_internet
                            perekidka_info_new.alem2 = s_korrect_alem
                            perekidka_info_new.telefon2 = s_korrect_telefoniya
                            perekidka_info_new.type_perekidka='полная перекидка (c корректировкой)'
                        else:
                            perekidka_info_new.internet1=user1.b_internet
                            perekidka_info_new.alem1=user1.b_alem
                            perekidka_info_new.telefon1=totalTelefonBalance
                            perekidka_info_new.internet2=user1.b_internet
                            perekidka_info_new.alem2=user1.b_alem
                            perekidka_info_new.telefon2=totalTelefonBalance
                            perekidka_info_new.type_perekidka='полная перекидка'
                        perekidka_info_new.save()

                        perekidka_info_new_pk = perekidka_info_new.pk
        # Для начало надо сохранить perekidka_info_new
                        if save_old_login_dogowor:
                            OldLoginDogowor.objects.create(login=user2.login, dogowor=user2.dogowor, etrap=user2.etrap, number=user2.number, is_enterprises=user2.is_enterprises, hb=hb_for_old_log_dog, operator=request.user.username, saved_in_action='Перекидка всех данных', account=user2.account)
                        if save_old_dogowor_alem:
                            OldLoginDogowor.objects.create(dogowor_alem=user2.dogowor_alem, etrap=user2.etrap, number=user2.number, is_enterprises=user2.is_enterprises, hb=hb_for_old_log_dog, operator=request.user.username, saved_in_action='Перекидка всех данных', account=user2.account)
                        if save_old_dogowor_telefoniya:
                            OldLoginDogowor.objects.create(dogowor_telefoniya=user2.dogowor_telefoniya, etrap=user2.etrap, number=user2.number, is_enterprises=user2.is_enterprises, hb=hb_for_old_log_dog, operator=request.user.username, saved_in_action='Перекидка всех данных', account=user2.account)
                        if save_old_dogowor_belet:
                            OldLoginDogowor.objects.create(dogowor_belet=user2.dogowor_belet, etrap=user2.etrap, number=user2.number, is_enterprises=user2.is_enterprises, hb=hb_for_old_log_dog, operator=request.user.username, saved_in_action='Перекидка всех данных', account=user2.account)

                    # Сохраняем user2 в архив если он занят
                        if user2.name or user2.surname:
                            user2hb = None
                            if user2.hb:
                                user2hb = user2.hb
                            arhiwUser2 = UserTableArhiw.objects.create(
                                number = user2.number,
                                etrap = user2.etrap,
                                surname = user2.surname,
                                name = user2.name,
                                street = user2.street,
                                home = user2.home,
                                flat = user2.flat,
                                is_enterprises = user2.is_enterprises,
                                account = user2.account,
                                accountName = user2.accountName,
                                hb = user2hb,     
                                internet_connect_date = user2.internet_connect_date,
                                internet_disconnect_date = user2.internet_disconnect_date,
                                abonplata = user2.abonplata,
                                login = user2.login,
                                dogowor = user2.dogowor,
                                dogowor_alem = user2.dogowor_alem,
                                dogowor_telefoniya = user2.dogowor_telefoniya,
                                dogowor_belet = user2.dogowor_belet,
                                beneficiary = user2.beneficiary,

                                b_internet = user2.b_internet,
                                b_kabel = user2.b_kabel,
                                b_alem = user2.b_alem,
                                b_telefon = user2.b_telefon,
                                b_slr = user2.b_slr,
                                b_kod = user2.b_kod,
                                b_zakaz = user2.b_zakaz,
                                b_prochee = user2.b_prochee,
                                b_dop_uslugi = user2.b_dop_uslugi,

                                s_internet = user2.s_internet,
                                s_kabel = user2.s_kabel,
                                s_alem = user2.s_alem,
                                s_telefon = user2.s_telefon,
                                s_slr = user2.s_slr,
                                s_kod = user2.s_kod,
                                s_zakaz = user2.s_zakaz,
                                s_prochee = user2.s_prochee,
                                s_dop_uslugi = user2.s_dop_uslugi,
                                
                                addDate = user2.addDate,
                                snyat_date = datetime.now(),
                                snyat_bool = True,
                                perekidka_info_new_pk = perekidka_info_new_pk
                                )
                            if user2.service.exists():
                                for i in user2.service.all():
                                    arhiwUser2.service.add(i)
                    # Сохраняем user2 в архив если он занят

                    # Сохраняем user1 в архив
                        user1hb = None
                        if user1.hb:
                            user1hb = user1.hb
                        arhiwUser1 = UserTableArhiw.objects.create(
                            number = user1.number,
                            etrap = user1.etrap,
                            surname = user1.surname,
                            name = user1.name,
                            street = user1.street,
                            home = user1.home,
                            flat = user1.flat,
                            is_enterprises = user1.is_enterprises,
                            account = user1.account,
                            accountName = user1.accountName,
                            hb = user1hb,     
                            internet_connect_date = user1.internet_connect_date,
                            internet_disconnect_date = user1.internet_disconnect_date,
                            abonplata = user1.abonplata,
                            login = user1.login,
                            dogowor = user1.dogowor,
                            dogowor_alem = user1.dogowor_alem,
                            dogowor_telefoniya = user1.dogowor_telefoniya,
                            dogowor_belet = user1.dogowor_belet,
                            beneficiary = user1.beneficiary,

                            b_internet = user1.b_internet,
                            b_kabel = user1.b_kabel,
                            b_alem = user1.b_alem,
                            b_telefon = user1.b_telefon,
                            b_slr = user1.b_slr,
                            b_kod = user1.b_kod,
                            b_zakaz = user1.b_zakaz,
                            b_prochee = user1.b_prochee,
                            b_dop_uslugi = user1.b_dop_uslugi,

                            s_internet = user1.s_internet,
                            s_kabel = user1.s_kabel,
                            s_alem = user1.s_alem,
                            s_telefon = user1.s_telefon,
                            s_slr = user1.s_slr,
                            s_kod = user1.s_kod,
                            s_zakaz = user1.s_zakaz,
                            s_prochee = user1.s_prochee,
                            s_dop_uslugi = user1.s_dop_uslugi,
                            
                            addDate = user1.addDate,
                            snyat_date = datetime.now(),
                            snyat_bool = True,
                            perekidka_info_new_pk = perekidka_info_new_pk
                            )
                        if user1.service.exists():
                            for i in user1.service.all():
                                arhiwUser1.service.add(i)
                    # Сохраняем user1 в архив

                        
        # Переносим данные с user1 на user2
                        user1hb = None
                        if user1.hb:
                            user1hb = user1.hb
                            
                        user2.surname = user1.surname
                        user2.name = user1.name
                        user2.street = user1.street
                        user2.home = user1.home
                        user2.flat = user1.flat
                        user2.sotowyy = user1.sotowyy

                        user2.is_enterprises = user1.is_enterprises
                        user2.account = user1.account
                        user2.hb = user1hb
                        user2.abonplata = user1.abonplata
                
                        user2.internet_connect_date = user1.internet_connect_date
                        user2.internet_disconnect_date = user1.internet_disconnect_date
                        user2.beneficiary = user1.beneficiary

                        # Сохраняем инфу об установленных и снятых услугах для UstanowkaSnyatieDopUslugHistory START
                        if user1.service.exists() or user2.service.exists():

                            if user1.service.exists():
                                mes1 = f"""Снятие услуг при перекидке с абонента {user1.number} {user1.etrap} на абонент {user2.number} {user2.etrap}:
            """
                                mes1_count = 0
                                for i in user1.service.all():
                                    mes1_count += 1
                                    mes1 += f"""{mes1_count}) {i.service}
            """
                                UstanowkaSnyatieDopUslugHistory.objects.create(
                                    user=request.user.username,
                                    which_action='при перекидке',
                                    which_type='снято',
                                    number=user1.number,
                                    etrap=user1.etrap,
                                    perekidka_info_new_pk = perekidka_info_new_pk,
                                    comment = f"""Снято услуг:
            {mes1}
            Комментарий: {comment}"""
                                )

                            if user1.service.exists() and user2.service.exists():
                                which_type = 'снято и установлено'
                            elif user1.service.exists() and not user2.service.exists():
                                which_type = 'установлено'
                            elif not user1.service.exists() and user2.service.exists():
                                which_type = 'снято'
                            mes2 = f"""{which_type} услуг при перекидке с абонента {user1.number} {user1.etrap} на абонент {user2.number} {user2.etrap}:
            """
                            if user2.service.exists():
                                mes2 += f"""снято услуг:
            """
                                mes2_count = 0
                                for i in user2.service.all():
                                    mes2_count += 1
                                    mes2 += f"""{mes2_count}) {i.service}
            """
                            if user1.service.exists():
                                mes2 += f"""установлено услуг:
            """
                                count_for_mes2 = 0
                                for i in user1.service.all():
                                    count_for_mes2 += 1
                                    mes2 += f"""{count_for_mes2}) {i.service}
            """ 

                            UstanowkaSnyatieDopUslugHistory.objects.create(
                                user=request.user.username,
                                which_action='при перекидке',
                                which_type=which_type,
                                number=user2.number,
                                etrap=user2.etrap,
                                perekidka_info_new_pk = perekidka_info_new_pk,
                                comment = f"""{mes2}
            Комментарий: {comment}"""
                            )
                        # Сохраняем инфу об установленных и снятых услугах для UstanowkaSnyatieDopUslugHistory END


                        # удаляем все услуги у абонента2 так как на него должны быть только услуги с абонента1, сохраняем для истории в staffhistory для serviceConnect если услуги есть
                        user2OldServices = ''
                        user2OldServicesCount = 0   
                        if user2.service.exists():  # Проверяем, есть ли связанные услуги
                            for old_service in user2.service.all():
                                user2OldServicesCount += 1
                                user2OldServices += f"\n        {user2OldServicesCount}) {old_service.service}"
                            user2.service.clear()  # Очищаем все старые услуги
                        else:
                            user2OldServices = '\n      Нет услуг'

                        # Устанавливаем новые услуги с абонент1 на абонент2, сохраняем для истории в staffhistory для serviceConnect если услуги есть 
                        user2NewServicesCount = 0
                        user2NewServices = ""

                        if user1.service.exists():  # Проверяем, есть ли связанные услуги
                            for i in user1.service.all():
                                user2NewServicesCount += 1
                                user2NewServices += f"\n        {user2NewServicesCount}) {i.service}"
                                user2.service.add(i)
                        else:
                            user2NewServices = '\n      Нет услуг'
                        
                        # Сам проццесс сохранения информации об услугах в staffhistory для serviceConnect если услуги есть 
                        if user1.service.exists() or user2.service.exists():
                            StaffAction.objects.create(user=request.user, perekidka_info_new_pk=perekidka_info_new_pk,  comment=f"""Перекидка улуг при полной перекидке в MTB.
            Перекидка с абонента {user1.number} {user1.etrap} на абонент {user2.number} {user2.etrap}.
            Перед перекидкой было услуг:
                у абонента {user1.number}:{user2NewServices}
                у абонента {user2.number}:{user2OldServices}
            После перекидки стало услуг:
                у абонента {user1.number}:
                    Нет услуг
                у абонента {user2.number}:{user2NewServices}
            """, 
                            action='Изменение Услуг')


                        user2.login = user1.login
                        user2.dogowor = user1.dogowor
                        user2.dogowor_alem = user1.dogowor_alem
                        user2.dogowor_telefoniya = user1.dogowor_telefoniya
                        user2.dogowor_belet = user1.dogowor_belet

                        if s_korrect_checkbox:
                            user2.b_prochee += s_korrect_telefoniya
                            user2.b_internet += s_korrect_internet
                            user2.b_alem += s_korrect_alem
                        else:
                            user2.b_internet += user1.b_internet
                            user2.b_kabel += user1.b_kabel
                            user2.b_alem += user1.b_alem
                            user2.b_telefon += user1.b_telefon
                            user2.b_slr += user1.b_slr
                            user2.b_kod += user1.b_kod
                            user2.b_zakaz += user1.b_zakaz
                            user2.b_prochee += user1.b_prochee
                            user2.b_dop_uslugi += user1.b_dop_uslugi

                        user2.addDate = datetime.now()
                        user2.snyat_date = None
                        user2.snyat_bool = False
                        user2.save()
        # Переносим данные с user1 на user2
                    


                    # Очищаем user1
                        user1.surname = ''
                        user1.name = ''
                        user1.street = ''
                        user1.home = ''
                        user1.flat = ''
                        user1.sotowyy = ''
                        user1.is_enterprises = False
                        user1.account = None
                        user1.accountName = ''
                        user1.hb = None
                        user1.internet_connect_date = None
                        user1.internet_disconnect_date = None
                        user1.abonplata = ''
                        user1.login = ''
                        user1.dogowor = ''
                        user1.dogowor_alem = ''
                        user1.dogowor_telefoniya = ''
                        user1.dogowor_belet = ''
                        user1.addDate = None
                        user1.snyat_date = None
                        user1.snyat_bool = False
                        user1.beneficiary = False
                        
                        if user1.service.exists():
                            user1.service.clear()
                        
                        if s_korrect_checkbox:
                            user1.b_prochee = (user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_dop_uslugi + user1.b_prochee) - float(s_korrect_telefoniya)
                            user1.b_telefon = 0
                            user1.b_slr = 0
                            user1.b_kod = 0
                            user1.b_zakaz = 0
                            user1.b_dop_uslugi = 0

                            user1.b_internet = user1.b_internet - float(s_korrect_internet)
                            user1.b_alem = user1.b_alem - float(s_korrect_alem)
                        else:
                            user1.b_telefon = 0
                            user1.b_slr = 0
                            user1.b_kod = 0
                            user1.b_zakaz = 0
                            user1.b_prochee = 0
                            user1.b_dop_uslugi = 0
                            user1.b_internet = 0
                            user1.b_kabel = 0
                            user1.b_alem = 0
                        user1.save()
                    # Очищаем user1

                    # refresh context
                        if number1:
                            if len(number1) < 6:
                                try:
                                    user1 = UserTable.objects.get(etrap=etrap1, number=number1)
                                except:
                                    user1 = False
                            else:
                                user1 = False
                        else:
                            user1 = False
                        if number2:
                            if len(number2) < 6:
                                try:
                                    user2 = UserTable.objects.get(etrap=etrap2, number=number2)
                                except:
                                    user2 = False
                            else:
                                user2 = False
                        else:
                            user2 = False

                        try:
                            user1Kabel = KabelTvNew.objects.get(number=number1)
                        except:
                            user1Kabel = False

                        try:
                            user2Kabel = KabelTvNew.objects.get(number=number2)
                        except:
                            user2Kabel = False

                        context['user1'] = user1
                        context['user2'] = user2
                        context['user2Kabel'] = user2Kabel
                        context['user1Kabel'] = user1Kabel
                        if user1:
                            context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
                        if user2:
                            context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
                    # refresh context
                # Перекидка всех данных только с абонента на абонент END
                #######################################################################################################################################################
                #################################################################################################################################################################


                #################################################################################################################################################################
                #######################################################################################################################################################
                # Перекидка всех данных только с кабеля на кабель START
                if whichPerekidka == 'kabel' or whichPerekidka == 'kabel_and_abonent':
                    ic('perekidka polnaya s kabel na kabel')
                    s_korrect_checkbox_kabel = request.POST.get('s_korrect_checkbox_kabel')
                    if s_korrect_checkbox_kabel:
                        s_korrect_kabel = float(request.POST.get('s_korrect_kabel')) if request.POST.get('s_korrect_kabel') != '' else 0

                    if s_korrect_checkbox_kabel:
                        if s_korrect_kabel:
                            s_kor_text = '(с корректировкой)'
                            set_bal = s_korrect_kabel
                        else:
                            s_kor_text = ''
                            set_bal = user1Kabel.balance
                    else:
                        s_kor_text = ''
                        set_bal = user1Kabel.balance

                    if user2Kabel:
                        # теперь сохраняем 2-й комментарий для PerekidkaInfoNew
                        perekidkaInfoNew = PerekidkaInfoNew(
                            user1KabelNumber = user1Kabel.number,
                            user1KabelNameSurname = f"{user1Kabel.surname} {user1Kabel.name}",
                            user2KabelNumber = user2Kabel.number,
                            user2KabelNameSurname = f"{user2Kabel.surname} {user2Kabel.name}",
                            operator = request.user.username,

                            user1Ksurname = user1Kabel.surname,
                            user1Kname = user1Kabel.name,
                            user1Kstreet = user1Kabel.street,
                            user1Khome = user1Kabel.home,
                            user1Kflat = user1Kabel.flat,
                            user1Ksotowyy = user1Kabel.sotowyy,
                            user1Kis_enterprises = user1Kabel.is_enterprises,
                            user1Kis_active = user1Kabel.is_active,
                            user1Kbalance = user1Kabel.balance,
                            user1Kcount = user1Kabel.count,

                            user2Ksurname = user2Kabel.surname,
                            user2Kname = user2Kabel.name,
                            user2Kstreet = user2Kabel.street,
                            user2Khome = user2Kabel.home,
                            user2Kflat = user2Kabel.flat,
                            user2Ksotowyy = user2Kabel.sotowyy,
                            user2Kis_enterprises = user2Kabel.is_enterprises,
                            user2Kis_active = user2Kabel.is_active,
                            user2Kbalance = user2Kabel.balance,
                            user2Kcount = user2Kabel.count,

                            comment = f"""Перекинуто с {user1Kabel.number} на {user2Kabel.number}:
            с кабель на кабель: {set_bal}
            баланс у кабельного перед перекидкой у абонента {user1Kabel.number}: {user1Kabel.balance}
            баланс у кабельного перед перекидкой у абонента {user2Kabel.number}: {user2Kabel.balance}
            Комментарий при перекидке: {comment}
            """,
                            type_perekidka = f'полная перекидка {s_kor_text}',
                            # kabel1=user1Kabel.balance,
                            # kabel2=user2Kabel.balance,
                            kabel1=set_bal,
                            kabel2=set_bal,
                        )
                        perekidkaInfoNew.save()
                        perekidka_info_new_pk = perekidkaInfoNew.pk

                        # perekidka на существующий номер (очистить user2Kabel и сохранить на нее данные с user1Kabel)
                        ic('perekidka на существующий номер (очистить user2Kabel и сохранить на нее данные с user1Kabel)')
                        # для начало создадим кооментарий для номера на который перекидываем данные
                        user2KabelComment = KabelComment(user=user2Kabel)
                        user2KabelComment.worker = request.user.username
                        user2KabelComment.action = 'Изменения данных'

                        is_enterprises1 = 'ilat'
                        if user1Kabel.is_enterprises:
                            is_enterprises1 = 'edara'
                        is_enterprises2 = 'ilat'
                        if user2Kabel.is_enterprises:
                            is_enterprises2 = 'edara'

                        is_active1 = 'Отключено'
                        if user1Kabel.is_active:
                            is_active1 = 'Включено'
                        is_active2 = 'Отключено'
                        if user2Kabel.is_active:
                            is_active2 = 'Включено'
                        
                        user2KabelComment.comment = f"""Перекидка данных {s_kor_text} с {user1Kabel.number} на {user2Kabel.number}:
            Изменения этого абонента:
                1) Фамилия: с {user2Kabel.surname} на {user1Kabel.surname}
                2) Имя: с {user2Kabel.name} на {user1Kabel.name} 
                3) Улица: с {user2Kabel.street} на {user1Kabel.street}
                4) Дом: с {user2Kabel.home} на {user1Kabel.home}
                5) Квартира: с {user2Kabel.flat} на {user1Kabel.flat}
                6) Сотовый: с {user2Kabel.sotowyy} на {user1Kabel.sotowyy}
                7) Предприятие: с {is_enterprises2} на {is_enterprises1}
                8) Статус: с {is_active2} на {is_active1}
                9) Баланс: с {user2Kabel.balance:.2f} на {(set_bal + user2Kabel.balance):.2f} (перекинуто {set_bal:.2f} манат)
                10) Точек: с {user2Kabel.count} на {user1Kabel.count}
                Комментарий при перекидке: {comment}
            """
                        user2KabelComment.perekidka_info_new_pk = perekidka_info_new_pk
                        user2KabelComment.save()
                        # Комментарий для номера с которого перекидываем
                        user1KabelComment = KabelComment(user=user1Kabel)
                        user1KabelComment.worker = request.user.username
                        user1KabelComment.action = 'Изменения данных'

                        is_enterprises1 = 'ilat'
                        if user1Kabel.is_enterprises:
                            is_enterprises1 = 'edara'
                        is_enterprises2 = 'ilat'
                        if user2Kabel.is_enterprises:
                            is_enterprises2 = 'edara'

                        is_active1 = 'Отключено'
                        if user1Kabel.is_active:
                            is_active1 = 'Включено'
                        is_active2 = 'Отключено'
                        if user2Kabel.is_active:
                            is_active2 = 'Включено'
                        user1KabelComment.comment = f"""Перекидка данных {s_kor_text} с {user1Kabel.number} на {user2Kabel.number}:
            Изменения этого абонента:
                1) Статус: с {is_active1} на {not is_active1}
                2) Баланс ({set_bal}): с {user1Kabel.balance} на {(user1Kabel.balance - set_bal):.2f}
                Комментарий при перекидке: {comment}
            """
                        user1KabelComment.perekidka_info_new_pk = perekidka_info_new_pk
                        user1KabelComment.save()

                        # Теперь меняем данные самого абонента на которого перекидывают данные
                        user2Kabel.name = user1Kabel.name
                        user2Kabel.surname = user1Kabel.surname
                        user2Kabel.street = user1Kabel.street
                        user2Kabel.home = user1Kabel.home
                        user2Kabel.flat = user1Kabel.flat
                        user2Kabel.sotowyy = user1Kabel.sotowyy
                        user2Kabel.is_enterprises = user1Kabel.is_enterprises
                        user2Kabel.is_active = user1Kabel.is_active
                        user2Kabel.balance += set_bal
                        user2Kabel.count = user1Kabel.count
                        user2Kabel.save()

                        # Теперь меняем данные самого абонента с которого перекидывают данные (просто отключем статус и обнуляем баланс) 
                        user1Kabel.is_active = False
                        user1Kabel.balance = user1Kabel.balance - set_bal
                        user1Kabel.save()
                
                        
                    else:

                        # создаем второй комментарий для PerekidkaInfoNew (для пустого абонента)
                    
                        newUserKabel = KabelTvNew(number=number2)
                        newUserKabel.name = user1Kabel.name
                        newUserKabel.surname = user1Kabel.surname
                        newUserKabel.street = user1Kabel.street
                        newUserKabel.home = user1Kabel.home
                        newUserKabel.flat = user1Kabel.flat
                        newUserKabel.sotowyy = user1Kabel.sotowyy
                        newUserKabel.is_enterprises = user1Kabel.is_enterprises
                        newUserKabel.is_active = user1Kabel.is_active
                        newUserKabel.balance += set_bal
                        newUserKabel.count += user1Kabel.count
                        newUserKabel.save()

                        comment2 = PerekidkaInfoNew(
                            user1KabelNumber = user1Kabel.number,
                            user1KabelNameSurname = f"{user1Kabel.name} {user1Kabel.surname}",
                            user2KabelNumber = newUserKabel.number,
                            user2KabelNameSurname = f"{newUserKabel.name} {newUserKabel.surname}",
                            operator = request.user.username,

                            user1Ksurname = user1Kabel.surname,
                            user1Kname = user1Kabel.name,
                            user1Kstreet = user1Kabel.street,
                            user1Khome = user1Kabel.home,
                            user1Kflat = user1Kabel.flat,
                            user1Ksotowyy = user1Kabel.sotowyy,
                            user1Kis_enterprises = user1Kabel.is_enterprises,
                            user1Kis_active = user1Kabel.is_active,
                            user1Kbalance = user1Kabel.balance,
                            user1Kcount = user1Kabel.count,
                            
                            comment = f"""Полная перекидка данных {s_kor_text} с кабельного на новый кабелный номер, c номера {user1Kabel.number} на новый номер {newUserKabel.number}:
            Переход баланса c кабеля на кабель: {set_bal:.2f}
            Комментарий при перекидке: {comment}
            """,
                            type_perekidka = 'полная перекидка',
                            kabel1 = set_bal,
                            kabel2 = set_bal,
                        )
                        comment2.save()
                        perekidka_info_new_pk = comment2.pk
                        # перекидка на новый номер (создать новый кабельный номер и сохранить на нее данные с user1Kabel)
                        ic('перекидка на новый номер (создать новый кабельный номер и сохранить на нее данные с user1Kabel)')
                        

                        # Создаем коментарий для нового номера
                        newUserComment = KabelComment(user=newUserKabel)
                        newUserComment.worker = request.user.username
                        newUserComment.action = 'Добавление абонента'

                        is_enterprises = 'Нет'
                        if user1Kabel.is_enterprises:
                            is_enterprises = 'Да'
                        is_active = 'Нет'
                        if user1Kabel.is_active:
                            is_active = 'Да'
                        newUserComment.comment = f"""Переход с номера ({user1Kabel.number} на номер {newUserKabel.number}:)
            Фамилия: {user1Kabel.surname}
            Имя: {user1Kabel.name}
            Улица: {user1Kabel.street}
            Дом: {user1Kabel.home}
            Квартира: {user1Kabel.flat}
            Сотовый: {user1Kabel.sotowyy}
            Предприятие: {is_enterprises}
            Ативный: {is_active}
            Баланс: {set_bal}
            Точек: {user1Kabel.count}
            Комментарий при перекидке: {comment}
            """
                        newUserComment.perekidka_info_new_pk = perekidka_info_new_pk
                        newUserComment.save()

                        
                        
                        # просто отключаем кабель старого номера но данные не удаляем (нет необходимости удалять данные старого номера)
                        user1Kabel.is_active = False
                        # Создаем комментарий для старого номера
                        oldUserComment = KabelComment(user=user1Kabel)
                        oldUserComment.worker = request.user.username
                        oldUserComment.action = 'Изменения данных'

                    
                        oldUserComment.comment = f"""Переход с номера ({user1Kabel.number} на номер {newUserKabel.number}:)
            Изменения в абоненте {user1Kabel.number}:
                1) стаус: (с ON на OFF)
                2) перекинули баланс с номера {user1Kabel.number} на новый номер {newUserKabel.number} на сумму {set_bal:.2f}
                3) Баланс нового номера ({newUserKabel.number}) перед перекидкой было 0 
                Комментарий при перекидке: {comment}
            """
                        user1Kabel.balance = user1Kabel.balance - set_bal
                        user1Kabel.save()
                        oldUserComment.perekidka_info_new_pk = perekidka_info_new_pk
                        oldUserComment.save()

                        

                        
                        

                        
                # Перекидка всех данных только с кабеля на кабель END
                #######################################################################################################################################################
                #################################################################################################################################################################



                if whichPerekidka == 'kabel':
                    mess_word = '(с кабеля на кабель)'
                elif whichPerekidka == 'abonent':
                    mess_word = '(с абонента на абонент)'
                else:
                    mess_word = '(с абонента на абонент и с кабеля на кабель)'

                messages.success(request, f'Успешная перекидка всех данных {mess_word}')
        except Exception as e:
            messages.error(request, f'откат перекидки ошибка с transaction == {e}')
            logger.error(f'==== откат перекидки ошибка с transaction при перекидкие всех данных == {e}')

    # отмена перекидки всех данных для абонента
    if request.method == 'POST' and 'change_perekidka' in request.POST:
        try:
            with transaction.atomic():
                change_perekidka = request.POST.get('change_perekidka')

                perekidka_info = PerekidkaInfoNew.objects.get(pk=change_perekidka)

                if perekidka_info.operator != request.user.username:
                    messages.error(request, f'Отменить перекидку может только {perekidka_info.operator}')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)

                
                
                seven_days_ago = timezone.now() - timedelta(days=7)
                if perekidka_info.date < seven_days_ago:
                    messages.error(request, 'Срок для отмены этой перекидки истек')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                else:
                    if 'полная' in perekidka_info.type_perekidka:
                        arhiw = UserTableArhiw.objects.filter(perekidka_info_new_pk=change_perekidka)
                        if not arhiw:
                            messages.error(request, 'эту перекидку невозможно отменить')
                            return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                        else:
                            count = 0
                            dogowor = ''
                            dogowor_alem = ''
                            dogowor_telefoniya = ''
                            dogowor_belet = ''
                            for u in arhiw:
                                user = UserTable.objects.get(number=u.number, etrap=u.etrap)
                                if perekidka_info.user2Number:
                                    if u.number == perekidka_info.user2Number:
                                        dogowor = u.dogowor
                                        dogowor_alem = u.dogowor_alem
                                        dogowor_telefoniya = u.dogowor_telefoniya
                                        dogowor_belet = u.dogowor_belet

                                user.surname = u.surname
                                user.name = u.name
                                user.street = u.street
                                user.home = u.home
                                user.flat = u.flat
                                user.is_enterprises = u.is_enterprises
                                user.account = u.account
                                user.hb = u.hb
                                user.abonplata = u.abonplata
                                user.beneficiary = u.beneficiary
                                user.login = u.login
                                user.dogowor = u.dogowor
                                user.dogowor_alem = u.dogowor_alem
                                user.dogowor_telefoniya = u.dogowor_telefoniya
                                user.dogowor_belet = u.dogowor_belet
                                user.b_internet = u.b_internet
                                user.b_kabel = u.b_kabel
                                user.b_alem = u.b_alem
                                user.b_telefon = u.b_telefon
                                user.b_slr = u.b_slr
                                user.b_kod = u.b_kod
                                user.b_zakaz = u.b_zakaz
                                user.b_prochee = u.b_prochee
                                user.b_dop_uslugi = u.b_dop_uslugi
                                user.service.set(u.service.all())
                                user.save()

                            if len(arhiw) == 1:
                                u2 = UserTable.objects.get(number=perekidka_info.user2Number, etrap=perekidka_info.user2Etrap)
                                u2.surname = ''
                                u2.name = ''
                                u2.street = ''
                                u2.home = ''
                                u2.flat = ''
                                u2.sotowyy = ''
                                u2.is_enterprises = False
                                u2.alem = False
                                u2.alemCount = None
                                u2.alem_connect_date = None
                                u2.alem_on_date = None
                                u2.alem_off_date = None
                                u2.alem_disconnect_date = None
                                u2.account = None
                                u2.accountName = ''
                                u2.accountAdress = ''
                                u2.hb = None
                                u2.internet_tarif = None
                                u2.internet_connect_date = None
                                u2.internet_disconnect_date = None
                                u2.abonplata = ''
                                u2.beneficiary = False
                                u2.is_on = False
                                u2.is_on_date = None
                                u2.kabel_count = None
                                u2.connect_date = None
                                u2.kabel_comments = ''
                                u2.ids = ''
                                u2.login = ''
                                u2.dogowor = ''
                                u2.dogowor_alem = ''
                                u2.dogowor_telefoniya = ''
                                u2.dogowor_belet = ''
                                u2.b_internet = 0
                                u2.b_kabel = 0
                                u2.b_alem = 0
                                u2.b_telefon = 0
                                u2.b_slr = 0
                                u2.b_kod = 0
                                u2.b_zakaz = 0
                                u2.b_prochee = 0
                                u2.b_dop_uslugi = 0
                                u2.s_internet = 0
                                u2.s_kabel = 0
                                u2.s_alem = 0
                                u2.s_telefon = 0
                                u2.s_slr = 0
                                u2.s_kod = 0
                                u2.s_zakaz = 0
                                u2.s_prochee = 0
                                u2.s_dop_uslugi = 0
                                u2.addDate = None
                                u2.wost_date = None
                                u2.snyat_bool = False
                                u2.snyat_date = None
                                u2.intOnDate = None
                                u2.intOffDate = None
                                # Очищаем M2M поле
                                u2.service.clear()
                                # Сохраняем изменения
                                u2.save()

                            UstanowkaSnyatieDopUslugHistory.objects.filter(perekidka_info_new_pk=change_perekidka).delete()
                            StaffAction.objects.filter(perekidka_info_new_pk=change_perekidka).delete() 
                            OldLoginDogowor.objects.filter(number=number2, etrap=etrap2, dogowor=dogowor).delete()
                            if dogowor_alem:
                                OldLoginDogowor.objects.filter(number=number2, etrap=etrap2, dogowor_alem=dogowor_alem).delete()
                            if dogowor_telefoniya:
                                OldLoginDogowor.objects.filter(number=number2, etrap=etrap2, dogowor_telefoniya=dogowor_telefoniya).delete()
                            if dogowor_belet:
                                OldLoginDogowor.objects.filter(number=number2, etrap=etrap2, dogowor_belet=dogowor_belet).delete()

                            arhiw.delete()
                            perekidka_info.delete()
                        
                            messages.success(request, f"Успешная отмена перекидки {change_perekidka}")
                            
                    elif perekidka_info.type_perekidka == 'перекидка баланса':
                        if perekidka_info.operator != request.user.username:
                            messages.error(request, f'Отменить перекидку может только {perekidka_info.operator}')
                            return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)

                        # if not KabelComment.objects.filter(perekidka_info_new_pk=change_perekidka).exists():
                        #     messages.error(request, f'Вы не можете отменить эту перекидку')
                        #     return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)


                        u1 = None
                        if perekidka_info.user1Number and perekidka_info.user1Etrap:
                            u1 = UserTable.objects.get(number=perekidka_info.user1Number, etrap=perekidka_info.user1Etrap)

                        u2 = None
                        if perekidka_info.user2Number and perekidka_info.user2Etrap:
                            u2 = UserTable.objects.get(number=perekidka_info.user2Number, etrap=perekidka_info.user2Etrap)

                        u1K = None
                        if perekidka_info.user1KabelNumber:
                            u1K = KabelTvNew.objects.get(number=perekidka_info.user1KabelNumber)

                        u2K = None
                        if perekidka_info.user2KabelNumber:
                            u2K = KabelTvNew.objects.get(number=perekidka_info.user2KabelNumber)

                        perekinuto_telefoniya1 = perekidka_info.telefon1
                        perekinuto_internet1 = perekidka_info.internet1
                        perekinuto_alem1 = perekidka_info.alem1
                        perekinuto_kabel1 = perekidka_info.kabel1

                        perekinuto_telefoniya2 = perekidka_info.telefon2
                        perekinuto_internet2 = perekidka_info.internet2
                        perekinuto_alem2 = perekidka_info.alem2
                        perekinuto_kabel2 = perekidka_info.kabel2

                    

                        if u1K and u2K:
                            if u1K.pk == u2K.pk:
                                if perekinuto_kabel1:
                                    u1K.balance += perekinuto_kabel1
                            else:
                                if perekinuto_kabel1:
                                    u1K.balance += perekinuto_kabel1   
                                if perekinuto_kabel2:
                                    u2K.balance -= perekinuto_kabel2
                        elif not u1K and u2K:
                            if perekinuto_kabel2:
                                u2K.balance -= perekinuto_kabel2

                        elif u1K and not u2K:
                            if perekinuto_kabel1:
                                u1K.balance += perekinuto_kabel1
                                

                        
                        if u1 and u2:
                            if u1.pk == u2.pk:
                                if perekinuto_telefoniya1:
                                    u1.b_prochee += perekinuto_telefoniya1
                                if perekinuto_internet1:
                                    u1.b_internet += perekinuto_internet1
                                if perekinuto_alem1:
                                    u1.b_alem += perekinuto_alem1
                                
                    
                                if perekinuto_telefoniya2:
                                    u1.b_prochee -= perekinuto_telefoniya2
                                if perekinuto_internet2:
                                    u1.b_internet -= perekinuto_internet2
                                if perekinuto_alem2:
                                    u1.b_alem -= perekinuto_alem2

                                
        
                            else:
                                if perekinuto_telefoniya1:
                                    u1.b_prochee += perekinuto_telefoniya1
                                if perekinuto_telefoniya2:
                                    u2.b_prochee -= perekinuto_telefoniya2

                                if perekinuto_internet1:
                                    u1.b_internet += perekinuto_internet1
                                if perekinuto_internet2:
                                    u2.b_internet -= perekinuto_internet2

                                if perekinuto_alem1:
                                    u1.b_alem += perekinuto_alem1
                                if perekinuto_alem2:
                                    u2.b_alem -= perekinuto_alem2
                        
                        elif not u1 and u2:
                            if perekinuto_telefoniya2:
                                u2.b_prochee -= perekinuto_telefoniya2
                            if perekinuto_internet2:
                                u2.b_internet -= perekinuto_internet2
                            if perekinuto_alem2:
                                u2.b_alem -= perekinuto_alem2
                        
                        elif u1 and not u2:
                            if perekinuto_telefoniya1:
                                u1.b_prochee += perekinuto_telefoniya1
                            if perekinuto_internet1:
                                u1.b_internet += perekinuto_internet1
                            if perekinuto_alem1:
                                u1.b_alem += perekinuto_alem1
             


                        if u1:
                            u1.save()
                        if u2:
                            if u1:
                                if u1.pk != u2.pk:
                                    u2.save()
                            else:
                                u2.save()
                        if u1K:
                            u1K.save()
                        if u2K:
                            if u1K:
                                if u1K.pk != u2K.pk:
                                    u2K.save()
                            else:
                                u2K.save()

                        KabelComment.objects.filter(perekidka_info_new_pk=change_perekidka).delete()
                        perekidka_info.delete()

                        messages.success(request, f"Успешная отмена перекидки баланса")
                            

                    
                        

                    else:
                        messages.error(request, 'непонятная фигня')
                        return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
        except Exception as e:
            messages.error(request, f'откат перекидки ошибка с transaction == {e}')
            logger.error(f' ==== откат перекидки ошибка с transaction при отмене либо перекидки всего сабонента на абонент либо перекидки баланса с абонента на абонент или с кабеля на кабель  == {e}')


    
    # отмена перекидки всех данных для кабельного
    if request.method == 'POST' and 'change_perekidka_kabel' in request.POST:
        try:
            with transaction.atomic():
                change_perekidka = request.POST.get('change_perekidka_kabel')
                
                perekidka_info = PerekidkaInfoNew.objects.get(pk=change_perekidka)

                seven_days_ago = timezone.now() - timedelta(days=7)
                if perekidka_info.date < seven_days_ago:
                    messages.error(request, 'Срок для отмены этой перекидки истек')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)


                if perekidka_info.operator != request.user.username:
                    messages.error(request, f'Отменить перекидку может только {perekidka_info.operator}')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)

                

                if perekidka_info.user2Ksurname or perekidka_info.user2Kname:
                    # востановить и u1 и u2
                    ic('change_perekidka', change_perekidka)
                    user1K = KabelTvNew.objects.get(number=perekidka_info.user1KabelNumber)
                    user2K = KabelTvNew.objects.get(number=perekidka_info.user2KabelNumber)

                    user1K.name = perekidka_info.user1Kname
                    user1K.surname = perekidka_info.user1Ksurname
                    user1K.street = perekidka_info.user1Kstreet
                    user1K.home = perekidka_info.user1Khome
                    user1K.flat = perekidka_info.user1Kflat
                    user1K.sotowyy = perekidka_info.user1Ksotowyy
                    user1K.is_enterprises = perekidka_info.user1Kis_enterprises
                    user1K.is_active = perekidka_info.user1Kis_active
                    user1K.balance = perekidka_info.user1Kbalance
                    user1K.count = perekidka_info.user1Kcount


                    user2K.name = perekidka_info.user2Kname
                    user2K.surname = perekidka_info.user2Ksurname
                    user2K.street = perekidka_info.user2Kstreet
                    user2K.home = perekidka_info.user2Khome
                    user2K.flat = perekidka_info.user2Kflat
                    user2K.sotowyy = perekidka_info.user2Ksotowyy
                    user2K.is_enterprises = perekidka_info.user2Kis_enterprises
                    user2K.is_active = perekidka_info.user2Kis_active
                    user2K.balance = perekidka_info.user2Kbalance
                    user2K.count = perekidka_info.user2Kcount

                    user1K.save()
                    user2K.save()
                
            

            


                else:
                    # востановить только u1
                    user1K = KabelTvNew.objects.get(number=perekidka_info.user1KabelNumber)
                    user2K = KabelTvNew.objects.get(number=perekidka_info.user2KabelNumber)

                    user1K.name = perekidka_info.user1Kname
                    user1K.surname = perekidka_info.user1Ksurname
                    user1K.street = perekidka_info.user1Kstreet
                    user1K.home = perekidka_info.user1Khome
                    user1K.flat = perekidka_info.user1Kflat
                    user1K.sotowyy = perekidka_info.user1Ksotowyy
                    user1K.is_enterprises = perekidka_info.user1Kis_enterprises
                    user1K.is_active = perekidka_info.user1Kis_active
                    user1K.balance = perekidka_info.user1Kbalance
                    user1K.count = perekidka_info.user1Kcount

                    user2K.delete()

                KabelComment.objects.filter(perekidka_info_new_pk=change_perekidka).delete()
                perekidka_info.delete()
                
                messages.success(request, f"Успешная отмена перекидки кабельного {change_perekidka}")
        except Exception as e:
            messages.error(request, f'откат перекидки ошибка с transaction == {e}')
            logger.error(f' ==== откат перекидки ошибка с transaction при отмене перекидки всего при кабеля на кабель  == {e}')
        
    
    if request.method == 'POST' and 'change_pay_with_comment' in request.POST:
        change_pay_pk = request.POST.get('change_pay_with_comment')
        cancel_reason = request.POST.get('cancel_reason')
        
        if not cancel_reason:
            messages.error(request, 'Введите комментарий')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
        
        if not change_pay_pk:
            messages.error(request, 'Не указан идентификатор платежа')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
        
        try:
            pays_with_comment = PaysWithComment.objects.get(pk=change_pay_pk)
        except PaysWithComment.DoesNotExist:
            messages.error(request, 'Платеж не найден')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
        
        try:
            if pays_with_comment.kabel != 0:
                try:
                    users_PWC = KabelTvNew.objects.get(number=pays_with_comment.number)
                    users_PWC.balance -= pays_with_comment.kabel
                    pay_obj = KabelTvPayHistory.objects.get(pk=pays_with_comment.pays_pk)
                except (KabelTvNew.DoesNotExist, KabelTvPayHistory.DoesNotExist) as e:
                    messages.error(request, f'Ошибка при отмене платежа: {e}')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
            else:
                try:
                    users_PWC = UserTable.objects.get(number=pays_with_comment.number, etrap=pays_with_comment.etrap)
                    pay_obj = PayHistory.objects.get(pk=pays_with_comment.pays_pk)
                    
                    if pays_with_comment.prochee != 0:
                        users_PWC.b_prochee -= pays_with_comment.prochee
                    elif pays_with_comment.internet != 0:
                        users_PWC.b_internet -= pays_with_comment.internet
                    elif pays_with_comment.alem != 0:
                        users_PWC.b_alem -= pays_with_comment.alem
                    else:
                        messages.error(request, 'Не указан тип платежа для отмены')
                        return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
                        
                except (UserTable.DoesNotExist, PayHistory.DoesNotExist) as e:
                    messages.error(request, f'Ошибка при отмене платежа: {e}')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)

            pays_with_comment.when_changed = datetime.now()
            pays_with_comment.changed = True
            pays_with_comment.who_changed = request.user.username
            pays_with_comment.changed_comment = cancel_reason

            try:
                with transaction.atomic():
                    pays_with_comment.save()
                    users_PWC.save()
                    pay_obj.delete()
                    messages.success(request, 'Платеж успешно отменен')
                    
            except Exception as e:
                messages.error(request, f'Откат отмены платежа, ошибка: {e}')
                logger.error(f'Ошибка при отмене платежа: {e}', exc_info=True)
                
        except Exception as e:
            messages.error(request, f'Ошибка при обработке запроса: {e}')
            logger.error(f'Ошибка при обработке запроса: {e}', exc_info=True)
    

    # if request.method == 'POST' and 'change_pay_with_comment' in request.POST:
    #     change_pay_pk = request.POST.get('change_pay_with_comment')
    #     cancel_reason = request.POST.get('cancel_reason')
    #     if cancel_reason == '':
    #         messages.error(request, 'Введите комментарий')
    #         return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
         
    #     pays_with_comment = PaysWithComment.objects.get(pk=change_pay_pk)

    #     if pays_with_comment.kabel != 0:
    #         users_PWC = KabelTvNew.objects.get(number=pays_with_comment.number)
    #         users_PWC.balance -= pays_with_comment.kabel
    #         pay_obj = KabelTvPayHistory.objects.get(pk=pays_with_comment.pays_pk)
    #     else:
    #         users_PWC = UserTable.objects.get(number=pays_with_comment.number, etrap=pays_with_comment.etrap)
    #         pay_obj = PayHistory.objects.get(pk=pays_with_comment.pays_pk)
    #         if pays_with_comment.prochee != 0:
    #             users_PWC.b_prochee -= pays_with_comment.prochee
    #         elif pays_with_comment.internet != 0:
    #             users_PWC.b_internet -= pays_with_comment.internet
    #         elif pays_with_comment.alem != 0:
    #             users_PWC.b_alem -= pays_with_comment.alem


    #     pays_with_comment.when_changed = datetime.now()
    #     pays_with_comment.who_changed = request.user.username
    #     pays_with_comment.changed_comment = cancel_reason

    #     try:
    #         with transaction.atomic():
    #             pays_with_comment.save()
    #             users_PWC.save()
    #             pay_obj.delete()
    #     except Exception as e:
    #         messages.error(request, f'откат отмены платежа, ошибка с transaction == {e}')
    #         logger.error(f' ==== откат отмены платежа, ошибка с transaction == {e}')
        

        
 

    return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)






# код идеально работает но в ней нет transaction и нет отмены перекидок (сделал +1 отступ для того чтобы свернуть код)
    # from django.shortcuts import render, redirect
    # from django.contrib import messages
    # from icecream import ic
    # from datetime import datetime
    # from telekom.models import *




    # def perekidka_new(request):
    #     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
        

    #     request_user = request.user
    #     groups = request_user.groups.all()
    #     request_user_etrap = ''
    #     request_user_type = ''
    #     for g in groups:
    #         request_user_etrap, request_user_type = g.name.split('_')
    #         if request_user_type == 'MTB':# or request.user.username == 'admin1':
    #             break

    #     if request_user_type != 'MTB' and (not request.user.is_superuser and request.user.username != 'admin1'):
    #         messages.error(request, 'Не достаточно прав')
    #         return redirect('HomePage')

    #     context = {}

    #     context['all_new_for_mtb'] = True
    #     context['etraps'] = etraps

    #     current_date = datetime.now().date()
    #     formatted_date = current_date.strftime('%Y-%m-%d')
    #     current_year, current_month, current_day = formatted_date.split('-')

    #     context['formatted_date'] = formatted_date
    #     context['current_year'] = current_year
    #     context['current_month'] = current_month
    #     context['current_day'] = current_day

        
    #     context['perekidka_new'] = True
    #     if request_user_type == 'MTB':
    #         context['matbIndex'] = True 
    #         context['request_user_etrap'] = request_user_etrap 

    #     etrap1 = request.GET.get('etrap1')
    #     number1 = request.GET.get('number1')
    #     etrap2 = request.GET.get('etrap2')
    #     number2 = request.GET.get('number2')

        

    #     allow = False
    #     if not request.user.is_superuser and request.user.username != 'admin1':
    #         if not etrap1 and not etrap2:
    #             allow = True
    #         if not etrap1 and etrap2 in etraps and etrap2 == request_user_etrap:
    #             allow = True
    #         if etrap1 and etrap1 in etraps and etrap1 == request_user_etrap and not etrap2:
    #             allow = True
    #         if etrap1 and etrap2 and etrap1 in etraps and etrap2 in etraps and etrap1 == request_user_etrap and etrap2 == request_user_etrap:
    #             allow = True
    #     else:
    #         allow = True

    #     if not allow:
    #         messages.error(request, f"Выберите абонента с своего этрапа")
    #         return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)

    #     context['etrap1'] = etrap1
    #     context['number1'] = number1
    #     context['etrap2'] = etrap2
    #     context['number2'] = number2
    #     context['selected_etrap1'] = etrap1
    #     context['selected_etrap2'] = etrap2
    #     if number1:
    #         if len(number1) < 6:
    #             try:
    #                 user1 = UserTable.objects.get(etrap=etrap1, number=number1)
    #             except:
    #                 user1 = False
    #         else:
    #             user1 = False
    #     else:
    #         user1 = False
    #     if number2:
    #         if len(number2) < 6:
    #             try:
    #                 user2 = UserTable.objects.get(etrap=etrap2, number=number2)
    #             except:
    #                 user2 = False
    #         else:
    #             user2 = False
    #     else:
    #         user2 = False
    #     if etrap1 == 'Dashoguz':
    #         try:
    #             user1Kabel = KabelTvNew.objects.get(number=number1)
    #         except:
    #             user1Kabel = False

    #         try:
    #             user2Kabel = KabelTvNew.objects.get(number=number2)
    #         except:
    #             user2Kabel = False
    #         context['user2Kabel'] = user2Kabel
    #         context['user1Kabel'] = user1Kabel
    #     else:
    #         user1Kabel = False
    #         user2Kabel = False

    #     context['user1'] = user1
    #     context['user2'] = user2
        
    #     if user1:
    #         context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #     if user2:
    #         context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi

    #     #################################################################################################################################################################
    #     #######################################################################################################################################################
    #     # Перекидка только баланс START
    #     if request.method == 'POST' and 'perekidkaBalance' in request.POST:
    #         priceTel = float(request.POST.get('priceTel')) if request.POST.get('priceTel') not in ['', None] else 0
    #         priceInt = float(request.POST.get('priceInt')) if request.POST.get('priceInt') not in ['', None] else 0
    #         priceAlem = float(request.POST.get('priceAlem')) if request.POST.get('priceAlem') not in ['', None] else 0
    #         priceKabel = float(request.POST.get('priceKabel')) if request.POST.get('priceKabel') not in ['', None] else 0
    #         user2_column_telefoniya = request.POST.get('user2_column_telefoniya')
    #         user2_column_internet = request.POST.get('user2_column_internet')
    #         user2_column_alem = request.POST.get('user2_column_alem')
    #         user2_column_kabel = request.POST.get('user2_column_kabel')
    #         comment = request.POST.get('comment')

    #         if not user1Kabel and not user1 and not user2 and not user2Kabel:
    #             # false false false false
    #             messages.error(request, 'Введите корректные данные')
    #             return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
    #         elif not user1Kabel and not user1 and not user2 and user2Kabel:
    #             # false false false true
    #             messages.error(request, 'Введите корректные данные')
    #             return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
    #         elif not user1Kabel and not user1 and user2 and not user2Kabel:
    #             # false false true false
    #             messages.error(request, 'Введите корректные данные')
    #             return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
    #         elif not user1Kabel and not user1 and user2 and user2Kabel:
    #             # false false true true
    #             messages.error(request, 'Введите корректные данные')
    #             return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
    #         elif not user1Kabel and user1 and not user2 and not user2Kabel:
    #             # false true false false
    #             messages.error(request, 'Введите корректные данные')
    #             return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
    #         elif not user1Kabel and user1 and not user2 and user2Kabel:
    #             # false true false true
    #             per_info = PerekidkaInfoNew(
    #                 user1Number = user1.number,
    #                 user1Etrap = user1.etrap,
    #                 user1NameSurname = f"{user1.surname} {user1.name}",

    #                 user2KabelNumber = user2Kabel.number,
    #                 user2KabelNameSurname = f"{user2Kabel.surname} {user2Kabel.name}",

    #                 operator = request.user.username,
    #                 type_perekidka = 'перекидка баланса',
    #             )
    #         elif not user1Kabel and user1 and user2 and not user2Kabel:
    #             # false true true false
    #             per_info = PerekidkaInfoNew(
    #                 user1Number = user1.number,
    #                 user1Etrap = user1.etrap,
    #                 user1NameSurname = f"{user1.surname} {user1.name}",

    #                 user2Number = user2.number,
    #                 user2Etrap = user2.etrap,
    #                 user2NameSurname = f"{user2.surname} {user2.name}",

    #                 operator = request.user.username,
    #                 type_perekidka = 'перекидка баланса',
    #             )
    #         elif not user1Kabel and user1 and user2 and user2Kabel:
    #             # false true true true
    #             per_info = PerekidkaInfoNew(
    #                 user1Number = user1.number,
    #                 user1Etrap = user1.etrap,
    #                 user1NameSurname = f"{user1.surname} {user1.name}",

    #                 user2Number = user2.number,
    #                 user2Etrap = user2.etrap,
    #                 user2NameSurname = f"{user2.surname} {user2.name}",

    #                 user2KabelNumber = user2Kabel.number,
    #                 user2KabelNameSurname = f"{user2Kabel.surname} {user2Kabel.name}",

    #                 operator = request.user.username,
    #                 type_perekidka = 'перекидка баланса',
    #             )
    #         elif user1Kabel and not user1 and not user2 and not user2Kabel:
    #             # true false false false
    #             messages.error(request, 'Введите корректные данные')
    #             return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
    #         elif user1Kabel and not user1 and not user2 and user2Kabel:
    #             # true false false true
    #             per_info = PerekidkaInfoNew(
    #                 user1KabelNumber = user1Kabel.number,
    #                 user1KabelNameSurname = f"{user1Kabel.surname} {user1Kabel.name}",
        
    #                 user2KabelNumber = user2Kabel.number,
    #                 user2KabelNameSurname = f"{user2Kabel.surname} {user2Kabel.name}",

    #                 operator = request.user.username,
    #                 type_perekidka = 'перекидка баланса',
    #             )
    #         elif user1Kabel and not user1 and user2 and not user2Kabel:
    #             # true false true false
    #             per_info = PerekidkaInfoNew(
    #                 user1KabelNumber = user1Kabel.number,
    #                 user1KabelNameSurname = f"{user1Kabel.surname} {user1Kabel.name}",

    #                 user2Number = user2.number,
    #                 user2Etrap = user2.etrap,
    #                 user2NameSurname = f"{user2.surname} {user2.name}",

    #                 operator = request.user.username,
    #                 type_perekidka = 'перекидка баланса',
    #             )
    #         elif user1Kabel and not user1 and user2 and user2Kabel:
    #             # true false true true
    #             per_info = PerekidkaInfoNew(
    #                 user1KabelNumber = user1Kabel.number,
    #                 user1KabelNameSurname = f"{user1Kabel.surname} {user1Kabel.name}",

    #                 user2Number = user2.number,
    #                 user2Etrap = user2.etrap,
    #                 user2NameSurname = f"{user2.surname} {user2.name}",

    #                 user2KabelNumber = user2Kabel.number,
    #                 user2KabelNameSurname = f"{user2Kabel.surname} {user2Kabel.name}",

    #                 operator = request.user.username,
    #                 type_perekidka = 'перекидка баланса',
    #             )
    #         elif user1Kabel and user1 and not user2 and not user2Kabel:
    #             # true true false false
    #             messages.error(request, 'Введите корректные данные')
    #             return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
    #         elif user1Kabel and user1 and not user2 and user2Kabel:
    #             # true true false true
    #             per_info = PerekidkaInfoNew(
    #                 user1KabelNumber = user1Kabel.number,
    #                 user1KabelNameSurname = f"{user1Kabel.surname} {user1Kabel.name}",

    #                 user1Number = user1.number,
    #                 user1Etrap = user1.etrap,
    #                 user1NameSurname = f"{user1.surname} {user1.name}",

    #                 user2KabelNumber = user2Kabel.number,
    #                 user2KabelNameSurname = f"{user2Kabel.surname} {user2Kabel.name}",

    #                 operator = request.user.username,
    #                 type_perekidka = 'перекидка баланса',
    #             )
    #         elif user1Kabel and user1 and user2 and not user2Kabel:
    #             # true true true false
    #             per_info = PerekidkaInfoNew(
    #                 user1KabelNumber = user1Kabel.number,
    #                 user1KabelNameSurname = f"{user1Kabel.surname} {user1Kabel.name}",

    #                 user1Number = user1.number,
    #                 user1Etrap = user1.etrap,
    #                 user1NameSurname = f"{user1.surname} {user1.name}",

    #                 user2Number = user2.number,
    #                 user2Etrap = user2.etrap,
    #                 user2NameSurname = f"{user2.surname} {user2.name}",

    #                 operator = request.user.username,
    #                 type_perekidka = 'перекидка баланса',
    #             )
    #         elif user1Kabel and user1 and user2 and user2Kabel:
    #             # true true true true
    #             per_info = PerekidkaInfoNew(
    #                 user1KabelNumber = user1Kabel.number,
    #                 user1KabelNameSurname = f"{user1Kabel.surname} {user1Kabel.name}",

    #                 user1Number = user1.number,
    #                 user1Etrap = user1.etrap,
    #                 user1NameSurname = f"{user1.surname} {user1.name}",

    #                 user2Number = user2.number,
    #                 user2Etrap = user2.etrap,
    #                 user2NameSurname = f"{user2.surname} {user2.name}",

    #                 user2KabelNumber = user2Kabel.number,
    #                 user2KabelNameSurname = f"{user2Kabel.surname} {user2Kabel.name}",

    #                 operator = request.user.username,
    #                 type_perekidka = 'перекидка баланса',
    #             )
            
    #         mess = f"""Перекинуто с {number1} на {number2}:
    #     """
    #         mess_kabel = f''

    #         ##################################################################################################################################################################
    #         ########################################################################################################################################################
    #         if not user1Kabel and not user1 and not user2 and not user2Kabel:
    #             # false false false false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #             pass
    #         elif not user1Kabel and not user1 and not user2 and user2Kabel:
    #             # false false false true ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #             pass
    #         elif not user1Kabel and not user1 and user2 and not user2Kabel:
    #             # false false true false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #             pass
    #         elif not user1Kabel and not user1 and user2 and user2Kabel:
    #             # false false true true ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #             pass
    #         elif not user1Kabel and user1 and not user2 and not user2Kabel:
    #             # false true false false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #             pass
    #         elif not user1Kabel and user1 and not user2 and user2Kabel:
    #             # false true false true ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #             ic('Перекидка баланса разные номера')
    #             if priceTel != 0:
    #                 totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                 per_info.telefon1 += priceTel
    #                 user1.b_telefon = 0
    #                 user1.b_slr = 0
    #                 user1.b_kod = 0
    #                 user1.b_zakaz = 0
    #                 user1.b_dop_uslugi = 0
    #                 user1.b_prochee = totalTelefoniya - priceTel
    #                 if user2_column_telefoniya == 'kabel' and user2Kabel:
    #                     per_info.kabel2 += priceTel
    #                     user2Kabel.balance += priceTel
    #                     mess += f"""c телефония на kabel: {priceTel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c Телефония на кабель: {priceTel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c Телефония на кабель: {priceTel} manat
    #     """
    #             if priceInt != 0:
    #                 per_info.internet1 += priceInt
    #                 user1.b_internet -= priceInt
    #                 if user2_column_internet == 'kabel' and user2Kabel:
    #                     per_info.kabel2 += priceInt
    #                     user2Kabel.balance += priceInt
    #                     mess += f"""c internet на kabel: {priceInt} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c Интернет на кабель: {priceInt} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c Интернет на кабель: {priceInt} manat
    #     """
    #             if priceAlem != 0:
    #                 per_info.alem1 += priceAlem
    #                 user1.b_alem -= priceAlem
    #                 if user2_column_alem == 'kabel' and user2Kabel:
    #                     per_info.kabel2 += priceAlem
    #                     user2Kabel.balance += priceAlem
    #                     mess += f"""c alem на kabel: {priceAlem} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c алем на кабель: {priceAlem} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c алем на кабель: {priceAlem} manat
    #     """      
    #             if priceTel != 0 or priceInt != 0 or priceAlem != 0:
    #                 mess += comment
    #                 per_info.comment = mess
    #                 per_info.save()
    #                 if user1:
    #                     user1.save()
    #                     context['user1'] = user1
    #                     context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                 if user2:
    #                     user2.save()
    #                     context['user2'] = user2
    #                     context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
    #                 if user2Kabel:
    #                     user2Kabel.save()
    #                     context['user2Kabel'] = user2Kabel
    #                 if mess_kabel != '':
    #                     KabelComment.objects.create(
    #                         user = user2Kabel,
    #                         worker = request.user.username,
    #                         action = 'Изменения данных',
    #                         comment = f"""{mess_kabel}
    #     Комментарий: {comment}
    #     """)
    #                 messages.success(request, 'Успешная перекидка баланса')
    #             else:
    #                 messages.error(request, 'Все цены перекидки 0')
    #         elif not user1Kabel and user1 and user2 and not user2Kabel:
    #             # false true true false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #             if number1 == number2:
    #                 ic('perekidka один и тот же номер')
    #                 if priceTel != 0:
    #                     totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                     per_info.telefon1 += priceTel
    #                     user1.b_telefon = 0
    #                     user1.b_slr = 0
    #                     user1.b_kod = 0
    #                     user1.b_zakaz = 0
    #                     user1.b_dop_uslugi = 0
    #                     user1.b_prochee = totalTelefoniya - priceTel
    #                     if user2_column_telefoniya == 'internet':
    #                         per_info.internet2 += priceTel
    #                         user1.b_internet += priceTel
    #                         mess += f"""c телефония на интернет: {priceTel} манат
    #     """
    #                     if user2_column_telefoniya == 'alem':
    #                         per_info.alem2 += priceTel
    #                         user1.b_alem += priceTel
    #                         mess += f"""c телефония на алем: {priceTel} манат
    #     """
    #                 # с интернета на (тут или на телефония или на алем или на кабель)
    #                 if priceInt != 0:
    #                     per_info.internet1 += priceInt
    #                     user1.b_internet -= priceInt
    #                     # Перекидываем баланс с internet на
    #                     if user2_column_internet == 'telefoniya':
    #                         # Перекидываем с internet в телефония
    #                         per_info.telefon2 += priceInt
    #                         totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                         user1.b_telefon = 0
    #                         user1.b_slr = 0
    #                         user1.b_kod = 0
    #                         user1.b_zakaz = 0
    #                         user1.b_dop_uslugi = 0
    #                         user1.b_prochee = totalTelefoniya + priceInt
    #                         mess += f"""c интернет на телефония: {priceInt} манат
    #     """
    #                     if user2_column_internet == 'alem':
    #                         # Перекидываем с internet в alem
    #                         per_info.alem2 += priceInt
    #                         user1.b_alem += priceInt
    #                         mess += f"""c интернет на алем: {priceInt} манат
    #     """
    #                 # с алем на (тут или на телефония или на интернет или на кабель)
    #                 if priceAlem != 0:
    #                     per_info.alem1 += priceAlem
    #                     user1.b_alem -= priceAlem
    #                     if user2_column_alem == 'telefoniya':
    #                         per_info.telefon2 += priceAlem
    #                         totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                         user1.b_telefon = 0
    #                         user1.b_slr = 0
    #                         user1.b_kod = 0
    #                         user1.b_zakaz = 0
    #                         user1.b_dop_uslugi = 0
    #                         user1.b_prochee = totalTelefoniya + priceAlem
    #                         mess += f"""c alem на телефония: {priceAlem} манат
    #     """
    #                     if user2_column_alem == 'internet':
    #                         per_info.internet2 += priceAlem
    #                         user1.b_internet += priceAlem
    #                         mess += f"""c alem на интернет: {priceAlem} манат
    #     """
    #                 if priceTel != 0 or priceInt != 0 or priceAlem != 0:
    #                     mess += comment
    #                     per_info.comment = mess
    #                     per_info.save()
    #                     if user1:
    #                         user1.save()
    #                         context['user1'] = user1
    #                         context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                     messages.success(request, 'Успешная перекидка баланса')
    #                 else:
    #                     messages.error(request, 'Все цены перекидки 0')
    #             else:
    #                 ic('Перекидка баланса разные номера')
    #                 if priceTel != 0:
    #                     totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                     per_info.telefon1 += priceTel
    #                     user1.b_telefon = 0
    #                     user1.b_slr = 0
    #                     user1.b_kod = 0
    #                     user1.b_zakaz = 0
    #                     user1.b_dop_uslugi = 0
    #                     user1.b_prochee = totalTelefoniya - priceTel
    #                     if user2_column_telefoniya == 'telefoniya':
    #                         per_info.telefon2 += priceTel
    #                         user2.b_prochee += priceTel
    #                         mess += f"""c телефония на телефония: {priceTel} манат
    #     """             
    #                     if user2_column_telefoniya == 'internet':
    #                         per_info.internet2 += priceTel
    #                         user2.b_internet += priceTel
    #                         mess += f"""c телефония на internet: {priceTel} манат
    #     """
    #                     if user2_column_telefoniya == 'alem':
    #                         per_info.alem2 += priceTel
    #                         user2.b_alem += priceTel
    #                         mess += f"""c телефония на alem: {priceTel} манат
    #     """
    #                 if priceInt != 0:
    #                     per_info.internet1 += priceInt
    #                     user1.b_internet -= priceInt
    #                     if user2_column_internet == 'telefoniya':
    #                         per_info.telefon2 += priceInt
    #                         user2.b_prochee += priceInt
    #                         mess += f"""c internet на телефония: {priceInt} манат
    #     """
    #                     if user2_column_internet == 'internet':
    #                         per_info.internet2 += priceInt
    #                         user2.b_internet += priceInt
    #                         mess += f"""c internet на internet: {priceInt} манат
    #     """
    #                     if user2_column_internet == 'alem':
    #                         per_info.alem2 += priceInt
    #                         user2.b_alem += priceInt
    #                         mess += f"""c internet на alem: {priceInt} манат
    #     """
    #                 if priceAlem != 0:
    #                     per_info.alem1 += priceAlem
    #                     user1.b_alem -= priceAlem
    #                     if user2_column_alem == 'telefoniya':
    #                         per_info.telefon2 += priceAlem
    #                         user2.b_prochee += priceAlem
    #                         mess += f"""c alem на телефония: {priceAlem} манат
    #     """
    #                     if user2_column_alem == 'internet':
    #                         per_info.internet2 += priceAlem
    #                         user2.b_internet += priceAlem
    #                         mess += f"""c alem на internet: {priceAlem} манат
    #     """
    #                     if user2_column_alem == 'alem':
    #                         per_info.alem2 += priceAlem
    #                         user2.b_alem += priceAlem
    #                         mess += f"""c alem на alem: {priceAlem} манат
    #     """           
    #                 if priceTel != 0 or priceInt != 0 or priceAlem != 0:
    #                     mess += comment
    #                     per_info.comment = mess
    #                     per_info.save()
    #                     if user1:
    #                         user1.save()
    #                         context['user1'] = user1
    #                         context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                     if user2:
    #                         user2.save()
    #                         context['user2'] = user2
    #                         context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
    #                     messages.success(request, 'Успешная перекидка баланса')
    #                 else:
    #                     messages.error(request, 'Все цены перекидки 0')

    #         elif not user1Kabel and user1 and user2 and user2Kabel:
    #             # false true true true (Тут не возможен вариант когда 2 номера одинаковые но у одного баланса кабель нет а у другого есть, поэтому в таких ситуациях один и тот же номер не возможен) ----------------------------
    #             ic('Перекидка баланса разные номера')
    #             if priceTel != 0:
    #                 totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                 per_info.telefon1 += priceTel
    #                 user1.b_telefon = 0
    #                 user1.b_slr = 0
    #                 user1.b_kod = 0
    #                 user1.b_zakaz = 0
    #                 user1.b_dop_uslugi = 0
    #                 user1.b_prochee = totalTelefoniya - priceTel
    #                 if user2_column_telefoniya == 'telefoniya':
    #                     per_info.telefon2 += priceTel
    #                     user2.b_prochee += priceTel
    #                     mess += f"""c телефония на телефония: {priceTel} манат
    #     """             
    #                 if user2_column_telefoniya == 'internet':
    #                     per_info.internet2 += priceTel
    #                     user2.b_internet += priceTel
    #                     mess += f"""c телефония на internet: {priceTel} манат
    #     """
    #                 if user2_column_telefoniya == 'alem':
    #                     per_info.alem2 += priceTel
    #                     user2.b_alem += priceTel
    #                     mess += f"""c телефония на alem: {priceTel} манат
    #     """
    #                 if user2_column_telefoniya == 'kabel' and user2Kabel:
    #                     per_info.kabel2 += priceTel
    #                     user2Kabel.balance += priceTel
    #                     mess += f"""c телефония на kabel: {priceTel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c Телефония на кабель: {priceTel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c Телефония на кабель: {priceTel} manat
    #     """
    #             if priceInt != 0:
    #                 per_info.internet1 += priceInt
    #                 user1.b_internet -= priceInt
    #                 if user2_column_internet == 'telefoniya':
    #                     per_info.telefon2 += priceInt
    #                     user2.b_prochee += priceInt
    #                     mess += f"""c internet на телефония: {priceInt} манат
    #     """
    #                 if user2_column_internet == 'internet':
    #                     per_info.internet2 += priceInt
    #                     user2.b_internet += priceInt
    #                     mess += f"""c internet на internet: {priceInt} манат
    #     """
    #                 if user2_column_internet == 'alem':
    #                     per_info.alem2 += priceInt
    #                     user2.b_alem += priceInt
    #                     mess += f"""c internet на alem: {priceInt} манат
    #     """
    #                 if user2_column_internet == 'kabel' and user2Kabel:
    #                     per_info.kabel2 += priceInt
    #                     user2Kabel.balance += priceInt
    #                     mess += f"""c internet на kabel: {priceInt} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c Интернет на кабель: {priceInt} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c Интернет на кабель: {priceInt} manat
    #     """
    #             if priceAlem != 0:
    #                 per_info.alem1 += priceAlem
    #                 user1.b_alem -= priceAlem
    #                 if user2_column_alem == 'telefoniya':
    #                     per_info.telefon2 += priceAlem
    #                     user2.b_prochee += priceAlem
    #                     mess += f"""c alem на телефония: {priceAlem} манат
    #     """
    #                 if user2_column_alem == 'internet':
    #                     per_info.internet2 += priceAlem
    #                     user2.b_internet += priceAlem
    #                     mess += f"""c alem на internet: {priceAlem} манат
    #     """
    #                 if user2_column_alem == 'alem':
    #                     per_info.alem2 += priceAlem
    #                     user2.b_alem += priceAlem
    #                     mess += f"""c alem на alem: {priceAlem} манат
    #     """
    #                 if user2_column_alem == 'kabel' and user2Kabel:
    #                     per_info.kabel2 += priceAlem
    #                     user2Kabel.balance += priceAlem
    #                     mess += f"""c alem на kabel: {priceAlem} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c алем на кабель: {priceAlem} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c алем на кабель: {priceAlem} manat
    #     """
    #             if priceTel != 0 or priceInt != 0 or priceAlem != 0:
    #                 mess += comment
    #                 per_info.comment = mess
    #                 per_info.save()
    #                 if user1:
    #                     user1.save()
    #                     context['user1'] = user1
    #                     context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                 if user2:
    #                     user2.save()
    #                     context['user2'] = user2
    #                     context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
    #                 if user2Kabel:
    #                     user2Kabel.save()
    #                     context['user2Kabel'] = user2Kabel
    #                 if mess_kabel != '':
    #                     KabelComment.objects.create(
    #                         user = user2Kabel,
    #                         worker = request.user.username,
    #                         action = 'Изменения данных',
    #                         comment = f"""{mess_kabel}
    #     Комментарий: {comment}
    #     """)

    #                 messages.success(request, 'Успешная перекидка баланса')
    #             else:
    #                 messages.error(request, 'Все цены перекидки 0')
    #         elif user1Kabel and not user1 and not user2 and not user2Kabel:
    #             # true false false false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #             pass
    #         elif user1Kabel and not user1 and not user2 and user2Kabel:
    #             # true false false true (Тут нельзя никак перекинуть если кабельные один и тот же номер) ------------------------------------------------------------------------------------------------------------
    #             ic('Перекидка баланса разные номера')
    #             if priceKabel != 0:
    #                 per_info.kabel1 += priceKabel
    #                 user1Kabel.balance -= priceKabel
    #                 if user2_column_kabel == 'kabel' and user2Kabel:
    #                     per_info.kabel2 += priceKabel
    #                     user2Kabel.balance += priceKabel
    #                     mess += f"""c kabel на kabel: {priceKabel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на кабель: {priceKabel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c кабель на кабель: {priceKabel} manat
    #     """
                
    #             if priceKabel != 0:
    #                 mess += comment
    #                 per_info.comment = mess
    #                 per_info.save()
    #                 if user2Kabel:
    #                     user2Kabel.save()
    #                     context['user2Kabel'] = user2Kabel
    #                 if user1Kabel:
    #                     user1Kabel.save()
    #                     context['user1Kabel'] = user1Kabel
    #                 if mess_kabel != '':
    #                     KabelComment.objects.create(
    #                         user = user1Kabel,
    #                         worker = request.user.username,
    #                         action = 'Изменения данных',
    #                         comment = f"""{mess_kabel}
    #     Комментарий: {comment}
    #     """)
    #                     KabelComment.objects.create(
    #                         user = user2Kabel,
    #                         worker = request.user.username,
    #                         action = 'Изменения данных',
    #                         comment = f"""{mess_kabel}
    #     Комментарий: {comment}
    #     """)

    #                 messages.success(request, 'Успешная перекидка баланса')
    #             else:
    #                 messages.error(request, 'Все цены перекидки 0')
    #         elif user1Kabel and not user1 and user2 and not user2Kabel:
    #             # true false true false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #             ic('Перекидка баланса разные номера')
    #             if priceKabel != 0:
    #                 per_info.kabel1 += priceKabel
    #                 user1Kabel.balance -= priceKabel
    #                 if user2_column_kabel == 'telefoniya':
    #                     per_info.telefon2 += priceKabel
    #                     user2.b_prochee += priceKabel
    #                     mess += f"""c kabel на телефония: {priceKabel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на телефония: {priceKabel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c кабель на телефония: {priceKabel} manat
    #     """
    #                 if user2_column_kabel == 'internet':
    #                     per_info.internet2 += priceKabel
    #                     user2.b_internet += priceKabel
    #                     mess += f"""c kabel на internet: {priceKabel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на интернет: {priceKabel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c кабель на интернет: {priceKabel} manat
    #     """
    #                 if user2_column_kabel == 'alem':
    #                     per_info.alem2 += priceKabel
    #                     user2.b_alem += priceKabel
    #                     mess += f"""c kabel на alem: {priceKabel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на алем: {priceKabel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c кабель на алем: {priceKabel} manat
    #     """
                
    #             if priceKabel != 0:
    #                 mess += comment
    #                 per_info.comment = mess
    #                 per_info.save()
    #                 if user2:
    #                     user2.save()
    #                     context['user2'] = user2
    #                     context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
    #                 if user1Kabel:
    #                     user1Kabel.save()
    #                     context['user1Kabel'] = user1Kabel
    #                 if mess_kabel != '':
    #                     KabelComment.objects.create(
    #                         user = user1Kabel,
    #                         worker = request.user.username,
    #                         action = 'Изменения данных',
    #                         comment = f"""{mess_kabel}
    #     Комментарий: {comment}
    #     """)
    #                 messages.success(request, 'Успешная перекидка баланса')
    #             else:
    #                 messages.error(request, 'Все цены перекидки 0')
    #         elif user1Kabel and not user1 and user2 and user2Kabel:
    #             # true false true true ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #             ic('Перекидка баланса разные номера')
    #             if priceKabel != 0:
    #                 per_info.kabel1 += priceKabel
    #                 user1Kabel.balance -= priceKabel
    #                 if user2_column_kabel == 'telefoniya':
    #                     per_info.telefon2 += priceKabel
    #                     user2.b_prochee += priceKabel
    #                     mess += f"""c kabel на телефония: {priceKabel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на телефония: {priceKabel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c кабель на телефония: {priceKabel} manat
    #     """
    #                 if user2_column_kabel == 'internet':
    #                     per_info.internet2 += priceKabel
    #                     user2.b_internet += priceKabel
    #                     mess += f"""c kabel на internet: {priceKabel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на интернет: {priceKabel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c кабель на интернет: {priceKabel} manat
    #     """
    #                 if user2_column_kabel == 'alem':
    #                     per_info.alem2 += priceKabel
    #                     user2.b_alem += priceKabel
    #                     mess += f"""c kabel на alem: {priceKabel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на алем: {priceKabel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c кабель на алем: {priceKabel} manat
    #     """
    #                 if user2_column_kabel == 'kabel' and user2Kabel:
    #                     per_info.kabel2 += priceKabel
    #                     user2Kabel.balance += priceKabel
    #                     mess += f"""c kabel на kabel: {priceKabel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на кабель: {priceKabel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c кабель на кабель: {priceKabel} manat
    #     """
                
    #             if priceKabel != 0:
    #                 mess += comment
    #                 per_info.comment = mess
    #                 per_info.save()
    #                 if user2:
    #                     user2.save()
    #                     context['user2'] = user2
    #                     context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
    #                 if user2Kabel:
    #                     user2Kabel.save()
    #                     context['user2Kabel'] = user2Kabel
    #                 if user1Kabel:
    #                     user1Kabel.save()
    #                     context['user1Kabel'] = user1Kabel
    #                 if mess_kabel != '':
    #                     KabelComment.objects.create(
    #                         user = user1Kabel,
    #                         worker = request.user.username,
    #                         action = 'Изменения данных',
    #                         comment = f"""{mess_kabel}
    #     Комментарий: {comment}
    #     """)
    #                     KabelComment.objects.create(
    #                         user = user2Kabel,
    #                         worker = request.user.username,
    #                         action = 'Изменения данных',
    #                         comment = f"""{mess_kabel}
    #     Комментарий: {comment}
    #     """)

    #                 messages.success(request, 'Успешная перекидка баланса')
    #             else:
    #                 messages.error(request, 'Все цены перекидки 0')
    #         elif user1Kabel and user1 and not user2 and not user2Kabel:
    #             # true true false false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #             pass
    #         elif user1Kabel and user1 and not user2 and user2Kabel:
    #             # true true false true ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #             ic('Перекидка баланса разные номера')
    #             if priceTel != 0:
    #                 totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                 per_info.telefon1 += priceTel
    #                 user1.b_telefon = 0
    #                 user1.b_slr = 0
    #                 user1.b_kod = 0
    #                 user1.b_zakaz = 0
    #                 user1.b_dop_uslugi = 0
    #                 user1.b_prochee = totalTelefoniya - priceTel
    #                 if user2_column_telefoniya == 'kabel' and user2Kabel:
    #                     per_info.kabel2 += priceTel
    #                     user2Kabel.balance += priceTel
    #                     mess += f"""c телефония на kabel: {priceTel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c Телефония на кабель: {priceTel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c Телефония на кабель: {priceTel} manat
    #     """
    #             if priceInt != 0:
    #                 per_info.internet1 += priceInt
    #                 user1.b_internet -= priceInt
    #                 if user2_column_internet == 'kabel' and user2Kabel:
    #                     per_info.kabel2 += priceInt
    #                     user2Kabel.balance += priceInt
    #                     mess += f"""c internet на kabel: {priceInt} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c Интернет на кабель: {priceInt} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c Интернет на кабель: {priceInt} manat
    #     """
    #             if priceAlem != 0:
    #                 per_info.alem1 += priceAlem
    #                 user1.b_alem -= priceAlem
    #                 if user2_column_alem == 'kabel' and user2Kabel:
    #                     per_info.kabel2 += priceAlem
    #                     user2Kabel.balance += priceAlem
    #                     mess += f"""c alem на kabel: {priceAlem} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c алем на кабель: {priceAlem} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c алем на кабель: {priceAlem} manat
    #     """
    #             if priceKabel != 0:
    #                 per_info.kabel1 += priceKabel
    #                 user1Kabel.balance -= priceKabel
    #                 if user2_column_kabel == 'alem':
    #                     per_info.alem2 += priceKabel
    #                     user2.b_alem += priceKabel
    #                     mess += f"""c kabel на alem: {priceKabel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на алем: {priceKabel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c кабель на алем: {priceKabel} manat
    #     """
    #                 if user2_column_kabel == 'kabel' and user2Kabel:
    #                     per_info.kabel2 += priceKabel
    #                     user2Kabel.balance += priceKabel
    #                     mess += f"""c kabel на kabel: {priceKabel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на кабель: {priceKabel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c кабель на кабель: {priceKabel} manat
    #     """
                
    #             if priceTel != 0 or priceInt != 0 or priceAlem != 0 or priceKabel != 0:
    #                 mess += comment
    #                 per_info.comment = mess
    #                 per_info.save()
    #                 if user1:
    #                     user1.save()
    #                     context['user1'] = user1
    #                     context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                 if user2:
    #                     user2.save()
    #                     context['user2'] = user2
    #                     context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
    #                 if user2Kabel:
    #                     user2Kabel.save()
    #                     context['user2Kabel'] = user2Kabel
    #                 if user1Kabel:
    #                     user1Kabel.save()
    #                     context['user1Kabel'] = user1Kabel
    #                 if mess_kabel != '':
    #                     KabelComment.objects.create(
    #                         user = user1Kabel,
    #                         worker = request.user.username,
    #                         action = 'Изменения данных',
    #                         comment = f"""{mess_kabel}
    #     Комментарий: {comment}
    #     """)
    #                     KabelComment.objects.create(
    #                         user = user2Kabel,
    #                         worker = request.user.username,
    #                         action = 'Изменения данных',
    #                         comment = f"""{mess_kabel}
    #     Комментарий: {comment}
    #     """)

    #                 messages.success(request, 'Успешная перекидка баланса')
    #             else:
    #                 messages.error(request, 'Все цены перекидки 0')
    #         elif user1Kabel and user1 and user2 and not user2Kabel:
    #             # true true true false ------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #             ic('Перекидка баланса разные номера')
    #             if priceTel != 0:
    #                 totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                 per_info.telefon1 += priceTel
    #                 user1.b_telefon = 0
    #                 user1.b_slr = 0
    #                 user1.b_kod = 0
    #                 user1.b_zakaz = 0
    #                 user1.b_dop_uslugi = 0
    #                 user1.b_prochee = totalTelefoniya - priceTel
    #                 if user2_column_telefoniya == 'telefoniya':
    #                     per_info.telefon2 += priceTel
    #                     user2.b_prochee += priceTel
    #                     mess += f"""c телефония на телефония: {priceTel} манат
    #     """             
    #                 if user2_column_telefoniya == 'internet':
    #                     per_info.internet2 += priceTel
    #                     user2.b_internet += priceTel
    #                     mess += f"""c телефония на internet: {priceTel} манат
    #     """
    #                 if user2_column_telefoniya == 'alem':
    #                     per_info.alem2 += priceTel
    #                     user2.b_alem += priceTel
    #                     mess += f"""c телефония на alem: {priceTel} манат
    #     """
    #             if priceInt != 0:
    #                 per_info.internet1 += priceInt
    #                 user1.b_internet -= priceInt
    #                 if user2_column_internet == 'telefoniya':
    #                     per_info.telefon2 += priceInt
    #                     user2.b_prochee += priceInt
    #                     mess += f"""c internet на телефония: {priceInt} манат
    #     """
    #                 if user2_column_internet == 'internet':
    #                     per_info.internet2 += priceInt
    #                     user2.b_internet += priceInt
    #                     mess += f"""c internet на internet: {priceInt} манат
    #     """
    #                 if user2_column_internet == 'alem':
    #                     per_info.alem2 += priceInt
    #                     user2.b_alem += priceInt
    #                     mess += f"""c internet на alem: {priceInt} манат
    #     """
    #             if priceAlem != 0:
    #                 per_info.alem1 += priceAlem
    #                 user1.b_alem -= priceAlem
    #                 if user2_column_alem == 'telefoniya':
    #                     per_info.telefon2 += priceAlem
    #                     user2.b_prochee += priceAlem
    #                     mess += f"""c alem на телефония: {priceAlem} манат
    #     """
    #                 if user2_column_alem == 'internet':
    #                     per_info.internet2 += priceAlem
    #                     user2.b_internet += priceAlem
    #                     mess += f"""c alem на internet: {priceAlem} манат
    #     """
    #                 if user2_column_alem == 'alem':
    #                     per_info.alem2 += priceAlem
    #                     user2.b_alem += priceAlem
    #                     mess += f"""c alem на alem: {priceAlem} манат
    #     """
    #             if priceKabel != 0:
    #                 per_info.kabel1 += priceKabel
    #                 user1Kabel.balance -= priceKabel
    #                 if user2_column_kabel == 'telefoniya':
    #                     per_info.telefon2 += priceKabel
    #                     user2.b_prochee += priceKabel
    #                     mess += f"""c kabel на телефония: {priceKabel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на телефония: {priceKabel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c кабель на телефония: {priceKabel} manat
    #     """
    #                 if user2_column_kabel == 'internet':
    #                     per_info.internet2 += priceKabel
    #                     user2.b_internet += priceKabel
    #                     mess += f"""c kabel на internet: {priceKabel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на интернет: {priceKabel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c кабель на интернет: {priceKabel} manat
    #     """
    #                 if user2_column_kabel == 'alem':
    #                     per_info.alem2 += priceKabel
    #                     user2.b_alem += priceKabel
    #                     mess += f"""c kabel на alem: {priceKabel} манат
    #     """
    #                     if mess_kabel == '':
    #                         mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на алем: {priceKabel} manat
    #     """
    #                     else:
    #                         mess_kabel += f"""c кабель на алем: {priceKabel} manat
    #     """         
    #             if priceTel != 0 or priceInt != 0 or priceAlem != 0 or priceKabel != 0:
    #                 mess += comment
    #                 per_info.comment = mess
    #                 per_info.save()
    #                 if user1:
    #                     user1.save()
    #                     context['user1'] = user1
    #                     context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                 if user2:
    #                     user2.save()
    #                     context['user2'] = user2
    #                     context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
    #                 if user1Kabel:
    #                     user1Kabel.save()
    #                     context['user1Kabel'] = user1Kabel
    #                 if mess_kabel != '':
    #                     KabelComment.objects.create(
    #                         user = user1Kabel,
    #                         worker = request.user.username,
    #                         action = 'Изменения данных',
    #                         comment = f"""{mess_kabel}
    #     Комментарий: {comment}
    #     """)
    #                 messages.success(request, 'Успешная перекидка баланса')
    #             else:
    #                 messages.error(request, 'Все цены перекидки 0')
    #         elif user1Kabel and user1 and user2 and user2Kabel:
    #             # true true true true ------------------------------------------------------------------------------------------------------------------------------------------------------------------------           
    #             if number1 == number2:
    #                 ic('perekidka один и тот же номер')
    #                 if priceTel != 0:
    #                     totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                     per_info.telefon1 += priceTel
    #                     user1.b_telefon = 0
    #                     user1.b_slr = 0
    #                     user1.b_kod = 0
    #                     user1.b_zakaz = 0
    #                     user1.b_dop_uslugi = 0
    #                     user1.b_prochee = totalTelefoniya - priceTel
    #                     if user2_column_telefoniya == 'internet':
    #                         per_info.internet2 += priceTel
    #                         user1.b_internet += priceTel
    #                         mess += f"""c телефония на интернет: {priceTel} манат
    #     """
    #                     if user2_column_telefoniya == 'alem':
    #                         per_info.alem2 += priceTel
    #                         user1.b_alem += priceTel
    #                         mess += f"""c телефония на алем: {priceTel} манат
    #     """
    #                     if user2_column_telefoniya == 'kabel' and user1Kabel:
    #                         if mess_kabel == '':
    #                             mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c телефония на кабель: {priceTel} manat
    #     """
    #                         else:
    #                             mess_kabel += f"""c телефония на кабель: {priceTel} manat
    #     """
    #                         per_info.kabel2 += priceTel
    #                         user1Kabel.balance += priceTel
    #                         mess += f"""c телефония на кабель: {priceTel} манат
    #     """
    #                 # с интернета на (тут или на телефония или на алем или на кабель)
    #                 if priceInt != 0:
    #                     per_info.internet1 += priceInt
    #                     user1.b_internet -= priceInt
    #                     # Перекидываем баланс с internet на
    #                     if user2_column_internet == 'telefoniya':
    #                         # Перекидываем с internet в телефония
    #                         per_info.telefon2 += priceInt
    #                         totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                         user1.b_telefon = 0
    #                         user1.b_slr = 0
    #                         user1.b_kod = 0
    #                         user1.b_zakaz = 0
    #                         user1.b_dop_uslugi = 0
    #                         user1.b_prochee = totalTelefoniya + priceInt
    #                         mess += f"""c интернет на телефония: {priceInt} манат
    #     """
    #                     if user2_column_internet == 'alem':
    #                         # Перекидываем с internet в alem
    #                         per_info.alem2 += priceInt
    #                         user1.b_alem += priceInt
    #                         mess += f"""c интернет на алем: {priceInt} манат
    #     """
    #                     if user2_column_internet == 'kabel' and user1Kabel:
    #                         # Перекидываем с internet в kabel
    #                         if mess_kabel == '':
    #                             mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c интернет на кабель: {priceInt} manat
    #     """
    #                         else:
    #                             mess_kabel += f"""c интернет на кабель: {priceInt} manat
    #     """
    #                         per_info.kabel2 += priceInt
    #                         user1Kabel.balance += priceInt
    #                         mess += f"""c интернет на kabel: {priceInt} манат
    #     """
    #                 # с алем на (тут или на телефония или на интернет или на кабель)
    #                 if priceAlem != 0:
    #                     per_info.alem1 += priceAlem
    #                     user1.b_alem -= priceAlem
    #                     if user2_column_alem == 'telefoniya':
    #                         per_info.telefon2 += priceAlem
    #                         totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                         user1.b_telefon = 0
    #                         user1.b_slr = 0
    #                         user1.b_kod = 0
    #                         user1.b_zakaz = 0
    #                         user1.b_dop_uslugi = 0
    #                         user1.b_prochee = totalTelefoniya + priceAlem
    #                         mess += f"""c alem на телефония: {priceAlem} манат
    #     """
    #                     if user2_column_alem == 'internet':
    #                         per_info.internet2 += priceAlem
    #                         user1.b_internet += priceAlem
    #                         mess += f"""c alem на интернет: {priceAlem} манат
    #     """
    #                     if user2_column_alem == 'kabel' and user1Kabel:
    #                         if mess_kabel == '':
    #                             mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c alem на кабель: {priceAlem} manat
    #     """
    #                         else:
    #                             mess_kabel += f"""c alem на кабель: {priceAlem} manat
    #     """
    #                         per_info.kabel2 += priceAlem
    #                         user1Kabel.balance += priceAlem
    #                         mess += f"""c alem на kabel: {priceAlem} манат
    #     """
    #                 if priceKabel != 0:
    #                     per_info.kabel1 += priceKabel
    #                     user1Kabel.balance -= priceKabel
    #                     if user2_column_kabel == 'telefoniya':
    #                         if mess_kabel == '':
    #                             mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на телефония: {priceKabel} manat
    #     """
    #                         else:
    #                             mess_kabel += f"""c кабель на телефония: {priceKabel} manat
    #     """
    #                         per_info.telefon2 += priceKabel
    #                         totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                         user1.b_telefon = 0
    #                         user1.b_slr = 0
    #                         user1.b_kod = 0
    #                         user1.b_zakaz = 0
    #                         user1.b_dop_uslugi = 0
    #                         user1.b_prochee = totalTelefoniya + priceKabel
    #                         mess += f"""c kabel на телефония: {priceKabel} манат
    #     """
    #                     if user2_column_kabel == 'internet':
    #                         if mess_kabel == '':
    #                             mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на интернет: {priceKabel} manat
    #     """
    #                         else:
    #                             mess_kabel += f"""c кабель на интернет: {priceKabel} manat
    #     """
    #                         per_info.internet2 += priceKabel
    #                         user1.b_internet += priceKabel
    #                         mess += f"""c kabel на интернет: {priceKabel} манат
    #     """
    #                     if user2_column_kabel == 'alem':
    #                         if mess_kabel == '':
    #                             mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на alem: {priceKabel} manat
    #     """
    #                         else:
    #                             mess_kabel += f"""c кабель на alem: {priceKabel} manat
    #     """
    #                         per_info.alem2 += priceKabel
    #                         user1.b_alem += priceKabel
    #                         mess += f"""c kabel на alem: {priceKabel} манат
    #     """

    #                 if priceTel != 0 or priceInt != 0 or priceAlem != 0 or priceKabel != 0:
    #                     mess += comment
    #                     per_info.comment = mess
    #                     per_info.save()
    #                     if user1:
    #                         user1.save()
    #                         context['user1'] = user1
    #                         context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                     if user1Kabel:
    #                         user1Kabel.save()
    #                         context['user1Kabel'] = user1Kabel
    #                     # теперь надо сохранить историю о перекидке в самом кабельном программе если перекидка баланса кабельного была
    #                     if mess_kabel != '':
    #                         KabelComment.objects.create(
    #                             user = user1Kabel,
    #                             worker = request.user.username,
    #                             action = 'Изменения данных',
    #                             comment = f"""{mess_kabel}
    #     Комментарий: {comment}
    #     """
    #                         )
    #                     messages.success(request, 'Успешная перекидка баланса')
    #                 else:
    #                     messages.error(request, 'Все цены перекидки 0')
    #             else:
    #                 ic('Перекидка баланса разные номера')
    #                 if priceTel != 0:
    #                     totalTelefoniya = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                     per_info.telefon1 += priceTel
    #                     user1.b_telefon = 0
    #                     user1.b_slr = 0
    #                     user1.b_kod = 0
    #                     user1.b_zakaz = 0
    #                     user1.b_dop_uslugi = 0
    #                     user1.b_prochee = totalTelefoniya - priceTel
    #                     if user2_column_telefoniya == 'telefoniya':
    #                         per_info.telefon2 += priceTel
    #                         user2.b_prochee += priceTel
    #                         mess += f"""c телефония на телефония: {priceTel} манат
    #     """             
    #                     if user2_column_telefoniya == 'internet':
    #                         per_info.internet2 += priceTel
    #                         user2.b_internet += priceTel
    #                         mess += f"""c телефония на internet: {priceTel} манат
    #     """
    #                     if user2_column_telefoniya == 'alem':
    #                         per_info.alem2 += priceTel
    #                         user2.b_alem += priceTel
    #                         mess += f"""c телефония на alem: {priceTel} манат
    #     """
    #                     if user2_column_telefoniya == 'kabel' and user2Kabel:
    #                         per_info.kabel2 += priceTel
    #                         user2Kabel.balance += priceTel
    #                         mess += f"""c телефония на kabel: {priceTel} манат
    #     """
    #                         if mess_kabel == '':
    #                             mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c Телефония на кабель: {priceTel} manat
    #     """
    #                         else:
    #                             mess_kabel += f"""c Телефония на кабель: {priceTel} manat
    #     """
    #                 if priceInt != 0:
    #                     per_info.internet1 += priceInt
    #                     user1.b_internet -= priceInt
    #                     if user2_column_internet == 'telefoniya':
    #                         per_info.telefon2 += priceInt
    #                         user2.b_prochee += priceInt
    #                         mess += f"""c internet на телефония: {priceInt} манат
    #     """
    #                     if user2_column_internet == 'internet':
    #                         per_info.internet2 += priceInt
    #                         user2.b_internet += priceInt
    #                         mess += f"""c internet на internet: {priceInt} манат
    #     """
    #                     if user2_column_internet == 'alem':
    #                         per_info.alem2 += priceInt
    #                         user2.b_alem += priceInt
    #                         mess += f"""c internet на alem: {priceInt} манат
    #     """
    #                     if user2_column_internet == 'kabel' and user2Kabel:
    #                         per_info.kabel2 += priceInt
    #                         user2Kabel.balance += priceInt
    #                         mess += f"""c internet на kabel: {priceInt} манат
    #     """
    #                         if mess_kabel == '':
    #                             mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c Интернет на кабель: {priceInt} manat
    #     """
    #                         else:
    #                             mess_kabel += f"""c Интернет на кабель: {priceInt} manat
    #     """
    #                 if priceAlem != 0:
    #                     per_info.alem1 += priceAlem
    #                     user1.b_alem -= priceAlem
    #                     if user2_column_alem == 'telefoniya':
    #                         per_info.telefon2 += priceAlem
    #                         user2.b_prochee += priceAlem
    #                         mess += f"""c alem на телефония: {priceAlem} манат
    #     """
    #                     if user2_column_alem == 'internet':
    #                         per_info.internet2 += priceAlem
    #                         user2.b_internet += priceAlem
    #                         mess += f"""c alem на internet: {priceAlem} манат
    #     """
    #                     if user2_column_alem == 'alem':
    #                         per_info.alem2 += priceAlem
    #                         user2.b_alem += priceAlem
    #                         mess += f"""c alem на alem: {priceAlem} манат
    #     """
    #                     if user2_column_alem == 'kabel' and user2Kabel:
    #                         per_info.kabel2 += priceAlem
    #                         user2Kabel.balance += priceAlem
    #                         mess += f"""c alem на kabel: {priceAlem} манат
    #     """
    #                         if mess_kabel == '':
    #                             mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c алем на кабель: {priceAlem} manat
    #     """
    #                         else:
    #                             mess_kabel += f"""c алем на кабель: {priceAlem} manat
    #     """
    #                 if priceKabel != 0:
    #                     per_info.kabel1 += priceKabel
    #                     user1Kabel.balance -= priceKabel
    #                     if user2_column_kabel == 'telefoniya':
    #                         per_info.telefon2 += priceKabel
    #                         user2.b_prochee += priceKabel
    #                         mess += f"""c kabel на телефония: {priceKabel} манат
    #     """
    #                         if mess_kabel == '':
    #                             mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на телефония: {priceKabel} manat
    #     """
    #                         else:
    #                             mess_kabel += f"""c кабель на телефония: {priceKabel} manat
    #     """
    #                     if user2_column_kabel == 'internet':
    #                         per_info.internet2 += priceKabel
    #                         user2.b_internet += priceKabel
    #                         mess += f"""c kabel на internet: {priceKabel} манат
    #     """
    #                         if mess_kabel == '':
    #                             mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на интернет: {priceKabel} manat
    #     """
    #                         else:
    #                             mess_kabel += f"""c кабель на интернет: {priceKabel} manat
    #     """
    #                     if user2_column_kabel == 'alem':
    #                         per_info.alem2 += priceKabel
    #                         user2.b_alem += priceKabel
    #                         mess += f"""c kabel на alem: {priceKabel} манат
    #     """
    #                         if mess_kabel == '':
    #                             mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на алем: {priceKabel} manat
    #     """
    #                         else:
    #                             mess_kabel += f"""c кабель на алем: {priceKabel} manat
    #     """
    #                     if user2_column_kabel == 'kabel' and user2Kabel:
    #                         per_info.kabel2 += priceKabel
    #                         user2Kabel.balance += priceKabel
    #                         mess += f"""c kabel на kabel: {priceKabel} манат
    #     """
    #                         if mess_kabel == '':
    #                             mess_kabel += f"""Перекидка баланса с {number1} на {number2}:
    #     c кабель на кабель: {priceKabel} manat
    #     """
    #                         else:
    #                             mess_kabel += f"""c кабель на кабель: {priceKabel} manat
    #     """
                    
    #                 if priceTel != 0 or priceInt != 0 or priceAlem != 0 or priceKabel != 0:
    #                     mess += comment
    #                     per_info.comment = mess
    #                     per_info.save()
    #                     if user1:
    #                         user1.save()
    #                         context['user1'] = user1
    #                         context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                     if user2:
    #                         user2.save()
    #                         context['user2'] = user2
    #                         context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
    #                     if user2Kabel:
    #                         user2Kabel.save()
    #                         context['user2Kabel'] = user2Kabel
    #                     if user1Kabel:
    #                         user1Kabel.save()
    #                         context['user1Kabel'] = user1Kabel
    #                     if mess_kabel != '':
    #                         KabelComment.objects.create(
    #                             user = user1Kabel,
    #                             worker = request.user.username,
    #                             action = 'Изменения данных',
    #                             comment = f"""{mess_kabel}
    #     Комментарий: {comment}
    #     """)
    #                         KabelComment.objects.create(
    #                             user = user2Kabel,
    #                             worker = request.user.username,
    #                             action = 'Изменения данных',
    #                             comment = f"""{mess_kabel}
    #     Комментарий: {comment}
    #     """)

    #                     messages.success(request, 'Успешная перекидка баланса')
    #                 else:
    #                     messages.error(request, 'Все цены перекидки 0')
    #     # Перекидка только баланс END
    #     #######################################################################################################################################################
    #     #################################################################################################################################################################

    #     if request.method == 'POST' and 'perekidkaAll' in request.POST:
    #         whichPerekidka = request.POST.get('perekidkaAll')
    #         comment = request.POST.get('comment')
    #         if comment == '':
    #             messages.error(request, 'Введите комментарий')
    #             return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
    #         #################################################################################################################################################################
    #         #######################################################################################################################################################
    #         # Перекидка всех данных  START
    #         if whichPerekidka == 'abonent' or whichPerekidka == 'kabel_and_abonent':
    #             ic('perekidka s abonent na abonent')
    #             if user1 and user2 and user1.number != user2.number:
    #                 # Сохраняем логин и договор user2 в OldLoginDogowor если такие есть
    #                 if user2.dogowor and user2.login:
    #                     try:
    #                         OldLoginDogowor.objects.get(login=user2.login, dogowor=user2.dogowor)
    #                         messages.error(request, f'Невозможно сохранить login dogowor абонента {user2.number} в old так как такой old login dogowor уже есть')
    #                         return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
    #                     except:
    #                         hb_for_old_log_dog = ''
    #                         if user2.hb:
    #                             hb_for_old_log_dog = user2.hb.name
    #                         OldLoginDogowor.objects.create(login=user2.login, dogowor=user2.dogowor, etrap=user2.etrap, number=user2.number, is_enterprises=user2.is_enterprises, hb=hb_for_old_log_dog, operator=request.user.username, saved_in_action='Перекидка всех данных')
    #                 # # Сохраняем логин и договор user1 в OldLoginDogowor если такие есть (Не надо так как его логин договор перейдет на новый номер)
    #                 # if user1.dogowor and user1.login:
    #                 #     try:
    #                 #         OldLoginDogowor.objects.get(login=user1.login, dogowor=user1.dogowor)
    #                 #         messages.error(request, f'Невозможно сохранить login dogowor абонента {user1.number} в old так как такой old login dogowor уже есть')
    #                 #         return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
    #                 #     except:
    #                 #         OldLoginDogowor.objects.create(login=user1.login, dogowor=user1.dogowor, etrap=user1.etrap, number=user1.number)

    #                 # Сначала сохраним данные user2 в архив если он занят
    #                 if user2.name or user2.surname:
    #                     user2hb = None
    #                     if user2.hb:
    #                         user2hb = user2.hb
    #                     arhiwUser2 = UserTableArhiw.objects.create(
    #                         number = user2.number,
    #                         etrap = user2.etrap,
    #                         surname = user2.surname,
    #                         name = user2.name,
    #                         street = user2.street,
    #                         home = user2.home,
    #                         flat = user2.flat,
    #                         is_enterprises = user2.is_enterprises,
    #                         account = user2.account,
    #                         accountName = user2.accountName,
    #                         hb = user2hb,     
    #                         internet_connect_date = user2.internet_connect_date,
    #                         internet_disconnect_date = user2.internet_disconnect_date,
    #                         abonplata = user2.abonplata,
    #                         login = user2.login,
    #                         dogowor = user2.dogowor,
    #                         beneficiary = user2.beneficiary,

    #                         b_internet = user2.b_internet,
    #                         b_kabel = user2.b_kabel,
    #                         b_alem = user2.b_alem,
    #                         b_telefon = user2.b_telefon,
    #                         b_slr = user2.b_slr,
    #                         b_kod = user2.b_kod,
    #                         b_zakaz = user2.b_zakaz,
    #                         b_prochee = user2.b_prochee,
    #                         b_dop_uslugi = user2.b_dop_uslugi,

    #                         s_internet = user2.s_internet,
    #                         s_kabel = user2.s_kabel,
    #                         s_alem = user2.s_alem,
    #                         s_telefon = user2.s_telefon,
    #                         s_slr = user2.s_slr,
    #                         s_kod = user2.s_kod,
    #                         s_zakaz = user2.s_zakaz,
    #                         s_prochee = user2.s_prochee,
    #                         s_dop_uslugi = user2.s_dop_uslugi,
                            
    #                         addDate = user2.addDate,
    #                         snyat_date = datetime.now(),
    #                         snyat_bool = True
    #                         )
    #                     if user2.service.exists():
    #                         for i in user2.service.all():
    #                             arhiwUser2.service.add(i)

                    
    #                 # Сохраняем user1 в архив
    #                 user1hb = None
    #                 if user1.hb:
    #                     user1hb = user1.hb
    #                 arhiwUser1 = UserTableArhiw.objects.create(
    #                     number = user1.number,
    #                     etrap = user1.etrap,
    #                     surname = user1.surname,
    #                     name = user1.name,
    #                     street = user1.street,
    #                     home = user1.home,
    #                     flat = user1.flat,
    #                     is_enterprises = user1.is_enterprises,
    #                     account = user1.account,
    #                     accountName = user1.accountName,
    #                     hb = user1hb,     
    #                     internet_connect_date = user1.internet_connect_date,
    #                     internet_disconnect_date = user1.internet_disconnect_date,
    #                     abonplata = user1.abonplata,
    #                     login = user1.login,
    #                     dogowor = user1.dogowor,
    #                     beneficiary = user1.beneficiary,

    #                     b_internet = user1.b_internet,
    #                     b_kabel = user1.b_kabel,
    #                     b_alem = user1.b_alem,
    #                     b_telefon = user1.b_telefon,
    #                     b_slr = user1.b_slr,
    #                     b_kod = user1.b_kod,
    #                     b_zakaz = user1.b_zakaz,
    #                     b_prochee = user1.b_prochee,
    #                     b_dop_uslugi = user1.b_dop_uslugi,

    #                     s_internet = user1.s_internet,
    #                     s_kabel = user1.s_kabel,
    #                     s_alem = user1.s_alem,
    #                     s_telefon = user1.s_telefon,
    #                     s_slr = user1.s_slr,
    #                     s_kod = user1.s_kod,
    #                     s_zakaz = user1.s_zakaz,
    #                     s_prochee = user1.s_prochee,
    #                     s_dop_uslugi = user1.s_dop_uslugi,
                        
    #                     addDate = user1.addDate,
    #                     snyat_date = datetime.now(),
    #                     snyat_bool = True
    #                     )
    #                 if user1.service.exists():
    #                     for i in user1.service.all():
    #                         arhiwUser1.service.add(i)

                    
    #                 # Сохраняем в PerekidkaInfoNew
    #                 totalTelefonBalance = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                 mess = f"""Перекинуто с {user1.number} на {user2.number} c ({user1.name} {user1.surname}) на ({user2.name} {user2.surname}):
    #     с телефония на телефонию: {totalTelefonBalance} manat
    #     с internet на internet: {user1.b_internet} manat
    #     с alem на alem: {user1.b_alem} manat
    #     комментарий: {comment}
    #     """
    #                 PerekidkaInfoNew.objects.create(
    #                     user1Number=user1.number,
    #                     user1Etrap=user1.etrap,
    #                     user1NameSurname=f"{user1.name} {user1.surname}",
    #                     user2Number=user2.number,
    #                     user2Etrap=user2.etrap,
    #                     user2NameSurname=f"{user2.name} {user2.surname}",
    #                     operator=request.user.username,
    #                     comment=mess,
    #                     type_perekidka='полная перекидка',
    #                     internet1=user1.b_internet,
    #                     alem1=user1.b_alem,
    #                     telefon1=totalTelefonBalance,
    #                     internet2=user1.b_internet,
    #                     alem2=user1.b_alem,
    #                     telefon2=totalTelefonBalance,
    #                 )
            

                    
    #                 # Переносим данные с user1 на user2   arhiwUser2.save()
    #                 user1hb = None
    #                 if user1.hb:
    #                     user1hb = user1.hb
                        
    #                 user2.surname = user1.surname
    #                 user2.name = user1.name
    #                 user2.street = user1.street
    #                 user2.home = user1.home
    #                 user2.flat = user1.flat
    #                 user2.sotowyy = user1.sotowyy

    #                 user2.is_enterprises = user1.is_enterprises
    #                 user2.account = user1.account
    #                 user2.hb = user1hb
    #                 user2.abonplata = user1.abonplata
            
    #                 user2.internet_connect_date = user1.internet_connect_date
    #                 user2.internet_disconnect_date = user1.internet_disconnect_date
    #                 user2.beneficiary = user1.beneficiary

    #                 # Сохраняем инфу об установленных и снятых услугах для UstanowkaSnyatieDopUslugHistory START
    #                 if user1.service.exists() or user2.service.exists():

    #                     if user1.service.exists():
    #                         mes1 = f"""Снятие услуг при перекидке с абонента {user1.number} {user1.etrap} на абонент {user2.number} {user2.etrap}:
    #     """
    #                         mes1_count = 0
    #                         for i in user1.service.all():
    #                             mes1_count += 1
    #                             mes1 += f"""{mes1_count}) {i.service}
    #     """
    #                         UstanowkaSnyatieDopUslugHistory.objects.create(
    #                             user=request.user.username,
    #                             which_action='при перекидке',
    #                             which_type='снято',
    #                             number=user1.number,
    #                             etrap=user1.etrap,
    #                             comment = f"""Снято услуг:
    #     {mes1}
    #     Комментарий: {comment}"""
    #                         )

    #                     if user1.service.exists() and user2.service.exists():
    #                         which_type = 'снято и установлено'
    #                     elif user1.service.exists() and not user2.service.exists():
    #                         which_type = 'установлено'
    #                     elif not user1.service.exists() and user2.service.exists():
    #                         which_type = 'снято'
    #                     mes2 = f"""{which_type} услуг при перекидке с абонента {user1.number} {user1.etrap} на абонент {user2.number} {user2.etrap}:
    #     """
    #                     if user2.service.exists():
    #                         mes2 += f"""снято услуг:
    #     """
    #                         mes2_count = 0
    #                         for i in user2.service.all():
    #                             mes2_count += 1
    #                             mes2 += f"""{mes2_count}) {i.service}
    #     """
    #                     if user1.service.exists():
    #                         mes2 += f"""установлено услуг:
    #     """
    #                         count_for_mes2 = 0
    #                         for i in user1.service.all():
    #                             count_for_mes2 += 1
    #                             mes2 += f"""{count_for_mes2}) {i.service}
    #     """ 

    #                     UstanowkaSnyatieDopUslugHistory.objects.create(
    #                         user=request.user.username,
    #                         which_action='при перекидке',
    #                         which_type=which_type,
    #                         number=user2.number,
    #                         etrap=user2.etrap,
    #                         comment = f"""{mes2}
    #     Комментарий: {comment}"""
    #                     )
    #                 # Сохраняем инфу об установленных и снятых услугах для UstanowkaSnyatieDopUslugHistory END


    #                 # удаляем все услуги у абонента2 так как на него должны быть только услуги с абонента1, сохраняем для истории в staffhistory для serviceConnect если услуги есть
    #                 user2OldServices = ''
    #                 user2OldServicesCount = 0   
    #                 if user2.service.exists():  # Проверяем, есть ли связанные услуги
    #                     for old_service in user2.service.all():
    #                         user2OldServicesCount += 1
    #                         user2OldServices += f"\n        {user2OldServicesCount}) {old_service.service}"
    #                     user2.service.clear()  # Очищаем все старые услуги
    #                 else:
    #                     user2OldServices = '\n      Нет услуг'

    #                 # Устанавливаем новые услуги с абонент1 на абонент2, сохраняем для истории в staffhistory для serviceConnect если услуги есть 
    #                 user2NewServicesCount = 0
    #                 user2NewServices = ""

    #                 if user1.service.exists():  # Проверяем, есть ли связанные услуги
    #                     for i in user1.service.all():
    #                         user2NewServicesCount += 1
    #                         user2NewServices += f"\n        {user2NewServicesCount}) {i.service}"
    #                         user2.service.add(i)
    #                 else:
    #                     user2NewServices = '\n      Нет услуг'
                    
    #                 # Сам проццесс сохранения информации об услугах в staffhistory для serviceConnect если услуги есть 
    #                 if user1.service.exists() or user2.service.exists():
    #                     StaffAction.objects.create(user=request.user, comment=f"""Перекидка улуг при полной перекидке в MTB.
    # Перекидка с абонента {user1.number} {user1.etrap} на абонент {user2.number} {user2.etrap}.
    # Перед перекидкой было услуг:
    #     у абонента {user1.number}:{user2NewServices}
    #     у абонента {user2.number}:{user2OldServices}
    # После перекидки стало услуг:
    #     у абонента {user1.number}:
    #         Нет услуг
    #     у абонента {user2.number}:{user2NewServices}
    # """, 
    #                     action='Изменение Услуг')


    #                 user2.login = user1.login
    #                 user2.dogowor = user1.dogowor
                    
    #                 user2.b_internet += user1.b_internet
    #                 user2.b_kabel += user1.b_kabel
    #                 user2.b_alem += user1.b_alem
    #                 user2.b_telefon += user1.b_telefon
    #                 user2.b_slr += user1.b_slr
    #                 user2.b_kod += user1.b_kod
    #                 user2.b_zakaz += user1.b_zakaz
    #                 user2.b_prochee += user1.b_prochee
    #                 user2.b_dop_uslugi += user1.b_dop_uslugi

    #                 user2.addDate = datetime.now()
    #                 user2.snyat_date = None
    #                 user2.snyat_bool = False
    #                 user2.save()
                


    #                 # Очищаем user1
    #                 user1.surname = ''
    #                 user1.name = ''
    #                 user1.street = ''
    #                 user1.home = ''
    #                 user1.flat = ''
    #                 user1.sotowyy = ''
    #                 user1.is_enterprises = False
    #                 user1.account = None
    #                 user1.accountName = ''
    #                 user1.hb = None
    #                 user1.internet_connect_date = None
    #                 user1.internet_disconnect_date = None
    #                 user1.abonplata = ''
    #                 user1.login = ''
    #                 user1.dogowor = ''
    #                 user1.addDate = None
    #                 user1.snyat_date = None
    #                 user1.snyat_bool = False
    #                 user1.beneficiary = False
                    
    #                 if user1.service.exists():
    #                     user1.service.clear()
    #                 user1.b_telefon = 0
    #                 user1.b_slr = 0
    #                 user1.b_kod = 0
    #                 user1.b_zakaz = 0
    #                 user1.b_prochee = 0
    #                 user1.b_dop_uslugi = 0
    #                 user1.b_internet = 0
    #                 user1.b_kabel = 0
    #                 user1.b_alem = 0
    #                 user1.save()

    #                 # refresh context
    #                 if number1:
    #                     if len(number1) < 6:
    #                         try:
    #                             user1 = UserTable.objects.get(etrap=etrap1, number=number1)
    #                         except:
    #                             user1 = False
    #                     else:
    #                         user1 = False
    #                 else:
    #                     user1 = False
    #                 if number2:
    #                     if len(number2) < 6:
    #                         try:
    #                             user2 = UserTable.objects.get(etrap=etrap2, number=number2)
    #                         except:
    #                             user2 = False
    #                     else:
    #                         user2 = False
    #                 else:
    #                     user2 = False

    #                 try:
    #                     user1Kabel = KabelTvNew.objects.get(number=number1)
    #                 except:
    #                     user1Kabel = False

    #                 try:
    #                     user2Kabel = KabelTvNew.objects.get(number=number2)
    #                 except:
    #                     user2Kabel = False

    #                 context['user1'] = user1
    #                 context['user2'] = user2
    #                 context['user2Kabel'] = user2Kabel
    #                 context['user1Kabel'] = user1Kabel
    #                 if user1:
    #                     context['telBalanceUser1'] = user1.b_telefon + user1.b_slr + user1.b_kod + user1.b_zakaz + user1.b_prochee + user1.b_dop_uslugi
    #                 if user2:
    #                     context['telBalanceUser2'] = user2.b_telefon + user2.b_slr + user2.b_kod + user2.b_zakaz + user2.b_prochee + user2.b_dop_uslugi
    #         # Перекидка всех данных только с абонента на абонент END
    #         #######################################################################################################################################################
    #         #################################################################################################################################################################


    #         #################################################################################################################################################################
    #         #######################################################################################################################################################
    #         # Перекидка всех данных только с кабеля на кабель START
    #         if whichPerekidka == 'kabel' or whichPerekidka == 'kabel_and_abonent':
    #             ic('perekidka polnaya s kabel na kabel')
    #             ic(user1Kabel)
    #             if user2Kabel:
    #                 # perekidka на существующий номер (очистить user2Kabel и сохранить на нее данные с user1Kabel)
    #                 ic('perekidka на существующий номер (очистить user2Kabel и сохранить на нее данные с user1Kabel)')
    #                 # для начало создадим кооментарий для номера на который перекидываем данные
    #                 user2KabelComment = KabelComment(user=user2Kabel)
    #                 user2KabelComment.worker = request.user.username
    #                 user2KabelComment.action = 'Изменения данных'

    #                 is_enterprises1 = 'ilat'
    #                 if user1Kabel.is_enterprises:
    #                     is_enterprises1 = 'edara'
    #                 is_enterprises2 = 'ilat'
    #                 if user2Kabel.is_enterprises:
    #                     is_enterprises2 = 'edara'

    #                 is_active1 = 'Отключено'
    #                 if user1Kabel.is_active:
    #                     is_active1 = 'Включено'
    #                 is_active2 = 'Отключено'
    #                 if user2Kabel.is_active:
    #                     is_active2 = 'Включено'
    #                 user2KabelComment.comment = f"""Перекидка данных с {user1Kabel.number} на {user2Kabel.number}:
    #     Изменения этого абонента:
    #         1) Фамилия: с {user2Kabel.surname} на {user1Kabel.surname}
    #         2) Имя: с {user2Kabel.name} на {user1Kabel.name} 
    #         3) Улица: с {user2Kabel.street} на {user1Kabel.street}
    #         4) Дом: с {user2Kabel.home} на {user1Kabel.home}
    #         5) Квартира: с {user2Kabel.flat} на {user1Kabel.flat}
    #         6) Сотовый: с {user2Kabel.sotowyy} на {user1Kabel.sotowyy}
    #         7) Предприятие: с {is_enterprises2} на {is_enterprises1}
    #         8) Статус: с {is_active2} на {is_active1}
    #         9) Баланс: с {user2Kabel.balance} на {user1Kabel.balance + user2Kabel.balance} (перекинуто {user1Kabel.balance} манат)
    #         10) Точек: с {user2Kabel.count} на {user1Kabel.count}
    #         Комментарий при перекидке: {comment}
    #     """
    #                 user2KabelComment.save()

    #                 # Комментарий для номера с которого перекидываем
    #                 user1KabelComment = KabelComment(user=user1Kabel)
    #                 user1KabelComment.worker = request.user.username
    #                 user1KabelComment.action = 'Изменения данных'

    #                 is_enterprises1 = 'ilat'
    #                 if user1Kabel.is_enterprises:
    #                     is_enterprises1 = 'edara'
    #                 is_enterprises2 = 'ilat'
    #                 if user2Kabel.is_enterprises:
    #                     is_enterprises2 = 'edara'

    #                 is_active1 = 'Отключено'
    #                 if user1Kabel.is_active:
    #                     is_active1 = 'Включено'
    #                 is_active2 = 'Отключено'
    #                 if user2Kabel.is_active:
    #                     is_active2 = 'Включено'
    #                 user1KabelComment.comment = f"""Перекидка данных с {user1Kabel.number} на {user2Kabel.number}:
    #     Изменения этого абонента:
    #         1) Статус: с {is_active1} на Отключено
    #         2) Баланс: с {user1Kabel.balance} на 0 (перекинули на {user2Kabel.number})
    #         Комментарий при перекидке: {comment}
    #     """
    #                 user1KabelComment.save()

    #                 # теперь сохраняем 2-й комментарий для PerekidkaInfoNew
    #                 perekidkaInfoNew = PerekidkaInfoNew(
    #                     user1KabelNumber = user1Kabel.number,
    #                     user1KabelNameSurname = f"{user1Kabel.surname} {user1Kabel.name}",
    #                     user2KabelNumber = user2Kabel.number,
    #                     user2KabelNameSurname = f"{user2Kabel.surname} {user2Kabel.name}",
    #                     operator = request.user.username,
    #                     comment = f"""Перекинуто с {user1Kabel.number} на {user2Kabel.number}:
    #     с кабель на кабель: {user1Kabel.balance}
    #     """,
    #                     type_perekidka = 'полная перекидка',
    #                     kabel1=user1Kabel.balance,
    #                     kabel2=user2Kabel.balance,
    #                 )
    #                 perekidkaInfoNew.save()

    #                 # Теперь меняем данные самого абонента на которого перекидывают данные
    #                 user2Kabel.name = user1Kabel.name
    #                 user2Kabel.surname = user1Kabel.surname
    #                 user2Kabel.street = user1Kabel.street
    #                 user2Kabel.home = user1Kabel.home
    #                 user2Kabel.flat = user1Kabel.flat
    #                 user2Kabel.sotowyy = user1Kabel.sotowyy
    #                 user2Kabel.is_enterprises = user1Kabel.is_enterprises
    #                 user2Kabel.is_active = user1Kabel.is_active
    #                 user2Kabel.balance += user1Kabel.balance
    #                 user2Kabel.count = user1Kabel.count
    #                 user2Kabel.save()

    #                 # Теперь меняем данные самого абонента с которого перекидывают данные (просто отключем статус и обнуляем баланс) 
    #                 user1Kabel.is_active = False
    #                 user1Kabel.balance = 0
    #                 user1Kabel.save()
            
                    
    #             else:
    #                 # перекидка на новый номер (создать новый кабельный номер и сохранить на нее данные с user1Kabel)
    #                 ic('перекидка на новый номер (создать новый кабельный номер и сохранить на нее данные с user1Kabel)')
    #                 # Создаем новоый кабель номер и перекидываем все данные старого номера на новый 
    #                 newUserKabel = KabelTvNew(number=number2)
    #                 newUserKabel.name = user1Kabel.name
    #                 newUserKabel.surname = user1Kabel.surname
    #                 newUserKabel.street = user1Kabel.street
    #                 newUserKabel.home = user1Kabel.home
    #                 newUserKabel.flat = user1Kabel.flat
    #                 newUserKabel.sotowyy = user1Kabel.sotowyy
    #                 newUserKabel.is_enterprises = user1Kabel.is_enterprises
    #                 newUserKabel.is_active = user1Kabel.is_active
    #                 newUserKabel.balance += user1Kabel.balance
    #                 newUserKabel.count += user1Kabel.count
    #                 newUserKabel.save()

    #                 # Создаем коментарий для нового номера
    #                 newUserComment = KabelComment(user=newUserKabel)
    #                 newUserComment.worker = request.user.username
    #                 newUserComment.action = 'Добавление абонента'

    #                 is_enterprises = 'Нет'
    #                 if user1Kabel.is_enterprises:
    #                     is_enterprises = 'Да'
    #                 is_active = 'Нет'
    #                 if user1Kabel.is_active:
    #                     is_active = 'Да'
    #                 newUserComment.comment = f"""Переход с номера ({user1Kabel.number} на номер {newUserKabel.number}:)
    #     Фамилия: {user1Kabel.surname}
    #     Имя: {user1Kabel.name}
    #     Улица: {user1Kabel.street}
    #     Дом: {user1Kabel.home}
    #     Квартира: {user1Kabel.flat}
    #     Сотовый: {user1Kabel.sotowyy}
    #     Предприятие: {is_enterprises}
    #     Ативный: {is_active}
    #     Баланс: {user1Kabel.balance}
    #     Точек: {user1Kabel.count}
    #     Комментарий при перекидке: {comment}
    #     """
    #                 newUserComment.save()

    #                 # создаем второй комментарий для PerekidkaInfoNew
    #                 comment2 = PerekidkaInfoNew(
    #                     user1KabelNumber = user1Kabel.number,
    #                     user1KabelNameSurname = f"{user1Kabel.name} {user1Kabel.surname}",
    #                     user2KabelNumber = newUserKabel.number,
    #                     user2KabelNameSurname = f"{newUserKabel.name} {newUserKabel.surname}",
    #                     operator = request.user.username,
    #                     comment = f"""Полная перекидка данных с кабельного на новый кабелный номер, c номера {user1Kabel.number} на новый номер {newUserKabel.number}:
    #     Переход баланса c кабеля на кабель: {user1Kabel.balance}
    #     Комментарий при перекидке: {comment}
    #     """,
    #                     type_perekidka = 'полная перекидка',
    #                     kabel1 = user1Kabel.balance,
    #                     kabel2 = user1Kabel.balance,
    #                 )
    #                 comment2.save()
                    
    #                 # просто отключаем кабель старого номера но данные не удаляем (нет необходимости удалять данные старого номера)
    #                 user1Kabel.is_active = False
    #                 # Создаем комментарий для старого номера
    #                 oldUserComment = KabelComment(user=user1Kabel)
    #                 oldUserComment.worker = request.user.username
    #                 oldUserComment.action = 'Изменения данных'

                
    #                 oldUserComment.comment = f"""Переход с номера ({user1Kabel.number} на номер {newUserKabel.number}:)
    #     Изменения в абоненте {user1Kabel.number}:
    #         1) стаус: (с ON на OFF)
    #         2) перекинули баланс с номера {user1Kabel.number} на новый номер {newUserKabel.number} на сумму {user1Kabel.balance}
    #         3) Баланс нового номера ({newUserKabel.number}) перед перекидкой было 0 
    #         Комментарий при перекидке: {comment}
    #     """
    #                 user1Kabel.balance = 0
    #                 user1Kabel.save()
    #                 oldUserComment.save()

                    

                    
                    

                    
    #         # Перекидка всех данных только с кабеля на кабель END
    #         #######################################################################################################################################################
    #         #################################################################################################################################################################



    #         if whichPerekidka == 'kabel':
    #             mess_word = '(с кабеля на кабель)'
    #         elif whichPerekidka == 'abonent':
    #             mess_word = '(с абонента на абонент)'
    #         else:
    #             mess_word = '(с абонента на абонент и с кабеля на кабель)'

    #         messages.success(request, f'Успешная перекидка всех данных {mess_word}')



        

    #     return render(request, 'telekom/MATB/NachislitWruchnuyu/perekidka_new.html', context)
# код идеально работает но в ней нет transaction и нет отмены перекидок END
