from django.shortcuts import render, redirect
from telekom.models import Zakaz
from django.db.models import Sum, F, Q
from django.db.models.functions import Cast
from django.db.models import DecimalField
from django.db.models.expressions import RawSQL

from django.contrib import messages

from telekom.views2.myFunc.myFunc import loggedUserEtrapAndGroup

from datetime import date
import re







def zakazCalls(request):
    
    EtrapAndGroup = loggedUserEtrapAndGroup(request.user)
    if EtrapAndGroup[1] == '071' or request.user.is_superuser and request.user.username != 'Kabayew':
        log = EtrapAndGroup[0]
    else:
        messages.error(request, f'Доступ только соотрудникам 071')
        return redirect('user-login')
    
    context = {}
    current_date = str(date.today())
    # context['current_date'] = current_date
    # current_year = current_date[0:4]
    # current_month = current_date[5:7]
    # current_day = current_date[8:]
    # days_in_month = monthrange(int(current_date[0:4]), int(current_date[5:7]))[1]
    
    # log = getLoggedUserEtrap(request.user.username)

    context['log'] = log
    context['operator071'] = True
    context['zakazCalls'] = True
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
	
    turkmenistan = ['Sotowyy',
			'Ashgabat','Ahal Baharly','Ahal Gokdepe','Ahal Kaka','Ahal Seraks','Ahal Tejen','Ahal Babadayhan','Ahal Anew','Ahal Abadan','Ahal Ruhabat','Ahal Ashgabat',
			'Balkan Nebitdag','Balkan Hazar','Balkan Gumdag','Balkan Gyzyl Atr','Balkan Turkmenbashy','Balkan Gumdag','Balkan Esenguly','Balkan Serdar','Balkan Bereket','Balkan Magtymguly',
			'Lebap Turkmenabat','Lebap Magdanly','Lebap Garashsyzlyk','Lebap Gazajak','Lebap Koytendag','Lebap Halach','Lebap Hojambaz','Lebap Garabekewul','Lebap Atamyrat','Lebap Birata',
			'Lebap Galkynysh','Lebap Sayat','Lebap Farap', 'Lebap Sakar','Lebap Seydi','Lebap Turkmenbashy','Lebap Serdarabat','Lebap Serdarabat',
			'Mary','Mary Garagum','Mary Wekilbazar','Mary Oguzhan','Mary Yoleten','Mary Serhetabat','Mary Bayramaly','Mary Murgap','Mary Sakarchage','Mary Tagtabazar','Mary Turkm-gala']

    international = ['Moldowa','Fransiya','Germaniya','Gresiya','Wengriya','Italiya','Niderlandy','Norwegiya','Polsha','Rumyniya','Shwesiya','Shweysariya','Welikobritaniya','Ispaniya','Albaniya','Andorra','Bosniya Gersogowina','Bolgariya','Horwatiya','Kipr',
			'Estoniya','Finlyandiya','Gibraltar','Grenlandiya','Islandiya','Latwiya','Lihtenshteyn','Litwa','Luksenburg','Makedoniya','Malta','Portugaliya','Slowakiya','Sloweniya','Yugoslawiya','Cheshskaya Respublika',
			'Kazakstan','Rossiya','Kyrgystan','Tajikistan','Uzbekistan','Belorussiya','Armeniya','Azerbayjan','Gruziya','Ukraina','Afganistan','Turkiya','Iran','Awstriya','Belgiya','Daniya',
			'Awstraliya','Nowaya Zenlandiya','Fidji','Fransuskaya Polineziya','Kiribati','Nowaya Kaledoniya','Norfolkskiye ostrowa','Papua Nowaya Gwineya','Tonga','Wanuatu','Hytay','Kuba','Indiya','Indoneziya','Yaponiya','Malaziya','Meksika','Myanma',
			'Pakistan','Filipiny','Singapur','Yujnaya Koreya','Tailand','Wyetnam','Bahreyn','Bangladesh','Bruney Daruesaalam','Kombodja','Kosta-Rika','Wostochnyy Timor','Gwatelama','Gaiti','Gonduras','Gonk-Kong','Irak','Izrail','Iordaniya','Kuweit','Laos','Liwan',
			'Makao (Aomyn)','Mongoliya','Nepal','Niderlandskie Antilly','Nikaragua','Sewernaya Koreya','Sewernyy Yemen','Oman','Panama' 'Katar','Saudowskaya Arawiya','Yujnyy Yemen','Siriya','Taiwan','O.A.E','USA/CANADA','Argentina','Braziliya','Chili',
			'Kolumbiya','Peru','Wenesuella','Boliwiya','Ekwador','Farerskie Ostrowa','Fransuskatya Gwiana','Gayana','Martitnka','Surinam','Urugway','Egipet','UAR','Aljir','Angola','Benin','Botswana','Burkina Faso','Burundi','Kamerun',
			'Kape Werde','SAR','Chad','Kongo','Jibuti','Ekwatorialnaya gwineya','Efiopiya','Gabon','Gambiya','Gana','Gwineya','Gwineya Bissau','Keniya','Liberiya','Liviya','Madagaskar','Malawi','Mali','Mawritaniya','Mawrikiy',
			'Moroko','Mozambik','Namibiya','Niger','Nigeriya','Reonyon','Respublika Ruanda','Senegal','Seyshelskie ostrowa','Syerra Leonne','Somali','Sudan','Tanzaniya','Respublika Togoleze','Tunis','Uganda','Zair','Zambiya','Zimbabwe']

    allContries = sorted(turkmenistan + international)
    context['allContries'] = allContries
    context['etraps'] = etraps
    context['etrap'] = request.GET.get('etrap') if request.GET.get('etrap') in etraps else ''

    start = f"{request.GET.get('start')} 00:00:00" if request.GET.get('start') != None else f"{current_date} 00:00:00"
    end = f"{request.GET.get('end')} 23:59:59" if request.GET.get('end') != None else f"{current_date} 23:59:59"

    context['start'] = request.GET.get('start') if request.GET.get('start') != None else current_date
    context['end'] = request.GET.get('end') if request.GET.get('end') != None else current_date

    if log in etraps:
        etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else log
    else:
        etrap = request.GET.get('etrap') if request.GET.get('etrap') != None else ''

    actions = ['повторно', 'бно', 'заказ подтвержден']
    context['actions'] = actions

    ZakazCallsList = Zakaz.objects.filter(DATE__range=[start,end], etrap=etrap)

    context['ZakazCalls'] = ZakazCallsList
    # context['lenZakazCalls'] = len(ZakazCallsList)

    # returns {'price__sum': 1000} for example

    # context['totalSum'] =  ZakazCallsList.aggregate(Sum('total_price'))['total_price__sum']
    # context['totalSum'] = ZakazCallsList.aggregate(
    #     total_sum=Sum(Cast(F('total_price'), output_field=DecimalField()))
    # )['total_sum'] or 0
    
    # Сначала отфильтруем некорректные значения:
    ZakazCallsList = ZakazCallsList.filter(
        Q(total_price__regex=r'^\d+\.?\d*$') | Q(total_price__isnull=True)
    )
    # Используем безопасное преобразование и агрегацию:
    try:
        context['totalSum'] = ZakazCallsList.annotate(
            clean_price=Cast(
                F('total_price'),
                output_field=DecimalField(max_digits=10, decimal_places=2)
            )
        ).aggregate(
            total_sum=Sum('clean_price')
        )['total_sum'] or 0
    except Exception as e:
        messages.error(request, f"Ошибка при расчете суммы: {e}")
        context['totalSum'] = 0

    # context['totalSumProc'] =  ZakazCallsList.aggregate(Sum('total_priceProc'))['total_priceProc__sum']

    if request.method == 'POST' and 'action' in request.POST:
        # lists = request.POST.getlist('action')
        # pkWord = {}
        # for l in lists:
        #     pk = re.sub('[^0-9]', '', l)
        #     word = ''
        #     for i in l:
        #         if i.isalpha() or i == ' ':
        #             word = "".join([word,i])
        #     pkWord[pk] = word

        countOfChanges = 0
        # for pk, word in pkWord.items():
        #     call = ZakazCallsList.get(pk=pk)
        #     if call.action != word:
        #         countOfChanges += 1
        #         call.action = word
        #         # call.save()

        list_of_changet_input_price = request.POST.getlist('tatalPriceInput')
        for price_pk in list_of_changet_input_price:
            if price_pk != '':
                correct = True
                parts = price_pk.split('p')
                if len(parts) != 2:
                    messages.error(request,f"Ошибка в цене который вы прописали")
                    correct = False
                if ',' in parts[0]:
                    try:
                        call_price = float(parts[0].replace(',', '.'))
                    except:
                        messages.error(request,f"Ошибка в цене который вы прописали")
                        correct = False
                else:
                    try:
                        call_price = float(parts[0])
                    except:
                        messages.error(request,f"Ошибка в цене который вы прописали")
                        correct = False
                if correct:
                    call_pk = parts[1]
                    zakazCall = Zakaz.objects.get(pk=call_pk)
                    if call_price > 0:
                        zakazCall.total_price = call_price
                        zakazCall.action = 'заказ подтвержден'
                    else:
                        zakazCall.total_price = ''
                        zakazCall.action = 'бно'
                    zakazCall.save()
                    countOfChanges += 1
                else:
                    ZakazCallsList = Zakaz.objects.filter(DATE__range=[start,end], etrap=etrap)
                    context['ZakazCalls'] = ZakazCallsList
                    return render(request, 'telekom/operator071/zakazCalls.html', context)
    




        ZakazCallsList = Zakaz.objects.filter(DATE__range=[start,end], etrap=etrap)
        context['ZakazCalls'] = ZakazCallsList
        messages.success(request,f"Сохранено {countOfChanges} изменений")




    return render(request, 'telekom/operator071/zakazCalls.html', context)