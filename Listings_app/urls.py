from django.urls import path
from . import views

app_name = 'listings'

urlpatterns = [
    path('listings/', views.listings, name='listings'),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('create/', views.create_listing, name='create'),
    # 1. The "Save" Handshake: Matches fetch('/listings/api/create/')
    # This receives the Cloudinary URL string and form data
    path('api/create/', views.create_listing_api, name='create_api'),

    # 2. The "Pull" Handshake: Matches fetch('/listings/api/me/')
    path('api/me/', views.get_my_listings, name='my_listings_api'),
    path('api/all/', views.get_all_listings, name='all_listings_api'),
    
    # 3. Management Actions
    path('api/delete/<int:listing_id>/', views.delete_listing_api, name='delete_api'),
    path('api/toggle-status/<int:listing_id>/', views.toggle_listing_status_api, name='toggle_status_api'),
    
    # 4. Page Routes: To serve the actual HTML files
    
]
