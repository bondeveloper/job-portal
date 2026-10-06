# 01: User authentication (signup, login, sessions, password reset)

**What to build:** Candidate can sign up with email/password, receive a verification email, log in with credentials, stay logged in for 30 days with optional remember-me, and reset a forgotten password via email.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] POST /auth/signup: accept email and password, create user, send verification email
- [ ] POST /auth/login: accept email and password, return session token (valid for 30 days)
- [ ] POST /auth/logout: end session
- [ ] Remember-me checkbox at login extends session persistence
- [ ] POST /auth/forgot-password: send password reset email with token
- [ ] POST /auth/reset-password: validate token, update password, allow login with new password
- [ ] Duplicate email signup rejected with clear error message and login link
- [ ] Password validation: min 8 characters, no complexity rules
- [ ] Integration tests: signup → login flow, password reset flow, session expiry
