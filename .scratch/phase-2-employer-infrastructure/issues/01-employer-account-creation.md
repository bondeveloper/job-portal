# 01: Employer Account Creation

**What to build:** Employers can register company accounts and become admin users. Company profile captures name, location, industry, and company size.

**Blocked by:** None (can start immediately - Phase 1 auth already complete)

**Status:** ready-for-agent

- [ ] Employer model: company name, location, industry, size, created_at, updated_at
- [ ] EmployerUser model: user relationship, role (admin, recruiter, viewer), created_at
- [ ] POST /api/employer/register: register company + create admin user
- [ ] GET /api/employer/profile: retrieve current employer's company profile
- [ ] Employer authentication: users know which employer they belong to
- [ ] Validation: company name required, unique email per user
- [ ] Integration tests: registration flow, duplicate email rejection, profile retrieval
