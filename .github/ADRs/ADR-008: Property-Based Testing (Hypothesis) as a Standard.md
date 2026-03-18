# ADR-008: Property-Based Testing (Hypothesis) as a Standard

## Record Header

- **Status:** Accepted
- **Date:** 2026-03-03
- **Deciders:** Lucas Silva (Lead Developer)
- **Consulted:** [Hypothesis Documentation](https://hypothesis.readthedocs.io/)

## Context

The existing test suite exercises the most common (“happy path”) code paths across models, views and the cryptographic layer. Given the security-critical nature of the project - AES-GCM, Argon2id, nonce handling, token formats - blind spots in tests translate directly into exploitable bugs.

- **Constraint:** Tests MUST uncover edge-cases and malformed inputs; a defect in the crypto logic MUST NOT slip through because only nominal values were exercised.
- **Requirement:** The project MUST adopt a methodology that systematically generates many inputs, especially for the encryption/decryption routines, and validates invariant properties (e.g. `decrypt(encrypt(x)) == x`).

## Decision

We standardise on **property-based testing using the `hypothesis` library** across all cryptographic and other sensitive modules.

- **Selection:** Add Hypothesis to the test dependencies (already present in `pyproject.toml`) and write strategies for bytes, JSON payloads and UUIDs. Existing unit tests remain; new tests live alongside them under `SWARDEN/crypt/tests/` and `SWARDEN/secret/tests/` (e.g. `test_crypt.py` already contains Hypothesis examples).
- **Implementation Detail:**
  - Use `@given(...)` decorators and custom `strategies` matching production formats (nonces 12-bytes, tags 16-bytes, passwords strings, etc.).
  - Employ `settings(deadline=None, max_examples=1000)` for crypto tests to avoid flaky timeouts.
  - Ensure Hypothesis is configured centrally (`tests/__init__.py`) to respect the project’s `uv` environment and to replay failing examples via `hypothesis.settings` `database`.

## Rationale

Property testing broadens the space explored automatically, reducing human bias about “likely” inputs.

- **Comparison:** Unit-only tests require hand-crafted vectors and often miss malformed or boundary cases. Fuzzing (another alternative) is valuable but infrastructure-heavy and less deterministic. Hypothesis complements the existing suite by generating thousands of examples per run and recording shrinking counter-examples for debugging.
- **Security Justification:** Crypto routines are especially brittle; a single nonce-reuse bug or a payload-parsing error can lead to catastrophic loss of confidentiality or integrity. Hypothesis tests will repeatedly exercise random lengths, empty strings, embedded nulls or corrupted base64, catching regression early.

## Consequences

- **Positive (Upsides):**
  - Increased confidence: tests now explore a far larger input space.
  - Early detection of edge-case bugs (e.g. zero-length ciphertext, bad tag).
  - Documentation-style examples: failing cases are automatically recorded.

- **Negative (Downsides):**
  - Longer test execution time; CI may need tuning (max_examples).
  - Developers must learn Hypothesis idioms and avoid over-complex strategies.
  - Risk of flakiness if not carefully configured; requires maintenance.

- **Technical Debt/Follow-up:**
  - Create shared strategy helpers (`tests/strategies.py`) to avoid duplication.
  - Add a CI job that runs the Hypothesis suite with a larger `max_examples` periodically (nightly).
  - Audit existing tests to convert more of them from fixed vectors to property tests where appropriate.
