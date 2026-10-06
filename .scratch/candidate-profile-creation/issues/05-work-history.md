# 05: Work history

**What to build:** Candidate can add, edit, and delete work history entries in their profile. Each entry includes company, role, start date, optional end date (for current roles), and description. Candidate can add multiple work history entries after initial signup.

**Blocked by:** #03 (Candidate profile creation)

**Status:** ready-for-agent

- [ ] POST /profiles/:id/work-history: add work history entry (company, role, start_date, end_date, description)
- [ ] End date is optional (if blank, indicates current role)
- [ ] PATCH /profiles/:id/work-history/:work_history_id: update work history entry
- [ ] DELETE /profiles/:id/work-history/:work_history_id: delete work history entry
- [ ] GET /profiles/:id returns all work history entries
- [ ] Work history entries are optional during initial profile creation
- [ ] Candidate can add multiple entries after signup (no limit)
- [ ] Required fields per entry: company, role, start_date
- [ ] Optional fields per entry: end_date, description (max 500 chars)
- [ ] Integration tests: add/edit/delete work history → verify persistence
