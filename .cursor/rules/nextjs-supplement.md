---
alwaysApply: true
---

# Next.js Development Supplement

Additional development rules and best practices for the MindWerk project, supplementing the core rules with project-specific guidelines and AI assistant behaviour protocols.

## Project Awareness & Context

### Essential Files to Check

- **Always read PLANNING.md** at the start of a new conversation to understand architecture, goals, naming schemes and constraints
- **Check TASK.md** before starting work
- **If a task is not listed**, add it with a one-line description and today's date under "Backlog"
- **When a task is finished**, move it to "Done" and append a short changelog bullet

### Architecture Compliance

- Match the file structure and conventions defined in PLANNING.md and nextjs-15-migration.md
- Use `/src/app` vs `/src/pages` as specified
- Follow server/client component patterns
- Use feature-based folders as defined

### Environment Management

- Use `pnpm dlx env-cmd` (or dotenv-flow) to load environment variables locally
- **Never hard-code secrets** in source code
- Node version is locked via `.nvmrc` – stick to it

## Code Structure & Modularity

### File Size Limits

- Keep any single file under ~300 lines (JS/TS, JSX/TSX, CSS/MDX, etc.)
- Split large React components into:
  - `ComponentName.view.tsx` (markup & styling)
  - `ComponentName.logic.ts` (hooks, helpers)
  - `ComponentName.test.tsx` (unit tests)

### Folder Structure

Prefer feature-first folders:

```text
src/
  features/
    blog/
      components/
      hooks/
      api/
      types.ts
```

### Import & Export Guidelines

- Barrel-export (`index.ts`) only when it simplifies imports – avoid circular deps
- Use absolute imports with `@/*` paths (configured in tsconfig.json)
- Never place generated files in Git (`.next`, `coverage`, `storybook-static`, etc.) - use `.gitignore`

## Testing & Reliability

### Testing Stack

- **Vitest + React-Testing-Library** for unit/component tests
- **Playwright** for E2E tests

### Test Organization

- Place tests in a `__tests__/` folder adjacent to the file under test
- Or mirror the structure in `/tests`

### Test Requirements

Each new component/util must ship with at least:

1. **1 happy-path test**
2. **1 edge-case test**
3. **1 failure/error-state test**

### Quality Gates

- Run `pnpm test --watch` locally before every commit
- CI must block merges if coverage falls below 80%

## Task Completion Workflow

### Completion Checklist

1. Finish the code & tests
2. Tick the checkbox in the relevant issue or PR template
3. Move the bullet in TASK.md to "Done" + short description of what changed
4. If you spot follow-up work, add a bullet under "Discovered During Work" in TASK.md

## Style & Conventions

### Technology Stack

- **Language**: TypeScript 5.x, React 18 server/client components, ES2022 syntax
- **Lint & format**: ESLint (next/core-web-vitals rules) + Prettier (`pnpm lint` & `pnpm format`)
- **Styling**: Tailwind CSS; component-level styles via `@apply` or CSS Modules only when Tailwind falls short

### Code Standards

- **Commit messages**: Conventional Commits (`feat:`, `fix:`, `chore:` …)
- **Docstrings/comments**: JSDoc style for exported functions & hooks

## Documentation & Explainability

### Documentation Requirements

- Update README.md whenever installation, scripts, or environment setup changes
- Component stories (Storybook) are mandatory for all public-facing UI components
- Add `// Reason:` inline comments for non-obvious logic, API hacks, or performance work-arounds

## AI Behaviour Rules (for in-editor assistants)

### Context & Assumptions

- **Ask if context is missing** – no silent assumptions
- **Never fabricate package names or APIs** – use only dependencies in package.json
- **Confirm file paths exist** before referencing them in code snippets

### Code Safety

- **Do not delete or overwrite existing code** unless the change is explicitly tied to an open task or migration step
- **When uncertain**, output a short clarification question rather than low-confidence code

## Integration Notes

This supplement should be used alongside the core rules files:

- [nextjs-15-migration.md](./nextjs-15-migration.md)
- [package-management.md](./package-management.md)
- [deployment-protocol.md](./deployment-protocol.md)
- [troubleshooting-guide.md](./troubleshooting-guide.md)
- [development-workflow.md](./development-workflow.md)

## Quick Commands Reference

```bash
# Environment setup
pnpm dlx env-cmd

# Testing
pnpm test --watch

# Linting and formatting
pnpm lint
pnpm format

# Node version check
nvm use
```
