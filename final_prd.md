# Product Requirements Document

## 1. Overview & Goals
- **Problem**: Users lack a secure, isolated, minimalist workspace to manage prioritized and scheduled personal tasks across sessions.
- **Benefits**: Instantaneous local-only CRUD operations with due-date tracking and priority sorting via a decoupled, high-performance async API and responsive UI.
- **KPI Metrics**: 100% data isolation compliance per user ID; <100ms API response time for local CRUD actions; 0 unhandled database session leaks.

## 2. Personas (Compact)
- [Task Owner]: Authenticated individual managing private daily to-do lists with specific priorities and deadlines, requiring secure session persistence and frictionless CRUD operations.

## 3. User Stories & Epics (Dense List)
* [Epic: Auth] As a visitor, I want to sign up and log in securely so that my tasks remain private.
  - AC: [1] Given valid credentials, When POST /auth/register, Then user is created and 201 returned. [2] Given invalid credentials, When POST /auth/token, Then 401 Unauthorized is returned. [3] Given active JWT, When accessing protected endpoints, Then user context is established.
* [Epic: Tasks] As a user, I want to create, read, update, and delete tasks with priority and due dates so that I can track and schedule my work effectively.
  - AC: [1] Given authenticated session, When POST /tasks with title, priority (low/medium/high), and due_date, Then task is created with status=false linked to owner_id. [2] Given owner's task ID, When GET /tasks, Then return user's task list sorted by priority/due date. [3] Given task ID, When PATCH /tasks/{id}, Then update status, title, priority, or due_date successfully. [4] Given task ID, When DELETE /tasks/{id}, Then remove record.

## 4. Functional Specs (Bullet Tree)
- Frontend Screens (Next.js + Tailwind CSS)
  - `/login` & `/register` -> Form validation (min 3 chars username, 6 chars password) -> Success: Store JWT in HTTP-only cookie / secure state, Redirect to `/dashboard`, Error: Inline toast notification.
  - `/dashboard` -> Task list grid with priority badges and due dates, inline create input with priority/date pickers, status toggle checkbox, delete icon -> Success: Optimistic UI updates, Error: Revert state & alert user.
- Backend Rules & Endpoints (FastAPI + PostgreSQL)
  - `POST /auth/register` -> Validate uniqueness of username -> Hash password via `passlib[bcrypt]` -> Save `User` model.
  - `POST /auth/token` -> OAuth2 compatible form parsing -> Issue `python-jose` signed JWT (30m expiry).
  - `GET/POST /tasks` -> Extract user from JWT via `OAuth2PasswordBearer` -> Validate task fields (`priority` enum: low/medium/high, `due_date` ISO-8601) -> Scope all SQLAlchemy queries to `owner_id = current_user.id`.
  - `PATCH/DELETE /tasks/{id}` -> Verify task existence AND `owner_id == current_user.id` -> Success: Execute commit, Error: 403 Forbidden or 404 Not Found.

## 5. Non-Functional Requirements
- **Performance**: API response time < 100ms for local queries; Next.js asset delivery optimized for local dev.
- **Security**: Passwords salted/hashed via bcrypt; JWT tokens signed securely; FastAPI CORS middleware explicitly whitelisting `http://localhost:3000`.
- **Reliability**: SQLAlchemy dependency injection (`get_db`) guaranteeing automated session commit/rollback and connection closure per request
.
- **Compatibility**: Modern browsers (Chrome, Firefox, Safari) running local environments (Node.js 18+, Python 3.10+, PostgreSQL 15+).

## 6. Out of Scope & Release Plan
- **Out of Scope**: 
  - 1. Social/OAuth login providers (Google, GitHub).
  - 2. Collaborative task sharing, workspaces, or public links.
  - 3. Production cloud deployment pipelines or CI/CD automation.
- **Release Plan**:
  - Phase 1 (Local Setup): Initialize PostgreSQL DB instances, configure FastAPI backend schema with priority/due_date attributes, and verify migrations.
  - Phase 2 (Core Logic & UI): Implement FastAPI auth/CRUD endpoints and build corresponding Next.js Tailwind views incorporating priority/date pickers.
  - Phase 3 (Integration & Validation): Execute end-to-end local testing verifying CORS, user data isolation, and error handling.