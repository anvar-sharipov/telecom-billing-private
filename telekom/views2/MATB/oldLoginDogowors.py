from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.views2.myFunc.myFunc import get_etrap_and_types
from telekom.models import OldLoginDogowor, StaffAction
import re
import datetime
from django.db.models import Q
from icecream import ic

from django.db import transaction
import logging
logger = logging.getLogger(__name__)



dogowors_words_list = ['DZA', 'DAD', 'DBS', 'DGD', 'DGE', 'DGO', 'DKU', 'DNZ', 'DRB', 'DTB']
def is_valid(s_dogowor):
    # Проверяем, что длина строки >= 4 (чтобы была хотя бы одна цифра)
    if len(s_dogowor) < 4:
        return False
    
    # Проверяем, что первые 3 символа есть в списке допустимых
    prefix = s_dogowor[:3]
    if prefix not in dogowors_words_list:
        return False

    # Проверяем, что после первых 3 символов идут только цифры
    return bool(re.fullmatch(r"\d+", s_dogowor[3:]))




def oldLoginDogowors(request):
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    context = {}

    request_user = request.user
    groups = request_user.groups.all()
    request_user_etrap = ''
    request_user_type = ''

    if not request.user.is_superuser and request.user.username != 'admin1':
        for g in groups:
            request_user_etrap, request_user_type = g.name.split('_')
            if request_user_type == 'MTB':# or request.user.username == 'admin1':
                break

        if request_user_type != 'MTB':
            messages.error(request, 'Не достаточно прав')
            return redirect('HomePage')
    else:
        request_user_etrap = 'Dashoguz'

   
    number_search = request.GET.get("number_search", "")
    etrap_search = request.GET.get("etrap_search", "")
    login_search = request.GET.get("login_search", "")
    dogowor_search = request.GET.get("dogowor_search", "")
    dogowor_alem_search = request.GET.get("dogowor_alem_search", "")
    dogowor_telefoniya_search = request.GET.get("dogowor_telefoniya_search", "")
    dogowor_belet_search = request.GET.get("dogowor_belet_search", "")
    is_enterprises_search = request.GET.get("is_enterprises_search", "")

    if number_search or etrap_search or login_search or dogowor_search or dogowor_alem_search or dogowor_telefoniya_search or dogowor_belet_search or is_enterprises_search:
        if request.user.is_superuser and request.user.username == 'admin1' or request.user.username == 'Gayyp':
            results = OldLoginDogowor.objects.all().order_by('-created_at')
        else:
            results = OldLoginDogowor.objects.filter(etrap=request_user_etrap).order_by('-created_at')


        if number_search:
            results = results.filter(number__icontains=number_search)
        if etrap_search:
            results = results.filter(etrap__icontains=etrap_search)
        if login_search:
            results = results.filter(login__icontains=login_search)
        if dogowor_search:
            results = results.filter(dogowor__icontains=dogowor_search)
        if dogowor_alem_search:
            results = results.filter(dogowor_alem__icontains=dogowor_alem_search)
        if dogowor_telefoniya_search:
            results = results.filter(dogowor_telefoniya__icontains=dogowor_telefoniya_search)
        if dogowor_belet_search:
            results = results.filter(dogowor_belet__icontains=dogowor_belet_search)
        if is_enterprises_search in ["1", "true", "да"]:
            results = results.filter(is_enterprises=True)
        elif is_enterprises_search in ["0", "false", "нет"]:
            results = results.filter(is_enterprises=False)

        context['results'] = results[:10]
        context['search_params'] = {
                "number_search": number_search,
                "etrap_search": etrap_search,
                "login_search": login_search,
                "dogowor_search": dogowor_search,
                "dogowor_alem_search": dogowor_alem_search,
                "dogowor_telefoniya_search": dogowor_telefoniya_search,
                "dogowor_belet_search": dogowor_belet_search,
                "is_enterprises_search": is_enterprises_search,
            }


    context['log'] = request_user_etrap
    context['request_user_etrap'] = request_user_etrap
    context['etrap'] = request.POST.get('etrap')
    context['etraps'] = etraps

    # Если нажал на сохранить
    if request.method == 'POST' and 'old_number' in request.POST:
        if request.POST.get('old_number'):
            old_number = re.sub('[-]', '', request.POST.get('old_number'))
            account = request.POST.get('account')
            

            old_login = request.POST.get('old_login').strip()
            old_dogowor = request.POST.get('old_dogowor').strip()
            old_dogowor_alem = request.POST.get('old_dogowor_alem').strip()
            old_dogowor_telefoniya = request.POST.get('old_dogowor_telefoniya').strip()
            old_dogowor_belet = request.POST.get('old_dogowor_belet').strip()

            edara = request.POST.get('edara')
            hozOrBud = request.POST.get('hozOrBud')

            context['old_number'] = request.POST.get('old_number')
            context['old_login'] = old_login
            context['edara'] = edara
            context['hozOrBud'] = hozOrBud

            if len(old_number) != 5:
                messages.error(request, f"Ошибка! Введите корректный номер телефона")
                return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            if edara and (not hozOrBud or not account):
                messages.error(request, f"Ошибка! Выберите Hoz или Bud и account")
                return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            # Логин и Договор (интернет) — либо оба заполнены, либо оба пустые
            if (old_dogowor and not old_login) or (old_login and not old_dogowor):
                messages.error(request, f"Ошибка! Логин и Договор Интернет должны быть заполнены оба или оба пустые")
                return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            # Хотя бы один из договоров должен быть заполнен
            if not old_dogowor and not old_dogowor_alem and not old_dogowor_telefoniya and not old_dogowor_belet:
                messages.error(request, f"Ошибка! Заполните хотя бы один договор (Интернет, Алем, Телефония, Белет)")
                return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            if old_dogowor and not is_valid(old_dogowor):
                messages.error(request, f"Ошибка! Введите корректный Dogowor")
                return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            if old_dogowor and OldLoginDogowor.objects.filter(dogowor=old_dogowor).exists():
                messages.error(request, f"Такой договор уже есть в Базе")
                return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            if old_login and OldLoginDogowor.objects.filter(login=old_login).exists():
                messages.error(request, f"Такой логин уже есть в Базе")
                return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            if old_dogowor_alem and OldLoginDogowor.objects.filter(dogowor_alem=old_dogowor_alem).exists():
                messages.error(request, f"Такой договор Алем уже есть в Базе")
                return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            if old_dogowor_telefoniya and OldLoginDogowor.objects.filter(dogowor_telefoniya=old_dogowor_telefoniya).exists():
                messages.error(request, f"Такой договор Телефония уже есть в Базе")
                return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            if old_dogowor_belet and OldLoginDogowor.objects.filter(dogowor_belet=old_dogowor_belet).exists():
                messages.error(request, f"Такой договор Белет уже есть в Базе")
                return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            is_enterprises = False
            if edara:
                is_enterprises = True

            try:
                with transaction.atomic():
                    create_kwargs = dict(
                        number=old_number,
                        etrap=request.POST.get('etrap'),
                        operator=request.user.username,
                        saved_in_action='При сохранении в Old',
                        login=old_login,
                        dogowor=old_dogowor,
                        dogowor_alem=old_dogowor_alem,
                        dogowor_telefoniya=old_dogowor_telefoniya,
                        dogowor_belet=old_dogowor_belet,
                    )
                    if edara:
                        create_kwargs['is_enterprises'] = is_enterprises
                        create_kwargs['hb'] = hozOrBud
                        create_kwargs['account'] = account
                    OldLoginDogowor.objects.create(**create_kwargs)
                    StaffAction.objects.create(user=request.user, action="Old Login Dogowor Save", comment=str(datetime.datetime.now()))
                    messages.success(request, f"Успешное сохранение номера {old_number} этрап {request.POST.get('etrap')} логин {old_login} договор {old_dogowor} алем {old_dogowor_alem} телефония {old_dogowor_telefoniya} белет {old_dogowor_belet}")
            except Exception as e:
                messages.error(request, f'Откат при сохранении OLD ошибка с transaction == {e}')
                logger.error(f'==== Откат при сохранении OLD ошибка с transaction == {e}')


        else:
            messages.error(request, f"Ошибка! Введите номер телефона")
            return render(request, 'telekom/MATB/oldLoginDogowors.html', context)


    # Если нажал на изменить
    if request.method == "POST" and 'change_old' in request.POST :
        item_id = request.POST.get('item_id')
        change_etrap = request.POST.get('change_etrap')
        change_number = request.POST.get('change_number')
        change_login = request.POST.get('change_login').strip()
        change_dogowor = request.POST.get('change_dogowor').strip()
        change_dogowor_alem = request.POST.get('change_dogowor_alem').strip()
        change_dogowor_telefoniya = request.POST.get('change_dogowor_telefoniya').strip()
        change_dogowor_belet = request.POST.get('change_dogowor_belet').strip()
        change_edara = True if request.POST.get('change_edara') else False
        change_hozOrBud = request.POST.get('change_hozOrBud')
        change_account = request.POST.get('change_account') if request.POST.get('change_account') else None


        o = OldLoginDogowor.objects.get(pk=item_id)
        old_account  = str(o.account) if o.account else None
        old_is_enterprises = True if o.is_enterprises else False

        if  (   o.number == change_number
            and o.etrap == change_etrap
            and o.login == change_login
            and o.dogowor == change_dogowor
            and o.dogowor_alem == change_dogowor_alem
            and o.dogowor_telefoniya == change_dogowor_telefoniya
            and o.dogowor_belet == change_dogowor_belet
            and o.hb == change_hozOrBud
            and old_account == change_account
            and old_is_enterprises == change_edara):
            messages.error(request, f"Нет изменений")
        else:
            if len(change_number) != 5:
                messages.error(request, f"Ошибка в поле номер")
                return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            if (change_dogowor and not change_login) or (change_login and not change_dogowor):
                messages.error(request, f"Ошибка! Логин и Договор Интернет должны быть заполнены оба или оба пустые")
                return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            if not change_dogowor and not change_dogowor_alem and not change_dogowor_telefoniya and not change_dogowor_belet:
                messages.error(request, f"Ошибка! Заполните хотя бы один договор (Интернет, Алем, Телефония, Белет)")
                return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            if change_dogowor and not is_valid(change_dogowor):
                messages.error(request, f"Ошибка в поле Договор")
                return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            # if OldLoginDogowor.objects.filter(dogowor=change_dogowor).exists():
            #     messages.error(request, f"Такой договор уже есть в OLD")
            #     return render(request, 'telekom/MATB/oldLoginDogowors.html', context)

            # if OldLoginDogowor.objects.filter(login=change_login).exists():
            #     messages.error(request, f"Такой логин уже есть в OLD")
            #     return render(request, 'telekom/MATB/oldLoginDogowors.html', context)


            try:
                with transaction.atomic():
                    if o.number != change_number:
                        o.number = change_number
                    if o.etrap != change_etrap:
                        o.etrap = change_etrap
                    if o.login != change_login:
                        o.login = change_login
                    if o.dogowor != change_dogowor:
                        o.dogowor = change_dogowor
                    if o.dogowor_alem != change_dogowor_alem:
                        o.dogowor_alem = change_dogowor_alem
                    if o.dogowor_telefoniya != change_dogowor_telefoniya:
                        o.dogowor_telefoniya = change_dogowor_telefoniya
                    if o.dogowor_belet != change_dogowor_belet:
                        o.dogowor_belet = change_dogowor_belet
                    if o.hb != change_hozOrBud:
                        o.hb = change_hozOrBud
                    if old_account != change_account:
                        o.account = change_account
                    if old_is_enterprises != change_edara:
                        o.is_enterprises = change_edara
                    o.saved_in_action = 'Изменено в old'
                    o.operator = request.user.username
                    o.save()
                    StaffAction.objects.create(user=request.user, action="Old Login Dogowor Update", comment=str(datetime.datetime.now()))
                    messages.success(request, f"Успешное изменение {o.number}")
            except Exception as e:
                messages.error(request, f'Откат при изменении в OLD ошибка с transaction == {e}')
                logger.error(f'==== Откат при изменении в OLD ошибка с transaction == {e}')
            

    
    # Если нажал на удалить
    if request.method == "POST" and 'delete_old' in request.POST :
        item_id = request.POST.get('item_id')
        # o = OldLoginDogowor.objects.get(pk=item_id)
        try:
            with transaction.atomic():
                o = OldLoginDogowor.objects.select_for_update().get(pk=item_id)
                n = o.number
                o.delete()
                StaffAction.objects.create(user=request.user, action="Old Login Dogowor Delete", comment=str(datetime.datetime.now()))
                messages.success(request, f"Успешное удаление {n}")
        except Exception as e:
            messages.error(request, f'Откат при удалении OLD ошибка с transaction == {e}')
            logger.error(f'==== Откат при удалении OLD ошибка с transaction == {e}')
        





    return render(request, 'telekom/MATB/oldLoginDogowors.html', context)