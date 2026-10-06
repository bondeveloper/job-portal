from django.contrib import admin
from django.urls import path, include
from profiles.skill_views import SkillListView, CandidateSkillView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/profiles', include('profiles.urls')),
    path('api/skills', SkillListView.as_view(), name='skill-list'),
    path('api/profiles/<int:pk>/skills', CandidateSkillView.as_view(), name='candidate-skills'),
]
