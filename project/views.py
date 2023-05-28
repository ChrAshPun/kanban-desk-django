from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.text import slugify
from .models import Project, Task
from config.mixins import GetFirstProjectMixin
from django.shortcuts import get_object_or_404

class ProjectCreateView(LoginRequiredMixin, GetFirstProjectMixin, CreateView):
    model = Project
    template_name='project_create.html'
    fields = ['name', 'description']

    def get_success_url(self):
        return reverse_lazy('project:kanban', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['name', 'description']

    def get_success_url(self):
        return reverse_lazy('project:settings', kwargs={'pk': self.object.pk})

class ProjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('project:create')

class ProjectKanbanView(LoginRequiredMixin, GetFirstProjectMixin, DetailView):
    model = Project
    template_name='project_kanban.html'
    context_object_name = 'project'

    def get_object(self, queryset=None):
        if 'pk' not in self.kwargs:
            first_project = self.request.context_data.get('first_project')
            if first_project != -1:
                return first_project # object
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        projects = Project.objects.filter(owner=user)
        context['projects'] = projects # for the projects-sidebar

        project = self.object 
        try:
            tasks = Task.objects.filter(project=project)
        except:
            tasks = []
        context['tasks'] = tasks
        return context

class ProjectSettingsView(LoginRequiredMixin, GetFirstProjectMixin, DetailView):
    model = Project
    template_name='project_settings.html'

    def get_object(self, queryset=None):
        if 'pk' not in self.kwargs:
            first_project = self.request.context_data.get('first_project')
            if first_project != -1:
                return first_project
        return super().get_object(queryset)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        projects = Project.objects.filter(owner=user)
        context['projects'] = projects
        return context

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['name', 'description', 'priority', 'status']
    project_pk = None  # save current project pk

    def get_success_url(self):
        return reverse_lazy('project:kanban', kwargs={'pk': self.project_pk})

    def form_valid(self, form):
        project = Project.objects.get(pk=self.kwargs['project_pk'])  # Use project_pk
        task_count = project.tasks.count()
        task_id = f'{project.name[:2].upper()}-{task_count + 1:02d}'
        form.instance.task_id = task_id
        form.instance.project = project
        self.project_pk = self.kwargs['project_pk']  # Use project_pk
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['name', 'description', 'priority', 'status']

    def get_object(self, queryset=None):
        task_pk = self.kwargs.get('task_pk')  # Get the task_pk from URL
        return get_object_or_404(Task, pk=task_pk)

    def get_success_url(self):
        project_pk = self.kwargs.get('project_pk') 
        return reverse_lazy('project:kanban', kwargs={'pk': project_pk})

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    
    def get_object(self, queryset=None):
        task_pk = self.kwargs.get('task_pk')  # Get the task_pk from URL
        return get_object_or_404(Task, pk=task_pk)

    def get_success_url(self):
        project_pk = self.kwargs.get('project_pk') 
        return reverse_lazy('project:kanban', kwargs={'pk': project_pk})