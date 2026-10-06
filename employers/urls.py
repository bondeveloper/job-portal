from django.urls import path
from .views import EmployerRegisterView, EmployerProfileView

urlpatterns = [
    path('register', EmployerRegisterView.as_view(), name='employer-register'),
    path('profile', EmployerProfileView.as_view(), name='employer-profile'),
]
