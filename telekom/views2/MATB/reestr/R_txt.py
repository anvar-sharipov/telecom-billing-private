from django.shortcuts import redirect
from django.contrib import messages

from telekom.models import NachMinus, NonLocalCall, PayHistory, UserTable, Zakaz
from telekom.views2.myFunc.myFunc import get_sahypa, monthСonvert
from calendar import monthrange
from icecream import ic

# для .txt
from django.http import HttpResponse

from collections import OrderedDict
import sys
def bell():
    sys.stdout.write('\r\a')
    sys.stdout.flush()




def R_txt (request, year, month, etrap):
    ic(year, month)

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']

    response = HttpResponse(content_type="text/plain")
    txtName = f'{etrap} R TXT {monthСonvert(month)}-{year} {etrap}'
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
        new_year = str(int(year) + 1) # neznayu pochemu no etot kod rabotal 2 goda no 2 dekabre putaet goda, naprimer pri zaprose 2025 12 daet dannye s 2026 12
        # new_year = str(int(year))

        year_is_new = True

    if len(month_numb) == 1:
        month_numb = f"0{month_numb}"

    days_in_nach_month = monthrange(int(year), int(month_numb))[1]
    start = f"{year}-{month_numb}-01"
    end = f"{year}-{month_numb}-{days_in_nach_month}"

    if etrap in etraps:
        users = UserTable.objects.filter(account__isnull=False, etrap=etrap)
    elif etrap == 'all':
        users = UserTable.objects.filter(account__isnull=False)
    else:
        users = False
    # print('1111111111111111111', start, end, etrap)
    callsAll = NonLocalCall.objects.filter(SUB_A_etrap=etrap, DATE__range=[start,end]).order_by('DATE')
    # calls = NonLocalCall.objects.filter(DATE__range=[f"{year}-{month_digit}-01", f"{year}-{month_digit}-{days_in_choosed_month}"], SUB_A_etrap=etrap)
    total_test = 0
    for i in callsAll:
        total_test += i.total_price


    print('start, end',start, end)

    # ✅ По просьбе пользователя: "Jemi HOZ (AMTC)"/"Jemi BUD (AMTC)" должны
    # быть равны бакетам Hoz/Bud в trafik.py — там звонок относится к Хоз/
    # Бюджету по его СОБСТВЕННОМУ edara (см. trafik.py::classify_call, ATS
    # проверяется первым и не попадает ни в Bud, ни в Hoz), а не по текущему
    # user.hb.name абонента (то же расхождение, что чинили в N_txt.py — если
    # у абонента hb поменяли ПОСЛЕ начисления, старая логика всё равно суммировала
    # его звонки под текущим hb, суммы не сходились с trafik.py). Поэтому здесь
    # к каждому звонку добавляем его edara, и дальше классифицируем по нему.
    ATSSALDO = -698 if etrap == 'Dashoguz' else -700
    numbersATS = set(int(u.number) for u in UserTable.objects.filter(account=ATSSALDO, etrap=etrap))

    my_dict = {}
    for i in callsAll:
        if int(i.SUB_A) not in my_dict:
            my_dict[int(i.SUB_A)] = [[i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, i.total_price, i.edara]]
        else:
           my_dict[int(i.SUB_A)].append([i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, i.total_price, i.edara])

    lines = []

    count = 0
    testCount = 0

    # {account: {key: [number, surname, name, count, total, tag]}} — key синтетический
    # (number_H / number_B), т.к. у одного абонента теперь может быть отдельная
    # строка под Hoz и отдельная под Bud, если за месяц его edara менялся.
    accountJemi = {}
    accountLenCalls = {}
    for user in users:
        testCount += 1

        try:
            calls = my_dict[int(user.number)]
        except:
            continue

        if len(calls) == 0:
            continue

        # ✅ По просьбе пользователя: в R_txt.py АТС-номера целиком идут в Hoz
        # (независимо от edara на их звонках) — разделение Hoz/ATS как отдельных
        # категорий существует только в trafik.py, здесь ATS — просто часть Hoz.
        is_ats = int(user.number) in numbersATS
        if is_ats:
            hoz_calls = calls
            bud_calls = []
        else:
            hoz_calls = [c for c in calls if c[6] == 'H']
            bud_calls = [c for c in calls if c[6] == 'B']
        if not hoz_calls and not bud_calls:
            continue  # ни одного Hoz/Bud/ATS звонка (Население/Неопознанные этому реестру не интересны)

        accountLenCalls[user.account] = accountLenCalls.get(user.account, 0) + len(hoz_calls) + len(bud_calls)
        accountJemi.setdefault(user.account, {})

        for tag, tag_calls in (('H', hoz_calls), ('B', bud_calls)):
            if not tag_calls:
                continue
            key = f"{user.number}_{tag}"
            total = sum(float(c[5]) for c in tag_calls)
            accountJemi[user.account][key] = [user.number, user.surname, user.name, len(tag_calls), total, tag]


    accountJemi = OrderedDict(sorted(accountJemi.items()))

    total_z_bud = 0
    total_z_hoz = 0
    ic(start)
    ic(end)
    if etrap == 'Dashoguz':
        zakaz = Zakaz.objects.filter(DATE__range=[start, end], total_price__gt=0)
        users_z = UserTable.objects.filter(etrap='Dashoguz', is_enterprises=True)
        dict_z_u = {}
        for u in users_z:
            num = int(u.number)
            if num not in dict_z_u:
                ady = f"{u.surname} {u.name}"
                dict_z_u[num] = [u.account, ady]
        print(new_year, month_numb)
        nachs_z =  NachMinus.objects.filter(year=year, month=month_numb, user__etrap='Dashoguz', zakaz__gt=0)
        dict_z = {}
        for n in nachs_z:
            num = int(n.user.number)
            if num in dict_z_u:
                if num == 92499:
                    print('tut3', num)
                account = dict_z_u[num][0]
                if account < 0:
                    total_z_hoz +=  n.zakaz
                else:
                    total_z_bud +=  n.zakaz

                ady = dict_z_u[num][1]
                price = n.zakaz
                if account in dict_z:
                    dict_z[account].append([num, ady, price])
                else:
                    dict_z[account] = [[num, ady, price]]
            






    umumy_manat_hoz = 0    
    umumy_manat_bud = 0    

    for account, val in accountJemi.items():
   
        # для Hoz
        umumy_jemi = 0
        umumy_jemi10proc = 0
        jemi_tolege = 0

        # Для edara bud
        jemi_tolege_Bud = 0

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


                
        sahypa = get_sahypa(accountLenCalls[account])
        if sahypa == False:
            continue
    

        lines.append(f"                            REYESTR {zeros}{count} Sahypa:{sahypa} \n")
        lines.append(f"==========================================================================\n")

        if year_is_new:
            lines.append(f"HASAP N:{account}               01/{month_numb}/{year} - 01/{month_numbPlus1}/{new_year}\n")
        else:
            lines.append(f"HASAP N:{account}               01/{month_numb} - 01/{month_numbPlus1}/{new_year}\n")

        lines.append(f"--------------------------------------------------------------------------\n")

        if account > 0:
            lines.append(f"Telefon |  Edara, karhana                                         |  Jemi \n")
            lines.append(f"        |                                                         | tolege\n")
            lines.append(f"        |                                                         |\n")
            lines.append(f"--------|---------------------------------------------------------|-------\n")     

        else:
            lines.append(f"Telefon |  Edara, karhana                      |        | \n") #| Aragat.|  Jemi
            lines.append(f"        |                                      |  Jemi  |\n") #| hyzmat | tolege
            lines.append(f"        |                                      |        |\n") #|   10%  |
            lines.append(f"--------|--------------------------------------|--------|--------|--------\n")


        # ✅ value теперь [number, surname, name, count, total, tag] — номер
        # печатаем из value[0] (реальный телефон), а не из ключа словаря
        # (ключ синтетический "number_H"/"number_B", см. цикл сборки выше).
        for _key, value in val.items():
            number = value[0]

            if value[1] != '' and value[2] == '':
                s1 = (40 - len(value[1])) * ' '
                s2 = ''

            if value[1] == '' and value[2] != '':
                s1 = ''
                s2 = (40 - len(value[2])) * ' '

            if value[1] == '' and value[2] == '':
                s1 = (20 - len(value[1])) * ' '
                s2 = (20 - len(value[2])) * ' '

            if value[1] != '' and value[2] != '':
                s1 = (20 - len(value[1])) * ' '
                s2 = (20 - len(value[2])) * ' '

            # [number, surname, name, count, total, tag]

            if value[5] == 'B':
                lines.append(f" {number}   {value[1]}{s1}{value[2]}{s2}{'%.2f' % value[4]}\n")
                jemi_tolege_Bud += value[4]
                umumy_manat_bud += value[4]
            elif value[5] == 'H':
                lines.append(f" {number}   {value[1]}{s1}{value[2]}{s2}{'%.2f' % value[4]}    \n")
                umumy_manat_hoz += value[4]
                jemi_tolege += value[4]
                umumy_jemi10proc += value[4]
                umumy_jemi += value[4] + (value[4])

        if account > 0:
            lines.append(f"-------------------------------------------------------------------------\n")
            lines.append(f"                                                    UMUMY JEMI:    {'%.2f' % jemi_tolege_Bud}\n\n")
            if etrap == 'Dashoguz' and account in dict_z:
                lines.append('---------------------- Sargyt geplesikler (zakaz) -----------------------\n')
                tot_z_bud = 0
                for acc_z, val_z in dict_z.items():
                    for v in val_z:
                        if account == acc_z:
                            z1 = (40 - len(v[1])) * ' '
                            lines.append(f" {v[0]}   {v[1]}{z1}{v[2]:.2f}\n")
                            tot_z_bud += v[2]
                jemi_tolege_Bud += tot_z_bud
                lines.append(f"-------------------------------------------------------------------------\n")
                lines.append(f"                                                    UMUMY JEMI:    {'%.2f' % jemi_tolege_Bud}\n")
            lines.append(f"{zeros}{count}------------------------------------------------------------------\n\n")
        else:
            lines.append(f"--------------------------------------------------------------------------\n")
            lines.append(f"                                 UMUMY JEMI:     {'%.2f' % jemi_tolege}     \n\n") # {'%.2f' % umumy_jemi10proc}      {'%.2f' % umumy_jemi}
            if etrap == 'Dashoguz' and account in dict_z:
                print('tut1', dict_z)
                lines.append('---------------------- Sargyt geplesikler (zakaz) -----------------------\n')
                tot_z_hoz = 0
                for acc_z, val_z in dict_z.items():
                    for v in val_z:
                        if account == acc_z:
                            z1 = (40 - len(v[1])) * ' '
                            print('tut4', v)
                            lines.append(f" {v[0]}   {v[1]}{z1}{v[2]:.2f}\n")
                            tot_z_hoz += v[2]
                jemi_tolege += tot_z_hoz
                lines.append(f"--------------------------------------------------------------------------\n")
                lines.append(f"                                 UMUMY JEMI:     {'%.2f' % jemi_tolege}     \n") # {'%.2f' % umumy_jemi10proc}      {'%.2f' % umumy_jemi}
            lines.append(f"{zeros}{count}-------------------------------------------------------------------\n\n")
            

        

      
    bell()
    
    lines.append(f"Jemi HOZ (AMTC) {(umumy_manat_hoz):.2f}\n")
    lines.append(f"Jemi BUD (AMTC) {(umumy_manat_bud):.2f}\n\n")

    lines.append(f"Jemi HOZ (ZAKAZ) {(total_z_hoz):.2f}\n")
    lines.append(f"Jemi BUD (ZAKAZ) {(total_z_bud):.2f}\n\n")

    print('umumy_manat_hoz', f"{(umumy_manat_hoz + total_z_hoz):.2f}")
    print('umumy_manat_bud', f"{(umumy_manat_bud + total_z_bud):.2f}")
    response.writelines(lines)
    return response


# rabotaet no pered razdeleniem etrapow
# from django.shortcuts import redirect
# from django.contrib import messages

# from telekom.models import NachMinus, NonLocalCall, PayHistory, UserTable, Zakaz
# from telekom.views2.myFunc.myFunc import get_sahypa, monthСonvert
# from calendar import monthrange

# # для .txt
# from django.http import HttpResponse

# from collections import OrderedDict
# import sys
# def bell():
#     sys.stdout.write('\r\a')
#     sys.stdout.flush()




# def R_txt (request, year, month, etrap):

#     etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

#     response = HttpResponse(content_type="text/plain")
#     txtName = f'{etrap} R TXT {monthСonvert(month)}-{year} {etrap}'
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
#         new_year = str(int(year) + 1)

#         year_is_new = True

#     if len(month_numb) == 1:
#         month_numb = f"0{month_numb}"

#     days_in_nach_month = monthrange(int(year), int(month_numb))[1]
#     start = f"{year}-{month_numb}-01"
#     end = f"{year}-{month_numb}-{days_in_nach_month}"

#     if etrap in etraps:
#         users = UserTable.objects.filter(account__isnull=False, etrap=etrap)
#     elif etrap == 'all':
#         users = UserTable.objects.filter(account__isnull=False)
#     else:
#         users = False
#     print('1111111111111111111', start, end, etrap)
#     callsAll = NonLocalCall.objects.filter(SUB_A_etrap=etrap, DATE__range=[start,end]).order_by('DATE')
#     # calls = NonLocalCall.objects.filter(DATE__range=[f"{year}-{month_digit}-01", f"{year}-{month_digit}-{days_in_choosed_month}"], SUB_A_etrap=etrap)
#     total_test = 0
#     for i in callsAll:
#         total_test += i.total_price


#     print('start, end',start, end)

#     my_dict = {}
#     for i in callsAll:
#         if int(i.SUB_A) not in my_dict:
#             # my_dict[int(i.SUB_A)] = [[i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price]]
#             my_dict[int(i.SUB_A)] = [[i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, i.total_price]]
#         else:
#         #    my_dict[int(i.SUB_A)].append([i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, '%.2f' % i.total_price])
#            my_dict[int(i.SUB_A)].append([i.DATE, i.START, i.SUB_B, i.SUB_B_locations, i.MT, i.total_price])

#     lines = []

#     count = 0
#     testCount = 0

#     # {account: {number: [surname, name, len(calls), 0], number2: [surname, name, len(calls), 0]}}
#     # accountLenCalls = 0
#     accountJemi = {}
#     accountLenCalls = {}
#     for user in users:
#         testCount += 1

#         # calls = NonLocalCall.objects.filter(SUB_A_etrap=user.etrap, SUB_A=user.number, type='intercity', DATE__range=[start,end]).order_by('DATE')
#         try:
#             calls = my_dict[int(user.number)]
#         except:
#             continue

#         if len(calls) == 0:
#             continue

#         if user.account not in accountLenCalls:
#             accountLenCalls[user.account] = len(calls)
#         else:
#             accountLenCalls[user.account] += len(calls)

#         if user.account not in accountJemi:
#             accountJemi[user.account] = {user.number: [user.surname, user.name, len(calls), 0, user.hb.name]}
#             for call in calls:
#                 accountJemi[user.account][user.number][3] += float(call[5])
#         else:
#             if user.number not in accountJemi[user.account]:
#                 accountJemi[user.account][user.number] = [user.surname, user.name, len(calls), 0, user.hb.name]
#             else:
#                 accountJemi[user.account][user.number][2] += len(calls)
#             for call in calls:
#                 accountJemi[user.account][user.number][3] += float(call[5])
#                 accountJemi[user.account][user.number][4] = user.hb.name


#     accountJemi = OrderedDict(sorted(accountJemi.items()))

#     total_z_bud = 0
#     total_z_hoz = 0
#     if etrap == 'Dashoguz':
#         zakaz = Zakaz.objects.filter(DATE__range=[start, end], total_price__gt=0)
#         users_z = UserTable.objects.filter(etrap='Dashoguz', is_enterprises=True)
#         dict_z_u = {}
#         for u in users_z:
#             num = int(u.number)
#             if num not in dict_z_u:
#                 ady = f"{u.surname} {u.name}"
#                 dict_z_u[num] = [u.account, ady]

#         nachs_z =  NachMinus.objects.filter(year=new_year, month=month_numb, user__etrap='Dashoguz', zakaz__gt=0)
#         dict_z = {}
#         for n in nachs_z:
#             num = int(n.user.number)
#             if num in dict_z_u:
#                 if num == 92499:
#                     print('tut3', num)
#                 account = dict_z_u[num][0]
#                 if account < 0:
#                     total_z_hoz +=  n.zakaz
#                 else:
#                     total_z_bud +=  n.zakaz

#                 ady = dict_z_u[num][1]
#                 price = n.zakaz
#                 if account in dict_z:
#                     dict_z[account].append([num, ady, price])
#                 else:
#                     dict_z[account] = [[num, ady, price]]
            






#     umumy_manat_hoz = 0    
#     umumy_manat_bud = 0    

#     for account, val in accountJemi.items():
   
#         # для Hoz
#         umumy_jemi = 0
#         umumy_jemi10proc = 0
#         jemi_tolege = 0

#         # Для edara bud
#         jemi_tolege_Bud = 0

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


                
#         sahypa = get_sahypa(accountLenCalls[account])
#         if sahypa == False:
#             continue
    

#         lines.append(f"                            REYESTR {zeros}{count} Sahypa:{sahypa} \n")
#         lines.append(f"==========================================================================\n")

#         if year_is_new:
#             lines.append(f"HASAP N:{account}               01/{month_numb}/{year} - 01/{month_numbPlus1}/{new_year}\n")
#         else:
#             lines.append(f"HASAP N:{account}               01/{month_numb} - 01/{month_numbPlus1}/{new_year}\n")

#         lines.append(f"--------------------------------------------------------------------------\n")

#         if account > 0:
#             lines.append(f"Telefon |  Edara, karhana                                         |  Jemi \n")
#             lines.append(f"        |                                                         | tolege\n")
#             lines.append(f"        |                                                         |\n")
#             lines.append(f"--------|---------------------------------------------------------|-------\n")     

#         else:
#             lines.append(f"Telefon |  Edara, karhana                      |        | \n") #| Aragat.|  Jemi
#             lines.append(f"        |                                      |  Jemi  |\n") #| hyzmat | tolege
#             lines.append(f"        |                                      |        |\n") #|   10%  |
#             lines.append(f"--------|--------------------------------------|--------|--------|--------\n")


#         for number,  value in val.items():

#             if value[0] != '' and value[1] == '':
#                 s1 = (40 - len(value[0])) * ' '
#                 s2 = ''

#             if value[0] == '' and value[1] != '':
#                 s1 = ''
#                 s2 = (40 - len(value[1])) * ' '

#             if value[0] == '' and value[1] == '':
#                 s1 = (20 - len(value[0])) * ' '
#                 s2 = (20 - len(value[1])) * ' '

#             if value[0] != '' and value[1] != '':
#                 s1 = (20 - len(value[0])) * ' '
#                 s2 = (20 - len(value[1])) * ' '

#             # [user.surname, user.name, len(calls), 0]}

         
#             if value[4] == 'B':
#             # if account > 0:
#                 lines.append(f" {number}   {value[0]}{s1}{value[1]}{s2}{'%.2f' % value[3]}\n")
#                 jemi_tolege_Bud += value[3]
#                 umumy_manat_bud += value[3]
#             elif value[4] == 'H':
#             # elif account < 0:
#                 # print(account)
#                 lines.append(f" {number}   {value[0]}{s1}{value[1]}{s2}{'%.2f' % value[3]}    \n") #{'%.2f' % (value[3] * 0.10)}      {'%.2f' % (value[3] + (value[3] * 0.10))}
#                 # print(value[3])
#                 umumy_manat_hoz += value[3]
#                 jemi_tolege += value[3]
#                 umumy_jemi10proc += value[3]
#                 umumy_jemi += value[3] + (value[3])

#         if account > 0:
#             lines.append(f"-------------------------------------------------------------------------\n")
#             lines.append(f"                                                    UMUMY JEMI:    {'%.2f' % jemi_tolege_Bud}\n\n")
#             if etrap == 'Dashoguz' and account in dict_z:
#                 lines.append('---------------------- Sargyt geplesikler (zakaz) -----------------------\n')
#                 tot_z_bud = 0
#                 for acc_z, val_z in dict_z.items():
#                     for v in val_z:
#                         if account == acc_z:
#                             z1 = (40 - len(v[1])) * ' '
#                             lines.append(f" {v[0]}   {v[1]}{z1}{v[2]:.2f}\n")
#                             tot_z_bud += v[2]
#                 jemi_tolege_Bud += tot_z_bud
#                 lines.append(f"-------------------------------------------------------------------------\n")
#                 lines.append(f"                                                    UMUMY JEMI:    {'%.2f' % jemi_tolege_Bud}\n")
#             lines.append(f"{zeros}{count}------------------------------------------------------------------\n\n")
#         else:
#             lines.append(f"--------------------------------------------------------------------------\n")
#             lines.append(f"                                 UMUMY JEMI:     {'%.2f' % jemi_tolege}     \n\n") # {'%.2f' % umumy_jemi10proc}      {'%.2f' % umumy_jemi}
#             if etrap == 'Dashoguz' and account in dict_z:
#                 print('tut1', dict_z)
#                 lines.append('---------------------- Sargyt geplesikler (zakaz) -----------------------\n')
#                 tot_z_hoz = 0
#                 for acc_z, val_z in dict_z.items():
#                     for v in val_z:
#                         if account == acc_z:
#                             z1 = (40 - len(v[1])) * ' '
#                             print('tut4', v)
#                             lines.append(f" {v[0]}   {v[1]}{z1}{v[2]:.2f}\n")
#                             tot_z_hoz += v[2]
#                 jemi_tolege += tot_z_hoz
#                 lines.append(f"--------------------------------------------------------------------------\n")
#                 lines.append(f"                                 UMUMY JEMI:     {'%.2f' % jemi_tolege}     \n") # {'%.2f' % umumy_jemi10proc}      {'%.2f' % umumy_jemi}
#             lines.append(f"{zeros}{count}-------------------------------------------------------------------\n\n")
            

        

      
#     bell()
    
#     lines.append(f"Jemi HOZ (AMTC) {(umumy_manat_hoz):.2f}\n")
#     lines.append(f"Jemi BUD (AMTC) {(umumy_manat_bud):.2f}\n\n")

#     lines.append(f"Jemi HOZ (ZAKAZ) {(total_z_hoz):.2f}\n")
#     lines.append(f"Jemi BUD (ZAKAZ) {(total_z_bud):.2f}\n\n")

#     print('umumy_manat_hoz', f"{(umumy_manat_hoz + total_z_hoz):.2f}")
#     print('umumy_manat_bud', f"{(umumy_manat_bud + total_z_bud):.2f}")
#     response.writelines(lines)
#     return response
