from django.urls import path
from .views import EmployerRegisterView, EmployerProfileView
from .team_views import TeamMembersListView, TeamMemberDetailView

urlpatterns = [
    path('register', EmployerRegisterView.as_view(), name='employer-register'),
    path('profile', EmployerProfileView.as_view(), name='employer-profile'),
    path('team-members', TeamMembersListView.as_view(), name='team-members-list'),
    path('team-members/<int:member_id>', TeamMemberDetailView.as_view(), name='team-member-detail'),
]
