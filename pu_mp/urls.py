"""
Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Base app (includes: home, about, help, terms, privacy, safety, contact)
    path('', include('Base_app.urls')),

    # Authentication
    path('auth/', include('Auth_app.urls')),
    
    # Main apps
    path('dashboard/', include('dash_app.urls')),
    path('listings/', include('Listings_app.urls')),
    path('profile/', include('Profile_app.urls')),
    path('chat/', include('chat_app.urls')),
    path('search/', include('search_app.urls')),
    path("accounts/", include("allauth.urls")),# Include allauth URLs for social authentication
    
]
# Media & Static files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)