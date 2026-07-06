from django.urls import path
from . import views

app_name = "monitoring"

urlpatterns = [
    path("", views.stations_list, name="stations_list"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("station/<int:pk>/", views.station_detail, name="station_detail"),
]
