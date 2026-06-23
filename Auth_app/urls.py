
from django.urls import path
from . import views

app_name = 'auth'

urlpatterns = [
    path('auth/api/login/', views.login_view, name='api_login'),
    path('auth-view', views.Auth_view, name='auth_view'),
    path('auth/api/signup/', views.signup_api, name='api_signup'),
    path('logout/', views.logout_view, name='logout'),
]