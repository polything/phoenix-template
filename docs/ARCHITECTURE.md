# Phoenix Template: System Architecture

## 1. Overview

This document outlines the high-level architecture for the Phoenix Template application. The system is designed as a modern, full-stack monorepo with a headless Python backend and a reactive Next.js frontend, providing a solid foundation for building various types of applications.

## 2. Architectural Principles

- **Monorepo:** A single repository (`pnpm` + `Poetry`) houses both the frontend and backend, simplifying dependency management and ensuring a single source of truth.
- **Headless Backend:** The FastAPI backend is a pure API, completely decoupled from the frontend. It is responsible for all business logic and database interactions.
- **Modern Stack:** Built with modern, well-supported technologies that provide excellent developer experience and performance.
- **Test-Driven:** Every component, from API endpoints to UI elements, is developed following a strict Test-Driven Development (TDD) methodology.
- **Component-Based UI:** The frontend is built with a reusable component architecture, governed by a well-defined design system.

---
## 3. Component Diagram

The system is composed of several key components that interact to deliver the final product.

- **User:** Interacts with the system via the Next.js frontend in a web browser.
- **Next.js Frontend (`apps/frontend`):** A React-based single-page application responsible for all user interface elements. It communicates with the FastAPI backend via RESTful API calls.
- **FastAPI Backend (`apps/backend`):** A Python-based API that serves as the central hub for the application. It handles user requests and manages all database operations.
- **Database:** A PostgreSQL database for storing persistent data. Can be configured to use Supabase, local PostgreSQL, or other database providers.

---
## 4. Data Flow Example

A typical data flow follows these steps:

1. The **User** interacts with the interface in the **Next.js Frontend**.
2. The frontend sends the data in a structured JSON payload to a specific endpoint on the **FastAPI Backend**.
3. The backend validates the incoming data using Pydantic models.
4. The backend's service layer processes the data and saves it to the **Database**.
5. The backend returns a success response to the frontend.

---
## 5. Monorepo Structure

The project is organized into a monorepo to keep all related code in a single repository.

- **`apps/`**: Contains our two main applications: the `frontend` (Next.js) and the `backend` (FastAPI).
- **`packages/`**: Intended for shared code between applications, such as generated TypeScript types from our Python schemas.
- **`docs/`**: Contains all high-level project documentation, including this file and the Tech Stack overview.
- **`design-system/`**: The source of truth for our UI, including design tokens, component guidelines, and accessibility notes.
- **`.cursor/rules/`**: The "Project Constitution" that governs the AI's behavior and enforces our development methodologies.