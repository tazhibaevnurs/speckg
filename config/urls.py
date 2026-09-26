from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from django.views.static import serve

from catalog.sitemaps import VehicleSitemap
from pages.sitemaps import StaticSitemap

sitemaps = {
    "static": StaticSitemap,
    "vehicles": VehicleSitemap,
}

admin.site.site_header = "SPEC-KG — админка"
admin.site.site_title = "SPEC-KG"
admin.site.index_title = "Управление сайтом"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),
    path("catalog/", include("catalog.urls")),
    path("calculator/", include("calculator.urls")),
    path("leads/", include("leads.urls")),
    path("", include("pages.urls")),
]

handler404 = "pages.views.page_not_found"
handler500 = "pages.views.server_error"

urlpatterns += [
    re_path(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT},
    ),
]
