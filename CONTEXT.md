# Job Portal — Domain Model

## Entities & Core Concepts

### User Types

**Candidate**
A person seeking employment. Has a profile containing structured CV data (name, contact, skills, work history, education, certifications, portfolio links). May apply to jobs and upload supporting documents. Not tied to an employer.

**Employer**
A company or organization hiring. Represented by a team account with multiple team members (HR staff). Posts jobs and searches/filters candidate profiles. Pays commissions on successful hires.

**Employer Team Member** (or **Team User**)
A person who belongs to an Employer account (e.g., HR manager, recruiter). Can post jobs, search candidates, review applications, confirm hires, manage team members. Multiple team members per Employer.

### Job & Application

**Job Listing** (or **Job**)
A posted position by an Employer. Contains: title, description, location, salary range, required skills (from predefined list), experience level. Status: published, closed, expired. Can be edited or unpublished by the Employer or a Platform Admin.

**Candidate Profile**
Structured CV data entered by a Candidate: name, email, phone, location, skills (multi-select from predefined list), work history (company, role, dates, description), education (institution, degree, field, dates), certifications, portfolio links, availability, salary expectations. The profile IS the CV (no separate CV file upload).

**Supporting Document**
Optional file uploaded by a Candidate to supplement their profile. Types: cover letter, portfolio sample, certification image, reference. Max 5 per Candidate. Sent with each application or visible on profile.

**Skill**
A searchable, predefined tag (e.g., "Python", "Django", "AWS", "Leadership"). Both Employers (on Job Listings) and Candidates (on profiles) select from this list. Searchable and filterable.

**Application**
A Candidate applies to a Job Listing. Includes: application date, Candidate profile snapshot, optional supporting documents, status. Statuses: **applied** (initial), **shortlisted** (Employer reviewed favorably), **rejected** (Employer rejected), **withdrawn** (Candidate withdrew), **hired_confirmed** (mutual hire confirmation complete).

### Hiring & Commission

**Hire Confirmation**
Mutual agreement between Employer and Candidate that the job is filled. Both must confirm:
1. Employer confirms the Candidate was hired for the Job.
2. Candidate confirms they accepted the job offer.
Until both confirm, the Application remains in shortlist state. Once both confirm, status moves to **hired_confirmed** and commission is due.

**Commission**
Payment from Employer to Platform on a successful hire. Triggered by **hired_confirmed** status.

**Commission Invoice**
Monthly batch invoice to Employer for all confirmed hires that month. Settled via Stripe or bank transfer.

**Refund Window**
30-day period after hire confirmation. If Candidate leaves or is terminated within 30 days, Employer is refunded the commission. After 30 days, commission is non-refundable.

### Data Lifecycle

**Archive** (soft-delete)
When a Candidate deletes their account, their profile and documents are marked archived (soft-deleted), not immediately erased. Archived data is retained for 90 days to resolve hire disputes.

**Erasure** (true deletion)
After 90-day archive period, archived Candidate data is permanently deleted per GDPR right to erasure.

---

## Relationships & Constraints

| Relationship | Cardinality | Notes |
|---|---|---|
| Candidate → Profile | 1:1 | One profile per Candidate. |
| Candidate → Supporting Documents | 1:N | Max 5 documents per Candidate. |
| Candidate → Applications | 1:N | Multiple applications to different jobs. |
| Employer → Job Listings | 1:N | One Employer posts many jobs. |
| Employer → Team Members | 1:N | Multiple HR staff per Employer. |
| Job Listing → Applications | 1:N | Multiple Candidates apply to one job. |
| Application → Hire (if hired) | 1:1 | One Candidate hired per Job (exclusive). |
| Hire → Commission Invoice | N:1 | Multiple hires billed on one monthly invoice. |

---

## Search & Discovery

**Candidate Search** (by Employer)
Employers search/filter candidate profiles by: skills (predefined dropdown), location, experience level, salary range, availability. Results ranked by relevance and newest-first. Full-text search on resume/profile text also supported (PostgreSQL FTS).

**Job Search** (by Candidate)
Candidates browse and search job listings by: title, location, skills required, salary range. Can bookmark or apply directly.

---

## Terms Under Review (Awaiting Clarification)

The following need stress-testing with edge cases:

- **Off-platform hiring**: Nothing prevents a Candidate and Employer from agreeing to hire off-platform (e.g., via email). Does this defraud the Platform? Needs a policy.
- **Multiple applications**: Can one Candidate apply to multiple jobs at the same Employer? Yes, but is there a limit?
- **Job deactivation**: If an Employer unpublishes a Job before hire confirmation, what happens to pending applications?
- **Hire without shortlist**: Can an Employer hire a Candidate without shortlisting first (direct hire)? Or must all hires come from applications?
