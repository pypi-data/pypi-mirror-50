from django.shortcuts import render
from django.http import HttpResponse
from hello.forms import ProjectForm
from hello.models import Project
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page


# Create your views here.

# CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# # @cache_page(CACHE_TTL)
def hello_world(request, *args, **kwargs):
    # return HttpResponse("<h1>hello world</h1>")
    
    return render(request, "hello_world.html")


def project_views(request):
    context = {}
    context["objects"] = Project.objects.all()
    return render(request, "project/project.html", context)


def project_create_view(request):
    form = ProjectForm(request.POST or None)
    return render(request, "project/project_create.html", {})

