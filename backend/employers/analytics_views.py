from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Count, Q, Avg
from django.utils import timezone
from datetime import timedelta
from .models import EmployerUser
from .commission_models import Commission
from .invoice_models import Invoice
from .payment_models import Payment
from .commission_audit_models import CommissionDispute


class RevenueAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employer_user = EmployerUser.objects.filter(user=request.user).first()
        if not employer_user or employer_user.role != 'admin':
            return Response(
                {'error': 'Admin access required.'},
                status=status.HTTP_403_FORBIDDEN
            )

        all_commissions = Commission.objects.all()

        total_revenue = all_commissions.aggregate(total=Sum('amount'))['total'] or 0
        pending_revenue = all_commissions.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0
        invoiced_revenue = all_commissions.filter(status='invoiced').aggregate(total=Sum('amount'))['total'] or 0
        paid_revenue = all_commissions.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0

        now = timezone.now()
        this_month_start = now.replace(day=1)
        this_year_start = now.replace(month=1, day=1)

        this_month_paid = all_commissions.filter(
            status='paid',
            paid_at__gte=this_month_start
        ).aggregate(total=Sum('amount'))['total'] or 0

        this_year_paid = all_commissions.filter(
            status='paid',
            paid_at__gte=this_year_start
        ).aggregate(total=Sum('amount'))['total'] or 0

        top_employers = []
        employer_groups = all_commissions.values('employer__name', 'employer__id').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')[:5]

        for group in employer_groups:
            top_employers.append({
                'employer_id': group['employer__id'],
                'employer_name': group['employer__name'],
                'total_amount': float(group['total']),
                'commission_count': group['count']
            })

        return Response({
            'total_revenue': float(total_revenue),
            'pending_revenue': float(pending_revenue),
            'invoiced_revenue': float(invoiced_revenue),
            'paid_revenue': float(paid_revenue),
            'this_month_paid': float(this_month_paid),
            'this_year_paid': float(this_year_paid),
            'top_employers': top_employers
        }, status=status.HTTP_200_OK)


class CommissionMetricsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employer_user = EmployerUser.objects.filter(user=request.user).first()
        if not employer_user or employer_user.role != 'admin':
            return Response(
                {'error': 'Admin access required.'},
                status=status.HTTP_403_FORBIDDEN
            )

        all_commissions = Commission.objects.all()

        total_count = all_commissions.count()
        pending_count = all_commissions.filter(status='pending').count()
        invoiced_count = all_commissions.filter(status='invoiced').count()
        paid_count = all_commissions.filter(status='paid').count()
        disputed_count = all_commissions.filter(status='disputed').count()

        total_amount = all_commissions.aggregate(total=Sum('amount'))['total'] or 0
        average_amount = all_commissions.aggregate(avg=Avg('amount'))['avg'] or 0

        return Response({
            'total_commissions': total_count,
            'by_status': {
                'pending': pending_count,
                'invoiced': invoiced_count,
                'paid': paid_count,
                'disputed': disputed_count,
            },
            'total_amount': float(total_amount),
            'average_amount': float(average_amount),
            'rate_distribution': {
                '10%': all_commissions.filter(rate=10.00).count(),
                '15%': all_commissions.filter(rate=15.00).count(),
                'other': all_commissions.exclude(rate__in=[10.00, 15.00]).count(),
            }
        }, status=status.HTTP_200_OK)


class PaymentReconciliationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employer_user = EmployerUser.objects.filter(user=request.user).first()
        if not employer_user or employer_user.role != 'admin':
            return Response(
                {'error': 'Admin access required.'},
                status=status.HTTP_403_FORBIDDEN
            )

        all_invoices = Invoice.objects.all()

        issued_amount = all_invoices.filter(status__in=['issued', 'partially_paid']).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

        completed_payments = Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0

        outstanding_amount = float(issued_amount) - float(completed_payments)

        overdue_invoices = all_invoices.filter(
            status__in=['issued', 'partially_paid'],
            due_date__lt=timezone.now()
        ).count()

        failed_payments = Payment.objects.filter(status='failed').count()

        return Response({
            'expected_payments': float(issued_amount),
            'received_payments': float(completed_payments),
            'outstanding_amount': outstanding_amount,
            'overdue_invoices': overdue_invoices,
            'failed_payments': failed_payments,
            'reconciliation_status': 'balanced' if outstanding_amount == 0 else 'outstanding'
        }, status=status.HTTP_200_OK)


class DisputeManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employer_user = EmployerUser.objects.filter(user=request.user).first()
        if not employer_user or employer_user.role != 'admin':
            return Response(
                {'error': 'Admin access required.'},
                status=status.HTTP_403_FORBIDDEN
            )

        disputes = CommissionDispute.objects.select_related('commission', 'resolved_by')

        status_filter = request.query_params.get('status', '')
        if status_filter:
            disputes = disputes.filter(status=status_filter)

        page = request.query_params.get('page', 1)
        try:
            page = int(page)
            if page < 1:
                page = 1
        except (ValueError, TypeError):
            page = 1

        page_size = 20
        start = (page - 1) * page_size
        end = start + page_size

        total_count = disputes.count()
        dispute_list = disputes[start:end]

        results = []
        for dispute in dispute_list:
            results.append({
                'id': dispute.id,
                'commission_id': dispute.commission.id,
                'amount': float(dispute.commission.amount),
                'status': dispute.status,
                'reason': dispute.reason,
                'created_at': dispute.created_at,
                'resolved_at': dispute.resolved_at,
                'resolved_by': dispute.resolved_by.email if dispute.resolved_by else None
            })

        return Response({
            'count': total_count,
            'page': page,
            'page_size': page_size,
            'results': results
        }, status=status.HTTP_200_OK)

    def post(self, request, commission_id):
        employer_user = EmployerUser.objects.filter(user=request.user).first()
        if not employer_user or employer_user.role != 'admin':
            return Response(
                {'error': 'Admin access required.'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            commission = Commission.objects.get(id=commission_id)
            reason = request.data.get('reason', '')

            if not reason:
                return Response(
                    {'error': 'Reason is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if hasattr(commission, 'dispute'):
                return Response(
                    {'error': 'Commission already has an open dispute'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            dispute = CommissionDispute.objects.create(
                commission=commission,
                reason=reason,
                status='open'
            )

            commission.status = 'disputed'
            commission.save()

            return Response({
                'id': dispute.id,
                'commission_id': commission.id,
                'status': dispute.status,
                'reason': dispute.reason
            }, status=status.HTTP_201_CREATED)
        except Commission.DoesNotExist:
            return Response(
                {'error': 'Commission not found'},
                status=status.HTTP_404_NOT_FOUND
            )
