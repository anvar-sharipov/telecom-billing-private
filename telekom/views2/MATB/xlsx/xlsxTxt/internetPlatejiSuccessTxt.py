
from django.http import HttpResponse

from telekom.models import ImportInternetPlateji, ImportInternetPlatejiOFF, OldLoginDogowor, UserTable
from telekom.views2.myFunc.myFunc import monthСonvert

from calendar import monthrange




def internetPlatejiSuccessTxt(request, year, month, etrap, off):
    month_word = month
    year = year
    month_numb = monthСonvert(month_word)



    days_in_nach_month = monthrange(int(year), int(month_numb))[1]

    first = f"{year}-{month_numb}-01"
    last = f"{year}-{month_numb}-{days_in_nach_month}"

    if etrap == 'all':
        if off == 'False':
            internetPlateji = ImportInternetPlateji.objects.filter(pay_date__range=[first, last])
        else:
            internetPlateji = ImportInternetPlatejiOFF.objects.filter(pay_date__range=[first, last])

    else:
        if off == 'False':
            internetPlateji = ImportInternetPlateji.objects.filter(pay_date__range=[first, last], etrap=etrap)
        else:
            internetPlateji = ImportInternetPlatejiOFF.objects.filter(pay_date__range=[first, last], etrap=etrap)


    UserTableDog = []

    if etrap == 'all':
            get_dogoworsBD = UserTable.objects.values('dogowor')
    else:
        get_dogoworsBD = UserTable.objects.filter(etrap=etrap).values('dogowor')

    for i in get_dogoworsBD:
        for key, value in i.items():
            if value != '':
                UserTableDog.append(''.join(value).upper())

    UserNumberEtrap = []

    if etrap == 'all':
        UserNumberEtrapObj = UserTable.objects.values('number', 'etrap')
    else:
        UserNumberEtrapObj = UserTable.objects.filter(etrap=etrap).values('number', 'etrap')

    for item in UserNumberEtrapObj:
        numberEtrap = ''
        for key, value in item.items():
            numberEtrap += value
        UserNumberEtrap.append(numberEtrap)


    ###
    oldLoginsDogowors = OldLoginDogowor.objects.all()
    old_dogowors = {}
    etrapNumberDogowors = {}
    for logDog in oldLoginsDogowors:
        if logDog.dogowor:
            old_dogowors[logDog.dogowor] = [logDog.etrap, logDog.number]
        if f"{logDog.etrap}{logDog.number}" not in etrapNumberDogowors:
            etrapNumberDogowors[f"{logDog.etrap}{logDog.number}"] = [logDog.dogowor]
        else:
            etrapNumberDogowors[f"{logDog.etrap}{logDog.number}"].append([logDog.dogowor])

    platejiOldDog = {}
    platejiOldDogPayCount = 0
    platejiOldDogPayTotalPrice = 0
    ####


    PlatejiDog = {}
    platejiDogoworPayCount = 0
    platejiDogoworTotalPrice = 0

    PlatejiDogError = {}
    platejiErrorDogoworPayCount = 0
    platejiErrorDogoworTotalPrice = 0

    PlatejiTelefon = {}
    platejiTelefonPayCount = 0
    platejiTelefonTotalPrice = 0

    PlatejiTelefonError = {}
    platejiErrorTelefonPayCount = 0
    platejiErrorTelefonTotalPrice = 0

    PlatejiAlem = {}
    platejiAlemPayCount = 0
    platejiAlemTotalPrice = 0

    PlatejiAlemError = {}
    platejiErrorAlemPayCount = 0
    platejiErrorAlemTotalPrice = 0

    
    for pay in internetPlateji:
        try:
            dogoworTelefon = int(pay.dogowor)       
        except:
            dogoworTelefon = None
        
        if dogoworTelefon:
            # f"{pay.dogowor[6:]}{pay.etrap}"
            if pay.dogowor not in PlatejiTelefon and f"{pay.dogowor[6:]}{pay.etrap}" in UserNumberEtrap:
                PlatejiTelefon[pay.dogowor] = [pay.type, pay.pay_date, pay.FAO, pay.price, pay.etrap]
                platejiTelefonPayCount += 1
                platejiTelefonTotalPrice += pay.price
            elif pay.dogowor in PlatejiTelefon and f"{pay.dogowor[6:]}{pay.etrap}" in UserNumberEtrap:
                PlatejiTelefon[pay.dogowor][3] += pay.price
                platejiTelefonPayCount += 1 
                platejiTelefonTotalPrice += pay.price
            elif pay.dogowor not in PlatejiTelefonError and f"{pay.dogowor[6:]}{pay.etrap}" not in UserNumberEtrap:
                PlatejiTelefonError[pay.dogowor] = [pay.type, pay.pay_date, pay.FAO, pay.price, pay.etrap]
                platejiErrorTelefonPayCount += 1
                platejiErrorTelefonTotalPrice += pay.price
            elif pay.dogowor in PlatejiTelefonError and f"{pay.dogowor[6:]}{pay.etrap}" not in UserNumberEtrap:
                PlatejiTelefonError[pay.dogowor][3] += pay.price
                platejiErrorTelefonPayCount += 1
                platejiErrorTelefonTotalPrice += pay.price
            continue  
    

        if pay.dogowor[:4] == 'IPTV':
            if pay.dogowor not in PlatejiAlem and f"{pay.dogowor[11:]}{pay.etrap}" in UserNumberEtrap:
                PlatejiAlem[pay.dogowor] = [pay.type, pay.pay_date, pay.FAO, pay.price, pay.etrap]
                platejiAlemPayCount += 1
                platejiAlemTotalPrice += pay.price
            elif pay.dogowor in PlatejiAlem and f"{pay.dogowor[11:]}{pay.etrap}" in UserNumberEtrap:
                PlatejiAlem[pay.dogowor][3] += pay.price
                platejiAlemPayCount += 1
                platejiAlemTotalPrice += pay.price
            elif pay.dogowor not in PlatejiAlemError and f"{pay.dogowor[11:]}{pay.etrap}" not in UserNumberEtrap:
                PlatejiAlemError[pay.dogowor] = [pay.type, pay.pay_date, pay.FAO, pay.price, pay.etrap]
                platejiErrorAlemPayCount += 1
                platejiErrorAlemTotalPrice += pay.price
            elif pay.dogowor in PlatejiAlemError and f"{pay.dogowor[11:]}{pay.etrap}" not in UserNumberEtrap:
                PlatejiAlemError[pay.dogowor][3] += pay.price
                platejiErrorAlemPayCount += 1
                platejiErrorAlemTotalPrice += pay.price
            continue


        if pay.dogowor not in PlatejiDog and pay.dogowor in UserTableDog:
            PlatejiDog[pay.dogowor] = [pay.type, pay.pay_date, pay.FAO, pay.price, pay.etrap]
            platejiDogoworPayCount += 1
            platejiDogoworTotalPrice += pay.price
        elif pay.dogowor in PlatejiDog and pay.dogowor in UserTableDog:
            PlatejiDog[pay.dogowor][3] += pay.price
            platejiDogoworPayCount += 1
            platejiDogoworTotalPrice += pay.price
        ###
        elif pay.dogowor not in platejiOldDog and pay.dogowor in old_dogowors:
            platejiOldDog[pay.dogowor] = [pay.type, pay.pay_date, pay.FAO, pay.price, pay.etrap]
            platejiOldDogPayCount += 1
            platejiOldDogPayTotalPrice += pay.price
        elif pay.dogowor in platejiOldDog and pay.dogowor in old_dogowors:
            platejiOldDog[pay.dogowor][3] += pay.price
            platejiOldDogPayCount += 1
            platejiOldDogPayTotalPrice += pay.price
        ####
        elif pay.dogowor not in PlatejiDogError and pay.dogowor not in UserTableDog:
            PlatejiDogError[pay.dogowor] = [pay.type, pay.pay_date, pay.FAO, pay.price, pay.etrap]
            platejiErrorDogoworPayCount += 1
            platejiErrorDogoworTotalPrice += pay.price
        elif pay.dogowor in PlatejiDogError and pay.dogowor not in UserTableDog:
            PlatejiDogError[pay.dogowor][3] += pay.price
            platejiErrorDogoworPayCount += 1
            platejiErrorDogoworTotalPrice += pay.price

    response = HttpResponse(content_type="text/plain")
    txtName = f'{year} {month_numb} Wneshnie Plateji Success {year}-{month_numb} {etrap}'
    response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
    lines = [f"{txtName} \n\n"]

    lines.append(f"                                                  ABONPLATA plateji \n\n")
    totalSum = 0
    count = 0
    for dogowor, value in PlatejiTelefon.items():
        count += 1
        s1 = (6 - len(str(count))) * ' '
        s2 = (20 - len(str(dogowor))) * ' '
        s3 = (30 - len(str(value[0]))) * ' '
        s4 = (40 - len(str(value[2]))) * ' '
        s5 = (8 - len(str(value[3]))) * ' '
        lines.append(f"  {count}.{s1}{dogowor}{s2}{value[0]}{s3}{value[1]}  {value[2]}{s4}  {value[3]}{s5}{value[4]}\n")
        totalSum += value[3]
    lines.append(f"\n                                                                                        Umumy Jemi               {'%.2f' % totalSum}\n\n\n")

    lines.append(f"                                                  ALEM TV plateji \n\n")
    totalSum = 0
    count = 0
    for dogowor, value in PlatejiAlem.items():
        count += 1
        s1 = (6 - len(str(count))) * ' '
        s2 = (20 - len(str(dogowor))) * ' '
        s3 = (30 - len(str(value[0]))) * ' '
        s4 = (40 - len(str(value[2]))) * ' '
        s5 = (8 - len(str(value[3]))) * ' '
        lines.append(f"  {count}.{s1}{dogowor}{s2}{value[0]}{s3}{value[1]}  {value[2]}{s4}  {value[3]}{s5}{value[4]}\n")
        totalSum += value[3]
    lines.append(f"\n                                                                                        Umumy Jemi               {'%.2f' % totalSum}\n\n\n")


    lines.append(f"                                                  INTERNET plateji \n\n")
    totalSum = 0
    count = 0
    for dogowor, value in PlatejiDog.items():
        count += 1
        s1 = (6 - len(str(count))) * ' '
        s2 = (20 - len(str(dogowor))) * ' '
        s3 = (30 - len(str(value[0]))) * ' '
        s4 = (40 - len(str(value[2]))) * ' '
        s5 = (8 - len(str(value[3]))) * ' '
        lines.append(f"  {count}.{s1}{dogowor}{s2}{value[0]}{s3}{value[1]}  {value[2]}{s4}  {value[3]}{s5}{value[4]}\n")
        totalSum += value[3]
    
    for dogowor, value in platejiOldDog.items():
        count += 1
        s1 = (6 - len(str(count))) * ' '
        s2 = (20 - len(str(dogowor))) * ' '
        s3 = (30 - len(str(value[0]))) * ' '
        s4 = (40 - len(str(value[2]))) * ' '
        s5 = (8 - len(str(value[3]))) * ' '
        lines.append(f"  {count}.{s1}{dogowor}{s2}{value[0]}{s3}{value[1]}  {value[2]}{s4}  {value[3]}{s5}{value[4]}\n")
        totalSum += value[3]
    
    lines.append(f"\n                                                                                        Umumy Jemi               {'%.2f' % totalSum}\n\n\n")

    response.writelines(lines)
    return response
