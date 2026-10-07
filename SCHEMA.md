# Database Schema Design

Based on CONTEXT.md and grilling decisions. This document maps entities to Django models.

## Existing Models (to Update)

### `accounts.models`
- ✅ `EmailVerificationToken` 
- ✅ `PasswordResetToken`
- ✅ `SessionToken`
- ❌ Missing: `UserType` field on User (candidate vs employer) - use `User.groups` or custom field

### `profiles.models`
- ✅ `CandidateProfile` — needs updates:
  - Add `salary_expectations` (currency in GBP)
  - Add `availability` (when available to start)
  - Add `archived_at` (soft-delete for GDPR)
  - Add `deleted_at` (hard-delete after 90 days)
  
### `profiles.skill_models`
- ✅ `Skill` (predefined list)
- ✅ `CandidateSkill` (M2M relation)

### `profiles.work_history_models`
- ✅ `WorkHistory`

### `employers.models`
- ✅ `Employer` — needs updates:
  - Add `verified` (email verification status)
  - Add `verification_token_expires_at`
- ✅ `EmployerUser` (team members with roles: admin, recruiter, viewer)

### `employers.job_models`
- ⚠️ `Job` — needs updates:
  - Change salary fields from ZAR to GBP (currency)
  - Update help text
- ✅ `JobSkill` (M2M relation)

### `jobs.application_models`
- ⚠️ `JobApplication` — needs updates:
  - Change statuses: `applied → shortlisted → hired_confirmed` + `rejected`, `withdrawn`
  - Remove `reviewed` status
  - Add `withdrawn_at` timestamp
  
### `jobs.hire_confirmation_models`
- ✅ `HireConfirmation` — mostly good, but needs:
  - Add commission tracking fields
  - Add refund logic (30-day window)
  - Add `finalized_at` for dispute closure

---

## New Models (to Create)

### `profiles.models`
- `Education` — degree, institution, graduation date
- `Certification` — name, issue date, expiry date (optional)
- `SupportingDocument` — file upload with type (cover_letter, portfolio, certificate, reference)

### `jobs.models`
- `ApplicationWithdrawal` — track when candidate withdraws (for audit)

### `employers.models`
- `Commission` — individual commission record (links Hire → Invoice)
- `CommissionInvoice` — monthly batch invoice to Employer
- `CommissionRefund` — track refunds within 30-day window
- `HireDispute` — disputes on hire confirmation (optional, for phase 2)

---

## Key Relationships

```
User (Django built-in)
├── CandidateProfile (1:1) — if user is candidate
│   ├── WorkHistory (1:N)
│   ├── Education (1:N)
│   ├── Certification (1:N)
│   ├── CandidateSkill (1:N)
│   ├── SupportingDocument (1:N)
│   └── JobApplication (1:N)
│       └── HireConfirmation (1:1)
│           ├── Commission (1:1)
│           └── CommissionRefund (0:1)
│
└── EmployerUser (1:N) — if user is employer team member
    └── Employer (N:1)
        ├── EmployerUser (1:N) — team members
        ├── Job (1:N)
        │   ├── JobSkill (1:N)
        │   └── JobApplication (1:N)
        └── CommissionInvoice (1:N) — monthly batches
            └── Commission (1:N)
```

---

## GDPR & Archive Strategy

**Soft Delete (Profile Level)**
- `CandidateProfile.archived_at` — marks profile as archived
- Archived profiles are excluded from candidate search
- Archived data retained for 90 days (disputes, hire records)

**Hard Delete (After 90 Days)**
- Run daily task to delete profiles where `archived_at < now() - 90 days`
- Delete: `CandidateProfile`, `WorkHistory`, `Education`, `Certification`, `SupportingDocument`
- Retain: `User` (login audit), `JobApplication` (hire records), `HireConfirmation` (disputes), `Commission` (billing)

---

## Commission & Invoicing

**Commission Trigger**
1. Employer confirms hire → `HireConfirmation.status = 'employer_confirmed'`
2. Candidate confirms hire → `HireConfirmation.status = 'confirmed'` → Create `Commission` record
3. Monthly batch → Create `CommissionInvoice` for all `Commission` records with `invoiced_at = null`

**Refund Window (30 Days)**
- After mutual confirmation, employer can claim "candidate left"
- Create `CommissionRefund` within 30 days post-hire
- After 30 days, hire is finalized (`hire_finalized_at`) — no new refunds allowed

---

## Indexes & Performance

Add indexes on:
- `CandidateProfile.status` — for active candidate queries
- `Job.status, employer` — for active job listings
- `JobApplication.status, job` — for application filtering
- `HireConfirmation.status` — for hire reporting
- `Commission.status` — for invoice batching
- `archived_at, deleted_at` — for cleanup tasks
