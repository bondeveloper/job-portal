import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Employer, EmployerUser
from accounts.models import SessionToken


@pytest.mark.django_db
class TestEmployerRegistration:
    def setup_method(self):
        self.client = APIClient()

    def test_employer_registration_success(self):
        data = {
            'email': 'employer@example.com',
            'password': 'SecurePass123',
            'company_name': 'TechCorp',
            'location': 'Johannesburg',
            'industry': 'Technology',
            'company_size': '11-50'
        }
        response = self.client.post('/api/employer/register', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == 'employer@example.com'
        assert 'token' in response.data
        assert User.objects.filter(email='employer@example.com').exists()
        assert Employer.objects.filter(name='TechCorp').exists()
        employer_user = EmployerUser.objects.get(user__email='employer@example.com')
        assert employer_user.role == 'admin'

    def test_employer_registration_duplicate_email(self):
        User.objects.create_user(email='existing@example.com', username='existing@example.com', password='Pass123')

        data = {
            'email': 'existing@example.com',
            'password': 'SecurePass123',
            'company_name': 'TechCorp',
            'location': 'Johannesburg'
        }
        response = self.client.post('/api/employer/register', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'Email already registered' in str(response.data)

    def test_employer_registration_invalid_password(self):
        data = {
            'email': 'employer@example.com',
            'password': '123456789',
            'company_name': 'TechCorp',
            'location': 'Johannesburg'
        }
        response = self.client.post('/api/employer/register', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_employer_registration_short_password(self):
        data = {
            'email': 'employer@example.com',
            'password': 'Pass12',
            'company_name': 'TechCorp',
            'location': 'Johannesburg'
        }
        response = self.client.post('/api/employer/register', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_employer_registration_missing_required_fields(self):
        data = {
            'email': 'employer@example.com',
            'password': 'SecurePass123',
        }
        response = self.client.post('/api/employer/register', data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestEmployerProfile:
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='employer@example.com',
            username='employer@example.com',
            password='SecurePass123'
        )
        self.employer = Employer.objects.create(
            name='TechCorp',
            location='Johannesburg',
            industry='Technology'
        )
        self.employer_user = EmployerUser.objects.create(
            user=self.user,
            employer=self.employer,
            role='admin'
        )
        self.token = SessionToken.objects.create(
            user=self.user,
            token='test-token-123',
            expires_at='2099-12-31T23:59:59Z'
        )

    def test_get_employer_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer test-token-123')
        response = self.client.get('/api/employer/profile')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == 'TechCorp'
        assert response.data['location'] == 'Johannesburg'
        assert response.data['email'] == 'employer@example.com'
        assert response.data['role'] == 'admin'

    def test_get_employer_profile_unauthenticated(self):
        response = self.client.get('/api/employer/profile')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_employer_profile_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid-token')
        response = self.client.get('/api/employer/profile')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
