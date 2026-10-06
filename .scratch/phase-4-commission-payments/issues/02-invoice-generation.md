# 02: Invoice Generation

**What to build:** Group pending commissions into invoices. Generate invoice documents with line items and payment terms.

**Blocked by:** #01 (Commission Calculation & Tracking)

**Status:** ready-for-agent

- [ ] Invoice model: employer FK, total_amount, status, date_issued, due_date, invoice_number
  - Status: draft, issued, partially_paid, paid, overdue, cancelled
  - Invoice number: unique, sequential (INV-2026-001)
  - Payment terms: Net 30 (due_date = date_issued + 30 days)
  - Timestamps: created_at, issued_at, paid_at
- [ ] InvoiceLineItem model: invoice FK, commission FK, description, amount
  - Links commission to invoice line item
  - Prevents orphaned commission data
- [ ] POST /api/employer/invoices/generate: create invoice from pending commissions
  - Groups all pending commissions for employer into one invoice
  - Sets status to 'issued'
  - Auto-generates invoice_number (sequential)
  - Updates commission status: pending → invoiced
  - Sets commission.invoiced_at
  - Returns invoice details with line items
- [ ] GET /api/employer/invoices: list employer's invoices
  - Paginated: 20 per page
  - Sort: newest first
  - Shows: invoice number, date, amount, status, due_date
  - Filters: status, date_range
- [ ] GET /api/employer/invoices/:id: invoice detail
  - Shows: invoice metadata, all line items (commissions), totals
  - Shows payment status if partially/fully paid
- [ ] GET /api/admin/invoices: list all invoices (admin only)
  - Aggregated view across all employers
  - Summary: total issued, total paid, total overdue
- [ ] Validation: cannot generate invoice if no pending commissions
- [ ] Invoice PDF generation: placeholder for v2 (html-to-pdf rendering)
- [ ] Integration tests (min 10): invoice creation, line items, filtering, permissions
