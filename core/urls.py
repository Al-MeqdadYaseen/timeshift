from django.urls import path
from . import views

app_name = "core"
urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("health/", views.health_check, name="health"),
    path("relativistic/", views.relativistic_view, name="relativistic"),
    path("gravitational/", views.gravitational_view, name="gravitational"),
    path("save/<str:calc_type>/", views.save_calculation, name="save_calculation"),
]
