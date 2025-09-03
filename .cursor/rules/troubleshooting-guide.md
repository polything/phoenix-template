---
alwaysApply: false
---

# Troubleshooting Guide

## Issue: Missing Styling on Production Site

### Symptoms

- Live site shows unstyled content
- 404 errors for Next.js static assets (`_next/static/...`)
- Console errors about missing CSS/JS files

### Root Causes

1. **Corrupted build cache on Vercel**
2. **Dependency conflicts from mixed package managers**
3. **Incomplete feature branch merges**
4. **Next.js 15 migration issues**

### Solutions (in order of preference)

1. **Force redeploy**: `git commit --allow-empty -m "chore: Force redeploy" && git push origin main`
2. **Clean environment locally**: `rm -rf .next node_modules pnpm-lock.yaml && pnpm store prune && pnpm install`
3. **Reset to stable commit**: `git reset --hard <stable-commit> && git push origin main --force`

## Issue: MODULE_NOT_FOUND Errors

### Symptoms

- `Cannot find module './255.js'` errors
- `Cannot find module './784.js'` errors
- Webpack runtime errors

### Root Causes

1. **Corrupted .next build cache**
2. **Dependency version conflicts**
3. **Mixed package manager usage**

### Solutions

1. **Clean build cache**: `rm -rf .next`
2. **Clean dependencies**: `rm -rf node_modules pnpm-lock.yaml`
3. **Clear global cache**: `pnpm store prune`
4. **Reinstall**: `pnpm install`
5. **Test build**: `pnpm build`

## Issue: Next.js 15 Params Errors

### Symptoms

- `"params should be awaited before using its properties"`
- `"Route used params.city. params should be awaited"`

### Root Causes

- **Next.js 15 breaking change**: params are now Promises
- **Missing await keywords**
- **Incorrect TypeScript interfaces**

### Solutions

1. **Update interfaces**: `params: Promise<{ slug: string }>`
2. **Add await**: `const { slug } = await params`
3. **Fix all dynamic routes**: Check all `[slug]` pages

## Issue: ESLint Configuration Errors

### Symptoms

- `Invalid Options: useEslintrc, extensions`
- `'extensions' has been removed`

### Root Causes

- **Incompatible ESLint configuration**
- **Old Next.js ESLint config**

### Solutions

1. **Update eslint.config.mjs** to use flat config format
2. **Remove deprecated options**
3. **Use compatible ESLint version**

## Issue: Build Failures on Vercel

### Symptoms

- Vercel deployment fails
- Build logs show errors
- Local build works but production fails

### Root Causes

1. **Environment variable issues**
2. **Dependency conflicts**
3. **Build cache corruption**

### Solutions

1. **Check Vercel environment variables**
2. **Verify local build**: `pnpm build`
3. **Clean and reinstall dependencies**
4. **Check for missing files in git**

## Issue: Feature Branch Merge Problems

### Symptoms

- Missing files after merge
- Incomplete feature integration
- Lost work after merge

### Root Causes

1. **Incorrect merge strategy**
2. **Force push overwriting changes**
3. **Branch divergence**

### Solutions

1. **Use integration branch**: `git checkout -b integration/merge-all`
2. **Merge feature branches one by one**
3. **Resolve conflicts carefully**
4. **Test thoroughly before pushing to main**

## Emergency Recovery Protocol

### When Everything is Broken

1. **Stop all development**
2. **Identify last stable commit**: `git log --oneline -n 20`
3. **Reset to stable state**: `git reset --hard <commit-hash>`
4. **Clean everything**: `rm -rf .next node_modules pnpm-lock.yaml && pnpm store prune`
5. **Fresh install**: `pnpm install`
6. **Test locally**: `pnpm build && pnpm dev`
7. **Force push**: `git push origin main --force`
8. **Monitor deployment**

## Prevention Checklist

- [ ] Always use pnpm, never npm/yarn
- [ ] Test builds locally before pushing
- [ ] Use feature branches for all development
- [ ] Merge via GitHub pull requests
- [ ] Keep dependencies up to date
- [ ] Monitor Vercel deployment logs
- [ ] Have a stable commit identified for emergencies