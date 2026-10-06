# 08: Profile management (edit, pause, delete)

**What to build:** Candidate can edit any field in their profile, pause their profile to hide it from employer search without deleting, and delete their profile (soft-archive). Paused profiles can be unpaused. Deleted profiles are soft-deleted and archived for 90 days before permanent erasure.

**Blocked by:** #03 (Candidate profile creation)

**Status:** ready-for-agent

- [ ] PATCH /profiles/:id: full edit of any profile field (name, phone, location, skills, work history, availability, salary)
- [ ] PATCH /profiles/:id/pause: toggle profile between active and paused status
- [ ] Paused profile not visible in employer search (status = paused)
- [ ] Candidate can unpause profile anytime (status = paused → active)
- [ ] DELETE /profiles/:id: soft-delete profile (status = active → archived)
- [ ] Archived profile not visible to employers
- [ ] Archived data retained for 90 days (for dispute resolution on successful hires)
- [ ] Candidate applications remain visible to employers even after profile archived (shared record)
- [ ] Candidate can view archived profile during 90-day window (for reference)
- [ ] Integration tests: edit profile → pause/unpause → delete → verify archived
