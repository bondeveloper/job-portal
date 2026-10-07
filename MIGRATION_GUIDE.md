# Database Schema Migrations

## Changes Made

### New Models Created

**profiles app:**
- `Education` — degree, institution, graduation date
- `Certification` — certifications with expiry dates
- `SupportingDocument` — candidate supporting docs (cover letter, portfolio, etc.)

**employers app:**
- `Commission` — individual hire commission record
- `CommissionInvoice` — monthly batch invoice to employer
- `CommissionRefund` — refund request within 30-day window

### Existing Models Updated

**profiles.models.CandidateProfile:**
- Added `salary_expectations` (GBP)
- Added `availability` (when available to start)
- Added `archived_at` (soft-delete for GDPR)
- Added `deleted_at` (hard-delete after 90 days)
- Added indexes for performance
- Added `archive()` method for GDPR compliance

**jobs.application_models.JobApplication:**
- Updated statuses: `applied → shortlisted → hired_confirmed` + `rejected`, `withdrawn`
- Changed `reviewed` to `shortlisted`
- Added `shortlisted_at`, `rejected_at`, `withdrawn_at` timestamps

**employers.job_models.Job:**
- Changed salary fields: ZAR → GBP (in help text)
- Added `published_at` timestamp

**jobs.hire_confirmation_models.HireConfirmation:**
- Updated status choices and logic
- Added helper methods: `candidate_confirm()`, `is_mutual()`, `can_request_refund()`, `finalize_hire()`
- Changed employer_confirmed default from True to required explicit confirmation

## Running Migrations

After setting up your environment:

### 1. Create and apply migrations

```bash
# In backend directory with venv activated
python manage.py makemigrations
python manage.py migrate
```

### 2. Load predefined skills (optional)

```bash
python manage.py seed_skills
```

## Migration Order

Migrations will be created in this order:

1. **profiles**: 
   - Update CandidateProfile fields
   - Create Education model
   - Create Certification model
   - Create SupportingDocument model

2. **jobs**:
   - Update JobApplication statuses and fields
   - Update HireConfirmation

3. **employers**:
   - Update Job salary fields
   - Create Commission model
   - Create CommissionInvoice model
   - Create CommissionRefund model

## GDPR Cleanup

After migrations, set up a scheduled task to handle GDPR deletions:

```bash
# Daily cron job
0 0 * * * cd /path/to/job-portal && python manage.py gdpr_cleanup_archived_profiles
```

This will hard-delete profiles archived more than 90 days ago.

## Verification

After migrations, verify with:

```bash
python manage.py dbshell
# Then run: \dt (PostgreSQL) or .tables (SQLite) to list all tables
```

Expected new tables:
- `education`
- `certifications`
- `supporting_documents`
- `commissions`
- `commission_invoices`
- `commission_refunds`
