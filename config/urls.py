"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from project.models import Project

def redirect_view(request):
    first_project = Project.objects.filter(owner=request.user).first()
    if first_project:
        return redirect('project:kanban', pk=first_project.pk)
    else:
        return redirect('project:create') 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('', redirect_view, name='home'), 
    path("accounts/", include("accounts.urls", namespace="accounts")),  
    path("project/", include("project.urls", namespace="project")),  
]