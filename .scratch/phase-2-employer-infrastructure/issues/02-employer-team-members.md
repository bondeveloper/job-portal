# 02: Employer Team Members

**What to build:** Employer admins can manage team members with role-based access control (admin, recruiter, viewer).

**Blocked by:** #01 (Employer Account Creation)

**Status:** ready-for-agent

- [ ] POST /api/employer/team-members: admin adds team member (email + role)
- [ ] GET /api/employer/team-members: list team members
- [ ] PATCH /api/employer/team-members/:id: update role
- [ ] DELETE /api/employer/team-members/:id: remove team member
- [ ] Roles: admin (manage team, post jobs, review apps), recruiter (post jobs, search, review), viewer (search only)
- [ ] Permission checks: only admin can manage team
- [ ] Email invitation flow (v2 optional)
- [ ] Integration tests: add/remove/update members, permission checks
