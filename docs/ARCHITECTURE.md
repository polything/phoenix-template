# Project Phoenix: System Architecture

## 1. Overview

This document outlines the high-level architecture for the Project Phoenix application. The system is designed as a modern, full-stack monorepo with a headless Python backend and a reactive Next.js frontend. The core business logic is encapsulated in an AI-driven pipeline orchestrated by LangChain.

## 2. Architectural Principles

- **Monorepo:** A single repository (`pnpm` + `Poetry`) houses both the frontend and backend, simplifying dependency management and ensuring a single source of truth.
- **Headless Backend:** The FastAPI backend is a pure API, completely decoupled from the frontend. It is responsible for all business logic, AI orchestration, and database interactions.
- **AI-First:** The system is built around an AI core. Key components like LangChain, LangSmith, and OpenRouter are integral to the design, not afterthoughts.
- **Test-Driven:** Every component, from API endpoints to UI elements, is developed following a strict Test-Driven Development (TDD) methodology.
- **Component-Based UI:** The frontend is built with a reusable component architecture, governed by a well-defined design system.

---
## 3. Component Diagram

The system is composed of several key components that interact to deliver the final product.



- **User (Marketing Strategist):** Interacts with the system via the Next.js frontend in a web browser.
- **Next.js Frontend (`apps/frontend`):** A React-based single-page application responsible for all user interface elements, including the intake form, dashboard, and review screens. It communicates with the FastAPI backend via RESTful API calls.
- **FastAPI Backend (`apps/backend`):** A Python-based API that serves as the central hub for the application. It handles user requests, orchestrates the AI pipeline, and manages all database operations.
- **Supabase (Database):** Our managed PostgreSQL database. It stores all persistent data, including client profiles, pipeline stage outputs (`JSONB`), and vector embeddings (`pgvector`).
- **AI Core (LangChain & LangSmith):** Running within the FastAPI backend, LangChain orchestrates the multi-step AI processes. LangSmith traces and monitors every AI call for debugging and observability.
- **OpenRouter (AI Gateway):** An external service that our backend calls. It acts as a unified gateway to various Large Language Models (LLMs), providing flexibility and cost-optimization.

---
## 4. Data Flow Example: Client Intake

A typical data flow for the initial "Client Intake" feature follows these steps:

1. The **User** fills out the intake form in the **Next.js Frontend**.
2. The frontend sends the form data in a structured JSON payload to a specific endpoint on the **FastAPI Backend**.
3. The backend validates the incoming data using Pydantic models.
4. The backend's service layer saves the validated client profile to the **Supabase** database.
5. The backend returns a success response to the frontend.
6. (In subsequent steps) The backend will use **LangChain** to fetch this client data from Supabase, process it, make calls to **OpenRouter**, and trace the entire operation with **LangSmith**.

---
## 5. Monorepo Structure

The project is organized into a monorepo to keep all related code in a single repository.

- **`apps/`**: Contains our two main applications: the `frontend` (Next.js) and the `backend` (FastAPI).
- **`packages/`**: Intended for shared code between applications, such as generated TypeScript types from our Python schemas.
- **`docs/`**: Contains all high-level project documentation, including this file, the PRD, and the Tech Stack overview.
- **`design-system/`**: The source of truth for our UI, including design tokens, component guidelines, and accessibility notes.
- **`.cursor/rules/`**: The "Project Constitution" that governs the AI's behavior and enforces our development methodologies.