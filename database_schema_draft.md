## 3. Database Schema
```yaml
version: "1.0"
tables:
  users:
    columns:
      - name: id
        type: SERIAL
        constraints: [PRIMARY KEY]
      - name: username
        type: VARCHAR(50)
        constraints: [UNIQUE, NOT NULL, INDEX]
      - name: hashed_password
        type: VARCHAR(255)
        constraints: [NOT NULL]
      - name: created_at
        type: TIMESTAMP WITH TIME ZONE
        constraints: [DEFAULT NOW()]

  tasks:
    columns:
      - name: id
        type: SERIAL
        constraints: [PRIMARY KEY]
      - name: owner_id
        type: INTEGER
        constraints: [NOT NULL, REFERENCES users(id) ON DELETE CASCADE, INDEX]
      - name: title
        type: VARCHAR(255)
        constraints: [NOT NULL]
      - name: priority
        type: VARCHAR(10)
        constraints: [NOT NULL, CHECK (priority IN ('low', 'medium', 'high'))]
      - name: due_date
        type: TIMESTAMP WITH TIME ZONE
        constraints: [NOT NULL]
      - name: status
        type: BOOLEAN
        constraints: [NOT NULL, DEFAULT FALSE]
      - name: created_at
        type: TIMESTAMP WITH TIME ZONE
        constraints: [DEFAULT NOW()]
```