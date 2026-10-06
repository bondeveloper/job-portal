# 05: Clean authentication class

**What to build:** Remove unnecessary `get_model()` override in SessionTokenAuthentication that simply returns self.model (middle-man pattern). Also review LogoutView's fragile coupling to auth backend structure.

**Blocked by:** #01 (Extract token models)

**Status:** ready-for-agent

- [ ] Remove unnecessary get_model() override from SessionTokenAuthentication
- [ ] Verify parent TokenAuthentication.get_model() works correctly
- [ ] Review LogoutView hasattr(request, 'auth') pattern - ensure it's the right way to access auth token
- [ ] Consider cleaner method to pass token to LogoutView (via serializer or clearer method)
- [ ] All existing tests pass
- [ ] No API changes
