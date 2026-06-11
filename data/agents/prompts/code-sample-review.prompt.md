---
name: "Engineering: Code Sample Review"
description: "Review educational or documentation code for correctness, clarity, decomposition, and executability."
agent: "CodeReviewer"
argument-hint: "Describe the code artifact, target language, audience, and the review depth required. Include file paths or snippets when possible."
---

Review the requested code sample:

1. **Executable Correctness** — Verify whether the sample can run as written:
   - Missing imports, dependencies, fixtures, or environment assumptions
   - API or syntax drift against current language/library versions
   - Hidden state or setup steps not explained to the reader

2. **Teaching Quality** — Check whether the sample teaches clearly:
   - Each block has a clear purpose and a reader can follow the flow
   - Complex sections are decomposed into manageable chunks
   - Public functions and important types are explained at the right level

3. **Language Standards** — Apply the language-specific quality bar:
   - Python: type hints, pytest patterns, async correctness
   - TypeScript: strict typing, component clarity, accessibility implications when relevant
   - Rust: safe ownership patterns, error handling, and testability

4. **Repository Fit** — Keep the sample aligned to repository guidance:
   - Follow writing and formatting rules already in force
   - Flag when the example crosses into architecture or platform concerns that need specialist review

5. **Deliverable** — Return:
   - Findings first, ordered by severity
   - Exact corrections or rewrite requests
   - Residual risks, missing tests, or missing explanatory prose
