---
status: ready-for-agent
labels: [ready-for-agent]
title: Refactor auth implementation - reduce duplication
created: 2026-10-06
---

# Refactor Auth Code Smells

## Overview

Code review identified 6 code smells in the authentication implementation (ticket #01). This ticket consolidates duplicated patterns and improves design before expanding the codebase.

## Issues Identified

1. **Duplicated token model logic**: `is_valid()` and `__str__()` methods repeated in 3 token models
2. **Duplicated serializer validation**: Password match and token expiry checks repeated
3. **Duplicated email sending**: Two nearly identical email methods
4. **Token generation scattered**: `secrets.token_urlsafe()` in 3 places
5. **Feature Envy**: Views directly manipulating User state
6. **Middle Man**: Unnecessary `get_model()` override in authentication

## Blocking Issues

Ticket #01 (User authentication) - DONE

## Related

- Code review report: authenticated backend has working implementation but code quality debt
- Password validator config also needs review: Django validators enabled but spec says no complexity rules
