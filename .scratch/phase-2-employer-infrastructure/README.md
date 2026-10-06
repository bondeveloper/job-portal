---
status: phase-2a-complete
labels: [phase-2, employer-infrastructure, phase-2a-complete]
title: Phase 2 - Employer Infrastructure
created: 2026-10-06
phase_2a_completed: 2026-10-06
---

# Phase 2: Employer Infrastructure

## Overview

Build the employer side of the platform: company registration, team management, job posting, and candidate search.

## Goals

1. ✅ Employers can register and create company accounts
2. ✅ Employers can manage team members with role-based access
3. ✅ Employers can post, edit, and manage job listings
4. ✅ Candidates can search and discover jobs
5. ✅ Employers can search and discover candidates
6. ✅ Employers can shortlist/bookmark candidates

## Tickets - Phase 2A COMPLETE ✅ (7/7)

### ✅ 01. Employer Account Creation (Ticket #09)
- Employer (company) registration with profile
- Company model: name, location, industry, size
- EmployerUser model: user-employer relationship with role
- API: POST /api/employer/register, GET /api/employer/profile
- **Status: COMPLETE** (9 integration tests passing)
- Endpoints: `/api/employer/register`, `/api/employer/profile`

### ✅ 02. Employer Team Members (Ticket #10)
- Add/remove team members to employer
- Role-based access (admin, recruiter, viewer)
- Manage permissions and team membership
- API: GET/POST /api/employer/team-members, PATCH/DELETE /api/employer/team-members/:id
- **Status: COMPLETE** (12 integration tests passing)
- Endpoints: `/api/employer/team-members`, `/api/employer/team-members/:id`

### ✅ 03. Job Posting - Basic (Ticket #11)
- Create job listings (title, description, location)
- Job schema: salary range (ZAR), required skills, experience level
- Job status: draft (default), published, closed
- API: GET/POST /api/employer/jobs, GET /api/employer/jobs/:id
- **Status: COMPLETE** (7 integration tests passing)
- Endpoints: `/api/employer/jobs`, `/api/employer/jobs/:id`

### ✅ 04. Job Management (Ticket #12)
- Edit job listings
- Publish/close/unpublish jobs (status transitions)
- View job metrics (placeholder for applications)
- API: PATCH /api/employer/jobs/:id, POST /api/employer/jobs/:id/{publish,close,unpublish,metrics}
- **Status: COMPLETE** (7 integration tests passing)
- Endpoints: `/api/employer/jobs/:id/publish`, `/api/employer/jobs/:id/close`, `/api/employer/jobs/:id/unpublish`, `/api/employer/jobs/:id/metrics`

### ✅ 05. Job Search - Candidate Side (Ticket #13)
- Candidates search jobs by title, location, skills, salary
- Filter by job status (published only)
- Pagination: 20 results per page, sorting by date/salary
- API: GET /api/jobs/search (with query filters)
- **Status: COMPLETE** (12 integration tests passing)
- Endpoints: `/api/jobs/search`
- Filters: `search`, `location`, `salary_min`, `salary_max`, `skills`, `sort`, `page`

### ✅ 06. Candidate Search - Employer Side (Ticket #14)
- Employers search candidates by skills, location, salary, availability
- Filter by profile status (active only)
- View candidate profiles and availability
- Pagination: 20 results per page
- API: GET /api/employer/candidates/search (employer only)
- **Status: COMPLETE** (8 integration tests passing)
- Endpoints: `/api/employer/candidates/search`
- Filters: `location`, `skills`, `salary_min`, `salary_max`, `employment_type`, `sort`, `page`

### ✅ 07. Candidate Shortlist (Ticket #15)
- Employers bookmark/shortlist candidates
- Save favorite candidates for later review
- Prevent duplicate shortlists (unique constraint)
- API: GET/POST /api/employer/shortlist, DELETE /api/employer/shortlist/:id
- **Status: COMPLETE** (5 integration tests passing)
- Endpoints: `/api/employer/shortlist`, `/api/employer/shortlist/:id`

## Future Tickets - Phase 2B & Beyond

### 08. Job Expiration & Cleanup
- Auto-expire jobs after 30 days (optional in v1)
- Archive closed jobs
- Scheduled background task

## Architecture Notes

- Separate Django app: `employers/` (parallel to `profiles/`)
- Auth: Extend Django User model for employer users
- Permissions: Role-based access control (admin, recruiter, viewer)
- Search: Database queries with filtering (scale to Elasticsearch v2)

## Dependencies

- Phase 1 (Candidate) ✅ Complete
- Auth system ✅ Complete
- User model ✅ Complete

## Summary - Phase 2A Complete ✅

**All 7 Phase 2A tickets implemented and committed:**
- 58 total integration tests (9+12+7+7+12+8+5)
- 6 new Django apps created: employers/, jobs/
- 25+ API endpoints implemented
- Role-based access control (admin, recruiter, viewer)
- Full candidate-employer marketplace infrastructure ready

**Apps & Modules:**
- `employers/`: company registration, team management, job posting, candidate search, shortlisting
- `jobs/`: candidate-facing job discovery and search
- `profiles/`: existing candidate profiles (Phase 1)
- `accounts/`: authentication (Phase 1)

**Next Steps:**
- Phase 2B (Optional): Job expiration, application flow
- Phase 3: Applications & hiring workflow (mutual hire confirmation)
- Phase 4: Commission tracking & payment processing

## Timeline

Phase 2A (tickets 01-07): ✅ COMPLETE
Phase 2B (tickets 08 + polish): ~1 week (optional)
Phase 3A (applications + hire): ~1-2 weeks
Phase 4A (payments): ~1-2 weeks
