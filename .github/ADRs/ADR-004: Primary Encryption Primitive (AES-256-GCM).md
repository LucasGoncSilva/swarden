# ADR-004: Primary Encryption Primitive (AES-256-GCM)

<!--
Example: "ADR-001: Use of BIP-39 Mnemonic for Account Recovery)"
> Architecture Decision Record (ADR)

> The Architecture Decision Record (ADR) is a short text file that captures a significant architectural decision made during the project’s lifecycle, along with its context and consequences. Its primary intention is to provide **contextual persistence** - answering the "why did we do this?" question months or years after the decision was made. For a solo developer, the ADR prevents "re-deciding" the same issue and ensures that security trade-offs are documented rather than forgotten. The benefits include **change traceability**, allowing you to see how the system evolved, and **reduced cognitive load**, as you don't have to keep every technical justification in your head. It serves as a defense mechanism against "Architecture Erosion", where small, undocumented changes slowly degrade the security or integrity of the original design. In a secret manager context, it is the primary evidence of "Security by Design."
 -->

## Record Header

- **Status:** Accepted
- **Date:** 2026-03-03
- **Deciders:** Lucas Silva (Lead Developer)
- **Consulted:** [OWASP Top10 - A04:2025 Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/), [AEAD (cryptography.io)](https://cryptography.io/en/latest/hazmat/primitives/aead/), [RFC 5116 - An Interface and Algorithms for Authenticated Encryption](https://datatracker.ietf.org/doc/html/rfc5116), [NIST SP 800-38D (GCM)](https://csrc.nist.gov/publications/detail/sp/800-38d/final), [Fernet - cryptography.io](https://cryptography.io/en/latest/fernet/)

## Context

sWarden must store sensitive user data encrypted at rest while ensuring tamper detection. The encrypting and decrypting strategy must be solid, valid, not a home-made one. The database trusty depends directly on the chosen approach to this.

- **Constraint:** Tampering with ciphertexts MUST be detectable.
- **Requirement:** Ciphertexts stored in the database MUST be able to handle different payload versions.

## Decision

We standardise on **AES-256-GCM** as the primary symmetric encryption primitive for sWarden.

- **Selection:** AES-256 in Galois/Counter Mode (AES-256-GCM) - AEAD with 128-bit tag.
- **Implementation Detail:** The logic will be all over a dedicated Python class using argon2id for key deriving, while `cryptography.hazmat.primitives.ciphers.aead.AESGCM` generates a fresh 96-bit nonce via `os.urandom(12)`. The contract over the encrypting and decrypting will be done with `dataclasses.dataclass`, defined as `@dataclass(frozen=True, slots=True)`. All the payloads versions inherits from `class PayloadVx` as it implements the `as_dict()` property, simplifying and standardizating the dict representation (`dataclasses.asdict`) for itself and every child class. Those payload classes will be constructed as contract to ensure all the required information over the encrypting is accessable for the decrypting function.

## Rationale

AES-GCM provides authenticated encryption (confidentiality + integrity) in a single, well-audited primitive plus a well structured interface for external apps and well defined contract for internal versions handling. Argon2id provides a strong key derive, as argon2id, the PHC 2015 winner, provides side-channels and GPU cracking. The dataclasses interface helps organizing payloads versioning introducing new policies without breaking old ones.

- **AEAD vs CBC+HMAC:** CBC requires a separate MAC and careful ordering (encrypt-then-MAC recommended). Combining modes increases implementation surface and risk (padding or ordering mistakes). AES-GCM avoids that by design.
- **Fernet tradeoffs:** Fernet wraps AES-CBC+HMAC and forces base64 encoding; it is convenient for Python but incurs larger ciphertexts and extra cryptographic steps. Benchmarks in [bench/default_algo.py](bench/default_algo.py) show AES-GCM is preferable for latency and memory under load.
- **Standards & interoperability:** AES-GCM is standardized (NIST SP 800-38D) and matches AEAD interfaces (RFC 5116). Widely available hardware AES acceleration improves throughput on server CPUs.
- **Implementation notes:** Nonce reuse undermines GCM security. Our implementation generates a fresh 96-bit IV per encryption (`urandom(12)` in [`sWardenCryptography.encrypt`](SWARDEN/crypt.py)); the Rust core mirrors this approach. Key derivation remains Argon2id as defined elsewhere so that derived keys are 32 bytes for AES-256.

## Consequences

- **Positive (Upsides):**
  - Native AEAD guarantees tamper detection; decryption fails on modification.
  - Simpler audit surface compared to separate CBC+HMAC constructions.
  - Better performance (esp. with CPU AES acceleration); benchmarks and load tests reflect the production primitive via [bench/default_algo.py](bench/default_algo.py).

- **Negative (Downsides):**
  - Catastrophic if nonces are reused - strict engineering discipline required.
  - Ties us to AES ecosystem; future migration (e.g., ChaCha20-Poly1305) requires a migration strategy and ADR.

- **Technical Debt/Follow-up:**
  - Add authenticated payload versioning and algorithm identifiers to enable safe algorithm rotation.
  - Add CI checks / property tests to detect accidental nonce reuse and validate AEAD behavior.
  - Periodically re-benchmark against alternatives (e.g., ChaCha20-Poly1305) before any migration.
