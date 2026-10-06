# 06: Candidate Search - Employer Side

**What to build:** Employers can search and filter active candidate profiles by skills, location, salary, and availability.

**Blocked by:** #01 (Employer Account Creation) - Phase 1 profiles already complete

**Status:** ready-for-agent

- [ ] GET /api/candidates/search: list active candidate profiles (employer only)
- [ ] Filter by: skills (multi-select), location, salary range, employment_type, availability
- [ ] Only show status=active (not paused/archived) profiles
- [ ] Pagination: 20 results per page
- [ ] Sort by: newest, relevance
- [ ] Permission: employer users (recruiter+) only
- [ ] Integration tests: filters, sorting, permission checks, hidden profiles
