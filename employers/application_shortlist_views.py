from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import EmployerUser
from jobs.application_models import JobApplication
from .application_shortlist_models import ApplicationShortlist
from .application_shortlist_serializers import ApplicationShortlistSerializer, AddToApplicationShortlistSerializer


class ApplicationShortlistListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            shortlist = ApplicationShortlist.objects.filter(
                employer=employer_user.employer
            ).select_related('application', 'application__candidate', 'application__job')

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

            total_count = shortlist.count()
            shortlisted = shortlist[start:end]

            serializer = ApplicationShortlistSerializer(shortlisted, many=True)
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
                    {'error': 'Only admins and recruiters can shortlist applications.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            serializer = AddToApplicationShortlistSerializer(data=request.data)
            if serializer.is_valid():
                application_id = serializer.validated_data['application_id']
                try:
                    application = JobApplication.objects.get(id=application_id)

                    if application.job.employer != employer_user.employer:
                        return Response(
                            {'error': 'Application does not belong to your employer.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    if ApplicationShortlist.objects.filter(
                        employer=employer_user.employer,
                        application=application
                    ).exists():
                        return Response(
                            {'error': 'Application is already shortlisted.'},
                            status=status.HTTP_400_BAD_REQUEST
                        )

                    shortlist = ApplicationShortlist.objects.create(
                        employer=employer_user.employer,
                        application=application
                    )

                    result_serializer = ApplicationShortlistSerializer(shortlist)
                    return Response(result_serializer.data, status=status.HTTP_201_CREATED)
                except JobApplication.DoesNotExist:
                    return Response(
                        {'error': 'Application not found.'},
                        status=status.HTTP_404_NOT_FOUND
                    )

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )


class ApplicationShortlistDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, shortlist_id):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            shortlist = ApplicationShortlist.objects.get(
                id=shortlist_id,
                employer=employer_user.employer
            )
            shortlist.delete()
            return Response({'message': 'Application removed from shortlist.'}, status=status.HTTP_204_NO_CONTENT)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except ApplicationShortlist.DoesNotExist:
            return Response(
                {'error': 'Shortlist item not found or does not belong to your employer.'},
                status=status.HTTP_404_NOT_FOUND
            )
