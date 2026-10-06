# 05: Job Search - Candidate Side

**What to build:** Candidates can search and filter published job listings by title, location, skills, and salary range.

**Blocked by:** #03 (Job Posting - Basic)

**Status:** ready-for-agent

- [ ] GET /api/jobs: list published jobs (paginated)
- [ ] Filter by: title (search), location, salary_min/max range, required_skills
- [ ] Sort by: newest, salary, relevance
- [ ] Only show status=published jobs to candidates
- [ ] Search query: text search on title + description
- [ ] Pagination: 20 results per page
- [ ] Integration tests: filters, sorting, pagination, hidden jobs
