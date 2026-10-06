---
status: ready-for-planning
labels: [phase-3, applications-hiring]
title: Phase 3 - Applications & Hiring Workflow
created: 2026-10-06
---

# Phase 3: Applications & Hiring Workflow

## Overview

Build the applications and hiring workflow: candidates apply to jobs, employers review applications, and both parties confirm a hire.

## Goals

1. ✅ Candidates can apply to published jobs
2. ✅ Employers can view and manage applications
3. ✅ Applications have status tracking (applied, reviewed, rejected, hired)
4. ✅ Employers can shortlist applications (separate from candidate shortlist)
5. ✅ Mutual hire confirmation (candidate + employer both agree)
6. ✅ Track hire dates and employment relationships

## Tickets - Phase 3A (4-5 planned)

### 01. Job Application - Candidate Side
**What to build:** Candidates can apply to published jobs with optional cover letter.

**Blocked by:** Phase 2 complete (jobs + candidate profiles)

**Status:** ready-for-agent

- [ ] JobApplication model: candidate FK, job FK, status (applied/reviewed/rejected/hired)
- [ ] Cover letter: optional text field
- [ ] Timestamps: applied_at, reviewed_at, hired_at
- [ ] Prevent duplicate applications (unique constraint: candidate + job)
- [ ] POST /api/jobs/:id/apply: submit application
- [ ] GET /api/jobs/:id/applications: list applications for a job (employer only)
- [ ] GET /api/my-applications: list candidate's applications
- [ ] GET /api/my-applications/:id: application detail
- [ ] Integration tests: apply, duplicate rejection, retrieval, permissions

### 02. Application Review - Employer Side
**What to build:** Employers can review applications, reject, or mark for consideration.

**Blocked by:** #01 (Job Application)

**Status:** ready-for-agent

- [ ] PATCH /api/jobs/:id/applications/:app_id/review: change application status
- [ ] Status transitions: applied → reviewed, reviewed → {rejected, hired}
- [ ] Rejection reasons: optional text field
- [ ] Review workflow: mark as reviewed, provide feedback (optional)
- [ ] GET /api/employer/applications: list all employer's applications (with filters)
- [ ] GET /api/employer/applications?status=applied: filter by status
- [ ] GET /api/employer/applications?job_id=:id: filter by job
- [ ] Permission: only employer that posted job can review
- [ ] Integration tests: status transitions, filtering, permissions

### 03. Application Shortlist
**What to build:** Employers can shortlist applications for final consideration.

**Blocked by:** #01 (Job Application)

**Status:** ready-for-agent

- [ ] ApplicationShortlist model: employer FK, application FK
- [ ] Unique constraint: employer + application (no duplicates)
- [ ] GET /api/employer/application-shortlist: list shortlisted applications
- [ ] POST /api/employer/application-shortlist: add application to shortlist
- [ ] DELETE /api/employer/application-shortlist/:id: remove from shortlist
- [ ] Permission: only recruiter+ can shortlist
- [ ] Integration tests: add, list, remove, permissions

### 04. Mutual Hire Confirmation
**What to build:** Candidate and employer both confirm the hire (2-way handshake).

**Blocked by:** #02 (Application Review)

**Status:** ready-for-agent

- [ ] HireConfirmation model: application FK, employer_confirmed, candidate_confirmed
- [ ] Timestamps: employer_confirmed_at, candidate_confirmed_at, hired_at (both confirmed)
- [ ] Workflow: employer marks hired → sends to candidate → candidate accepts/rejects
- [ ] GET /api/my-applications/:id/hire-status: candidate views hire offer
- [ ] POST /api/my-applications/:id/accept-hire: candidate accepts
- [ ] POST /api/my-applications/:id/decline-hire: candidate declines
- [ ] GET /api/employer/applications/:id/hire-status: employer views confirmation
- [ ] Only employer can initiate hire, candidate must accept
- [ ] Integration tests: confirmation flow, status transitions, permissions

### 05. Application Notifications & Analytics (Optional)
**What to build:** Track application metrics and send basic notifications.

**Blocked by:** #02 (Application Review)

**Status:** ready-for-agent (optional)

- [ ] Application metrics: total applications, applied/reviewed/hired counts per job
- [ ] GET /api/employer/jobs/:id/application-stats: job application metrics
- [ ] Notification hooks: emit events on status changes (for webhooks/email v2)
- [ ] GET /api/employer/applications?status=applied&sort=-applied_at: sorted listing
- [ ] Candidate can see application status history
- [ ] Integration tests: metrics, filtering, status history

## Architecture Notes

- New Django model: `JobApplication` in `jobs/` app
- New model: `HireConfirmation` for mutual agreement tracking
- New model: `ApplicationShortlist` in `employers/` app
- Workflow: candidates apply → employers review → mutual confirmation → hire
- Status machine: applied → reviewed → {rejected | hired}
- Mutual confirmation: both must agree before hire is final

## Dependencies

- Phase 1 (Candidate profiles) ✅ Complete
- Phase 2A (Employer infrastructure) ✅ Complete
- Auth system ✅ Complete
- Job posting ✅ Complete

## Timeline

Phase 3A (tickets 01-04): ~1-2 weeks
Phase 3B (ticket 05 + analytics): ~1 week (optional)
