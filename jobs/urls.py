from django.urls import path
from .views import JobSearchView
from .application_views import ApplyToJobView, MyApplicationsListView, MyApplicationDetailView

urlpatterns = [
    path('search', JobSearchView.as_view(), name='job-search'),
    path('<int:job_id>/apply', ApplyToJobView.as_view(), name='apply-to-job'),
    path('my-applications', MyApplicationsListView.as_view(), name='my-applications-list'),
    path('my-applications/<int:application_id>', MyApplicationDetailView.as_view(), name='my-application-detail'),
]
