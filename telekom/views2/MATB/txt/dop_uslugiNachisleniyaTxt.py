from django.shortcuts import redirect
from django.contrib import messages


from telekom.models import NachMinus, UserTable
from telekom.views2.myFunc.myFunc import monthСonvert


# для .txt
from django.http import HttpResponse


def dop_uslugiNachisleniyaTxt(request, year, month, etrap):
    

    if month == 'None' or year == 'None' or etrap == 'None':
        messages.error(request, f'Ошибка! Выберите месяц начисления')
        return redirect('dop-uslugi-nachisleniya') 
    
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

    month_numb = monthСonvert(month)
   
    response = HttpResponse(content_type="text/plain")
    txtName = f'{year} {month_numb} {etrap} Dop Uslugi nachisleniya'
    response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
    lines = [f"{txtName} \n\n"]

    if etrap in etraps:
        users = UserTable.objects.filter(etrap=etrap).exclude(service=None)
    elif etrap == 'all':
        users = UserTable.objects.filter().exclude(service=None)
    else:
        users = False

    nachMinus = NachMinus.objects.filter(month=month_numb, year=year)

    list_items = []
    count = 0


    if users:
        count = 0
        total_price = 0
        for user in users:
            count += 1
            services = user.service.all()
            price = 0
            service_name = []
            for service in services:
                price += service.price
                total_price += service.price
                service_name.append(service.service)
            
            s1 = (5 - len(str(count))) * ' '
            s2 = ((11 - len(user.etrap)) * ' ')
            s3 = ((15 - len(user.name)) * ' ')
            s4 = ((15 - len(user.surname)) * ' ')
            s5 = ((6 - len(str(price))) * ' ')



            lines.append(f"{count}{s1}{user.etrap}{s2}{user.number} {user.name}{s3}{user.surname}{s4}{price}{s5}{service_name}\n")

    lines.append(f"\n\n\n                                         Umumy Jemi {total_price} manat")

    response.writelines(lines)
    return response

