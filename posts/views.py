#!/usr/bin/env python
# -- coding: utf-8 --
from django.http import HttpResponse
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from posts.models import Post, UserChoice
from django.core.context_processors import csrf
from django.shortcuts import render_to_response
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def detail(request, post_id):
    template = loader.get_template('posts/base_post.html')
    context = Context({
        'post': Post.objects.get(id=post_id).position
    })
    return HttpResponse(template.render(context))

def home(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/')
    all_pos = Post.objects.all()
    template = loader.get_template('home.html')

    if request.method == 'POST':
        new_post = request.POST['choice']
        last_choice = UserChoice.objects.filter(user=request.user)
        last_choice.delete()
        new_choice = Post.objects.get(position=new_post)
        new_choice.userchoice_set.create(user=request.user, date=timezone.now())
        new_choice.save()
        context = Context({
                'posts': all_pos,
                'user': request.user
            })
        return HttpResponseRedirect(reverse('home'))
    else:
        c = {}
        c.update(csrf(request))
        context = Context({
                'posts': all_pos,
                'user': request.user
            })
        #print(render_to_response("home.html", c, context))
        return render_to_response("home.html", c, context)

def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            error = 'К сожалению, ваш аккаунт заблокирован. '
    else:
        error = 'Введенные данные некорректны.'

    template = loader.get_template('logerror.html')
    context = Context({
        'error': error
    })
    return HttpResponse(template.render(context))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def prelog(request):
    c = {}
    c.update(csrf(request))
    context = Context({
    })
    return render_to_response('login.html', c, context)

def prereg(request):
    c = {}
    c.update(csrf(request))
    context = Context({
    })
    return render_to_response('registration.html', c, context)

def registration_view(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
    user = authenticate(username=username, password=password)
    login(request, user)
    return HttpResponseRedirect(reverse('home'))