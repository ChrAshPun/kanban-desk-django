from django.urls import path
from django.http import HttpResponse
# from .views import ProjectCreateView
from django.shortcuts import redirect

def project_page(request):
  # if request.user.is_authenticated:
    return HttpResponse('<h1>Project Page</h1>')
  # else:
    # return redirect('login')

urlpatterns = [
  path('', project_page, name='project_view'),
  # path('project/new/', ProjectCreateView.as_view(), name='project_create'),
]