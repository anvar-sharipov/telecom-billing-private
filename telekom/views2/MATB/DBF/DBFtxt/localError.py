from django.shortcuts import redirect

from telekom.models import LocalCall, UserTable
from telekom.views2.myFunc.myFunc import monthСonvert

from calendar import monthrange
from datetime import datetime

# для .txt
from django.http import HttpResponse
# для сортировки словаря по ключу
import collections


def localError(request, year, month):
    month_numb = monthСonvert(month)
    try:
        days_in_nach_month = monthrange(int(year), int(month_numb))[1]
    except:
        return redirect('slr-nachisleniya')
    response = HttpResponse(content_type="text/plain")
    txtName = f'{year} {month_numb} local error nachisleniya'
    response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
    lines = [f"{txtName} \n\n"]

    first = f"{year}-{month_numb}-01"
    last = f"{year}-{month_numb}-{days_in_nach_month}"
    localCalls = LocalCall.objects.filter(DATE__range=[first, last])

    



    # Users = UserTable.objects.values('number', 'etrap')

    

    # ['20000Dashoguz', '20000Akdepe']
    # list_of = []
    # for dict_ in Users:
    #     for key, val in dict_.items():
    #         if key == 'number':
    #             word = val
    #         if key == 'etrap':
    #             word += val

    # for call in localCalls:
    #     numberEtrap = f"{call.SUB_A}{call.etrap}"
    #     if numberEtrap not in list_of:
    #         lines.append(f"{call.SUB_A} {call.SUB_B} {call.DATE} {call.START} {call.FIN} {call.DUR} {call.MT} {etrap}")

    usersDict = {}
    for i in range(1, days_in_nach_month+1):        
            start = datetime(2023,int(month_numb),i)
            end = datetime(2023,int(month_numb),i)

            tables = localCalls.filter(DATE__range=[start, end])

            # делаем {20000Dashoguz: {date: [call, call, call], date2: [call, call, call]}, 20001Dashoguz: {date: [call, call, call]}}
            for table in tables:
                if f"{table.SUB_A}{table.etrap}" not in usersDict:
                    usersDict[f"{table.SUB_A}{table.etrap}"] = {f"{str(start)[:10]}": [[table.SUB_B, table.DATE, table.START, table.FIN, table.DUR, table.MT]]}
                else:
                    if f"{str(start)[:10]}" not in usersDict[f"{table.SUB_A}{table.etrap}"]:
                        usersDict[f"{table.SUB_A}{table.etrap}"][f"{str(start)[:10]}"] = [[table.SUB_B, table.DATE, table.START, table.FIN, table.DUR, table.MT]]
                    else:
                        usersDict[f"{table.SUB_A}{table.etrap}"][f"{str(start)[:10]}"].append([table.SUB_B, table.DATE, table.START, table.FIN, table.DUR, table.MT])





    Users = UserTable.objects.values('number', 'etrap')


    ['20000Dashoguz', '20000Akdepe']
    list_of = []
    for dict_ in Users:
        for key, val in dict_.items():
            if key == 'number':
                word = val
            if key == 'etrap':
                word += val
        
        list_of.append(word)
    
    # удаляем тех у которых меньше 5 минут разговора  
    usersDictCopy = usersDict.copy()
    for key, val in usersDictCopy.items():
        if key not in list_of:
            valCopy = val.copy() 
            for date, v in valCopy.items():
                total_MT = 0
                for i in v:
                    total_MT += int(i[5])
                if total_MT < 6:
                    del usersDict[key][date]
        else:
            del usersDict[key]

    

    orderedUsersDict = collections.OrderedDict(sorted(usersDict.items()))
    umumyNetto = 0
    umumyBrutto = 0
    count = 0
    for key, val in orderedUsersDict.items():
        if val:
            count += 1
            number = key[:5]
            etrap = key[5:]
            lines.append(f"{count}    {etrap} {number} \n")
            for date, v in val.items():
                count2 = 0
                lines.append(f'    {date} \n\n')
                total_MT = 0
                for i in v:
                    count2 += 1
                    s1 = ((5 - int(len(str(count2)))) * ' ')
                    lines.append(f"    {count2}.{s1} {i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]} \n")
                    total_MT += int(i[5])
                umumyNetto += total_MT - 5
                umumyBrutto += total_MT
                lines.append(f'    ---------------------------------------------\nJemi Minut Brutto: {total_MT};        Jemi manat: {"%.4f" % ((total_MT - 5) * 0.0006)}\n\n')
            lines.append(f"    =============================================\n")
    lines.append(f'    Jemi 1 ay minut Brutto: {umumyBrutto}   Jemi 1 ay minut Netto: {umumyNetto}    Jemi 1 ay manat:  {"%.4f" % (umumyNetto * 0.0006)}')
    response.writelines(lines)
    return response
    
