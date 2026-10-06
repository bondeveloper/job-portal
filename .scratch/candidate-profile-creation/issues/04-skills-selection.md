# 04: Skills selection

**What to build:** Candidate selects skills from a predefined list of ~80 skills, with a maximum of 10 skills per profile. Skills are stored in the profile and displayed on the candidate's public profile.

**Blocked by:** #03 (Candidate profile creation)

**Status:** ready-for-agent

- [ ] Predefined skills list: ~80 common skills (e.g., Python, React, AWS, Leadership, Project Management, etc.)
- [ ] Skills stored as JSON array or separate skill_selections table on profile
- [ ] POST /profiles/:id/skills or PATCH /profiles/:id with skills array: add/update skills
- [ ] Multi-select validation: max 10 skills per profile
- [ ] Reject skills not in predefined list
- [ ] Skills returned in GET /profiles/:id
- [ ] Searchable multi-select dropdown (type to find skills)
- [ ] Skills are required: at least 1 skill must be selected (enforced during profile creation)
- [ ] Integration tests: select skills → verify max 10 → reject unknown skills
