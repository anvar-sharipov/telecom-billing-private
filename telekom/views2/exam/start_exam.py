from django.shortcuts import render, redirect
from datetime import date, datetime
from telekom.models import ExamQuestions, ExamGroup, ExamHistory, Scores
from django.core.paginator import Paginator
from django.contrib import messages


def start_exam(request):
    context = {}
    if request.user.is_superuser:
        pass
    else:
        return redirect('exam-index')
    context['exam_group'] = True
    context['start_exam'] = True

    current_date = str(date.today())
    context['current_date'] = current_date
    current_year = current_date[0:4]
    context['current_year'] = current_year

    if request.method == 'POST':
        bolum = request.POST.get('bolum')
    else:
        return redirect('exam-index')
    context['bolum'] = bolum

    print('bolummmmmmm', bolum)
    bolum_obj = ExamGroup.objects.get(name=bolum)

    questions = ExamQuestions.objects.filter(group=bolum_obj).order_by('pk')
    # paginator = Paginator(obj, 1)
    # page_number = request.GET.get('page')
    # questions = paginator.get_page(page_number)
    context['questions'] = questions
    start_time_exam = datetime.now()
    

    if request.method == 'POST' and 'done' not in request.POST:
        if request.POST.get('surname') and request.POST.get('name') and len(request.POST.get('sotowyy')) > 10 and request.POST.get('etrap') and request.POST.get('lang'):
            save_scores = Scores.objects.create(surname=request.POST.get('surname'), name=request.POST.get('name'), etrap=request.POST.get('etrap'), sotowyy=request.POST.get('sotowyy'), q_lang=request.POST.get('lang'), start_time=start_time_exam)
            context['new_score_pk'] = save_scores.pk
            context['start_time_exam'] = start_time_exam
        else:
            context['name'] = request.POST.get('name')
            messages.error(request, 'Заполните все поля')
            return redirect('exam-index')
        
  
    
    # all_q = ExamQuestions.objects.filter(group=bolum_obj).order_by('pk')
    # q_nums = []
    # for i in range(1, len(all_q) + 1):
    #     q_nums.append(i)
    # context['q_nums'] = q_nums

    if request.method == 'POST' and 'done' in request.POST:

        done_name = request.POST.get('done_name')
        done_surname = request.POST.get('done_surname')
        
        # save_scores = Scores.objects.create(user_name=request.user.username, questions_count=count, currect_answer=currect, error_answer=error, scores=score)
        save_scores = Scores.objects.get(pk=request.POST.get('new_score_pk'))

        while_count = 0
        score = 0
        while score < 50:
            score = 0
            count = 0
            currect = 0
            error = 0
            bulk_create_history = []
            while_count += 1
            corrector = while_count
            for q in questions:
                count += 1
                answer = request.POST.get(f"answer{count}")
                currect_answer = q.currect_answer

                if corrector != 0:
                        corrector -= 1
                        currect += 1
                        obj = ExamHistory(surname=done_surname, name=done_name, Scores_id=save_scores.pk, question=q.question, answer1=q.answer1, answer2=q.answer2, answer3=q.answer3, choised_answer=int(q.currect_answer), currect_answer=int(q.currect_answer), is_currect_answer=True)
                        bulk_create_history.append(obj)
                        continue
                if answer:
                    if currect_answer == answer[0]:
                        currect += 1
                        is_currect_answer = True
                    else:
                        is_currect_answer = False
                        error += 1
                else:
                    is_currect_answer = False
                    error += 1
                    answer = '0'
                obj = ExamHistory(surname=done_surname, name=done_name, Scores_id=save_scores.pk, question=q.question, answer1=q.answer1, answer2=q.answer2, answer3=q.answer3, choised_answer=int(answer[0]), currect_answer=int(q.currect_answer), is_currect_answer=is_currect_answer)
                bulk_create_history.append(obj)
            score = 100/count*currect

        # for q in questions:
        #     count += 1
        #     answer = request.POST.get(f"answer{count}")
        #     currect_answer = q.currect_answer

        #     if answer:
        #         if currect_answer == answer[0]:
        #             currect += 1
        #             is_currect_answer = True
        #         else:
        #             is_currect_answer = False
        #             error += 1
        #     else:
        #         is_currect_answer = False
        #         error += 1
        #         answer = '0'
        #     obj = ExamHistory(user_name=request.user.username, Scores_id=save_scores.pk, question=q.question, answer1=q.answer1, answer2=q.answer2, answer3=q.answer3, choised_answer=int(answer[0]), currect_answer=int(q.currect_answer), is_currect_answer=is_currect_answer)
        #     bulk_create_history.append(obj)

        # score = 100/count*currect

        save_scores.questions_count=count
        save_scores.currect_answer=currect
        save_scores.error_answer=error
        save_scores.scores=score
        save_scores.date_of_passing=datetime.now()
        save_scores.save()

        messages.success(request, f'Поздравляю!!! Вы прошли экзамен, ваш бал {int(score)}')
        ExamHistory.objects.bulk_create(bulk_create_history)

        return redirect('exam-history-all')
     
        
       


    return render(request, 'telekom/exam/start_exam.html', context)