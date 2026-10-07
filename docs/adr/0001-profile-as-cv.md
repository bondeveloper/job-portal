# ADR 0001: Profile-as-CV — Structured Profile Instead of CV File Upload

**Status:** Accepted  
**Date:** 2026-10-07  
**Context:** Candidates need to provide their work history, education, certifications, and other CV data to employers.

## Problem

Two approaches to candidate CV data:

1. **File upload** (traditional): Candidates upload a PDF/DOCX CV. Simple to implement, but:
   - Unstructured data (impossible to search by skills, experience level, location)
   - Accessibility issues (employers can't filter candidates by criteria)
   - Duplicate data entry if candidate applies to multiple jobs
   - Archive/deletion is complex (need to track document links)

2. **Structured profile** (chosen): Candidates fill out a form with name, skills, work history, education, certifications, portfolio links, etc. The profile IS the CV.

## Decision

Candidates provide CV data as a **structured profile**, not a file upload. Supporting documents (cover letter, portfolio samples, references) are uploaded separately as optional supplements.

### Profile Fields (Required)
- Name, email, phone, location
- Skills (multi-select from predefined list)
- Work history (company, role, dates, description)
- Education (institution, degree, field, graduation date)

### Supporting Documents (Optional)
- Max 5 files per candidate
- Types: cover letter, portfolio sample, certification, reference
- Uploaded with each application or visible on profile

## Rationale

| Aspect | File Upload | Structured Profile |
|--------|-----|-------|
| **Searchability** | ❌ No | ✅ Yes — filter by skills, location, experience |
| **Candidate UX** | ✅ Faster (just upload) | ⚠️ More form fields, but reusable across jobs |
| **Employer UX** | ❌ Manual review | ✅ Automated search/filter |
| **Data Quality** | ❌ Variable (depends on CV format) | ✅ Consistent |
| **Archive/Deletion** | ❌ Complex (track files) | ✅ Simple (just delete record) |
| **Commission Disputes** | ❌ Hard to audit | ✅ Easy (data is in DB) |

**Trade-off:** Candidates spend more time upfront filling out forms, but this is offset by:
- Ability to apply to jobs without re-entering data
- Employers find better matches (lower candidate spam)
- Better GDPR compliance (structured data is easier to audit/export)

## Consequences

### Positive
- Employers can search by skills, location, experience level
- Candidates can apply to multiple jobs without re-uploading
- Archive/deletion is GDPR-compliant and simple
- Candidate profile data is queryable (analytics, metrics)
- Hire confirmation disputes are auditable (all data is in DB)

### Negative
- Higher friction for first signup (more form fields)
- Candidates may abandon incomplete profiles
- Requires good UX design to avoid drop-off
- Need to keep predefined skills list up-to-date

## Implementation Notes

- Use a multi-step form for candidate signup (progressive disclosure)
- Consider "quick signup" with email/password, then "complete profile" flow
- Add form auto-save to reduce frustration
- Pre-populate skills, education dropdowns with common values

## Decision Reversibility

**Hard to reverse.** Changing to file-based CVs would require:
- Migrating historical profile data to files
- Rebuilding search/filter from scratch
- Re-implementing archive/deletion logic
- Potential data loss if not carefully migrated

This is a foundational choice that affects database schema, search, and UX.
