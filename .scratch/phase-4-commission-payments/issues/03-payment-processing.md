# 03: Payment Processing

**What to build:** Process payments through AddPay payment gateway. Handle payment callbacks and status reconciliation.

**Blocked by:** #02 (Invoice Generation)

**Status:** ready-for-agent

- [ ] Payment model: invoice FK, amount (ZAR), status, payment_method, payment_reference
  - Status: pending, processing, completed, failed, refunded
  - Payment method: bank_transfer, credit_card, paycloud_balance
  - Timestamp: created_at, completed_at, refunded_at
  - Transaction ID from payment gateway
- [ ] Payment gateway integration: mock PayCloud API (real integration v2)
  - Mock: /api/webhooks/payment-callback accepts payment confirmations
  - Real: integrate with AddPay PayCloud gateway for production
- [ ] POST /api/employer/invoices/:id/pay: initiate payment (redirect to payment page)
  - Create Payment record with status: pending
  - Return payment_url for redirect to payment gateway
  - Contains: invoice_id, amount, employer_email, return_url
- [ ] POST /api/webhooks/payment-callback: payment provider callback endpoint
  - Receives payment confirmation (webhook or polling)
  - Validates payment_reference matches Payment record
  - Updates Payment.status: processing → completed
  - Updates Invoice.status: issued → partially_paid (or paid if full amount)
  - Updates Commission.status: invoiced → paid
  - Sets Commission.paid_at timestamp
  - Idempotent: safe to receive duplicate webhooks
- [ ] GET /api/employer/payments: payment history
  - Shows: invoice, amount, status, date, transaction ID
  - Filters: status, date_range
- [ ] GET /api/admin/payments: admin view of all payments
  - Reconciliation report: expected vs received amounts
  - Failed payments: retry capabilities
- [ ] Error handling: failed payments, timeouts, partial payments
- [ ] Refund support: POST /api/admin/payments/:id/refund (mark for refund processing)
- [ ] Integration tests (min 12): payment creation, callbacks, status updates, refunds, permissions
