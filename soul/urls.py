from django.urls import path

from .views import home as home_views

app_name = "env_page"

urlpatterns = [
    path('', home_views.index,),
    path('index/', home_views.index,),
]