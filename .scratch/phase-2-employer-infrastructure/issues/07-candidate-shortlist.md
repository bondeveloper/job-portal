# 07: Candidate Shortlist

**What to build:** Employers can bookmark/shortlist candidates for later reference.

**Blocked by:** #06 (Candidate Search - Employer Side)

**Status:** ready-for-agent

- [ ] Shortlist model: employer FK, candidate FK, created_at
- [ ] POST /api/shortlist: add candidate to shortlist
- [ ] GET /api/shortlist: view employer's shortlisted candidates
- [ ] DELETE /api/shortlist/:id: remove from shortlist
- [ ] Only employer that added can remove
- [ ] Integration tests: add, list, remove, not-own-shortlist error
