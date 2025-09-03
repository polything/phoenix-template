---
alwaysApply: true
---

# Package Management Rules

## Package Manager Consistency

- **MANDATORY**: Use ONLY `pnpm` for this project
- **NEVER** use `npm` or `yarn` - this causes lockfile conflicts
- **ALWAYS** use `pnpm` commands for all package operations

## Commands to Use

- Install packages: `pnpm add <package-name>`
- Remove packages: `pnpm remove <package-name>`
- Update packages: `pnpm update`
- Install dependencies: `pnpm install`
- Run scripts: `pnpm dev`, `pnpm build`, `pnpm start`

## Commands to NEVER Use

- ❌ `npm install`
- ❌ `npm add <package>`
- ❌ `yarn add <package>`
- ❌ `yarn install`

## Build Environment Management

- **Before major changes**: Clean environment completely
- **Clean command**: `rm -rf .next node_modules pnpm-lock.yaml && pnpm store prune`
- **Reinstall**: `pnpm install`
- **Verify build**: `pnpm build`

## Dependency Conflicts Prevention

- Always check `package.json` for correct package manager
- Never mix package managers in the same project
- If lockfile conflicts occur, delete all lockfiles and reinstall with pnpm
- Use `pnpm store prune` to clear global cache if needed

## Vercel Analytics Integration

- Use `pnpm add @vercel/analytics @vercel/speed-insights`
- Add components to `src/app/layout.tsx`
- Ensure proper import and usage

## Troubleshooting Steps

1. Stop development server
2. Clean environment: `rm -rf .next node_modules pnpm-lock.yaml`
3. Clear cache: `pnpm store prune`
4. Reinstall: `pnpm install`
5. Test build: `pnpm build`
6. Start dev server: `pnpm dev`
