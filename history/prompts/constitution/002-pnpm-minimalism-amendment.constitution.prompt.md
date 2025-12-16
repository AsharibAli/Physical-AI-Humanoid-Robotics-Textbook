---
id: 002
title: pnpm and UI Minimalism Amendment
stage: constitution
date: 2025-12-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "amendment", "pnpm", "minimalism", "ui-design"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (documentation only)
---

## Prompt

You are Claude Code operating as a senior AI technical author, software architect, and documentation engineer.

Your mission is to design, write, and deploy a unified technical book project using Spec-Kit Plus and Docusaurus, following a strict spec-driven development workflow.

====================================
PRIMARY OBJECTIVE
====================================

Create a complete, modular documentation book that:
1. Is written and structured using Docusaurus.
2. Is generated through Spec-Kit Plus specifications.
3. Is deployed to GitHub Pages.
4. Includes an embedded Retrieval-Augmented Generation (RAG) chatbot capable of answering questions about the book content.

====================================
BOOK CONTENT SOURCE OF TRUTH
====================================

- Use the file "Book-Content-Details.md" as the authoritative reference for:
  - Book scope
  - Chapter structure
  - Topics
  - Learning objectives
- Do NOT invent content beyond this file unless explicitly instructed.
- Every documentation module must map back to this file.

====================================
AUTHORING & QUALITY RULES
====================================

- Treat the book as a single coherent product.
- Prefer clarity, correctness, and minimalism.
- Avoid unnecessary UI decoration.
- Use pnpm exclusively for all package management.
- Do not write implementation before specification.

====================================
FINAL OUTCOME
====================================

A public GitHub Pages site containing:
- A clean, minimal Docusaurus-based technical book
- A fully functional embedded RAG chatbot
- A reference-quality AI-powered documentation system

## Response snapshot

Amended constitution from v1.0.0 to v1.1.0 (MINOR version bump) with the following changes:

**Modified Principles**:
- Principle VI (Tech Stack Adherence): Added pnpm as exclusive package manager with explicit prohibition of npm/yarn

**Added Sections**:
1. Principle IX: UI Minimalism
   - Clean, minimal Docusaurus theme
   - Avoid unnecessary UI embellishments and animations
   - Focus on content readability and navigation efficiency
   - Color palette serves function, not aesthetics
   - Custom CSS requires user-need justification

2. Technical Standards - Package Management subsection:
   - Required tool: pnpm only
   - Documented pnpm commands (install, add, run)
   - Commit pnpm-lock.yaml (not package-lock.json or yarn.lock)

**Workflow Updates**:
- Phase 5 (Validation & Deployment): Changed `npm run start/build` to `pnpm run start/build`

**Rationale for MINOR bump**:
- No breaking changes to existing principles
- New principle (UI Minimalism) adds guidance without invalidating prior work
- pnpm requirement is additive (no existing code yet to break)
- Materially expands technical standards section

## Outcome

- ✅ Impact: Established package management standard (pnpm) and UI design philosophy (minimalism)
- 🧪 Tests: N/A (documentation artifact)
- 📁 Files: Updated .specify/memory/constitution.md (v1.0.0 → v1.1.0)
- 🔁 Next prompts: Resume /sp.specify to create Docusaurus structure spec using pnpm and minimal UI principles
- 🧠 Reflection: Amendment successfully integrates tooling requirements (pnpm) with design philosophy (minimalism) while maintaining constitution structure. The UI Minimalism principle aligns well with Quality Over Quantity principle and strengthens the overall focus on content over presentation.

## Evaluation notes (flywheel)

- Failure modes observed: None detected
- Graders run and results (PASS/FAIL): PASS - Version correctly incremented to 1.1.0, sync impact report updated, all changes documented, no unresolved placeholders
- Prompt variant (if applicable): Standard /sp.constitution amendment workflow
- Next experiment (smallest change to try): Monitor whether UI Minimalism principle requires refinement after first Docusaurus implementation (may need specific Docusaurus theme guidance)
