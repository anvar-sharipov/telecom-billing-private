from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from datetime import datetime
from telekom.models import *

from django.db import transaction
import logging
logger = logging.getLogger(__name__)




def snyatie_new(request):
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

    
    context['snyatie_new'] = True
    if request_user_type == 'MTB':
        context['matbIndex'] = True 
        context['request_user_etrap'] = request_user_etrap 

    
    if request.method == 'POST' and 'snyat' not in request.POST:
        selected_etrap = request.POST.get('selected_etrap')
        users = UserTable.objects.filter(etrap=selected_etrap, snyat_bool=True)
        context['users'] = users.order_by('-snyat_date')
        context['selected_etrap'] = selected_etrap

    if request.method == 'POST' and 'snyat' in request.POST:
        try:
            with transaction.atomic():
                neSnimat = request.POST.getlist('neSnimat')
                selected_etrap = request.POST.get('selected_etrap')
                context['selected_etrap'] = selected_etrap

                users_for_snyatie = UserTable.objects.filter(etrap=selected_etrap, snyat_bool=True).exclude(pk__in=neSnimat)

                # процесс снятия абонента, проверим сначала все логины и договоры нет ли их в old
                for u in users_for_snyatie:
                    # если есть логин или договор то сохраняем в OldLoginDogowor
                    if u.login and u.dogowor:
                        try:
                            OldLoginDogowor.objects.get(login=u.login, dogowor=u.dogowor)
                            messages.error(request, f'Невозможно сохранить login dogowor абонента {u.number} в old так как такой old login dogowor уже есть')
                            return render(request, 'telekom/MATB/NachislitWruchnuyu/snyatie_new.html', context)
                        except:
                            pass

                # процесс снятия абонента, сохраняем в архив и очищаем номера
                for u in users_for_snyatie:
                    # если есть логин или договор то сохраняем в OldLoginDogowor
                    if u.login and u.dogowor:
                        try:
                            OldLoginDogowor.objects.get(login=u.login, dogowor=u.dogowor)
                            messages.error(request, f'Невозможно сохранить login dogowor абонента {u.number} в old так как такой old login dogowor уже есть')
                            return render(request, 'telekom/MATB/NachislitWruchnuyu/snyatie_new.html', context)
                        except:
                            hb_for_old_log_dog = ''
                            if u.hb:
                                hb_for_old_log_dog = u.hb.name
                            OldLoginDogowor.objects.create(login=u.login, dogowor=u.dogowor, etrap=u.etrap, number=u.number, is_enterprises=u.is_enterprises, hb=hb_for_old_log_dog, operator=request.user.username, saved_in_action='Снятие', account=u.account)

                    # если есть услуги то сохраняем инфу о том что услуги отключаются тут
                    if u.service.exists():
                        services_name = ''
                        services_name_count = 0
                        for s in u.service.all():
                            services_name_count += 1
                            services_name += f"""{services_name_count}) {s.service}
        """
                        StaffAction.objects.create(user=request.user, comment=f"""Удаления улуг при снятии абонента {u.number} {u.etrap} в MTB.
            Снято услуг:
                {services_name}
            """, 
                            action='Изменение Услуг')

                        UstanowkaSnyatieDopUslugHistory.objects.create(
                            user=request.user.username,
                            which_action='при снятии',
                            which_type='снято',
                            number=u.number,
                            etrap=u.etrap,
                            comment = f"""Снятие услуг при снятии абонента {u.number} {u.etrap} (делается в MTB)
            Снято услуг:
                {services_name}"""
                        )
                    # сохраняем в архив
                    u_hb = None
                    if u.hb:
                        u_hb = u.hb
                    arhiw = UserTableArhiw.objects.create(
                        number = u.number,
                        etrap = u.etrap,
                        surname = u.surname,
                        name = u.name,
                        street = u.street,
                        home = u.home,
                        flat = u.flat,
                        is_enterprises = u.is_enterprises,
                        account = u.account,
                        accountName = u.accountName,
                        hb = u_hb,     
                        internet_connect_date = u.internet_connect_date,
                        internet_disconnect_date = u.internet_disconnect_date,
                        abonplata = u.abonplata,
                        login = u.login,
                        dogowor = u.dogowor,
                        beneficiary = u.beneficiary,

                        b_internet = u.b_internet,
                        b_kabel = u.b_kabel,
                        b_alem = u.b_alem,
                        b_telefon = u.b_telefon,
                        b_slr = u.b_slr,
                        b_kod = u.b_kod,
                        b_zakaz = u.b_zakaz,
                        b_prochee = u.b_prochee,
                        b_dop_uslugi = u.b_dop_uslugi,

                        s_internet = u.s_internet,
                        s_kabel = u.s_kabel,
                        s_alem = u.s_alem,
                        s_telefon = u.s_telefon,
                        s_slr = u.s_slr,
                        s_kod = u.s_kod,
                        s_zakaz = u.s_zakaz,
                        s_prochee = u.s_prochee,
                        s_dop_uslugi = u.s_dop_uslugi,
                        
                        addDate = u.addDate,
                        snyat_date = datetime.now(),
                        snyat_bool = True
                        )
                    if u.service.exists():
                        for i in u.service.all():
                            arhiw.service.add(i)

                    # Сохраняем инфу о снятии для истории
                    try:
                        snyatie_info = SnyatieInfo.objects.get(number=u.number, etrap=u.etrap)
                    except:
                        snyatie_info = SnyatieInfo.objects.create(
                                number = u.number,
                                etrap = u.etrap,
                                operator_galochka = request.user.username,
                                date_galochka = datetime.now(),
                                namesurname1 = f"{u.surname} {u.name}",
                                comment_galochka = request.POST.get('comment')
                            )
                    snyatie_info.operator_snyal = request.user.username
                    snyatie_info.date_snyal = datetime.now()
                    snyatie_info.namesurname2 = f"{u.surname} {u.name}"
                    snyatie_info.save()


                    # Очищаем nomer
                    u.surname = ''
                    u.name = ''
                    u.street = ''
                    u.home = ''
                    u.flat = ''
                    u.sotowyy = ''
                    if u.is_enterprises:
                        u.b_telefon = 0
                        u.b_slr = 0
                        u.b_kod = 0
                        u.b_zakaz = 0
                        u.b_prochee = 0
                        u.b_dop_uslugi = 0
                        u.b_internet = 0
                        u.b_alem = 0
                        u.b_kabel = 0
                        u.is_enterprises = False
                    u.account = None
                    u.accountName = ''
                    u.hb = None
                    u.internet_connect_date = None
                    u.internet_disconnect_date = None
                    u.abonplata = ''
                    u.login = ''
                    u.dogowor = ''
                    u.addDate = None
                    u.snyat_date = None
                    u.snyat_bool = False
                    u.beneficiary = False
                    
                    if u.service.exists():
                        u.service.clear()

                    u.save()



                messages.success(request, f'Успешное снятие')
                users = UserTable.objects.filter(etrap=selected_etrap, snyat_bool=True)
                context['users'] = users.order_by('-snyat_date')
        except Exception as e:
            messages.error(request, f'Откат снятия ошибка с transaction == {e}')
            logger.error(f'==== Откат снятия ошибка с transaction при снятии == {e}')



    
    return render(request, 'telekom/MATB/NachislitWruchnuyu/snyatie_new.html', context)