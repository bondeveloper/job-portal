# 06: Fix password validator config

**What to build:** Django password validators are enabled in settings (CommonPasswordValidator, NumericPasswordValidator) but spec says "min 8 chars, no complexity rules". Currently validators don't enforce (not called during user creation), but config violates spec intent. Remove validators or update spec documentation.

**Blocked by:** None (can fix anytime)

**Status:** ready-for-agent

- [ ] Disable CommonPasswordValidator in config/settings.py
- [ ] Disable NumericPasswordValidator in config/settings.py
- [ ] Keep only MinimumLengthValidator (min 8 chars)
- [ ] Keep only UserAttributeSimilarityValidator (reasonable security)
- [ ] Verify tests still pass
- [ ] Document in spec that these two validators were disabled per spec requirement
