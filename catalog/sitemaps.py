from django.contrib.sitemaps import Sitemap

from .models import Vehicle


class VehicleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Vehicle.objects.filter(is_published=True)

    def lastmod(self, obj):
        return obj.updated_at
