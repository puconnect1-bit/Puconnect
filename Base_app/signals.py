from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.conf import settings
import os

@receiver(post_migrate)
def update_site_domain(sender, **kwargs):
    """
    Automatically updates the Site object and cleans up SocialApp duplicates.
    """
    if sender.name == 'django.contrib.sites':
        from django.contrib.sites.models import Site
        try:
            domain = 'puconnect-jr7q.onrender.com'
            name = 'PU-Marketplace'
            site_id = getattr(settings, 'SITE_ID', 1)
            
            Site.objects.filter(id=site_id).update(domain=domain, name=name)
            if not Site.objects.filter(id=site_id).exists():
                Site.objects.create(id=site_id, domain=domain, name=name)
        except Exception:
            pass

    # Cleanup duplicate SocialApps to prevent MultipleObjectsReturned
    if sender.name == 'allauth.socialaccount':
        from allauth.socialaccount.models import SocialApp
        try:
            google_apps = SocialApp.objects.filter(provider='google')
            if google_apps.count() > 1:
                # Keep the first one, delete the rest
                first_app = google_apps.first()
                SocialApp.objects.filter(provider='google').exclude(id=first_app.id).delete()
        except Exception:
            pass
