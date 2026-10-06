# 01: Extract token model base class

**What to build:** Eliminate duplicated `is_valid()` and `__str__()` methods from EmailVerificationToken, PasswordResetToken, and SessionToken by creating a BaseToken model or mixin.

**Blocked by:** None (can refactor anytime after ticket #01)

**Status:** ready-for-agent

- [ ] Create BaseToken abstract model with common `is_valid()` and `__str__()` methods
- [ ] Update EmailVerificationToken to inherit from BaseToken
- [ ] Update PasswordResetToken to inherit from BaseToken
- [ ] Update SessionToken to inherit from BaseToken
- [ ] All existing tests pass
- [ ] No behavioral changes
