from django.urls import path
from vendorprofile import views

app_name = 'vendorprofile'
urlpatterns = [
    path('home',views.index,name="home"),
    path('help',views.help,name="help"),
    ]
