from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Sum, Max

from datetime import datetime

from telekom.models import MilliBillingPay, PayHistory, KabelTvNew, KabelTvPayHistory, UserTable, StaffAction, SaveInfoAboutWhoAddAndNachPaysFromBilling

from django.db import transaction

import logging
logger = logging.getLogger(__name__)


ALLOWED_USERS = ['intizar_gorogly', 'lenashb', 'testMTBDZ', 'AyshatGoroglyMtb', 'GuljahanAkdepeMtb', 'AzizShabatMtb', 'Saryyewa_Gozel_Shabat_MTB', 'BaharKoneurgenchKassa', 'Merjen_Yylally_MTB', 'GozelGubadagMtb', 'SelbiBoldumsazMtb', 'MahymAkdepeMtb', 'Aramedowa_Oguljemal', 'shirmamedowa_gulalek', 'Jumyazowa_Oguljemal', 'Kurbanowa_Gulnabat_Koneurgench', 'Baltabayewa_Sewara_MTB_DGE', 'Ishangulyyewa_Nurjemal_Koneurgench_kassa']


def nachMilliBillingPay(request):
    context = {}

    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.username in ALLOWED_USERS:
            context['nachMilliBillingPay'] = True
            if request.user.is_superuser:
                context['kassaIndex'] = True
            else:
                context['SHBIndex'] = True
                context['matbIndex'] = True
        else:
            messages.error(request, f'Доступ разрешен только администратору')
            return redirect('user-login')
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')

    groups = request.user.groups.all()
    request_user_etrap = None
    for g in groups:
        request_user_etrap, request_user_type = g.name.split('_')

    if request.user.is_superuser and request.user.username == 'admin1':
        request_user_etrap = 'Dashoguz'

    if not request_user_etrap:
        messages.error(request, f'Не достаточно прав')
        return redirect('user-login')

    # Начислять файл может только тот, кто его добавил
    pending_files = MilliBillingPay.objects.filter(who_add_file=request.user.username, is_nach=False).values('file_name').annotate(
        count=Count('id'),
        total_price=Sum('price'),
        when_added_file=Max('when_added_file'),
    ).order_by('-when_added_file')
    context['pending_files'] = pending_files

    need_nach_file_names = []
    for f in pending_files:
        if request.GET.get(f['file_name']):
            need_nach_file_names.append(f['file_name'])
    context['need_nach_file_names'] = need_nach_file_names

    if need_nach_file_names:
        counts = {'Internet': 0, 'Abonplata': 0, 'Alem': 0, 'Kabel': 0}
        totals = {'Internet': 0, 'Abonplata': 0, 'Alem': 0, 'Kabel': 0}

        pays_preview = MilliBillingPay.objects.filter(file_name__in=need_nach_file_names, who_add_file=request.user.username, is_nach=False)
        for p in pays_preview:
            if p.type_pay in counts:
                counts[p.type_pay] += 1
                totals[p.type_pay] += p.price

        total_count = sum(counts.values())
        total_price = float('%.2f' % sum(totals.values()))

        context['counts'] = counts
        context['totals'] = {k: float('%.2f' % v) for k, v in totals.items()}
        context['total_count'] = total_count
        context['total_price'] = total_price

        if request.method != 'POST':
            messages.success(request, f"Есть платежи для начисления")
    else:
        if request.method != 'POST':
            messages.error(request, f"Выберите файлы которые надо начислить")

    if request.method == 'POST' and 'nachislit' in request.POST:
        if not request.POST.get('comment'):
            messages.error(request, f"Оставьте комментарий! Комментарий не может быть пустым")
            return render(request, 'telekom/Kassa/nachMilliBillingPay.html', context)

        if not need_nach_file_names:
            messages.error(request, f"Выберите файлы которые надо начислить")
            return render(request, 'telekom/Kassa/nachMilliBillingPay.html', context)

        # Защита: начислять может только тот, кто добавил файл
        for file_name in need_nach_file_names:
            if MilliBillingPay.objects.filter(file_name=file_name).exclude(who_add_file=request.user.username).exists():
                messages.error(request, f'Начисление запрещено: файл "{file_name}" добавлен другим пользователем.')
                return render(request, 'telekom/Kassa/nachMilliBillingPay.html', context)

        pays = MilliBillingPay.objects.filter(file_name__in=need_nach_file_names, who_add_file=request.user.username, is_nach=False, is_matched=True)

        etrap_number_pk = {}
        for user in UserTable.objects.all():
            etrap_number_pk.setdefault(user.etrap, {})[user.number] = user.pk

        user_pk_val = {}  # {pk: [b_prochee, b_internet, b_alem]}
        kabel_pk_balance = {}  # {pk: balance}
        bulk_create_pay = []
        bulk_create_kabel_pay = []

        errors = []

        for p in pays:
            is_card = 'nagt' not in (p.depository_name or '').lower()

            if p.type_pay == 'Kabel':
                try:
                    user_k = KabelTvNew.objects.get(number=p.number)
                except KabelTvNew.DoesNotExist:
                    errors.append(f'Кабель абонент {p.number} не найден (платёж {p.pk})')
                    continue

                bulk_create_kabel_pay.append(KabelTvPayHistory(
                    user=user_k,
                    pay=p.price,
                    pay_date=p.date or datetime.now(),
                    pay_kassir=p.manager,
                    card=is_card,
                    milli_billing_file_name=p.file_name,
                ))
                kabel_pk_balance[user_k.pk] = kabel_pk_balance.get(user_k.pk, 0) + p.price
                continue

            try:
                user_pk = etrap_number_pk[p.user_etrap][p.number]
            except KeyError:
                errors.append(f'Абонент {p.user_etrap} {p.number} не найден (платёж {p.pk})')
                continue

            if p.type_pay == 'Abonplata':
                v = user_pk_val.setdefault(user_pk, [0, 0, 0])
                v[0] += p.price
                bulk_create_pay.append(PayHistory(abonent_id=user_pk, prochee=p.price, is_card=is_card, kassir=p.manager, kassa=p.depository_name, total=p.price, date=p.date or datetime.now(), type='Default', kassir_etrap=p.kassir_etrap or None, milli_billing_file_name=p.file_name))
            elif p.type_pay == 'Internet':
                v = user_pk_val.setdefault(user_pk, [0, 0, 0])
                v[1] += p.price
                bulk_create_pay.append(PayHistory(abonent_id=user_pk, internet=p.price, is_card=is_card, kassir=p.manager, kassa=p.depository_name, total=p.price, date=p.date or datetime.now(), type='Default', kassir_etrap=p.kassir_etrap or None, milli_billing_file_name=p.file_name))
            elif p.type_pay == 'Alem':
                v = user_pk_val.setdefault(user_pk, [0, 0, 0])
                v[2] += p.price
                bulk_create_pay.append(PayHistory(abonent_id=user_pk, alem=p.price, is_card=is_card, kassir=p.manager, kassa=p.depository_name, total=p.price, date=p.date or datetime.now(), type='Default', kassir_etrap=p.kassir_etrap or None, milli_billing_file_name=p.file_name))
            else:
                errors.append(f'Неизвестный тип платежа {p.type_pay} (платёж {p.pk})')

        if errors:
            messages.error(request, f'Начисление отменено, найдены ошибки: {"; ".join(errors[:10])}')
            return render(request, 'telekom/Kassa/nachMilliBillingPay.html', context)

        try:
            with transaction.atomic():
                bulk_update_user = []
                for pk, v in user_pk_val.items():
                    user = UserTable.objects.get(pk=pk)
                    user.b_prochee += v[0]
                    user.b_internet += v[1]
                    user.b_alem += v[2]
                    bulk_update_user.append(user)
                if bulk_update_user:
                    UserTable.objects.bulk_update(bulk_update_user, ['b_prochee', 'b_internet', 'b_alem'])

                bulk_update_kabel = []
                for pk, balance in kabel_pk_balance.items():
                    user_k = KabelTvNew.objects.get(pk=pk)
                    user_k.balance += balance
                    bulk_update_kabel.append(user_k)
                if bulk_update_kabel:
                    KabelTvNew.objects.bulk_update(bulk_update_kabel, ['balance'])

                if bulk_create_pay:
                    PayHistory.objects.bulk_create(bulk_create_pay)
                if bulk_create_kabel_pay:
                    KabelTvPayHistory.objects.bulk_create(bulk_create_kabel_pay)

                for file_name in need_nach_file_names:
                    MilliBillingPay.objects.filter(file_name=file_name).update(is_nach=True)
                    SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.filter(file_name=file_name).update(
                        etrap_nach=request_user_etrap,
                        who_nach=request.user.username,
                        when_nach=datetime.now(),
                    )

                StaffAction.objects.create(user=request.user, comment=request.POST.get('comment'), action='Начисление платежей Milli Billing')
                messages.success(request, f"Успешно начислены файлы: {', '.join(need_nach_file_names)}")
        except Exception as e:
            messages.error(request, f'ошибка с transaction при начислении, тип ошибки == {e}')
            logger.error(f'ошибка с transaction при начислении Milli Billing == {e}')

        return redirect('nachMilliBillingPay')

    return render(request, 'telekom/Kassa/nachMilliBillingPay.html', context)
