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

@pytest.mark.django_db
class TestTeamMembers:
    def setup_method(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            username='admin@example.com',
            password='SecurePass123'
        )
        self.recruiter_user = User.objects.create_user(
            email='recruiter@example.com',
            username='recruiter@example.com',
            password='SecurePass123'
        )
        self.viewer_user = User.objects.create_user(
            email='viewer@example.com',
            username='viewer@example.com',
            password='SecurePass123'
        )
        self.new_user = User.objects.create_user(
            email='newuser@example.com',
            username='newuser@example.com',
            password='SecurePass123'
        )
        self.employer = Employer.objects.create(
            name='TechCorp',
            location='Johannesburg'
        )
        self.admin_employer_user = EmployerUser.objects.create(
            user=self.admin_user,
            employer=self.employer,
            role='admin'
        )
        self.recruiter_employer_user = EmployerUser.objects.create(
            user=self.recruiter_user,
            employer=self.employer,
            role='recruiter'
        )
        self.admin_token = SessionToken.objects.create(
            user=self.admin_user,
            token='admin-token',
            expires_at='2099-12-31T23:59:59Z'
        )
        self.recruiter_token = SessionToken.objects.create(
            user=self.recruiter_user,
            token='recruiter-token',
            expires_at='2099-12-31T23:59:59Z'
        )

    def test_list_team_members(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer admin-token')
        response = self.client.get('/api/employer/team-members')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['email'] in ['admin@example.com', 'recruiter@example.com']

    def test_add_team_member_as_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer admin-token')
        data = {
            'email': 'newuser@example.com',
            'role': 'recruiter'
        }
        response = self.client.post('/api/employer/team-members', data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['email'] == 'newuser@example.com'
        assert response.data['role'] == 'recruiter'
        assert EmployerUser.objects.filter(user=self.new_user, employer=self.employer).exists()

    def test_add_team_member_as_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer recruiter-token')
        data = {
            'email': 'newuser@example.com',
            'role': 'recruiter'
        }
        response = self.client.post('/api/employer/team-members', data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_add_duplicate_team_member(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer admin-token')
        data = {
            'email': 'recruiter@example.com',
            'role': 'viewer'
        }
        response = self.client.post('/api/employer/team-members', data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'already a team member' in str(response.data)

    def test_add_nonexistent_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer admin-token')
        data = {
            'email': 'nonexistent@example.com',
            'role': 'recruiter'
        }
        response = self.client.post('/api/employer/team-members', data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update_team_member_role(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer admin-token')
        data = {
            'role': 'viewer'
        }
        response = self.client.patch(f'/api/employer/team-members/{self.recruiter_employer_user.id}', data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['role'] == 'viewer'
        self.recruiter_employer_user.refresh_from_db()
        assert self.recruiter_employer_user.role == 'viewer'

    def test_update_team_member_as_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer recruiter-token')
        data = {
            'role': 'viewer'
        }
        response = self.client.patch(f'/api/employer/team-members/{self.admin_employer_user.id}', data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_remove_team_member(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer admin-token')
        response = self.client.delete(f'/api/employer/team-members/{self.recruiter_employer_user.id}')
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not EmployerUser.objects.filter(id=self.recruiter_employer_user.id).exists()

    def test_remove_team_member_as_non_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer recruiter-token')
        response = self.client.delete(f'/api/employer/team-members/{self.admin_employer_user.id}')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
class TestJobPosting:
    def setup_method(self):
        from profiles.skill_models import Skill
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            username='admin@example.com',
            password='SecurePass123'
        )
        self.recruiter_user = User.objects.create_user(
            email='recruiter@example.com',
            username='recruiter@example.com',
            password='SecurePass123'
        )
        self.viewer_user = User.objects.create_user(
            email='viewer@example.com',
            username='viewer@example.com',
            password='SecurePass123'
        )
        self.employer = Employer.objects.create(
            name='TechCorp',
            location='Johannesburg'
        )
        EmployerUser.objects.create(user=self.admin_user, employer=self.employer, role='admin')
        EmployerUser.objects.create(user=self.recruiter_user, employer=self.employer, role='recruiter')
        EmployerUser.objects.create(user=self.viewer_user, employer=self.employer, role='viewer')

        self.admin_token = SessionToken.objects.create(
            user=self.admin_user,
            token='admin-token',
            expires_at='2099-12-31T23:59:59Z'
        )
        self.recruiter_token = SessionToken.objects.create(
            user=self.recruiter_user,
            token='recruiter-token',
            expires_at='2099-12-31T23:59:59Z'
        )
        self.viewer_token = SessionToken.objects.create(
            user=self.viewer_user,
            token='viewer-token',
            expires_at='2099-12-31T23:59:59Z'
        )

        self.python_skill = Skill.objects.create(name='Python')
        self.react_skill = Skill.objects.create(name='React')

    def test_create_job_as_recruiter(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer recruiter-token')
        data = {
            'title': 'Senior Python Developer',
            'description': 'We are looking for a senior Python developer',
            'location': 'Johannesburg',
            'salary_min': 150000,
            'salary_max': 250000,
            'experience_level': 'senior',
            'required_skill_ids': [self.python_skill.id]
        }
        response = self.client.post('/api/employer/jobs', data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['title'] == 'Senior Python Developer'
        assert response.data['status'] == 'draft'
        from .job_models import Job
        assert Job.objects.filter(title='Senior Python Developer').exists()

    def test_create_job_as_viewer_denied(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer viewer-token')
        data = {
            'title': 'Senior Python Developer',
            'description': 'We are looking for a senior Python developer',
            'location': 'Johannesburg',
            'salary_min': 150000,
            'salary_max': 250000,
            'experience_level': 'senior'
        }
        response = self.client.post('/api/employer/jobs', data, format='json')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_job_invalid_salary(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer recruiter-token')
        data = {
            'title': 'Senior Python Developer',
            'description': 'We are looking for a senior Python developer',
            'location': 'Johannesburg',
            'salary_min': 250000,
            'salary_max': 150000,
            'experience_level': 'senior'
        }
        response = self.client.post('/api/employer/jobs', data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_list_employer_jobs(self):
        from .job_models import Job
        Job.objects.create(
            employer=self.employer,
            title='Python Developer',
            description='Looking for a Python dev',
            location='Johannesburg',
            salary_min=100000,
            salary_max=200000,
            experience_level='mid',
            status='draft'
        )
        self.client.credentials(HTTP_AUTHORIZATION='Bearer admin-token')
        response = self.client.get('/api/employer/jobs')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'Python Developer'

    def test_get_job_detail(self):
        from .job_models import Job
        job = Job.objects.create(
            employer=self.employer,
            title='Python Developer',
            description='Looking for a Python dev',
            location='Johannesburg',
            salary_min=100000,
            salary_max=200000,
            experience_level='mid',
            status='draft'
        )
        response = self.client.get(f'/api/employer/jobs/{job.id}')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Python Developer'

    def test_update_job_as_recruiter(self):
        from .job_models import Job
        job = Job.objects.create(
            employer=self.employer,
            title='Python Developer',
            description='Looking for a Python dev',
            location='Johannesburg',
            salary_min=100000,
            salary_max=200000,
            experience_level='mid',
            status='draft'
        )
        self.client.credentials(HTTP_AUTHORIZATION='Bearer recruiter-token')
        data = {
            'title': 'Senior Python Developer',
            'salary_min': 150000
        }
        response = self.client.patch(f'/api/employer/jobs/{job.id}', data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == 'Senior Python Developer'
        assert response.data['salary_min'] == 150000


@pytest.mark.django_db
class TestJobManagement:
    def setup_method(self):
        from .job_models import Job
        self.client = APIClient()
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            username='admin@example.com',
            password='SecurePass123'
        )
        self.recruiter_user = User.objects.create_user(
            email='recruiter@example.com',
            username='recruiter@example.com',
            password='SecurePass123'
        )
        self.viewer_user = User.objects.create_user(
            email='viewer@example.com',
            username='viewer@example.com',
            password='SecurePass123'
        )
        self.employer = Employer.objects.create(
            name='TechCorp',
            location='Johannesburg'
        )
        EmployerUser.objects.create(user=self.admin_user, employer=self.employer, role='admin')
        EmployerUser.objects.create(user=self.recruiter_user, employer=self.employer, role='recruiter')
        EmployerUser.objects.create(user=self.viewer_user, employer=self.employer, role='viewer')

        self.admin_token = SessionToken.objects.create(
            user=self.admin_user,
            token='admin-token',
            expires_at='2099-12-31T23:59:59Z'
        )
        self.recruiter_token = SessionToken.objects.create(
            user=self.recruiter_user,
            token='recruiter-token',
            expires_at='2099-12-31T23:59:59Z'
        )
        self.viewer_token = SessionToken.objects.create(
            user=self.viewer_user,
            token='viewer-token',
            expires_at='2099-12-31T23:59:59Z'
        )

        self.job = Job.objects.create(
            employer=self.employer,
            title='Python Developer',
            description='Looking for a Python dev',
            location='Johannesburg',
            salary_min=100000,
            salary_max=200000,
            experience_level='mid',
            status='draft'
        )

    def test_publish_job(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer recruiter-token')
        response = self.client.post(f'/api/employer/jobs/{self.job.id}/publish')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'published'
        self.job.refresh_from_db()
        assert self.job.status == 'published'

    def test_publish_job_as_viewer_denied(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer viewer-token')
        response = self.client.post(f'/api/employer/jobs/{self.job.id}/publish')
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_close_job(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer admin-token')
        response = self.client.post(f'/api/employer/jobs/{self.job.id}/close')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'closed'
        self.job.refresh_from_db()
        assert self.job.status == 'closed'

    def test_unpublish_job(self):
        from .job_models import Job
        job = Job.objects.create(
            employer=self.employer,
            title='React Developer',
            description='Looking for React dev',
            location='Johannesburg',
            salary_min=100000,
            salary_max=200000,
            experience_level='mid',
            status='published'
        )
        self.client.credentials(HTTP_AUTHORIZATION='Bearer recruiter-token')
        response = self.client.post(f'/api/employer/jobs/{job.id}/unpublish')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'draft'
        job.refresh_from_db()
        assert job.status == 'draft'

    def test_get_job_metrics(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer admin-token')
        response = self.client.get(f'/api/employer/jobs/{self.job.id}/metrics')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['job_id'] == self.job.id
        assert response.data['title'] == 'Python Developer'
        assert 'applications_count' in response.data
        assert 'views_count' in response.data

    def test_publish_nonexistent_job(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer admin-token')
        response = self.client.post('/api/employer/jobs/9999/publish')
        
        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestCandidateSearch:
    def setup_method(self):
        from profiles.models import CandidateProfile
        from profiles.availability_models import Availability
        self.client = APIClient()
        
        self.employer_user = User.objects.create_user(
            email='employer@example.com',
            username='employer@example.com',
            password='SecurePass123'
        )
        self.employer = Employer.objects.create(
            name='TechCorp',
            location='Johannesburg'
        )
        self.employer_recruiter = EmployerUser.objects.create(
            user=self.employer_user,
            employer=self.employer,
            role='recruiter'
        )
        self.employer_token = SessionToken.objects.create(
            user=self.employer_user,
            token='employer-token',
            expires_at='2099-12-31T23:59:59Z'
        )

        self.python_skill = Skill.objects.create(name='Python')
        self.react_skill = Skill.objects.create(name='React')

        self.candidate1_user = User.objects.create_user(
            email='candidate1@example.com',
            username='candidate1@example.com',
            password='SecurePass123'
        )
        self.candidate1 = CandidateProfile.objects.create(
            user=self.candidate1_user,
            first_name='John',
            last_name='Doe',
            location='Johannesburg',
            phone='0721234567',
            status='active'
        )
        self.candidate1.skills.add(self.python_skill)
        Availability.objects.create(
            profile=self.candidate1,
            available_from_month=1,
            available_from_year=2026,
            employment_type='full-time',
            salary_min=100000,
            salary_max=200000
        )

        self.candidate2_user = User.objects.create_user(
            email='candidate2@example.com',
            username='candidate2@example.com',
            password='SecurePass123'
        )
        self.candidate2 = CandidateProfile.objects.create(
            user=self.candidate2_user,
            first_name='Jane',
            last_name='Smith',
            location='Cape Town',
            phone='0729876543',
            status='active'
        )
        self.candidate2.skills.add(self.react_skill)
        Availability.objects.create(
            profile=self.candidate2,
            available_from_month=2,
            available_from_year=2026,
            employment_type='contract',
            salary_min=80000,
            salary_max=150000
        )

        self.paused_candidate_user = User.objects.create_user(
            email='paused@example.com',
            username='paused@example.com',
            password='SecurePass123'
        )
        self.paused_candidate = CandidateProfile.objects.create(
            user=self.paused_candidate_user,
            first_name='Bob',
            last_name='Johnson',
            location='Johannesburg',
            status='paused'
        )

    def test_search_all_active_candidates(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer employer-token')
        response = self.client.get('/api/employer/candidates/search')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2
        assert len(response.data['results']) == 2

    def test_search_candidates_by_location(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer employer-token')
        response = self.client.get('/api/employer/candidates/search?location=Cape+Town')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['first_name'] == 'Jane'

    def test_search_candidates_by_skills(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer employer-token')
        response = self.client.get(f'/api/employer/candidates/search?skills={self.python_skill.id}')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['first_name'] == 'John'

    def test_search_candidates_by_salary_range(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer employer-token')
        response = self.client.get('/api/employer/candidates/search?salary_min=90000&salary_max=180000')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['first_name'] == 'Jane'

    def test_search_candidates_by_employment_type(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer employer-token')
        response = self.client.get('/api/employer/candidates/search?employment_type=contract')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['first_name'] == 'Jane'

    def test_paused_candidates_not_visible(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer employer-token')
        response = self.client.get('/api/employer/candidates/search')
        
        assert response.status_code == status.HTTP_200_OK
        names = [c['first_name'] for c in response.data['results']]
        assert 'Bob' not in names

    def test_search_requires_authentication(self):
        response = self.client.get('/api/employer/candidates/search')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_search_pagination(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer employer-token')
        response = self.client.get('/api/employer/candidates/search?page=1')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['page'] == 1
        assert response.data['page_size'] == 20
