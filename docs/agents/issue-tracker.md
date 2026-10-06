# Issue tracker

This project uses local markdown files under `.scratch/` to track work.

## Structure

Issues live as directories under `.scratch/<feature-name>/`, with a `README.md` containing:
- Title and description
- Status (open, in-progress, done, wontfix)
- Labels from triage vocabulary
- Links to relevant ADRs

Example:
```
.scratch/
  user-auth/
    README.md          # Issue description, status, labels
```

## Workflow

Skills like `triage` and `to-tickets` read `.scratch/` to route work based on labels and status.
