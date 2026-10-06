# 03: Job Posting - Basic

**What to build:** Employers can create and publish job listings with title, description, location, salary, required skills, and experience level.

**Blocked by:** #01 (Employer Account Creation)

**Status:** ready-for-agent

- [ ] Job model: employer FK, title, description, location, salary_min, salary_max (ZAR)
- [ ] Job fields: required_skills (multi-select), experience_level, status (draft/published/closed)
- [ ] POST /api/jobs: create job (employer users only)
- [ ] GET /api/jobs/:id: retrieve job details
- [ ] Job status: defaults to draft, can be published by recruiter+ role
- [ ] Only published jobs visible to candidates
- [ ] Validation: title required, location required, salary_min/max validated
- [ ] Integration tests: create job, validation, permission checks
