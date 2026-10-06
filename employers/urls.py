from django.urls import path
from .views import EmployerRegisterView, EmployerProfileView
from .team_views import TeamMembersListView, TeamMemberDetailView
from .job_views import JobListCreateView, JobDetailView
from .job_management_views import JobPublishView, JobCloseView, JobUnpublishView, JobMetricsView
from .candidate_search_views import CandidateSearchView

urlpatterns = [
    path('register', EmployerRegisterView.as_view(), name='employer-register'),
    path('profile', EmployerProfileView.as_view(), name='employer-profile'),
    path('team-members', TeamMembersListView.as_view(), name='team-members-list'),
    path('team-members/<int:member_id>', TeamMemberDetailView.as_view(), name='team-member-detail'),
]

urlpatterns += [
    path('jobs', JobListCreateView.as_view(), name='job-list-create'),
    path('jobs/<int:job_id>', JobDetailView.as_view(), name='job-detail'),
    path('jobs/<int:job_id>/publish', JobPublishView.as_view(), name='job-publish'),
    path('jobs/<int:job_id>/close', JobCloseView.as_view(), name='job-close'),
    path('jobs/<int:job_id>/unpublish', JobUnpublishView.as_view(), name='job-unpublish'),
    path('jobs/<int:job_id>/metrics', JobMetricsView.as_view(), name='job-metrics'),
    path('candidates/search', CandidateSearchView.as_view(), name='candidate-search'),
]
