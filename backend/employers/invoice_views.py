from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.utils import timezone
from .models import EmployerUser
from .commission_models import Commission
from .invoice_models import Invoice, InvoiceLineItem
from .invoice_serializers import InvoiceListSerializer, InvoiceDetailSerializer


class EmployerInvoicesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            if employer_user.role not in ['admin', 'recruiter']:
                return Response(
                    {'error': 'Only admins and recruiters can view invoices.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            queryset = Invoice.objects.filter(employer=employer_user.employer)

            status_filter = request.query_params.get('status', '')
            if status_filter:
                queryset = queryset.filter(status=status_filter)

            sort = request.query_params.get('sort', '-date_issued')
            if sort in ['-date_issued', 'date_issued', '-total_amount', 'total_amount']:
                queryset = queryset.order_by(sort)

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

            total_count = queryset.count()
            invoices = queryset[start:end]

            serializer = InvoiceListSerializer(invoices, many=True)
            return Response({
                'count': total_count,
                'page': page,
                'page_size': page_size,
                'results': serializer.data
            }, status=status.HTTP_200_OK)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )

    def post(self, request):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            if employer_user.role not in ['admin', 'recruiter']:
                return Response(
                    {'error': 'Only admins and recruiters can generate invoices.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            pending_commissions = Commission.objects.filter(
                employer=employer_user.employer,
                status='pending'
            )

            if not pending_commissions.exists():
                return Response(
                    {'error': 'No pending commissions to invoice.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            total_amount = pending_commissions.aggregate(total=Sum('amount'))['total']

            invoice_count = Invoice.objects.filter(employer=employer_user.employer).count()
            invoice_number = f"INV-2026-{str(invoice_count + 1).zfill(6)}"

            invoice = Invoice.objects.create(
                employer=employer_user.employer,
                invoice_number=invoice_number,
                total_amount=total_amount,
                status='issued'
            )

            for commission in pending_commissions:
                candidate_name = f"{commission.hire_confirmation.application.candidate.first_name} {commission.hire_confirmation.application.candidate.last_name}"
                job_title = commission.hire_confirmation.application.job.title
                description = f"Commission: {candidate_name} - {job_title}"

                InvoiceLineItem.objects.create(
                    invoice=invoice,
                    commission=commission,
                    description=description,
                    amount=commission.amount
                )

                commission.status = 'invoiced'
                commission.invoiced_at = timezone.now()
                commission.save()

            serializer = InvoiceDetailSerializer(invoice)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )


class EmployerInvoiceDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, invoice_id):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            invoice = Invoice.objects.get(id=invoice_id, employer=employer_user.employer)
            serializer = InvoiceDetailSerializer(invoice)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Invoice.DoesNotExist:
            return Response(
                {'error': 'Invoice not found or does not belong to your employer.'},
                status=status.HTTP_404_NOT_FOUND
            )


class AdminInvoicesListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employer_user = EmployerUser.objects.filter(user=request.user).first()
        if not employer_user or employer_user.role != 'admin':
            return Response(
                {'error': 'Admin access required.'},
                status=status.HTTP_403_FORBIDDEN
            )

        queryset = Invoice.objects.select_related('employer')

        status_filter = request.query_params.get('status', '')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        employer_id = request.query_params.get('employer_id')
        if employer_id:
            try:
                employer_id = int(employer_id)
                queryset = queryset.filter(employer__id=employer_id)
            except (ValueError, TypeError):
                pass

        sort = request.query_params.get('sort', '-date_issued')
        if sort in ['-date_issued', 'date_issued', '-total_amount', 'total_amount']:
            queryset = queryset.order_by(sort)

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

        total_count = queryset.count()
        total_revenue = queryset.aggregate(total=Sum('total_amount'))['total'] or 0

        invoices = queryset[start:end]

        serializer = InvoiceListSerializer(invoices, many=True)
        return Response({
            'count': total_count,
            'total_revenue': float(total_revenue),
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        }, status=status.HTTP_200_OK)
