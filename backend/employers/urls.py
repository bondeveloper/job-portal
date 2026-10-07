from django.urls import path
from .views import EmployerRegisterView, EmployerProfileView
from .team_views import TeamMembersListView, TeamMemberDetailView
from .job_views import JobListCreateView, JobDetailView
from .job_management_views import JobPublishView, JobCloseView, JobUnpublishView, JobMetricsView
from .candidate_search_views import CandidateSearchView
from .shortlist_views import ShortlistListView, ShortlistDetailView
from .application_review_views import EmployerApplicationsListView, EmployerApplicationDetailView
from .application_shortlist_views import ApplicationShortlistListView, ApplicationShortlistDetailView
from .hire_confirmation_views import MarkApplicationHiredView
from .commission_views import AdminCommissionsListView, EmployerCommissionsListView
from .invoice_views import EmployerInvoicesListView, EmployerInvoiceDetailView, AdminInvoicesListView
from .payment_views import InitiatePaymentView, PaymentCallbackView, EmployerPaymentsListView, AdminPaymentsListView
from .analytics_views import RevenueAnalyticsView, CommissionMetricsView, PaymentReconciliationView, DisputeManagementView

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
    path('shortlist', ShortlistListView.as_view(), name='shortlist-list'),
    path('shortlist/<int:shortlist_id>', ShortlistDetailView.as_view(), name='shortlist-detail'),
    path('applications', EmployerApplicationsListView.as_view(), name='applications-list'),
    path('applications/<int:application_id>', EmployerApplicationDetailView.as_view(), name='application-detail'),
    path('applications/<int:application_id>/mark-hired', MarkApplicationHiredView.as_view(), name='mark-hired'),
    path('application-shortlist', ApplicationShortlistListView.as_view(), name='application-shortlist-list'),
    path('application-shortlist/<int:shortlist_id>', ApplicationShortlistDetailView.as_view(), name='application-shortlist-detail'),
    path('commissions', EmployerCommissionsListView.as_view(), name='commissions-list'),
    path('invoices', EmployerInvoicesListView.as_view(), name='invoices-list'),
    path('invoices/<int:invoice_id>', EmployerInvoiceDetailView.as_view(), name='invoice-detail'),
    path('invoices/<int:invoice_id>/pay', InitiatePaymentView.as_view(), name='initiate-payment'),
    path('payments', EmployerPaymentsListView.as_view(), name='payments-list'),
]

admin_urlpatterns = [
    path('admin/commissions', AdminCommissionsListView.as_view(), name='admin-commissions-list'),
    path('admin/invoices', AdminInvoicesListView.as_view(), name='admin-invoices-list'),
    path('admin/payments', AdminPaymentsListView.as_view(), name='admin-payments-list'),
    path('admin/analytics/revenue', RevenueAnalyticsView.as_view(), name='revenue-analytics'),
    path('admin/analytics/commissions', CommissionMetricsView.as_view(), name='commission-metrics'),
    path('admin/reconciliation', PaymentReconciliationView.as_view(), name='payment-reconciliation'),
    path('admin/disputes', DisputeManagementView.as_view(), name='disputes-list'),
    path('admin/commissions/<int:commission_id>/dispute', DisputeManagementView.as_view(), name='mark-disputed'),
]

webhook_urlpatterns = [
    path('webhooks/payment-callback', PaymentCallbackView.as_view(), name='payment-callback'),
]

urlpatterns += admin_urlpatterns + webhook_urlpatterns
