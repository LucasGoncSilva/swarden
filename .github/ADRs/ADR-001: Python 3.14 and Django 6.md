# ADR-001: Python 3.14 and Django 6

<!--
Example: "ADR-001: Use of BIP-39 Mnemonic for Account Recovery)"

> Architecture Decision Record (ADR)

> The Architecture Decision Record (ADR) is a short text file that captures a significant architectural decision made during the project’s lifecycle, along with its context and consequences. Its primary intention is to provide **contextual persistence** - answering the "why did we do this?" question months or years after the decision was made. For a solo developer, the ADR prevents "re-deciding" the same issue and ensures that security trade-offs are documented rather than forgotten. The benefits include **change traceability**, allowing you to see how the system evolved, and **reduced cognitive load**, as you don't have to keep every technical justification in your head. It serves as a defense mechanism against "Architecture Erosion", where small, undocumented changes slowly degrade the security or integrity of the original design. In a secret manager context, it is the primary evidence of "Security by Design."
 -->

## Record Header

- **Status:** Accepted
- **Date:** 2026-02-28
- **Deciders:** Lucas Silva (Lead Developer)
- **Consulted:** [Django 6 Release Notes](https://docs.djangoproject.com/en/6.0/releases/6.0/), [Python 3.14 Release Notes](https://docs.python.org/3/whatsnew/3.14.html)

## Context

A Secret Manager requires the highest possible level of "Security by Default." Traditional LTS (Long Term Support) versions often lag behind in implementing modern defensive headers and memory-safety improvements. This system must demonstrate "Real-World" production readiness while utilizing the most modern defensive features available. The stack must be NOT the problem, in a way the stack itself solves the problem and not creates them.

- **Constraint:** Must maintain a zero-PII footprint, maximum test coverage, stack simple enough to not become a problem.
- **Requirement:** Implementation of modern browser-level defenses (CSP) and efficient request handling in a structured logic.

## Decision

Python 3.14 and Django 6 as the core runtime and framework.

- **Selection:** Python 3.14, Django 6
- **Implementation Detail:** Utilize Django 6.0’s Native Content Security Policy (CSP) integration to replace third-party middleware. Leverage Python 3.14's improved Error Tracebacks and Type Hinting for stricter static analysis.

## Rationale

Django 6.0 introduces native, more granular control over CSP (Content Security Policy), reducing the project's dependency on django-csp. This minimizes the supply-chain risk. Furthermore, Python 3.14 continues the trend of "Secure by Default" by removing legacy, insecure modules (e.g., telnetlib, cgi) that are often targets for scanners.

- **Comparison:** Using Django 5.2.x provides stability but lacks the native modern security attributes, requiring more third-party "glue" code which increases the audit surface.
- **Security Justification:** The latest version of Django and Python aims to improve not just the security, fixing known bugs and dependencies, but does this while improving performance.

## Consequences

- **Positive (Upsides):**
  - Native Security: Reduced reliance on third-party middleware for CSP and security headers.
  - Future-Proofing: The project will not require a major version migration for several years.
  - Rust Synergy: Python 3.14’s stable C-API ensures our Rust-based encryption logic (`crypt.algo` and `rust`) performs consistently.

- **Negative (Downsides):**
  - Ecosystem Risk: If a critical security patch is needed for a minor dependency, it may not support Python 3.14 immediately.
  - Image Size: Compiling from `bookworm` for 3.14 results in slightly larger initial build times compared to using pre-built Alpine images for older versions.

- **Technical Debt/Follow-up:**
  - Periodically audit the slim-bookworm base image for CVEs specifically related to the Python 3.14 interpreter.
