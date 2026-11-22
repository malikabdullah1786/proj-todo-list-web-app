## 4. API Contracts
```yaml
paths:
  /auth/register: { post: { summary: Register user } }
  /auth/token: { post: { summary: Issue JWT in HttpOnly cookie } }
  /tasks:
    get: 
      summary: List tasks (supports ?status=true/false)
      security: [{ CookieAuth: [] }]
    post: { summary: Create task }
  /tasks/{id}:
    patch: { summary: Update task }
    delete: { summary: Delete task }
```