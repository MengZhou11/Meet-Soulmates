from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.db.models import Q
from soul import models
import joblib
import pandas as pd


'''提交表单必须加csrf'''
# Create your views here.

@csrf_exempt
def index(request):
    return render_to_response('index.html', {'request': request,})

@csrf_exempt
def forum(request):
    blogs = models.Blog.objects.order_by('-create_date')
    blogs2 = blogs[6:12]
    blogs = blogs[0:6]
    return render_to_response('forum.html', {'request': request,
                                             'blogs': blogs,
                                             'blogs2': blogs2,})

@csrf_exempt
def post_detail(request, blog_id):
    blog = models.Blog.objects.get(id=blog_id)
    return render_to_response('post_detail.html', {'request': request,
                                                   'blog': blog,})

@csrf_exempt
def post_create(request):
    if request.user.is_active:
        return render_to_response('post_create.html', {'request': request,})
    else:
        return redirect('/signup')

@csrf_exempt
def post_create_submit(request):
    if not request.user.is_active:
        return redirect('/signup')
    if request.POST.get('subject') == "" or request.POST.get('content') == "":
        return redirect('/post_create/error')
    profile = models.Profile.objects.get(email=request.user.username)
    new_post = models.Blog(
        user=profile.first_name + " " + profile.last_name,
        subject=request.POST.get('subject'),
        content=request.POST.get('content'),
        create_date=timezone.now(),
    )
    new_post.save()
    return redirect('/forum/' + str(new_post.id))

@csrf_exempt
def post_create_error(request):
    return render_to_response('post_create.html', {'error': "Subject or context is empty",})

@csrf_exempt
def matching(request):
    if request.user.is_active:
        profile = models.Profile.objects.get(email=request.user.username)
        if profile.type == 'unknown':
            return redirect('/personality_test')
        matching_list = models.Profile.objects.filter(type=profile.type).filter(~Q(email=request.user.username)).order_by('?')
        if len(matching_list) == 0:
            matching_list = models.Profile.objects.filter(~Q(email=request.user.username)).order_by('?')
        if len(matching_list) == 0:
            first_name = 'You'
            last_name = 'Are'
            email = 'The Only'
            persona = 'User'
        else:
            user = matching_list[0]
            first_name = user.first_name
            last_name = user.last_name
            email = user.email
            persona = user.type

        return render_to_response('matching.html', {'f_name': first_name,
                                                   'l_name': last_name,
                                                   'email': email,
                                                   'type': persona,
                                                   'request': request,})
    else:
        return redirect('/signup')

@csrf_exempt
def profile(request):
    if request.user.is_active:
        profile = models.Profile.objects.get(email=request.user.username)
        return render_to_response('profile.html', {'f_name': profile.first_name,
                                                   'l_name': profile.last_name,
                                                   'email': profile.email,
                                                   'type': profile.type,
                                                   'request': request,})
    else:
        return redirect('/signup')

@csrf_exempt
def signup(request):
    return render_to_response('signup.html', {'request': request,})

@csrf_exempt
def login(request):
    return render_to_response('login.html', {'request': request,})


@csrf_exempt
def signup_submit(request):
    if request.POST.get('password') != request.POST.get('password2'):
        return redirect('/signup/error')
    User.objects.create_user(username=request.POST.get('email'), password=request.POST.get('password'))
    user = auth.authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
    new_profile = models.Profile(
        first_name=request.POST.get('first_name'),
        last_name=request.POST.get('last_name'),
        type='unknown',
        email=request.POST.get('email'),
        update_date=timezone.now(),
        create_date=timezone.now(),
    )
    new_profile.save()

    if user is not None and user.is_active:
        auth.login(request, user)
        return redirect('/index')
    else:
        return render_to_response('page_404.html')

@csrf_exempt
def login_submit(request):
    user = auth.authenticate(username=request.POST.get('email'), password=request.POST.get('password'))
    if user is not None and user.is_active:
        auth.login(request, user)
        return redirect('/index')
    else:
        return render_to_response('login.html', {'error': "Password not match",})

@csrf_exempt
def personality_test(request):
    if request.user.is_active:
        return render_to_response('personality_test.html', {'request': request,})
    else:
        return redirect('/signup')

@csrf_exempt
def personality_test_submit(request):
    if request.user.is_active:
        profile = models.Profile.objects.get(email=request.user.username)
        EXT = []
        EST = []
        AGR = []
        CSN = []
        OPN = []
        for i in range(1, 11):
            if request.POST.get('EXT' + str(i)):
                EXT.append(request.POST.get('EXT' + str(i)))
            else:
                EXT.append('0')

            if request.POST.get('EST' + str(i)):
                EST.append(request.POST.get('EST' + str(i)))
            else:
                EST.append('0')

            if request.POST.get('AGR' + str(i)):
                AGR.append(request.POST.get('AGR' + str(i)))
            else:
                AGR.append('0')

            if request.POST.get('CSN' + str(i)):
                CSN.append(request.POST.get('CSN' + str(i)))
            else:
                CSN.append('0')

            if request.POST.get('OPN' + str(i)):
                OPN.append(request.POST.get('OPN' + str(i)))
            else:
                OPN.append('0')
        profile.EXT = ";".join(EXT)
        profile.EST = ";".join(EST)
        profile.AGR = ";".join(AGR)
        profile.CSN = ";".join(CSN)
        profile.OPN = ";".join(OPN)
        l = {}
        for i,v in enumerate(EXT):
            l['EXT' + str(i + 1)] = [v]
        for i,v in enumerate(EST):
            l['EST' + str(i + 1)] = [v]
        for i,v in enumerate(AGR):
            l['AGR' + str(i + 1)] = [v]
        for i,v in enumerate(CSN):
            l['CSN' + str(i + 1)] = [v]
        for i,v in enumerate(OPN):
            l['OPN' + str(i + 1)] = [v]
        input = pd.DataFrame(l)
        model = joblib.load('soul/my_model.pkl')
        profile.type = model.predict(input)[0]
        print(profile.type)
        profile.save()
        return redirect('/profile')
    else:
        return redirect('/signup')

@csrf_exempt
def signup_error(request):
    return render_to_response('signup.html', {'error': "Password not match",})

@csrf_exempt
def logout(request):
    auth.logout(request)
    return redirect('/index')


@csrf_exempt
def error(request):
    return render_to_response('page_404.html')
