---
status: ready-for-agent
labels: [ready-for-agent]
title: Candidate Profile Creation
created: 2026-10-06
---

# Candidate Profile Creation

## Overview

Implement the candidate signup and onboarding flow, allowing candidates to create a searchable profile in the South African job market.

## Links

- **Spec**: [spec.md](./spec.md)
- **Related**: Job search (coming next)

## Acceptance Criteria

- [ ] Candidate can sign up with email/password
- [ ] Email verification required before profile is searchable
- [ ] Onboarding wizard guides through 4 steps (basic info → skills → work history → availability/salary)
- [ ] Required fields enforced; optional fields can be skipped
- [ ] Profile immediately searchable after completion
- [ ] Candidates can edit, pause, delete profiles
- [ ] Password reset via email works end-to-end
- [ ] Session lasts 30 days with "remember me" option
- [ ] Deleted profiles archived for 90 days, then auto-purged
- [ ] API contract (signup, login, profile CRUD, pause) implemented
- [ ] Integration tests at HTTP API boundary with real test database

## Blocking Issues

None. This is the entry point for the platform.

## Notes

- South African focus: ZAR currency, SA employers primary target.
- Lean profile for v1: name, email, phone, location, skills, work history, availability.
- No supporting documents, 2FA, or mobile app in v1.
