import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from employers.models import Employer, EmployerUser
from employers.job_models import Job
from profiles.models import CandidateProfile
from profiles.availability_models import Availability
from accounts.models import SessionToken
from .application_models import JobApplication


@pytest.mark.django_db
class TestJobApplication:
    def setup_method(self):
        self.client = APIClient()

        self.candidate_user = User.objects.create_user(
            email='candidate@example.com',
            username='candidate@example.com',
            password='SecurePass123'
        )
        self.candidate = CandidateProfile.objects.create(
            user=self.candidate_user,
            first_name='John',
            last_name='Doe',
            location='Johannesburg',
            status='active'
        )
        Availability.objects.create(
            profile=self.candidate,
            available_from_month=1,
            available_from_year=2026,
            employment_type='full-time',
            salary_min=100000,
            salary_max=200000
        )
        self.candidate_token = SessionToken.objects.create(
            user=self.candidate_user,
            token='candidate-token',
            expires_at='2099-12-31T23:59:59Z'
        )

        self.employer = Employer.objects.create(
            name='TechCorp',
            location='Johannesburg'
        )
        self.employer_user = User.objects.create_user(
            email='employer@example.com',
            username='employer@example.com',
            password='SecurePass123'
        )
        EmployerUser.objects.create(user=self.employer_user, employer=self.employer, role='recruiter')

        self.job = Job.objects.create(
            employer=self.employer,
            title='Senior Python Developer',
            description='We are looking for a senior Python developer',
            location='Johannesburg',
            salary_min=150000,
            salary_max=250000,
            experience_level='senior',
            status='published'
        )
        self.draft_job = Job.objects.create(
            employer=self.employer,
            title='Junior React Developer',
            description='We are looking for a junior React developer',
            location='Johannesburg',
            salary_min=80000,
            salary_max=150000,
            experience_level='entry',
            status='draft'
        )

    def test_apply_to_published_job(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer candidate-token')
        data = {
            'cover_letter': 'I am interested in this position because I have 5 years of Python experience.'
        }
        response = self.client.post(f'/api/jobs/{self.job.id}/apply', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['job_id'] == self.job.id
        assert response.data['job_title'] == 'Senior Python Developer'
        assert response.data['company_name'] == 'TechCorp'
        assert response.data['status'] == 'applied'
        assert response.data['cover_letter'] == 'I am interested in this position because I have 5 years of Python experience.'
        assert JobApplication.objects.filter(candidate=self.candidate, job=self.job).exists()

    def test_apply_without_cover_letter(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer candidate-token')
        data = {}
        response = self.client.post(f'/api/jobs/{self.job.id}/apply', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['cover_letter'] == ''

    def test_apply_to_draft_job_denied(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer candidate-token')
        data = {'cover_letter': 'Interested'}
        response = self.client.post(f'/api/jobs/{self.draft_job.id}/apply', data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_duplicate_application_rejected(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer candidate-token')
        data = {'cover_letter': 'First application'}
        self.client.post(f'/api/jobs/{self.job.id}/apply', data, format='json')

        data2 = {'cover_letter': 'Second application'}
        response = self.client.post(f'/api/jobs/{self.job.id}/apply', data2, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'already applied' in str(response.data)
        assert JobApplication.objects.filter(candidate=self.candidate, job=self.job).count() == 1

    def test_apply_requires_candidate_profile(self):
        user_without_profile = User.objects.create_user(
            email='noprofile@example.com',
            username='noprofile@example.com',
            password='SecurePass123'
        )
        token = SessionToken.objects.create(
            user=user_without_profile,
            token='noprofile-token',
            expires_at='2099-12-31T23:59:59Z'
        )
        self.client.credentials(HTTP_AUTHORIZATION='Bearer noprofile-token')
        data = {'cover_letter': 'Interested'}
        response = self.client.post(f'/api/jobs/{self.job.id}/apply', data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert 'profile not found' in str(response.data)

    def test_apply_requires_authentication(self):
        data = {'cover_letter': 'Interested'}
        response = self.client.post(f'/api/jobs/{self.job.id}/apply', data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_list_my_applications(self):
        JobApplication.objects.create(candidate=self.candidate, job=self.job, cover_letter='Application 1')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer candidate-token')
        response = self.client.get('/api/jobs/my-applications')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['job_title'] == 'Senior Python Developer'

    def test_list_my_applications_empty(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer candidate-token')
        response = self.client.get('/api/jobs/my-applications')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0

    def test_filter_applications_by_status(self):
        app1 = JobApplication.objects.create(candidate=self.candidate, job=self.job, status='applied')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer candidate-token')
        response = self.client.get('/api/jobs/my-applications?status=applied')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['status'] == 'applied'

    def test_filter_applications_by_job_title(self):
        JobApplication.objects.create(candidate=self.candidate, job=self.job)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer candidate-token')
        response = self.client.get('/api/jobs/my-applications?job_title=Python')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

    def test_get_application_detail(self):
        app = JobApplication.objects.create(candidate=self.candidate, job=self.job, cover_letter='My application')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer candidate-token')
        response = self.client.get(f'/api/jobs/my-applications/{app.id}')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == app.id
        assert response.data['job_title'] == 'Senior Python Developer'
        assert response.data['cover_letter'] == 'My application'

    def test_get_application_detail_not_own(self):
        other_candidate_user = User.objects.create_user(
            email='other@example.com',
            username='other@example.com',
            password='SecurePass123'
        )
        other_candidate = CandidateProfile.objects.create(
            user=other_candidate_user,
            first_name='Jane',
            last_name='Smith',
            location='Cape Town',
            status='active'
        )
        app = JobApplication.objects.create(candidate=other_candidate, job=self.job)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer candidate-token')
        response = self.client.get(f'/api/jobs/my-applications/{app.id}')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_list_pagination(self):
        for i in range(25):
            Job.objects.create(
                employer=self.employer,
                title=f'Job {i}',
                description='Test',
                location='Johannesburg',
                salary_min=100000,
                salary_max=200000,
                experience_level='mid',
                status='published'
            )
        for job in Job.objects.all()[:25]:
            JobApplication.objects.create(candidate=self.candidate, job=job)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer candidate-token')
        response = self.client.get('/api/jobs/my-applications?page=1')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 20
        assert response.data['page'] == 1
        assert response.data['page_size'] == 20
        assert response.data['count'] >= 25

    def test_sort_applications(self):
        app1 = JobApplication.objects.create(candidate=self.candidate, job=self.job)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer candidate-token')
        response = self.client.get('/api/jobs/my-applications?sort=-created_at')

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
