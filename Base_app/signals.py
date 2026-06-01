from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings
import os

@receiver(post_migrate)
def update_site_domain(sender, **kwargs):
    """
    Automatically updates the Site object to match the current production domain.
    This is required for reliable Google Social Auth redirects.
    """
    if sender.name == 'django.contrib.sites':
        from django.contrib.sites.models import Site
        
        # Determine the domain from environment or settings
        # On Render, we can use ALLOWED_HOSTS or a custom env var
        domain = 'puconnect-jr7q.onrender.com'
        name = 'PU-Marketplace'
        
        site_id = getattr(settings, 'SITE_ID', 1)
        
        Site.objects.filter(id=site_id).update(domain=domain, name=name)
        # Ensure it exists if not present
        if not Site.objects.filter(id=site_id).exists():
            Site.objects.create(id=site_id, domain=domain, name=name)
