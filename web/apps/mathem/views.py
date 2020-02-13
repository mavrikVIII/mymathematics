from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from .models import Question, Comment, PeoplesErrors
from django.http import Http404,HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from registration.views import index
from django.shortcuts import get_object_or_404

#доп ф-я для проверки администратора
def it_is_admin(request):
    username=request.user
    if str(username)=='admin':
        is_admin = True
    else:
        is_admin = False
    return is_admin


def detail(request,question_id):
    # try:
    #     a=Question.objects.get(id=question_id)
    # except:
    #     raise Http404('Статья не найдена')
    a = get_object_or_404(Question, id = question_id)
    is_admin = it_is_admin(request)
    latest_comment_list = a.comment_set.order_by('id')[:10]
    return render(request, 'mathem/detail.html',{'question':a,  'latest_comment_list':latest_comment_list, 'is_admin':is_admin})

def leave_answer(request,question_id):
    # try:
    #     a = Question.objects.get(id=question_id)
    # except:
    #     raise Http404('Задача не найдена')
    a = get_object_or_404(Question, id = question_id) # это строка замена 4-ем строкам сверху
    user_answer=request.POST.get('answer')
    latest_comment_list = a.comment_set.order_by('id')[:10]
    
    is_admin = it_is_admin(request)
    visible_ = True
    if user_answer==str(a.answer_text):
        results='Вы ответили правильно!'
        get_result = True
    else:
        results='Вы ответили неправильно'
        get_result = False
    context={'question': a, 'result': results, 'get_result':get_result, 'visible_':visible_, 'latest_comment_list':latest_comment_list, 'is_admin':is_admin}
    return render(request, 'mathem/detail.html', context)

def add_task(request):
    return render(request, 'mathem/addTask.html')

def task_add_in(request):
    user_question_title=request.POST['question_title']
    user_question_text=request.POST['question_text']
    user_answer_question=int(request.POST['answer_text'])

    a=Question(question_title = user_question_title, question_text=user_question_text, answer_text=user_answer_question)
    a.save()
    question_list = Question.objects.all()

    return redirect('..')

def manyuser(request):
    users = User.objects.count()
    this_user=request.user
    # this_id=this_user.id
    if users:
        visi_=True
    context={'users':users,'visi_':visi_,}
    #return HttpResponseRedirect(reverse('registration:index' ),context)
    return render(request,'registration/index.html',context)

def change_question(request, question_id):
    # try:
    #     a = Question.objects.get(id=question_id)
    # except:
    #     raise Http404('Задача не найдена');
    a = get_object_or_404(Question, id = question_id)
    username = request.user
    user_question_title=a.question_title
    user_question_text=a.question_text
    user_answer_question=int(a.answer_text)
    context={'username' : username, 'question_id' : question_id, 'a' : a }
    return render(request,'mathem/edit.html',context)

def save_edit_question(request, question_id):
    # try:
    #     a = Question.objects.get(id=question_id)
    # except:
    #     raise Http404('Задача не найдена')
    a = get_object_or_404(Question, id = question_id)
    user_question_title=request.POST['edit_title']
    user_question_text=request.POST['edit_text']
    user_answer_question=request.POST['edit_answer']

    a.question_title=user_question_title
    a.question_text=user_question_text
    a.answer_text=user_answer_question

    a.save()

    return redirect('..')

def leave_comment(request,question_id):
    # try:
    #     a = Question.objects.get(id=question_id)
    # except:
    #     raise Http404('Задача не найдена')
    a = get_object_or_404(Question, id = question_id)
    now=timezone.now()
    a.comment_set.create( author_name = request.user, comment_text=request.POST['text_comment'], pub_date=now)

    return HttpResponseRedirect(reverse('mathem:detail',args=(a.id,) ))


def report_error(request, question_id):

    # try:
    #     a = Question.objects.get(id=question_id)
    # except:
    #     raise Http404('Задача не найдена')
    a = get_object_or_404(Question, id = question_id)
    people_user=request.user
    time_now = timezone.now()
    people_errors = request.POST['text_error']
    visible = True


    # s = PeoplesErrors(people_name = people_user, people_message = people_errors, date_message = time_now)
    a.peopleserrors_set.create(people_name = people_user, people_message = people_errors, date_message = time_now)
    # s.save()
    # context = {'alert_message': alert_message, 'visible': visible}
    return HttpResponseRedirect(reverse('mathem:detail',args=(a.id,)))
    # return render(request, 'mathem/detail.html', context)

def views_errors(request,question_id):
    # try:
    #     a = Question.objects.get(id=question_id)
    # except:
    #     raise Http404('Задача не найдена')
    a = get_object_or_404(Question, id = question_id)
    errors_all = PeoplesErrors.objects.all()
    return render(request, 'mathem/report_errors.html', {'errors_all': errors_all})
