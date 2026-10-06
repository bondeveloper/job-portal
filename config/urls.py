from django.contrib import admin
from django.urls import path, include
from profiles.skill_views import SkillListView, CandidateSkillView
from profiles.work_history_views import WorkHistoryListView, WorkHistoryDetailView
from profiles.availability_views import AvailabilityView
from profiles.profile_status_views import ProfileStatusView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/profiles', include('profiles.urls')),
    path('api/skills', SkillListView.as_view(), name='skill-list'),
    path('api/profiles/<int:pk>/skills', CandidateSkillView.as_view(), name='candidate-skills'),
    path('api/profiles/<int:pk>/work-history', WorkHistoryListView.as_view(), name='work-history-list'),
    path('api/profiles/<int:pk>/work-history/<int:work_history_id>', WorkHistoryDetailView.as_view(), name='work-history-detail'),
    path('api/profiles/<int:pk>/availability', AvailabilityView.as_view(), name='availability'),
    path('api/profiles/<int:pk>/status', ProfileStatusView.as_view(), name='profile-status'),
]
