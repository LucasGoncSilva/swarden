# Software Architecture Document (SAD)

## 1. Document Purpose and Overview

> The Software Architecture Document (SAD) serves as the "source of truth" for the system's structural design. Its primary intention is to provide a high-level map of how the application is built, why certain architectural patterns were chosen, and how various components interact to meet functional and non-functional requirements. For a Secret Manager, the SAD is critical because it documents the "Trust Boundary" - where data is encrypted and where it is vulnerable. The benefits are three-fold: first, it ensures **Design Consistency**, preventing "ad-hoc" features that might bypass security protocols. Second, it facilitates **Knowledge Transfer**, allowing future collaborators (or your future self) to understand the "why" behind the code. Third, it acts as a **Security Audit Baseline**, mapping out data flows to identify potential attack vectors like SQL injection or IDOR before a single line of code is written. It transforms a collection of scripts into a professional, engineered system.

## 2. Architectural Representation

- **Architecture Style:** Monolith Archtecture
- **Language/Framework:** Python + Django, Rust
- **Pattern:** Standard Django MVC/MVT

## 3. Architecture Goals and Constraints

- **Security (Primary):** Captcha + Rate Limit + Anonymizaion + Encriptation at-Rest
- **Portability:** Docker-based Deployment with Linux Image
- **Scalability:** 120 req/s + p99 ~170ms + 250 Connected Users (2vCPU + 4GB RAM)
- **Constraint:** No PII Stored + Recovery via 12-Words Mnemonic Only

## 4. Logic View (Data Models & Flow)

| Component                | Description                                      | Responsibility                                         |
| ------------------------ | ------------------------------------------------ | ------------------------------------------------------ |
| **User Model**           | Custom User Model (`account.models`)             | Handles authentication via username + long passphrase. |
| **Auth Logic**           | Django Session + Argon2id derivation             | Manages secure entry without storing PII.              |
| **Encryptation at Rest** | Field designed for encryptation (`crypt.fields`) | Encrypt and decrypt model's fields in-rest.            |

## 5. Security Architecture (The "Vault" Design)

- **Encryption at Rest:** Argon2id + AES-256-GCM
- **Encryption in Transit:** HTTPS/SSL
- **Secret Management:** Environment Variables
- **Key Derivation:** Argon2id based on 2 system's master keys for secrets

## 6. Deployment & Infrastructure View

- **Hosting:** Docker
- **Database:** PostgreSQL
- **CI/CD:** GitHub Actions
- **Containerization:** Docker/Docker-Compose

## 7. Data View (LGPD Compliance)

- **Data Classification:** Highly Sensitive - Secrets
- **PII Strategy:** Strict No-PII Policy - No emails, names, usernames stored
- **Data Deletion:** Hard-delete on user request

## 8. Observability & Risks

- **Logging:** Wide-Structured JSON Logging per Request
- **Risk-Mitigation:**

| Risk                           | Mitigation                                                                                                                  |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------------------- |
| **Brute Force**                | Rate limiting at the **middleware level** (before hitting the DB) to protect all endpoints from mass database hits.         |
| **SQL Injection**              | Strict use of **Django ORM** + **Psycopg 3** (automatically handles server-side parameter binding and safe data types).     |
| **Password Cracking**          | **Argon2id** (standard in Django 6.0 default hashers) with high memory/time cost to resist GPU/ASIC attacks.                |
| **Automated Bot Abuse**        | Integrated **CAPTCHA challenges** via `django-simple-captcha` for auth forms.                                               |
| **Session Hijacking**          | **HTTP Strict Transport Security (HSTS)** and `Secure/HttpOnly` cookie flags (enforced via Django Security Middleware).     |
| **Slowloris/DoS**              | **Granian (Rust-based HTTP Server)** handles high-concurrency connections more efficiently than pure-Python workers.        |
| **Static File Injection**      | **WhiteNoise** serves static assets with hashed filenames (Cache-Busting) and prevents directory traversal.                 |
| **Seed Phrase Leakage**        | `mnemonic` library used for **BIP39 deterministic seeds**, ensuring entropy is handled via cryptographically secure RNGs.   |
| **Database Connection Leak**   | **Psycopg 3 connection pooling** ensures connections are recycled safely, preventing DoS via "too many connections" errors. |
| **XSS (Cross-Site Scripting)** | Django’s **Auto-escaping template engine** and `X-Content-Type-Options: nosniff` headers.                                   |

## 9. Definition of Done

1. Code passes all test suites (99% coverage)
1. Confirm no hardcoded secrets/keys
1. Confirm no PII is logged
1. Documentation updated (ADR/SAD if architectural changes occurred)
