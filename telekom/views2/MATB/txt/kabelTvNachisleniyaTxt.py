from django.shortcuts import render, redirect
from django.contrib import messages


from telekom.models import NachMinus, NonLocalCall, UserTable
from telekom.views2.myFunc.myFunc import monthСonvert

from calendar import monthrange
from datetime import datetime

# для .txt
from django.http import HttpResponse

def kabelTvNachisleniyaTxt(request, year, month, etrap):


    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

    month_numb = monthСonvert(month)
   
    response = HttpResponse(content_type="text/plain")
    txtName = f'{year} {month_numb} {etrap} Kabel Tv nachisleniya'
    response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
    lines = [f"{txtName} \n\n"]

    if etrap in etraps:
        users = UserTable.objects.filter(is_on=True, kabel_count__isnull=False, etrap=etrap)
    elif etrap == 'all':
        users = UserTable.objects.filter(is_on=True, kabel_count__isnull=False)

    print(users)
    count = 0
    total_price = 0
    lines.append(f"№     Etrap        Nomer   Familiyasy                    Ady                         Edara Точек   Baha\n")
    lines.append(f"---------------------------------------------------------------------------------------------------------\n")
    for user in users:
        count += 1
        total_price += user.kabel_count.price
        s1 = (5 - len(str(count))) * ' '
        s2 = (13 - len(user.etrap)) * ' '
        s3 = (30 - len(user.surname)) * ' '
        s4 = (30 - len(user.name)) * ' '
        if user.is_enterprises:
            s5 = '+'
        else:
            s5 = ' '
        

        lines.append(f"{count}.{s1}{user.etrap}{s2}{user.number}   {user.surname}{s3}{user.name}{s4}{s5}     {user.kabel_count.kabel_count}     {user.kabel_count.price}\n")


    lines.append(f"\n\n\n                                         Umumy Jemi {total_price} manat")

    response.writelines(lines)
    return response