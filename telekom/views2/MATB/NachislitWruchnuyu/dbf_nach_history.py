# dbf_nach_history
from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from telekom.models import *
from telekom.models import dbfNameList, NonLocalCall, LocalCall
from datetime import datetime, date, timedelta
from calendar import monthrange
from collections import defaultdict


def dbf_nach_history(request):
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    months = [
        ('01', 'Январь'), ('02', 'Февраль'), ('03', 'Март'), ('04', 'Апрель'),
        ('05', 'Май'), ('06', 'Июнь'), ('07', 'Июль'), ('08', 'Август'),
        ('09', 'Сентябрь'), ('10', 'Октябрь'), ('11', 'Ноябрь'), ('12', 'Декабрь'),
    ]
    # current_date = datetime.now()
    current_date = datetime.now().date()

    if (not request.user.is_superuser and request.user.username != 'admin1') and request.user.username != 'Gayyp':
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')

 
    context = {
        'dbf_nach_history': True,
        'etraps': etraps,
        'month_choices': months,
        'current_year': current_date.year,
        'current_month': f"{current_date.month:02d}",
    }
    

    
   
    year = request.GET.get('year', '')
    month = request.GET.get('month', '')

    ic(month)
    context['selected_month'] = month
    context['selected_year'] = year

    
    
    current_year = current_date.year
    current_month = current_date.month

    try:
        selected_year = int(year) if year else current_date.year
        selected_month = int(month) if month else current_date.month
    except ValueError:
        selected_year = current_date.year
        selected_month = current_date.month

    first_day = date(selected_year, selected_month, 1)
    last_day = date(selected_year, selected_month, monthrange(selected_year, selected_month)[1])

    context['formatted_date'] = current_date.strftime('%Y-%m-%d')
    context['current_year'] = current_year
    context['current_month'] = current_month
    context['current_day'] = current_date.day


    
    
    
    locals = LocalCall.objects.filter(DATE__range=(first_day, last_day)).order_by('pk')

    names = {}
    for l in locals:
        if l.file_name not in names:
            names[l.file_name] = False
        
    
    for n in dbfNameList.objects.all():
        if n.name in names and n.is_nach:
            names[n.name] = True
            
    # ic(names)

    
   

    dict_ = {
        "kunya": [],
        "gub": [],
        # "z": [],
        "x": [],
        "uly I": [],
        "kichi i": [],
        "ha": [],
        "hu": [],
        "h": [],
        "a": [],
        "zte": [],
    }

    for name, is_nach in names.items():
        pair = [name, is_nach]
        
        if 'Kunya' in name or 'kunya' in name:
            dict_["kunya"].append(pair)
        elif 'gub' in name or 'Gub' in name:
            dict_["gub"].append(pair)
        # elif name[-1:] == 'z':
        #     dict_["z"].append(pair)
        elif name[-1:] == 'x':
            dict_["x"].append(pair)
        elif name[-1:] == 'i':
            dict_["kichi i"].append(pair)
        elif name[-1:] == 'I':
            dict_["uly I"].append(pair)
        elif name[-2:] == 'ha':
            dict_["ha"].append(pair)
        elif name[-2:] == 'hu':
            dict_["hu"].append(pair)
        elif name[-1:] == 'h':
            dict_["h"].append(pair)
        elif name[-1:] == 'a' and name[-2:] != 'ha':
            dict_["a"].append(pair)
        elif name.isdigit():
            dict_["zte"].append(pair)
        else:
            ic("nonono", name)


    ic(dict_)
    context['dict_'] = dict_
        
    
    return render(request, 'telekom/MATB/NachislitWruchnuyu/dbf_nach_history.html', context)
