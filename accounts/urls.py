# accounts/urls.py
from django.urls import path
from .views import SignUpView, UserDeleteView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('user/<int:pk>/delete', UserDeleteView.as_view(), name='user_delete'),
]