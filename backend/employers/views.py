from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from accounts.models import SessionToken
from django.utils import timezone
from datetime import timedelta
import secrets
from .models import Employer, EmployerUser
from .serializers import EmployerRegistrationSerializer, EmployerProfileSerializer


class EmployerRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = EmployerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            user = result['user']

            token = secrets.token_urlsafe(32)
            expires_at = timezone.now() + timedelta(days=30)
            SessionToken.objects.create(
                user=user,
                token=token,
                expires_at=expires_at
            )

            return Response({
                'message': 'Employer account created successfully.',
                'user_id': user.id,
                'email': user.email,
                'token': token
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            employer_user = EmployerUser.objects.get(user=request.user)
            employer = employer_user.employer
            serializer = EmployerProfileSerializer(employer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except EmployerUser.DoesNotExist:
            return Response(
                {'error': 'Employer not found for this user.'},
                status=status.HTTP_404_NOT_FOUND
            )
