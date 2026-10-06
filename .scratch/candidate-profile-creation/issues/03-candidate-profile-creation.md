# 03: Candidate profile creation (basic info)

**What to build:** After signup and email verification, candidate enters basic information (first name, last name, phone, location) and creates their profile. Profile is stored in the database and candidate can view it.

**Blocked by:** #02 (Email verification)

**Status:** ready-for-agent

- [ ] POST /profiles: create candidate profile with required fields (first name, last name, location) and optional fields (phone)
- [ ] First and last name accepted as-is (no format validation, allow single names or pseudonyms)
- [ ] Phone is optional
- [ ] Location is free-text (no city dropdown)
- [ ] GET /profiles/:id: retrieve candidate's own profile
- [ ] Profile schema includes: id, user_id, first_name, last_name, email (from user), phone, location, created_at, updated_at
- [ ] Email prefilled from user account (read-only)
- [ ] PATCH /profiles/:id: update profile fields
- [ ] Integration tests: create profile → retrieve → update fields
