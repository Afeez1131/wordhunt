from django.urls import path

from account import views
from account.ajax import ajax_login_user

app_name = 'accounts'
urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('ajax-verify-username', ajax_login_user, name='ajax_login_user'),
]
