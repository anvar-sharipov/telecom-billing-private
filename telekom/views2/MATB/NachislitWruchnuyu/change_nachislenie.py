from django.shortcuts import render, redirect
from django.contrib import messages
from icecream import ic
from datetime import datetime
from telekom.models import *
from telekom.views2.myFunc.myFunc import monthСonvert

from django.db import transaction
import logging
logger = logging.getLogger(__name__)




def change_nachislenie(request):
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench','Garashsyzlyk', 'Gubadag' ]

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

    context['etraps'] = etraps

    current_date = datetime.now().date()
    formatted_date = current_date.strftime('%Y-%m-%d')
    current_year, current_month, current_day = formatted_date.split('-')

    context['formatted_date'] = formatted_date
    context['current_year'] = current_year
    context['current_month'] = current_month
    context['current_day'] = current_day

    
    context['change_nachislenie'] = True
    if request_user_type == 'MTB':
        context['matbIndex'] = True 
        context['request_user_etrap'] = request_user_etrap 

    etrap = request.GET.get('etrap')
    number = request.GET.get('number')
    year = request.GET.get('year')
    month_digit = request.GET.get('month')
    month_word = monthСonvert(month_digit)
    context['number'] = number
    context['etrap'] = etrap
    context['year'] = year
    context['month_digit'] = month_digit
    context['month_word'] = month_word

    ic(etrap, number, year, month_digit)

    if etrap in etraps and number and year and month_digit:

        allow = False
        if not request.user.is_superuser and request.user.username != 'admin1' and request.user.username != "Gayyp":
            if etrap == request_user_etrap:
                allow = True
        else:
            allow = True

        if not allow:
            messages.error(request, f"Выберите абонента с своего этрапа")
            return render(request, 'telekom/MATB/NachislitWruchnuyu/change_nachislenie.html', context)


        if len(number) < 5 or len(number) > 6:
            messages.error(request, f'Введите корректный номер')
        else:
            if len(number) > 5:
                context['only_kabel'] = True
            else:
                context['only_kabel'] = False
            if len(number) == 5:
                try:
                    user_table = UserTable.objects.get(number=number, etrap=etrap)
                    context['user_table'] = user_table
                  
                    user_table_nach = NachMinus.objects.filter(year=year, month=month_digit, user=user_table)
                    if len(user_table_nach) > 1:
                        messages.error(request, 'Больше двух начислений в NachMinus')
                        return render(request, 'telekom/MATB/NachislitWruchnuyu/change_nachislenie.html', context)
                    context['user_table_nach'] = user_table_nach
               
                except:
                    messages.error(request, 'Абонент не найден')
            if etrap == 'Dashoguz':
                try:
                    user_kabel = KabelTvNew.objects.get(number=number)
                    user_kabel_nach = KabelNach.objects.filter(year=year, month=month_digit, user=user_kabel)
                    
                    if len(user_kabel_nach) > 1:
                        messages.error(request, 'Больше двух начислений в KabelNach')
                        return render(request, 'telekom/MATB/NachislitWruchnuyu/change_nachislenie.html', context)
                    ic(user_kabel_nach)
                    context['user_kabel_nach'] = user_kabel_nach
                except:
                    user_kabel = False
                context['user_kabel'] = user_kabel

        if request.method == 'POST':

            telefon = float(request.POST.get('telefon')) if request.POST.get('telefon') != None else None
            slr = float(request.POST.get('slr')) if request.POST.get('slr') != None else None
            kod = float(request.POST.get('kod')) if request.POST.get('kod') != None else None
            zakaz = float(request.POST.get('zakaz')) if request.POST.get('zakaz') != None else None
            prochee = float(request.POST.get('prochee')) if request.POST.get('prochee') != None else None
            dop_uslugi = float(request.POST.get('dop_uslugi')) if request.POST.get('dop_uslugi') != None else None
            internet = float(request.POST.get('internet')) if request.POST.get('internet') != None else None
            alem = float(request.POST.get('alem')) if request.POST.get('alem') != None else None
            kabel = float(request.POST.get('kabel')) if request.POST.get('kabel') != None else None
            comment = request.POST.get('comment')
            ic(telefon, slr, kod, zakaz, prochee, dop_uslugi, internet, alem, kabel, comment)
            if len(comment) < 1:
                messages.error(request, 'Оставьте комментарий')
                return render(request, 'telekom/MATB/NachislitWruchnuyu/change_nachislenie.html', context)

            mes = ''
            have_a_save_kabel = False
            have_a_save_user = False
            nach_comment = NachWithComment(etrap=etrap, number=number, operator=request.user.username)
            if kabel != None:
                if user_kabel_nach:
                    if len(user_kabel_nach) > 1:
                        messages.error(request, 'Больше двух начислений в KabelNach')
                        return render(request, 'telekom/MATB/NachislitWruchnuyu/change_nachislenie.html', context)
                    for n in user_kabel_nach:
                        obj_kabel_nach = KabelNach.objects.get(pk=n.pk)
                    n_kabel = obj_kabel_nach.nach
                    if n_kabel != kabel:
                        user_kabel.balance = user_kabel.balance + n_kabel - kabel
                        obj_kabel_nach.nach = kabel
                        mes += f'Начисления на Кабельное за {month_word} {year} года\nНачислено {kabel}, а до этого было {n_kabel}\n\n'
                        nach_comment.kabel = kabel
                        have_a_save_kabel = True
                else:
                    if kabel != 0:
                        obj_kabel_nach = KabelNach(user=user_kabel, year=year, month=month_digit, nach=kabel)
                        user_kabel.balance -= kabel
                        mes += f'Начисления на Кабельное за {month_word} {year} года\nНачислено {kabel}, а до этого начислений небыло\n\n'
                        nach_comment.kabel = kabel
                        have_a_save_kabel = True

            if telefon != None or slr != None or kod != None or zakaz != None or prochee != None or dop_uslugi != None or internet != None or alem != None:
                if user_table_nach:
                    if len(user_table_nach) > 1:
                        messages.error(request, 'Больше двух начислений в KabelNach')
                        return render(request, 'telekom/MATB/NachislitWruchnuyu/change_nachislenie.html', context)
                    for n in user_table_nach:
                        obj_user_nach = NachMinus.objects.get(pk=n.pk)
                    n_telefon = obj_user_nach.telefon
                    n_slr = obj_user_nach.slr
                    n_kod = obj_user_nach.kod
                    n_zakaz = obj_user_nach.zakaz
                    n_prochee = obj_user_nach.prochee
                    n_dop_uslugi = obj_user_nach.dop_uslugi
                    n_internet = obj_user_nach.internet
                    n_alem = obj_user_nach.alem

                    if n_telefon != telefon:
                        user_table.b_telefon = user_table.b_telefon + n_telefon - telefon
                        obj_user_nach.telefon = telefon
                        mes += f'Начисления на telefon за {month_word} {year} года\nНачислено {telefon}, а до этого было {n_telefon}\n\n'
                        nach_comment.telefon = telefon
                        have_a_save_user = True
                    
                    if n_slr != slr:
                        user_table.b_slr = user_table.b_slr + n_slr - slr
                        obj_user_nach.slr = slr
                        mes += f'Начисления на Slr за {month_word} {year} года\nНачислено {slr}, а до этого было {n_slr}\n\n'
                        nach_comment.slr = slr
                        have_a_save_user = True

                    if n_kod != kod:
                        user_table.b_kod = user_table.b_kod + n_kod - kod
                        obj_user_nach.kod = kod
                        mes += f'Начисления на kod за {month_word} {year} года\nНачислено {kod}, а до этого было {n_kod}\n\n'
                        nach_comment.kod = kod
                        have_a_save_user = True

                    if n_zakaz != zakaz:
                        user_table.b_zakaz = user_table.b_zakaz + n_zakaz - zakaz
                        obj_user_nach.zakaz = zakaz
                        mes += f'Начисления на zakaz за {month_word} {year} года\nНачислено {zakaz}, а до этого было {n_zakaz}\n\n'
                        nach_comment.zakaz = zakaz
                        have_a_save_user = True

                    if n_prochee != prochee:
                        user_table.b_prochee = user_table.b_prochee + n_prochee - prochee
                        obj_user_nach.prochee = prochee
                        mes += f'Начисления на prochee за {month_word} {year} года\nНачислено {prochee}, а до этого было {n_prochee}\n\n'
                        nach_comment.prochee = prochee
                        have_a_save_user = True

                    if n_dop_uslugi != dop_uslugi:
                        user_table.b_dop_uslugi = user_table.b_dop_uslugi + n_dop_uslugi - dop_uslugi
                        obj_user_nach.dop_uslugi = dop_uslugi
                        mes += f'Начисления на dop_uslugi за {month_word} {year} года\nНачислено {dop_uslugi}, а до этого было {n_dop_uslugi}\n\n'
                        nach_comment.dop_uslugi = dop_uslugi
                        have_a_save_user = True


                    if n_internet != internet:
                        user_table.b_internet = user_table.b_internet + n_internet - internet
                        obj_user_nach.internet = internet
                        mes += f'Начисления на internet за {month_word} {year} года\nНачислено {internet}, а до этого было {n_internet}\n\n'
                        nach_comment.internet = internet
                        have_a_save_user = True

                    if n_alem != alem:
                        user_table.b_alem = user_table.b_alem + n_alem - alem
                        obj_user_nach.alem = alem
                        mes += f'Начисления на alem за {month_word} {year} года\nНачислено {alem}, а до этого было {n_alem}\n\n'
                        nach_comment.alem = alem
                        have_a_save_user = True
                else:
                    obj_user_nach = NachMinus(user=user_table, year=year, month=month_digit)
                    if telefon != 0:
                        user_table.b_telefon -= telefon
                        obj_user_nach.telefon = telefon
                        mes += f'Начисления на telefon за {month_word} {year} года\nНачислено {telefon}, а до этого начислений небыло\n\n'
                        nach_comment.telefon = telefon
                        have_a_save_user = True
                    if slr != 0:
                        user_table.b_slr -= slr
                        obj_user_nach.slr = slr
                        mes += f'Начисления на slr за {month_word} {year} года\nНачислено {slr}, а до этого начислений небыло\n\n'
                        nach_comment.slr = slr
                        have_a_save_user = True
                    if kod != 0:
                        user_table.b_kod -= kod
                        obj_user_nach.kod = kod
                        mes += f'Начисления на kod за {month_word} {year} года\nНачислено {kod}, а до этого начислений небыло\n\n'
                        nach_comment.kod = kod
                        have_a_save_user = True
                    if zakaz != 0:
                        user_table.b_zakaz -= zakaz
                        obj_user_nach.zakaz = zakaz
                        mes += f'Начисления на zakaz за {month_word} {year} года\nНачислено {zakaz}, а до этого начислений небыло\n\n'
                        nach_comment.zakaz = zakaz
                        have_a_save_user = True
                    if prochee != 0:
                        user_table.b_prochee -= prochee
                        obj_user_nach.prochee = prochee
                        mes += f'Начисления на prochee за {month_word} {year} года\nНачислено {prochee}, а до этого начислений небыло\n\n'
                        nach_comment.prochee = prochee
                        have_a_save_user = True
                    if dop_uslugi != 0:
                        user_table.b_dop_uslugi -= dop_uslugi
                        obj_user_nach.dop_uslugi = dop_uslugi
                        mes += f'Начисления на dop_uslugi за {month_word} {year} года\nНачислено {dop_uslugi}, а до этого начислений небыло\n\n'
                        nach_comment.dop_uslugi = dop_uslugi
                        have_a_save_user = True
                    if internet != 0:
                        user_table.b_internet -= internet
                        obj_user_nach.internet = internet
                        mes += f'Начисления на internet за {month_word} {year} года\nНачислено {internet}, а до этого начислений небыло\n\n'
                        nach_comment.internet = internet
                        have_a_save_user = True
                    if alem != 0:
                        user_table.b_alem -= alem
                        obj_user_nach.alem = alem
                        mes += f'Начисления на alem за {month_word} {year} года\nНачислено {alem}, а до этого начислений небыло\n\n'
                        nach_comment.alem = alem
                        have_a_save_user = True
            
            if have_a_save_user or have_a_save_kabel:

                mes += f'Комментарий: {comment}'
                
                nach_comment.comment = mes
                nach_comment.year = year
                nach_comment.month = month_digit

                try: 
                    with transaction.atomic():
                        if have_a_save_user:
                            user_table.save()
                            obj_user_nach.save()
                            context['user_table_nach'] = NachMinus.objects.filter(year=year, month=month_digit, user=user_table)
                        if have_a_save_kabel:
                            user_kabel.save()
                            obj_kabel_nach.save()
                            context['user_kabel_nach'] = KabelNach.objects.filter(year=year, month=month_digit, user=user_kabel)
                        nach_comment.save()
                        messages.success(request, f'Успешное изменение начислений')
                except Exception as e:
                    messages.error(request, f'откат записей, ошибка в {str(e)}')
                    logger.warning(f"откат записей, ошибка в {str(e)}")
                    return render(request, 'telekom/MATB/NachislitWruchnuyu/change_nachislenie.html', context)
            else:
                messages.error(request, f'Нет изменений')



    return render(request, 'telekom/MATB/NachislitWruchnuyu/change_nachislenie.html', context)