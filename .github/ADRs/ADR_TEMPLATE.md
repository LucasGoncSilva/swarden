# ADR-NNN: [Short, Descriptive Title]

<!--
Example: "ADR-001: Use of BIP-39 Mnemonic for Account Recovery)"
> Architecture Decision Record (ADR)

> The Architecture Decision Record (ADR) is a short text file that captures a significant architectural decision made during the project’s lifecycle, along with its context and consequences. Its primary intention is to provide **contextual persistence** - answering the "why did we do this?" question months or years after the decision was made. For a solo developer, the ADR prevents "re-deciding" the same issue and ensures that security trade-offs are documented rather than forgotten. The benefits include **change traceability**, allowing you to see how the system evolved, and **reduced cognitive load**, as you don't have to keep every technical justification in your head. It serves as a defense mechanism against "Architecture Erosion", where small, undocumented changes slowly degrade the security or integrity of the original design. In a secret manager context, it is the primary evidence of "Security by Design."
 -->

## Record Header

- **Status:** `[Proposed | Accepted | Rejected | Deprecated | Superseded by ADR-XXX]`
- **Date:** `[YYYY-MM-DD]`
- **Deciders:** `[Your Name / Senior Tech Lead]`
- **Consulted:** `[e.g., LGPD Documentation, Django Security Releases]`

## Context

{ Describe the problem to be solved. }

- **Constraint:** `[e.g., No PII storage allowed under LGPD]`
- **Requirement:** `[e.g., User must be able to recover data without a central server reset]`

## Decision

{ What is the chosen solution? State it clearly and definitively. }

- **Selection:** `[e.g., Implementing a 12-word seed phrase using the BIP-39 standard]`
- **Implementation Detail:** `[e.g., Using the 'mnemonic' Python library to generate seeds on the client-side/server-side]`

## Rationale

{ Why is this the best choice among the alternatives? }

- **Comparison:** `[e.g., Alternative: Email-based 'Forgot Password' requires storing PII and an SMTP server, which increases attack surface.]`
- **Security Justification:** `[e.g., Mnemonic seeds provide zero-knowledge recovery; the server never knows the "backdoor" to the user's vault.]`

## Consequences

- **Positive (Upsides):**
  - Lorem: Ipsum dolor sit amet

- **Negative (Downsides):**
  - Lorem: Ipsum dolor sit amet

- **Technical Debt/Follow-up:**
  - Lorem ipsum dolor sit amet
