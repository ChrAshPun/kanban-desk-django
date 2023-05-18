from http.client import HTTPResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Project

class ProjectCreateView(CreateView):
  model = Project
  template_name = "project_create.html"
  fields = ['name', 'description']
