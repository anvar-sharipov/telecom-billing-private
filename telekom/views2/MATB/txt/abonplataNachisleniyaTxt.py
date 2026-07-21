
# from django.shortcuts import redirect
# from django.contrib import messages


from telekom.models import NachMinus, UserTable
from telekom.views2.myFunc.myFunc import monthСonvert


# для .txt
from django.http import HttpResponse

def abonplataNachisleniyaTxt(request, etrap):
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']

    if etrap in etraps:
        users = UserTable.objects.filter(etrap=etrap)
    elif etrap == 'all':
        users = UserTable.objects.all() 
    else:
        users = False

    response = HttpResponse(content_type="text/plain")
    txtName = f'{etrap} Abonplata nachisleniya'
    response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
    lines = [f"#:number:etrap:name:surname:abonplata:edara\n"]
    count = 0
    test = 0
    if users:
        for user in users:
            if user.abonplata:
                a = float(user.abonplata)
                count += 1
                test += float(user.abonplata)
                if user.is_enterprises:
                    lines.append(f'{count}:{user.number}:{user.etrap}:{user.name}:{user.surname}:{a}:E\n')
                else:
                    lines.append(f'{count}:{user.number}:{user.etrap}:{user.name}:{user.surname}:{a}:N\n')

        response.writelines(lines)
        return response
