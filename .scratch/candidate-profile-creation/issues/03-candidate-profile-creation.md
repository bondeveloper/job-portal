# 03: Candidate profile creation (basic info)

**What to build:** After signup and email verification, candidate enters basic information (first name, last name, phone, location) and creates their profile. Profile is stored in the database with a status field and can be viewed/updated by the candidate or viewed by employers.

**Blocked by:** #02 (Email verification)

**Status:** ready-for-agent

- [ ] POST /profiles: create candidate profile with required fields (first name, last name, location) and optional fields (phone)
- [ ] Profile includes status field (pending, active, paused, archived; defaults to pending)
- [ ] Required fields (first_name, last_name, location) cannot be empty or whitespace-only
- [ ] First and last name accept any characters (no other format validation; allow single names or pseudonyms)
- [ ] Phone is optional
- [ ] Location is free-text (no city dropdown)
- [ ] GET /profiles/:id: retrieve candidate profile by ID (any authenticated user can view; used for employer profile browsing)
- [ ] Profile schema includes: id, user_id, first_name, last_name, email (from user, read-only), phone, location, status (read-only), created_at (read-only), updated_at (read-only)
- [ ] Email prefilled from user account (read-only)
- [ ] PATCH /profiles/:id: update profile fields (only candidate can update their own profile; returns 403 if not owner)
- [ ] Integration tests: create profile → retrieve → update fields, employer viewing, permission checks
