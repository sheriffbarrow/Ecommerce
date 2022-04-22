from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'chat_app'
urlpatterns = [
    path('bot/', views.bot, name='bot'),
    path('post', views.ask, name='post'),
]
