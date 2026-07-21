from django.shortcuts import redirect

from telekom.models import LocalCall, UserTable
from telekom.views2.myFunc.myFunc import monthСonvert

# для .txt
from django.http import HttpResponse


def slrSuccessTxt(request):
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

    NumberEtrap_CallsLocal = {}

    if getNameList:
        for name in getNameList: 
            localCalls = LocalCall.objects.filter(file_name = name)

            # {20000Dashoguz: {2023.02.01: [totalMt, [cal], [cal], [cal]], {2023.02.02: [totalMt, [cal], [cal], [cal]]}}
            # {'20000Dashoguz': {'2023-02-01': [5, ['Dashoguz', '20000', '91456', datetime.date(2023, 2, 1), '11:00:00', '11:01:56', '00:02:00', '2'], ['Dashoguz', '20000', '91456', datetime.date(2023, 2, 1), '12:00:00', '12:02:56', '00:03:00', '3']], '2023-02-02': [6, ['Dashoguz', '20000', '20005', datetime.date(2023, 2, 2), '11:00:00', '11:05:56', '00:06:00', '6']]}, '50000Dashoguz': {'2023-02-01': [2, ['Dashoguz', '50000', '20005', datetime.date(2023, 2, 1), '11:00:00', '11:01:56', '00:02:00', '2']]}}
            # Разделения по дням   делаем словарь как сверху
            if localCalls:
                for call in localCalls:
                    
                    if (f'{call.SUB_A}{call.etrap}') not in NumberEtrap_CallsLocal:
                        NumberEtrap_CallsLocal[f'{call.SUB_A}{call.etrap}'] = {str(call.DATE): [int(call.MT), [call.etrap, call.SUB_A, call.SUB_B, call.DATE, call.START, call.FIN, call.DUR, call.MT]]}
                    else:
                        if f'{str(call.DATE)}' not in NumberEtrap_CallsLocal[f'{call.SUB_A}{call.etrap}']:
                            NumberEtrap_CallsLocal[f'{call.SUB_A}{call.etrap}'][str(call.DATE)] = [int(call.MT), [call.etrap, call.SUB_A, call.SUB_B, call.DATE, call.START, call.FIN, call.DUR, call.MT]]
                        else:
                            NumberEtrap_CallsLocal[f'{call.SUB_A}{call.etrap}'][str(call.DATE)][0] += int(call.MT)
                            NumberEtrap_CallsLocal[f'{call.SUB_A}{call.etrap}'][str(call.DATE)].append([call.etrap, call.SUB_A, call.SUB_B, call.DATE, call.START, call.FIN, call.DUR, call.MT])

        # убираем разговоры > 5 минут в день
        copy_dict = NumberEtrap_CallsLocal.copy()
        for numEtr, date_ in copy_dict.items():
            if numEtr in usersNumEtrList:
                date_copy = date_.copy()
                for dat_, calls in date_copy.items():
                    if calls[0] < 6:
                        del NumberEtrap_CallsLocal[numEtr][dat_]
                    else:
                        pass
            else:
                del NumberEtrap_CallsLocal[numEtr]

            # После удаления звонков могут остаться пустые словари {'24182Dashoguz': {}}, надо их удалить
            try:
                if NumberEtrap_CallsLocal[numEtr] == {}:
                    del NumberEtrap_CallsLocal[numEtr]
            except:
                pass

        response = HttpResponse(content_type="text/plain")
        txtName = f'slr success nachisleniya'
        response['Content-Disposition'] = f'attachment; filename={txtName}.txt'
        lines = [f"{txtName} files {getNameList}  \n\n"]    

        count = 0
        umumyTotalMinut = 0

        for numEtr, calls_ in NumberEtrap_CallsLocal.items():
            count += 1
            abonMt = 0
            abonPrice = 0
            s1 = (4 - len(str(count))) * ' '
            lines.append(f"============== {count}.{s1}{numEtr[:5]} {numEtr[5:].upper()} ====================\n")
            for date_, calls in calls_.items():
                lines.append(f"                      {date_}\n")
                lines.append(f"№    SUB_B   DATE       START      END       DUR     MT\n")
                count2 = 0
                dayMinut = calls[0] - 5
                dayPrice = (calls[0] - 5) * 0.0006
                abonMt += dayMinut
                abonPrice += dayPrice
                umumyTotalMinut += calls[0] - 5
                for call in calls[1:]:
                    count2 += 1
                    s2 = (4 - len(str(count2))) * ' '
                    s3 = (14 - len(call[1])) * ' '
                    s4 = (18 - len(call[1])) * ' '

                    s5 = (7 - len(call[6])) * ' '
                    s6 = (11 - len(str(call[7]))) * ' '

                     # 023-02-01': [7, ['S.A.Nyyazow', '31698', '50221', datetime.date(2023, 2, 1), '09:55:01', '10:01:26', '00:06:25', '7']]}}

                    lines.append(f"{count2}.{s2}{call[2]} {str(call[3])}  {call[4]}  {call[5]}  {call[6]}  {call[7]}\n")
                lines.append(f"------------------------------------------------------\n")
                lines.append(f"{date_}-ne JEMI: {dayMinut} minut    {'%.4f' % dayPrice} manat\n")
            lines.append(f"{numEtr[:5]} {numEtr[5:].upper()} abonentyn JEMI: {abonMt} minut    {'%.4f' % abonPrice} manat\n\n")

        umumyTotalPrice = umumyTotalMinut * 0.0006

        lines.append(f'                        UMUMY JEMI     {umumyTotalMinut} minut           {"%.4f" % umumyTotalPrice} manat')

    response.writelines(lines)
    return response
    
