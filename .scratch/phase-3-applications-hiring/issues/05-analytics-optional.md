# 05: Application Notifications & Analytics (Optional)

**What to build:** Track application metrics and provide analytics dashboard data.

**Blocked by:** #02 (Application Review)

**Status:** ready-for-agent (optional for Phase 3A)

- [ ] GET /api/employer/jobs/:id/application-stats: job application metrics
  - total_applications (count)
  - applied_count, reviewed_count, rejected_count, hired_count
  - average_response_time (reviewed_at - created_at for reviewed apps)
- [ ] GET /api/employer/applications: enhanced with sorting
  - sort=-applied_at (newest first)
  - sort=status (by application status)
  - sort=job_title (by job name)
- [ ] Application status history: track all status changes with timestamps
- [ ] GET /api/my-applications/:id/history: candidate sees status changes
  - Show timeline: applied, reviewed, rejected/hired, confirmed
- [ ] Analytics reserved for future: email notifications, webhooks
- [ ] Integration tests (min 5): metrics calculation, sorting, history tracking
