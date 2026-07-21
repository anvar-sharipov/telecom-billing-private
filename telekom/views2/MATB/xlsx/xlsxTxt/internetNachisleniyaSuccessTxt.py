from django.http import HttpResponse

from telekom.models import ImportInternetNachisleniyaOFF, ImportInternetNachisleniyaON, OldLoginDogowor, UserTable
from telekom.views2.myFunc.myFunc import monthСonvert


def internetNachisleniyaSuccessTxt(request, year, month, etrap, off):

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


    response = HttpResponse(content_type="text/plain")
    txtName = f'{year} {month_numb} Internet Nachisleniya Success {year}-{month_numb} {etrap}'
    response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
    lines = [f"\n\n    {txtName} \n\n"]

    lines.append(f"    Dogowor boyuncha tapylan {year} yylyn {month_numb}-nji ayy\n\n")

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
    lines.append(f"\n\n\n     Dogowor boyuncha tapylan {successDogoworCount} sany, Jemi Bahasy: {successDogoworPrice}")
    lines.append(f"\n\n     Login boyuncha tapylan {successLoginCount} sany, Jemi Bahasy: {successLoginPrice}")

    ###
    lines.append(f"\n\n\n\n    Old login, dogowor {year} yylyn {month_numb}-nji ayy\n\n")
    for n in internetNachisleniya:
        if n.login not in logins and n.dogowor not in dogowors and (n.login in old_logins or n.dogowor in old_dogowors):
            if n.login in old_logins:
                count += 1
                user = users.get(etrap=old_logins[n.login][0], number=old_logins[n.login][1])
                s1 = (50 - len(f"{user.name} {user.surname}")) * ' '
                s2 = (20 - len(n.dogowor)) * ' '
                s3 = (20 - len(n.login)) * ' '
                s4 = (10 - len(str(n.price))) * ' '
                s5 = (6 - len(str(count))) * ' '

                lines.append(f"{count}.{s5}{user.name} {user.surname}{s1}{n.dogowor}{s2}{n.login}{s3}{n.price}{s4}{user.etrap}\n")
                continue
            if n.dogowor in old_dogowors:
                count += 1
                user = users.get(etrap=old_dogowors[n.dogowor][0], number=old_dogowors[n.dogowor][1])
                s1 = (50 - len(f"{user.name} {user.surname}")) * ' '
                s2 = (20 - len(n.dogowor)) * ' '
                s3 = (20 - len(n.login)) * ' '
                s4 = (10 - len(str(n.price))) * ' '
                s5 = (6 - len(str(count))) * ' '

                lines.append(f"{count}.{s5}{user.name} {user.surname}{s1}{n.dogowor}{s2}{n.login}{s3}{n.price}{s4}{user.etrap}\n")
                continue
    ####

    response.writelines(lines)
    return response
