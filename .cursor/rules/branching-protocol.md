# Branching Protocol Rules

## Always Start from Latest Main

### 1. Update Local Main

```bash
git checkout main
git pull origin main
```

- Ensures your local `main` is up to date with the remote repository.

### 2. Create a New Feature Branch

```bash
git checkout -b feature/your-description
```

- Always branch off from the updated `main`.

### 3. Push Your Feature Branch

```bash
git push -u origin feature/your-description
```

- Sets up the branch to track the remote.

### 4. Regularly Sync with Main During Development

```bash
git checkout main
git pull origin main
git checkout feature/your-description
git merge main
# or, for a cleaner history:
# git rebase main
```

- Keeps your feature branch up to date and reduces merge conflicts.

### 5. Complete Work and Open Pull Request

- Push your changes: `git push`
- Open a pull request on GitHub to merge into `main`
- Merge via GitHub interface (never push directly to `main`)

---

## Branching Checklist

- [ ] Local `main` is up to date before branching
- [ ] New branch created from latest `main`
- [ ] Feature branch regularly synced with `main`
- [ ] All work merged via GitHub pull request

---

## Common Issues & Recovery

- **Forgot to update main before branching:**  
  Merge or rebase latest `main` into your feature branch before opening a PR.
- **Conflicts during merge/rebase:**  
  Resolve conflicts locally, test, and push resolved branch.

---

## Summary

- **Never** branch from an outdated `main`
- **Always** keep your feature branch up to date with `main`
- **Always** merge via GitHub pull requests
