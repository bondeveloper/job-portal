# 03: Application Shortlist

**What to build:** Employers can shortlist applications (separate from candidate shortlist) for final consideration and faster access.

**Blocked by:** #01 (Job Application)

**Status:** ready-for-agent

- [ ] ApplicationShortlist model: employer FK, application FK, created_at
- [ ] Unique constraint: employer + application (no duplicate shortlists)
- [ ] GET /api/employer/application-shortlist: list shortlisted applications
  - Paginated: 20 per page
  - Sorted: newest first (most recent adds to top)
  - Shows candidate, job, application status, shortlist date
- [ ] POST /api/employer/application-shortlist: add application to shortlist
  - Returns shortlist entry with metadata
  - Validates application belongs to employer's jobs
  - Prevents duplicate shortlists
- [ ] DELETE /api/employer/application-shortlist/:id: remove from shortlist
  - Only employer that added can remove
- [ ] Permission: only recruiter+ can shortlist (not viewers)
- [ ] Integration tests (min 8): add, list, remove, duplicates, permissions
