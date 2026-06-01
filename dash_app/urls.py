from django.urls import path
from . import views


app_name = 'Dash_app'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('services/', views.dashboard_services, name='dashboard_services'),
    path('products/', views.dashboard_products, name='dashboard_products'),
]