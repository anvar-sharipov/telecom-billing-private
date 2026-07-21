from django.shortcuts import render, redirect
from telekom.models import *
from django.db.models import Sum
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
import tablib

from datetime import date
from calendar import monthrange
from tablib import Dataset
from icecream import ic
from telekom.views2.myFunc.myFunc import monthСonvert

from datetime import datetime
import calendar
import re

from django.db import transaction
import logging
logger = logging.getLogger(__name__)

# из строки Dashoguz_on_ 2025_февраль.xlsx Взвращает {"year": '2025', "month": 'февраль', "etrap": 'Dashoguz', "status": 'on'}
def parse_string(s):
    pattern = r"^(\d{4})([А-Яа-я]+)([A-Za-z]+)(ON|OFF)$"
    match = re.match(pattern, s)
    if match:
        year, month, etrap, status = match.groups()
        return {"year": year, "month": month, "etrap": etrap, "status": status}
    return None

MB_tarifs = ['ADSL128 DL(B)', '1024/0/05', 'TAZE Chaksiz/10/0.08"TIZLIK-2016"(01.07.2016ý)', '(1) OBADASH-3tarif/512kbit /10man/0.10(rayat) (TAZE-01.01.2017ý)']
# Проверка договоров на корректность:
#  1) Первые 3 символа должны быть буквами ([A-Z]).
#  2) Остальные только цифры (\d).
#  3) Если первые 3 символа не буквы, но дальше есть хотя бы 1 буква — строка не подходит.
# def is_valid(s):
#     return bool(re.fullmatch(r"[A-Z]{3}\d+", s))
dogowors_words_list = ['DZA', 'DAD', 'DBS', 'DGD', 'DGE', 'DGO', 'DKU', 'DNZ', 'DRB', 'DTB']
excludes_dogowor_list = ['DZA27']
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


dogowors_words = {
    'Dashoguz': ['DZA', 'DNZ'], 
    'S.A.Nyyazow': ['DNZ'], 
    'Akdepe': ['DAD', 'DGE'], 
    'Gorogly': ['DGO'], 
    'Ruhubelent': ['DRB'], 
    'Turkmenbashy': ['DTB'], 
    'Boldumsaz': ['DBS', 'DGD'], 
    'Koneurgench': ['DKU']}


def import_internet_nach_new(request):

    if not ((request.user.is_superuser and request.user.username == 'admin1') or request.user.username == 'Gayyp'):
        messages.error(request, f'У вас нет доступа')
        return redirect('user-login')
   
    context={}
    context['import_internet_nach_new'] = True
    context['allow_nach'] = False

    current_date = datetime.now().date()
    formatted_date = current_date.strftime('%Y-%m-%d')
    current_year, current_month, current_day = formatted_date.split('-')
    current_month_word = monthСonvert(current_month)
    context['current_year'] = current_year
    context['current_month_word'] = current_month_word

    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    years = ['2024','2025', '2026', '2027', '2028', '2029', '2030', '2031', '2032', '2033', '2034', '2035']

   
# Для вывода информацию последних начислений за 3 месяца
    year_month = f"{str(int(current_year))}{current_month_word}"
    months_dict = {
        'Январь': 1, 'Февраль': 2, 'Март': 3, 'Апрель': 4, 'Май': 5, 'Июнь': 6,
        'Июль': 7, 'Август': 8, 'Сентябрь': 9, 'Октябрь': 10, 'Ноябрь': 11, 'Декабрь': 12
    }

    months_reverse = {v: k for k, v in months_dict.items()}  # Обратный словарь

    # Разбираем строку
    year = int(year_month[:4])
    month_name = year_month[4:]
    month = months_dict[month_name]  # Получаем номер месяца

    # Генерируем 3 предыдущих месяца
    previous_months = []
    for i in range(1, 4):
        new_month = month - i
        new_year = year

        if new_month < 1:  # Если месяц стал 0 или отрицательным, переходим на предыдущий год
            new_month += 12
            new_year -= 1

        previous_months.append(f"{new_year}{months_reverse[new_month]}")

    # Распаковка в переменные
    last_year_month_1, last_year_month_2, last_year_month_3 = previous_months

    # Вывод результата
    # ic(last_year_month_1)  # '2025Февраль'
    # ic(last_year_month_2)  # '2025Январь'
    # ic(last_year_month_3)  # '2024Декабрь'

    dry = DontRepeatYourself.objects.filter(
        Q(internetNachisleniyaYearMonthEtrapONOFF__icontains=year_month) |
        Q(internetNachisleniyaYearMonthEtrapONOFF__icontains=last_year_month_1) |
        Q(internetNachisleniyaYearMonthEtrapONOFF__icontains=last_year_month_2) |
        Q(internetNachisleniyaYearMonthEtrapONOFF__icontains=last_year_month_3)
    )

    list_dry = []
    for d in dry:
        # dr: {'etrap': 'Akdepe', 'month': 'Март', 'status': 'ON', 'year': '2024'}
        dr = parse_string(d.internetNachisleniyaYearMonthEtrapONOFF) 
        list_dry.append(dr)

    # Убираем `None` из списка
    list_dry = [item for item in list_dry if item]

    # Сортируем по году и месяцу
    list_dry.sort(key=lambda x: (int(x['year']), months_dict[x['month']]), reverse=True)

    context['dry'] = list_dry
# Для вывода информацию последних начислений за 3 месяца





   
    
    context['months'] = months
    context['etraps'] = etraps
    context['years'] = years

    if request.method == 'POST':
        dataset = Dataset()

        # Если файл не выбран то ошибка
        try:
            xlsx_data = request.FILES['xlsx_file']
            context['file_name'] = str(xlsx_data)
        except:
            messages.error(request, f'Выберите Файл')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)

        # Если при скачивании выбрали не тот же файл что и при проверке то вывести ошибку
        if ('download_error' in request.POST or 'download_error_dublicate_logins_old' in request.POST or 'download_error_dublicate_logins' in request.POST) and str(xlsx_data) != request.POST.get('file_name'):
            messages.error(request, f"Во второй раз вы выбрали не тот файл который был первым")
            return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)

        # если формат не xlsx то Ошибка
        try:
            imported_data = dataset.load(xlsx_data.read(), format='xlsx', headers=False)
        except:
            messages.error(request, f'Файл должен быть формата xlsx')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)

        month_word = request.POST.get('month')
        year = request.POST.get('year')
        etrap = request.POST.get('etrap')
        status = request.POST.get('status')
        action = request.POST.get('action')
        

        context['month_word'] = month_word
        context['year'] = year
        context['etrap'] = etrap
        context['status'] = status
        context['action'] = action

        if etrap == 'no':
            messages.error(request, f'Выберите этрап')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)

        if month_word and year and etrap and status and action:

        # сверка выбранных месяца, года, статуса, этрапа с названием файла. DontRepeatYourself. сверка выбранного месяца и года с месяцем и годов в 1 строке excel
            text = str(xlsx_data).lower()
            if month_word.lower() not in text:
                messages.error(request, f'Вашего выбранного месяца {month_word} нет в названии файла')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)
            if year not in text:
                messages.error(request, f'Вашего выбранного года {year} нет в названии файла')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)
            if status.lower() not in text:
                messages.error(request, f'Вашего выбранного {status} нет в названии файла')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)
            if etrap.lower() not in text:
                messages.error(request, f'Вашего выбранного этрапа {etrap} нет в названии файла')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)
            
            
            if DontRepeatYourself.objects.filter(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}{status.upper()}").exists():
                messages.error(request, f"{month_word} {year} etrap {etrap} '{status}' уже был добавлен")
                return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)
   
            
            head = imported_data[0][0].lower()

            if month_word.lower() not in head:
                messages.error(request, f'месяц в первой строке excel не совпадает с месяцем в названии файла')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)

            if year not in head:
                messages.error(request, f'год в первой строке excel не совпадает с годом в названии файла')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)
        # сверка выбранных месяца, года, статуса, этрапа с названием файла. DontRepeatYourself. сверка выбранного месяца и года с месяцем и годов в 1 строке excel

            
            
            if status == 'on':
                count = 0
                count_dogowors = 0
                
            # проверка на дублирования dogowor и login в БД и в OLD
                dict_dog_pk = {}
                dublicate_dogowors_and_logins = set()
                users = UserTable.objects.exclude(Q(dogowor='') | Q(dogowor__isnull=True)).values_list('pk', 'dogowor')
                for pk, dogowor in users:
                    d = dogowor.upper().strip()
                    if d in dict_dog_pk:
                        dublicate_dogowors_and_logins.add(d)
                    else:
                        dict_dog_pk[d] = pk

                dict_login_pk = {}
                users = UserTable.objects.exclude(Q(login='') | Q(login__isnull=True)).values_list('pk', 'login')
                for pk, login in users:
                    log = login.lower().strip()
                    if log in dict_login_pk:
                        dublicate_dogowors_and_logins.add(log)
                    else:
                        dict_login_pk[log] = pk

                number_pk = {}
                users = UserTable.objects.filter(etrap=etrap)
                for u in users:
                    n = int(u.number)
                    number_pk[n] = u.pk

                dict_dog_pk_old = {}
                dublicate_dogowors_and_logins_old = set()
                users =  OldLoginDogowor.objects.exclude(Q(dogowor='') | Q(dogowor__isnull=True)).values_list('number', 'dogowor')
                for num, dogowor in users:
                    d = dogowor.upper().strip()
                    if d in dict_dog_pk_old:
                        dublicate_dogowors_and_logins_old.add(d)
                    else:
                        dict_dog_pk_old[d] = number_pk[int(num)]

                dict_login_pk_old = {}
                users =  OldLoginDogowor.objects.exclude(Q(login='') | Q(login__isnull=True)).values_list('number', 'login')
                for num, login in users:
                    d = login.lower().strip()
                    if d in dict_login_pk_old:
                        dublicate_dogowors_and_logins_old.add(d)
                    else:
                        dict_login_pk_old[d] = number_pk[int(num)]
                
                # Проверка на дубликат логина и договора в Old
                if dublicate_dogowors_and_logins_old:
                    if 'download_error_dublicate_logins_old' in request.POST:
                        headers = ("№", "Договор/login")
                        data = []
                        data = tablib.Dataset(*data, headers=headers)
                        for count, d in enumerate(dublicate_dogowors_and_logins_old, start=1):
                            data.append((count, d))
                        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
                        response['Content-Disposition'] = f"attachment; filename= DUBLICATE_DOGOWOR_AND_LOGIN_OLD.xlsx"
                        return response
                    else:
                        context['dublicate_dogowors_and_logins_old'] = dublicate_dogowors_and_logins_old
                        messages.error(request, f"В Old есть повторяющиеся договора и логины")
                        return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)

                # Проверка на дубликат логина и договора в БД
                if dublicate_dogowors_and_logins:
                    if 'download_error_dublicate_logins' in request.POST:
                        headers = ("№", "Договор/login")
                        data = []
                        data = tablib.Dataset(*data, headers=headers)
                        for count, d in enumerate(dublicate_dogowors_and_logins, start=1):
                            data.append((count, d))
                        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
                        response['Content-Disposition'] = f"attachment; filename= DUBLICATE_DOGOWOR_AND_LOGIN.xlsx"
                        return response
                    else:
                        context['dublicate_dogowors_and_logins'] = dublicate_dogowors_and_logins
                        # messages.error(request, f"В БД есть повторяющиеся договора и логины: {', '.join(sorted(dublicate_dogowors_and_logins))}")
                        messages.error(request, f"В БД есть повторяющиеся договора и логины")
                        return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)
            # проверка на дублирования dogowor и login в БД и в OLD
       
                dogowor_user_value = {}
                error_inenterprises = {}
                users = UserTable.objects.exclude(Q(dogowor='') | Q(dogowor__isnull=True)).values_list('dogowor', 'number', 'hb__name', 'account', 'is_enterprises', 'etrap')
                for u_dogowor, u_number, u_hb, u_account, u_is_enterprises, u_etrap in users:
                    
                    u_dogowor = u_dogowor.upper().strip()
                    if u_is_enterprises and (not u_account or not u_hb):
                        error_inenterprises[u_dogowor] = {'number': u_number, 'etrap': u_etrap, 'error_in': 'Data Base'}
                        continue
                    if u_account and (not u_is_enterprises or not u_hb):
                        error_inenterprises[u_dogowor] = {'number': u_number, 'etrap': u_etrap, 'error_in': 'Data Base'}
                        continue
                    if u_hb and (not u_is_enterprises or not u_account):
                        error_inenterprises[u_dogowor] = {'number': u_number, 'etrap': u_etrap, 'error_in': 'Data Base'}
                        continue
                    dogowor_user_value[u_dogowor] = {
                        'number': u_number,
                        'hb': u_hb,
                        'account': u_account,
                        'is_enterprises': u_is_enterprises,
                        'etrap': u_etrap
                    }
                
                
                dogowor_user_value_old = {}
                users = OldLoginDogowor.objects.exclude(Q(dogowor='') | Q(dogowor__isnull=True)).values_list('dogowor', 'number', 'hb', 'account', 'is_enterprises', 'etrap')
                for u2_dogowor, u2_number, u2_hb, u2_account, u2_is_enterprises, u2_etrap in users:
                    u2_dogowor = u2_dogowor.upper().strip()
                    if u2_is_enterprises and (not u2_account or not u2_hb):
                        error_inenterprises[u2_dogowor] = {'number': u2_number, 'etrap': u2_etrap, 'error_in': 'Old'}
                        continue
                    if u2_account and (not u2_is_enterprises or not u2_hb):
                        error_inenterprises[u2_dogowor] = {'number': u2_number, 'etrap': u2_etrap, 'error_in': 'Old'}
                        continue
                    if u2_hb and (not u2_is_enterprises or not u2_account):
                        error_inenterprises[u2_dogowor] = {'number': u2_number, 'etrap': u2_etrap, 'error_in': 'Old'}
                        continue
                    dogowor_user_value_old[u2_dogowor] = {
                        'number': u2_number,
                        'hb': u2_hb,
                        'account': 0,
                        'is_enterprises': u2_is_enterprises,
                        'etrap': u2_etrap
                    }

                # Проверка на присуствие и галочки эдара и счет_номера и hb
                if error_inenterprises:
                    if 'error_inenterprises' in request.POST:
                        headers = ("Этрап", "Номер", "Договор", "Ошибка в")
                        data = []
                        data = tablib.Dataset(*data, headers=headers)
                        for dog, val in error_inenterprises.items():
                            data.append((val['etrap'], val['number'], dog, val['error_in']))
                        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
                        response['Content-Disposition'] = f"attachment; filename= ERRORS_IN_EDARA_DB.xlsx"
                        return response

                    else:
                        context['error_inenterprises'] = error_inenterprises
                        messages.error(request, f"Есть ошибки в эдара (либо едара без счет номера или без 'H' и 'B' и т.п)")
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)



                error_dict = {}
                bulk_create = []
                edara_hoz_arenda = {'count':0, 'price':0}
                edara_bud_arenda = {'count':0, 'price':0}
                ilat_arenda = {'count':0, 'price':0}

                edara_hoz_MB = {'count':0, 'price':0}
                edara_bud_MB = {'count':0, 'price':0}
                ilat_MB = {'count':0, 'price':0}

                # 0=name  1=dogowor  2=login  3=tarif  4=аренда  5=Превышение  6=Превышение(мб)  7=Итого  8=манат
                for d in imported_data:
                    if d[8]:
                        if 'manat' in d[8]:
                            count += 1
                        # Проверку на корректность колонок
                            try:
                                price_arenda = float(d[4])
                            except:
                                error_dict[count] = {'Пользователь': d[0], 'Договор': d[1], 'Логин': d[2], 'Тариф': d[3], 'Аренда': d[4], 'Превышение': d[5], 'Превышение (Мб)': d[6], 'Итого': d[7], 'Тип ошибки': "Неправильная колонка аренда"}
                                continue   
                            try:
                                price_MB = float(d[5])
                            except:
                                error_dict[count] = {'Пользователь': d[0], 'Договор': d[1], 'Логин': d[2], 'Тариф': d[3], 'Аренда': d[4], 'Превышение': d[5], 'Превышение (Мб)': d[6], 'Итого': d[7], 'Тип ошибки': "Неправильная колонка Превышение"}
                                continue
                            try:
                                tarif = d[3].strip()
                            except:
                                error_dict[count] = {'Пользователь': d[0], 'Договор': d[1], 'Логин': d[2], 'Тариф': d[3], 'Аренда': d[4], 'Превышение': d[5], 'Превышение (Мб)': d[6], 'Итого': d[7], 'Тип ошибки': "Неправильная колонка Тариф"}
                                continue
                            try:
                                itogo = float(d[7])
                            except:
                                error_dict[count] = {'Пользователь': d[0], 'Договор': d[1], 'Логин': d[2], 'Тариф': d[3], 'Аренда': d[4], 'Превышение': d[5], 'Превышение (Мб)': d[6], 'Итого': d[7], 'Тип ошибки': "Неправильная колонка Итого"}
                                continue
                            try:
                                dogowor = d[1].upper().replace(" ", "").replace("OLD", "").replace("-", "").strip()
                            except:
                                error_dict[count] = {'Пользователь': d[0], 'Договор': d[1], 'Логин': d[2], 'Тариф': d[3], 'Аренда': d[4], 'Превышение': d[5], 'Превышение (Мб)': d[6], 'Итого': d[7], 'Тип ошибки': "Неправильный Договор"}
                                continue
                            if 'IKDZ' in dogowor or dogowor in excludes_dogowor_list:
                                continue
                            try:
                                login = d[2].lower().replace(" ", "").replace("old", "").replace("-", "").strip()
                            except:
                                error_dict[count] = {'Пользователь': d[0], 'Договор': d[1], 'Логин': d[2], 'Тариф': d[3], 'Аренда': d[4], 'Превышение': d[5], 'Превышение (Мб)': d[6], 'Итого': d[7], 'Тип ошибки': "Неправильный Логин"}
                                continue
                            
                            dog_word = dogowor[:3]
                            # print(etrap, dogowors_words, dog_word)
                            if dog_word in dogowors_words[etrap]:
                                count_dogowors += 1         
                                 
                            if not is_valid(dogowor):
                                error_dict[count] = {'Пользователь': d[0], 'Договор': d[1], 'Логин': d[2], 'Тариф': d[3], 'Аренда': d[4], 'Превышение': d[5], 'Превышение (Мб)': d[6], 'Итого': d[7], 'Тип ошибки': "Неправильный Договор"}
                                continue
                         
                            if dogowor not in dict_dog_pk and dogowor not in dict_dog_pk_old and login not in dict_login_pk and login not in dict_login_pk_old:
                                error_dict[count] = {'Пользователь': d[0], 'Договор': d[1], 'Логин': d[2], 'Тариф': d[3], 'Аренда': d[4], 'Превышение': d[5], 'Превышение (Мб)': d[6], 'Итого': d[7], 'Тип ошибки': "Договор и логин не найден в БД и в OLD"}
                                continue
                        # Проверку на корректность колонок
                            
                            # 0=name  1=dogowor  2=login  3=tarif  4=аренда  5=Превышение  6=Превышение(мб)  7=Итого  8=манат
                            # bulk_create
                            # не забыть поставить в условие action == 'save'
                            if not error_dict:
                                name = d[0]
                                try:
                                    etrap_save =  dogowor_user_value[dogowor]['etrap']
                                except:
                                    try:
                                        etrap_save =  dogowor_user_value_old[dogowor]['etrap']
                                    except:
                                        pass
                                
                                try:
                                    number_save =  dogowor_user_value[dogowor]['number']
                                except:
                                    try:
                                        number_save =  dogowor_user_value_old[dogowor]['number']
                                    except:
                                        pass

                                try:
                                    hb_save =  dogowor_user_value[dogowor]['hb']
                                except:
                                    try:
                                        hb_save =  dogowor_user_value_old[dogowor]['hb']
                                    except:
                                        pass

                                try:
                                    account_save =  dogowor_user_value[dogowor]['account']
                                except:
                                    try:
                                        account_save =  dogowor_user_value_old[dogowor]['account']
                                    except:
                                        pass

                                try:
                                    is_enterprises_save =  dogowor_user_value[dogowor]['is_enterprises']
                                except:
                                    try:
                                        is_enterprises_save =  dogowor_user_value_old[dogowor]['is_enterprises']
                                    except:
                                        pass

                                

                                if is_enterprises_save:
                                    if dogowor == 'DZA16111':
                                        ic(hb_save)
                                        ic(dogowor_user_value['DZA16111'])
                                    if hb_save == 'H':
                                        if dogowor == 'DZA16111':
                                            ic(dogowor_user_value['DZA16111']['is_enterprises'])
                                            ic(is_enterprises_save)
                                        edara_hoz_arenda['count'] += 1
                                        edara_hoz_arenda['price'] += price_arenda
                                    elif hb_save == 'B':
                                        edara_bud_arenda['count'] += 1
                                        edara_bud_arenda['price'] += price_arenda
                                    else:
                                        # сюда не дойдет так как проверка на присуствие и галочки эдара и счет номера и hb проверяется ранее
                                        pass
                                else:
                                    ilat_arenda['count'] += 1
                                    ilat_arenda['price'] += price_arenda
                                
                                if tarif in MB_tarifs:
                                    if is_enterprises_save:
                                        if hb_save == 'H':
                                            edara_hoz_MB['count'] += 1
                                            edara_hoz_MB['price'] += price_MB
                                        elif hb_save == 'B':
                                            edara_bud_MB['count'] += 1
                                            edara_bud_MB['price'] += price_MB
                                        else:
                                            # сюда не дойдет так как проверка на присуствие и галочки эдара и счет номера и hb проверяется ранее
                                            pass
                                    else:
                                        ilat_MB['count'] += 1
                                        ilat_MB['price'] += price_MB

                                        

                                # obj = ImportInternetNachisleniyaON(
                                #         year=year, 
                                #         month=month_word, 
                                #         FAO=name, 
                                #         dogowor=dogowor, 
                                #         login=login, 
                                #         price=price_arenda, 
                                #         etrap=etrap_save,
                                #         number=number_save,
                                #         hb=hb_save,
                                #         account=account_save,
                                #         is_enterprises=is_enterprises_save,
                                #         tarif=tarif,
                                #         price_MB=price_MB,
                                #         itogo=itogo
                                #     )
                                # bulk_create.append(obj)
                if count_dogowors < 1:
                    messages.error(request, f'Договоры в excel не принадлежат тому этрапу который вы написали в названии файла')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)
                
                # скачивание ошибок error_dict в excel
                if error_dict:
                    if 'download_error' in request.POST:
                        headers = ("№", "Пользователь", "Договор", "Логин", "Тариф", "Аренда", "Превышение", "Превышение (Мб)", "Итого", "Тип ошибки")
                        data = []
                        data = tablib.Dataset(*data, headers=headers)
                        for key, v in error_dict.items():
                            data.append((key, v['Пользователь'], v['Договор'], v['Логин'], v['Тариф'], v['Аренда'], v['Превышение'], v['Превышение (Мб)'], v['Итого'], v['Тип ошибки']))
                        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
                        response['Content-Disposition'] = f"attachment; filename= ERRORS_{str(xlsx_data)}.xlsx"
                        return response
                    else: 
                        messages.error(request, f"Есть ошибки в excel")
                        context['error_dict'] = error_dict
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)
                
                if action == 'check':
                    context['edara_hoz_arenda'] = edara_hoz_arenda
                    context['edara_bud_arenda'] = edara_bud_arenda
                    context['ilat_arenda'] = ilat_arenda
                    context['edara_hoz_MB'] = edara_hoz_MB
                    context['edara_bud_MB'] = edara_bud_MB
                    context['ilat_MB'] = ilat_MB
                    context['allow_nach'] = True
                    messages.success(request, f"Успешное проверка '{status}'")
                else:
                    if request.POST.get('file_name') == str(xlsx_data):
                        context['allow_nach'] = False
                        messages.success(request, f"Успешный импорт '{status}'")
                    else:
                        messages.error(request, f"Во второй раз вы выбрали не тот файл который был первым")
                        return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)

            else:
                if not DontRepeatYourself.objects.filter(internetNachisleniyaYearMonthEtrapONOFF=f"{year}{month_word}{etrap}ON").exists():
                    messages.error(request, f'Невозможно начислить OFF пока не начислен ON')
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)

                messages.success(request, f"Успешное проверка '{status}'")


            # if action == 'save':
            #     pass
            # else:
            #     if status == 'on':
            #     messages.success(request, f"Успешное сохранение '{status}' в бд")
            # else:
            #     messages.success(request, f"Успешное сохранение '{status}' в бд")



            

            


        else:
            messages.error(request, f"Заполните все поля")




                    

 


    

    return render(request, 'telekom/MATB/NachislitWruchnuyu/internet_nachisleniya_new/import_internet_nach_new.html', context)