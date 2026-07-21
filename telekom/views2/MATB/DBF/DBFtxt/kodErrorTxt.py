
from telekom.models import NonLocalCall, UserTable
# для .txt
from django.http import HttpResponse


def kodErrorTxt(request):
    getNameList = request.POST.getlist('nameLists')

    usersNumEtrap = UserTable.objects.values('number', 'etrap')
    # ['20000Dashoguz', '20000Akdepe'] список из numberetrap которые есть в нашей БД
    usersNumEtrList = {}
    for dict_ in usersNumEtrap:
        for key, val in dict_.items():
            if key == 'number':
                word = val
            if key == 'etrap':
                word += val
        usersNumEtrList[word] = True

    globalNumberEtrap_CallsGlobal = {}

    if getNameList:
         for name in getNameList: 

            globalCalls = NonLocalCall.objects.filter(file_name = name)

            if globalCalls:
                for call in globalCalls:
                    
                    if f"{call.SUB_A}{call.SUB_A_etrap}" not in globalNumberEtrap_CallsGlobal:
                        globalNumberEtrap_CallsGlobal[f"{call.SUB_A}{call.SUB_A_etrap}"] = [[call.SUB_B, call.SUB_B_locations, call.DATE, call.START, call.FIN, call.DUR, call.MT, call.price, call.total_price]]
                    else:
                        globalNumberEtrap_CallsGlobal[f"{call.SUB_A}{call.SUB_A_etrap}"].append([call.SUB_B, call.SUB_B_locations, call.DATE, call.START, call.FIN, call.DUR, call.MT, call.price, call.total_price])

    copy_dict = globalNumberEtrap_CallsGlobal.copy()

    for numEtr, calls in copy_dict.items():
        if numEtr in usersNumEtrList:
            del globalNumberEtrap_CallsGlobal[numEtr]

    response = HttpResponse(content_type="text/plain")
    txtName = f'kod error nachisleniya'
    response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
    lines = [f"{txtName} file {getNameList}  \n\n"]

    count = 0
    umumyTotalMinut = 0
    umumyTotalPrice = 0
    for numEtr, calls in globalNumberEtrap_CallsGlobal.items():
        count += 1
        s1 = (6 - len(str(count))) * ' '
        lines.append(f"======================================== {count}.{s1}{numEtr[:5]} {numEtr[5:].upper()} ========================================= \n")
        lines.append(f"№       SUB_B        LOCATION             DATE       START     END       DUR     MT   Min/manat umumy/manat\n")
        count2 = 0
        totalMinut = 0
        totalPrice = 0
        for call in calls:
            totalMinut += int(call[6])
            totalPrice += call[8]
            count2 += 1
            s2 = (4 - len(str(count2))) * ' '
            s3 = (16 - len(call[0])) * ' '
            s4 = (18 - len(call[1])) * ' '

            s5 = (7 - len(call[6])) * ' '
            s6 = (11 - len(str(call[7]))) * ' '
   

            #   '94066Dashoguz': [['80062708004', 'Sotowyy', datetime.date(2023, 2, 9), '10:42:14', '10:42:38', '00:00:24', '1', 0.08, 0.08]]}
            lines.append(f"{count2}.{s2}{call[0]}{s3}{call[1]}{s4}{str(call[2])}  {call[3]}  {call[4]}  {call[5]}  {call[6]}{s5}{call[7]}{s6}{call[8]}\n")

        umumyTotalMinut += totalMinut
        umumyTotalPrice += totalPrice

        lines.append(f'\n                                JEMI     {totalMinut} minut           {"%.2f" % totalPrice} manat\n\n')

    lines.append(f'                        UMUMY JEMI     {umumyTotalMinut} minut           {"%.2f" % umumyTotalPrice} manat')

    response.writelines(lines)
    return response
