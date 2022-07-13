from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from . import views

urlpatterns = [
    path('login/', views.login, name='login'), # /accounts/login/ => settings.LOGIN_URL의 설정값도 해당 문자열
    path('logout/', views.logout, name='logout'),
    path(
        "password_change/", views.password_change, name="password_change"
    ),
    path('signup/', views.signup, name='signup'),
    path('edit/', views.profile_edit, name='profile_edit'),

]