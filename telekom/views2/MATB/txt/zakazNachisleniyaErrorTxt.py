from telekom.models import NachMinus, UserTable, Zakaz

from django.http import HttpResponse

from telekom.views2.myFunc.myFunc import monthСonvert

from calendar import monthrange




def zakazNachisleniyaErrorTxt(request, year, month, etrap):

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    month_numb = monthСonvert(month)

    days_in_nach_month = str(monthrange(int(year), int(month_numb))[1])
    start = f'{year}-{month_numb}-01 00:00:00'
    end = f'{year}-{month_numb}-{str(days_in_nach_month)} 23:59:59'

    if etrap in etraps:
        zakazCalls = Zakaz.objects.filter(DATE__range=[start, end], action='заказ подтвержден', etrap=etrap)
        users = UserTable.objects.filter(etrap=etrap)
    elif etrap == 'all':
        zakazCalls = Zakaz.objects.filter(DATE__range=[start, end], action='заказ подтвержден')
        users = UserTable.objects.all()
    
    response = HttpResponse(content_type="text/plain")
    txtName = f'{etrap} Zakaz Nachisleniya Error {year}.{month_numb} {etrap}'
    response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
    lines = [f"{txtName} \n\n\n"]

    lines.append(f"                                                                                                               без %    с %     без %   с %  \n")
    lines.append(f"№        Дата/Время        SUB_A    etrap          SUB_B       SUB_B location                   DURATION   MT  1 min   1 min    jemi    jemi   type  action\n")
    
    lines.append(f"======================================================================================================================================================================\n")


    didntHaveUser = 0
    count = 0
    totalSum = 0
    totalSumProc = 0
    for call in zakazCalls:
        try:
            users.get(number=call.NUMBER_A, etrap=call.etrap)
        except:
            count += 1
            totalSum += float(call.total_price)
            totalSumProc += float(call.total_priceProc)
            s1 = (5 - int((len(str(count))))) * ' '
            s2 = (13 - len(call.etrap)) * ' '
            s3 = (18 - len(call.NUMBER_B)) * ' '
            locations = call.NUMBER_LOCATIONS if call.NUMBER_LOCATIONS != 'five' else 'Dashoguz'
            s4 = (30 - len(locations)) * ' '
            s5 = (11 - len(call.DUR)) * ' '
            s6 = (5 - len(call.MT)) * ' '
            s7 = (8 - len(str('%.2f' % float(call.price)))) * ' '
            s8 = (8 - len(str('%.2f' % float(call.priceProc)))) * ' '

            s9 = (8 - len(str('%.2f' % float(call.total_price)))) * ' '
            s10 = (8 - len(str('%.2f' % float(call.total_priceProc)))) * ' '
            s11 = (5 - len(call.CALL_TYPE)) * ' '
            s12 = (20 - len(call.action)) * ' '
            lines.append(f"{count}{s1}{call.DATE}   {call.NUMBER_A}   {call.etrap}{s2}{call.NUMBER_B}{s3}{locations}{s4}{call.DUR}{s5}{call.MT}{s6}{'%.2f' % float(call.price)}{s7}{'%.2f' % float(call.priceProc)}{s8}{'%.2f' % float(call.total_price)}{s9}{'%.2f' % float(call.total_priceProc)}{s10}{call.CALL_TYPE}{s11}{call.action}{s12}\n")
    lines.append(f"======================================================================================================================================================================\n")
    lines.append(f"                                                                                                                        Jemi:   {'%.2f' % totalSum}    {'%.2f' % totalSumProc}      ")

    response.writelines(lines)
    return response