# 04: Move user state logic to serializers/services

**What to build:** Move User state manipulation (setting is_active, resetting password) from views to serializers or a dedicated service. Currently VerifyEmailView and ResetPasswordView directly manipulate user.is_active and call user.save().

**Blocked by:** #02 (Extract email service), #03 (Extract validation utilities)

**Status:** ready-for-agent

- [ ] Create UserService class with methods: activate_user(user), reset_user_password(user, new_password)
- [ ] Update VerifyEmailView to use UserService.activate_user()
- [ ] Update ResetPasswordView to use UserService.reset_user_password()
- [ ] Remove direct user state manipulation from views
- [ ] All existing tests pass
- [ ] No API changes
