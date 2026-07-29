from django.shortcuts import render, redirect
from django.db.models import Q

from telekom.models import StaffAction

from datetime import date

def staffActionList(request):
    context = {}
    context['matbIndex'] = True
    context['staffActionList'] = True

    current_date = date.today()
    current_date = str(current_date)
    context['current_date'] = current_date

    types = list(StaffAction.objects.order_by().values_list('action', flat=True).distinct())
    users = list(StaffAction.objects.order_by().values_list('user__username', flat=True).distinct())
    akt = list(StaffAction.objects.order_by().values_list('akt_raport', flat=True).distinct())

    




    comment = request.GET.get('comment') if request.GET.get('comment') != None else ''
    operator = request.GET.get('operator') if request.GET.get('operator') != None else ''
    action = request.GET.get('action') if request.GET.get('action') != None else ''
    akt_get = request.GET.get('akt') if request.GET.get('akt') != None else ''
    start = request.GET.get('start') if request.GET.get('start') != None else current_date
    end = request.GET.get('end') if request.GET.get('end') != None else current_date

    operatorAll = request.GET.get('operator') if request.GET.get('operator') == 'operatorAll' else None
    context['operatorAll'] = operatorAll 

    actionAll = request.GET.get('action') if request.GET.get('action') == 'actionAll' else None
    context['actionAll'] = actionAll

    aktAll = request.GET.get('akt') if request.GET.get('akt') == 'aktAll' else None
    context['aktAll'] = aktAll

    context['users'] = users
    context['types'] = types
    context['akt'] = akt
    context['akt_get'] = akt_get

    context['comment'] = comment

    context['operator'] = operator
    context['type_'] = action

    context['start'] = start
    context['end'] = end

    if actionAll or operatorAll or aktAll:
        print('2', actionAll, operatorAll, aktAll)


        if actionAll and operatorAll and aktAll:
            objs = StaffAction.objects.select_related('user').filter(date__range=[start,end], comment__icontains=comment).order_by('-date')
            print('titti')



        elif actionAll == 'actionAll' and operatorAll == None and aktAll == None:
            objs = StaffAction.objects.select_related('user').filter(Q(comment__icontains=comment) & Q(user__username__icontains=operator) & Q(akt_raport__icontains=akt_get)).filter(date__range=[start,end]).order_by('-date')        
        elif actionAll == 'actionAll' and operatorAll == 'operatorAll' and aktAll == None:
            objs = StaffAction.objects.select_related('user').filter(Q(comment__icontains=comment) & Q(akt_raport__icontains=akt_get)).filter(date__range=[start,end]).order_by('-date')    
        elif actionAll == 'actionAll' and operatorAll == None and aktAll == 'aktAll':
            objs = StaffAction.objects.select_related('user').filter(Q(comment__icontains=comment) & Q(user__username__icontains=operator)).filter(date__range=[start,end]).order_by('-date')


        elif actionAll == None and operatorAll == 'operatorAll' and aktAll == 'aktAll':
            objs = StaffAction.objects.select_related('user').filter(Q(comment__icontains=comment) & Q(action__icontains=action)).filter(date__range=[start,end]).order_by('-date')
        elif actionAll == None and operatorAll == 'operatorAll' and aktAll == None:
            objs = StaffAction.objects.select_related('user').filter(Q(comment__icontains=comment) & Q(action__icontains=action) & Q(akt_raport__icontains=akt_get)).filter(date__range=[start,end]).order_by('-date')
        elif actionAll == None and operatorAll == None and aktAll == 'aktAll':
            objs = StaffAction.objects.select_related('user').filter(Q(comment__icontains=comment) & Q(action__icontains=action) & Q(user__username__icontains=operator)).filter(date__range=[start,end]).order_by('-date')

    else:
        objs = StaffAction.objects.select_related('user').filter(
            Q(comment__icontains=comment) &
            Q(user__username__icontains=operator) &
            Q(action__icontains=action) &
            Q(akt_raport__icontains=akt_get)
        ).filter(date__range=[start,end]).order_by('-date')

    # if actionAll and operatorAll:
    #     objs = StaffAction.objects.select_related('user').filter(date__range=[start,end], comment__icontains=comment).order_by('-date')

    # elif actionAll == 'actionAll' and operatorAll == None:
    #     objs = StaffAction.objects.select_related('user').filter(Q(comment__icontains=comment) & Q(user__username__icontains=operator)).filter(date__range=[start,end]).order_by('-date')
        
    # elif actionAll == None and operatorAll == 'operatorAll':
    #     objs = StaffAction.objects.select_related('user').filter(Q(comment__icontains=comment) & Q(action__icontains=action)).filter(date__range=[start,end]).order_by('-date')
       
    # elif actionAll == None and operatorAll == None:
    #     objs = StaffAction.objects.filter(
    #         Q(comment__icontains=comment) &
    #         Q(user__username__icontains=operator) &
    #         Q(action__icontains=action) &
    #         Q(akt_raport__icontains=akt_get)
    #     ).filter(date__range=[start,end]).order_by('-date')


    context['objs'] = objs[:20000]
    return render(request, 'telekom/MATB/staffActionList.html', context)