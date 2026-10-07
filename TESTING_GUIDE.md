# Backend API Testing Guide

## Setup

Before testing, ensure the backend is running:

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Create admin user
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

---

## 1. Authentication Tests

### Test 1.1: Candidate Signup

**Endpoint:** `POST /api/auth/signup`

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "candidate@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "user_type": "candidate"
  }'
```

**Expected Response:** 201 Created
```json
{
  "message": "User created successfully",
  "user_id": 1,
  "email": "candidate@example.com"
}
```

### Test 1.2: Employer Signup

**Endpoint:** `POST /api/auth/signup`

```bash
curl -X POST http://localhost:8000/api/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "employer@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "user_type": "employer"
  }'
```

### Test 1.3: Login

**Endpoint:** `POST /api/auth/login`

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "candidate@example.com",
    "password": "securepass123"
  }'
```

**Expected Response:** 200 OK
```json
{
  "token": "abc123xyz",
  "user_id": 1,
  "email": "candidate@example.com"
}
```

Save the token for subsequent requests: `export TOKEN="abc123xyz"`

---

## 2. Candidate Profile Tests

### Test 2.1: Get Current Profile

**Endpoint:** `GET /api/profiles/`

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/profiles/
```

**Expected Response:** 200 OK
```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "candidate@example.com",
  "phone": "07123456789",
  "location": "London, UK",
  "salary_expectations": 60000,
  "availability": "immediate",
  "status": "active",
  "created_at": "2026-10-06T12:00:00Z"
}
```

### Test 2.2: Update Profile

**Endpoint:** `PATCH /api/profiles/`

```bash
curl -X PATCH http://localhost:8000/api/profiles/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Smith",
    "phone": "07987654321",
    "location": "Manchester, UK",
    "salary_expectations": 65000,
    "availability": "notice_2_weeks"
  }'
```

---

## 3. Education Tests

### Test 3.1: Add Education

**Endpoint:** `POST /api/profiles/1/education/`

```bash
curl -X POST http://localhost:8000/api/profiles/1/education/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "institution": "University of London",
    "degree": "Bachelor of Science",
    "field": "Computer Science",
    "graduation_date": "2020-06-15",
    "description": "First class honours"
  }'
```

**Expected Response:** 201 Created
```json
{
  "id": 1,
  "institution": "University of London",
  "degree": "Bachelor of Science",
  "field": "Computer Science",
  "graduation_date": "2020-06-15",
  "description": "First class honours",
  "created_at": "2026-10-06T12:00:00Z"
}
```

### Test 3.2: List Education

**Endpoint:** `GET /api/profiles/1/education/`

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/profiles/1/education/
```

---

## 4. Certification Tests

### Test 4.1: Add Certification

**Endpoint:** `POST /api/profiles/1/certifications/`

```bash
curl -X POST http://localhost:8000/api/profiles/1/certifications/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "AWS Certified Solutions Architect",
    "issuer": "Amazon Web Services",
    "issue_date": "2024-03-10",
    "expiry_date": "2026-03-10",
    "credential_id": "AWS-12345",
    "credential_url": "https://aws.amazon.com/verify/..."
  }'
```

---

## 5. Supporting Documents Tests

### Test 5.1: Upload Document

**Endpoint:** `POST /api/profiles/1/documents/`

```bash
curl -X POST http://localhost:8000/api/profiles/1/documents/ \
  -H "Authorization: Bearer $TOKEN" \
  -F "document_type=cover_letter" \
  -F "file=@/path/to/cover_letter.pdf"
```

**Expected Response:** 201 Created
```json
{
  "id": 1,
  "document_type": "cover_letter",
  "file_name": "cover_letter.pdf",
  "file_size": 15360,
  "file_size_kb": 15.0,
  "created_at": "2026-10-06T12:00:00Z"
}
```

### Test 5.2: List Documents

**Endpoint:** `GET /api/profiles/1/documents/`

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/profiles/1/documents/
```

### Test 5.3: Delete Document

**Endpoint:** `DELETE /api/profiles/1/documents/1/`

```bash
curl -X DELETE http://localhost:8000/api/profiles/1/documents/1/ \
  -H "Authorization: Bearer $TOKEN"
```

**Expected Response:** 204 No Content

---

## 6. Job Tests

### Test 6.1: Create Job (as Employer)

**Endpoint:** `POST /api/jobs/`

First, login as employer and get employer token:

```bash
# Login as employer
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "employer@example.com",
    "password": "securepass123"
  }'

export EMPLOYER_TOKEN="<token>"

# Create job
curl -X POST http://localhost:8000/api/jobs/ \
  -H "Authorization: Bearer $EMPLOYER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Senior Python Developer",
    "description": "We are looking for an experienced Python developer...",
    "location": "London, UK",
    "salary_min": 70000,
    "salary_max": 90000,
    "experience_level": "senior",
    "required_skills": [1, 2, 3]
  }'
```

**Expected Response:** 201 Created
```json
{
  "id": 1,
  "title": "Senior Python Developer",
  "location": "London, UK",
  "salary_min": 70000,
  "salary_max": 90000,
  "status": "draft",
  "created_at": "2026-10-06T12:00:00Z"
}
```

### Test 6.2: Publish Job

**Endpoint:** `PATCH /api/jobs/1/`

```bash
curl -X PATCH http://localhost:8000/api/jobs/1/ \
  -H "Authorization: Bearer $EMPLOYER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "published"}'
```

### Test 6.3: List Jobs

**Endpoint:** `GET /api/jobs/`

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/jobs/
```

---

## 7. Application Tests

### Test 7.1: Apply to Job (as Candidate)

**Endpoint:** `POST /api/jobs/1/applications/`

```bash
curl -X POST http://localhost:8000/api/jobs/1/applications/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cover_letter": "I am very interested in this position..."
  }'
```

**Expected Response:** 201 Created
```json
{
  "id": 1,
  "job_id": 1,
  "job_title": "Senior Python Developer",
  "company_name": "Acme Corp",
  "status": "applied",
  "created_at": "2026-10-06T12:00:00Z"
}
```

### Test 7.2: Shortlist Application (as Employer)

**Endpoint:** `PATCH /api/jobs/1/applications/1/`

```bash
curl -X PATCH http://localhost:8000/api/jobs/1/applications/1/ \
  -H "Authorization: Bearer $EMPLOYER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "shortlisted"
  }'
```

**Expected Response:** 200 OK
```json
{
  "status": "shortlisted",
  "shortlisted_at": "2026-10-06T13:00:00Z"
}
```

### Test 7.3: View Application Status (as Candidate)

**Endpoint:** `GET /api/jobs/1/applications/1/`

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/jobs/1/applications/1/
```

---

## 8. Hire Confirmation Tests

### Test 8.1: Employer Confirms Hire

**Endpoint:** `POST /api/jobs/1/applications/1/hire-confirmation/`

```bash
curl -X POST http://localhost:8000/api/jobs/1/applications/1/hire-confirmation/ \
  -H "Authorization: Bearer $EMPLOYER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected Response:** 201 Created
```json
{
  "id": 1,
  "status": "employer_confirmed",
  "employer_confirmed_at": "2026-10-06T13:30:00Z",
  "candidate_confirmed_at": null,
  "is_mutual": false,
  "can_request_refund": false
}
```

### Test 8.2: Candidate Confirms Hire

**Endpoint:** `POST /api/jobs/1/applications/1/accept-hire/`

```bash
curl -X POST http://localhost:8000/api/jobs/1/applications/1/accept-hire/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Expected Response:** 200 OK
```json
{
  "id": 1,
  "status": "confirmed",
  "employer_confirmed_at": "2026-10-06T13:30:00Z",
  "candidate_confirmed_at": "2026-10-06T14:00:00Z",
  "is_mutual": true,
  "can_request_refund": true
}
```

### Test 8.3: Check Hire Status

**Endpoint:** `GET /api/jobs/1/applications/1/hire-status/`

```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8000/api/jobs/1/applications/1/hire-status/
```

---

## 9. Commission Tests

### Test 9.1: View Commissions (as Employer)

**Endpoint:** `GET /api/employer/commissions/`

```bash
curl -H "Authorization: Bearer $EMPLOYER_TOKEN" \
  http://localhost:8000/api/employer/commissions/
```

**Expected Response:** 200 OK
```json
[
  {
    "id": 1,
    "amount_gbp": 5000,
    "amount_pounds": 50.0,
    "status": "pending",
    "confirmed_at": "2026-10-06T14:00:00Z",
    "invoiced_at": null,
    "paid_at": null
  }
]
```

### Test 9.2: View Invoices (as Employer)

**Endpoint:** `GET /api/employer/invoices/`

```bash
curl -H "Authorization: Bearer $EMPLOYER_TOKEN" \
  http://localhost:8000/api/employer/invoices/
```

### Test 9.3: Send Invoice

**Endpoint:** `POST /api/employer/invoices/1/send/`

```bash
curl -X POST http://localhost:8000/api/employer/invoices/1/send/ \
  -H "Authorization: Bearer $EMPLOYER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## 10. Refund Tests

### Test 10.1: Request Refund (within 30 days)

**Endpoint:** `POST /api/employer/refunds/`

```bash
curl -X POST http://localhost:8000/api/employer/refunds/ \
  -H "Authorization: Bearer $EMPLOYER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "commission_id": 1,
    "reason": "candidate_left",
    "reason_detail": "Candidate did not start on agreed date",
    "evidence": "Confirmed with candidate on 2026-10-15"
  }'
```

### Test 10.2: Approve Refund

**Endpoint:** `POST /api/employer/refunds/1/approve/`

```bash
curl -X POST http://localhost:8000/api/employer/refunds/1/approve/ \
  -H "Authorization: Bearer $EMPLOYER_TOKEN"
```

---

## Common Issues & Fixes

### Issue: 401 Unauthorized
- **Cause:** Missing or invalid token
- **Fix:** Ensure token is valid and passed in header: `Authorization: Bearer <token>`

### Issue: 403 Forbidden
- **Cause:** Trying to access another user's data
- **Fix:** Only authenticated users can see their own data

### Issue: 404 Not Found
- **Cause:** Resource doesn't exist
- **Fix:** Check resource IDs in URL

### Issue: File Upload Fails
- **Cause:** Wrong content-type or missing file
- **Fix:** Use multipart form data: `-F "file=@path/to/file"`

---

## Smoke Test Checklist

Run these tests in order to verify the complete flow:

- [ ] Candidate signup
- [ ] Candidate login
- [ ] Update profile
- [ ] Add education
- [ ] Add certification
- [ ] Upload supporting documents
- [ ] Employer signup
- [ ] Employer login
- [ ] Create and publish job
- [ ] Candidate applies to job
- [ ] Employer shortlists application
- [ ] Employer confirms hire
- [ ] Candidate accepts hire
- [ ] Verify mutual confirmation
- [ ] View commission
- [ ] Send invoice
- [ ] (Optional) Request refund

All tests should pass with appropriate HTTP status codes (200, 201, 204, etc.)

---

## Notes

- All timestamps are in ISO 8601 format (UTC)
- All currency amounts are in pence (GBP)
- File uploads limited to PDF, DOCX, JPG, PNG (5 max per candidate)
- Refund window is 30 days from mutual confirmation
- Archive/deletion follows GDPR rules (90-day soft-delete)
