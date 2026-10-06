# 02: Application Review - Employer Side

**What to build:** Employers can review applications, reject candidates, or mark for consideration. Track review status and feedback.

**Blocked by:** #01 (Job Application)

**Status:** ready-for-agent

- [ ] PATCH /api/employer/applications/:app_id: change application status
  - Status transitions: applied → reviewed (no-op), reviewed → rejected
  - Rejection reason: optional text field (max 500 chars)
  - Only employer that posted job can review
- [ ] GET /api/employer/applications: list all employer's applications
  - Paginated: 20 per page
  - Filters: status (applied, reviewed, rejected, hired), job_id
  - Sorted: newest first, by job title
  - Shows candidate name, job, status, dates
- [ ] GET /api/employer/applications/:app_id: application detail
  - Show candidate profile preview, cover letter, job details
  - Show review status and feedback (if rejected)
- [ ] Permission: only recruiter+ can review applications
- [ ] Permission: can only review applications for own employer's jobs
- [ ] Integration tests (min 10): status transitions, filtering, permissions, rejections
