# Phoenix Template: Technology Stack Documentation

This document provides an overview of the technologies, frameworks, and services used to build the Phoenix Template application. The stack was chosen to be modern, scalable, and highly productive, with a strong emphasis on supporting Test-Driven Development (TDD) workflow.

---
## Frontend

The frontend is a modern web application built with a focus on developer experience, performance, and a consistent user interface driven by our design system.

### Next.js (with React & TypeScript)

* **Role**: The primary framework for building our user interface and application shell.
* **Rationale**: We chose **Next.js** for its best-in-class performance features (like the App Router), strong TypeScript integration, and the vast ecosystem of the React library. This provides a robust foundation for our user-facing dashboard and intake forms.
* **Key Links**:
    * **Next.js Documentation**: [nextjs.org/docs](https://nextjs.org/docs)
    * **React Documentation**: [react.dev](https://react.dev/)
    * **TypeScript Documentation**: [www.typescriptlang.org/docs/](https://www.typescriptlang.org/docs/)

### Tailwind CSS

* **Role**: Our utility-first CSS framework for styling the application.
* **Rationale**: **Tailwind CSS** allows for rapid UI development and enables us to directly implement our design system tokens (colours, fonts, spacing) into the code. We are using the latest version, which uses the `@theme` directive in `globals.css` for configuration.
* **Key Links**:
    * **Tailwind CSS Documentation**: [tailwindcss.com/docs](https://tailwindcss.com/docs)

### shadcn/ui

* **Role**: Our library of UI components (buttons, forms, cards, etc.).
* **Rationale**: Unlike traditional component libraries, **shadcn/ui** allows us to copy pre-built, accessible components directly into our project. This gives us full ownership and control over the code, making it easy to customize them to match our specific design system.
* **Key Links**:
    * **shadcn/ui Documentation**: [ui.shadcn.com/docs](https://ui.shadcn.com/docs)

### Phosphor Icons

* **Role**: The icon library for the entire application.
* **Rationale**: **Phosphor Icons** provides a comprehensive, high-quality set of icons with a consistent design style, which is essential for a professional UI.
* **Key Links**:
    * **Official Website**: [phosphoricons.com](https://phosphoricons.com/)

---
## Backend

Our backend is built on Python, chosen for its mature AI/ML ecosystem and high-performance web frameworks.

### FastAPI

* **Role**: The high-performance web framework for our Python backend API.
* **Rationale**: We chose **FastAPI** for its incredible speed, asynchronous capabilities, and automatic data validation powered by Pydantic. This is perfect for building a robust API to handle our AI pipeline's structured JSON inputs and outputs.
* **Key Links**:
    * **FastAPI Documentation**: [fastapi.tiangolo.com](https://fastapi.tiangolo.com/)

---
## Database & Data Layer

We use a modern, flexible database solution that can be configured for different deployment scenarios.

### PostgreSQL

* **Role**: Our primary database for storing application data.
* **Rationale**: **PostgreSQL** provides a robust, feature-rich relational database with excellent performance and reliability. It supports JSON data types for flexible schema design and can be extended with additional functionality as needed.
* **Key Links**:
    * **PostgreSQL Documentation**: [postgresql.org/docs](https://postgresql.org/docs)

### Database Options

* **Local Development**: PostgreSQL running in Docker or locally installed
* **Production**: Can be configured to use Supabase, AWS RDS, or other managed PostgreSQL services
* **Extensions**: Support for pgvector and other PostgreSQL extensions when needed

---
## Optional AI & ML Integration

The template is designed to easily integrate AI and ML capabilities when needed.

### AI Integration Options

* **LangChain**: Framework for building AI applications with LLMs
* **OpenAI API**: Direct integration with OpenAI's models
* **Anthropic Claude**: Integration with Claude models
* **Custom ML Models**: Support for deploying custom machine learning models

### When to Add AI

* Content generation and processing
* Data analysis and insights
* Natural language processing
* Recommendation systems
* Automated workflows

---
## Tooling & Workflow

This set of tools defines our development environment, ensuring consistency, quality, and adherence to our TDD methodology.

### pnpm & Poetry

* **Role**: Our package managers for the JavaScript (frontend) and Python (backend) ecosystems, respectively.
* **Rationale**: Using **pnpm** workspaces and **Poetry** enforces consistent and reliable dependency management within our monorepo structure.
* **Key Links**:
    * **pnpm Documentation**: [pnpm.io/docs](https://pnpm.io/docs)
    * **Poetry Documentation**: [python-poetry.org/docs/](https://python-poetry.org/docs/)

### Pytest & Jest / React Testing Library

* **Role**: Our frameworks for automated testing.
* **Rationale**: **Pytest** (for the backend) and the combination of **Jest** and **React Testing Library** (for the frontend) are the industry standards for their respective ecosystems. They are the engine that powers our TDD workflow.
* **Key Links**:
    * **Pytest Documentation**: [docs.pytest.org](https://docs.pytest.org/)
    * **Jest Documentation**: [jestjs.io/docs/](https://jestjs.io/docs/)
    * **React Testing Library Documentation**: [testing-library.com/docs/react-testing-library/intro/](https://testing-library.com/docs/react-testing-library/intro/)

### Cursor

* **Role**: Our primary AI-first code editor.
* **Rationale**: We use **Cursor** to facilitate our AI-driven development workflow, leveraging its deep integration with our codebase and our custom "Project Constitution" rules.
* **Key Links**:
    * **Official Website**: [cursor.sh](https://cursor.sh/)