# 02: Extract email service and token utilities

**What to build:** Consolidate email sending patterns and token generation logic into a reusable service layer. Currently `_send_verification_email()` and `_send_reset_email()` are nearly identical, and token generation is scattered across 3 views.

**Blocked by:** #01 (Extract token models)

**Status:** ready-for-agent

- [ ] Create EmailService class with methods: send_verification_email(user), send_password_reset_email(user)
- [ ] Create TokenUtil class with method: generate_token() and shared expiry logic
- [ ] Refactor SignupView to use EmailService
- [ ] Refactor ForgotPasswordView to use EmailService
- [ ] Update token generation in LoginView, SignupView, ForgotPasswordView to use TokenUtil
- [ ] All existing tests pass
- [ ] No API changes
