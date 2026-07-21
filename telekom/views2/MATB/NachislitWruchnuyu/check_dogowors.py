from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from datetime import datetime
from telekom.models import *
from datetime import datetime, timedelta
import calendar
import tablib
from tablib import Dataset
from django.http import HttpResponse



def check_dogowors(request):
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    wn_p = ['Dostluk Bank', 'E-government', 'Saray Tolegy', 'Tolleg APP TMCELL', 'Turkmen Pochta', 'TM POST Dealers']
    dogowors_words_list = ['DZA', 'DAD', 'DBS', 'DGD', 'DGE', 'DGO', 'DKU', 'DNZ', 'DRB', 'DTB']
    kod = {
            '344': 'Akdepe',
            '346': 'Boldumsaz',
            '340': 'Gorogly',
            '347': 'Koneurgench',
            '349': 'Turkmenbashy',
            '348': 'S.A.Nyyazow',
            '342': 'Ruhubelent',
            '322': 'Dashoguz',
        }

    request_user = request.user
    groups = request_user.groups.all()
    request_user_etrap = ''
    request_user_type = ''
    for g in groups:
        request_user_etrap, request_user_type = g.name.split('_')
        if request_user_type == 'MTB':# or request.user.username == 'admin1':
            break

    if request_user_type != 'MTB' and (not request.user.is_superuser and request.user.username != 'admin1'):
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')

    context = {}
    context['all_new_for_mtb'] = True
    context['check_dogowors'] = True
    context['etraps'] = etraps

    if request.method == 'POST':
        # Если файл не выбран то ошибка
        try:
            xlsx_data = request.FILES['xlsx_file']
            context['file_name'] = str(xlsx_data)
        except:
            messages.error(request, f'Выберите Файл')
            return render(request, 'telekom/MATB/NachislitWruchnuyu/check_dogowors.html', context)

        etrap = request.POST.get('etrap')
        context['etrap'] = etrap

        number_dogowor = {}
        users = UserTable.objects.filter(etrap=etrap)
        for u in users:
            number_dogowor[u.number] = u.dogowor

        users2 = OldLoginDogowor.objects.filter(etrap=etrap)
        number_dogowor_old = {}
        for o in users2:
            if o.number in number_dogowor_old:
                number_dogowor_old[o.number].append(o.dogowor)
            else:
                number_dogowor_old[o.number] = [o.dogowor]

        
      


        

        

        dataset = Dataset()
        xlsx_data = request.FILES['xlsx_file']
        imported_data = dataset.load(xlsx_data.read(), format='xlsx')
        
        dostluk = 0
        egov = 0
        saray = 0
        toleg = 0
        pochta = 0
        post = 0
        # # 3  - type (TOLLEG APP, seray, ...),     6 - date    10 - kod oplaty (32254356),  11- dogowor    14 - price
        error_list = []
        
        dict_ = {}
        for d in dataset:
            # kod_oplaty = str(d[10])
            dogowor = str(d[11]).upper().strip()
            for i in dogowors_words_list:
                if i in dogowor:
                    if d[10]:
                        
                        k = str(d[10]).strip()
                        if len(k) != 5:
                            for i in [' ', '.']:
                                k = k.replace(i, '') 
                            kod_oplaty = k[3:]
                            if len(kod_oplaty) != 5:
                                error_list.append([d[10], d[11], d[12], d[14], '', '', 'abonentyn nomeri excelde nadogry'])
                                continue

                        else:
                            kod_oplaty = k


                        
                        if kod_oplaty in number_dogowor or kod_oplaty in number_dogowor_old:
                            error1 = False
                            error2 = False

                            if kod_oplaty in number_dogowor:
                                if number_dogowor[kod_oplaty] == dogowor:
                                    continue
                            if kod_oplaty in number_dogowor_old:
                                if dogowor in number_dogowor_old[kod_oplaty]:
                                    continue

                            try:
                                u = UserTable.objects.get(etrap=etrap, number=kod_oplaty)
                                bd_log_dog = f'{u.dogowor} {u.login}'
                            except:
                                bd_log_dog = ''
                 
                            u = OldLoginDogowor.objects.filter(etrap=etrap, number=kod_oplaty)
                            bd_log_dog_old = []
                            for i in u:
                                bd_log_dog_old.append(f'{i.dogowor} {i.login}')
                        
                            error_list.append([d[10], d[11], d[12], d[14], bd_log_dog, bd_log_dog_old, 'Lan billindaki Dogowor PyView bilen dogry gelenak'])
                            continue
                        else:
                            error_list.append([d[10], d[11], d[12], d[14], '', '', 'abonentyn nomeri excelde nadogry'])
                            continue
                    else:
                        pass
                        # error_list.append([d[10], d[11], d[12], d[14], '', '', 'nomeri excelde yok shon uchin barlagdan gechirip bolanok, yalnysh dal yone bir barlap gormeli'])
                        # continue

        headers = ("Код оплаты (Lan Billing)", "№ договора (Lan Billing)", "Наименование абонента (Lan Billing)", "Сумма платежа (Lan Billing)", "bazadaky login dogowor (PyView)", "oldaky login dogowor (PyView)", "yalnyshyk sebabi")
        data = []
        data = tablib.Dataset(*data, headers=headers)
    
        
        if error_list:
            for v in error_list:
                ic(v)
                data.append((v[0], v[1], v[2], v[3], v[4], v[5], v[6]))

            response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
            response['Content-Disposition'] = f"attachment; filename= error_dogowors_{etrap}.xlsx"
            return response 



    return render(request, 'telekom/MATB/NachislitWruchnuyu/check_dogowors.html', context)