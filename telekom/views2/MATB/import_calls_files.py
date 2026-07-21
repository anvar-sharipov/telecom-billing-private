from django.shortcuts import render, redirect
from django.contrib import messages
from telekom.views2.myFunc.sort_number_to_ilat_bud_hoz_empty_and_unknown import sort_number_to_ilat_bud_hoz_empty_and_unknown
from telekom.views2.myFunc.variables_for_dbf import mugut, etraps, turkmenistan, international, add_secs_to_time, check_a_file_has_been_added
from telekom.views2.myFunc.getNumberLocations import getNumberLocations

from dbfread import DBF
import datetime
import sqlite3

import sys
import os
def bell():
    sys.stdout.write('\r\a')
    sys.stdout.flush()


def import_calls_files(request):
    context = {}
    if request.user.is_authenticated:
        if request.user.is_superuser:
            log = 'Dashoguz'
            context['matbIndex'] = True
            context['import_calls_files'] = True   
        else:
            messages.error(request, f'У вас нет доступа, там очень секретная информация)')
            return redirect('user-login')
    else:
        messages.error(request, f'Вы не аутентифицированы')
        return redirect('user-login')
    

    if request.method == 'POST' and 'dbf_a' in request.POST:
        
        my_dict = sort_number_to_ilat_bud_hoz_empty_and_unknown('Dashoguz')
        hozUsers = my_dict['hozUsers']
        budUsers = my_dict['budUsers']
        UnknowEdaraUsers = my_dict['UnknowEdaraUsers']
        emptyNumberUsers = my_dict['emptyNumberUsers']

        file_names = os.listdir(r"C:\\Users\\Home\Desktop\dbf_a_file_DZ")
        for index in range(len(file_names)):
            file_names[index] = f"{file_names[index][:-4]}"

        
        if request.POST.get('dbf_a_check_input'):
            # Добавление
            print('add')
            pass
        else:
            # проверка
            print('check')
            for file_ in file_names:
                print('file_', file_)
                error_name_list = []
                if file_[-1] != 'a':
                    error_name_list.append(file_)
                    # messages.error(request, f"У вас файл {file_} не является a файлом")

                # Проверка не был ли начислен этот файл
                already_added = check_a_file_has_been_added(file_)
                already_added_list = []
                if already_added:
                    already_added_list.append(file_)
                    
                
            if already_added_list:
                print('already_added_list', already_added_list)
                messages.error(request, f"файл {file_} уже был добавлен в БД")
                return render(request, 'telekom/MATB/import_calls_files.html', context)
            # for file_ in file_names:
            #     dbf = DBF(file_ + '.dbf')

                
                    

        

        
            
    return render(request, 'telekom/MATB/import_calls_files.html', context)


# hozUsers, budUsers, UnknowEdaraUsers, emptyNumberUsers 
# hozUsersBoldumsaz, budUsersBoldumsaz, UnknowEdaraUsersBoldumsaz, emptyNumberUsersBoldumsaz 
# hozUsersTurkmenbashy, budUsersTurkmenbashy, UnknowEdaraUsersTurkmenbashy, emptyNumberUsersTurkmenbashy
# hozUsersGorogly, budUsersGorogly, UnknowEdaraUsersGorogly, emptyNumberUsersGorogly
# hozUsersKoneurgench, budUsersKoneurgench, UnknowEdaraUsersKoneurgench, emptyNumberUsersKoneurgench
# hozUsersRuhubelent, budUsersRuhubelent, UnknowEdaraUsersRuhubelent, emptyNumberUsersRuhubelent
# hozUsersAkdepe, budUsersAkdepe, UnknowEdaraUsersAkdepe, emptyNumberUsersAkdepe
# hozUsersNyyazow, budUsersNyyazow, UnknowEdaraUsersNyyazow, emptyNumberUsersNyyazow