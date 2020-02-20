from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from mathem.models import Question, Profile
from django.http import Http404,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django import forms
from django.shortcuts import get_object_or_404

#Преобразует строку в массив целых чисел - ВСПОМАГАТЕЛЬНАЯ ФУНКЦИЯ
def TextToMass(s):
    s = s.replace('{','')
    s = s.replace('}','')

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
            solved_list = TextToMass(list)
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
        if b.wrong_solved_task:
            list_wrong = b.wrong_solved_task
            list_wrong = TextToMass(list_wrong)
        else:
            list_wrong = []
    else:
        list_wrong = []
    return list_wrong
# Create your views here.
def index(request):
    latest_question_list=Question.objects.all() #order_by

    username = 'пользователь'
    if request.user.is_authenticated:
        username = request.user
        user_id = username.id
        a = get_object_or_404(Profile, id = user_id)
        list_finish_question = a.solved_task
        list_false_finished_question = a.wrong_solved_task
        if list_finish_question:
            list_finish_question = TextToMass(list_finish_question)
        else:
            list_finish_question = []

        if list_false_finished_question:
            list_false_finished_question = TextToMass(list_false_finished_question)
        else:
            list_false_finished_question = []
    else:
        list_finish_question = []
        list_false_finished_question = []

    context = {'user_name': username, 'latest_question_list':latest_question_list, 'list_finish_question': list_finish_question,
    'list_false_finished_question':list_false_finished_question }
    return render(request, 'registration/index.html', context)



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        email = request.POST.get('email')
        if User.objects.filter(email=email):
            #messages.error(request, 'Пользователь с таким E-MAIL уже зарегестрирован!')
            form.add_error('email', "Some message")
        if form.is_valid():
            ins = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            user = authenticate(username=username, password=password, email=email)
            ins.email = email
            ins.save()
            form.save_m2m()
            #messages.success(request, 'Вы успешно зарегестрировались!')

            login(request, user)
            #return render(request,'registration/index.html')
            return redirect('..')
    else:
        form = UserRegisterForm()

    context = {'form':form }

    return render(request, 'registration/reg.html', context)

    def it_is_admin(request):
        username=request.user
        if str(username)=='admin':
            is_admin = True
        else:
            is_admin = False
        return is_admin
