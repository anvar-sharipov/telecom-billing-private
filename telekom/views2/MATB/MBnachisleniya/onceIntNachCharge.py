from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db import transaction
from django.db.models import Count, Sum, Max
from django.contrib.postgres.aggregates import BoolOr

from datetime import datetime
import urllib.parse
import tablib

from telekom.models import UserTable, YhlasIyul2026InternetNach, NachMinus, StaffAction

import logging

logger = logging.getLogger(__name__)

ALLOWED_USERNAMES = ['Gayyp', 'yhlas_mtb']

SERVICE_TYPE_LABELS = {'internet': 'Internet', 'alem': 'Alem', 'belet': 'Belet'}

# В какое поле NachMinus начислять
NACH_FIELD_BY_SERVICE = {'internet': 'internet', 'alem': 'alem', 'belet': 'belet'}

# С какого баланса UserTable списывать. Belet своего баланса не имеет — списывается с b_internet.
BALANCE_FIELD_BY_SERVICE = {'internet': 'b_internet', 'alem': 'b_alem', 'belet': 'b_internet'}


def build_problem_rows_xlsx_response(rows):
    headers = ('Пользователь', 'Договор', 'Учетное имя', 'Сумма', 'etrap', 'Номер абонента', 'Причина')
    data = tablib.Dataset(headers=headers)
    for row in rows:
        data.append((row['fio'], row['dogowor'], row['login'], row['arenda'], row['etrap'], row['number'], row['reason']))

    filename = f"onceIntNach_charge_problem_rows_{datetime.now().strftime('%Y-%m-%d_%H%M')}.xlsx"
    encoded_filename = urllib.parse.quote(filename.encode('utf-8'))

    response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
    return response


def resolve_users_and_problems(rows, etrap):
    """Повторно проверяет, что каждая строка YhlasIyul2026InternetNach всё ещё
    сопоставляется с реальным абонентом UserTable (по number+etrap, сохранённым при add).
    Возвращает (user_by_number, user_charge_total, problem_rows)."""

    numbers = {r.number for r in rows if r.number}
    users_qs = UserTable.objects.filter(etrap=etrap, number__in=numbers)
    user_by_number = {u.number: u for u in users_qs}

    problem_rows = []
    user_charge_total = {}  # user.pk -> сумма arenda

    for r in rows:
        user = user_by_number.get(r.number) if r.number else None
        if not user:
            problem_rows.append({'fio': r.fio, 'dogowor': r.dogowor, 'login': r.login, 'arenda': r.arenda, 'etrap': r.etrap, 'number': r.number, 'reason': 'Абонент не найден в UserTable по number+etrap (изменился/удалён после add)'})
            continue
        user_charge_total[user.pk] = user_charge_total.get(user.pk, 0) + r.arenda

    return user_by_number, user_charge_total, problem_rows


def get_etraps_data():
    return YhlasIyul2026InternetNach.objects.values('etrap', 'service_type', 'year', 'month').annotate(
        count=Count('id'),
        total_arenda=Sum('arenda'),
        is_nach=BoolOr('is_nach'),
        who_add=Max('who_add'),
    ).order_by('-year', '-month', 'etrap', 'service_type')


def onceIntNachCharge(request):
    context = {}

    if not request.user.is_authenticated:
        messages.error(request, 'Вы не аутентифицированы')
        return redirect('user-login')

    if not (request.user.is_superuser or request.user.username in ALLOWED_USERNAMES):
        messages.error(request, 'Доступ разрешен только администратору')
        return redirect('user-login')

    context['onceIntNachCharge'] = True
    context['matbIndex'] = True
    context['etraps_data'] = get_etraps_data()

    if request.method == 'POST':
        etrap = request.POST.get('etrap') or ''
        service_type = request.POST.get('service_type') or ''
        year = request.POST.get('year') or ''
        month = request.POST.get('month') or ''

        if not etrap:
            messages.error(request, 'Не выбран этрап')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNachCharge.html', context)

        if service_type not in NACH_FIELD_BY_SERVICE:
            messages.error(request, 'Не выбрана услуга')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNachCharge.html', context)

        if not year or not month:
            messages.error(request, 'Не выбран год/месяц начисления')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNachCharge.html', context)

        rows_qs = YhlasIyul2026InternetNach.objects.filter(etrap=etrap, service_type=service_type, year=year, month=month)
        if not rows_qs.exists():
            messages.error(request, f'Этрап "{etrap}" для услуги "{SERVICE_TYPE_LABELS[service_type]}" за {year}-{month} ещё не добавлен (нет записей в YhlasIyul2026InternetNach)')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNachCharge.html', context)

        if rows_qs.filter(is_nach=True).exists():
            messages.error(request, f'Этрап "{etrap}" для услуги "{SERVICE_TYPE_LABELS[service_type]}" за {year}-{month} уже начислен ранее. Повторное начисление запрещено.')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNachCharge.html', context)

        who_add_values = sorted(set(rows_qs.exclude(who_add='').values_list('who_add', flat=True)))
        if not request.user.is_superuser and request.user.username not in who_add_values:
            messages.error(request, f'Начислять может только тот пользователь, который делал добавление ({", ".join(who_add_values) or "неизвестно"})')
            return render(request, 'telekom/MATB/MBnachisleniya/onceIntNachCharge.html', context)

        rows = list(rows_qs)
        user_by_number, user_charge_total, problem_rows = resolve_users_and_problems(rows, etrap)

        if request.POST.get('onceIntNachChargeExportProblems'):
            if not problem_rows:
                messages.success(request, 'Проблемных строк нет')
                return render(request, 'telekom/MATB/MBnachisleniya/onceIntNachCharge.html', context)
            return build_problem_rows_xlsx_response(problem_rows)

        totalCount = len(rows)
        context['chargeEtrap'] = etrap
        context['chargeServiceType'] = SERVICE_TYPE_LABELS[service_type]
        context['chargeYear'] = year
        context['chargeMonth'] = month
        context['totalCount'] = totalCount
        context['problem_count'] = len(problem_rows)
        context['totalArenda'] = float('%.2f' % sum(user_charge_total.values()))
        context['is_test_mode'] = bool(request.POST.get('onceIntNachChargeTest'))

        if context['is_test_mode']:
            messages.success(request, 'Проверка прошла успешно (ничего не начислено)')
        elif problem_rows:
            messages.error(request, f'Начисление запрещено: {len(problem_rows)} проблемных строк из {totalCount}. Скачайте список проблемных строк.')
        else:
            nach_field = NACH_FIELD_BY_SERVICE[service_type]
            balance_field = BALANCE_FIELD_BY_SERVICE[service_type]
            try:
                with transaction.atomic():
                    if YhlasIyul2026InternetNach.objects.select_for_update().filter(etrap=etrap, service_type=service_type, year=year, month=month, is_nach=True).exists():
                        messages.error(request, f'Этрап "{etrap}" для услуги "{SERVICE_TYPE_LABELS[service_type]}" за {year}-{month} уже начислен ранее (повторная проверка).')
                        return render(request, 'telekom/MATB/MBnachisleniya/onceIntNachCharge.html', context)

                    existing_nach = {nm.user_id: nm for nm in NachMinus.objects.filter(user_id__in=user_charge_total.keys(), year=year, month=month)}
                    users_by_pk = {u.pk: u for u in user_by_number.values()}

                    bulk_create_nach = []
                    bulk_update_nach = []
                    bulk_update_user = []

                    for user_pk, total_amount in user_charge_total.items():
                        user = users_by_pk[user_pk]
                        setattr(user, balance_field, getattr(user, balance_field) - total_amount)
                        bulk_update_user.append(user)

                        if user_pk in existing_nach:
                            nm = existing_nach[user_pk]
                            setattr(nm, nach_field, getattr(nm, nach_field) + total_amount)
                            bulk_update_nach.append(nm)
                        else:
                            bulk_create_nach.append(NachMinus(user=user, year=year, month=month, **{nach_field: total_amount}))

                    if bulk_create_nach:
                        NachMinus.objects.bulk_create(bulk_create_nach)
                    if bulk_update_nach:
                        NachMinus.objects.bulk_update(bulk_update_nach, [nach_field])
                    if bulk_update_user:
                        UserTable.objects.bulk_update(bulk_update_user, [balance_field])

                    YhlasIyul2026InternetNach.objects.filter(etrap=etrap, service_type=service_type, year=year, month=month).update(is_nach=True, who_nach=request.user.username, nach_at=datetime.now())

                    StaffAction.objects.create(
                        user=request.user,
                        comment=f'Начисление YhlasIyul2026InternetNach в NachMinus.{nach_field}, этрап {etrap}, {year}-{month}, строк {totalCount}, начислил {request.user.username}',
                        action='Импорт с xlsx Интернет Начисления в БД',
                    )
                messages.success(request, f'Успешно начислено {totalCount} строк ({len(user_charge_total)} абонентов) в NachMinus.{nach_field} (этрап {etrap}, {year}-{month})')
            except Exception as e:
                messages.error(request, f'Ошибка при начислении, тип ошибки == {e}')
                logger.error(f'Ошибка при начислении YhlasIyul2026InternetNach -> NachMinus, тип ошибки == {e}')

        context['etraps_data'] = get_etraps_data()

    return render(request, 'telekom/MATB/MBnachisleniya/onceIntNachCharge.html', context)
