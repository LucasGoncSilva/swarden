# ADR-003: Encryption Strategy (SSE)

<!--
Example: "ADR-001: Use of BIP-39 Mnemonic for Account Recovery)"
> Architecture Decision Record (ADR)

> The Architecture Decision Record (ADR) is a short text file that captures a significant architectural decision made during the project’s lifecycle, along with its context and consequences. Its primary intention is to provide **contextual persistence** - answering the "why did we do this?" question months or years after the decision was made. For a solo developer, the ADR prevents "re-deciding" the same issue and ensures that security trade-offs are documented rather than forgotten. The benefits include **change traceability**, allowing you to see how the system evolved, and **reduced cognitive load**, as you don't have to keep every technical justification in your head. It serves as a defense mechanism against "Architecture Erosion", where small, undocumented changes slowly degrade the security or integrity of the original design. In a secret manager context, it is the primary evidence of "Security by Design."
 -->

## Record Header

- **Status:** Accepted
- **Date:** 2026-03-02
- **Deciders:** Lucas Silva (Lead Developer)
- **Consulted:** [OWASP Top10 - A04:2025 Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/), [Security in Django](https://docs.djangoproject.com/en/6.0/topics/security/)

## Context

The system must protect sensitive user secrets stored in the database against "at-rest" theft (e.g., a database dump leak). However, the application uses Django Templates, where the server is responsible for rendering the UI. If data is encrypted on the client side, the server cannot "see" it to inject it into the HTML templates, effectively breaking the MVT (Model-View-Template) pattern.

- **Constraint:** Back-End server MUST NOT store in no way nor moment the sensitive data, barely being able to see anything. Logs MUST NOT expose any sensitive data. Database MUST NOT store sensitive data in raw string.
- **Requirement:** Database MUST BE able to filter secrets based on their owners. Database MUST be encrypted at-rest for sensitive information with valid, secure algorythm based on private keys. Admin MUST NOT be able to se sensitive data on production, even from development environment.

## Decision

All encryption and decryption operations will be performed on the Back-End (Server-Side) before data hits the persistence layer.

- **Selection:** Use the `cryptography` library (Fernet) to encrypt specific model fields. `dataclasses` will be used to for structured payloads and integrity validation
- **Implementation Detail:** The encryption key will be stored in an environment variable (managed by a Secret Manager in production) and will never be stored in the database itself. `cryptography` module handles the data's integrity, while `dataclasses` handles the versions and definitions for encrypting/decrypting.

## Rationale

The team is extremely more experiencied with Python than JS and this is more than enough when remembering this is a MVP project. Despite this, the primary tension in this decision is between Zero-Knowledge Privacy (Client-Side) and Functional Velocity (Server-Side). For a product in the MVP stage using a monolithic framework, SSE is the superior choice for the following reasons:

- Architectural Alignment: Our current stack relies on Django Templates. In a Client-Side Encryption (CSE) model, the server only handles "opaque blobs" of data. Since the server cannot decrypt these blobs without the user's local key, it cannot inject that data into HTML templates, render forms, or perform server-side validation. Opting for SSE allows us to maintain the Model-View-Template (MVT) pattern without moving to a decoupled Single Page Application (SPA) architecture, which would double our frontend development time.

- Comparison to Alternatives: - Client-Side Encryption (CSE): While more secure against a total server compromise, it introduces massive "Key Management" overhead. If a user loses their local device or clears their browser cache without a backup, their data is mathematically unrecoverable. For an MVP, the UX friction of "recovery phrases" often outweighs the privacy benefits for general users.

- **Comparison:** Client-Side Encryption (CSE) was considered but rejected for the MVP. CSE would require a decoupled frontend (like React or Vue) to handle decryption in the browser. Moving to CSE would require a complete rewrite of the existing Django Template architecture.
- **Security Justification:** SSE successfully mitigates the primary risk: a leaked database. By using TLS for data-in-transit and Fernet for data-at-rest, we provide a robust security baseline that fits the current technical stack. Although the Back-End Server can theoretically "see" raw data, since nothing is logged out, nothing is really saved: no sensitive data is logged to log files, no sensitive data is shonw on error pages (traceback), no sensitive data is sent outside the applications environment (email, SMS, ...), no sensitive data is shared with admins.

## Consequences

- **Positive (Upsides):**
  - Compatibility: Full support for Django's built-in Forms, Templates, Admin panels and tests.

  - Simplicity: No need to manage complex browser-based cryptographic keys or WebCrypto APIs for the MVP launch.

  - Developer Experience: Fast implementation using standard Python libraries.

- **Negative (Downsides):**
  - Trust Dependency: The application server becomes a "trusted" entity; if the server itself is fully compromised, the keys in memory can be stolen.

  - Not Zero-Knowledge: We cannot claim "Zero-Knowledge" status to users, as the backend technically has access to the plaintext during the request lifecycle.

- **Technical Debt/Follow-up:**
  - Plan a dedicated Key Management Service (KMS) like AWS KMS or HashiCorp Vault for production use.

  - Research "blind indexing" if we eventually need to search through encrypted fields without decrypting them first.
