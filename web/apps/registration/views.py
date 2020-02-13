from django.shortcuts import render,redirect
from django.shortcuts import HttpResponse
from mathem.models import Question
from django.http import Http404,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django import forms

# Create your views here.
def index(request):
    latest_question_list=Question.objects.all() #order_by

    username = 'пользователь'
    if request.user.is_authenticated:
        username = request.user
    
    context = {'user_name': username, 'latest_question_list':latest_question_list }
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
