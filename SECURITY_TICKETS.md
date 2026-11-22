## [SEC-1795379955] Potential hardcoded secret in backend/app/auth.py
**Severity:** HIGH

**Mitigation Plan:**
Remove any hardcoded secrets, API keys, or JWT signing keys from backend/app/auth.py and load them securely from environment variables using os.environ or a configuration management system like pydantic-settings.

---

