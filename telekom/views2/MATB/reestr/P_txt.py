from django.shortcuts import redirect
from django.contrib import messages

from telekom.models import NachMinus, NonLocalCall, PayHistory, UserTable, Zakaz
from telekom.views2.myFunc.myFunc import monthСonvert
from calendar import monthrange
from datetime import datetime, timedelta

# для .txt
from django.http import HttpResponse
import sys
def bell():
    sys.stdout.write('\r\a')
    sys.stdout.flush()






def P_txt (request, year, month, etrap):

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']

    response = HttpResponse(content_type="text/plain")
    txtName = f'{etrap} P TXT {monthСonvert(month)}-{year} {etrap}'
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
        month_numbPlus1 = '1'
        if len(month_numbPlus1) == 1:
            month_numbPlus1 = f"0{month_numbPlus1}"
        new_year = year
        print('new_year1', new_year)
        new_year = str(int(year) + 1)
        print('new_year2', new_year)



        year_is_new = True

    if len(month_numb) == 1:
        month_numb = f"0{month_numb}"

    days_in_nach_month = monthrange(int(year), int(month_numb))[1]
    start = f"{year}-{month_numb}-01"
    convert_date = datetime.strptime(start, "%Y-%m-%d")
    end2 = convert_date + timedelta(days=int(days_in_nach_month))
    next_year = end2.year
    next_month = end2.month
    end3 = f"{next_year}-{next_month}-01"
    end = f"{year}-{month_numb}-{days_in_nach_month}"

    print('GGGGGGGGGGGGGGGG', end2)
    lines = []
    print('start, end',start, end)

    # ✅ По просьбе пользователя: сумма P_txt.py должна быть равна сумме
    # бакетов Bud+Hoz+ATS в trafik.py (ATS входит в Hoz, как и в R_txt.py —
    # разделение Hoz/ATS есть только в trafik.py). Звонок относится к
    # "Предприятие" по его СОБСТВЕННОМУ edara (edara in ('B','H')) ИЛИ если
    # номер — АТС (numbersATS), независимо от edara на его звонках. Раньше
    # тут вообще не смотрели на edara/ATS, только на текущий is_enterprises
    # абонента — суммы расходились, если is_enterprises меняли позже (та же
    # причина, что чинили в N_txt.py/R_txt.py).
    ATSSALDO = -698 if etrap == 'Dashoguz' else -700
    numbersATS = set(int(u.number) for u in UserTable.objects.filter(account=ATSSALDO, etrap=etrap))

    callsObj = NonLocalCall.objects.filter(SUB_A_etrap=etrap, DATE__range=[start,end]).order_by('DATE')
    my_dict = {} # {number: [[DATE, START, SUB_B, SUB_B_loc, MT, total_price], [DATE, START, SUB_B, SUB_B_loc, MT, total_price]]}
    for i in callsObj:
        if int(i.SUB_A) not in numbersATS and i.edara not in ('B', 'H'):
            continue
        if int(i.SUB_A) not in my_dict:
            my_dict[int(i.SUB_A)] = [[i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price]]
        else:
            my_dict[int(i.SUB_A)].append([i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price])

    # ✅ Список абонентов реестра строим по номерам из my_dict (у кого реально
    # есть звонки "Предприятие"/ATS), а не по текущему is_enterprises — та же
    # причина, что в N_txt.py (см. подробный комментарий там). old_style_users
    # держим только чтобы не потерять абонентов с ТОЛЬКО Zakaz-переговорами.
    if etrap in etraps:
        old_style_users = UserTable.objects.filter(is_enterprises = True, etrap=etrap)
        combined_numbers = set(my_dict.keys()) | set(int(u.number) for u in old_style_users)
        users = UserTable.objects.filter(number__in=[str(n) for n in combined_numbers], etrap=etrap).order_by('account')
    elif etrap == 'all':
        pass
        # users = UserTable.objects.filter(is_enterprises = True).order_by('account')
    else:
        users = []

    # --- Старый код (по текущему is_enterprises, без edara/ATS) — оставлен закомментированным ---
    # if etrap in etraps:
    #     users = UserTable.objects.filter(is_enterprises = True, etrap=etrap).order_by('account')
    # elif etrap == 'all':
    #     pass
    #     # users = UserTable.objects.filter(is_enterprises = True).order_by('account')
    # else:
    #     users = []
    #
    # callsObj = NonLocalCall.objects.filter(SUB_A_etrap=etrap, DATE__range=[start,end]).order_by('DATE')
    # my_dict = {}
    # for i in callsObj:
    #     if int(i.SUB_A) not in my_dict:
    #         my_dict[int(i.SUB_A)] = [[i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price]]
    #     else:
    #         my_dict[int(i.SUB_A)].append([i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price])


    zakaz = Zakaz.objects.filter(DATE__range=[start,f"{end} 23:59:59"])
    dict_z = {} # [[count, DATE, NUMBER_B, NUMBER_LOCATIONS, MT, total_price], [count, DATE, NUMBER_B, NUMBER_LOCATIONS, MT, total_price]]
    total_zakaz_count = 0
    total_zakaz_minut = 0
    total_zakaz_price = 0
    for z in zakaz:
        if float(z.total_price) > 0:
            num = int(z.NUMBER_A)
            if num not in dict_z:
                dict_z[num] = [[1, f'{z.DATE.hour}:{z.DATE.minute}:{z.DATE.second}', z.NUMBER_B, z.NUMBER_LOCATIONS, z.MT, z.total_price, f'{z.DATE.day}']]
            else:
                count_z = dict_z[num][-1][0] + int(1)
                dict_z[num].append([count_z, f'{z.DATE.hour}:{z.DATE.minute}:{z.DATE.second}', z.NUMBER_B, z.NUMBER_LOCATIONS, z.MT, z.total_price, f'{z.DATE.day}'])
                

    

    count = 0
    testCount = 0
    umumyPrice = 0
    umumyMinut = 0

    
    for user in users:
        
        testCount += 1
     

        try:
            calls = my_dict[int(user.number)]
        except:
            if etrap == 'Dashoguz' and int(user.number) in dict_z:
                num_z = int(user.number)
                surname_z = user.surname
                name_z = user.name
                account_z = user.account
                # Шапка #
                lines.append(f'\n           "Turkmenaragatnasyk" ministrligi. "Dasoguztelekom" WEAK\n')

            
                lines.append(f'Dasoguz saheri, Turkmenbasybank, H/H 23201934131327400056000  tel.52327,50026\n')

                if year_is_new:
                    lines.append(f'       01/{month_numb}/{year} - 01/{month_numbPlus1}/{new_year} dowur ucin aragatansyk hyzmatlarynyn\n')
                else:
                    lines.append(f'       01/{month_numb} - 01/{month_numbPlus1}/{new_year} dowur ucin aragatansyk hyzmatlarynyn\n')
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

                lines.append(f'                        HASAPLASYK-HASABY №{zeros}{count}\n')
                # Шапка END #

                lines.append(' --------------------------------------------------------------------------\n')
                lines.append(f" Abonent_{num_z}   {surname_z}   {name_z}\n")
                lines.append(f" HASAP № {account_z}\n")
                lines.append(' --------------------------------------------------------------------------\n')
                lines.append(f" GUNI  WAGTY   TELEFON              UGRY           MIN. MANAT  Bellik.\n")
                lines.append(f" ---------------------- Sargyt geplesikler (zakaz) ----------------------- \n")
                for z in dict_z[int(user.number)]:
                    lines.append(f"  {z[6]}   {z[1]}   {z[2]}      {z[3]} {z[4]}   {float(z[5]):.2f}\n")
                    c_z = z[0]
                    t_m_z += int(z[4])
                    t_p_z += float(z[5])
                    total_zakaz_count += 1
                    total_zakaz_minut += int(z[4])
                    total_zakaz_price += float(z[5])
                lines.append(' --------------------------------------------------------------------------\n')
                lines.append(f" Jemi geplesikler: {c_z}              UMUMY JEMI:  {'%.2f' % t_p_z}m.\n\n")
                lines.append(f" \n{zeros}{count}-------------------------------------------------------------------\n\n")
            continue


        
    
        # Шапка #
        lines.append(f'\n           "Turkmenaragatnasyk" ministrligi. "Dasoguztelekom" WEAK\n')

        if etrap == 'Dashoguz':
            lines.append(f'Dasoguz saheri, Turkmenbasybank, H/H 23201934131327400056000  tel.52327,50026\n')
        elif etrap in etraps:
            lines.append(f'{etrap} etraby, Turkmenbasybank, H/H 23201934131327400056000  tel.52327,50026\n')
        elif etrap == 'all':
            lines.append(f'Dashoguz welayaty, Turkmenbasybank, H/H 23201934131327400056000  tel.52327,50026\n')

        if year_is_new:
            lines.append(f'       01/{month_numb}/{year} - 01/{month_numbPlus1}/{new_year} dowur ucin aragatansyk hyzmatlarynyn\n')
        else:
            lines.append(f'       01/{month_numb} - 01/{month_numbPlus1}/{new_year} dowur ucin aragatansyk hyzmatlarynyn\n')
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

        lines.append(f'                        HASAPLASYK-HASABY №{zeros}{count}\n')
        # Шапка END #


        lines.append(' --------------------------------------------------------------------------\n')
        lines.append(f" Abonent_{user.number}   {user.surname}   {user.name}\n")
        lines.append(f" HASAP № {user.account}\n")
        lines.append(' --------------------------------------------------------------------------\n')
        lines.append(f" GUNI  WAGTY   TELEFON              UGRY           MIN. MANAT  Bellik.\n")
        lines.append(f" ---------------------- KOD b-ca geplesikler (AMTS) -----------------------\n")

        callCount = 0
        price = 0

        for values in calls:
            callCount += 1
            price += float(values[5])
            umumyPrice += float(values[5])
            umumyMinut += int(values[4])
            s1 = (20 - len(values[3])) * ' '
            lines.append(f"  {str(values[0])[8:10]}   {str(values[1])}   {values[2]}      {values[3]}{s1}{values[4]}   {values[5]}\n")

            

        lines.append(' --------------------------------------------------------------------------\n')
        lines.append(f" Jemi geplesikler: {callCount}               UMUMY JEMI:  {'%.2f' % price}m.\n")

        c_z = 0
        t_m_z = 0
        t_p_z = 0
        
        if etrap == 'Dashoguz' and int(user.number) in dict_z:
            lines.append('---------------------- Sargyt geplesikler (zakaz) -----------------------\n')
            for z in dict_z[int(user.number)]:
                lines.append(f"  {z[6]}   {z[1]}   {z[2]}      {z[3]} {z[4]}   {z[5]}\n")
                c_z = z[0]
                t_m_z += int(z[4])
                t_p_z += float(z[5])
                total_zakaz_count += 1
                total_zakaz_minut += int(z[4])
                total_zakaz_price += float(z[5])
            lines.append(' --------------------------------------------------------------------------\n')
            lines.append(f" Jemi geplesikler: {c_z}              UMUMY JEMI:  {'%.2f' % t_p_z}m.\n")
            lines.append(' --------------------------------------------------------------------------\n')
            lines.append(f" Jemi geplesikler: {c_z+ callCount}                  UMUMY JEMI:      {'%.2f' % (t_p_z + price)}m.\n")
        lines.append(f" \n{zeros}{count}-------------------------------------------------------------------\n\n")

    print('total_zakaz_price',total_zakaz_price)
    print('umumyPrice',umumyPrice)
    lines.append(f'\n\n\n---- AMTC Umumy Manat {(umumyPrice):.2f}-------Umumy Minut  {(umumyMinut):.2f}\n\n')
    lines.append(f'---- ZAKAZ Umumy Manat {(total_zakaz_price):.2f}-------Umumy Minut  {(total_zakaz_minut):.2f}\n\n')
    

    bell()



            

        
 


    response.writelines(lines)
    return response






# from django.shortcuts import redirect
# from django.contrib import messages

# from telekom.models import NachMinus, NonLocalCall, PayHistory, UserTable, Zakaz
# from telekom.views2.myFunc.myFunc import monthСonvert
# from calendar import monthrange
# from datetime import datetime, timedelta

# # для .txt
# from django.http import HttpResponse
# import sys
# def bell():
#     sys.stdout.write('\r\a')
#     sys.stdout.flush()






# def P_txt (request, year, month, etrap):

#     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']

#     response = HttpResponse(content_type="text/plain")
#     txtName = f'{etrap} P TXT {monthСonvert(month)}-{year} {etrap}'
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
#         month_numbPlus1 = '1'
#         if len(month_numbPlus1) == 1:
#             month_numbPlus1 = f"0{month_numbPlus1}"
#         new_year = year
#         print('new_year1', new_year)
#         new_year = str(int(year) + 1)
#         print('new_year2', new_year)



#         year_is_new = True

#     if len(month_numb) == 1:
#         month_numb = f"0{month_numb}"

#     days_in_nach_month = monthrange(int(year), int(month_numb))[1]
#     start = f"{year}-{month_numb}-01"
#     convert_date = datetime.strptime(start, "%Y-%m-%d")
#     end2 = convert_date + timedelta(days=int(days_in_nach_month))
#     next_year = end2.year
#     next_month = end2.month
#     end3 = f"{next_year}-{next_month}-01"
#     end = f"{year}-{month_numb}-{days_in_nach_month}"

#     print('GGGGGGGGGGGGGGGG', end2)
#     if etrap in etraps:
#         users = UserTable.objects.filter(is_enterprises = True, etrap=etrap).order_by('account')
#     elif etrap == 'all':
#         pass
#         # users = UserTable.objects.filter(is_enterprises = True).order_by('account')
#     else:
#         users = []


#     lines = []
#     print('start, end',start, end)


#     # lines.append(f"  {str(call.DATE)[8:10]}   {str(call.START[:5])}   {call.SUB_B}      {call.SUB_B_locations}{s1}{call.MT}   {call.total_price}\n")
#     callsObj = NonLocalCall.objects.filter(SUB_A_etrap=etrap, DATE__range=[start,end]).order_by('DATE')
#     my_dict = {} # {number: [[DATE, START, SUB_B, SUB_B_loc, MT, total_price], [DATE, START, SUB_B, SUB_B_loc, MT, total_price]]}
#     for i in callsObj:
#         if int(i.SUB_A) not in my_dict:
#             my_dict[int(i.SUB_A)] = [[i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price]]
#         else:
#             my_dict[int(i.SUB_A)].append([i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price])

   

    
#     zakaz = Zakaz.objects.filter(DATE__range=[start,f"{end} 23:59:59"])
#     dict_z = {} # [[count, DATE, NUMBER_B, NUMBER_LOCATIONS, MT, total_price], [count, DATE, NUMBER_B, NUMBER_LOCATIONS, MT, total_price]]
#     total_zakaz_count = 0
#     total_zakaz_minut = 0
#     total_zakaz_price = 0
#     for z in zakaz:
#         if float(z.total_price) > 0:
#             num = int(z.NUMBER_A)
#             if num not in dict_z:
#                 dict_z[num] = [[1, f'{z.DATE.hour}:{z.DATE.minute}:{z.DATE.second}', z.NUMBER_B, z.NUMBER_LOCATIONS, z.MT, z.total_price, f'{z.DATE.day}']]
#             else:
#                 count_z = dict_z[num][-1][0] + int(1)
#                 dict_z[num].append([count_z, f'{z.DATE.hour}:{z.DATE.minute}:{z.DATE.second}', z.NUMBER_B, z.NUMBER_LOCATIONS, z.MT, z.total_price, f'{z.DATE.day}'])
                

    

#     count = 0
#     testCount = 0
#     umumyPrice = 0
#     umumyMinut = 0

    
#     for user in users:
        
#         testCount += 1
     

#         try:
#             calls = my_dict[int(user.number)]
#         except:
#             if etrap == 'Dashoguz' and int(user.number) in dict_z:
#                 num_z = int(user.number)
#                 surname_z = user.surname
#                 name_z = user.name
#                 account_z = user.account
#                 # Шапка #
#                 lines.append(f'\n           "Turkmenaragatnasyk" ministrligi. "Dasoguztelekom" WEAK\n')

            
#                 lines.append(f'Dasoguz saheri, Turkmenbasybank, H/H 23201934131327400056000  tel.52327,50026\n')

#                 if year_is_new:
#                     lines.append(f'       01/{month_numb}/{year} - 01/{month_numbPlus1}/{new_year} dowur ucin aragatansyk hyzmatlarynyn\n')
#                 else:
#                     lines.append(f'       01/{month_numb} - 01/{month_numbPlus1}/{new_year} dowur ucin aragatansyk hyzmatlarynyn\n')
#                 count += 1
                
#                 if len(str(count)) == 1:
#                     zeros = '000000'
#                 elif len(str(count)) == 2:
#                     zeros = '00000'
#                 elif len(str(count)) == 3:
#                     zeros = '0000'
#                 elif len(str(count)) == 4:
#                     zeros = '0000'
#                 elif len(str(count)) == 5:
#                     zeros = '000'
#                 elif len(str(count)) == 6:
#                     zeros = '00'
#                 elif len(str(count)) == 7:
#                     zeros = '0'
#                 elif len(str(count)) == 8:
#                     zeros = ''

#                 lines.append(f'                        HASAPLASYK-HASABY №{zeros}{count}\n')
#                 # Шапка END #

#                 lines.append(' --------------------------------------------------------------------------\n')
#                 lines.append(f" Abonent_{num_z}   {surname_z}   {name_z}\n")
#                 lines.append(f" HASAP № {account_z}\n")
#                 lines.append(' --------------------------------------------------------------------------\n')
#                 lines.append(f" GUNI  WAGTY   TELEFON              UGRY           MIN. MANAT  Bellik.\n")
#                 lines.append(f" ---------------------- Sargyt geplesikler (zakaz) ----------------------- \n")
#                 for z in dict_z[int(user.number)]:
#                     lines.append(f"  {z[6]}   {z[1]}   {z[2]}      {z[3]} {z[4]}   {float(z[5]):.2f}\n")
#                     c_z = z[0]
#                     t_m_z += int(z[4])
#                     t_p_z += float(z[5])
#                     total_zakaz_count += 1
#                     total_zakaz_minut += int(z[4])
#                     total_zakaz_price += float(z[5])
#                 lines.append(' --------------------------------------------------------------------------\n')
#                 lines.append(f" Jemi geplesikler: {c_z}              UMUMY JEMI:  {'%.2f' % t_p_z}m.\n\n")
#                 lines.append(f" \n{zeros}{count}-------------------------------------------------------------------\n\n")
#             continue


        
    
#         # Шапка #
#         lines.append(f'\n           "Turkmenaragatnasyk" ministrligi. "Dasoguztelekom" WEAK\n')

#         if etrap == 'Dashoguz':
#             lines.append(f'Dasoguz saheri, Turkmenbasybank, H/H 23201934131327400056000  tel.52327,50026\n')
#         elif etrap in etraps:
#             lines.append(f'{etrap} etraby, Turkmenbasybank, H/H 23201934131327400056000  tel.52327,50026\n')
#         elif etrap == 'all':
#             lines.append(f'Dashoguz welayaty, Turkmenbasybank, H/H 23201934131327400056000  tel.52327,50026\n')

#         if year_is_new:
#             lines.append(f'       01/{month_numb}/{year} - 01/{month_numbPlus1}/{new_year} dowur ucin aragatansyk hyzmatlarynyn\n')
#         else:
#             lines.append(f'       01/{month_numb} - 01/{month_numbPlus1}/{new_year} dowur ucin aragatansyk hyzmatlarynyn\n')
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

#         lines.append(f'                        HASAPLASYK-HASABY №{zeros}{count}\n')
#         # Шапка END #


#         lines.append(' --------------------------------------------------------------------------\n')
#         lines.append(f" Abonent_{user.number}   {user.surname}   {user.name}\n")
#         lines.append(f" HASAP № {user.account}\n")
#         lines.append(' --------------------------------------------------------------------------\n')
#         lines.append(f" GUNI  WAGTY   TELEFON              UGRY           MIN. MANAT  Bellik.\n")
#         lines.append(f" ---------------------- KOD b-ca geplesikler (AMTS) -----------------------\n")

#         callCount = 0
#         price = 0

#         for values in calls:
#             callCount += 1
#             price += float(values[5])
#             umumyPrice += float(values[5])
#             umumyMinut += int(values[4])
#             s1 = (20 - len(values[3])) * ' '
#             lines.append(f"  {str(values[0])[8:10]}   {str(values[1])}   {values[2]}      {values[3]}{s1}{values[4]}   {values[5]}\n")

            

#         lines.append(' --------------------------------------------------------------------------\n')
#         lines.append(f" Jemi geplesikler: {callCount}               UMUMY JEMI:  {'%.2f' % price}m.\n")

#         c_z = 0
#         t_m_z = 0
#         t_p_z = 0
        
#         if etrap == 'Dashoguz' and int(user.number) in dict_z:
#             lines.append('---------------------- Sargyt geplesikler (zakaz) -----------------------\n')
#             for z in dict_z[int(user.number)]:
#                 lines.append(f"  {z[6]}   {z[1]}   {z[2]}      {z[3]} {z[4]}   {z[5]}\n")
#                 c_z = z[0]
#                 t_m_z += int(z[4])
#                 t_p_z += float(z[5])
#                 total_zakaz_count += 1
#                 total_zakaz_minut += int(z[4])
#                 total_zakaz_price += float(z[5])
#             lines.append(' --------------------------------------------------------------------------\n')
#             lines.append(f" Jemi geplesikler: {c_z}              UMUMY JEMI:  {'%.2f' % t_p_z}m.\n")
#             lines.append(' --------------------------------------------------------------------------\n')
#             lines.append(f" Jemi geplesikler: {c_z+ callCount}                  UMUMY JEMI:      {'%.2f' % (t_p_z + price)}m.\n")
#         lines.append(f" \n{zeros}{count}-------------------------------------------------------------------\n\n")

#     print('total_zakaz_price',total_zakaz_price)
#     print('umumyPrice',umumyPrice)
#     lines.append(f'\n\n\n---- AMTC Umumy Manat {(umumyPrice):.2f}-------Umumy Minut  {(umumyMinut):.2f}\n\n')
#     lines.append(f'---- ZAKAZ Umumy Manat {(total_zakaz_price):.2f}-------Umumy Minut  {(total_zakaz_minut):.2f}\n\n')
    

#     bell()



            

        
 


#     response.writelines(lines)
#     return response


