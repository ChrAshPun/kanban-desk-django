# accounts/views.py

# Standard library imports
import os

# Third-party imports
from dotenv import load_dotenv
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DeleteView, TemplateView

# Local application imports
from project.models import Project
from config.mixins import GetFirstProjectMixin

# Load environment variables
load_dotenv()

User = get_user_model()

def guest_login(request):
    # Get credentials from environment variables
    username = os.getenv('GUEST_USERNAME')
    password = os.getenv('GUEST_PASSWORD')

    # Attempt to authenticate the user
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('home')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("home")
    template_name = "accounts/templates/signup.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Sign in the user
        user = authenticate(
            self.request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)

        return response

class UserLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.username == 'guestuser':
            # guestuser is for employers to use for testing purposes
            # delete all Projects by guestuser on logout
            Project.objects.filter(owner=self.request.user).delete() 

        # Call the parent class's dispatch method to handle the actual logout process
        return super().dispatch(request, *args, **kwargs)

class UserSettingsView(GetFirstProjectMixin, TemplateView):
    template_name = "accounts/templates/user_settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_projects_count = Project.objects.filter(owner=self.request.user).count()
        context['user_projects_count'] = user_projects_count
        return context

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        logout(request)
        return super().delete(request, *args, **kwargs)