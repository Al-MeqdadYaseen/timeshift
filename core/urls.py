from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("health/", views.health_check, name="health"),
    path("relativistic/", views.relativistic_view, name="relativistic"),
    path("save-calculation/", views.save_calculation, name="save_calculation"),
    path("gravitational/", views.gravitational_view, name="gravitational"),
    path("save-gravitational/", views.save_gravitational, name="save_gravitational"),
]
