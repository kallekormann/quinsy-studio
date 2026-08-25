# Skill: Backend, Server & Database Security Auditor
**ID:** SKILL-SEC-002 
**Version:** 2026.1 
**Target:** Backend Services, APIs, Server Configurations, Database Schemas, CI/CD & Cloud Infrastructure 
**Environment:** Cursor IDE / Codebase Context 

## Objective
Analyze server-side code, API routes, database implementations, deployment configurations (Docker, K8s), and environment setups to detect, isolate, and remediate backend security flaws, access control failures, and infrastructure vulnerabilities.

---

## 1. Reference Frameworks & Security Standards
When analyzing backend systems or writing refactors, the agent MUST comply with:
*   **OWASP Top 10 API Security Risks:** Focus on BOLA, Broken Authentication, Mass Assignment, and SSRF.
*   **CIS Benchmarks:** Secure configuration guidelines for OS, Docker, and Databases (PostgreSQL, MongoDB, Redis).
*   **NIST SP 800-53 / 800-204:** Security strategies for microservices and cloud-native application architectures.

---

## 2. Vulnerability Checklist & Code Search Patterns

### A. Broken Object Level Authorization (BOLA / IDOR)
*   **Rule:** Every endpoint fetching, modifying, or deleting resource data based on an ID must strictly validate that the requesting user owns or has permission to access that specific object.
*   **Code Search Pattern:** Scan controllers/routes with patterns like `/api/v1/resource/:id` or queries using `req.params.id` or `req.body.id`.
*   **Requirement:** Flag any database query that fetches an object purely by ID without a compounding tenant, workspace, or owner check (e.g., `WHERE id = :id AND user_id = :current_user_id`).

### B. Injection Flaws (SQLi, NoSQLi, Command Injection)
*   **Rule:** Raw inputs must never be concatenated directly into query strings, database commands, or OS system execution calls.
*   **Code Search Pattern:**
    *   SQL: Raw string templates in ORMs/Query builders (`db.raw("SELECT ... " + input)`), raw Prisma `$queryRawUnsafe`.
    *   NoSQL: Dynamic object passing to MongoDB fields without validation (e.g., passing `{ $ne: null }` via JSON body).
    *   OS: `child_process.exec()`, `spawn()`, `system()`, or shell executions handling variables.
*   **Requirement:** Enforce parameterized queries, ORM safety wrappers, or strict input schema validation using libraries like Zod, Joi, or TypeBox.

### C. Mass Assignment & Improper Input Validation
*   **Rule:** Users must never be able to bind payload fields directly to database models without strict filtering.
*   **Code Search Pattern:** Look for pattern bindings like `User.update(req.body)` or `db.save(...req.body)`.
*   **Requirement:** Ensure request data passes through a strict transfer object schema (DTO) or whitelist. Malicious actors must not be able to elevate their privileges by passing variables like `{"is_admin": true, "role": "superuser"}` via a profile update payload.

### D. Server-Side Request Forgery (SSRF)
*   **Rule:** Restrict the backend from making arbitrary, unvalidated outbound HTTP requests to internal networks or external third-party endpoints based on user input.
*   **Code Search Pattern:** Look for server-side network utilities handling user-supplied URLs: `axios.get(userUrl)`, `fetch(userInput)`, webhooks processors, or PDF generation utilities parsing external imagery.
*   **Requirement:** Ensure outbound requests are validated against a strict domain whitelist or routed through an isolated proxy block that completely denies access to internal metadata endpoints (e.g., `169.254.169.254`) and local networks (`127.0.0.1`, `10.0.0.0/8`).

### E. Database Configuration & Credential Leakage
*   **Rule:** Secure database access layers, connection pools, and credentials.
*   **Code Search Pattern:** Scan `docker-compose.yml`, Dockerfiles, `knexfile.js`, database initialization scripts, and config configurations.
*   **Requirement:**
    *   Flag any cleartext database passwords, API tokens, or root user access strings (`root`/`password`).
    *   Ensure database connections utilize TLS encapsulation over wire protocols (e.g., `sslmode=require`).
    *   Flag missing indexing or lack of pagination on high-volume GET endpoints that could trigger a Database Denial of Service (DB-DoS).

### F. Broken Authentication & Session Management
*   **Rule:** Enforce cryptographically sound password hashing, secure rate-limiting, and resilient token handling.
*   **Code Search Pattern:** Look for authentication controllers, middleware, password management files.
*   **Requirement:**
    *   Ensure password hashing relies on computationally expensive algorithms like **Argon2id** or **Bcrypt** (minimum 10-12 rounds). *MD5, SHA1, and SHA256 are critical failures for credentials.*
    *   Enforce aggressive Rate Limiting on authentication vectors (`/login`, `/register`, `/reset-password`) using Redis-backed token buckets or middleware like `express-rate-limit`.

---

## 3. Operational Instructions for Cursor AI

When instructed to **"Audit this backend logic/endpoint/config for security"**, execute these steps:
1.  **Architecture Mapping:** Assess whether the code handles Auth, DB Transactions, Network/I/O processing, or Configuration management.
2.  **Threat Analysis:** Contrast the operational footprint against the exploit vectors in Section 2.
3.  **Reporting Structure:** Report any findings instantly using this layout:

### 🛡️ Backend Security Flaw Identified

| Component / Endpoint | Threat Vector | Risk Level | Exploit Scenario | Remediation / Code Fix |
| :--- | :--- | :--- | :--- | :--- |
| *e.g., controllers/invoice.js* | *BOLA / IDOR on Invoice deletion* | **CRITICAL** | *User A sends `DELETE /invoice/999` and deletes User B's invoice because backend only checks ID.* | *Add tenant validation clause to the delete query block.* |

4.  **Secure Code Implementation:** Provide a secure, production-grade rewrite of the problematic code snippet directly below the matrix table.