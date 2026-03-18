# ADR-007: Django Session vs JWT

## Record Header

- **Status:** Accepted
- **Date:** 2026-03-03
- **Deciders:** Lucas Silva (Lead Developer)
- **Consulted:** [OWASP Top10 - A03:2021 - Data Integrity Failures](https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/), [Django Sessions](https://docs.djangoproject.com/en/6.0/topics/http/sessions/), [JWT Critiques - Auth0 Blog](https://auth0.com/blog/why-jwt-may-not-be-the-best-choice/), [JWT and Revocation](https://www.baeldung.com/java-jwt-revocation)

## Context

sWarden must authenticate users and maintain access to their encrypted vaults. Authentication tokens carry significant power: compromise or misuse equalsfull data exposure.

- **Constraint:** Session tokens MUST be revocable immediately (instant logout, administration disable). Revocation MUST NOT depend on token expiration alone.
- **Requirement:** Backend MUST support at least 150 concurrent authenticated users with acceptable latency; horizontal scaling is anticipated but not at the expense of security. The solution SHOULD integrate cleanly with Django’s built-in auth and not leak sensitive information (e.g. vault keys) client-side.

## Decision

We retain **standard Django server-side sessions stored in PostgreSQL** as the sole session mechanism. JSON Web Tokens (JWT) will **not be used** for authentication or session management.

- **Selection:** Django's default sessions engine with regular cleanup via `clearsessions` command (already part of the codebase).
- **Implementation Detail:** All views and decorators continue to rely on `request.session` provided by Django. Server's workers share the same database; no additional caching layer is introduced. The `SessionMiddleware` remains in `MIDDLEWARE` and sessions are bound to user `id` via the usual Django mechanism.

## Rationale

The trade-off is between a small amount of server-side state versus the complexity and security pitfalls of self-contained tokens. Kinda over-engineering nowadays.

- **Comparison:** JWT are stateless; they carry claims and expiry and are signed. For a secret manager, the inability to revoke a token without maintaining a server-side blacklist is unacceptable. An attacker who steals a valid JWT has access until it expires; implementing revocation requires additional state anyway, negating the “stateless” benefit. Django sessions store only a random key in the cookie; all sensitive data stays on the server. Revoking access is as simple as deleting a row from `django_session`. The database is already part of our stack and scaling to 250 users has been proven in load tests (see `loadtests/`).

- **Security Justification:** JWTs encourage developers to put too much into the token (user roles, vault identifiers) and sign with long-lived keys. Any key compromise allows mass impersonation. With DB sessions the secret key never leaves the server, and the only value in the cookie is a lookup key. Session expiration is short (configurable via `SESSION_COOKIE_AGE`) and can be extended on activity. Instant revocation supports scenarios like detected breaches or administrator disables, which are non-negotiable in a vault product.

- **Performance Note:** The overhead of a simple `SELECT`/`DELETE` per request is negligible at our scale; database connection pooling and Granian’s async model cover this. If we eventually exceed tens of thousands of sessions, we can move to a cache backend (Redis) without changing the API, still preserving revocation semantics.

## Consequences

- **Positive (Upsides):**
  - Session "ACID": True instant logout/revocation by deleting session records.
  - Simplicity: No need to rotate or securely distribute JWT signing keys; leverages existing Django auth middleware.
  - Smaller Attack Surface: Reduces risk of inadvertently exposing claims or keys via client storage.

- **Negative (Downsides):**
  - Server-Side Storage: Requires server-side storage and periodic cleanup (`clearsessions` cron).
  - Scaling: Horizontal scaling demands shared session storage (currently satisfied by Postgres).
  - Processing: Slightly more I/O per request compared to fully stateless tokens.

- **Technical Debt/Follow-up:**
  - Monitor session table size and add Redis/Memcached backend if load grows beyond Postgres comfort zone.
  - Document a potential path to token-based auth only if we ever adopt a micro-services architecture that justifies it.
  - Add automated tests verifying that deleted sessions no longer authenticate (already implicit in many existing view tests).
