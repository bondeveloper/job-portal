# 01: Commission Calculation & Tracking

**What to build:** Automatically calculate commissions on hire confirmation. Track commission status lifecycle and provide visibility to admins and employers.

**Blocked by:** Phase 3 complete (hire confirmation)

**Status:** ready-for-agent

- [ ] Commission model: hire_confirmation FK, employer FK, amount (ZAR), status, timestamps
  - Status: pending, invoiced, disputed, paid, refunded
  - Calculated on HireConfirmation.hire_finalized_at
- [ ] Commission rate: configurable (default 10% of job salary_min)
- [ ] Commission amount calculation: salary_min * rate (e.g., 150000 * 0.10 = 15000 ZAR)
- [ ] Auto-create Commission when HireConfirmation.status = confirmed
- [ ] Commission starts in 'pending' status (awaiting invoice)
- [ ] GET /api/admin/commissions: list all commissions (admin only)
  - Filters: status, employer_id, date_range
  - Sort: newest, by amount
  - Shows: employer, candidate, job, salary, commission amount, status
  - Pagination: 20 per page
- [ ] GET /api/employer/commissions: list employer's commissions (recruiter+ only)
  - Shows: candidate, job, salary, commission amount, status, hire date
  - Summary: total pending, total invoiced, total paid
- [ ] Timestamps: created_at, updated_at, invoiced_at, paid_at, refunded_at
- [ ] Integration tests (min 12): creation on hire, calculation, filtering, permissions
