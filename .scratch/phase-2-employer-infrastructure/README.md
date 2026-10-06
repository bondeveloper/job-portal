---
status: ready-for-planning
labels: [phase-2, employer-infrastructure]
title: Phase 2 - Employer Infrastructure
created: 2026-10-06
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

## Tickets (7-8 planned)

### 01. Employer Account Creation
- Employer (company) registration
- Company profile (name, location, industry, size)
- Employer user creation (first admin)
- API: POST /api/employer/register

### 02. Employer Team Members
- Add/remove team members to employer
- Role-based access (admin, recruiter, viewer)
- Manage permissions
- API: CRUD for team members

### 03. Job Posting - Basic
- Create job listings (title, description, location)
- Job schema: salary range, required skills, experience level
- Job status: draft, published, closed
- API: POST /api/jobs

### 04. Job Management
- Edit job listings
- Publish/unpublish jobs
- View job metrics (applications count)
- API: PATCH /api/jobs/:id

### 05. Job Search - Candidate Side
- Candidates search jobs by title, location, skills, salary
- Filter by job status (published only)
- Bookmark/save jobs
- API: GET /api/jobs (with filters)

### 06. Candidate Search - Employer Side
- Employers search candidates by skills, location, salary, availability
- Filter by profile status (active only)
- View candidate profiles
- API: GET /api/candidates/search (employer only)

### 07. Candidate Shortlist
- Employers bookmark/shortlist candidates
- Save favorite candidates
- API: POST /api/shortlist

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

## Timeline

Phase 2A (tickets 01-06): ~2-3 weeks
Phase 2B (tickets 07-08 + polish): ~1 week
