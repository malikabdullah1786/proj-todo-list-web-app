## 2. Topology
- **Client (Browser)**: Next.js SPA; state managed via React Query; auth tokens stored in `HttpOnly` cookies.
- **API (FastAPI)**: Stateless REST service; CORS restricted to `http://localhost:3000`; JWT validation via `OAuth2PasswordBearer` (cookie-aware).
- **Database (PostgreSQL)**: Async connection pool; `owner_id` indexing for row-level isolation.

## 5. Directory Tree
```text
task-manager/
├── backend/
│   ├── alembic/
│   │   ├── versions/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app/
│   │   ├── routers/{auth.py, tasks.py}
│   │   ├── {main.py, database.py, models.py, schemas.py, auth.py}
│   ├── alembic.ini
│   └── pyproject.toml
└── frontend/
    ├── src/
    │   ├── app/
    │   │   ├── layout.tsx, page.tsx, dashboard/page.tsx
    │   │   └── login/page.tsx
    │   ├── components/{TaskCard.tsx, TaskForm.tsx}
    │   ├── lib/{api.ts, auth.ts}
    │   └── middleware.ts
    ├── package.json
    └── tailwind.config.js
```