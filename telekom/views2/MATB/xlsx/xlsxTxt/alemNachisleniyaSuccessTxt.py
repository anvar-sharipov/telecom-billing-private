from django.http import HttpResponse

from telekom.models import ImportAlemNachisleniyaOFF, ImportAlemNachisleniyaON, ImportInternetNachisleniyaOFF, ImportInternetNachisleniyaON, UserTable
from telekom.views2.myFunc.myFunc import getCodeEtrap, monthСonvert


def alemNachisleniyaSuccessTxt(request, year, month, etrap, off):

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
    txtName = f'{year}-{month_numb} Internet Alem Toleg BD-da  tapylan abonentlat {year}-{month_numb} {etrap}'
    response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
    lines = [f"\n\n    {txtName} \n\n"]

    totalPrice = 0
    count = 0
    lines.append(f"№    Etrap        Nomer   Familiyasy                    Ady                              Bahasy\n")
    lines.append(f"------------------------------------------------------------------------------------------------\n")
    for n in alemNachisleniya:
        try:
            user = users.get(etrap=getCodeEtrap(n.dogowor[8:11]), number=n.dogowor[11:])
            count += 1
            s1 = (5 - len(str(count))) * ' '
            s2 = (13 - len(user.etrap)) * ' '
            s3 = (30 - len(user.surname)) * ' '
            s4 = (30 - len(user.name)) * ' '
            lines.append(f"{count}{s1}{user.etrap}{s2}{user.number}   {user.surname}{s3}{user.name}{s4}   {n.price}\n")
            totalPrice += n.price
        except:
            pass 

    lines.append(f"\n\n Jemi Bahasy: {totalPrice}")

    response.writelines(lines)
    return response
