# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.generic import TemplateView
from project.models import Project

User = get_user_model()

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "registration/signup.html"

class UserDeleteView(generic.edit.DeleteView):
    model = User
    success_url = reverse_lazy('home')
    template_name = 'user_delete.html'

class UserSettingsView(TemplateView):
    template_name = 'user_settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_projects_count = Project.objects.filter(owner=self.request.user).count()
        context['user_projects_count'] = user_projects_count
        return context

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('home')
    else:
        return render(request, 'delete_user.html')