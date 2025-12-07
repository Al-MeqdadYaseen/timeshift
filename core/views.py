from django.http import JsonResponse
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "core/home.html"


def health_check(request):
    return JsonResponse({"status": "ok"})


# Create your views here.
