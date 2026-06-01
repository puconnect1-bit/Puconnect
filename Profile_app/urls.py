from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('complete/', views.complete_profile, name='complete_profile'),
     # The API endpoints used by the JS
    path('api/profile/me/', views.get_my_profile, name='get_my_profile'),
    path('api/profile/update/', views.update_profile_api, name='update_profile'),
    
    # ... your existing paths ...
    path('logout/', views.logout_view, name='logout'),
    path('deactivate/', views.deactivate_account, name='deactivate_account'),
    path('delete-account/', views.delete_account, name='delete_account'),
]

