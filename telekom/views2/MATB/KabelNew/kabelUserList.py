from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.views2.myFunc.myFunc import get_etrap_and_types
from telekom.models import *
# # from telekom.models import AbonentService, DontRepeatYourself, NachMinus, NachisleniyaOtchet, StaffAction, UserTable
# from django.db.models import Sum
from django.db.models import Q
# from calendar import monthrange
from datetime import datetime

from datetime import date

from django.db import transaction
import logging
logger = logging.getLogger(__name__)

# from telekom.models import DontRepeatYourself, NachMinus, NachisleniyaOtchet, PayHistory, StaffAction, UserTable

# from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup, monthСonvert

def get_user_data_from_request(request):
    number = request.POST.get('number')
    surname = request.POST.get('surname').capitalize()
    name = request.POST.get('name').capitalize()
    street = request.POST.get('street')
    home = request.POST.get('home')
    flat = request.POST.get('flat')
    sotowyy = request.POST.get('sotowyy')
    is_enterprises = True if request.POST.get('is_enterprises') else False
    count = request.POST.get('count')
    comment = request.POST.get('comment')
    is_active = True if request.POST.get('is_active') else False

    return {
        'number': number,
        'surname': surname,
        'name': name,
        'street': street,
        'home': home,
        'flat': flat,
        'sotowyy': sotowyy,
        'is_enterprises': is_enterprises,
        'count': count,
        'comment': comment,
        'is_active': is_active,
    }


def kabelUserList(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            log = 'Dashoguz'
            context['KabelNew'] = True
            context['KabelNewDropDown'] = True
            context['is_allow_to_change_base'] = True
            context['is_allow_to_pay'] = True
        else:
            etrap_types = get_etrap_and_types(request.user)
            etraps = etrap_types['etraps']
            log = etraps[0]
            types = etrap_types['types']
            if 'subadmin' in request.user.username:
                context['is_allow_to_change_base'] = True
                log = 'Dashoguz'
                context['KabelNew'] = True
                context['KabelNewDropDown'] = True
            if 'Kassa' in types:
                context['KabelNewDropDown'] = True
                context['KabelNew'] = True
                context['kassaIndex'] = True
                context['is_allow_to_pay'] = False
                context['is_allow_to_change_base'] = False
            elif 'SHB' in types:
                context['KabelNewDropDown'] = True
                context['KabelNew'] = True
                context['SHBIndex'] = True
                context['is_allow_to_pay'] = False
                context['is_allow_to_change_base'] = False
            elif 'MB' in types:
                context['KabelNewDropDown'] = True
                context['KabelNew'] = True
                context['setService'] = True
                context['is_allow_to_pay'] = False
                context['is_allow_to_change_base'] = False
            elif 'Internet' in types:
                context['KabelNewDropDown'] = True
                context['KabelNew'] = True
                context['internetBilling'] = True
                context['is_allow_to_pay'] = False
                context['is_allow_to_change_base'] = False
            elif 'MTB' in types:
                context['KabelNewDropDown'] = True
                context['KabelNew'] = True
                context['matbIndex'] = True
                context['is_allow_to_pay'] = False
                context['is_allow_to_change_base'] = False
            else:
                messages.error(request, f'У вас нет доступа в Kabel TV')
                return redirect('user-login')
          
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')

    number = request.GET.get('number', '').strip()
    name = request.GET.get('name', '').strip()
    surname = request.GET.get('surname', '').strip()
    street = request.GET.get('street', '').strip()
    home = request.GET.get('home', '').strip()
    flat = request.GET.get('flat', '').strip()
    edara_or_not_left = request.GET.get('edara_or_not_left', '')

    # Находим наименьший свободный id
    get_users = KabelTvNew.objects.filter(number__gt=99999).order_by('-number')
    context['smallest_empty_id'] = get_users[0].number + 1 if get_users else 1
  

    current_date = str(date.today())
    year, month, day = current_date.split('-')
    context['year'] = year
    reversed_date_str = f"{day}-{month}-{year}"
    context['reversed_date_str'] = reversed_date_str

    # Поиск по номеру
    if number:
        if number.isdigit():
            users = KabelTvNew.objects.filter(number=number)
        else:
            users = []
        context['number'] = number
    # поиск по фильтру
    elif any([name, surname, street, home, flat, edara_or_not_left]):
        context.update({
            'name': name,
            'surname': surname,
            'street': street,
            'home': home,
            'flat': flat,
            'edara_or_not_left': edara_or_not_left
        })

        if edara_or_not_left:
            users = KabelTvNew.objects.filter(is_enterprises=True).order_by('-is_active')
        else:
            users = KabelTvNew.objects.filter(
                Q(name__icontains=name) &
                Q(surname__icontains=surname) &
                Q(street__icontains=street) &
                Q(home__icontains=home) &
                Q(flat__icontains=flat)
            ).order_by('-is_active')[:50]    
    else:
        users = []

    for user in users:
        user.sorted_payments = user.kabeltvpayhistory_set.order_by('-pay_date')
        user.kabel_price = 10 + ((user.count - 1) * 5)
    context['users'] = users if users else False

    if len(users) == 1:
        number_for_shapka = users[0].number
        context['number_for_shapka'] = number_for_shapka


    



    # Нажал на оплатить
    if request.method == 'POST' and 'payKabel' in request.POST:
        try:
            with transaction.atomic():
                card = True if request.POST.get('is_card') else False
                pk = request.POST.get('hiddenPk')
                paySum = request.POST.get('payKabel')
                try:
                    payKabel = float(paySum.replace(",", ".")) if ',' in paySum else float(paySum)
                except:
                    messages.error(request, f"Ошибка в сумме платежа: {paySum}")
                    users = KabelTvNew.objects.filter(pk=pk)
                    for user in users:
                        user.sorted_payments = user.kabeltvpayhistory_set.order_by('-pay_date')
                    context['users'] = users
                    context['number'] = users[0].number
                    return render(request, 'telekom/MATB/KabelNew/kabelUserList.html', context)

                KabelTvPayHistory.objects.create(
                    user = KabelTvNew.objects.get(pk=pk),
                    pay = payKabel,
                    pay_kassir = request.user.username,
                    card = card,
                    pay_date = datetime.now()
                )
                users = KabelTvNew.objects.filter(pk=pk)
                for user in users:
                    user.sorted_payments = user.kabeltvpayhistory_set.order_by('-pay_date')
                    user.kabel_price = 10 + ((user.count - 1) * 5)
                    user.balance += float(payKabel)
                    user.save()
                context['users'] = users
                context['number'] = users[0].number
                context['success_pay'] = True
        except Exception as e:
            messages.error(request, f'Откат платежа ошибка с transaction == {e}')
            logger.error(f'==== Откат платежа ошибка с transaction при платеже == {e}')

    
    # Нажал на добавить
    if request.method == 'POST' and 'add_user_form' in request.POST:
        try:
            with transaction.atomic():
                user_data = get_user_data_from_request(request)
                currect = True
                if not user_data['number']:
                    currect = False
                    context['errorEnteredNumber'] = True
                    context['errorNumberIsEmpty'] = True
                else:
                    try:
                        # если номер уже занят
                        KabelTvNew.objects.get(number=user_data['number'])
                        currect = False
                        context['errorEnteredNumber'] = True
                        context['errorNumberIsAlreadyExist'] = user_data['number']
                    except:
                        pass
                if not (user_data['name'] or user_data['surname']):
                    currect = False
                    context['errorEnteredNameSurname'] = True
                if len(user_data['sotowyy']) not in {0, 11}:
                    context['errorEnteredSotowyy'] = True
                    currect = False
                # if not user_data['count']:
                #     currect = False
                try:
                    int(user_data['count'])
                    if int(user_data['count']) > 50:
                        context['errorEnteredCount'] = True
                        context['errorCountMoreThan50'] = True
                        currect = False
                    else:
                        pass
                except:
                    context['errorEnteredCount'] = True
                    context['errorCountEmpty'] = True
                    currect = False
                if len(user_data['comment']) <= 12:
                    context['errorEnteredComment'] = True
                    currect = False

                # Если все поля заполнены правильно сохраняем нового абонента
                if currect:
                    user = KabelTvNew.objects.create(
                        number = user_data['number'],
                        surname = user_data['surname'],
                        name = user_data['name'],
                        street = user_data['street'],
                        home = user_data['home'],
                        flat = user_data['flat'],
                        sotowyy = user_data['sotowyy'],
                        is_enterprises = user_data['is_enterprises'],
                        is_active = user_data['is_active'],
                        count = user_data['count']
                    )
                
                    users = KabelTvNew.objects.filter(pk=user.pk)
                    for user in users:
                        user.sorted_payments = user.kabeltvpayhistory_set.order_by('-pay_date')
                        user.kabel_price = 10 + ((user.count - 1) * 5)
                    context['users'] = users
                    context['new_user_added'] = True
                    context['number'] = user.number
                    messages.success(request, f"Новый пользователь успешно добавлен: {user.number} {user.surname} {user.name}")

                    KabelComment.objects.create(
                        user=user,
                        worker = request.user.username,
                        comment = f"""Комментарий: {user_data['comment']}  
                            Имя: {user.surname} {user.name}
                            Номер: {user.number}
                            Улица: {user.street}
                            Дом: {user.home}
                            Квартира: {user.flat}
                            Мобильный: {user.sotowyy}
                            П/Н.: {'Предприятие' if user.is_enterprises else 'Население'}
                            Статус: {'Включен' if user.is_active else 'Отключен'}
                            Точек: {user.count}""",
                        action = 'Добавление абонента'
                    )
                else:
                    context.update({
                    'add_user_number': user_data['number'],
                    'add_user_name': user_data['name'],
                    'add_user_surname': user_data['surname'],
                    'add_user_street': user_data['street'],
                    'add_user_home': user_data['home'],
                    'add_user_flat': user_data['flat'],
                    'add_user_sotowyy': user_data['sotowyy'],
                    'add_user_is_enterprises': user_data['is_enterprises'],
                    'add_user_is_active': user_data['is_active'],
                    'add_user_count': user_data['count'],
                    'add_user_comment': user_data['comment'],
                })
                    messages.error(request, "Ошибка при заполнении полей")
        except Exception as e:
            messages.error(request, f'Откат добавления ошибка с transaction == {e}')
            logger.error(f'==== Откат добавления ошибка с transaction при добавлении == {e}')


    # Нажал на Изменить
    if request.method == 'POST' and 'change_user_form_pk' in request.POST:
        try:
            with transaction.atomic():
                user_data = get_user_data_from_request(request)
                
                user = KabelTvNew.objects.get(pk=request.POST.get('change_user_form_pk'))
                users = KabelTvNew.objects.filter(pk=user.pk)
                for user in users:
                    user.sorted_payments = user.kabeltvpayhistory_set.order_by('-pay_date')
                    user.kabel_price = 10 + ((user.count - 1) * 5)
                context['users'] = users
                context['number'] = user.number
                

                currect = True
                if not user_data['number']:
                    context['errorEnteredNumber'] = True
                    context['errorNumberIsEmpty'] = True
                    currect = False
                else:
                    try:
                        KabelTvNew.objects.get(number=user_data['number']) #.exists() and user.number != int(user_data['number']):
                        if user.number != int(user_data['number']):
                            context['errorEnteredNumber'] = True
                            context['errorNumberIsAlreadyExist'] = user_data['number']
                        if user.number != int(user_data['number']):
                            context['errorEnteredNumber'] = True
                            context['errorNumberIsAlreadyExist'] = user_data['number']
                    except:
                        pass
                if not (user_data['name'] or user_data['surname']):
                    context['errorEnteredNameSurname'] = True
                    currect = False
                if len(user_data['sotowyy']) not in {0, 11}:
                    context['errorEnteredSotowyy'] = True
                    currect = False
                if not user_data['count']:
                    context['errorEnteredCount'] = True
                    currect = False
                # if int(user_data['count']) > 50:
                #     context['errorEnteredCount'] = True
                #     currect = False
                try:
                    int(user_data['count'])
                    if int(user_data['count']) > 50:
                        context['errorEnteredCount'] = True
                        context['errorCountMoreThan50'] = True
                        currect = False
                    else:
                        pass
                except:
                    context['errorEnteredCount'] = True
                    context['errorCountEmpty'] = True
                    currect = False
                if len(user_data['comment']) <= 12:
                    context['errorEnteredComment'] = True
                    currect = False
                if currect:

                    if (
                        user.number == int(user_data['number']) 
                        and user.surname == user_data['surname']
                        and user.name == user_data['name']
                        and user.street == user_data['street']
                        and user.home == user_data['home']
                        and user.flat == user_data['flat']
                        and user.sotowyy == user_data['sotowyy']
                        and user.is_enterprises == user_data['is_enterprises']
                        and user.count == int(user_data['count'])
                        and user.is_active == user_data['is_active']
                    ):

                        messages.error(request, 'Нет изменений')
                    else:
                        # context.pop('change_user_number', None)
                        # context.pop('change_user_name', None)
                        # context.pop('change_user_surname', None)
                        # context.pop('change_user_street', None)
                        # context.pop('change_user_home', None)
                        # context.pop('change_user_flat', None)
                        # context.pop('change_user_sotowyy', None)
                        # context.pop('change_user_is_enterprises', None)
                        # context.pop('change_user_is_active', None)
                        # context.pop('change_user_count', None)
                        # context.pop('change_user_comment', None)

                        comment_parts = """"""
                                    
                        if user.number != int(user_data['number']):
                            comment_parts += (f"""Смена Номера с {user.number} на {user_data['number']}
                            """)
                            user.number = int(user_data['number'])
                        if user.surname != user_data['surname']:
                            comment_parts += (f"""Смена Фамилии с {user.surname} на {user_data['surname']}
                            """)
                            user.surname = user_data['surname']
                        if user.name != user_data['name']:
                            comment_parts += (f"""Смена Имени с {user.name} на {user_data['name']}
                            """)
                            user.name = user_data['name']
                        if user.street != user_data['street']:
                            comment_parts += (f"""Смена улицы с {user.street} на {user_data['street']}
                            """)
                            user.street = user_data['street']
                        if user.home != user_data['home']:
                            comment_parts += (f"""Смена дома с {user.home} на {user_data['home']}
                            """)
                            user.home = user_data['home']
                        if user.flat != user_data['flat']:
                            comment_parts += (f"""Смена квартиры с {user.flat} на {user_data['flat']}
                            """)
                            user.flat = user_data['flat']
                        if user.sotowyy != user_data['sotowyy']:
                            comment_parts += (f"""Смена мобильного с {user.sotowyy} на {user_data['sotowyy']}
                            """)
                            user.sotowyy = user_data['sotowyy']
                        if user.is_enterprises != user_data['is_enterprises']:
                            comment_parts += (f"""Смена п/н с {user.is_enterprises} на {user_data['is_enterprises']}
                            """)
                            user.is_enterprises = user_data['is_enterprises']
                        if user.is_active != user_data['is_active']:
                            comment_parts += (f"""Смена статуса с {user.is_active} на {user_data['is_active']}
                            """)
                            user.is_active = user_data['is_active']
                        if user.count != int(user_data['count']):
                            comment_parts += (f"""Смена точки с {user.count} на {user_data['count']}
                            """)
                            user.count = user_data['count']
                        
                        user.save()
                        messages.success(request, f"Данные пользователя {user.number} {user.surname} {user.name} изменены")
                        context['user_changed'] = True
                

                        KabelComment.objects.create(
                        user=user,
                        worker = request.user.username,
                        comment = f"""{comment_parts} 
                        {request.POST.get('comment')}""",
                        action = 'Изменения данных'
                    )

                else:
                    context.update({
                        'change_user_number': user_data['number'],
                        'change_user_name': user_data['name'],
                        'change_user_surname': user_data['surname'],
                        'change_user_street': user_data['street'],
                        'change_user_home': user_data['home'],
                        'change_user_flat': user_data['flat'],
                        'change_user_sotowyy': user_data['sotowyy'],
                        'change_user_is_enterprises': user_data['is_enterprises'],
                        'change_user_is_active': user_data['is_active'],
                        'change_user_count': user_data['count'],
                        'change_user_comment': user_data['comment'],
                    })
                    messages.error(request, f"Некоторые поля заполнены неправильно")
        except Exception as e:
            messages.error(request, f'Откат изменении ошибка с transaction == {e}')
            logger.error(f'==== Откат изменении ошибка с transaction при изменении == {e}')

    # Если нажал на перекидку
    if request.method == 'POST' and 'perekidka' in request.POST:
        try:
            with transaction.atomic():

                # Если нажал на перекинуть баланс
                if request.method == 'POST' and 'perekidka1' in request.POST:

                    allow = True
                    per_number = request.POST.get('na_nomer')
                    per_type = request.POST.get('perekidka_type')
                    per_etrap = request.POST.get('perekidka_etrap')
                    numberA = request.POST.get('numberA')
                    userA = KabelTvNew.objects.get(number=numberA)
                    try:
                        per_sum = float(request.POST.get('per_sum')) if "," not in request.POST.get('per_sum') else float(request.POST.get('per_sum').replace(",","."))
                    except:
                        allow = False
                        per_sum = 0
                        messages.error(request, f"Ишибка в колонке сумма перекидки")
                    numberA_bal = float(request.POST.get('numberA_bal')) if "," not in request.POST.get('numberA_bal') else float(request.POST.get('numberA_bal').replace(",","."))
                    per_akt = request.POST.get('per_akt')
                    
                    context['per_number'] = per_number
                    context['per_type'] = per_type
                    context['per_etrap'] = per_etrap
                    context['numberA'] = numberA
                    context['per_sum'] = per_sum
                    context['numberA_bal'] = numberA_bal
                    context['per_akt'] = per_akt



                    if per_sum < 0:
                        allow = False
                        messages.error(request, f"Тут нельзя перекинуть отрицательный баланс")

                    if numberA_bal < per_sum:
                        allow = False
                        messages.error(request, f"Сумма перекидки не может быть больше {numberA_bal} манат")

                    


                    # if float(per_sum) > numberA_bal or float(per_sum) < numberA_bal
                    user = False

                    if allow:
                        if per_type in ['abonplata', 'internet', 'alem']:
                            try:
                                user = UserTable.objects.get(etrap=per_etrap, number=per_number)
                            except:
                                messages.error(request, f"Абонент {per_number} {per_etrap} не найден")

                            if user:
                                prochee = 0
                                internet = 0
                                alem = 0
                                if per_type == 'abonplata':
                                    user.b_prochee += per_sum
                                    prochee = per_sum
                                if per_type == 'internet':
                                    user.b_internet += per_sum
                                    internet = per_sum
                                if per_type == 'alem':
                                    user.b_alem += per_sum
                                    alem = per_sum

                                userA.balance -= per_sum
                                userA.save()
                                user.save()
                                
                                PerekidkaInfo.objects.create(
                                    user1Number = numberA,
                                    user1Etrap = 'Dashoguz',
                                    user2Number = per_number,
                                    user2Etrap = per_etrap,
                                    kabel1=per_sum, 
                                    telefon2=prochee,
                                    internet2 = internet,
                                    alem2 = alem,
                                    comment=per_akt,
                                    operator=request.user
                                )

                                KabelComment.objects.create(
                                    user=userA,
                                    worker = request.user.username,
                                    comment = f"""Перекидка с номера {numberA} на номер {per_number} с kabel на {per_type} сумма {per_sum}, 
                                    {per_akt}""",
                                    action = 'Перекидка'
                                )
                                context['users'] = KabelTvNew.objects.filter(number=numberA)
                                messages.success(request, f"Успешная перекидка с номера {numberA} на номер {per_number} на {per_type}")
                        elif per_type == 'kabel':
                            try:
                                user = KabelTvNew.objects.get(number=per_number)
                            except:
                                messages.error(request, f"Абонент {per_number} {per_etrap} в базе KabelTV не найден")
                            if user:
                                user.balance += per_sum
                                userA.balance -= per_sum
                                user.save()
                                userA.save()
                                KabelComment.objects.create(
                                    user=userA,
                                    worker = request.user.username,
                                    comment = f"""Перекидка с номера {numberA} на номер {per_number} с kabel на {per_type} сумма {per_sum}, 
                                    {per_akt}""",
                                    action = 'Перекидка'
                                )
                                KabelComment.objects.create(
                                    user=user,
                                    worker = request.user.username,
                                    comment = f"""Перекидка с номера {numberA} на номер {per_number} с kabel на {per_type} сумма {per_sum}, 
                                    {per_akt}""",
                                    action = 'Перекидка'
                                )
                                context['users'] = KabelTvNew.objects.filter(number=numberA)
                                messages.success(request, f"Успешная перекидка с номера {numberA} на номер {per_number} с kabel на {per_type} сумма {per_sum}")

                # Если нажал на перекинуть все данные (только для кабель TV)
                if request.method == 'POST' and 'perekidka2' in request.POST:
                    na_etrap = request.POST.get('perekidka_etrap')
                    na_nomer = request.POST.get('na_nomer')
                    numberA = request.POST.get('numberA')
                    per_akt = request.POST.get('per_akt')
                    context['users'] = KabelTvNew.objects.filter(number=numberA)
                    
                    userA = KabelTvNew.objects.get(number=numberA)
                    try:
                        userB = KabelTvNew.objects.get(number=na_nomer)
                    except:
                        userB = KabelTvNew.objects.create(number=na_nomer)

                    userB.name = userA.name
                    userB.surname = userA.surname
                    userB.street = userA.street
                    userB.home = userA.home
                    userB.flat = userA.flat
                    userB.sotowyy = userA.sotowyy
                    userB.is_enterprises = userA.is_enterprises
                    userB.is_active = userA.is_active
                    userB.balance += userA.balance
                    userB.count = userA.count

                    userB.save()
                    userA.is_active = False
                    userA.balance = 0
                    userA.save()

                
                    KabelComment.objects.create(
                        user=userA,
                        worker = request.user.username,
                        comment = f"""Перекидка всех данных с {userA.number} на {userB.number} в частности, 
                        Фамилия: {userB.surname},
                        Имя: {userB.name},
                        Улица: {userB.street},
                        Дом: {userB.home},
                        Кв.: {userB.flat},
                        Сотовый: {userB.sotowyy},
                        Эдара?: {userB.is_enterprises},
                        Актив?: {userB.is_active},
                        Balance: {userB.balance},
                        Точка: {userB.count},
                        {per_akt}""",
                        action = 'Перекидка'
                    )

                    KabelComment.objects.create(
                        user=userB,
                        worker = request.user.username,
                        comment = f"""Перекидка всех данных с {userA.number} на {userB.number} в частности, 
                        Фамилия: {userB.surname},
                        Имя: {userB.name},
                        Улица: {userB.street},
                        Дом: {userB.home},
                        Кв.: {userB.flat},
                        Сотовый: {userB.sotowyy},
                        Эдара?: {userB.is_enterprises},
                        Актив?: {userB.is_active},
                        Balance: {userB.balance},
                        Точка: {userB.count},
                        {per_akt}""",
                        action = 'Перекидка'
                    )
                    messages.success(request, f"Успешная перекидка всех данных с номера {numberA} на номер {na_nomer}")


                # Если нажал возврат
                if request.method == 'POST' and 'wozwrat' in request.POST:
                    print('wozwrat')
        except Exception as e:
            messages.error(request, f'Откат перекидки ошибка с transaction == {e}')
            logger.error(f'==== Откат перекидки ошибка с transaction при перекидке == {e}')

                



    latest_comments = KabelComment.objects.order_by('-comment_add_date')[:1]
    context['latest_comments'] = latest_comments


    return render(request, 'telekom/MATB/KabelNew/kabelUserList.html', context)