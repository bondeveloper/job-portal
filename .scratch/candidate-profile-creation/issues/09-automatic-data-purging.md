# 09: Automatic data purging after 90 days

**What to build:** A scheduled background job that runs daily and checks for candidate profiles archived for ≥90 days. Those profiles are permanently deleted (hard-delete) from the database to comply with GDPR/POPIA right to erasure.

**Blocked by:** #08 (Profile management - soft delete)

**Status:** ready-for-agent

- [ ] Scheduled job (cron or task queue) runs daily to purge old archived profiles
- [ ] Query: find all profiles where status = archived AND updated_at <= (now - 90 days)
- [ ] Hard-delete matching profiles and all associated data (skills, work history, etc.)
- [ ] Logging: log number of profiles purged per run (for audit trail)
- [ ] Error handling: if purge fails, log error and retry next day (don't crash)
- [ ] Integration tests: archive profile → verify not purged before 90 days → advance time → verify purged
