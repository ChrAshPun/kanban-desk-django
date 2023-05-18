# accounts/urls.py
from django.urls import path
from .views import SignUpView, UserDeleteView, UserSettingsView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('user/<int:pk>/delete', UserDeleteView.as_view(), name='delete'),
    path('settings/', UserSettingsView.as_view(), name='settings'),
]