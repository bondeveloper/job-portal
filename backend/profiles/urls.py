from django.urls import path
from .views import CandidateProfileView, CandidateProfileDetailView

urlpatterns = [
    path('', CandidateProfileView.as_view(), name='candidate-profile-create'),
    path('<int:pk>', CandidateProfileDetailView.as_view(), name='candidate-profile-detail'),
]
