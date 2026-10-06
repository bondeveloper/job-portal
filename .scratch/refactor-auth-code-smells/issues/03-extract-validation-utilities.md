# 03: Extract validation utilities

**What to build:** Consolidate duplicated validation logic in serializers (password match validation, token expiry checks) into shared validator functions.

**Blocked by:** #01 (Extract token models)

**Status:** ready-for-agent

- [ ] Create validators.py with: validate_password_match(password, password_confirm)
- [ ] Create validators.py with: validate_token_expiry(token_obj)
- [ ] Update SignupSerializer to use validate_password_match()
- [ ] Update ResetPasswordSerializer to use validate_password_match() and validate_token_expiry()
- [ ] Update VerifyEmailSerializer to use validate_token_expiry()
- [ ] All existing tests pass
- [ ] No API changes
