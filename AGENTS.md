# AGENTS.md

## sWarden - AI Operational & Architectural Guide

This document defines the **technical, architectural, security, and behavioral constraints** that any AI agent must follow when interacting with the sWarden codebase.

sWarden is not a toy Django app. It is a performance-benchmarked, security-oriented credential manager using **Django 6**, **Rust (via Maturin)**, strict linting, custom encrypted fields, and load-tested infrastructure.

Agents must treat this project as production-grade software.

# 1. Critical Context (Non-Negotiable Rules)

## 1.1 Security Is the First Principle

- All sensitive data **must be encrypted at rest**.
- Encryption logic lives in:
  - `SWARDEN/rust/` (high-performance crypto core)
  - `SWARDEN/crypt/` (Django interface layer)

- Custom encrypted fields **must** use one of them:

  ```python
  crypt.fields.EncryptedTextField
  crypt.fields.EncryptedCharField
  ```

- No sensitive field may use raw `TextField` or `CharField`.

## 1.2 Model Hard Requirements

When creating or modifying models:

- ✅ `id` MUST be `UUIDv4`
- ✅ All code MUST include type hints
- ✅ Sensitive fields MUST use encrypted fields
- ✅ Foreign keys MUST explicitly define `db_column='id_<field>'`
- ✅ `__str__()` MUST be implemented
- ✅ `class Meta` MUST exist
- ✅ Default ordering MUST be defined (`-created` if nothing else is relevant)
- ✅ Codebase MUST remain English-only
- ❌ Never use introspective or vague variable names
- ❌ Never waste CPU or memory
- ❌ Never introduce unnecessary abstraction

Follow existing models as the source of truth.

## 1.3 Crypto Architecture

Encryption flow:

```
Django Model
   ↓
crypt.fields (interface)
   ↓
Rust module (argon2id + encryption core)
   ↓
Database (PostgreSQL)
```

- Argon2id is used inside Rust to derive base keys.
- Keys are currently loaded from environment variables.
- No encryption logic lives in PostgreSQL.
- Supabase is only database hosting - no Supabase Auth or storage is used.

Agents must NEVER:

- Suggest moving encryption to the database
- Suggest removing Rust crypto
- Suggest plaintext storage
- Introduce key storage in code

## 1.4 Performance Philosophy

This project is benchmarked with:

- **Locust** (load, spike, soak, stress)
- Docker-based CPU & memory analysis
- memray memory profiling
- Rust vs Python crypto comparisons
- Granian vs Gunicorn benchmarks

Granian was chosen because it showed ~15% better RPS performance.

Agents must:

- Prefer efficient data structures
- Avoid redundant loops
- Avoid excessive queryset evaluation
- Avoid unnecessary object allocations
- Respect Python's Zen

This codebase is 99% test-covered and performance-sensitive.

# 2. Tech Stack & Tooling

## Backend

- Django 6.x
- PostgreSQL
- Rust (via Maturin)
- Argon2id
- Granian (primary runtime server)
- Gunicorn (alternative)
- WhiteNoise (static files)

## Security & Control

- django-simple-captcha (auth views only)
- django-smart-ratelimit (global)
- Custom logging middleware (log wide events only)

## Quality & Tooling

- uv (dependency management)
- Ruff (linting + formatting)
- ty (static typing checker by Astral)
- Coverage (99% target)
- Memray (memory tracking)
- Hypothesis (property testing)
- Locust (load testing)

## Documentation

- MkDocs (Material theme)
- Mosheh (doc generation)
- Docs located under `/documentation`

## Architecture Decision Documents

The main architecture documents are: SAD (.github/SAD.md), TDD (.github/TDD.md) and ADRs (.github/ADRs/...):

- SAD: The Software Architecture Document (SAD) serves as the "source of truth" for the system's structural design. Its primary intention is to provide a high-level map of how the application is built, why certain architectural patterns were chosen, and how various components interact to meet functional and non-functional requirements. For a Secret Manager, the SAD is critical because it documents the "Trust Boundary" - where data is encrypted and where it is vulnerable. The benefits are three-fold: first, it ensures **Design Consistency**, preventing "ad-hoc" features that might bypass security protocols. Second, it facilitates **Knowledge Transfer**, allowing future collaborators (or your future self) to understand the "why" behind the code. Third, it acts as a **Security Audit Baseline**, mapping out data flows to identify potential attack vectors like SQL injection or IDOR before a single line of code is written. It transforms a collection of scripts into a professional, engineered system.

- TDD: The Technical Design Document (TDD) is a low-level blueprint that describes the specific implementation details of a feature or module. Its primary intention is to translate high-level architectural requirements into actionable engineering tasks, focusing on data structures, algorithms, and logic flow. For a solo developer, the TDD acts as a "Rubber Duck" session in written form, forcing you to think through edge cases (like race conditions or malformed inputs) before writing code. The benefits include **Error Prevention**, as it identifies logical flaws in the design phase, and **Testing Alignment**, as it defines exactly what needs to be validated to maintain your 99% coverage goal. In the context of a Secret Manager using Python 3.14 and Django 6, it ensures that "security by design" is baked into every model method and view, preventing vulnerabilities like insecure direct object references (IDOR) or timing attacks.

- ADR: The Architecture Decision Record (ADR) is a short text file that captures a significant architectural decision made during the project’s lifecycle, along with its context and consequences. Its primary intention is to provide **contextual persistence** - answering the "why did we do this?" question months or years after the decision was made. For a solo developer, the ADR prevents "re-deciding" the same issue and ensures that security trade-offs are documented rather than forgotten. The benefits include **change traceability**, allowing you to see how the system evolved, and **reduced cognitive load**, as you don't have to keep every technical justification in your head. It serves as a defense mechanism against "Architecture Erosion", where small, undocumented changes slowly degrade the security or integrity of the original design. In a secret manager context, it is the primary evidence of "Security by Design."

To maintain our **"Security by Design"** philosophy and 99% test coverage, every feature, fix, or improvement follows a disciplined documentation-first trajectory. We prioritize architectural intent before a single line of code is written.

### The Documentation Pipeline

When a new issue is triaged, it moves through these three stages:

#### 1. The Decision (ADR)

**When:** Significant architectural changes or security trade-offs.

- **Purpose:** Captures the _why_ and the _context_.
- **Action:** Create or update an **Architecture Decision Record**. If we are changing how secrets are salted or choosing a new middleware strategy in Django 6, it starts here.
- **Goal:** Prevent "architecture erosion" and document the rationale for security trade-offs.

#### 2. The Alignment (SAD)

**When:** Changes affecting system structure or the **Trust Boundary**.

- **Purpose:** Updates the high-level map of the system.
- **Action:** Update the **Software Architecture Document**. Ensure the data flow diagrams accurately reflect how information moves between encrypted and decrypted states.
- **Goal:** Maintain **Design Consistency** and ensure new features don't inadvertently create side-channels or bypass security protocols.

#### 3. The Blueprint (TDD)

**When:** Every non-trivial feature or complex bug fix.

- **Purpose:** Detailed implementation logic and "Rubber Ducking."
- **Action:** Draft the **Technical Design Document**. Define the specific Django models, managers, and logic flows. This is where we identify edge cases (race conditions, malformed inputs, or IDOR risks).
- **Goal:** **Error Prevention.** This document serves as the checklist for our 99% testing alignment.

### The Engineering Loop

We follow a "Documentation-as-Constraint" workflow. Documentation isn't just a record of what was done; it is the set of requirements for what _will_ be done.

1. **ADR (The Decision):** If the issue requires a change in strategy or a security trade-off, we record the "Why" first.
2. **SAD (The Alignment):** Before coding, we update the SAD to ensure the new feature respects the **Trust Boundary** and **No-PII Constraints**. If a new risk is introduced, the mitigation must be added to the Risk Table here first.
3. **TDD (The Blueprint):** We map out the specific Django 6 models, logic, and 99% coverage test plan.
4. **Implementation:** Code is written to satisfy the TDD and SAD.
5. **Validation:** The "Definition of Done" requires a final check to ensure the SAD and TDD perfectly reflect the shipped code.

> **Note:** For minor patches or documentation fixes, a TDD may be truncated, but the SAD must always be consulted to ensure no architectural "blind spots" are introduced.

**CONSTRAINTS**:

- for ADRs, the template ".github/ADRs/ADR_TEMPLATE.md" MUST be followed when creating new ADRs, with that exact structure
- for ADRs, new files must be created under ".github/ADRs/ADR-{num}: {Chosen Solution}"
- for ADRs, no newline is enforced wrapping words or long phrases, but they are desired to be full size
- for ADRs, the "Comparison", "Security Justification" and any other theme under "Rationale" MUST have the corresponding topics defined as "**Example Topic**: This topic is an example" and not "_Example topic_ is an example" or any other form
- for ADRs, the "Positive (Upsides)" and "Negative (Downsides)" under "Consequences" MUST have the corresponding topics defined as "Example Topic: This topic is an example" and not "_Example topic_ is an example" or any other form
- for ADRs, all implementations MUST be written as the solution is the official, current implementation, applied to the codebase, as if the decision was done today, not refering as a past decision
- for ADRs, the "Constraints" and "Requirements" over "Context" topic MUST be statements containing "MUST" or "MUST NOT" (e.g. "Models MUST contains indexes. Models MUST NOT contains 2 ids") separetad with "."

# 3. Project Structure Overview

```
SWARDEN/
    account/        → Authentication logic
    CORE/           → Settings, middleware, utils, custom test runner
    crypt/          → Django ↔ Rust crypto interface
    err/            → Custom error pages (403, 404, 429, 500)
    home/           → Static institutional pages
    plans/          → Static pricing pages (no business logic)
    secret/         → Secrets domain logic
    rust/           → Rust encryption module
```

## 3.1 CORE

- `testcase.py`
  - Custom test discovery runner
  - Warms up crypto before tests
  - Integrates memray tracking

- `utils.py`
  - Public logging interface
  - Follows "loggingsucks" principle:
    - Log wide events
    - Avoid noisy micro-events

No middleware injects request mutation.

## 3.2 secret App

Handles:

- Passwords
- Secure notes
- Credentials

Includes:

- Custom management commands
- Custom models
- Custom encrypted fields
- Search functionality

`secret/month/`:

- Local replacement for deprecated django-monthfields
- Do not replace without strong justification

## 3.3 Rust Integration

Located in:

```
SWARDEN/rust/
```

Built via:

```
uv run maturin develop --release
```

Compiled wheels located in `/target/`.

Agents must:

- Ignore `/target/`
- Never edit compiled artifacts
- Modify only Rust source under `/rust/src`

# 4. Development Workflow

## 4.1 Environment

Python: **3.14** (defined in `.python-version`)

Dependency manager:

```
uv sync
```

Database:

```
uv run task startdb
```

## 4.2 Running

Local Django:

```
uv run manage.py runserver
```

Granian (preferred):

```
uv run server.py
```

## 4.3 Testing

Standard:

```
uv run manage.py test
```

Coverage:

```
uv run manage.py testwithcoverage
```

Lint:

```
uv run task lint
```

Static typing:

```
uv run ty check
```

Load testing:

```
uv run task loadtest
```

## 4.4 Migrations

AI agents:

- May write model code
- Must NOT generate migration files
- Developer runs `makemigrations`

## 4.5 Static Files

- `static/` → development assets
- `staticfiles/` → collected production files
- SCSS compiles automatically on save
- JS has no special pipeline

# 5. Testing Philosophy

Load scenario:

- 250 distributed users
- Login
- Navigation
- Listing secrets
- Searching secrets

Memory profiling uses:

```
PYTHONMALLOC=malloc
```

Tests are highly strict.

Admin hides sensitive data in production.

# 6. AI Behavioral Guidelines

## 6.1 Verbosity Requirement

High verbosity explanations are REQUIRED.

Every suggestion must:

- Explain reasoning
- Consider performance impact
- Consider security impact
- Consider test impact

## 6.2 Code Style Rules

- English only
- Full type hints
- Clean naming
- No magic numbers
- No hidden complexity
- No premature abstraction
- Respect Ruff configuration

Follow:

```
uv run task lint
```

as reference behavior.

## 6.3 When Creating a New Model

Checklist:

- [ ] UUIDv4 primary key
- [ ] Encrypted fields for sensitive data
- [ ] Explicit db_column on FK
- [ ] `__str__`
- [ ] Meta ordering
- [ ] Type hints
- [ ] English naming
- [ ] Tests for behavior
- [ ] No CPU/memory waste

## 6.4 When Writing Views

Choice guideline:

- Complex logic → Function-Based View
- Simple CRUD → Class-Based View

No strict rule, but complexity drives choice.

## 6.5 Logging Philosophy

- Log high-level events
- Never log sensitive content
- Never log decrypted secrets
- Avoid noisy micro-logging

## 6.6 Documentation Updates

Documentation lives in:

```
/documentation
```

Mosheh auto-updates:

- README
- CONTRIBUTING
- CHANGELOG

AI may modify documentation there.

# 7. What AI Must NEVER Suggest

- Removing encryption
- Using plaintext fields
- Moving crypto logic to Python
- Adding unnecessary database triggers
- Introducing ORM inefficiencies
- Adding caching without benchmark
- Changing server from Granian without benchmark
- Reducing verbosity in explanation
- Ignoring Ruff or ty rules
- Using introspective variable names

# 8. Architectural Summary

sWarden follows a layered model:

```
User
  ↓
Granian
  ↓
Django View (FBV/CBV)
  ↓
Model
  ↓
crypt.fields
  ↓
Rust crypto
  ↓
PostgreSQL (Supabase hosted)
```

No business logic exists in database.

All heavy crypto operations are handled in Rust.

# 9. Project Philosophy

- Python's Zen is law.
- Performance matters.
- Security is non-negotiable.
- Simplicity over cleverness.
- Benchmarks over assumptions.
- Tests before conclusions.
- High verbosity technical explanations.

# 10. Final Directive to AI Agents

If unsure:

1. Follow existing code patterns.
2. Prioritize security.
3. Prioritize performance.
4. Explain every decision.
5. Never assume production shortcuts.
6. Respect the engineering discipline of the project.

This is a benchmarked, tested, performance-sensitive, crypto-based Django system.

Treat it accordingly.
