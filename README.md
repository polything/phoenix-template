# Project Phoenix

**AI-Enhanced Autonomous Content Pipeline**

A full-stack monorepo featuring a FastAPI backend and Next.js frontend, built with modern development practices and comprehensive AI-assisted development workflows.

## 🏗️ Architecture

This is a monorepo containing:

- **Backend**: FastAPI application with Poetry dependency management
- **Frontend**: Next.js 15 with TypeScript, Tailwind CSS, and shadcn/ui
- **Design System**: Centralised design tokens and component guidelines
- **Development Rules**: Comprehensive AI assistant guidelines and workflows

## 📁 Project Structure

```
├── apps/
│   ├── backend/          # FastAPI Python application
│   └── frontend/         # Next.js TypeScript application
├── packages/             # Shared packages (future)
├── design-system/        # Design system documentation
├── docs/                 # Project documentation
├── .cursor/rules/        # AI assistant development rules
└── snippets/             # Code snippets and examples
```

## 🚀 Quick Start

### Prerequisites

- Node.js (version specified in `.nvmrc`)
- Python 3.9+
- pnpm (package manager)
- Poetry (Python dependency management)

### Development Setup

1. **Install dependencies**:
   ```bash
   # Install frontend dependencies
   cd apps/frontend && pnpm install
   
   # Install backend dependencies
   cd apps/backend && poetry install
   ```

2. **Run development servers**:
   ```bash
   # Frontend (Next.js)
   cd apps/frontend && pnpm dev
   
   # Backend (FastAPI)
   cd apps/backend && poetry run uvicorn src.backend.main:app --reload
   ```

## 🤖 AI Assistant Rules & Guidelines

This project includes comprehensive guidelines for AI-assisted development located in `.cursor/rules/`. These rules ensure consistent, high-quality code generation and development practices.

### Core Development Rules

| Rule File | Purpose | Always Applied |
|-----------|---------|----------------|
| **[standards.mdc](.cursor/rules/standards.mdc)** | General coding and project standards including design system usage, conventional commits, and language-specific guidelines | ✅ |
| **[tdd.mdc](.cursor/rules/tdd.mdc)** | Test-Driven Development methodology - the primary development approach for this project | ✅ |

### Workflow & Process Rules

| Rule File | Purpose | Always Applied |
|-----------|---------|----------------|
| **[development-workflow.md](.cursor/rules/development-workflow.md)** | Daily development process, code quality standards, file organisation, and testing protocols | ✅ |
| **[branching-protocol.md](.cursor/rules/branching-protocol.md)** | Git workflow guidelines for feature branches, syncing, and pull request management | ❌ |
| **[deployment-protocol.md](.cursor/rules/deployment-protocol.md)** | Deployment procedures, environment management, and recovery protocols | ✅ |
| **[package-management.md](.cursor/rules/package-management.md)** | Package manager consistency rules (pnpm-only) and dependency management | ✅ |

### Technology-Specific Rules

| Rule File | Purpose | Always Applied |
|-----------|---------|----------------|
| **[nextjs-supplement.md](.cursor/rules/nextjs-supplement.md)** | Next.js-specific development guidelines, project awareness, and AI behaviour protocols | ✅ |

### Documentation & Process Rules

| Rule File | Purpose | Always Applied |
|-----------|---------|----------------|
| **[create-prd.mdc](.cursor/rules/create-prd.mdc)** | Guidelines for generating Product Requirements Documents (PRDs) from user prompts | ❌ |
| **[process-task-list.mdc](.cursor/rules/process-task-list.mdc)** | Task list management for tracking progress on PRD implementation | ❌ |
| **[troubleshooting-guide.md](.cursor/rules/troubleshooting-guide.md)** | Common issues, solutions, and recovery protocols for development and deployment | ❌ |

### Rule Categories

- **🔧 Always Applied**: Rules that are automatically applied to all AI interactions
- **📋 Contextual**: Rules that are applied based on specific contexts or when explicitly requested

## 🎨 Design System

The project includes a comprehensive design system with:

- **Colour Palette**: Purple-accent light theme with semantic colours
- **Typography**: Raleway (headlines) and Inter (body text)
- **Component Library**: Built with Tailwind CSS and shadcn/ui
- **Design Tokens**: Centralised in `design-system/01-core-elements.md`

## 🧪 Development Methodology

This project follows **Test-Driven Development (TDD)** as the primary methodology:

1. **Plan First**: Generate step-by-step plans before coding
2. **Red Phase**: Write failing tests first
3. **Green Phase**: Write minimal code to pass tests
4. **Refactor Phase**: Improve code while maintaining test coverage

## 📦 Package Management

- **Frontend**: pnpm (mandatory - never use npm/yarn)
- **Backend**: Poetry for Python dependencies
- **Monorepo**: pnpm workspaces for shared packages

## 🚢 Deployment

- **Frontend**: Automatic deployment via Vercel on GitHub merge to main
- **Backend**: Configured for containerised deployment
- **Process**: Feature branches → GitHub PR → Automated deployment

## 🔧 Development Tools

- **TypeScript**: Strict mode enabled
- **ESLint**: Next.js configuration with custom rules
- **Prettier**: Code formatting
- **Tailwind CSS**: Utility-first styling
- **shadcn/ui**: Component library

## 📚 Documentation

- **Architecture**: `docs/ARCHITECTURE.md`
- **Design System**: `design-system/01-core-elements.md`
- **API Documentation**: Auto-generated from FastAPI
- **Component Documentation**: Storybook (planned)

## 🤝 Contributing

1. Follow the branching protocol in `.cursor/rules/branching-protocol.md`
2. Adhere to TDD methodology
3. Ensure all tests pass and builds succeed locally
4. Use conventional commit messages
5. Create pull requests for all changes

## 📄 License

This project is proprietary and confidential.

---

**Built with ❤️ using AI-assisted development practices**
