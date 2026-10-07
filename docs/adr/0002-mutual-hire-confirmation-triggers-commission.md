# ADR 0002: Mutual Hire Confirmation Triggers Commission

**Status:** Accepted  
**Date:** 2026-10-07  
**Context:** Platform charges commission on confirmed hires. Need to define when a hire is "confirmed" and commission is due.

## Problem

Three approaches to hire confirmation:

1. **Employer-only** (early approach): Employer confirms hire → commission triggered immediately
   - ❌ Risks: Employer can claim hire without candidate knowledge; dispute risk
   - ❌ Candidate has no say in hire confirmation

2. **Candidate-only**: Candidate confirms they accepted → commission triggered
   - ❌ Candidate incentivized to NOT confirm (delays payment)
   - ❌ Employer has no recourse if candidate goes silent

3. **Mutual confirmation** (chosen): Both employer AND candidate must confirm hire → commission triggered
   - ✅ Fair to both parties
   - ✅ Lower dispute risk
   - ✅ Aligned incentives

## Decision

A **hire is confirmed only when both employer and candidate have confirmed** the hire. Commission is triggered and invoiced only after mutual confirmation.

### State Machine
```
Application → Shortlisted → Hired (unconfirmed)
                                    ↓
                    Employer Confirms Hire (employer-confirmed, candidate-pending)
                                    ↓
                    Candidate Confirms Hire (hired-confirmed) ← Commission triggered
```

### Rules
- Employer confirms first (within application review flow)
- Candidate receives notification to confirm
- Candidate has 30 days to confirm; after 30 days, employer can cancel unconfirmed hire
- If either party cancels within 30 days after mutual confirmation, commission is refunded
- After 30 days post-confirmation, hire is finalized; no new disputes allowed

## Rationale

| Aspect | Employer-Only | Mutual (Chosen) |
|--------|-------|--------|
| **Employer protection** | ✅ Quick billing | ⚠️ Candidate might not confirm |
| **Candidate protection** | ❌ No say | ✅ Must agree to hire |
| **Dispute risk** | ❌ High | ✅ Low (both agreed) |
| **Commission fairness** | ❌ Employer can game | ✅ Both parties validated |
| **GDPR compliance** | ⚠️ Unilateral action | ✅ Mutual agreement |
| **Implementation** | ✅ Simple | ⚠️ Requires notifications + state management |

**Trade-off:** Slightly more complex implementation and longer time to commission (candidate must confirm), but significantly lower dispute risk and fairer to both parties.

## Consequences

### Positive
- **Fair**: Both parties must agree before commission is due
- **Dispute-resistant**: Hard for either party to claim misunderstanding
- **Candidate retention**: Candidates feel respected (not auto-hired without consent)
- **Employer confidence**: Employer knows candidate actually accepted before being charged
- **GDPR-friendly**: Mutual consent = lawful basis for data processing

### Negative
- **Slower cash flow**: Commission not due until candidate confirms
- **Candidate friction**: Candidate must take action to finalize hire (might go silent)
- **30-day dispute window**: Employer must handle refunds if candidate leaves within 30 days
- **Complexity**: State machine is more complex than single confirmation

## Implementation Notes

1. **Notifications**: Email candidate when employer confirms, with clear "confirm hire" call-to-action
2. **Reminders**: Send reminder at day 20 if candidate hasn't confirmed
3. **Auto-cancel**: Automatically cancel unconfirmed hires after 30 days, notify employer
4. **Invoice delay**: Hold commission invoice until mutual confirmation complete
5. **Dashboard**: Show both parties the hire confirmation status clearly

## Edge Cases Handled

- **Candidate confirms but then withdraws before 30 days**: Commission refunded
- **Employer confirms, candidate silent for 30 days**: Hire auto-cancelled, no commission
- **Both confirm, then candidate leaves on day 5**: Commission refunded per refund window policy
- **Both confirm, then candidate leaves on day 40**: No refund (past 30-day window)

## Decision Reversibility

**Hard to reverse.** Changing to employer-only confirmation would require:
- Changing hire state machine (database migration)
- Removing candidate confirmation email/UI flow
- Re-implementing commission trigger logic
- Handling existing mutual confirmations (what happens?)
- Potentially refunding commissions already charged

This is a core business logic decision that affects invoicing, disputes, and customer relationships.

## Related Decisions

- See ADR 0001 (Profile-as-CV) for how candidate profile data supports hire auditing
- See CONTEXT.md for "Hire Confirmation" and "Refund Window" definitions
