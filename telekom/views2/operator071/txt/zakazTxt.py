from django.http import HttpResponse
from django.db.models import Sum

from telekom.models import Zakaz


def zakazTxt(request, etrap, start, end):

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    zakazCallsList = Zakaz.objects.filter(DATE__range=[start,end], etrap=etrap)

    totalSum =  zakazCallsList.aggregate(Sum('total_price'))['total_price__sum']
    totalSumProc =  zakazCallsList.aggregate(Sum('total_priceProc'))['total_priceProc__sum']
    
    response = HttpResponse(content_type="text/plain")
    txtName = f'{etrap} Zakaz {etrap} {start}-{end}'
    response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
    lines = [f"{txtName} \n\n\n"]
    lines.append(f"№        Дата/Время        SUB_A    etrap          SUB_B       SUB_B location                   DURATION   MT  1 min   1 min    jemi    jemi   type  action\n")
    lines.append(f"                                                                                                               без %    с %     без %   с %  ")
    lines.append(f"======================================================================================================================================================================\n")

    count = 0
    for call in zakazCallsList:
        count += 1
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

    lines.append(f"\n\n                                                                                                                        Jemi:   {'%.2f' % totalSum}    {'%.2f' % totalSumProc}      ")  
    response.writelines(lines)
    return response