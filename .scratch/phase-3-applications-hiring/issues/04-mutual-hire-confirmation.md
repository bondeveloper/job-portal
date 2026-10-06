# 04: Mutual Hire Confirmation

**What to build:** Candidate and employer both confirm the hire (2-way handshake). Final agreement before employment relationship created.

**Blocked by:** #02 (Application Review)

**Status:** ready-for-agent

- [ ] HireConfirmation model: application OneToOne, employer_confirmed bool, candidate_confirmed bool
- [ ] Timestamps: employer_confirmed_at, candidate_confirmed_at, hire_finalized_at
- [ ] Status field: pending_candidate, pending_employer, confirmed, declined
- [ ] Workflow: employer marks application as hired → HireConfirmation created (employer_confirmed=true)
  - Sends to candidate for acceptance
  - Candidate can accept or decline
  - Once both confirm: hire_finalized_at set, application status = hired
- [ ] GET /api/my-applications/:id/hire-status: candidate views hire offer
  - Shows employer, job, offer status, dates
  - If declined before, shows that history
- [ ] POST /api/my-applications/:id/accept-hire: candidate accepts
  - Sets candidate_confirmed=true, hire_finalized_at
  - Application status → hired
  - Can only accept once
- [ ] POST /api/my-applications/:id/decline-hire: candidate declines
  - Sets candidate_confirmed=false
  - Application status → rejected
  - Can re-apply if job still published
- [ ] GET /api/employer/applications/:id/hire-status: employer views confirmation status
  - Shows candidate's acceptance/decline status
- [ ] Only employer can initiate hire (by marking application hired)
- [ ] Candidate must explicitly accept or decline (no auto-acceptance)
- [ ] Integration tests (min 10): confirmation flow, status transitions, accept/decline, permissions
