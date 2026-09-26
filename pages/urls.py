from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("faw/", views.FAWView.as_view(), name="faw"),
    path("pochemu-kyrgyzstan/", views.WhyKGView.as_view(), name="why_kg"),
    path("uslugi/", views.ServicesView.as_view(), name="services"),
    path("o-kompanii/", views.AboutView.as_view(), name="about"),
    path("dokumenty/", views.DocumentsView.as_view(), name="documents"),
    path("faq/", views.FAQView.as_view(), name="faq"),
    path("kontakty/", views.ContactsView.as_view(), name="contacts"),
    path("politika-konfidencialnosti/", views.PrivacyView.as_view(), name="privacy"),
]
