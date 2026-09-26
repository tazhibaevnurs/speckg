from django.urls import path

from . import views

app_name = "leads"

urlpatterns = [
    path("submit/", views.create_lead, name="submit"),
]
