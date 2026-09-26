from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.CatalogListView.as_view(), name="list"),
    path("<slug:slug>/", views.VehicleDetailView.as_view(), name="detail"),
]
