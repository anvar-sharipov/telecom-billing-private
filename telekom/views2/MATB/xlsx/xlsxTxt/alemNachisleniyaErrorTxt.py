from django.http import HttpResponse

from telekom.models import ImportAlemNachisleniyaOFF, ImportAlemNachisleniyaON, ImportInternetNachisleniyaOFF, ImportInternetNachisleniyaON, UserTable
from telekom.views2.myFunc.myFunc import getCodeEtrap, monthСonvert


def alemNachisleniyaErrorTxt(request, year, month, etrap, off):

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    month_numb = monthСonvert(month)

    if off == 'False':
        if etrap in etraps:
            alemNachisleniya = ImportAlemNachisleniyaON.objects.filter(month=month, year=year, etrap=etrap)
        elif etrap == 'all':
            alemNachisleniya = ImportAlemNachisleniyaON.objects.filter(month=month, year=year)

    elif off == 'True':
        if etrap in etraps:
            alemNachisleniya = ImportAlemNachisleniyaOFF.objects.filter(month=month, year=year, etrap=etrap)
        elif etrap == 'all':
            alemNachisleniya = ImportAlemNachisleniyaOFF.objects.filter(month=month, year=year)


    users = UserTable.objects.all()
    response = HttpResponse(content_type="text/plain")
    txtName = f'{year}-{month_numb} Internet Alem toleg BD-da tapylmadyk abonentlar {year}-{month_numb} {etrap}'
    response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
    lines = [f"\n\n    {txtName} \n\n"]

    totalPrice = 0
    count = 0
    lines.append(f"№      F.A.A                                             Dogowor             Login               Bahasy    Etrap\n")
    lines.append(f"--------------------------------------------------------------------------------------------------------------------\n")
    for i in alemNachisleniya:
        try:
            user = users.get(etrap=getCodeEtrap(i.dogowor[8:11]), number=i.dogowor[11:])
        except:
            count += 1
            s1 = (50 - len(i.FAO)) * ' '
            s2 = (20 - len(i.dogowor)) * ' '
            s3 = (20 - len(i.login)) * ' '
            s4 = (10 - len(str(i.price))) * ' '
            s5 = (6 - len(str(count))) * ' '
            lines.append(f"{count}.{s5}{i.FAO}{s1}{i.dogowor}{s2}{i.login}{s3}{i.price}{s4}{i.etrap}\n")
            totalPrice += i.price

    lines.append(f"\n\n                                                                                    Jemi Bahasy: {totalPrice}")

    response.writelines(lines)
    return response
