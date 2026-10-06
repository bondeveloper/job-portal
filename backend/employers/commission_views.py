from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum
from .models import EmployerUser
from .commission_models import Commission
from .commission_serializers import CommissionListSerializer, CommissionDetailSerializer


class AdminCommissionsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employer_user = EmployerUser.objects.filter(user=request.user).first()
        if not employer_user or employer_user.role != 'admin':
            return Response(
                {'error': 'Admin access required.'},
                status=status.HTTP_403_FORBIDDEN
            )

        queryset = Commission.objects.select_related('employer', 'hire_confirmation', 'hire_confirmation__application')

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

        sort = request.query_params.get('sort', '-created_at')
        if sort in ['-created_at', 'created_at', '-amount', 'amount']:
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
        total_amount = queryset.aggregate(total=Sum('amount'))['total'] or 0

        commissions = queryset[start:end]

        serializer = CommissionListSerializer(commissions, many=True)
        return Response({
            'count': total_count,
            'total_amount': float(total_amount),
            'page': page,
            'page_size': page_size,
            'results': serializer.data
        }, status=status.HTTP_200_OK)


class EmployerCommissionsListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            if employer_user.role not in ['admin', 'recruiter']:
                return Response(
                    {'error': 'Only admins and recruiters can view commissions.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            queryset = Commission.objects.filter(
                employer=employer_user.employer
            ).select_related('hire_confirmation', 'hire_confirmation__application')

            status_filter = request.query_params.get('status', '')
            if status_filter:
                queryset = queryset.filter(status=status_filter)

            sort = request.query_params.get('sort', '-created_at')
            if sort in ['-created_at', 'created_at', '-amount', 'amount']:
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

            pending_amount = queryset.filter(status='pending').aggregate(total=Sum('amount'))['total'] or 0
            invoiced_amount = queryset.filter(status='invoiced').aggregate(total=Sum('amount'))['total'] or 0
            paid_amount = queryset.filter(status='paid').aggregate(total=Sum('amount'))['total'] or 0
            total_amount = queryset.aggregate(total=Sum('amount'))['total'] or 0

            commissions = queryset[start:end]

            serializer = CommissionListSerializer(commissions, many=True)
            return Response({
                'count': total_count,
                'summary': {
                    'pending_amount': float(pending_amount),
                    'invoiced_amount': float(invoiced_amount),
                    'paid_amount': float(paid_amount),
                    'total_amount': float(total_amount),
                },
                'page': page,
                'page_size': page_size,
                'results': serializer.data
            }, status=status.HTTP_200_OK)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )
