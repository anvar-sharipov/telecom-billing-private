from django.shortcuts import render, redirect
from datetime import date
from telekom.models import ExamHistory, Scores


def exam_history_all(request):
    if request.user.is_superuser:
        pass
    else:
        return redirect('exam-index')
    
    context = {}


    # ids = []
    # history = ExamHistory.objects.all().order_by('Scores_id')

    # for h in history:
    #     if h.Scores_id not in ids:
    #         ids.append(h.Scores_id)
    

    if request.user.is_superuser:
        scores_h = Scores.objects.all().order_by('-date_of_passing')
    else:
        last_pk = Scores.objects.all().latest('pk')
        scores_h = Scores.objects.filter(pk=last_pk.pk)
        print('gggggggg', scores_h)

    context['scores_h'] = scores_h

    if request.method == 'POST':
        context['view'] = True
        score_id = request.POST.get('score_id')
        examHistory = ExamHistory.objects.filter(Scores_id = score_id).order_by('?')
        context['examHistory'] = examHistory


    
   

    return render(request, 'telekom/exam/exam_history_all.html', context)