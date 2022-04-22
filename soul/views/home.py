from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.auth.models import User


'''提交表单必须加csrf'''
# Create your views here.

@csrf_exempt
def index(request):
    return render_to_response('index.html')


@csrf_exempt
def login(request):
    return render_to_response('login.html')


@csrf_exempt
def signup(request):
    User.objects.create_user(username=request.POST.get('username'), password=request.POST.get('password'))
    return redirect('/login')


@csrf_exempt
def logout(request):
    auth.logout(request)
    return redirect('/login')


@csrf_exempt
def error(request):
    return render_to_response('page_404.html')
