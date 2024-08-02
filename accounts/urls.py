# accounts/urls.py
from django.urls import path
from .views import guest_login, UserLogoutView, SignUpView, UserSettingsView, UserDeleteView

app_name = 'accounts'

urlpatterns = [
    path('guest-login/', guest_login, name='guest-login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('settings/', UserSettingsView.as_view(), name='settings'),
    path('delete/', UserDeleteView.as_view(), name='delete'),
]