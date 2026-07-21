from django.shortcuts import redirect

from telekom.models import NonLocalCall, UserTable
from telekom.views2.myFunc.myFunc import monthСonvert

from calendar import monthrange
from datetime import datetime

# для .txt
from django.http import HttpResponse


def globalError(request, year, month):
    month_numb = monthСonvert(month)
    try:
        days_in_nach_month = monthrange(int(year), int(month_numb))[1]
    except:
        return redirect('kod-nachisleniya')
    response = HttpResponse(content_type="text/plain")
    txtName = f'{year} {month_numb} none local error nachisleniya'
    response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
    lines = [f"{txtName} \n\n"]

    first = f"{year}-{month_numb}-01"
    last = f"{year}-{month_numb}-{days_in_nach_month}"

    globalCalls = NonLocalCall.objects.filter(DATE__range=[first, last]).order_by('DATE')
    users = UserTable.objects.all()

    userTable = {}

    for call in globalCalls:
        if f"{call.SUB_A}{call.SUB_A_etrap}" not in userTable:
            userTable[f"{call.SUB_A}{call.SUB_A_etrap}"] = [[call.SUB_B, call.SUB_B_locations, call.DATE, call.START, call.FIN, call.DUR, call.MT, call.price, call.total_price]]
        else:
            userTable[f"{call.SUB_A}{call.SUB_A_etrap}"].append([call.SUB_B, call.SUB_B_locations, call.DATE, call.START, call.FIN, call.DUR, call.MT, call.price, call.total_price])


    
    umumyJemiMT = 0
    umumyJemiPrice = 0
    count = 0
    for key, calls in userTable.items():
        count2 = 0
        number = key[:5]
        etrap = key[5:]
        totalMtSuccess = 0
        totalSuccessPrice = 0
        if users.filter(number=key[:5], etrap=key[5:]):
            pass
        else:
            count += 1
            lines.append(f"{count}.    {etrap} {number} \n\n")
            for i in calls:
                count2 += 1
                s1 = (15 - len(i[0])) * ' '
                s2 = ((5 - int(len(str(count2)))) * ' ')
                s3 = ((3 - int(len(i[6]))) * ' ')
                s4 = ((5 - int(len(str(i[8])))) * ' ')
                lines.append(f"    {count2}.{s2} {i[0]}{s1} {i[2]} {i[3]} {i[4]} {i[5]} {i[6]}{s3} {i[7]} {i[8]}{s4} {i[1]} \n")
                totalMtSuccess += int(i[6])
                umumyJemiMT += int(i[6])
                totalSuccessPrice += float(i[8])
                umumyJemiPrice += float(i[8])
            lines.append(f"\n                  Umumy minut: {totalMtSuccess}       Umumy manat: {totalSuccessPrice}\n")
            lines.append(f"===================================================================================================\n\n")

    lines.append(f"\n\n\n    Umumy Jemi minut: {umumyJemiMT}                   Umumy jemi manat:{umumyJemiPrice} \n\n")

    response.writelines(lines)
    return response