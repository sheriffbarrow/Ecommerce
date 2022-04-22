from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


from . import views
app_name = 'account'
urlpatterns = [
    path('register/', views.registration_view, name="register"),
    path('login/', views.login_view, name='login'),
    path('login-required/', views.login_view_required, name='login_required'),
    path('logout/', views.logout_view, name='logout'),
    path('update/', views.account_view, name='update'),
    path('product/history/', views.account_fitler, name='filter'),
    path('client/register/', views.registration_client_view, name='client'),
    path('settings/', views.accountSettings, name='accountsettings'),
    path('settings/', views.account_view, name='settings'),
]
