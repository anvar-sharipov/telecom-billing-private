from django.shortcuts import render, redirect
from datetime import date
from telekom.models import ExamHistory, Scores


def exam_history(request):

    if request.user.is_superuser:
        pass
    else:
        return redirect('exam-index')
    context = {}


    ids = []
    history = ExamHistory.objects.latest('pk')

    
    scores_h = Scores.objects.filter(surname=history.surname, name=history.name).order_by('-date_of_passing')
    context['scores_h'] = scores_h

    if request.method == 'POST':
        context['view'] = True
        score_id = request.POST.get('score_id')
        examHistory = ExamHistory.objects.filter(Scores_id = score_id).order_by('?')
        context['examHistory'] = examHistory


    
   

    return render(request, 'telekom/exam/exam_history.html', context)