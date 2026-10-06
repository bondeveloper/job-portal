# 07: Profile searchability after wizard completion

**What to build:** After candidate completes all wizard steps (basic info, skills, work history, availability/salary), their profile is marked as complete and immediately becomes searchable by employers. Incomplete profiles remain invisible to employer search until all required fields are set.

**Blocked by:** #04 (Skills), #05 (Work history), #06 (Availability & salary)

**Status:** ready-for-agent

- [ ] Profile status field: pending (incomplete), active (complete and searchable), paused, archived
- [ ] Profile automatically transitions from pending → active when all required fields are set
- [ ] Required fields for searchability: first_name, last_name, location, ≥1 skill, availability_start_date, employment_type
- [ ] Optional fields do NOT block searchability: phone, work_history, salary_expectations
- [ ] GET /profiles/:id shows profile.status
- [ ] Employer search only returns profiles with status = active (separate feature, but schema must support filtering)
- [ ] Profile complete confirmation message shown to candidate after final wizard step
- [ ] Integration tests: partial profile not searchable → complete profile → verify searchable
