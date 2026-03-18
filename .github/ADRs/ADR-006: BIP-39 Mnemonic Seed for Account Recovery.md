# ADR-006: BIP-39 Mnemonic Seed for Account Recovery

## Record Header

- **Status:** Accepted
- **Date:** 2026-03-03
- **Deciders:** Lucas Silva (Lead Developer)
- **Consulted:** [LGPD (Lei Geral de Proteção de Dados)](https://www.gov.br/secretariageral/pt-br/assuntos/lgpd), [BIP-39 Specification](https://github.com/bitcoin/bips/blob/master/bip-0039.mediawiki), [OWASP Top10 - A02:2021 Cryptographic Failures](https://owasp.org/Top10/A02_2021-Cryptographic_Failures/), [Why Mnemonics? (blog post)](https://blog.example.com/bip39-mnemonic-security)

## Context

The traditional “forgot password” email flow requires storing or processing personally identifiable information (PII) - namely the user’s email address - and sending reset links. In sWarden we have committed to an anonymous-first, zero-knowledge design; collecting PII would violate **LGPD** and undermine the no-PII guarantee described throughout the privacy policy.

- **Constraint:** User accounts MUST NOT be tied to any PII. No email, phone,
  or name may be stored for recovery purposes.
- **Requirement:** Users MUST be able to regain access to their vaults without
  server-side involvement, and the recovery mechanism MUST be resilient enough
  for production use even though it places responsibility on the user.

## Decision

We replace the email-based reset flow with a **BIP-39 mnemonic seed phrase** (12-words) as the sole account recovery mechanism.

- **Selection:** Generate a 128-bit entropy phrase using the [BIP-39](https://pypi.org/project/mnemonic/) wordlist; present it to the user once during registration. The phrase is hashed (via `RecoveryPhrase.set_phrase` in `SWARDEN/account/models.py`) before storage, and only its hash and fingerprint are kept.
- **Implementation Detail:** The mnemonic generation logic already exists in `account/models.py` (`settings.MNEMONIC.generate(strength=128)`). Recovery uses `RecoveryPhrase.generate_fingerprint` and a hash-comparison without ever retaining the plaintext words. No email is sent; password resets occur solely by re-entering the 12 words on the recovery page.

## Rationale

The mnemonic seed provides self-sovereignty: the user controls the only thing that can unlock their data.

- **Comparison:** Email reset would violate the no-PII constraint and require running an SMTP infrastructure, increasing attack surface and compliance burden. Third-party tokens or SMS would similarly leak identifiers. Hardware tokens are impractical for general users.

- **Security Justification:** BIP-39 is a well-known standard from the crypto wallet world, reviewed by hundreds of auditors. A 12-word phrase has ~128-bit entropy; when combined with the existing Argon2id-derived passphrase and AES-GCM storage, it resists offline brute-force. Hashing the phrase before persistence ensures that a stolen database dump offers no direct recovery aid (the fingerprint is a deterministic SHA-256 of the normalized phrase).

## Consequences

- **Positive (Upsides):**
  - Compliance: Full compliance with LGPD and other privacy laws since no PII stored or processed.
  - Anonymous-first: Aligns with existing anonymous-first UI and documentation.

- **Negative (Downsides):**
  - Full Users's Responsability: Users bear full responsibility for safekeeping the phrase; lost phrases mean irrevocable data loss and support requests cannot be satisfied.
  - Onboarding friction increases; UI and help text must emphasize the severity (see `account.views.wordlist` and templates).

- **Technical Debt/Follow-up:**
  - Add GUI warnings during registration.
  - Periodically review the BIP-39 wordlist for any cultural or localization concerns; migrate to a 15-words phrase or more if entropy needs rise.
