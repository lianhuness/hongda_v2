# -*- coding: UTF-8 -*-

from django.shortcuts import render

import json

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib import messages

# from .models import Article
from .forms import LoginForm
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.user.is_authenticated():
        messages.warning(request, '用户 {username}, 你已经登陆'.format(username=request.user.username))
        return HttpResponseRedirect('/')
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            messages.success(request, '欢迎回来, {username}'.format(username=request.user.username))
            return HttpResponseRedirect('/')
        else:
            messages.error(request, '账号或密码错误')
    return render(request, 'login.html', {'login_form': form})


def logout(request):
    messages.success(request, '登出成功, Bye~')
    auth.logout(request)
    return HttpResponseRedirect('/')

@permission_required('auth.change_user')
def list_users(request):
    users = User.objects.filter(is_superuser=False)
    return render(request, 'list_users.html', {'users': users})

def edit_user(request):

    return render(request, 'edit_user.html')
