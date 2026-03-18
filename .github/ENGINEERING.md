# Engineering Workflow & Documentation Flow

To maintain our **"Security by Design"** philosophy and 99% test coverage, every feature, fix, or improvement follows a disciplined documentation-first trajectory. We prioritize architectural intent before a single line of code is written.

## The Documentation Pipeline

When a new issue is triaged, it moves through these three stages:

### 1. The Decision (ADR)

**When:** Significant architectural changes or security trade-offs.

- **Purpose:** Captures the _why_ and the _context_.
- **Action:** Create or update an **Architecture Decision Record**. If we are changing how secrets are salted or choosing a new middleware strategy in Django 6, it starts here.
- **Goal:** Prevent "architecture erosion" and document the rationale for security trade-offs.

### 2. The Alignment (SAD)

**When:** Changes affecting system structure or the **Trust Boundary**.

- **Purpose:** Updates the high-level map of the system.
- **Action:** Update the **Software Architecture Document**. Ensure the data flow diagrams accurately reflect how information moves between encrypted and decrypted states.
- **Goal:** Maintain **Design Consistency** and ensure new features don't inadvertently create side-channels or bypass security protocols.

### 3. The Blueprint (TDD)

**When:** Every non-trivial feature or complex bug fix.

- **Purpose:** Detailed implementation logic and "Rubber Ducking."
- **Action:** Draft the **Technical Design Document**. Define the specific Django models, managers, and logic flows. This is where we identify edge cases (race conditions, malformed inputs, or IDOR risks).
- **Goal:** **Error Prevention.** This document serves as the checklist for our 99% testing alignment.

## The Engineering Loop

We follow a "Documentation-as-Constraint" workflow. Documentation isn't just a record of what was done; it is the set of requirements for what _will_ be done.

1. **ADR (The Decision):** If the issue requires a change in strategy or a security trade-off, we record the "Why" first.
2. **SAD (The Alignment):** Before coding, we update the SAD to ensure the new feature respects the **Trust Boundary** and **No-PII Constraints**. If a new risk is introduced, the mitigation must be added to the Risk Table here first.
3. **TDD (The Blueprint):** We map out the specific Django 6 models, logic, and 99% coverage test plan.
4. **Implementation:** Code is written to satisfy the TDD and SAD.
5. **Validation:** The "Definition of Done" requires a final check to ensure the SAD and TDD perfectly reflect the shipped code.

> **Note:** For minor patches or documentation fixes, a TDD may be truncated, but the SAD must always be consulted to ensure no architectural "blind spots" are introduced.
