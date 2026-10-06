# 02: Email verification

**What to build:** After signup, a verification email is automatically sent to the candidate's email address. Candidate clicks verification link, token is validated, and their account is marked as verified. Email verification is required before the candidate's profile can be searched by employers.

**Blocked by:** #01 (User authentication)

**Status:** ready-for-agent

- [ ] POST /auth/signup triggers email send (verification email with link/token)
- [ ] Verification email contains link with time-limited token (e.g., 24 hours)
- [ ] POST /auth/verify-email: accept token, mark user as email-verified
- [ ] Invalid or expired token returns clear error message
- [ ] Unverified user cannot proceed to profile creation
- [ ] Profile cannot be searched by employers until user is verified
- [ ] Integration tests: signup → receive email → click verification → profile ready for search
