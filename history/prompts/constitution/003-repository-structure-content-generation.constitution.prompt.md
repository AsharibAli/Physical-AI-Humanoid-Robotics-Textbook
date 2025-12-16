---
id: 003
title: Repository Structure and Content Generation
stage: constitution
date: 2025-12-16
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "major-amendment", "breaking-change", "repository-structure", "content-generation"]
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

Create a complete technical book titled:

"Physical AI & Humanoid Robotics"

The system must:
1. Generate the full book content as Markdown files.
2. Render the book using Docusaurus.
3. Deploy the documentation to GitHub Pages.
4. Embed a Retrieval-Augmented Generation (RAG) chatbot that can converse with users about the book content.

====================================
REPOSITORY STRUCTURE (MANDATORY)
====================================

- frontend/
  - Docusaurus documentation site
  - All Markdown book content
  - Minimalist UI

- backend/
  - RAG chatbot backend
  - Vector ingestion pipeline
  - Conversation API

====================================
BOOK CONTENT SOURCE OF TRUTH
====================================

- The file "Book-Content-Details.md" is a reference guide ONLY.
- You must generate the complete book content yourself.
- All chapters must be written as Markdown files under frontend/docs/.
- Do NOT copy the reference file verbatim.
- Expand, structure, and formalize content professionally.

====================================
QUALITY BAR
====================================

- No filler content.
- No vague explanations.
- Technical accuracy is mandatory.
- Content must read like a real published technical book.

====================================
FINAL OUTCOME
====================================

A public GitHub Pages site hosting:
- The book "Physical AI & Humanoid Robotics"
- A working embedded conversational RAG chatbot
- Clean architecture separating frontend and backend

## Response snapshot

**MAJOR VERSION AMENDMENT**: Constitution v1.1.0 → v2.0.0

**BREAKING CHANGES**:

1. **Principle I Redefined**: "Content Authenticity" → "Content Generation & Book Authorship"
   - **Old behavior**: Book-Content-Details.md was strict source of truth (cannot deviate)
   - **New behavior**: Book-Content-Details.md is reference guide (agent generates full content)
   - **Impact**: Agent now responsible for authoring complete technical book content
   - **Location requirement**: All content MUST be in `frontend/docs/`

2. **Repository Structure Made Mandatory**:
   - Added Technical Standards section: Repository Structure (MANDATORY)
   - Required directory layout:
     ```
     frontend/   # Docusaurus + book Markdown
     backend/    # RAG API + vector pipeline
     ```
   - **Impact**: All future specs must comply with frontend/backend separation
   - Clean architectural boundaries for independent deployment

3. **Authority Hierarchy Reordered**:
   - **Old hierarchy**: Book-Content-Details.md (#1) > Constitution (#2)
   - **New hierarchy**: Constitution (#1) > Book-Content-Details.md (#2 as reference)
   - **Rationale**: Constitution must supersede reference guide to enable content generation

**Modified Sections**:
- Documentation Structure: Updated to specify `frontend/` subdirectory context

**Version Bump Justification**:
- Principle I redefinition is backward-incompatible (changes core authorship model)
- Repository structure requirement breaks any flat-structure assumptions
- Authority hierarchy change affects governance decision-making
- All three changes qualify as MAJOR per semantic versioning

**Follow-up Actions Required**:
- All existing specs must be reviewed for new repository structure compliance
- Content generation strategy must be explicitly defined in next feature spec
- Frontend/backend separation must be reflected in all planning artifacts

## Outcome

- ✅ Impact: Redefined project from "documentation mapper" to "book author and system builder"
- 🧪 Tests: N/A (documentation artifact)
- 📁 Files: Updated .specify/memory/constitution.md (v1.1.0 → v2.0.0)
- 🔁 Next prompts: Create feature spec for frontend/backend structure initialization and book content generation workflow
- 🧠 Reflection: This MAJOR amendment fundamentally shifts the project scope from constraint-following to creative content generation. The agent is now empowered to author a complete technical book using the reference guide as a blueprint rather than a strict boundary. The frontend/backend split provides clean architecture for the RAG system integration.

## Evaluation notes (flywheel)

- Failure modes observed: None detected
- Graders run and results (PASS/FAIL): PASS - Version correctly incremented to 2.0.0 (MAJOR), breaking changes documented in sync impact report, authority hierarchy updated, repository structure made explicit
- Prompt variant (if applicable): Standard /sp.constitution major amendment workflow
- Next experiment (smallest change to try): Monitor whether content generation guidelines in Principle I need further refinement after first book chapter authoring (may need writing style guide or quality checklist)
