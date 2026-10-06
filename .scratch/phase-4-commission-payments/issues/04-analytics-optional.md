# 04: Commission Analytics & Admin Dashboard (Optional)

**What to build:** Admin view for commission tracking, revenue analytics, dispute management, and reconciliation.

**Blocked by:** #03 (Payment Processing)

**Status:** ready-for-agent (optional)

- [ ] GET /api/admin/analytics/revenue: revenue metrics
  - Total revenue (all time, this month, this year)
  - By employer: top employers by commission amount
  - By month: monthly revenue trend
- [ ] GET /api/admin/analytics/commissions: commission metrics
  - Total pending commissions (unpaid)
  - Total invoiced commissions (awaiting payment)
  - Total paid commissions
  - Average commission amount
  - Commission rate distribution
- [ ] GET /api/admin/commissions/:id/dispute: mark commission as disputed
  - PATCH endpoint to update status: pending/invoiced → disputed
  - Reason: required text field (max 500 chars)
  - Prevents invoice generation for disputed commissions
- [ ] PATCH /api/admin/commissions/:id: approve, reject, or adjust commission
  - Approve: change status, allow invoicing
  - Reject: mark as refunded, prevent invoicing
  - Adjust: modify amount with reason (audit trail)
- [ ] Admin audit trail: log all commission changes
  - Created by: admin user
  - Action: created, disputed, approved, adjusted, refunded
  - Timestamp, amount (if adjusted), reason
- [ ] Commission reconciliation report:
  - GET /api/admin/reconciliation: pending vs actual payments
  - Shows: invoices awaiting payment, overdue invoices, payment mismatches
- [ ] GET /api/admin/payments/reconciliation: payment status dashboard
  - Expected payments: sum of invoices issued
  - Received payments: sum of completed payments
  - Outstanding: expected - received
  - Failed payments: retry history
- [ ] Dispute workflow endpoints:
  - Mark disputed: POST /api/admin/commissions/:id/dispute
  - Resolve dispute: PATCH /api/admin/commissions/:id (approve/reject)
  - Close dispute: auto-closed on approve/reject
- [ ] Integration tests (min 10): analytics queries, disputes, auditing
