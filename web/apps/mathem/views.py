from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from .models import Question, Comment, PeoplesErrors, Profile
from django.http import Http404,HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from registration.views import index
from django.shortcuts import get_object_or_404

#доп функция для определения количества неправильных ответов
def wrong_solved(solved_list,list_wrong):
    # solved_list = list(solved_list)
    # list_wrong = list(list_wrong)
    i = 0
    while i < len(list_wrong):
        if list_wrong[i] in solved_list:
            list_wrong.remove(list_wrong[i])
        else:
            i+=1
    return list_wrong
#доп ф-я для проверки администратора
def it_is_admin(request):
    username=request.user
    if str(username)=='admin':
        is_admin = True
    else:
        is_admin = False
    return is_admin
#Преобразует строку в массив целых чисел - ВСПОМАГАТЕЛЬНАЯ ФУНКЦИЯ
def TextToMass(s):
    s = s.replace('{','')
    s = s.replace('}','')
    s = s.replace('set','')
    s = s.replace('(','')
    s = s.replace(')','')
    b = []
    a = s.split(', ')
    for i in a:
        b.append(int(i))
    return b
#Возвращает список решенных пользователем задач - ВСПОМАГАТЕЛЬНАЯ ФУНКЦИЯ
def ReturnList(request):
    if request.user.is_authenticated:
        username = request.user
        b = Profile.objects.get( user = username )
        if b.solved_task:
            solved_list = b.solved_task
            solved_list = TextToMass(solved_list)
        else:
            solved_list = []
    else:
        solved_list = []
    return solved_list
# доп ф-я для ошибочных ответов
def ReturnListWrong(request):
    if request.user.is_authenticated:
        username = request.user
        b = Profile.objects.get( user = username )
        solved_list = b.solved_task
        if b.wrong_solved_task:
            list_wrong = b.wrong_solved_task
            list_wrong = TextToMass(list_wrong)
        else:
            list_wrong = []
    else:
        list_wrong = []
    return list_wrong

def detail(request,question_id):
    # try:
    #     a=Question.objects.get(id=question_id)
    # except:
    #     raise Http404('Статья не найдена')
    if request.user.is_authenticated:
        usernmane = request.user
        user_id = usernmane.id
        b = get_object_or_404(Profile, id = user_id)
        list_finish_question = b.solved_task
        if list_finish_question:
            list_finish_question = TextToMass(list_finish_question)
        else:
            list_finish_question = []
    else:
        usernmane = 'Пользователь'
        list_finish_question = []

    a = get_object_or_404(Question, id = question_id)  # это строка замена 4-ем строкам сверху
    is_admin = it_is_admin(request)
    latest_comment_list = a.comment_set.order_by('id')[:10]
    context = {'usernmane': usernmane,'question':a,  'latest_comment_list':latest_comment_list, 'is_admin':is_admin, 'list_finish_question':list_finish_question }
    return render(request, 'mathem/detail.html',context)


def leave_answer(request,question_id):

    a = get_object_or_404(Question, id = question_id) # это строка замена 4-ем строкам сверху

    solved_list = ReturnList(request)
    list_wrong = ReturnListWrong(request)

    user_answer=request.POST.get('answer')
    latest_comment_list = a.comment_set.order_by('id')[:10]

    is_admin = it_is_admin(request)
    visible_ = True
    b = Profile.objects.get( user = request.user )
    if user_answer==str(a.answer_text):

        results='Вы ответили правильно!'
        solved_list.append(question_id)
        b.solved_task = str(set(solved_list))
        if (question_id in solved_list) and (question_id in list_wrong):
            list_wrong = wrong_solved(solved_list, list_wrong)
            if not list_wrong:
                b.wrong_solved_task = '{0}'
                b.save()
            else:
                b.wrong_solved_task = str(set(list_wrong))
                b.save()
        b.save()
        get_result = True
    else:
        solved_list = ReturnList(request)
        list_wrong.append(question_id)
        if not list_wrong:
            b.wrong_solved_task = '{0}'
            b.save()
        else:
            b.wrong_solved_task = str(set(list_wrong))
            b.save()

        b.save()
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


def change_question(request, question_id):

    a = get_object_or_404(Question, id = question_id)
    username = request.user
    user_question_title=a.question_title
    user_question_text=a.question_text
    user_answer_question=int(a.answer_text)
    context={'username' : username, 'question_id' : question_id, 'a' : a }
    return render(request,'mathem/edit.html',context)

def save_edit_question(request, question_id):

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

    a = get_object_or_404(Question, id = question_id)
    now=timezone.now()
    a.comment_set.create( author_name = request.user, comment_text=request.POST['text_comment'], pub_date=now)

    return HttpResponseRedirect(reverse('mathem:detail',args=(a.id,) ))


def report_error(request, question_id):


    a = get_object_or_404(Question, id = question_id)
    people_user=request.user
    time_now = timezone.now()
    people_errors = request.POST['text_error']
    visible = True

    a.peopleserrors_set.create(people_name = people_user, people_message = people_errors, date_message = time_now)

    return HttpResponseRedirect(reverse('mathem:detail',args=(a.id,)))


def views_errors(request,question_id):

    a = get_object_or_404(Question, id = question_id)
    errors_all = PeoplesErrors.objects.all()
    return render(request, 'mathem/report_errors.html', {'errors_all': errors_all})
#доп ф-я
def id_questuins(request):
    question_list_all = Question.objects.all()
    question_list_all_id = []
    for i in question_list_all:
         question_list_all_id.append(i.id)
    return question_list_all_id

def see_profile(request):



    user_name = request.user
    user_id = user_name.id
    a = get_object_or_404(Profile, id = user_id)

    list_finish_question = a.solved_task
    if list_finish_question:
        list_finish_question = list(set(TextToMass(list_finish_question)))
    else:
        list_finish_question = []

    question_list_all_id = id_questuins(request)
    question_not_finished = set(question_list_all_id) - set(list_finish_question)
    context = {'user': user_name, 'list_finish_question': list_finish_question, 'question_not_finished':question_not_finished}

    return render(request, 'mathem/profile.html',context)
