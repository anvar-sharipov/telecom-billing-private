from django.shortcuts import redirect
from django.contrib import messages

from telekom.models import NachMinus, NonLocalCall, PayHistory, UserTable, Zakaz
from telekom.views2.myFunc.myFunc import monthСonvert
from calendar import monthrange

# для .txt
from django.http import HttpResponse

import sys
def bell():
    sys.stdout.write('\r\a')
    sys.stdout.flush()




def N_txt (request, year, month, etrap):
    print('tut')

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']

    response = HttpResponse(content_type="text/plain")
    txtName = f'{etrap} N TXT {monthСonvert(month)}-{year} {etrap}'
    response['Content-Disposition'] = f'attachment; filename={txtName}.txt'

    month_numb = monthСonvert(month)

    if month_numb == False:
        messages.error(request, f"Выберите месяц")
        return redirect('reestr-main')

    if month_numb != '12':
        month_numbPlus1 = str(int(month_numb) + 1)
        if len(month_numbPlus1) == 1:
            month_numbPlus1 = f"0{month_numbPlus1}"
        new_year = year


        
        year_is_new = False
    else:
        print('da')
        month_numbPlus1 = '1'
        if len(month_numbPlus1) == 1:
            month_numbPlus1 = f"0{month_numbPlus1}"
        new_year = year
        print('new_year1', new_year)
        # new_year = str(int(year) + 1)
        print('new_year2', new_year)


        year_is_new = True
    
    print('month_numbPlus1', month_numbPlus1)

    if len(month_numb) == 1:
        month_numb = f"0{month_numb}"

    days_in_nach_month = monthrange(int(year), int(month_numb))[1]
    start = f"{new_year}-{month_numb}-01"
    end = f"{new_year}-{month_numb}-{days_in_nach_month}"


    lines = []
    count = 0

    print('start, end',start, end)
    # ✅ По просьбе пользователя: сумма N_txt.py должна быть равна бакету
    # "Население" в trafik.py. Там звонок относится к "Население" по его
    # СОБСТВЕННОМУ edara (см. trafik.py::classify_call — ATS проверяется
    # первым и не попадает ни в один из Bud/Hoz/Naseleniya, edara in ('B','H')
    # это Bud/Hoz, edara=='E' это Unknown, всё остальное — Население). Раньше
    # тут вообще не смотрели на edara, только на текущий is_enterprises
    # абонента — суммы расходились, если is_enterprises поменяли позже.
    ATSSALDO = -698 if etrap == 'Dashoguz' else -700
    numbersATS = set(int(u.number) for u in UserTable.objects.filter(account=ATSSALDO, etrap=etrap))

    callsAll = NonLocalCall.objects.filter(SUB_A_etrap=etrap, DATE__range=[start,end]).order_by('DATE')
    my_dict = {} # {number: [[DATE, START, SUB_B, SUB_B_loc, MT, total_price], [DATE, START, SUB_B, SUB_B_loc, MT, total_price]]}
    for i in callsAll:
        if int(i.SUB_A) in numbersATS:
            continue
        if i.edara in ('B', 'H', 'E'):
            continue
        if int(i.SUB_A) not in my_dict:
            my_dict[int(i.SUB_A)] = [[i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price]]
        else:
            my_dict[int(i.SUB_A)].append([i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price])
    testCount = 0

    # ✅ Список абонентов реестра строим по номерам из my_dict (у кого реально
    # есть звонки "Население"), а не по текущему is_enterprises — иначе
    # абонент, у которого is_enterprises разошёлся с edara на его звонках,
    # вообще не появлялся бы в N_txt, и сумма не сходилась бы с trafik.py.
    # old_style_users держим только чтобы не потерять абонентов, у которых в
    # месяце были ТОЛЬКО Zakaz-переговоры без обычных звонков (см. блок ZAKAZ
    # ниже — на сумму AMTC/trafik.py это не влияет).
    if etrap in etraps:
        old_style_users = UserTable.objects.filter(is_enterprises = False, etrap=etrap)
    elif etrap == 'all':
        old_style_users = UserTable.objects.filter(is_enterprises = False)
    else:
        old_style_users = UserTable.objects.none()

    combined_numbers = set(my_dict.keys()) | set(int(u.number) for u in old_style_users)
    if etrap in etraps:
        users = UserTable.objects.filter(number__in=[str(n) for n in combined_numbers], etrap=etrap).order_by('number')
    elif etrap == 'all':
        users = UserTable.objects.filter(number__in=[str(n) for n in combined_numbers]).order_by('number')
    else:
        users = []

    # --- Старый код (по текущему is_enterprises, без edara/ATS) — оставлен закомментированным ---
    # if etrap in etraps:
    #     users = UserTable.objects.filter(is_enterprises = False, etrap=etrap).order_by('number')
    # elif etrap == 'all':
    #     users = UserTable.objects.filter(is_enterprises = False).order_by('number')
    # else:
    #     users = []
    #
    # callsAll = NonLocalCall.objects.filter(SUB_A_etrap=etrap, DATE__range=[start,end]).order_by('DATE')
    # my_dict = {}
    # for i in callsAll:
    #     if int(i.SUB_A) not in my_dict:
    #         my_dict[int(i.SUB_A)] = [[i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price]]
    #     else:
    #         my_dict[int(i.SUB_A)].append([i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price])
    # testCount = 0

    umumyManat = 0

    total_z = 0
    zakaz = Zakaz.objects.filter(DATE__range=[start,f"{end} 23:59:59"])
    dict_z = {} # [[count, DATE, NUMBER_B, NUMBER_LOCATIONS, MT, total_price], [count, DATE, NUMBER_B, NUMBER_LOCATIONS, MT, total_price]]
    total_zakaz_count = 0
    total_zakaz_minut = 0
    total_zakaz_price = 0
    for z in zakaz:
        if float(z.total_price) > 0:
            num = int(z.NUMBER_A)
            if num not in dict_z:
                dict_z[num] = [[1, z.DATE, z.NUMBER_B, z.NUMBER_LOCATIONS, z.MT, z.total_price]]
            else:
                count_z = dict_z[num][-1][0] + int(1)
                dict_z[num].append([count_z, z.DATE, z.NUMBER_B, z.NUMBER_LOCATIONS, z.MT, z.total_price])

    for user in users:
        testCount += 1

        # calls = callsAll.filter(SUB_A=user.number)
        try:
            calls = my_dict[int(user.number)]
        except:
            if etrap == 'Dashoguz' and int(user.number) in dict_z:
                lines.append(f" Абонент_{user.number} {user.surname}   {user.name}   Адрес {user.street} Дом {user.home} Кв. {user.flat}")
                lines.append(f"\n                        Переговоры  (ZAKAZ) \n")
                c_z = 0
                t_p = 0
                for z in dict_z[int(user.number)]:
                    print('dada3')
                    c_z = z[0]
                    t_p += float(z[5])
                    lines.append(f" {z[1]} {z[2]}   {z[3]}             {z[4]}   {z[5]} \n")
                lines.append(f" ------------------------------------------------------------------------\n")
                lines.append(f" Всего переговоров (ZAKAZ): {c_z}                  Всего :     {'%.2f' % t_p}м.\n\n")
                total_z += t_p
            continue

        


        if year_is_new:
            lines.append(f" Период расчета с 01/{month_numb}/{year} - 01/{month_numbPlus1}/{new_year}           Тел. для справок 5-65-75\n")
        else:
            lines.append(f" Период расчета с 01/{month_numb} - 01/{month_numbPlus1}/{new_year}           Тел. для справок 5-65-75\n")

        lines.append(f" ------------------------------------------------------------------------\n")
        lines.append(f" Абонент_{user.number} {user.surname}   {user.name}   Адрес {user.street} Дом {user.home} Кв. {user.flat} \n")
        lines.append(f" ------------------------------------------------------------------------\n")
        lines.append(f" ДАТА  ВРЕМЯ  ТЕЛЕФОН            НАПРАВЛЕНИЕ             МИН. СУММА  Примеч.\n")
        lines.append(f" ---------------------- Переговоры по коду (АМТС) -----------------------\n")

        callCount = 0
        price = 0

        count += 1

        if len(str(count)) == 1:
            zeros = '000000'
        elif len(str(count)) == 2:
            zeros = '00000'
        elif len(str(count)) == 3:
            zeros = '0000'
        elif len(str(count)) == 4:
            zeros = '0000'
        elif len(str(count)) == 5:
            zeros = '000'
        elif len(str(count)) == 6:
            zeros = '00'
        elif len(str(count)) == 7:
            zeros = '0'
        elif len(str(count)) == 8:
            zeros = ''
        # [[i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price]]
        for values in calls:
            callCount += 1
            price += float(values[5])
            s1 = (20 - len(values[3])) * ' '
            lines.append(f"  {str(values[0])[8:10]}   {str(values[1])}   {values[2]}      {values[3]}{s1}{values[4]}   {values[5]}\n")
        lines.append(f" ------------------------------------------------------------------------\n")
        umumyManat += price
        lines.append(f" Всего переговоров (AMTC): {callCount}                 Всего :     {'%.2f' % price}м.\n")

        if etrap == 'Dashoguz' and int(user.number) in dict_z:
            lines.append(f" Абонент_{user.number} {user.surname}   {user.name}   Адрес {user.street} Дом {user.home} Кв. {user.flat}")
            lines.append(f"\n                        Переговоры  (ZAKAZ) \n")
            c_z = 0
            t_p = 0
            for z in dict_z[int(user.number)]:
                c_z = z[0]
                t_p += float(z[5])
                lines.append(f" {z[1]} {z[2]}   {z[3]}             {z[4]}   {z[5]} \n")
            lines.append(f" ------------------------------------------------------------------------\n")
            lines.append(f" Всего переговоров (ZAKAZ): {c_z}                  Всего :     {'%.2f' % t_p}м.\n\n")
            lines.append(f" Всего переговоров (AMTC + ZAKAZ): {callCount + c_z}         Всего :     {'%.2f' % (t_p+price)}м.\n\n")
            total_z += t_p



        lines.append(f" {zeros}{count}-------------------------------------------------------------------\n\n")

    bell()
    lines.append(f"Umumy manat (AMTC)    {umumyManat:.2f}\n\n")
    if total_z:
        lines.append(f"Umumy manat (ZAKAZ)  {total_z:.2f}")
    response.writelines(lines)
    return response

        



# from django.shortcuts import redirect
# from django.contrib import messages

# from telekom.models import NachMinus, NonLocalCall, PayHistory, UserTable, Zakaz
# from telekom.views2.myFunc.myFunc import monthСonvert
# from calendar import monthrange

# # для .txt
# from django.http import HttpResponse

# import sys
# def bell():
#     sys.stdout.write('\r\a')
#     sys.stdout.flush()




# def N_txt (request, year, month, etrap):
#     print('tut')

#     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']

#     response = HttpResponse(content_type="text/plain")
#     txtName = f'{etrap} N TXT {monthСonvert(month)}-{year} {etrap}'
#     response['Content-Disposition'] = f'attachment; filename={txtName}.txt'

#     month_numb = monthСonvert(month)

#     if month_numb == False:
#         messages.error(request, f"Выберите месяц")
#         return redirect('reestr-main')

#     if month_numb != '12':
#         month_numbPlus1 = str(int(month_numb) + 1)
#         if len(month_numbPlus1) == 1:
#             month_numbPlus1 = f"0{month_numbPlus1}"
#         new_year = year


        
#         year_is_new = False
#     else:
#         print('da')
#         month_numbPlus1 = '1'
#         if len(month_numbPlus1) == 1:
#             month_numbPlus1 = f"0{month_numbPlus1}"
#         new_year = year
#         print('new_year1', new_year)
#         # new_year = str(int(year) + 1)
#         print('new_year2', new_year)


#         year_is_new = True
    
#     print('month_numbPlus1', month_numbPlus1)

#     if len(month_numb) == 1:
#         month_numb = f"0{month_numb}"

#     days_in_nach_month = monthrange(int(year), int(month_numb))[1]
#     start = f"{new_year}-{month_numb}-01"
#     end = f"{new_year}-{month_numb}-{days_in_nach_month}"


#     if etrap in etraps:
#         users = UserTable.objects.filter(is_enterprises = False, etrap=etrap).order_by('number')
#     elif etrap == 'all':
#         users = UserTable.objects.filter(is_enterprises = False).order_by('number')
#     else:
#         users = []

#     lines = []

#     count = 0

#     print('start, end',start, end)
#     callsAll = NonLocalCall.objects.filter(SUB_A_etrap=etrap, DATE__range=[start,end]).order_by('DATE') 
#     my_dict = {} # {number: [[DATE, START, SUB_B, SUB_B_loc, MT, total_price], [DATE, START, SUB_B, SUB_B_loc, MT, total_price]]}
#     for i in callsAll:
#         if int(i.SUB_A) not in my_dict:
#             my_dict[int(i.SUB_A)] = [[i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price]]
#         else:
#             my_dict[int(i.SUB_A)].append([i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price])
#     testCount = 0

#     umumyManat = 0

#     total_z = 0
#     zakaz = Zakaz.objects.filter(DATE__range=[start,f"{end} 23:59:59"])
#     dict_z = {} # [[count, DATE, NUMBER_B, NUMBER_LOCATIONS, MT, total_price], [count, DATE, NUMBER_B, NUMBER_LOCATIONS, MT, total_price]]
#     total_zakaz_count = 0
#     total_zakaz_minut = 0
#     total_zakaz_price = 0
#     for z in zakaz:
#         if float(z.total_price) > 0:
#             num = int(z.NUMBER_A)
#             if num not in dict_z:
#                 dict_z[num] = [[1, z.DATE, z.NUMBER_B, z.NUMBER_LOCATIONS, z.MT, z.total_price]]
#             else:
#                 count_z = dict_z[num][-1][0] + int(1)
#                 dict_z[num].append([count_z, z.DATE, z.NUMBER_B, z.NUMBER_LOCATIONS, z.MT, z.total_price])

#     for user in users:
#         testCount += 1

#         # calls = callsAll.filter(SUB_A=user.number)
#         try:
#             calls = my_dict[int(user.number)]
#         except:
#             if etrap == 'Dashoguz' and int(user.number) in dict_z:
#                 lines.append(f" Абонент_{user.number} {user.surname}   {user.name}   Адрес {user.street} Дом {user.home} Кв. {user.flat}")
#                 lines.append(f"\n                        Переговоры  (ZAKAZ) \n")
#                 c_z = 0
#                 t_p = 0
#                 for z in dict_z[int(user.number)]:
#                     print('dada3')
#                     c_z = z[0]
#                     t_p += float(z[5])
#                     lines.append(f" {z[1]} {z[2]}   {z[3]}             {z[4]}   {z[5]} \n")
#                 lines.append(f" ------------------------------------------------------------------------\n")
#                 lines.append(f" Всего переговоров (ZAKAZ): {c_z}                  Всего :     {'%.2f' % t_p}м.\n\n")
#                 total_z += t_p
#             continue

        


#         if year_is_new:
#             lines.append(f" Период расчета с 01/{month_numb}/{year} - 01/{month_numbPlus1}/{new_year}           Тел. для справок 5-65-75\n")
#         else:
#             lines.append(f" Период расчета с 01/{month_numb} - 01/{month_numbPlus1}/{new_year}           Тел. для справок 5-65-75\n")

#         lines.append(f" ------------------------------------------------------------------------\n")
#         lines.append(f" Абонент_{user.number} {user.surname}   {user.name}   Адрес {user.street} Дом {user.home} Кв. {user.flat} \n")
#         lines.append(f" ------------------------------------------------------------------------\n")
#         lines.append(f" ДАТА  ВРЕМЯ  ТЕЛЕФОН            НАПРАВЛЕНИЕ             МИН. СУММА  Примеч.\n")
#         lines.append(f" ---------------------- Переговоры по коду (АМТС) -----------------------\n")

#         callCount = 0
#         price = 0

#         count += 1

#         if len(str(count)) == 1:
#             zeros = '000000'
#         elif len(str(count)) == 2:
#             zeros = '00000'
#         elif len(str(count)) == 3:
#             zeros = '0000'
#         elif len(str(count)) == 4:
#             zeros = '0000'
#         elif len(str(count)) == 5:
#             zeros = '000'
#         elif len(str(count)) == 6:
#             zeros = '00'
#         elif len(str(count)) == 7:
#             zeros = '0'
#         elif len(str(count)) == 8:
#             zeros = ''
#         # [[i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price]]
#         for values in calls:
#             callCount += 1
#             price += float(values[5])
#             s1 = (20 - len(values[3])) * ' '
#             lines.append(f"  {str(values[0])[8:10]}   {str(values[1])}   {values[2]}      {values[3]}{s1}{values[4]}   {values[5]}\n")
#         lines.append(f" ------------------------------------------------------------------------\n")
#         umumyManat += price
#         lines.append(f" Всего переговоров (AMTC): {callCount}                 Всего :     {'%.2f' % price}м.\n")

#         if etrap == 'Dashoguz' and int(user.number) in dict_z:
#             lines.append(f" Абонент_{user.number} {user.surname}   {user.name}   Адрес {user.street} Дом {user.home} Кв. {user.flat}")
#             lines.append(f"\n                        Переговоры  (ZAKAZ) \n")
#             c_z = 0
#             t_p = 0
#             for z in dict_z[int(user.number)]:
#                 c_z = z[0]
#                 t_p += float(z[5])
#                 lines.append(f" {z[1]} {z[2]}   {z[3]}             {z[4]}   {z[5]} \n")
#             lines.append(f" ------------------------------------------------------------------------\n")
#             lines.append(f" Всего переговоров (ZAKAZ): {c_z}                  Всего :     {'%.2f' % t_p}м.\n\n")
#             lines.append(f" Всего переговоров (AMTC + ZAKAZ): {callCount + c_z}         Всего :     {'%.2f' % (t_p+price)}м.\n\n")
#             total_z += t_p



#         lines.append(f" {zeros}{count}-------------------------------------------------------------------\n\n")

#     bell()
#     lines.append(f"Umumy manat (AMTC)    {umumyManat:.2f}\n\n")
#     if total_z:
#         lines.append(f"Umumy manat (ZAKAZ)  {total_z:.2f}")
#     response.writelines(lines)
#     return response

        
