# Candidate Profile Creation Spec

## Problem Statement

Candidates in the South African job market need a way to create a professional profile and become discoverable by employers. Without an easy onboarding experience, candidates can't access job opportunities, and the platform has no supply of talent.

## Solution

Build a signup and onboarding flow that guides candidates through creating a structured profile in minimal steps. The flow consists of:
1. Email/password signup with email verification
2. A step-by-step wizard (basic info → skills → work history → availability/salary)
3. Profile immediately searchable by employers after completion
4. Full edit/delete/pause capabilities post-signup
5. Password recovery via email

## User Stories

1. As a candidate, I want to sign up with an email and password, so that I can create an account without friction.
2. As a candidate, I want to verify my email address, so that employers can trust my contact information is real.
3. As a candidate, I want to enter my first and last name during onboarding, so that employers see who I am.
4. As a candidate, I want to provide my phone number (optional), so that employers can call me if interested.
5. As a candidate, I want to enter my location (freeform text), so that employers can search for candidates in my area.
6. As a candidate, I want to select my skills from a predefined list (max 10), so that employers can find me by what I'm good at.
7. As a candidate, I want to add my work history (company, role, dates, description), so that employers understand my experience.
8. As a candidate, I want to leave the work history field blank during onboarding, so that I can finish quickly even if I'm entry-level.
9. As a candidate, I want to set my availability start date (month/year), so that employers know when I'm ready to work.
10. As a candidate, I want to specify my employment type preference (full-time, part-time, contract), so that employers only see relevant opportunities.
11. As a candidate, I want to provide salary expectations (min/max ZAR, optional), so that employers know my range before applying.
12. As a candidate, I want to skip optional fields in the wizard and come back to them later, so that I'm not forced through a long form.
13. As a candidate, I want to see a success confirmation after I complete the wizard, so that I know my profile was created.
14. As a candidate, I want my profile to be immediately searchable by employers, so that I can start getting noticed right away.
15. As a candidate, I want to edit my profile after creation, so that I can keep my information up to date.
16. As a candidate, I want to add multiple work history entries after signup, so that I can show my full career history.
17. As a candidate, I want to pause my profile without deleting it, so that I can temporarily hide from employer search.
18. As a candidate, I want to change my email address with re-verification, so that I can fix typos or update my contact info.
19. As a candidate, I want to delete my profile, so that I can fully remove my information from the platform.
20. As a candidate, I want my deleted profile data to be archived for 90 days, so that disputes can be resolved if I was hired.
21. As a candidate, I want my archived data to be permanently deleted after 90 days, so that my information is eventually erased per GDPR/POPIA.
22. As a candidate, I want to reset my forgotten password via email, so that I can regain access to my account.
23. As a candidate, I want my session to last 30 days, so that I don't get logged out while I'm actively job hunting.
24. As a candidate, I want a "remember me" option at login, so that I can stay logged in longer if I choose.
25. As a candidate, I want to see an error message if I try to sign up with an email that's already registered, so that I know to log in instead.
26. As a candidate, I want password validation (min 8 characters), so that I know my password meets security standards.
27. As a candidate, I want my password requirements to be clear (no unnecessary complexity rules), so that I can create a strong password easily.
28. As a candidate, I want to know which fields are required during onboarding, so that I understand what I must fill in.
29. As a candidate, I want to know which work history fields are required (company, role, dates), so that I provide complete information.
30. As a candidate, I want my location field to be free-text, so that I can enter any city or region in South Africa.
31. As a candidate, I want skill selection to be a searchable dropdown, so that I can quickly find and add the skills I have.
32. As a candidate, I want work history end dates to be optional, so that I can indicate I'm still in a current role.
33. As a candidate, I want availability to default to "immediately available, full-time" if I don't set it, so that I don't have to be explicit if I'm ready now.
34. As a candidate, I want salary expectations to be optional, so that I'm not forced to disclose if I prefer not to.
35. As a candidate, I want my salary range to use South African Rand (ZAR), so that I see prices in my local currency.
36. As an employer, I want applications from candidates with complete profiles to include their full information, so that I can make informed hiring decisions.

## Implementation Decisions

### Authentication & Account Management
- **Email/password authentication**: Candidates sign up with email and password. No social login or third-party auth in v1.
- **Email verification**: Required before profile is searchable. Verification email sent after signup; candidate must click link to activate.
- **Password requirements**: Minimum 8 characters. No complexity rules (uppercase, numbers, special chars) to reduce friction.
- **Password reset**: Available via email link (standard "forgot password" flow). Reset link valid for 24 hours.
- **Session management**: 30-day session duration with optional "remember me" checkbox at login for longer persistence.
- **Duplicate email handling**: Reject signup with message "Email already registered. [Log in instead]" to guide to login flow.
- **Email change**: Candidates can change email in profile settings; requires re-verification.

### Profile Data Model
- **Candidate profile** contains:
  - Email (unique, verified)
  - First name, last name (required, no validation on format)
  - Phone (optional)
  - Location (freeform text, required)
  - Skills (multi-select, max 10, from predefined list of ~80 skills)
  - Work history (multiple entries, each with: company, role, start date, end date [optional], description [optional])
  - Availability: start date (month/year, required), employment type (full-time/part-time/contract, required)
  - Salary expectations: min ZAR, max ZAR (both optional)
  - Profile status: active, paused, archived
  - Created/updated timestamps

### Skills
- **Predefined skill list**: ~80 common skills curated for global/generic use (e.g., Python, React, AWS, Leadership, Project Management).
- **South African tuning**: Skills are generic for v1; will be monitored and updated based on actual Candidate/Employer searches. SA-specific skills (e.g., "SARS eFiling") added later if demand exists.
- **No custom skills**: Candidates can only select from predefined list in v1.

### Onboarding Wizard
- **Step sequence**: (1) Basic info (first name, last name, email, phone, location) → (2) Skills (multi-select, min 1 required) → (3) Work history (company, role, dates; optional but encouraged) → (4) Availability & salary (start date + employment type required; salary optional).
- **Skip behavior**: Candidates can skip optional steps (phone, work history, salary) and complete wizard with only required fields.
- **Profile completeness**: Required fields are: first name, last name, email, location, ≥1 skill, availability start date, employment type. All other fields optional.
- **Post-wizard flow**: Success page shows profile summary + "Browse jobs" button. Redirect to job search.

### Profile Lifecycle
- **Searchability**: Profile immediately searchable by employers after wizard completion (no manual publish step).
- **Profile pause**: Candidate can pause profile to hide from search without deleting. Can unpause anytime.
- **Profile edit**: Candidates can edit any field after creation. Can add multiple work history entries (only 1 in wizard).
- **Profile deletion**: Soft-delete (archive) with 90-day retention for dispute resolution. After 90 days, automatic hard-delete via scheduled job.
- **Deleted profile visibility**: Candidate profile archived, but their applications remain visible to employers (shared record).

### Candidate Search (by Employer)
- **Searchable fields**: Employer can search/filter candidates by: skills, location (text match), experience level, salary range, availability.
- **Visibility**: Only active (non-paused, non-archived) profiles are searchable.

### API Contract (outline)
- `POST /auth/signup`: Register candidate (email, password). Returns user ID, triggers verification email.
- `POST /auth/verify-email`: Confirm email verification token.
- `POST /auth/login`: Login with email/password. Returns session token.
- `POST /auth/logout`: End session.
- `POST /auth/forgot-password`: Request password reset email.
- `POST /auth/reset-password`: Reset password with token.
- `POST /profiles`: Create candidate profile (wizard completion).
- `GET /profiles/:id`: Retrieve candidate profile.
- `PATCH /profiles/:id`: Update candidate profile.
- `DELETE /profiles/:id`: Soft-delete (archive) candidate profile.
- `PATCH /profiles/:id/pause`: Pause/unpause profile.
- `GET /profiles/:id/applications`: Retrieve candidate's applications (in later feature).

### Employer Context (out of scope for this spec, but shapes decisions)
- Employers will search/browse candidate profiles and view full details when interested.
- Applications are a separate feature (coming after profile creation).

## Testing Decisions

### Testing Philosophy
- **Seam**: Test at the HTTP API boundary with a real test database (integration testing). This validates the full flow as a Candidate would experience it (signup → verification → wizard → profile saved).
- **Good tests**: Only test external behavior (API responses, database state), not internal implementation. E.g., test that `POST /auth/signup` rejects duplicate emails, not that a specific validation function is called.
- **Mock vs. Real**: Use a real test database (PostgreSQL in-memory or test instance), not mocked ORM. This catches real data migration bugs, constraint violations, and race conditions.

### Modules to Test
- **Authentication module**: Signup, email verification, login, password reset, session management.
- **Profile module**: Create, read, update, delete (soft), pause/unpause profile.
- **Skill module**: Multi-select, predefined list validation.
- **Wizard module**: Step-by-step flow, skip logic, required field validation.
- **Email module**: Verification email, password reset email delivery.

### Test Scenarios
- Signup with valid email/password → profile created.
- Signup with duplicate email → reject with error.
- Signup with weak password → reject with error.
- Signup → email verification → profile becomes searchable.
- Wizard: skip optional fields → profile completes with required fields only.
- Wizard: invalid skill selection (non-existent skill) → reject.
- Wizard: too many skills (>10) → reject.
- Profile edit: change email → re-verification required.
- Profile delete: soft-archive → after 90 days, hard-delete.
- Profile pause → hidden from search. Unpause → searchable again.
- Password reset: request → email sent → token valid for 24h → reset password → login with new password.
- Session: login → session lasts 30 days → automatic logout after 30 days.
- Work history: add 1 in wizard → add more after signup.

## Out of Scope

- **Supporting documents**: Cover letters, portfolio samples, certifications, references. Deferred to post-v1.
- **Notifications**: Email notifications for job matches, application updates, etc. Managed in account settings (deferred).
- **Two-factor authentication (2FA)**: Optional 2FA at signup/login. Deferred for later security hardening.
- **LinkedIn import**: Auto-populate profile from LinkedIn. Deferred.
- **Multi-language UI**: English-only for v1. Afrikaans/other language support deferred.
- **Mobile app**: Web-first (responsive). Native mobile app deferred.
- **Private/public profile toggle**: Profile pause feature is sufficient for privacy in v1.
- **Profile completeness scoring**: UI indicator showing "60% complete." Nice-to-have, deferred.
- **Candidate notifications/preferences**: Opt-in/out of updates. Deferred to account settings.
- **Off-platform hiring detection/policy**: Handled separately by platform policy team.
- **Multiple applications limit**: Candidate can apply multiple times to same employer; policy TBD.
- **Job deactivation impact**: Employer unpublishes job before hire confirmation; impact on applications TBD (separate feature).

## Further Notes

- **South African market focus**: Currency is ZAR. Employers are primarily SA-based. Skills are generic for v1, tuned later based on data.
- **Data retention**: Archived Candidate data is automatically deleted after 90 days per GDPR/POPIA erasure requirements. This requires a scheduled job.
- **Email delivery**: Assumes reliable email service (e.g., SendGrid, AWS SES) for verification and password reset emails.
- **Security**: Passwords hashed with bcrypt or similar. Session tokens are signed/encrypted. Email tokens are short-lived (24h for reset, immediate verification).
- **Candidates applying without work history**: Entry-level candidates can complete onboarding and be hired without any work history (it's optional). This is intentional to lower barrier to employment.
- **Search integration**: Profile search (by Employer) is a separate feature; this spec focuses only on profile creation. Search API will query the profile data model defined here.
