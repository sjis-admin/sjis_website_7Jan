from .models import SiteConfiguration, PopupAnnouncement

def site_configuration(request):
    try:
        config = SiteConfiguration.objects.first()
        # Get the latest active popup
        popup = PopupAnnouncement.objects.filter(is_active=True).first()
    except:
        config = None
        popup = None
    return {
        'site_config': config,
        'active_popup': popup
    }
