# 01: Job Application - Candidate Side

**What to build:** Candidates can apply to published jobs with optional cover letter. Track application status and provide history.

**Blocked by:** Phase 2 complete (jobs + candidate profiles)

**Status:** ready-for-agent

- [ ] JobApplication model: candidate FK, job FK, status (applied/reviewed/rejected/hired)
- [ ] Cover letter: optional text field (max 2000 chars)
- [ ] Timestamps: created_at (applied_at), updated_at, reviewed_at, hired_at
- [ ] Prevent duplicate applications (unique constraint: candidate + job)
- [ ] POST /api/jobs/:id/apply: submit application with cover letter
  - Returns application ID and confirmation
  - Validates job is published
  - Prevents duplicate applications
- [ ] GET /api/my-applications: list candidate's applications
  - Paginated: 20 per page
  - Filters: status, job_title
  - Sorted: newest first
  - Shows job title, company, status, dates
- [ ] GET /api/my-applications/:id: application detail with job info
- [ ] Validation: candidate exists, job is published, not already applied
- [ ] Integration tests (min 10): apply, duplicate rejection, retrieval, list, permissions
