---
alwaysApply: true
---

# Deployment Protocol Rules

## Git Workflow

- **NEVER** push directly to `main` branch
- **ALWAYS** use feature branches for development
- **ALWAYS** merge via GitHub pull requests
- **NEVER** force push to main unless absolutely necessary

## Branch Management

- Create feature branches: `git checkout -b feature/description`
- Push to feature branch: `git push origin feature/description`
- Create pull request on GitHub
- Merge via GitHub interface to trigger Vercel deployment

## Deployment Triggers

- **Primary**: GitHub merge to main triggers Vercel deployment
- **Secondary**: Force redeploy with empty commit if needed
- **Emergency**: Force push only as last resort

## Force Redeploy Protocol

```bash
# Only use when Vercel cache is corrupted
git commit --allow-empty -m "chore: Force redeploy to clear Vercel cache"
git push origin main
```

## Emergency Recovery Protocol

1. **Identify stable commit**: `git log --oneline -n 20`
2. **Reset to stable state**: `git reset --hard <commit-hash>`
3. **Clean environment**: `rm -rf .next node_modules pnpm-lock.yaml && pnpm store prune`
4. **Reinstall**: `pnpm install`
5. **Test locally**: `pnpm build && pnpm dev`
6. **Force push**: `git push origin main --force`

## Pre-Deployment Checklist

- [ ] Local build succeeds: `pnpm build`
- [ ] Development server works: `pnpm dev`
- [ ] All dynamic routes await params correctly
- [ ] No ESLint errors
- [ ] No TypeScript errors
- [ ] All feature branches merged correctly

## Post-Deployment Verification

- [ ] Check Vercel deployment logs
- [ ] Verify live site functionality
- [ ] Test critical user journeys
- [ ] Check for 404 errors on static assets
- [ ] Verify styling is applied correctly

## Common Deployment Issues

- **Styling missing**: Usually corrupted build cache
- **404 errors**: Missing static assets or build failure
- **Module not found**: Dependency conflicts or missing files
- **Params errors**: Next.js 15 migration issues

## Recovery Actions

- **Styling issues**: Force redeploy with empty commit
- **Build failures**: Check local build first, then clean environment
- **Dependency issues**: Clean install with pnpm
- **Cache issues**: Clear Vercel cache via force redeploy
