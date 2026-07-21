from django.shortcuts import render, redirect
from datetime import date
from telekom.models import ExamGroup, Scores, ExamHistory


def exam_index(request):

    if request.user.is_superuser and 'admin1' in request.user.username:
        # Scores.objects.all().delete()
        # ExamHistory.objects.all().delete()
        pass


    context = {}
    etraps = ['Dashoguz', 'Akdepe', 'Gorogly', 'Ruhubelent', 'S.A.Nyyazow', 'Turkmenbashy', 'Boldumsaz', 'Koneurgench']
    context['etraps'] = etraps
    context['exam_group'] = True
    current_date = str(date.today())
    context['current_date'] = current_date
    current_year = current_date[0:4]
    context['current_year'] = current_year

    groups = []
    for g in ExamGroup.objects.all():
        groups.append(g.name)
    context['groups'] = groups

    return render(request, 'telekom/exam/exam_index.html', context)