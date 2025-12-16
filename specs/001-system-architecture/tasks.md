---
description: "Task breakdown for Physical AI & Humanoid Robotics Interactive Textbook Platform"
---

# Tasks: Physical AI & Humanoid Robotics Interactive Textbook Platform

**Input**: Design documents from `/specs/001-system-architecture/`
**Prerequisites**: plan.md (✅ complete), spec.md (✅ complete)

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are omitted. Focus is on implementation and validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Web app structure**: `backend/` and `frontend/` at repository root
- Backend: Python with FastAPI (`backend/api/`, `backend/ingestion/`, `backend/services/`)
- Frontend: TypeScript with Docusaurus (`frontend/src/`, `frontend/docs/`)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and monorepo structure

- [ ] T001 Create frontend/ and backend/ directories at repository root
- [ ] T002 [P] Initialize .gitignore with Node.js and Python patterns
- [ ] T003 [P] Create README.md with project overview and quickstart links
- [ ] T004 [P] Initialize pnpm workspace configuration in pnpm-workspace.yaml (optional)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [ ] T005 Initialize backend with `uv init backend` and update pyproject.toml metadata
- [ ] T006 [P] Add core dependencies with `uv add fastapi uvicorn[standard] pydantic pydantic-settings openai qdrant-client`
- [ ] T007 [P] Add utility dependencies with `uv add httpx aiofiles markdown python-frontmatter python-dotenv slowapi python-multipart`
- [ ] T007a [P] Add dev dependencies with `uv add --dev pytest pytest-asyncio pytest-cov black flake8 mypy isort`
- [ ] T008 [P] Create backend/.env.example with required environment variables (OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY)
- [ ] T009 [P] Create backend/config/settings.py for environment-based configuration loading
- [ ] T010 [P] Create backend/config/qdrant_config.py with Qdrant connection settings
- [ ] T011 [P] Create backend/api/main.py with FastAPI app initialization
- [ ] T012 [P] Implement CORS middleware in backend/api/middleware/cors.py allowing frontend origins
- [ ] T013 [P] Implement rate limiting middleware in backend/api/middleware/rate_limit.py
- [ ] T014 Create backend/models/__init__.py package marker

### Frontend Foundation

- [ ] T015 Run `pnpm create docusaurus@latest frontend classic --typescript` to scaffold Docusaurus site
- [ ] T016 Configure docusaurus.config.js with site title "Physical AI & Humanoid Robotics", GitHub Pages deployment settings
- [ ] T017 Create frontend/src/css/custom.css with minimalist theme (clean typography, minimal visual noise)
- [ ] T018 Create frontend/sidebars.js structure for 12 modules (module-01-ros2 through module-12)
- [ ] T019 [P] Create frontend/.env.example with BACKEND_API_URL variable
- [ ] T020 [P] Create frontend/static/img/ directory for diagrams and assets

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 4 - Generate Complete Book Content (Priority: P1) 🎯 MVP PREREQUISITE

**Goal**: Generate 40-60 Markdown chapters with professional technical content following four-section structure (Concepts, Architectures, Algorithms, Real-World Considerations)

**Independent Test**: Generated content validates with structure checks, renders correctly in Docusaurus, and passes 90% quality review

**Why US4 First**: Content generation must complete before US1 (reading content) and US2 (searching content) can be implemented. This is a prerequisite for displaying and indexing.

### Content Generation Infrastructure

- [ ] T021 [US4] Create backend/models/content_template.py with Pydantic model defining four required sections
- [ ] T022 [US4] Create backend/services/content_generator.py with OpenAI API integration for chapter generation
- [ ] T023 [US4] Implement content validation in backend/services/content_validator.py (check for four sections, structure, quality)
- [ ] T024 [US4] Create backend/scripts/generate_content.py CLI script accepting topic and module parameters

### Module 1: ROS 2 Content Generation

- [ ] T025 [P] [US4] Generate frontend/docs/module-01-ros2/index.md (module overview)
- [ ] T026 [P] [US4] Generate frontend/docs/module-01-ros2/chapter-01-fundamentals.md
- [ ] T027 [P] [US4] Generate frontend/docs/module-01-ros2/chapter-02-nodes-topics.md
- [ ] T028 [P] [US4] Generate frontend/docs/module-01-ros2/chapter-03-urdf.md

### Module 2: Simulation Content Generation

- [ ] T029 [P] [US4] Generate frontend/docs/module-02-simulation/index.md
- [ ] T030 [P] [US4] Generate frontend/docs/module-02-simulation/chapter-01-gazebo-setup.md
- [ ] T031 [P] [US4] Generate frontend/docs/module-02-simulation/chapter-02-physics-simulation.md
- [ ] T032 [P] [US4] Generate frontend/docs/module-02-simulation/chapter-03-unity-integration.md

### Module 3: NVIDIA Isaac Content Generation

- [ ] T033 [P] [US4] Generate frontend/docs/module-03-isaac/index.md
- [ ] T034 [P] [US4] Generate frontend/docs/module-03-isaac/chapter-01-isaac-sim.md
- [ ] T035 [P] [US4] Generate frontend/docs/module-03-isaac/chapter-02-isaac-ros.md
- [ ] T036 [P] [US4] Generate frontend/docs/module-03-isaac/chapter-03-nav2-planning.md

### Module 4: Vision-Language-Action Content Generation

- [ ] T037 [P] [US4] Generate frontend/docs/module-04-vla/index.md
- [ ] T038 [P] [US4] Generate frontend/docs/module-04-vla/chapter-01-voice-to-action.md
- [ ] T039 [P] [US4] Generate frontend/docs/module-04-vla/chapter-02-cognitive-planning.md
- [ ] T040 [P] [US4] Generate frontend/docs/module-04-vla/chapter-03-capstone-project.md

### Modules 5-12: Additional Content Generation

- [ ] T041 [P] [US4] Generate frontend/docs/module-05-sensors/ (index + 3-4 chapters)
- [ ] T042 [P] [US4] Generate frontend/docs/module-06-locomotion/ (index + 3-4 chapters)
- [ ] T043 [P] [US4] Generate frontend/docs/module-07-manipulation/ (index + 3-4 chapters)
- [ ] T044 [P] [US4] Generate frontend/docs/module-08-perception/ (index + 3-4 chapters)
- [ ] T045 [P] [US4] Generate frontend/docs/module-09-control-systems/ (index + 3-4 chapters)
- [ ] T046 [P] [US4] Generate frontend/docs/module-10-hri/ (index + 3-4 chapters on human-robot interaction)
- [ ] T047 [P] [US4] Generate frontend/docs/module-11-deployment/ (index + 3-4 chapters)
- [ ] T048 [P] [US4] Generate frontend/docs/module-12-advanced-topics/ (index + 3-4 chapters)

### Content Validation & Integration

- [ ] T049 [US4] Run structure validation on all generated chapters (verify four sections present)
- [ ] T050 [US4] Run consistency check across all chapters (terminology, cross-references)
- [ ] T051 [US4] Create frontend/docs/intro.md landing page summarizing all 12 modules
- [ ] T052 [US4] Update frontend/sidebars.js with all generated chapters in hierarchical structure

**Checkpoint**: All book content generated (40-60 chapters, 150k-200k words). Content is ready for display (US1) and embedding (US2).

---

## Phase 4: User Story 1 - Read Technical Book Content (Priority: P1) 🎯 MVP

**Goal**: Technical developers can access well-organized textbook content through clean, minimalist documentation interface with sidebar navigation

**Independent Test**: Deploy static Docusaurus site locally, navigate through all 12 modules, verify clean typography and sidebar navigation, confirm all chapters render correctly

### Frontend Display Implementation

- [ ] T053 [US1] Configure Docusaurus theme in frontend/docusaurus.config.js for minimalist design
- [ ] T054 [US1] Customize frontend/src/css/custom.css for clean typography (line height, font size, heading hierarchy)
- [ ] T055 [US1] Update frontend/src/theme/Layout/index.tsx to remove unnecessary UI elements
- [ ] T056 [US1] Configure search plugin in frontend/docusaurus.config.js for keyword chapter search
- [ ] T057 [US1] Add metadata (title, description, keywords) to all chapter Markdown frontmatter
- [ ] T058 [US1] Test responsive design on desktop and tablet viewports

### Local Development Validation

- [ ] T059 [US1] Run `pnpm run start` and verify site loads on localhost:3000
- [ ] T060 [US1] Navigate through all modules and chapters via sidebar
- [ ] T061 [US1] Verify chapter content displays with clear section headings (Concepts, Architectures, Algorithms, Real-World)
- [ ] T062 [US1] Run `pnpm run build` and verify production build succeeds

**Checkpoint**: User Story 1 complete. Static documentation site is fully functional and independently testable. Users can read all content without chatbot.

---

## Phase 5: User Story 2 - Search Book Content with AI Assistant (Priority: P2)

**Goal**: Technical developers can ask natural language questions about any topic and receive accurate answers with source citations from the RAG system

**Independent Test**: Ingest all chapters into Qdrant, deploy backend API, submit test queries via API, verify responses cite specific chapters with no hallucinations

### Backend Data Models

- [ ] T063 [P] [US2] Create backend/models/query.py with Pydantic models for QueryRequest (query_text, query_mode, session_id, selected_text, max_results)
- [ ] T064 [P] [US2] Create backend/models/query.py with Pydantic models for QueryResponse (response_text, source_citations, confidence_score, session_id, retrieved_chunks)
- [ ] T065 [P] [US2] Create backend/models/embedding.py with Pydantic models for EmbeddingMetadata (chapter_id, chapter_title, module_id, section_type, chunk_index, file_path, topics)

### Document Ingestion Pipeline

- [ ] T066 [US2] Implement backend/ingestion/markdown_parser.py to read all files from frontend/docs/
- [ ] T067 [US2] Implement backend/ingestion/chunker.py with 500-word chunks and 100-word overlap (respects Markdown section boundaries)
- [ ] T068 [US2] Implement backend/ingestion/embedder.py using OpenAI ada-002 embeddings API
- [ ] T069 [US2] Implement backend/ingestion/vector_store.py with Qdrant client operations (create collection, upsert vectors)
- [ ] T070 [US2] Create backend/scripts/ingest_content.py CLI script to run full ingestion pipeline
- [ ] T071 [US2] Run ingestion script to embed all ~40-60 chapters into Qdrant (expect ~1,500-2,000 chunks)

### RAG Service Implementation

- [ ] T072 [US2] Implement backend/services/retrieval_service.py with Qdrant similarity search (query → top K chunks)
- [ ] T073 [US2] Implement backend/services/response_generator.py using OpenAI completion API with retrieved context
- [ ] T074 [US2] Implement backend/services/rag_service.py orchestrating retrieval + response generation with strict RAG enforcement (no hallucinations)
- [ ] T075 [US2] Add source citation extraction in backend/services/rag_service.py (map chunks → chapter/section references)

### API Endpoints

- [ ] T076 [P] [US2] Implement POST /api/v1/query endpoint in backend/api/routes/query.py (accepts QueryRequest, returns QueryResponse)
- [ ] T077 [P] [US2] Implement GET /api/v1/health endpoint in backend/api/routes/health.py (checks Qdrant and OpenAI connectivity)
- [ ] T078 [US2] Register routes in backend/api/main.py
- [ ] T079 [US2] Add error handling for 400 (invalid query), 429 (rate limit), 500 (internal error)
- [ ] T080 [US2] Run backend with `uvicorn api.main:app --reload` and verify health endpoint

### RAG System Validation

- [ ] T081 [US2] Test POST /api/v1/query with sample question "What is ROS 2?" and verify response cites module-01-ros2
- [ ] T082 [US2] Test RAG accuracy with 10 ground truth questions (expect 90% accuracy per SC-003)
- [ ] T083 [US2] Verify zero hallucinations (all responses traceable to book sections per SC-004)
- [ ] T084 [US2] Test response time <2s p95 latency per SC-002

**Checkpoint**: User Story 2 complete. Backend RAG system is fully functional via API. Chatbot backend can answer questions accurately without hallucinations.

---

## Phase 6: User Story 3 - Context-Aware Text Selection Queries (Priority: P3)

**Goal**: Technical developers can highlight specific passages and ask AI assistant questions focused exclusively on that selected text

**Independent Test**: Select text from any chapter, submit query with selected_text context, verify response focuses only on highlighted content

### Text Selection Context Enhancement

- [ ] T085 [US3] Update backend/models/query.py QueryRequest to require selected_text when query_mode='selected-text'
- [ ] T086 [US3] Implement backend/services/selection_handler.py to filter retrieved chunks by selected text context
- [ ] T087 [US3] Update backend/services/rag_service.py to handle query_mode='selected-text' with context filtering
- [ ] T088 [US3] Add validation in backend/api/routes/query.py to enforce min 20 words, max 2000 words for selected_text

### Frontend Text Selection Component

- [ ] T089 [US3] Create frontend/src/components/ChatBot/TextSelectionContext.tsx using window.getSelection() API
- [ ] T090 [US3] Implement selection capture with Markdown context preservation (code blocks, headers)
- [ ] T091 [US3] Add "Ask about selection" button that appears when text is highlighted
- [ ] T092 [US3] Update frontend/src/components/ChatBot/QueryModeToggle.tsx to switch between full-book and selected-text modes

### Integration & Validation

- [ ] T093 [US3] Integrate TextSelectionContext into chat component, pass selected text to backend via API
- [ ] T094 [US3] Test selected-text query: highlight paragraph about bipedal walking, ask "explain this in simpler terms"
- [ ] T095 [US3] Verify 95% of selected-text queries focus exclusively on highlighted content per SC-010

**Checkpoint**: User Story 3 complete. Text selection feature works independently. Users can ask focused questions about specific passages.

---

## Phase 7: Chat UI Integration (Combines US2 + US3)

**Goal**: Embed @openai/chatkit-react into Docusaurus pages, connecting frontend chat widget to backend RAG API

**Independent Test**: Open any documentation page, submit queries via chat widget, verify responses with source citations, test both full-book and selected-text modes

### Chat Component Setup

- [X] T096 Install @openai/chatkit-react dependency in frontend/ via `pnpm add @openai/chatkit-react`
- [X] T097 Create frontend/src/components/ChatBot/ChatKitWrapper.tsx wrapping @openai/chatkit-react component with session management
- [X] T098 Integrated frontend/src/components/ChatBot/QueryModeToggle.tsx for full-book vs selected-text toggle (from Phase 6)
- [X] T099 ChatKit natively handles source citations and annotations

### Backend Connection

- [X] T100 Created backend/api/routes/chatkit.py with session creation and refresh endpoints
- [X] T101 ChatKit handles loading states natively with streaming responses
- [X] T102 Implemented error handling in ChatKitWrapper component for session errors
- [X] T103 ChatKit includes conversation management (clear, history) natively

### Layout Integration

- [X] T104 Created frontend/src/theme/Root.tsx to provide ChatKit globally on all pages
- [X] T105 Positioned chat widget as fixed overlay (bottom-right corner, expandable/collapsible with toggle button)
- [X] T106 Chat widget integrated via Root component - appears on all documentation pages

### End-to-End Validation

- [ ] T107 Test full-book query: "What sensors are used in humanoid robots?" and verify response cites multiple chapters
- [ ] T108 Test selected-text query: highlight "LIDAR" paragraph, ask "what are the advantages?"
- [ ] T109 Test source citations link back to specific chapters in sidebar navigation
- [ ] T110 Verify response time <3s for 95% of queries per SC-002
- [ ] T111 Test concurrent usage with 10 simulated users (no degradation expected per SC-005)

**Checkpoint**: Chat UI fully integrated. Users can query from any page, receive responses with citations, and use text selection mode.

---

## Phase 8: Deployment

**Goal**: Deploy frontend to GitHub Pages, deploy backend to container platform, validate end-to-end in production

**Independent Test**: Access deployed frontend URL, verify chatbot functional, test navigation and queries in production environment

### Frontend Deployment

- [ ] T112 Create .github/workflows/deploy-frontend.yml with GitHub Actions workflow
- [ ] T113 Configure workflow to run `pnpm run build` and deploy to gh-pages branch
- [ ] T114 Update docusaurus.config.js with production baseUrl and URL
- [ ] T115 Push to main branch and trigger GitHub Actions deployment
- [ ] T116 Verify frontend accessible at `<username>.github.io/<repo>/` or custom domain

### Backend Deployment

- [ ] T117 Create backend/Dockerfile for containerized Python application
- [ ] T118 Configure environment variables in container platform (Railway/Render/Fly.io)
- [ ] T119 Deploy backend container and verify health endpoint accessible
- [ ] T120 Update frontend environment variable BACKEND_API_URL to point to deployed backend

### CORS & Security

- [ ] T121 Update backend/api/middleware/cors.py to allow production frontend domain
- [ ] T122 Configure rate limiting for production traffic (stricter limits per backend/api/middleware/rate_limit.py)
- [ ] T123 Test CORS: Submit query from deployed frontend to deployed backend

### Production Validation

- [ ] T124 Run end-to-end test: navigate to deployed site, navigate through modules (verify SC-001: <10s to any chapter)
- [ ] T125 Submit 10 test queries via deployed chatbot, verify responses and source citations
- [ ] T126 Monitor backend logs for errors or performance issues
- [ ] T127 Verify system uptime 99.5% over first 24 hours per SC-009

**Checkpoint**: System fully deployed. Frontend and backend operational in production. All success criteria validated.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories or overall system quality

- [ ] T128 [P] Create comprehensive README.md at repository root with architecture overview, setup instructions, deployment guide
- [ ] T129 [P] Document API endpoints in specs/001-system-architecture/contracts/backend-api.openapi.yaml
- [ ] T130 [P] Create backend/scripts/validate_vectors.py to verify Qdrant vector store integrity
- [ ] T131 [P] Add logging for all backend operations (ingestion, queries, errors) using Python logging module
- [ ] T132 [P] Implement query result caching in backend/services/rag_service.py (cache common queries for 1 hour)
- [ ] T133 [P] Add analytics tracking for query patterns (optional: which chapters are queried most)
- [ ] T134 [P] Security audit: Review input validation, rate limiting, CORS policy, API key handling
- [ ] T135 [P] Performance optimization: Profile backend response time, optimize chunking if needed
- [ ] T136 Code cleanup: Remove unused imports, format with Black (Python) and Prettier (TypeScript)
- [ ] T137 Create quickstart validation checklist in specs/001-system-architecture/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) completion - BLOCKS all user stories
- **User Story 4 (Phase 3)**: Depends on Foundational - BLOCKS US1 and US2 (content must exist before display/search)
- **User Story 1 (Phase 4)**: Depends on US4 completion (content must be generated first)
- **User Story 2 (Phase 5)**: Depends on US4 completion (content must be generated before embedding)
- **User Story 3 (Phase 6)**: Depends on US2 completion (extends RAG with selection context)
- **Chat UI Integration (Phase 7)**: Depends on US2 and US3 completion (integrates backend with frontend)
- **Deployment (Phase 8)**: Depends on all desired user stories being complete
- **Polish (Phase 9)**: Can run in parallel with deployment or after

### User Story Dependencies

```
Foundational (Phase 2) - REQUIRED FIRST
    ↓
US4 (Phase 3: Content Generation) - REQUIRED BEFORE US1/US2
    ↓
    ├─→ US1 (Phase 4: Read Content) - CAN RUN IN PARALLEL WITH US2
    └─→ US2 (Phase 5: RAG Chatbot) - CAN RUN IN PARALLEL WITH US1
            ↓
        US3 (Phase 6: Text Selection) - DEPENDS ON US2
            ↓
        Chat UI Integration (Phase 7) - COMBINES US2 + US3
            ↓
        Deployment (Phase 8)
```

### Critical Path

1. Setup (Phase 1) → 2. Foundational (Phase 2) → 3. Content Generation (US4) → 4. RAG Backend (US2) → 5. Text Selection (US3) → 6. Chat UI (Phase 7) → 7. Deployment (Phase 8)

**Estimated Timeline**:
- Setup: 1 day
- Foundational: 2-3 days
- Content Generation (US4): 5-7 days (40-60 chapters, quality review)
- Read Content (US1): 2-3 days (can overlap with US4)
- RAG Backend (US2): 5-7 days (ingestion, RAG service, API)
- Text Selection (US3): 2-3 days
- Chat UI Integration: 3-4 days
- Deployment: 2-3 days
- **Total: 22-30 days** (single developer, sequential)

### Parallel Opportunities

- **Phase 1 (Setup)**: T001-T004 all marked [P] - run in parallel
- **Phase 2 (Foundational)**: T005-T014 (backend) and T015-T020 (frontend) can run in parallel
- **Phase 3 (US4)**: T025-T048 (content generation) all marked [P] - run in parallel (batch generation)
- **After US4 completes**: US1 and US2 can run in parallel (different codebases: frontend display vs backend RAG)
- **Phase 9 (Polish)**: T128-T137 all marked [P] - run in parallel

---

## Parallel Example: Content Generation (US4)

All chapter generation tasks are parallelizable because they create different files:

```bash
# Launch all Module 1 chapters together:
Task: "Generate frontend/docs/module-01-ros2/chapter-01-fundamentals.md"
Task: "Generate frontend/docs/module-01-ros2/chapter-02-nodes-topics.md"
Task: "Generate frontend/docs/module-01-ros2/chapter-03-urdf.md"

# Launch all Module 2 chapters together:
Task: "Generate frontend/docs/module-02-simulation/chapter-01-gazebo-setup.md"
Task: "Generate frontend/docs/module-02-simulation/chapter-02-physics-simulation.md"
Task: "Generate frontend/docs/module-02-simulation/chapter-03-unity-integration.md"
```

---

## Implementation Strategy

### MVP First (Minimum Viable Product)

**Goal**: Readable documentation with AI chatbot (US1 + US2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: US4 (Content Generation) - BLOCKS MVP
4. Complete Phase 4: US1 (Read Content) - MVP Feature 1
5. Complete Phase 5: US2 (RAG Chatbot) - MVP Feature 2
6. Complete Phase 7: Chat UI Integration
7. Complete Phase 8: Deployment
8. **STOP and VALIDATE**: Test MVP independently

**MVP Success Criteria**:
- Users can read all book content with clean navigation (SC-001)
- Users can ask questions and get accurate responses with citations (SC-002, SC-003, SC-004)
- System handles 100 concurrent users (SC-005)

### Incremental Delivery

1. **Foundation** (Phases 1-2): Setup + infrastructure → Can start user stories
2. **Content** (Phase 3, US4): Book content generated → Can display and search
3. **MVP** (Phases 4-5, US1 + US2): Documentation + Chatbot → Deploy/Demo
4. **Enhancement** (Phase 6, US3): Text selection → Deploy/Demo
5. **Production** (Phase 8): Full deployment with monitoring

### Parallel Team Strategy

With 3 developers:

1. **All devs**: Complete Setup + Foundational together (Phases 1-2)
2. **All devs**: Complete Content Generation together (Phase 3, US4) - BLOCKS everything
3. **After US4 completes**:
   - **Developer A**: User Story 1 (Frontend display)
   - **Developer B**: User Story 2 (Backend RAG)
   - **Developer C**: Prepare deployment infrastructure
4. **Developer A + B**: Chat UI Integration (Phase 7)
5. **Developer C**: Deploy and monitor (Phase 8)
6. **All devs**: Polish (Phase 9) in parallel

---

## Notes

- [P] tasks = different files, no dependencies between them
- [Story] label maps task to specific user story (US1, US2, US3, US4) for traceability
- **Content Generation (US4) is critical path** - all other user stories depend on it
- US1 and US2 can run in parallel after US4 completes (frontend vs backend)
- Each user story should be independently testable at its checkpoint
- Commit after each task or logical group of parallel tasks
- Stop at any checkpoint to validate story independently
- **Success criteria validation**: After each phase, check relevant SC-XXX criteria from spec.md
- **Constitution compliance**: All tasks implement mandated architecture (frontend/docs/, pnpm, Docusaurus, FastAPI, Qdrant)
