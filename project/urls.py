from django.urls import path
from django.http import HttpResponse
from .views import ProjectCreateView
from django.shortcuts import redirect

app_name = 'project'

def test(request):
  return HttpResponse("<h1>Projects View</h1>")

urlpatterns = [
  path('new/', ProjectCreateView.as_view(), name='create'),
  path('', test, name='view'),
  # path('project/new/', ProjectCreateView.as_view(), name='project_create'),
]