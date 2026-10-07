

@pytest.mark.django_db
class TestAnalyticsAndDisputes:
    def setup_method(self):
        from jobs.application_models import JobApplication
        from jobs.hire_confirmation_models import HireConfirmation
        from employers.commission_models import Commission
        from employers.invoice_models import Invoice
        from employers.payment_models import Payment
        
        self.admin_user = User.objects.create_user(
            email='admin@example.com',
            username='admin@example.com',
            password='SecurePass123'
        )
        self.employer = Employer.objects.create(name='TechCorp', location='Johannesburg')
        EmployerUser.objects.create(user=self.admin_user, employer=self.employer, role='admin')
        
        self.admin_token = SessionToken.objects.create(
            user=self.admin_user,
            token='admin-token',
            expires_at='2099-12-31T23:59:59Z'
        )

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer admin-token')

        self.job = Job.objects.create(
            employer=self.employer,
            title='Senior Python Developer',
            description='Test job',
            location='Johannesburg',
            salary_min=150000,
            salary_max=250000,
            experience_level='senior',
            status='published'
        )

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

        self.application = JobApplication.objects.create(
            candidate=self.candidate,
            job=self.job,
            cover_letter='Interested'
        )

        self.hire = HireConfirmation.objects.create(
            application=self.application,
            employer_confirmed=True,
            status='confirmed'
        )

    def test_revenue_analytics(self):
        response = self.client.get('/api/admin/analytics/revenue')

        assert response.status_code == status.HTTP_200_OK
        assert 'total_revenue' in response.data
        assert 'paid_revenue' in response.data
        assert 'pending_revenue' in response.data
        assert response.data['total_revenue'] == 15000.00

    def test_commission_metrics(self):
        response = self.client.get('/api/admin/analytics/commissions')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_commissions'] >= 1
        assert 'by_status' in response.data
        assert response.data['total_amount'] == 15000.00

    def test_payment_reconciliation(self):
        response = self.client.get('/api/admin/reconciliation')

        assert response.status_code == status.HTTP_200_OK
        assert 'expected_payments' in response.data
        assert 'received_payments' in response.data
        assert 'outstanding_amount' in response.data
        assert 'reconciliation_status' in response.data

    def test_mark_commission_disputed(self):
        from employers.commission_models import Commission
        commission = Commission.objects.get(hire_confirmation=self.hire)
        
        data = {
            'reason': 'Dispute reason for testing'
        }
        response = self.client.post(f'/api/admin/commissions/{commission.id}/dispute', data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] == 'open'
        
        commission.refresh_from_db()
        assert commission.status == 'disputed'

    def test_list_disputes(self):
        from employers.commission_models import Commission
        commission = Commission.objects.get(hire_confirmation=self.hire)
        
        data = {'reason': 'Test dispute'}
        self.client.post(f'/api/admin/commissions/{commission.id}/dispute', data, format='json')

        response = self.client.get('/api/admin/disputes')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1

    def test_non_admin_cannot_access_analytics(self):
        recruiter_user = User.objects.create_user(
            email='recruiter@example.com',
            username='recruiter@example.com',
            password='SecurePass123'
        )
        EmployerUser.objects.create(user=recruiter_user, employer=self.employer, role='recruiter')
        recruiter_token = SessionToken.objects.create(
            user=recruiter_user,
            token='recruiter-token',
            expires_at='2099-12-31T23:59:59Z'
        )

        self.client.credentials(HTTP_AUTHORIZATION='Bearer recruiter-token')
        response = self.client.get('/api/admin/analytics/revenue')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_revenue_analytics_with_multiple_employers(self):
        other_employer = Employer.objects.create(name='OtherCorp', location='Cape Town')
        other_job = Job.objects.create(
            employer=other_employer,
            title='Developer',
            description='Test',
            location='Cape Town',
            salary_min=100000,
            salary_max=200000,
            experience_level='mid',
            status='published'
        )
        from jobs.application_models import JobApplication
        from jobs.hire_confirmation_models import HireConfirmation
        
        app = JobApplication.objects.create(candidate=self.candidate, job=other_job)
        hire = HireConfirmation.objects.create(application=app, employer_confirmed=True, status='confirmed')

        response = self.client.get('/api/admin/analytics/revenue')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_revenue'] >= 20000.00

    def test_dispute_cannot_be_created_twice(self):
        from employers.commission_models import Commission
        commission = Commission.objects.get(hire_confirmation=self.hire)
        
        data = {'reason': 'First dispute'}
        self.client.post(f'/api/admin/commissions/{commission.id}/dispute', data, format='json')

        data2 = {'reason': 'Second dispute'}
        response = self.client.post(f'/api/admin/commissions/{commission.id}/dispute', data2, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'already has an open dispute' in str(response.data)
