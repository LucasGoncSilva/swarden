# ADR-009: Use of Rust for Cryptographic Operations via Maturin and PyO3

## Record Header

- **Status:** Accepted
- **Date:** 2026-03-17
- **Deciders:** Lucas Silva (Lead Developer)
- **Consulted:** [Rust Book](https://doc.rust-lang.org/book/), [Python vs Benchmark by Medium](https://medium.com/@theodoreotzenberger/rust-vs-python-performance-insights-from-a-simple-backend-task-ae05ec36583f), [Discord Migrate from Go to Rust](https://discord.com/blog/why-discord-is-switching-from-go-to-rust)

## Context

The sWarden project requires high-performance cryptographic operations for encryption and decryption of sensitive data. Initial implementations in pure Python resulted in suboptimal performance, with encryption taking approximately 15.9 microseconds and decryption taking 8.8 microseconds. This performance bottleneck impacts the overall responsiveness and scalability of the credential manager, especially under load-tested conditions.

- **Constraint:** Performance MUST be improved without compromising security.
- **Requirement:** Cryptographic operations MUST remain secure and use established primitives like AES-256-GCM and Argon2id.

## Decision

Implement the encrypt and decrypt algorithms in Rust, utilizing Maturin for building Python extensions and PyO3 for seamless Python-Rust bindings. The Rust implementation achieves encryption in 2.6 microseconds and decryption in 0.48 microseconds, representing a 10 to 16x performance improvement over the Python baseline.

- **Selection:** Migrate cryptographic core to Rust with Maturin/PyO3 integration.
- **Implementation Detail:** Use AES-256-GCM for encryption, Argon2id for key derivation, and random policy version selection for encryption.

## Rationale

Rust offers superior performance compared to Python for CPU-intensive tasks like cryptography, while maintaining memory safety and preventing common vulnerabilities. The 10-16x speedup (from 15.9/8.8 μs to 2.6/0.48 μs) directly addresses performance constraints without altering the security model. Alternatives like optimizing Python code or using C extensions were considered but did not yield comparable gains. Maturin and PyO3 provide reliable, maintainable bindings that integrate well with the Django ecosystem.

- **Comparison:** Pure Python implementation lacks performance; C extensions introduce complexity without Rust's safety guarantees.
- **Security Justification:** Rust's memory safety prevents buffer overflows and other exploits; cryptographic primitives remain unchanged.

## Consequences

- **Positive (Upsides):**
  - Performance: Achieves 10-16x faster encryption/decryption operations.
  - Scalability: Supports higher load without performance degradation.
  - Maintainability: Rust code is type-safe and testable.

- **Negative (Downsides):**
  - Complexity: Adds Rust dependency and build process complexity.
  - Learning Curve: Requires Rust expertise for maintenance.
  - Build Time: Maturin builds increase development setup time.

- **Technical Debt/Follow-up:**
  - Documentation: Update SAD and TDD to reflect Rust integration.
  - Testing: Ensure 99% coverage includes Rust components.
  - Monitoring: Add performance benchmarks for ongoing validation.
