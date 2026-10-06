# 06: Availability & salary expectations

**What to build:** Candidate specifies their availability (start date and employment type preference) and optional salary expectations in South African Rand (ZAR). These fields are stored and searchable by employers.

**Blocked by:** #03 (Candidate profile creation)

**Status:** ready-for-agent

- [ ] Availability fields: start_date (month/year picker, required), employment_type (full-time / part-time / contract, required)
- [ ] Defaults to "immediately available, full-time" if not explicitly set
- [ ] Salary expectations: salary_min (ZAR, optional), salary_max (ZAR, optional)
- [ ] Both salary_min and salary_max optional; if provided, both must be numeric
- [ ] Validation: if both salary fields provided, salary_max must be >= salary_min
- [ ] PATCH /profiles/:id: update availability and salary fields
- [ ] GET /profiles/:id: return availability and salary data
- [ ] Salary range displayed in profile (e.g., "R60,000 – R80,000" or blank if not set)
- [ ] Employers can filter candidates by availability and salary range in search (separate feature, but schema must support it)
- [ ] Integration tests: set availability/salary → validate ranges → retrieve profile
