# ADR-005: Key Derivation Function (Argon2id)

<!--
Architecture Decision Record (ADR)

The Architecture Decision Record (ADR) is a short text file that captures a significant architectural decision made during the project's lifecycle, along with its context and consequences. Its primary intention is to provide **contextual persistence** - answering the "why did we do this?" question months or years after the decision was made. For a solo developer, the ADR prevents "re-deciding" the same issue and ensures that security trade-offs are documented rather than forgotten. The benefits include **change traceability**, allowing you to see how the system evolved, and **reduced cognitive load**, as you don't have to keep every technical justification in your head. It serves as a defense mechanism against "Architecture Erosion", where small, undocumented changes slowly degrade the security or integrity of the original design. In a secret manager context, it is the primary evidence of "Security by Design."
 -->

## Record Header

- **Status:** Accepted
- **Date:** 2026-03-03
- **Deciders:** Lucas Silva (Lead Developer)
- **Consulted:** [OWASP Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html), [Argon2 RFC 9106](https://datatracker.ietf.org/doc/html/rfc9106), [Argon2 Official Documentation](https://argon2-cffi.readthedocs.io/en/stable/), [NIST SP 800-132 (PBKDF2)](https://csrc.nist.gov/publications/detail/sp/800-132/final), [GPU Brute-Force Attack Vectors (2024)](https://www.usenix.org/conference/usenixsecurity24)

## Context

sWarden derives encryption keys from a system-defined keys (master key - which is not the same of `django.conf.settings.SECRET_KEY`) plus a random salt (individual per secret) to encrypt all sensitive secrets at rest. The key derivation function (KDF) is the **critical bridge** between the system's key and the cryptographic strength of the vault. A weak or fast KDF allows attackers with GPU access to perform billion-operation brute-force attacks in seconds (here, being slow for deriving the key is good, slowing down attackers, while the rest of operation being fast is desired).

The implementation currently uses Argon2id (found in [`SWARDEN/crypt.py`](SWARDEN/crypt.py) and configured in [`SWARDEN/CORE/settings/base.py`](SWARDEN/CORE/settings/base.py) with time cost, memory cost, and parallelism parameters). This decision documents why Argon2id was chosen over alternatives like PBKDF2, bcrypt, or scrypt.

- **Constraint:** The KDF MUST be memory-hard and time-hard. The KDF MUST NOT permit trivial GPU acceleration that renders human-memorable passphrases defensible against attackers with modern ASIC/GPU clusters.
- **Requirement:** The KDF MUST derive 32-byte keys suitable for AES-256-GCM. The implementation MUST accept configurable arguments for (de)encrypting parameters to allow security "tuning" as hardware evolves.

## Decision

We standardise on **Argon2id** as the sole key derivation function for converting system's key into encryption key in sWarden.

- **Selection:** Argon2id with parameterized time cost (default: 3 - `time_cost=3`), memory cost (default: 65536 KiB - `memory_cost=65536`), and parallelism (default: 1 thread - `p=1`). The function generates a 32-byte output suitable for AES-256-GCM encryption.
- **Implementation Detail:** The [`sWardenCryptography._derive_key()`](SWARDEN/crypt.py) classmethod in `SWARDEN/crypt.py` uses `argon2.low_level.hash_secret_raw()` with `Type.ID` variant. Parameters are configurable via environment variable `DEFAULT_TC_MC_P` (comma-separated values: `tc,mc,p`) or hardcoded defaults. The same KDF is used in Django's password hashing layer via [`Argon2PasswordHasher`](SWARDEN/CORE/settings/base.py) for user authentication, ensuring consistency across the security model.

## Rationale

Argon2id is a **memory-hard, time-hard** KDF resistant to GPU and ASIC acceleration - a critical requirement in a secret manager where an attacker may obtain encrypted vaults.

- **Comparison to PBKDF2:** PBKDF2 (the older standard) applies a hash function iteratively but uses minimal memory. An attacker with a GPU cluster can compute billions of PBKDF2 iterations per second per GPU. Argon2id with 64 MiB as default memory cost value forces an attacker to provision memory for each parallel attempt, increasing total cost by orders of magnitude. OWASP Password Storage Cheat Sheet (2024) explicitly recommends Argon2 over PBKDF2 for new systems.

- **Comparison to bcrypt:** Bcrypt is memory-efficient but not memory-hard by design. It was built for Unix password hashing in the 1990s and lacks the tuning flexibility modern threats demand. Argon2id's memory cost parameter allows us to require attackers to allocate gigabytes of RAM per attempt, making distributed GPU attacks economically infeasible.

- **Comparison to scrypt:** Scrypt is memory-hard but has a smaller security margin than Argon2 against advanced attacks (e.g., Hellman time-memory trade-offs). Argon2 (winner of the Password Hashing Competition, 2015) was designed to address scrypt's theoretical weaknesses. RFC 9106 standardizes Argon2 as the recommended modern choice.

- **Security Justification:** If database (encrypted with AES-256-GCM, ciphertext + AEAD tag) is leaked, an offline brute-force attack is a practical threat. A 12-character passphrase has ~88 bits of entropy; without a memory-hard KDF, GPU clusters can exhaust modern passphrase spaces in days. Argon2id with 64 MiB memory cost forces each guess to allocate 64 MiB, reducing a GPU's parallel capacity from thousands of simultaneous attempts to single digits. This shifts the attacker's cost-benefit calculus from "rent a GPU cluster for $1000" to "rent an ASIC memory cluster for $10 million", making the attack impractical for individual users.

## Consequences

- **Positive (Upsides):**
  - GPU-Resistant: Attackers cannot trivially parallelize Argon2id on GPUs or ASICs due to memory-hard properties; even with hardware acceleration, cost-per-guess remains high.
  - Tunable Security: Parameters (tc, mc, p) can be increased as hardware evolves (e.g., in 2030, increase `mc` from 65536 to 262144 KiB), extending security margins without breaking existing vaults.
  - RFC-Standardized: Argon2 is standardized in RFC 9106 and recommended by OWASP, ensuring peer review and future compatibility.
  - Consistency: The same KDF is used for both user authentication (Django password hasher) and vault encryption ([`sWardenCryptography`](SWARDEN/crypt.py)), eliminating a class of KDF mismatch bugs.

- **Negative (Downsides):**
  - CPU & Memory Cost: Argon2id is intentionally slow (~1-2 seconds per derivation on a modern CPU). This is by design but impacts user experience during login and secret decryption.
  - Parallelism Trade-off: The default parallelism is 1 (single-threaded). Increasing `p` improves performance but requires more cores; web servers with many concurrent users may experience CPU contention.
  - Parameter Tuning Risk: Misconfigured parameters (e.g., `mc=1024` instead of 65536) drastically weaken security. Documentation and defaults must be strict, and upgrades require migration logic.

- **Technical Debt/Follow-up:**
  - Implement a KDF **versioning scheme** to allow future migration from Argon2id to a successor (e.g., Argon3, PhC2, or post-quantum KDFs). Payloads should include a KDF version identifier so old vaults can be re-keyed transparently.
  - Add monitoring to detect if users are exploiting weak passphrases (entropy < 50 bits) and encourage stronger choices during account creation.
  - Periodically audit parameter tuning (tc, mc, p) against emerging GPU/ASIC performance benchmarks. Publish a security advisory if recommendations change.
  - Consider offering a "high-security" mode (e.g., `tc=4, mc=262144, p=2`) for users who prioritize security over login speed.
