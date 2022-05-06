from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from soul import models


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
    return render_to_response('matching.html', {'request': request,})

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
        type='test_type',
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
        return render_to_response('page_404.html')

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
