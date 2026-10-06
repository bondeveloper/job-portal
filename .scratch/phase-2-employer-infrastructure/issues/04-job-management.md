# 04: Job Management

**What to build:** Employers can edit jobs, publish/unpublish, view metrics, and manage job lifecycle.

**Blocked by:** #03 (Job Posting - Basic)

**Status:** ready-for-agent

- [ ] PATCH /api/jobs/:id: edit job (title, description, location, salary, skills)
- [ ] POST /api/jobs/:id/publish: change status from draft → published
- [ ] POST /api/jobs/:id/close: change status to closed (no more applications)
- [ ] POST /api/jobs/:id/unpublish: revert published → draft
- [ ] GET /api/jobs/:id/metrics: application count, views (basic)
- [ ] Permission: only employer that posted can edit/manage
- [ ] Validation: cannot edit published job (create new instead, v2)
- [ ] Integration tests: edit, publish, close, permission checks
