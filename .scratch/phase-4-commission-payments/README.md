---
status: ready-for-planning
labels: [phase-4, commission-payments]
title: Phase 4 - Commission Tracking & Payments
created: 2026-10-06
---

# Phase 4: Commission Tracking & Payments

## Overview

Build the revenue model: track commissions on successful hires, generate invoices for employers, and process payments through AddPay's payment infrastructure.

## Goals

1. ✅ Calculate commissions on successful hires (fixed % or tiered)
2. ✅ Track commission status (pending, invoiced, paid)
3. ✅ Generate invoices for employer payment
4. ✅ Integrate with payment gateway (PayCloud via AddPay)
5. ✅ Track payment status and reconciliation
6. ✅ Provide admin dashboard for commission analytics

## Tickets - Phase 4A (3-4 planned)

### 01. Commission Calculation & Tracking
**What to build:** Automatically calculate commissions on hire confirmation. Track commission status lifecycle.

**Blocked by:** Phase 3 complete (hire confirmation)

**Status:** ready-for-agent

- [ ] Commission model: hire_confirmation FK, employer FK, amount (ZAR), status, timestamps
- [ ] Commission status: pending, invoiced, disputed, paid, refunded
- [ ] Commission rate: configurable % (default 10% of salary min for first 3 months)
- [ ] Auto-create Commission on hire confirmation
- [ ] Commission amount = (salary_min * commission_rate) e.g., 150000 * 0.10 = 15000 ZAR
- [ ] GET /api/admin/commissions: list all commissions with filters
- [ ] GET /api/employer/commissions: list employer's commissions and revenue
- [ ] Integration tests: creation, filtering, calculations

### 02. Invoice Generation
**What to build:** Group commissions into invoices, generate invoice documents, track payment terms.

**Blocked by:** #01 (Commission Calculation)

**Status:** ready-for-agent

- [ ] Invoice model: employer FK, date_issued, due_date, amount (sum of commissions)
- [ ] Invoice status: draft, issued, partially_paid, paid, overdue, cancelled
- [ ] InvoiceLineItem model: invoice FK, commission FK, description, amount
- [ ] Invoice number: unique, sequential (INV-2026-001, INV-2026-002)
- [ ] POST /api/employer/invoices/generate: create invoice from pending commissions
- [ ] GET /api/employer/invoices: list invoices
- [ ] GET /api/employer/invoices/:id: view invoice detail with line items
- [ ] Invoice PDF generation (placeholder for v2: html-to-pdf rendering)
- [ ] Integration tests: invoice creation, line items, filtering

### 03. Payment Processing
**What to build:** Process payments through AddPay payment gateway. Track payment status and reconciliation.

**Blocked by:** #02 (Invoice Generation)

**Status:** ready-for-agent

- [ ] Payment model: invoice FK, amount (ZAR), status, payment_method, reference
- [ ] Payment status: pending, processing, completed, failed, refunded
- [ ] Payment gateway integration: PayCloud API (mock for MVP)
- [ ] POST /api/employer/invoices/:id/pay: initiate payment (employer-initiated or redirect to payment page)
- [ ] POST /api/webhooks/payment-callback: webhook endpoint for payment provider callbacks
- [ ] Payment callback validates signature and updates payment status
- [ ] Automatic invoice status update on payment completion
- [ ] Commission status → paid when payment succeeds
- [ ] GET /api/employer/payments: list payment history
- [ ] Integration tests: payment creation, status updates, webhook handling

### 04. Commission Analytics & Admin Dashboard (Optional)
**What to build:** Admin view for commission tracking, revenue analytics, dispute management.

**Blocked by:** #03 (Payment Processing)

**Status:** ready-for-agent (optional)

- [ ] GET /api/admin/analytics/revenue: total revenue, by month, by employer
- [ ] GET /api/admin/analytics/commissions: commission metrics, pending amount, paid amount
- [ ] GET /api/admin/commissions/:id/dispute: mark commission as disputed
- [ ] PATCH /api/admin/commissions/:id: approve, reject, or adjust commission
- [ ] Admin audit trail: log all commission changes with reason and actor
- [ ] Commission reconciliation report: pending vs actual payments
- [ ] GET /api/admin/payments/reconciliation: payment status for all invoices
- [ ] Dispute workflow: mark disputed → investigate → approve/reject → close

## Architecture Notes

- Commission model tracks per-hire commissions
- Invoice model groups commissions into billing statements
- Payment model tracks actual payments received
- Payment gateway integration via AddPay's PayCloud API
- Webhook endpoints for asynchronous payment confirmations
- Idempotent payment endpoints to handle retries safely

## Key Business Rules

- Commission rate: 10% of salary_min (configurable)
- Commission trigger: on hire confirmation (both parties accept)
- Payment terms: Net 30 (invoice due 30 days from issue)
- Refund: full refund if hire cancelled/disputed within 30 days
- Payment methods: bank transfer, credit card, PayCloud balance
- Multi-currency: ZAR primary, support for USD/GBP in v2

## Dependencies

- Phase 1 (Candidate profiles) ✅ Complete
- Phase 2A (Employer infrastructure) ✅ Complete
- Phase 3A (Applications & hiring) ✅ Complete
- Payment gateway credentials (PayCloud API key)

## Timeline

Phase 4A (tickets 01-03): ~2-3 weeks
Phase 4B (ticket 04 + polish): ~1 week (optional)
Phase 4C (integrations): ~1-2 weeks (payment provider, webhooks, reconciliation)
