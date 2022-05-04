from django.urls import path

from .views import home

app_name = "soul"

urlpatterns = [
    path('', home.index,),
    path('index/', home.index,),
    path('blog/', home.blog,),
    path('matching/', home.matching,),
    path('profile/', home.profile,),
    path('signup/', home.signup,),
    path('login/', home.login,),
    path('login/submit/', home.login_submit,),
    path('logout/', home.logout,),
    path('signup/error/', home.signup_error,),
    path('signup/submit/', home.signup_submit,),
]