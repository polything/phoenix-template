---
alwaysApply: true
---

# Development Workflow Rules

## Daily Development Process

1. **Start with clean environment**: Ensure no cached issues
2. **Create feature branch**: `git checkout -b feature/description`
3. **Make changes**: Develop and test locally
4. **Test thoroughly**: `pnpm build && pnpm dev`
5. **Commit changes**: `git add . && git commit -m "descriptive message"`
6. **Push to feature branch**: `git push origin feature/description`
7. **Create pull request**: Use GitHub interface
8. **Merge via GitHub**: Triggers Vercel deployment

## Code Quality Standards

- **TypeScript**: All files must be properly typed
- **ESLint**: No linting errors before commit
- **Build**: Must pass `pnpm build` locally
- **Development**: Must work with `pnpm dev`

## File Organization

- **Components**: `src/components/`
- **Pages**: `src/app/`
- **Utilities**: `src/lib/`
- **Types**: `src/types/`
- **Styles**: `src/styles/`

## Naming Conventions

- **Files**: kebab-case (e.g., `feature-component.tsx`)
- **Components**: PascalCase (e.g., `FeatureComponent`)
- **Functions**: camelCase (e.g., `handleClick`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `API_ENDPOINT`)

## Git Commit Messages

- **Format**: `type(scope): description`
- **Types**: feat, fix, docs, style, refactor, test, chore
- **Examples**:
  - `feat(directory): add provider search functionality`
  - `fix(styles): resolve CSS loading issues`
  - `chore(deps): update Next.js to 15.3.3`

## Testing Protocol

### Before Every Commit

- [ ] Code compiles without errors
- [ ] No TypeScript errors
- [ ] No ESLint warnings
- [ ] Development server runs
- [ ] Build succeeds locally

### Before Every Push

- [ ] All tests pass (if applicable)
- [ ] Feature works as expected
- [ ] No console errors
- [ ] Responsive design works

### Before Every Merge

- [ ] Pull request reviewed
- [ ] All checks pass
- [ ] Deployment successful
- [ ] Live site functional

## Environment Management

### Local Development

- **Node version**: Use project's specified version
- **Package manager**: pnpm only
- **Environment variables**: Copy from `.env.example`

### Production Deployment

- **Vercel**: Automatic deployment from GitHub
- **Environment variables**: Set in Vercel dashboard
- **Domain**: mindwerk.app

## Error Handling

### Development Errors

1. **Check console**: Look for error messages
2. **Check terminal**: Look for build errors
3. **Check network**: Look for 404 errors
4. **Check dependencies**: Ensure all packages installed

### Production Errors

1. **Check Vercel logs**: Look for deployment errors
2. **Check browser console**: Look for runtime errors
3. **Check network tab**: Look for failed requests
4. **Check environment variables**: Ensure all set correctly

## Performance Considerations

- **Bundle size**: Monitor with `pnpm build`
- **Loading speed**: Use Next.js Image component
- **SEO**: Implement proper meta tags
- **Accessibility**: Use semantic HTML and ARIA labels

## Security Best Practices

- **Environment variables**: Never commit secrets
- **API keys**: Store in Vercel environment variables
- **Input validation**: Validate all user inputs
- **HTTPS**: Always use secure connections

## Documentation

- **Code comments**: Explain complex logic
- **README**: Keep updated with setup instructions
- **API docs**: Document all endpoints
- **Component docs**: Document props and usage
