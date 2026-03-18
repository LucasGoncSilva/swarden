# ADR-002: Monolith-First with Modular Boundaries

<!--
Example: "ADR-001: Use of BIP-39 Mnemonic for Account Recovery)"
> Architecture Decision Record (ADR)

> The Architecture Decision Record (ADR) is a short text file that captures a significant architectural decision made during the project’s lifecycle, along with its context and consequences. Its primary intention is to provide **contextual persistence** - answering the "why did we do this?" question months or years after the decision was made. For a solo developer, the ADR prevents "re-deciding" the same issue and ensures that security trade-offs are documented rather than forgotten. The benefits include **change traceability**, allowing you to see how the system evolved, and **reduced cognitive load**, as you don't have to keep every technical justification in your head. It serves as a defense mechanism against "Architecture Erosion", where small, undocumented changes slowly degrade the security or integrity of the original design. In a secret manager context, it is the primary evidence of "Security by Design."
 -->

## Record Header

- **Status:** Accepted
- **Date:** 2026-03-02
- **Deciders:** Lucas Silva (Lead Developer)
- **Consulted:** [Django's Documentation](https://docs.djangoproject.com/en/6.0/), [Makimo's Blog - Modular Monolith in Django](https://makimo.com/blog/modular-monolith-in-django/)

## Context

The Secret Manager is currently in early-stage development with an initial target of ~10-250 users. While the long-term vision may require a distributed microservices architecture for scaling the "Vault" independently from the "Web UI", implementing microservices now would be extremely-high-ultra-premature over-engineering. However, standard Django projects often suffer from "Tight Coupling", where apps import directly from each other’s models, making future extraction impossible. We need a middle ground that allows the team to learn and build quickly without creating a legacy mess.

- **Constraint:** The provenient codebase MUST be readable, but also "workable" even if the interactions get complex.
- **Requirement:** High development velocity without sacrificing future scalability, no over-engineering, no go-horse.

## Decision

Implement Django's default architecture, programmed and deployed as a single unit (Monolith) for now.

- **Selection:** Django's default way to do, relying on native's ORM and Model's FKs, for instance.
- **Implementation Detail:** Also Django's default way to do, but always with well described and clear code.

## Rationale

Although a Modular Monolith Architecture seems to be the best solution on this case, the team is not experiencied enough to apply a high security-level project in a way never done before, even with a simple, small project. Aiming to be as a reference project, while not in a modular arch, the codebase must be implemented in a very organized way, for future migration.

- **Comparison:** Microservices are a high operational overhead, too complex for a 10-user starting point.
- **Learning Curve:** A full microservices split requires service discovery, distributed tracing, and complex CI/CD. A Modular Monolith allows the team to master Domain-Driven Design (DDD) within the familiar Django environment. A full Django-like traditional project, if well designed and organized, can be very easy to migrate to a Modular style.

## Consequences

- **Positive (Upsides):**
  - Codebase Verbosity: Less worry about contracts to be followed, leading a simpler, less verbose codebase
  - Simpler Structure: Easier to handle imports, functions calls and use the ORMs benefits, such as `select_related` and `prefetch_related`
- **Negative (Downsides):**
  - Go-Horse Trend: With no contract to be followed, the influence of a go-horse development always exists, so developers must be caution to not fall for this temptation of fast-unruled-writing code.
- **Technical Debt/Follow-up:**
  - Implement well defined contracts, DTOs, interfaces and logic's services in the future, while keeping the codebase easy to understand for now.
