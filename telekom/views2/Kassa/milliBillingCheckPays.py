from django.shortcuts import render, redirect
from django.contrib import messages
from datetime import datetime, timedelta
import calendar
import tablib
import urllib.parse

from telekom.models import PayHistory, KabelTvPayHistory, CheckMilliBillingPaysWithKassirs, OldLoginDogowor
from django.http import HttpResponse
from django.db import transaction

import logging
logger = logging.getLogger(__name__)


ETRAPS = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']


def build_summary(etrap, date_from, date_to, options):
    """Считает сводку по платежам Milli Billing (только те, что помечены milli_billing_file_name)
    за период для этрапа, сгруппированную по кассирам, плюс статус сверки/закрытия по дням."""

    start_date = datetime.strptime(date_from, '%Y-%m-%d')
    end_date = datetime.strptime(date_to, '%Y-%m-%d')
    date_list = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]

    mojno_nachislyat = start_date.year == end_date.year and start_date.month == end_date.month

    closed_days_dict = {}
    for d in date_list:
        for obj in CheckMilliBillingPaysWithKassirs.objects.filter(checked_date=d, etrap=etrap, day_is_closed=True):
            closed_days_dict[d] = obj.who_close_the_day
    opened_days_list = [d for d in date_list if d not in closed_days_dict]

    if options == 'po_kassiram':
        pays = PayHistory.objects.filter(kassir_etrap=etrap, milli_billing_file_name__isnull=False, date__range=[date_from, f"{date_to} 23:59:59"])
    else:
        pays = PayHistory.objects.filter(abonent__etrap=etrap, milli_billing_file_name__isnull=False, date__range=[date_from, f"{date_to} 23:59:59"])

    pays_k = KabelTvPayHistory.objects.filter(milli_billing_file_name__isnull=False, pay_date__range=[date_from, f"{date_to} 23:59:59"]) if etrap == 'Dashoguz' else KabelTvPayHistory.objects.none()

    dict_ = {}
    total = {'telefoniya': 0, 'internet': 0, 'alem': 0, 'kabel': 0, 'umumy': 0}
    managers_list = []
    managers_list_dict = {}

    for p in pays:
        pay_date = p.date.strftime('%Y-%m-%d')
        managers_list_dict.setdefault(pay_date, [])
        if p.kassir not in managers_list_dict[pay_date]:
            managers_list_dict[pay_date].append(p.kassir)
        if p.kassir not in managers_list:
            managers_list.append(p.kassir)

        telefoniya, internet, alem = p.prochee, p.internet, p.alem
        row = dict_.setdefault(p.kassir, {'telefoniya': 0, 'internet': 0, 'kabel': 0, 'alem': 0, 'total_kassir': 0})
        row['telefoniya'] += telefoniya
        row['internet'] += internet
        row['alem'] += alem
        row['total_kassir'] += telefoniya + internet + alem

        total['telefoniya'] += telefoniya
        total['internet'] += internet
        total['alem'] += alem
        total['umumy'] += telefoniya + internet + alem

    for p in pays_k:
        pay_date = p.pay_date.strftime('%Y-%m-%d')
        managers_list_dict.setdefault(pay_date, [])
        if p.pay_kassir not in managers_list_dict[pay_date]:
            managers_list_dict[pay_date].append(p.pay_kassir)
        if p.pay_kassir not in managers_list:
            managers_list.append(p.pay_kassir)

        row = dict_.setdefault(p.pay_kassir, {'telefoniya': 0, 'internet': 0, 'kabel': 0, 'alem': 0, 'total_kassir': 0})
        row['kabel'] += p.pay
        row['total_kassir'] += p.pay

        total['kabel'] += p.pay
        total['umumy'] += p.pay

    cheked_days = []
    dont_cheked_days = []
    dont_cheked_days_dict = {}
    pks_checked_days = []
    dont_checked_managers_name = []
    day_is_closed = False

    for day_ in date_list:
        for m in managers_list:
            obj = CheckMilliBillingPaysWithKassirs.objects.filter(checked_date=day_, etrap=etrap, checked_kassir=m).first()
            if obj:
                if len(date_list) == 1 and obj.day_is_closed:
                    day_is_closed = True
                pks_checked_days.append(obj.pk)
                cheked_days.append(day_)
            else:
                dont_cheked_days.append(day_)
                if m in managers_list_dict.get(day_, []):
                    dont_cheked_days_dict.setdefault(day_, {'managers_dict': []})
                    dont_cheked_days_dict[day_]['managers_dict'].append(m)
                dont_checked_managers_name.append(m)

    return {
        'date_list': date_list,
        'len_date_list': len(date_list),
        'num_days': calendar.monthrange(start_date.year, start_date.month)[1],
        'mojno_nachislyat': mojno_nachislyat,
        'closed_days_dict': closed_days_dict,
        'opened_days_list': opened_days_list,
        'dict_': dict_,
        'total': total,
        'managers_list': managers_list,
        'cheked_days': cheked_days,
        'dont_cheked_days': dont_cheked_days,
        'dont_cheked_days_dict': dont_cheked_days_dict,
        'dont_checked_managers_name': dont_checked_managers_name,
        'day_is_closed': day_is_closed,
        'check_pays_obj': CheckMilliBillingPaysWithKassirs.objects.filter(pk__in=pks_checked_days) if pks_checked_days else False,
        '_pays': pays,
        '_pays_k': pays_k,
    }


def milliBillingCheckPays(request):
    request_user = request.user
    groups = request_user.groups.all()
    request_user_etrap = ''
    request_user_type = ''
    for g in groups:
        request_user_etrap, request_user_type = g.name.split('_')
        if request_user_type == 'MTB' or (request_user_type == 'SHB' and request.user.username == 'lenashb'):
            break

    if request_user_type == 'SHB' and request.user.username != 'lenashb':
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')

    if request_user_type != 'MTB' and request_user_type != 'SHB' and (not request.user.is_superuser and request.user.username != 'admin1'):
        messages.error(request, 'Не достаточно прав')
        return redirect('HomePage')

    context = {}
    context['milliBillingCheckPays'] = True
    if request_user_type == 'MTB':
        context['matbIndex'] = True
    if request_user_type == 'SHB':
        context['SHBIndex'] = True
    context['request_user_etrap'] = request_user_etrap
    context['etraps'] = ETRAPS

    today_str = datetime.now().strftime('%Y-%m-%d')
    etrap = request.GET.get('etrap')
    date_from = request.GET.get('date_from') or today_str
    date_to = request.GET.get('date_to') or today_str
    options = request.GET.get('options') or 'po_kassiram'
    context['options'] = options
    context['etrap'] = etrap
    context['date_from'] = date_from
    context['date_to'] = date_to

    if etrap in ETRAPS:
        allow = request.user.is_superuser or request.user.username in ['admin1', 'Gayyp'] or etrap == request_user_etrap
        if not allow:
            messages.error(request, "Выберите этрап с своего этрапа")
            return render(request, 'telekom/Kassa/milliBillingCheckPays.html', context)

    if request.user.username in ['intizar_gorogly', 'lenashb', 'testMTBDZ', 'AyshatGoroglyMtb', 'GuljahanAkdepeMtb', 'AzizShabatMtb', 'Saryyewa_Gozel_Shabat_MTB', 'BaharKoneurgenchKassa', 'Merjen_Yylally_MTB', 'GozelGubadagMtb', 'SelbiBoldumsazMtb', 'MahymAkdepeMtb', 'Aramedowa_Oguljemal', 'Kurbanowa_Gulnabat_Koneurgench', 'Baltabayewa_Sewara_MTB_DGE', 'Ishangulyyewa_Nurjemal_Koneurgench_kassa'] or (request.user.is_superuser and request.user.username == 'admin1'):
        context['allow_podtwerdit'] = True

    if not (etrap and date_from and date_to):
        return render(request, 'telekom/Kassa/milliBillingCheckPays.html', context)

    summary = build_summary(etrap, date_from, date_to, options)
    context['dontScroll'] = False
    context.update({k: v for k, v in summary.items() if not k.startswith('_')})

    # Подтвердить (сверить) кассира за 1 день
    if request.method == 'POST' and 'check_button' in request.POST:
        comment = request.POST.get('comment')
        kassir = request.POST.get('kassir')
        context['dontScroll'] = True
        if not comment:
            messages.error(request, "Оставьте комментарий")
        elif options != 'po_kassiram':
            messages.error(request, "Вы можете подтвердить только проверив по кассирам")
        elif not summary['mojno_nachislyat']:
            messages.error(request, "Вы можете подтвердить только 1 день")
        else:
            try:
                with transaction.atomic():
                    for d in summary['date_list']:
                        if not CheckMilliBillingPaysWithKassirs.objects.filter(checked_date=d, etrap=etrap, checked_kassir=kassir).exists():
                            row = summary['dict_'].get(kassir, {'telefoniya': 0, 'internet': 0, 'alem': 0, 'kabel': 0, 'total_kassir': 0})
                            CheckMilliBillingPaysWithKassirs.objects.create(
                                etrap=etrap,
                                checked_date=d,
                                checked_kassir=kassir,
                                operator=request.user.username,
                                comment=comment,
                                total_telefon=row['telefoniya'],
                                total_alem=row['alem'],
                                total_internet=row['internet'],
                                total_kabel=row['kabel'],
                                itogo_kassir=row['total_kassir'],
                            )
                messages.success(request, f"Подтверждено {summary['date_list'][0]}")
            except Exception as e:
                logger.warning(f"Не удалось подтвердить: {e}")
                messages.error(request, f'Не удалось подтвердить по причине {e}')

        summary = build_summary(etrap, date_from, date_to, options)
        context.update({k: v for k, v in summary.items() if not k.startswith('_')})

    # Закрыть день
    if request.method == 'POST' and 'close_day' in request.POST:
        checked_objs = summary['check_pays_obj']
        count_dates = list({i.checked_date for i in checked_objs}) if checked_objs else []
        if len(count_dates) != 1:
            messages.error(request, 'Выберите только 1 день')
        else:
            try:
                with transaction.atomic():
                    for i in checked_objs:
                        i.day_is_closed = True
                        i.who_close_the_day = request.user.username
                        i.total_telefon_when_closed_day = summary['total']['telefoniya']
                        i.total_alem_when_closed_day = summary['total']['alem']
                        i.total_internet_when_closed_day = summary['total']['internet']
                        i.total_kabel_when_closed_day = summary['total']['kabel']
                        i.itogo_when_closed_day = summary['total']['umumy']
                        i.save()
                messages.success(request, 'Успешное закрытие дня')
            except Exception as e:
                logger.warning(f"Не удалось закрыть день: {e}")
                messages.error(request, f'Не удалось закрыть день по причине {e}')

        summary = build_summary(etrap, date_from, date_to, options)
        context.update({k: v for k, v in summary.items() if not k.startswith('_')})

    # Скачать платежи кассира в excel
    if request.method == 'POST' and 'download_pays' in request.POST:
        manager = request.POST.get('manager')
        filtered_pays = summary['_pays'].filter(kassir=manager)

        headers = ("number", "dogowors", "telefoniya", "internet", "alem", "kabel", "kassir", "date", "is_card")
        data = tablib.Dataset(headers=headers)

        for i in filtered_pays:
            dogowors = i.abonent.dogowor or ''
            old_dogowors = OldLoginDogowor.objects.filter(etrap=etrap, number=i.abonent.number)
            for d in old_dogowors:
                dogowors += f" {d.dogowor}"

            telefoniya = i.telefon + i.slr + i.kod + i.zakaz + i.dop_uslugi + i.prochee
            is_card = 'cart' if i.is_card else ''
            data.append((i.abonent.number, dogowors, telefoniya, i.internet, i.alem, 0, i.kassir, i.date, is_card))

        if etrap == 'Dashoguz':
            for i in summary['_pays_k'].filter(pay_kassir=manager):
                is_card = 'cart' if i.card else ''
                data.append((i.user.number, '', 0, 0, 0, i.pay, i.pay_kassir, i.pay_date, is_card))

        filename = f"milli_billing_tolegler_{manager}_{date_from}__{date_to}_{etrap}.xlsx"
        encoded_filename = urllib.parse.quote(filename.encode('utf-8'))

        response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel;charset=utf-8')
        response['Content-Disposition'] = f"attachment; filename= {encoded_filename}"
        return response

    return render(request, 'telekom/Kassa/milliBillingCheckPays.html', context)
