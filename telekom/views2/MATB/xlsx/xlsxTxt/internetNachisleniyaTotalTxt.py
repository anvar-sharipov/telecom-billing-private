from django.http import HttpResponse

from telekom.models import ImportInternetNachisleniyaOFF, ImportInternetNachisleniyaON, OldLoginDogowor, UserTable
from telekom.views2.myFunc.myFunc import monthСonvert


def internetNachisleniyaTotalTxt(request, year, month, etrap, off):

    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench', 'Garashsyzlyk', 'Gubadag']
    month_numb = monthСonvert(month)

    if off == 'False':
        if etrap in etraps:
            internetNachisleniya = ImportInternetNachisleniyaON.objects.filter(month=month, year=year, etrap=etrap)
            users = UserTable.objects.filter(etrap=etrap)
        elif etrap == 'all':
            internetNachisleniya = ImportInternetNachisleniyaON.objects.filter(month=month, year=year)
            users = UserTable.objects.all()

    elif off == 'True':
        if etrap in etraps:
            internetNachisleniya = ImportInternetNachisleniyaOFF.objects.filter(month=month, year=year, etrap=etrap)
            users = UserTable.objects.filter(etrap=etrap)
        elif etrap == 'all':
            internetNachisleniya = ImportInternetNachisleniyaOFF.objects.filter(month=month, year=year)
            users = UserTable.objects.all()

    dogoworLogin = UserTable.objects.values('dogowor', 'login')

    dogowors = []
    logins = []

    for item_ in dogoworLogin:
        for col, val in item_.items():
            if col == 'dogowor' and val != '':
                dogowors.append(item_['dogowor'])
            elif col == 'login' and val != '':
                logins.append(item_['login'])

    ###
    oldLoginDogowor = OldLoginDogowor.objects.all()
    old_logins = {}
    old_dogowors = {}

    for logDog in oldLoginDogowor:
        if logDog.login:
            old_logins[logDog.login] = [logDog.etrap, logDog.number]
        if logDog.dogowor:
            old_dogowors[logDog.dogowor] = [logDog.etrap, logDog.number]
    ####


    error = []
    errorCount = 0
    errorPrice = 0

    successDogowor = []
    successDogoworCount = 0
    successDogoworPrice = 0

    successLogin = []
    successLoginCount = 0
    successLoginPrice = 0


    for nach in internetNachisleniya:
        if nach.dogowor in dogowors:
            successDogowor.append(nach)
            successDogoworCount += 1
            successDogoworPrice += nach.price
        elif nach.login in logins:
            successLogin.append(nach)
            successLoginCount += 1
            successLoginPrice += nach.price
        elif nach.login in old_logins:
            successLogin.append(nach)
            successLoginCount += 1
            successLoginPrice += nach.price
        elif nach.dogowor in old_dogowors:
            successDogowor.append(nach)
            successDogoworCount += 1
            successDogoworPrice += nach.price
        else:
            error.append(nach)
            errorCount += 1
            errorPrice += nach.price


    response = HttpResponse(content_type="text/plain")
    txtName = f'{year} {month_numb} Internet Nachisleniya Total {year}-{month_numb} {etrap}'
    response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
    lines = [f"\n\n    {txtName} \n\n"]

    
    lines.append(f"    Dogowor boyuncha tapylan {year} yylyn {month_numb}-nji ayy\n\n")
    count = 0
    for i in successDogowor:
        count += 1
        s1 = (50 - len(i.FAO)) * ' '
        s2 = (20 - len(i.dogowor)) * ' '
        s3 = (20 - len(i.login)) * ' '
        s4 = (10 - len(str(i.price))) * ' '
        s5 = (6 - len(str(count))) * ' '

        lines.append(f"{count}.{s5}{i.FAO}{s1}{i.dogowor}{s2}{i.login}{s3}{i.price}{s4}{i.etrap}\n")

    lines.append(f"    Login boyuncha tapylan {year} yylyn {month_numb}-nji ayy\n\n")

    for i in successLogin:
        count += 1
        s1 = (50 - len(i.FAO)) * ' '
        s2 = (20 - len(i.dogowor)) * ' '
        s3 = (20 - len(i.login)) * ' '
        s4 = (10 - len(str(i.price))) * ' '
        s5 = (6 - len(str(count))) * ' '

        lines.append(f"{count}.{s5}{i.FAO}{s1}{i.dogowor}{s2}{i.login}{s3}{i.price}{s4}{i.etrap}\n")

    lines.append(f"    Nachisleniya tapylmadyk {year} yylyn {month_numb}-nji ayy\n\n")

    for i in error:
        count += 1
        s1 = (50 - len(i.FAO)) * ' '
        s2 = (20 - len(i.dogowor)) * ' '
        s3 = (20 - len(i.login)) * ' '
        s4 = (10 - len(str(i.price))) * ' '
        s5 = (6 - len(str(count))) * ' '

        lines.append(f"{count}.{s5}{i.FAO}{s1}{i.dogowor}{s2}{i.login}{s3}{i.price}{s4}{i.etrap}\n")


    lines.append(f"\n\n\n     Dogowor boyuncha tapylan {successDogoworCount} sany, Jemi Bahasy: {successDogoworPrice}")
    lines.append(f"\n\n     Login boyuncha tapylan {successLoginCount} sany, Jemi Bahasy: {successLoginPrice}")
    lines.append(f"\n\n     Dogowor hem login boyuncha tapylmadyk abonentlar sany {errorCount}, Jemi Bahasy: {errorPrice}")

    response.writelines(lines)
    return response
