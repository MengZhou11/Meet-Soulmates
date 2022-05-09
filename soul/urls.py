from django.urls import path

from .views import home

app_name = "soul"

urlpatterns = [
    path('', home.index,),
    path('index/', home.index,),
    path('forum/', home.forum,),
    path('matching/', home.matching,),
    path('profile/', home.profile,),
    path('signup/', home.signup,),
    path('login/', home.login,),
    path('login/submit/', home.login_submit,),
    path('logout/', home.logout,),
    path('signup/error/', home.signup_error,),
    path('signup/submit/', home.signup_submit,),
    path('forum/<blog_id>', home.post_detail),
    path('post_create/',home.post_create),
    path('post_create/error/',home.post_create_error),
    path('post_create/submit/',home.post_create_submit),
    path('personality_test/',home.personality_test),
    path('personality_test/submit/',home.personality_test_submit),
]