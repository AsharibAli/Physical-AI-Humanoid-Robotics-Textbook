---
id: 002
title: Implementation Plan
stage: plan
date: 2025-12-16
surface: agent
model: claude-sonnet-4-5
feature: system-architecture
branch: 001-system-architecture
user: AsharibAli <asharibarain4@gmail.com>
command: /sp.plan
labels: ["implementation-plan", "architecture", "monorepo", "rag-system", "docusaurus", "fastapi"]
links:
  spec: specs/001-system-architecture/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-system-architecture/plan.md
tests:
 - Constitution Check (10/10 gates passed)
---

## Prompt

Derive execution phases strictly from specifications.

PHASE 1: Repository & Tooling
- Initialize monorepo
- Configure pnpm
- Create frontend/ and backend/ directories

PHASE 2: Frontend Setup
- Scaffold Docusaurus in frontend/
- Apply minimalist UI configuration
- Configure sidebar and routing

PHASE 3: Book Content Generation
- Use Book-Content-Details.md as guidance
- Generate full Markdown chapters
- Store under frontend/docs/
- Ensure cohesive narrative across chapters

PHASE 4: Backend RAG System
- Build FastAPI service
- Ingest Markdown content
- Generate embeddings
- Store vectors in Qdrant

PHASE 5: Chat UI Integration
- Embed @openai/chatkit-react in frontend
- Connect to backend API
- Implement selected-text context flow

PHASE 6: Deployment
- Deploy frontend to GitHub Pages
- Validate chatbot functionality end-to-end

## Response snapshot

Created comprehensive implementation plan for Physical AI & Humanoid Robotics Interactive Textbook Platform (957 lines).

**Technical Context Defined**:
- Languages: Node.js 20.x LTS (frontend), Python 3.11+ (backend)
- Dependencies: Docusaurus 3.x, @openai/chatkit-react, FastAPI 0.109+, Qdrant Client 1.7+, OpenAI SDK 1.10+
- Storage: Qdrant Cloud (1GB free tier), Optional Neon Postgres, Git + GitHub Pages
- Performance: FCP <1.5s, TTI <3s, p95 query <2s, 100 concurrent users
- Scale: 40-60 Markdown files, 150k-200k words, ~1,500-2,000 vector chunks

**Constitution Check: 10/10 Gates Passed**:
1. ✅ Content Generation & Book Authorship (frontend/docs/ location enforced)
2. ✅ Spec-Driven Development (spec → plan → tasks workflow)
3. ✅ Modular Coherence (consistent terminology, four-section structure)
4. ✅ Quality Over Quantity (90% first-gen pass rate, no filler)
5. ✅ RAG-First Architecture (strict no-hallucination enforcement)
6. ✅ Tech Stack Adherence (Docusaurus, pnpm, FastAPI, Qdrant, OpenAI)
7. ✅ Progressive Disclosure (week-by-week learning progression)
8. ✅ Test-Driven Documentation (validation + testing strategy)
9. ✅ UI Minimalism (clean typography, low visual noise)
10. ✅ Repository Structure (frontend/backend separation)

**Project Structure**:
- **Frontend**: `frontend/docs/` (book content), `src/components/ChatBot/` (UI), Docusaurus config
- **Backend**: `api/` (FastAPI), `ingestion/` (embedding pipeline), `services/` (RAG logic), `models/` (Pydantic schemas)
- **Deployment**: GitHub Pages (frontend), containerized backend (Railway/Render/Fly.io)

**Phase 0: Research (8 tasks defined)**:
- R1: Docusaurus chat integration pattern (SSR vs client-side)
- R2: Markdown chunking strategy (500-word chunks, overlap, boundaries)
- R3: Qdrant Cloud free tier limits (1GB = how many 1536-dim vectors?)
- R4: FastAPI streaming responses (SSE/WebSocket feasibility)
- R5: Content generation workflow (serial vs batch, quality validation)
- R6: Text selection context handling (browser API, Markdown preservation)
- R7: Embedding cost estimation (~$0.025 one-time for 253k tokens)
- R8: GitHub Pages CORS configuration (OPTIONS preflight handling)

**Phase 1: Design & Contracts (4 deliverables)**:
- P1.1: Data model (7 entities: Chapter, Module, Embedding, Query, Response, ConversationSession, ContentTemplate)
- P1.2: API contracts (backend-api.openapi.yaml with 4 endpoints, embedding-schema.json)
- P1.3: Quickstart guide (prerequisites, setup, integration verification)
- P1.4: Agent context update (add technologies to Claude context file)

**Execution Phases (6 phases)**:
1. Repository & Tooling (monorepo, pnpm, gitignore)
2. Frontend Setup (Docusaurus scaffold, minimalist theme, sidebar)
3. Book Content Generation (40-60 chapters, 4 sections each, 150k-200k words)
4. Backend RAG System (embedding pipeline, Qdrant ingestion, FastAPI endpoints)
5. Chat UI Integration (@openai/chatkit-react, text selection, query modes)
6. Deployment (GitHub Pages + containerized backend)

**ADR Candidates (3 significant decisions)**:
- ADR-001: Monorepo with frontend/backend separation (vs monolithic/microservices)
- ADR-002: RAG-only response strategy (vs hybrid with generative fallback)
- ADR-003: Static site generation (Docusaurus) vs SSR (Next.js/Gatsby)

**Risks & Mitigations**:
- Risk 1: RAG accuracy depends on content quality → Rigorous review before ingestion
- Risk 2: OpenAI API disruptions → Request queuing, caching, graceful degradation
- Risk 3: Vector DB cost scaling → Usage monitoring, query caching, budget alerts
- Risk 4: Content generation depth → Quality rubrics, automated validation, 90% pass rate
- Risk 5: Selected-text context insufficiency → Min/max length enforcement (20-2000 words)

## Outcome

- ✅ Impact: Complete architectural plan ready for Phase 0 research and Phase 1 design. Establishes monorepo structure, RAG pipeline, content generation workflow, and deployment strategy.
- 🧪 Tests: Constitution compliance validation - 10/10 gates passed (all principles satisfied)
- 📁 Files: Created plan.md (957 lines) with technical context, research tasks, design specifications, and execution roadmap
- 🔁 Next prompts: Execute Phase 0 research (create `research.md`), then Phase 1 design artifacts (`data-model.md`, `contracts/`, `quickstart.md`), then `/sp.tasks` for task breakdown
- 🧠 Reflection: Plan successfully translates specification into actionable architecture. Constitution-first validation ensures compliance before implementation. Research phase addresses 8 technical unknowns that could block development. Monorepo structure balances independent deployment with cohesive codebase. ADR candidates identified for user consent.

## Evaluation notes (flywheel)

- Failure modes observed: None - planning completed successfully on first iteration
- Graders run and results (PASS/FAIL): Constitution Check - PASS (10/10 gates), Complexity Tracking - PASS (zero violations)
- Prompt variant (if applicable): Standard /sp.plan workflow with user-provided execution phases
- Next experiment (smallest change to try): Consider adding performance budgets table to plan template for quantitative tracking of SC metrics during implementation
