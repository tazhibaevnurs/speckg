from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return [
            "pages:home",
            "catalog:list",
            "pages:faw",
            "pages:why_kg",
            "pages:services",
            "pages:about",
            "pages:documents",
            "pages:faq",
            "pages:contacts",
            "pages:privacy",
        ]

    def location(self, item):
        return reverse(item)
