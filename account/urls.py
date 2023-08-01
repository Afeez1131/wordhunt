from django.urls import path

from account import views
from account.ajax import ajax_login_user, ajax_register_user

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('ajax-login-user', ajax_login_user, name='ajax_login_user'),
    path('ajax-register-user', ajax_register_user, name='ajax_register_user'),
]
