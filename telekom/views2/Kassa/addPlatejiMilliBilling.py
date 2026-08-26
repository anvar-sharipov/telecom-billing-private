from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

from datetime import datetime
import csv
import io
import re
import urllib.parse
import tablib

from telekom.models import KassaExcelFiles, ManagerNames, OldLoginDogowor, UserTable, KabelTvNew, MilliBillingPay, SaveInfoAboutWhoAddAndNachPaysFromBilling, StaffAction

from telekom.views2.myFunc.myFunc import getEtrapNameFromCode, monthСonvert

from django.db import transaction

import logging

logger = logging.getLogger(__name__)


# Соответствие этрапа коду в contractCode/dogowor старого образца (lanbilling)
ETRAP_CODES = {
    'Dashoguz': '322',
    'Akdepe': '344',
    'Boldumsaz': '346',
    'Gorogly': '340',
    'Koneurgench': '347',
    'Turkmenbashy': '349',
    'S.A.Nyyazow': '348',
    'Ruhubelent': '342',
    'Garashsyzlyk': '343',
    'Gubadag': '345',
}

# tariffGroupName (Milli Billing) -> type_pay (как принято в остальном проекте)
TARIFF_TO_TYPE = {
    'Internet': 'Internet',
    'Telefon': 'Abonplata',
    'Älem TV': 'Alem',
    'Kabel TW': 'Kabel',
}

REQUIRED_COLUMNS = {'paymentNumber', 'date', 'userName', 'depositoryName', 'contractCode', 'subscriberFullName', 'tariffGroupName', 'amount', 'currencyName', 'description'}


def normalize_cell(value):
    if value is None:
        return ''
    if isinstance(value, datetime):
        return value.strftime('%d.%m.%Y %H:%M')
    return str(value).strip()


def load_milli_billing_rows(uploaded_file):
    """Читает csv или xlsx выгрузку Milli Billing, возвращает (fieldnames, rows) со строковыми значениями."""
    name_lower = uploaded_file.name.lower()

    if name_lower.endswith('.xlsx'):
        dataset = tablib.Dataset()
        dataset.load(uploaded_file.read(), format='xlsx')
        fieldnames = [str(h).strip() if h is not None else '' for h in (dataset.headers or [])]
        rows = [dict(zip(fieldnames, (normalize_cell(v) for v in row))) for row in dataset]
        return fieldnames, rows

    if name_lower.endswith('.csv'):
        decoded = uploaded_file.read().decode('utf-8-sig')
        reader = csv.DictReader(io.StringIO(decoded), delimiter=';')
        fieldnames = reader.fieldnames or []
        rows = list(reader)
        return fieldnames, rows

    raise ValueError('Файл должен быть формата csv или xlsx (Milli Billing)')


def build_unmatched_xlsx_response(rows, filename_prefix='milli_billing_bez_dogowora'):
    headers = ('paymentNumber', 'date', 'kassir', 'depositoryName', 'contractCode', 'subscriberFullName', 'tariffGroupName', 'amount', 'currency', 'description', 'file_name', 'who_add_file')
    data = tablib.Dataset(headers=headers)
    for p in rows:
        data.append((
            p.payment_number,
            p.date.strftime('%d.%m.%Y %H:%M') if p.date else '',
            p.manager,
            p.depository_name,
            p.contract_code,
            p.subscriber_full_name,
            p.tariff_group_name,
            p.price,
            p.currency_name,
            p.description,
            p.file_name,
            p.who_add_file,
        ))

    filename = f"{filename_prefix}_{datetime.now().strftime('%Y-%m-%d_%H%M')}.xlsx"
    encoded_filename = urllib.parse.quote(filename.encode('utf-8'))

    response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
    response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
    return response


def addPlatejiMilliBilling(request):
    context = {}

    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.username in ['intizar_gorogly', 'lenashb', 'testMTBDZ', 'AyshatGoroglyMtb', 'GuljahanAkdepeMtb', 'AzizShabatMtb', 'Saryyewa_Gozel_Shabat_MTB', 'BaharKoneurgenchKassa', 'Merjen_Yylally_MTB', 'GozelGubadagMtb', 'SelbiBoldumsazMtb', 'MahymAkdepeMtb', 'Aramedowa_Oguljemal', 'shirmamedowa_gulalek', 'Jumyazowa_Oguljemal', 'Kurbanowa_Gulnabat_Koneurgench', 'Baltabayewa_Sewara_MTB_DGE', 'Ishangulyyewa_Nurjemal_Koneurgench_kassa']:
            context['addPlatejiMilliBilling'] = True
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

    months_ru = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    context['months'] = months_ru
    context['years'] = ['2024', '2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']
    context['days'] = [i for i in range(1, 32)]

    today = datetime.now()
    month = request.GET.get('month') or months_ru[today.month - 1]
    year = request.GET.get('year') or str(today.year)
    day = int(request.GET.get('day')) if request.GET.get('day') else today.day

    context['month'] = month
    context['year'] = year
    context['day'] = day

    if request.method == 'POST' and 'milliBillingPlateji' in request.POST:
        if not (year and month and day):
            messages.error(request, f'Выберите год, месяц и день')
            return render(request, 'telekom/Kassa/addPlatejiMilliBilling.html', context)

        day2 = f"0{day}" if len(str(day)) == 1 else str(day)
        month2 = monthСonvert(month)

        try:
            uploaded_file = request.FILES['my_file_milli']
        except Exception:
            messages.error(request, f'Выберите Файл')
            return render(request, 'telekom/Kassa/addPlatejiMilliBilling.html', context)

        try:
            fieldnames, rows = load_milli_billing_rows(uploaded_file)
        except Exception as e:
            messages.error(request, f'Ошибка чтения файла: {e}')
            return render(request, 'telekom/Kassa/addPlatejiMilliBilling.html', context)

        if not REQUIRED_COLUMNS.issubset(set(fieldnames)):
            messages.error(request, f'Не хватает колонок в файле, ожидались: {", ".join(sorted(REQUIRED_COLUMNS))}')
            return render(request, 'telekom/Kassa/addPlatejiMilliBilling.html', context)

        # Защита от дурака: имя файла должно содержать выбранную дату
        need_str = [f'{year}-{month2}-{day2}', f'{day2}-{month2}-{year}', f'{year}.{month2}.{day2}', f'{day2}.{month2}.{year}', f'{year}_{month2}_{day2}', f'{day2}_{month2}_{year}', f'{year} {month2} {day2}', f'{day2} {month2} {year}']
        have_date_in_name = any(i in str(uploaded_file) for i in need_str)
        if not have_date_in_name:
            messages.error(request, f'!Ошибка, дата в названии файла не совпадает с выбранной датой {day2}.{month2}.{year}: {str(uploaded_file)}')
            return render(request, 'telekom/Kassa/addPlatejiMilliBilling.html', context)

        # Защита от дурака: даты в колонке date файла должны совпадать с выбранной датой
        mismatched_dates = []
        for d in rows:
            raw_date = (d.get('date') or '').strip()
            try:
                row_date = datetime.strptime(raw_date, '%d.%m.%Y %H:%M')
            except Exception:
                continue
            if row_date.strftime('%Y') != year or row_date.strftime('%m') != month2 or row_date.strftime('%d') != day2:
                if raw_date not in mismatched_dates:
                    mismatched_dates.append(raw_date)

        if mismatched_dates:
            messages.error(request, f'!Ошибка, в файле есть платежи с датой, отличной от выбранной {day2}.{month2}.{year}: {", ".join(mismatched_dates[:10])}')
            return render(request, 'telekom/Kassa/addPlatejiMilliBilling.html', context)

        # Защита от дурака: имя кассира в названии файла должно совпадать с userName во всех строках
        unique_usernames = {(d.get('userName') or '').strip() for d in rows if (d.get('userName') or '').strip()}
        mismatched_names = [name for name in unique_usernames if name.replace(' ', '_') not in str(uploaded_file) and name not in str(uploaded_file)]
        if mismatched_names:
            messages.error(request, f'!Ошибка, кассир в файле не совпадает с именем в названии файла {str(uploaded_file)}: {", ".join(sorted(mismatched_names))}')
            return render(request, 'telekom/Kassa/addPlatejiMilliBilling.html', context)

        try:
            SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.get(file_name=str(uploaded_file))
            messages.error(request, f'Файл уже добавлен в БД')
            return render(request, 'telekom/Kassa/addPlatejiMilliBilling.html', context)
        except SaveInfoAboutWhoAddAndNachPaysFromBilling.DoesNotExist:
            pass

        managarNames = {}
        for i in ManagerNames.objects.all():
            managarNames[i.name] = i.etrap

        # Предзагрузка абонентов для сопоставления
        code_number_pk = {}
        dogowor_pk = {}
        dogowor_telefoniya_pk = {}
        dogowor_alem_pk = {}
        for user in UserTable.objects.all():
            code = ETRAP_CODES.get(user.etrap)
            if code:
                code_number_pk[f"{code}{user.number}"] = (user.pk, user.number, user.etrap)
            if user.dogowor:
                dogowor_pk[user.dogowor.lower().strip()] = (user.pk, user.number, user.etrap)
            if user.dogowor_telefoniya:
                dogowor_telefoniya_pk[user.dogowor_telefoniya.lower().strip()] = (user.pk, user.number, user.etrap)
            if user.dogowor_alem:
                dogowor_alem_pk[user.dogowor_alem.lower().strip()] = (user.pk, user.number, user.etrap)

        old_login_dogowor = {o.dogowor.upper(): o for o in OldLoginDogowor.objects.exclude(dogowor='')}
        old_login_dogowor_telefoniya = {o.dogowor_telefoniya.upper(): o for o in OldLoginDogowor.objects.exclude(dogowor_telefoniya='')}
        old_login_dogowor_alem = {o.dogowor_alem.upper(): o for o in OldLoginDogowor.objects.exclude(dogowor_alem='')}

        def match_by_old_dogowor(old_login_dict, dogowor_dict, contract_code):
            cc_upper = contract_code.upper()
            if cc_upper in old_login_dict:
                old_user = old_login_dict[cc_upper]
                try:
                    u = UserTable.objects.get(etrap=old_user.etrap, number=old_user.number)
                    return (u.pk, u.number, u.etrap)
                except UserTable.DoesNotExist:
                    return None
            return dogowor_dict.get(contract_code.lower())

        errorManager = []
        bulk_create = []

        counts = {'Internet': 0, 'Abonplata': 0, 'Alem': 0, 'Kabel': 0}
        totals = {'Internet': 0, 'Abonplata': 0, 'Alem': 0, 'Kabel': 0}
        matched_count = 0
        unmatched_count = 0

        for row_num, d in enumerate(rows, start=2):
            manager = (d.get('userName') or '').strip()
            tariff = (d.get('tariffGroupName') or '').strip()
            contract_code = (d.get('contractCode') or '').strip()
            subscriber_full_name = (d.get('subscriberFullName') or '').strip()
            depository_name = (d.get('depositoryName') or '').strip()
            payment_number = (d.get('paymentNumber') or '').strip()
            currency_name = (d.get('currencyName') or '').strip()
            description = (d.get('description') or '').strip()

            try:
                price = float(d.get('amount') or 0)
            except ValueError:
                messages.error(request, f'Некорректная сумма в строке {row_num}: {d.get("amount")}')
                return render(request, 'telekom/Kassa/addPlatejiMilliBilling.html', context)

            try:
                pay_date = datetime.strptime(d.get('date').strip(), '%d.%m.%Y %H:%M')
            except Exception:
                pay_date = None

            type_pay = TARIFF_TO_TYPE.get(tariff)
            if not type_pay:
                # неизвестная категория услуги - сохраняем как есть, без сопоставления
                bulk_create.append(MilliBillingPay(
                    type_pay=tariff or 'Неизвестно',
                    is_matched=False,
                    payment_number=payment_number,
                    depository_name=depository_name,
                    contract_code=contract_code,
                    subscriber_full_name=subscriber_full_name,
                    tariff_group_name=tariff,
                    currency_name=currency_name,
                    description=description,
                    manager=manager,
                    kassir_etrap=managarNames.get(manager, ''),
                    date=pay_date,
                    price=price,
                    file_name=str(uploaded_file),
                    who_add_file=request.user.username,
                ))
                unmatched_count += 1
                continue

            # Проверка менеджера (кассира)
            if manager and manager not in managarNames:
                if manager not in errorManager:
                    errorManager.append(manager)
                    try:
                        with transaction.atomic():
                            ManagerNames.objects.create(name=manager)
                    except Exception as e:
                        messages.error(request, f'ошибка с transaction при сохранении нового менеджера в ManagerNames, тип ошибки == {e}')
                        logger.error(f'ошибка с transaction при сохранении нового менеджера в ManagerNames, тип ошибки == {e}')
                        return render(request, 'telekom/Kassa/addPlatejiMilliBilling.html', context)
                    managarNames[manager] = None
                continue
            elif manager and (managarNames[manager] == '' or managarNames[manager] is None):
                if manager not in errorManager:
                    errorManager.append(manager)
                continue

            match = None  # (pk, number, etrap)

            if type_pay == 'Abonplata':
                digits = re.sub(r'\D', '', contract_code)
                if len(digits) in (10, 11):
                    number = digits[-5:]
                    code = digits[-8:-5]
                    match = code_number_pk.get(f"{code}{number}")
                if not match:
                    match = match_by_old_dogowor(old_login_dogowor_telefoniya, dogowor_telefoniya_pk, contract_code)

            elif type_pay == 'Internet':
                match = match_by_old_dogowor(old_login_dogowor, dogowor_pk, contract_code)

            elif type_pay == 'Alem':
                if contract_code.upper().startswith('IPTV'):
                    digits = re.sub(r'\D', '', contract_code)
                    number = digits[-5:]
                    code = digits[-8:-5]
                    match = code_number_pk.get(f"{code}{number}")
                if not match:
                    match = match_by_old_dogowor(old_login_dogowor_alem, dogowor_alem_pk, contract_code)

            elif type_pay == 'Kabel':
                m = re.search(r'993(\d{3})(\d+)', contract_code)
                if m:
                    try:
                        kabel_user = KabelTvNew.objects.get(number=m.group(2))
                        match = ('kabel', kabel_user.number, 'Dashoguz')
                    except KabelTvNew.DoesNotExist:
                        match = None

            if match:
                _, number, user_etrap = match
                matched_count += 1
                counts[type_pay] += 1
                totals[type_pay] += price
            else:
                number, user_etrap = '', ''
                unmatched_count += 1

            bulk_create.append(MilliBillingPay(
                number=number,
                user_etrap=user_etrap,
                kassir_etrap=managarNames.get(manager, ''),
                type_pay=type_pay,
                is_matched=bool(match),
                payment_number=payment_number,
                depository_name=depository_name,
                contract_code=contract_code,
                subscriber_full_name=subscriber_full_name,
                tariff_group_name=tariff,
                currency_name=currency_name,
                description=description,
                manager=manager,
                date=pay_date,
                price=price,
                file_name=str(uploaded_file),
                who_add_file=request.user.username,
            ))

        if errorManager:
            messages.error(request, f"Есть новые менеджеры, надо определить их этрап")
            context['errorManager'] = errorManager
            return render(request, 'telekom/Kassa/addPlatejiMilliBilling.html', context)

        # Скачать список "без договора" сразу, без сохранения в БД (для предварительного просмотра)
        if request.POST.get('milliBillingExportUnmatched'):
            unmatched_rows = [obj for obj in bulk_create if not obj.is_matched]
            return build_unmatched_xlsx_response(unmatched_rows, filename_prefix='milli_billing_bez_dogowora_preview')

        totalCount = matched_count + unmatched_count
        totalPrice = float('%.2f' % sum(totals.values()))
        context['counts'] = counts
        context['totals'] = {k: float('%.2f' % v) for k, v in totals.items()}
        context['matched_count'] = matched_count
        context['unmatched_count'] = unmatched_count
        context['totalCount'] = totalCount
        context['totalPrice'] = totalPrice
        context['is_test_mode'] = bool(request.POST.get('milliBillingTest'))

        if request.POST.get('milliBillingTest'):
            messages.success(request, f"Проверка прошла успешно (ничего не сохранено в БД)")
        elif unmatched_count > 0:
            messages.error(request, f'Добавление запрещено: {unmatched_count} платежей без найденного договора в базе. Скачайте список "без договора", заведите договора и загрузите файл заново.')
        else:
            try:
                with transaction.atomic():
                    if bulk_create:
                        MilliBillingPay.objects.bulk_create(bulk_create)
                    StaffAction.objects.create(user=request.user, comment=f'Добавления платежей Milli Billing в Базу Данных, файл {str(uploaded_file)}, дата добавления {datetime.now()}, добавил {request.user.username}', action='Добавления платежей в базу')
                    SaveInfoAboutWhoAddAndNachPaysFromBilling.objects.create(
                        file_name=str(uploaded_file),
                        etrap_add=request_user_etrap,
                        who_add=request.user.username,
                        when_add=datetime.now()
                    )
                    KassaExcelFiles.objects.create(operator=request.user, document=uploaded_file)
                    messages.success(request, f"Успешно добавлено в БД ({matched_count} сопоставлено, {unmatched_count} ожидают заведения договора)")
            except Exception as e:
                messages.error(request, f'ошибка с transaction при сохранении, тип ошибки == {e}')
                logger.error(f'ошибка с transaction при сохранении, тип ошибки == {e}')

    return render(request, 'telekom/Kassa/addPlatejiMilliBilling.html', context)


def exportMilliBillingUnmatched(request):
    if not request.user.is_authenticated:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')

    if not (request.user.is_superuser or request.user.username in ['intizar_gorogly', 'lenashb', 'testMTBDZ', 'AyshatGoroglyMtb', 'GuljahanAkdepeMtb', 'AzizShabatMtb', 'Saryyewa_Gozel_Shabat_MTB', 'BaharKoneurgenchKassa', 'Merjen_Yylally_MTB', 'GozelGubadagMtb', 'SelbiBoldumsazMtb', 'MahymAkdepeMtb', 'Aramedowa_Oguljemal', 'shirmamedowa_gulalek', 'Jumyazowa_Oguljemal', 'Kurbanowa_Gulnabat_Koneurgench', 'Baltabayewa_Sewara_MTB_DGE', 'Ishangulyyewa_Nurjemal_Koneurgench_kassa']):
        messages.error(request, f'Доступ разрешен только администратору')
        return redirect('user-login')

    unmatched = MilliBillingPay.objects.filter(is_matched=False).order_by('-date')
    return build_unmatched_xlsx_response(unmatched)
