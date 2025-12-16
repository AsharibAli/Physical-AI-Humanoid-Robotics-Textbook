# Implementation Plan: Physical AI & Humanoid Robotics Interactive Textbook Platform

**Branch**: `001-system-architecture` | **Date**: 2025-12-16 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-system-architecture/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Create a comprehensive interactive textbook platform for Physical AI & Humanoid Robotics that combines static documentation (Docusaurus frontend), AI-powered Q&A (FastAPI + RAG backend), and automated content generation. The platform enables technical developers and AI engineers to learn through clean, minimalist documentation enhanced by an embedded chatbot that answers questions with strict adherence to book content (no hallucinations). Content generation workflow produces publication-quality Markdown chapters following a consistent structure (Concepts, Architectures, Algorithms, Real-World Considerations).

**Technical Approach**: Monorepo structure with clear frontend/backend separation. Frontend deployed as static site to GitHub Pages. Backend deployed as standalone API service. Content generation happens during development phase before embedding and deployment.

## Technical Context

**Language/Version**:
- Frontend: Node.js 20.x LTS (Docusaurus requires Node 18+)
- Backend: Python 3.11+ (for FastAPI async features and type hints)

**Primary Dependencies**:
- Frontend: Docusaurus 3.x, @openai/chatkit-react (chat UI), pnpm 8.x (package manager)
- Backend: FastAPI 0.109+, Qdrant Client 1.7+, OpenAI Python SDK 1.10+, Pydantic 2.x
- Content Generation: OpenAI API (GPT-4 or equivalent for technical accuracy)

**Storage**:
- Vector Store: Qdrant Cloud (free tier: 1GB vectors, sufficient for ~500 pages)
- Metadata/Chat History: Optional Neon Serverless Postgres (free tier: 512MB)
- Static Content: Git repository + GitHub Pages CDN

**Testing**:
- Frontend: Jest (unit tests), Playwright (E2E tests for chat integration)
- Backend: pytest (unit), pytest-asyncio (async endpoints), httpx (API client tests)
- Content Validation: Custom Markdown linters, structure validators

**Target Platform**:
- Frontend: Static HTML/JS/CSS deployed to GitHub Pages (CDN)
- Backend: Linux containers (Docker) deployable to Render/Railway/Fly.io
- Development: Windows/Linux/macOS (cross-platform via pnpm + Python venv)

**Project Type**: Web application (frontend + backend separation)

**Performance Goals**:
- Frontend: First Contentful Paint <1.5s, Time to Interactive <3s
- Backend: p95 query latency <2s, embedding generation <5s per chapter
- Vector search: <500ms for similarity retrieval (depends on Qdrant Cloud)
- Concurrent users: 100 simultaneous queries without degradation

**Constraints**:
- Frontend bundle size: <500KB gzipped (excluding content Markdown)
- Backend memory: <512MB per instance (for free tier compatibility)
- Rate limits: OpenAI API 3,500 RPM (Tier 1), Qdrant Cloud 1 RPS (free tier)
- Content generation: Serial processing (avoid parallel API calls to respect rate limits)
- Markdown files: Maximum 10,000 words per chapter for optimal chunking

**Scale/Scope**:
- Expected content: 12 modules × 3-5 chapters = ~40-60 Markdown files
- Total book length: ~150,000-200,000 words
- Vector store: ~1,500-2,000 text chunks (500-word chunks with 100-word overlap)
- Expected users: 50-500 concurrent readers during peak (post-launch)
- Chat queries: ~100-500 per day (estimated based on documentation patterns)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### ✅ PASS: I. Content Generation & Book Authorship

**Rule**: Generate complete technical book content as professional Markdown under `frontend/docs/`

**Compliance**:
- User Story 4 (P1) explicitly covers book content generation
- FR-023 through FR-029 define content generation requirements
- Book-Content-Details.md used as reference guide (not verbatim copy)
- Content destination: `frontend/docs/` per constitution

**Evidence**: Spec sections 8-11 (User Story 4), requirements FR-023 to FR-029

---

### ✅ PASS: II. Spec-Driven Development

**Rule**: All implementation driven by spec.md, plan.md, tasks.md before code

**Compliance**:
- spec.md created and validated (13/13 quality checks passed)
- plan.md (this document) generated via `/sp.plan`
- tasks.md will be generated via `/sp.tasks` before implementation
- Each subsystem has clear requirements in spec

**Evidence**: specs/001-system-architecture/ directory structure

---

### ✅ PASS: III. Modular Coherence

**Rule**: Book is unified product with consistent terminology and clear learning progression

**Compliance**:
- Content generation includes consistency requirements (FR-026, FR-028)
- Book-Content-Details.md provides module progression (Weeks 1-13 breakdown)
- Each chapter requires four sections: Concepts, Architectures, Algorithms, Real-World Considerations
- Content validation includes coherence checks (FR-029)

**Evidence**: FR-024, FR-026, FR-028, Book-Content-Details.md lines 14-93

---

### ✅ PASS: IV. Quality Over Quantity

**Rule**: No filler content, concrete examples, runnable code

**Compliance**:
- Content generation targets technical audience (developers, AI engineers)
- Success criteria SC-007: 90% first-generation pass rate (quality gate)
- Validation checks for completeness and structural correctness (FR-029)
- Target audience explicitly defined in spec

**Evidence**: FR-027, SC-007, spec.md lines 164-171 (Key Assumptions)

---

### ✅ PASS: V. RAG-First Documentation Architecture

**Rule**: Embedded chatbot as core feature with strict RAG enforcement

**Compliance**:
- RAG system is P2 user story (core feature)
- Backend requirements FR-007 through FR-015 (9 requirements for RAG)
- Chatbot integration FR-016 through FR-022 (7 requirements)
- Strict no-hallucination requirement: FR-011, SC-004

**Evidence**: User Story 2 (P2), FR-011, SC-004, spec.md lines 154

---

### ✅ PASS: VI. Tech Stack Adherence

**Rule**: Use only specified stack (Docusaurus, pnpm, FastAPI, Qdrant, OpenAI)

**Compliance**:
- Frontend: Docusaurus + pnpm (per constitution)
- Backend: FastAPI + Qdrant Cloud + OpenAI API (per constitution)
- Chatbot: @openai/chatkit-react (specified in user input)
- No alternative technologies proposed

**Evidence**: Technical Context section above, constitution lines 125-143

---

### ✅ PASS: VII. Progressive Disclosure & Layered Learning

**Rule**: Introduce concepts before using them, explicit knowledge prerequisites

**Compliance**:
- Book-Content-Details.md follows week-by-week progression (Weeks 1-13)
- Module 1 (ROS basics) precedes Module 3 (Isaac platform)
- Content structure enforces layered approach via four required sections
- Each chapter builds on previous knowledge per Book-Content-Details

**Evidence**: Book-Content-Details.md lines 58-93 (Weekly Breakdown)

---

### ✅ PASS: VIII. Test-Driven Documentation

**Rule**: Code examples must be tested and verified before inclusion

**Compliance**:
- Content validation requirement (FR-029) includes correctness checks
- Testing strategy defined in Technical Context (pytest for backend, Jest/Playwright for frontend)
- Acceptance scenarios define verification methods

**Evidence**: FR-029, spec.md User Story 4 acceptance scenarios

---

### ✅ PASS: IX. UI Minimalism

**Rule**: Clean, minimal Docusaurus theme prioritizing content readability

**Compliance**:
- Frontend requirements emphasize minimalism (FR-003: "clean typography")
- User input specifies "Minimalist, Clean typography, Low visual noise"
- No unnecessary UI embellishments in requirements
- Focus on sidebar navigation and content display

**Evidence**: FR-003, FR-006, spec.md lines 6-11 (user input)

---

### ✅ PASS: Repository Structure

**Rule**: Separate frontend/ and backend/ directories with clean separation

**Compliance**:
- Project structure below implements required frontend/backend split
- All book content in `frontend/docs/` (constitutional requirement)
- Backend independently deployable
- No mixing of concerns

**Evidence**: Project Structure section below

---

**Constitution Check Result**: ✅ ALL GATES PASSED (10/10)

**Proceed to**: Phase 0 Research

## Project Structure

### Documentation (this feature)

```text
specs/001-system-architecture/
├── spec.md                      # ✅ Complete (218 lines)
├── plan.md                      # This file
├── research.md                  # Phase 0 output (to be created)
├── data-model.md                # Phase 1 output (to be created)
├── quickstart.md                # Phase 1 output (to be created)
├── contracts/                   # Phase 1 output (to be created)
│   ├── backend-api.openapi.yaml # OpenAPI spec for RAG endpoints
│   └── embedding-schema.json    # Vector embedding metadata schema
├── checklists/
│   └── requirements.md          # ✅ Complete (quality validation passed)
└── tasks.md                     # Phase 2 output (/sp.tasks - not created by /sp.plan)
```

### Source Code (repository root)

```text
Physical-AI-Humanoid-Robotics-Textbook/
├── frontend/
│   ├── docs/                    # All book Markdown content (generated)
│   │   ├── intro.md            # Landing page
│   │   ├── module-01-ros2/     # Module 1: ROS 2 Nervous System
│   │   │   ├── index.md
│   │   │   ├── chapter-01-fundamentals.md
│   │   │   ├── chapter-02-nodes-topics.md
│   │   │   └── chapter-03-urdf.md
│   │   ├── module-02-simulation/
│   │   ├── module-03-isaac/
│   │   ├── module-04-vla/
│   │   └── [... 8 more modules]
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── ChatBot/       # @openai/chatkit-react wrapper
│   │   │   │   ├── ChatInterface.tsx
│   │   │   │   ├── TextSelectionContext.tsx
│   │   │   │   └── QueryModeToggle.tsx
│   │   │   └── Layout/
│   │   ├── pages/              # Custom pages (optional)
│   │   ├── theme/              # Docusaurus theme customization
│   │   └── css/
│   │       └── custom.css      # Minimalist styling
│   ├── static/
│   │   ├── img/               # Diagrams, architecture images
│   │   └── assets/
│   ├── docusaurus.config.js   # Docusaurus configuration
│   ├── sidebars.js            # Sidebar navigation structure
│   ├── package.json
│   ├── pnpm-lock.yaml
│   └── tsconfig.json
│
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI application entry
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── query.py       # POST /query endpoint
│   │   │   ├── health.py      # GET /health endpoint
│   │   │   └── admin.py       # Embedding management (optional)
│   │   └── middleware/
│   │       ├── cors.py        # CORS configuration
│   │       ├── rate_limit.py  # Rate limiting
│   │       └── auth.py        # Optional API key validation
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── markdown_parser.py # Parse frontend/docs/ Markdown
│   │   ├── chunker.py         # Text chunking (500-word with overlap)
│   │   ├── embedder.py        # OpenAI embedding generation
│   │   └── vector_store.py    # Qdrant client operations
│   ├── models/
│   │   ├── __init__.py
│   │   ├── query.py           # Pydantic models for query/response
│   │   ├── embedding.py       # Embedding metadata schema
│   │   └── conversation.py    # Optional: conversation history
│   ├── services/
│   │   ├── __init__.py
│   │   ├── rag_service.py     # Core RAG logic
│   │   ├── retrieval_service.py # Vector similarity search
│   │   └── response_generator.py # OpenAI completion with context
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py        # Environment-based configuration
│   │   └── qdrant_config.py   # Qdrant connection settings
│   ├── scripts/
│   │   ├── ingest_content.py  # CLI script to embed all docs
│   │   └── validate_vectors.py # Verify vector store integrity
│   ├── tests/
│   │   ├── unit/
│   │   │   ├── test_chunker.py
│   │   │   ├── test_embedder.py
│   │   │   └── test_rag_service.py
│   │   ├── integration/
│   │   │   ├── test_api_endpoints.py
│   │   │   └── test_qdrant_operations.py
│   │   └── fixtures/
│   │       └── sample_markdown.md
│   ├── .env.example           # Environment variables template
│   ├── .python-version        # Python version specification
│   ├── pyproject.toml         # Project metadata and dependencies
│   ├── uv.lock                # Dependency lock file (managed by uv)
│   └── Dockerfile             # Container image for backend
│
├── .github/
│   └── workflows/
│       ├── deploy-frontend.yml # GitHub Actions: Deploy to Pages
│       └── test-backend.yml    # GitHub Actions: Backend tests
│
├── .specify/                   # Spec-Kit Plus framework
│   ├── memory/
│   │   └── constitution.md     # ✅ Constitution v2.0.0
│   ├── templates/
│   └── scripts/
│
├── specs/                      # Feature specifications
│   └── 001-system-architecture/ # This feature
│
├── history/
│   └── prompts/
│       └── system-architecture/
│           └── 001-system-architecture-specification.spec.prompt.md
│
├── .gitignore
├── README.md                   # Project overview and quickstart
├── Book-Content-Details.md     # ✅ Reference guide for content generation
└── pnpm-workspace.yaml         # pnpm monorepo configuration (optional)
```

**Structure Decision**:

Selected **Option 2: Web application** structure due to clear frontend/backend separation mandated by constitution (v2.0.0, lines 190-217). This architecture provides:

1. **Independent Deployment**: Frontend as static site (GitHub Pages), backend as API service (containerized)
2. **Technology Isolation**: Node.js ecosystem (frontend) vs Python ecosystem (backend)
3. **Scalability**: Backend can scale independently based on query load
4. **Development Workflow**: Teams can work on frontend (content + UI) and backend (RAG) in parallel
5. **Cost Optimization**: Static frontend has zero hosting cost, backend uses free tier services

The `frontend/docs/` location for book content is constitutionally mandated (constitution lines 50-51, 195-196). The backend ingestion pipeline reads from this location to generate embeddings.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

*No violations detected. All constitutional requirements are met by the proposed architecture.*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A       | N/A        | N/A                                 |

## Phase 0: Research & Outline

**Objective**: Resolve all technical unknowns and establish best practices for each component.

### Research Tasks

Based on the Technical Context analysis, the following areas require investigation to ensure optimal implementation:

#### R1: Docusaurus Chat Integration Pattern

**Unknown**: How to embed @openai/chatkit-react into Docusaurus pages without conflicting with React hydration

**Research Questions**:
- What is the recommended pattern for embedding third-party React components in Docusaurus?
- How to handle SSR (server-side rendering) vs client-side rendering for chat widget?
- Where should the chat component be mounted (global vs per-page)?
- How to pass selected text from documentation to chat component?

**Deliverable**: Architectural pattern for chat integration with code examples

---

#### R2: Markdown Chunking Strategy for RAG

**Unknown**: Optimal chunk size and overlap for semantic retrieval from technical documentation

**Research Questions**:
- What chunk size (tokens/words) works best for technical content with code blocks?
- How to handle chunk boundaries (mid-sentence, mid-code-block)?
- Should chunks respect Markdown section boundaries (headers)?
- What metadata to attach to chunks (chapter, section, topic tags)?
- How to handle cross-references between chunks?

**Deliverable**: Chunking algorithm specification with parameters

---

#### R3: Qdrant Cloud Free Tier Limits

**Unknown**: Practical limits of Qdrant Cloud free tier for estimated content volume

**Research Questions**:
- Free tier: 1GB vectors = how many 1536-dimensional embeddings (OpenAI ada-002)?
- Rate limits: 1 RPS sufficient for 100 concurrent users with caching?
- Latency expectations: p95 search latency for 2,000 vectors?
- Upgrade triggers: When to move to paid tier?

**Deliverable**: Capacity plan with scaling thresholds

---

#### R4: FastAPI Streaming Responses for Chat

**Unknown**: Whether to implement streaming responses for real-time chat experience

**Research Questions**:
- Does @openai/chatkit-react support streaming responses (SSE/WebSocket)?
- FastAPI StreamingResponse vs standard JSON response for RAG queries?
- Tradeoff: streaming complexity vs perceived responsiveness?
- OpenAI API: stream=True for completion API?

**Deliverable**: Decision document with performance tradeoffs

---

#### R5: Content Generation Workflow

**Unknown**: Best practice for generating 40-60 consistent, high-quality Markdown chapters

**Research Questions**:
- Serial generation (one chapter at a time) vs batch generation?
- How to maintain consistent terminology across 150k-200k words?
- Should we generate outline first, then expand? Or full chapters directly?
- Quality validation: automated checks vs manual review?
- Regeneration strategy for chapters that fail quality checks?

**Deliverable**: Content generation pipeline design

---

#### R6: Text Selection Context Handling

**Unknown**: How to capture and transmit selected text from Docusaurus to backend

**Research Questions**:
- Browser API: `window.getSelection()` sufficient or need library?
- How to preserve Markdown context (code blocks, headers) in selection?
- Should selected text include surrounding paragraphs for context?
- Backend: How to distinguish full-book vs selected-text queries?

**Deliverable**: Text selection implementation pattern

---

#### R7: Embedding Cost Estimation

**Unknown**: Total cost for generating embeddings for entire book content

**Research Questions**:
- OpenAI ada-002 pricing: $0.0001 per 1K tokens
- Estimated total tokens: 150k words × 1.3 (tokens/words) = ~195k tokens
- Chunks: 195k ÷ 500-word chunks = ~390 chunks × 650 tokens/chunk = ~253k tokens
- Cost: 253k tokens × $0.0001/1k = ~$0.025 (one-time)
- Re-embedding after content updates: How often?

**Deliverable**: Cost model and budget allocation

---

#### R8: GitHub Pages Deployment with Backend CORS

**Unknown**: CORS configuration for static frontend (GitHub Pages) calling backend API

**Research Questions**:
- GitHub Pages domain: `<username>.github.io/<repo>/`
- Backend domain: Custom domain or Railway/Render default?
- CORS policy: Allow all origins (public API) or restrict to GitHub Pages domain?
- Preflight requests: How to handle OPTIONS method?

**Deliverable**: CORS configuration and deployment checklist

---

### Research Consolidation

**Output Location**: `specs/001-system-architecture/research.md`

**Format** (per specification):
```markdown
# Research Findings: [Feature Name]

## R1: [Research Task Name]

**Decision**: [What was chosen]

**Rationale**: [Why chosen, with evidence/benchmarks]

**Alternatives Considered**:
- [Alternative 1]: [Why rejected]
- [Alternative 2]: [Why rejected]

**Implementation Notes**: [Key technical details]

---

[Repeat for R2-R8]
```

**Next Step**: After `research.md` is complete, proceed to Phase 1.

## Phase 1: Design & Contracts

**Prerequisite**: `research.md` complete with all research tasks resolved

### P1.1: Data Model Design

**Input**: Key Entities from spec.md (lines 132-146)

**Output**: `specs/001-system-architecture/data-model.md`

**Entities to Model**:

1. **Chapter** (Frontend & Backend)
   - Fields: `id`, `title`, `description`, `module_id`, `chapter_number`, `file_path`, `topics[]`
   - Relationships: Has many `Module`, belongs to `Book`
   - Validation: `title` required, `chapter_number` unique within module

2. **Module** (Frontend & Backend)
   - Fields: `id`, `title`, `markdown_content`, `parent_chapter_id`, `module_number`, `sections{}`, `prerequisites[]`
   - Relationships: Belongs to `Chapter`
   - Validation: Must contain all four required sections (concepts, architectures, algorithms, real-world)

3. **Embedding** (Backend only - Qdrant)
   - Fields: `vector[1536]`, `source_reference{}`, `text_chunk`, `metadata{}`
   - Metadata schema: `chapter_id`, `module_id`, `section_type`, `chunk_index`, `file_path`
   - Validation: Vector dimension must match OpenAI ada-002 (1536)

4. **Query** (Backend - API Request)
   - Fields: `query_text`, `query_mode`, `session_id`, `selected_text?`, `max_results?`
   - Validation: `query_text` max 500 chars, `query_mode` enum ['full-book', 'selected-text']

5. **Response** (Backend - API Response)
   - Fields: `response_text`, `source_citations[]`, `confidence_score`, `session_id`, `retrieved_chunks[]`
   - Citations schema: `chapter_title`, `module_title`, `section_type`, `file_path`

6. **ConversationSession** (Backend - Optional Postgres)
   - Fields: `session_id`, `query_response_pairs[]`, `created_at`, `last_activity_at`, `user_context{}`
   - Validation: `session_id` UUID v4, expires after 24 hours inactive

7. **ContentTemplate** (Backend - Content Generation)
   - Fields: `section_definitions[]`, `formatting_guidelines`, `style_requirements`, `validation_rules[]`
   - Sections: `concepts`, `architectures`, `algorithms`, `real_world_considerations`

**Data Model Deliverable**: Markdown document with:
- Entity definitions (fields, types, constraints)
- Relationship diagrams (ASCII or Mermaid syntax)
- Validation rules per entity
- Storage mapping (Qdrant, Postgres, Git)

---

### P1.2: API Contracts

**Input**: Functional Requirements FR-007 through FR-022 (Backend + Chatbot)

**Output**: `specs/001-system-architecture/contracts/`

#### Contract 1: Backend API (OpenAPI Spec)

**File**: `contracts/backend-api.openapi.yaml`

**Endpoints to Define**:

1. **POST /api/v1/query**
   - Description: Submit query to RAG system
   - Request body: `Query` model
   - Response: `Response` model
   - Error codes: 400 (invalid query), 429 (rate limit), 500 (internal)

2. **GET /api/v1/health**
   - Description: Health check for backend service
   - Response: `{ "status": "healthy", "qdrant_connected": bool, "openai_available": bool }`

3. **POST /api/v1/embed** (Admin only, optional)
   - Description: Trigger re-embedding of content
   - Request: `{ "file_paths": string[] }`
   - Response: `{ "embedded_count": int, "failed_count": int }`
   - Auth: API key required

4. **GET /api/v1/stats** (Optional)
   - Description: Query statistics
   - Response: `{ "total_queries": int, "avg_response_time_ms": float, "cache_hit_rate": float }`

**OpenAPI Spec Must Include**:
- Schema definitions for all request/response models
- Example payloads for each endpoint
- Error response schemas
- Security schemes (API key for admin endpoints)
- Rate limit headers (`X-RateLimit-Limit`, `X-RateLimit-Remaining`)

---

#### Contract 2: Embedding Metadata Schema

**File**: `contracts/embedding-schema.json`

**Purpose**: Define metadata structure attached to each vector in Qdrant

**Schema**:
```json
{
  "chapter_id": "string (e.g., 'module-01-ros2')",
  "chapter_title": "string (e.g., 'The Robotic Nervous System')",
  "module_id": "string (e.g., 'chapter-01-fundamentals')",
  "module_title": "string (e.g., 'ROS 2 Architecture')",
  "section_type": "enum ['concepts', 'architectures', 'algorithms', 'real-world', 'introduction', 'other']",
  "chunk_index": "integer (0-based position within module)",
  "file_path": "string (relative path: 'docs/module-01-ros2/chapter-01-fundamentals.md')",
  "word_count": "integer (chunk size for analytics)",
  "topics": "array<string> (extracted keywords/tags)",
  "generated_at": "ISO 8601 timestamp"
}
```

**Validation Rules**:
- All fields required except `topics`
- `section_type` must match one of five values
- `file_path` must exist in `frontend/docs/`
- `chunk_index` must be sequential within same `module_id`

---

### P1.3: Quickstart Guide

**Output**: `specs/001-system-architecture/quickstart.md`

**Target Audience**: Developers setting up local development environment

**Required Sections**:

1. **Prerequisites**
   - Node.js 20.x LTS
   - Python 3.11+
   - pnpm 8.x (`npm install -g pnpm`)
   - uv (Modern Python package manager: `pip install uv` or see https://github.com/astral-sh/uv)
   - Git
   - Qdrant Cloud account (free tier)
   - OpenAI API key

2. **Repository Setup**
   ```bash
   git clone <repo-url>
   cd Physical-AI-Humanoid-Robotics-Textbook
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   pnpm install
   pnpm run start  # Development server on localhost:3000
   ```

4. **Backend Setup**
   ```bash
   cd backend

   # Sync dependencies (creates .venv automatically)
   uv sync

   # Configure environment
   cp .env.example .env
   # Edit .env: Add OPENAI_API_KEY, QDRANT_URL, QDRANT_API_KEY

   # Run ingestion script
   uv run python -m scripts.ingest_content

   # Start API server
   uv run uvicorn api.main:app --reload  # localhost:8000
   ```

5. **Verify Integration**
   - Open frontend (localhost:3000)
   - Open chat widget
   - Submit test query: "What is ROS 2?"
   - Verify response with source citations

6. **Common Issues**
   - CORS errors: Check backend CORS middleware allows `http://localhost:3000`
   - Embedding failures: Verify OpenAI API key has sufficient quota
   - Qdrant connection: Check firewall allows outbound HTTPS to Qdrant Cloud

---

### P1.4: Agent Context Update

**Action**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude`

**Purpose**: Update Claude-specific context file with technologies from this plan

**Technologies to Add**:
- Frontend: Docusaurus 3.x, @openai/chatkit-react, pnpm
- Backend: FastAPI, Qdrant Client, OpenAI SDK, Pydantic
- Deployment: GitHub Pages, Docker containers

**Preservation**: Existing manual entries in context file must be preserved between markers

---

## Re-evaluation: Constitution Check (Post-Design)

**Trigger**: After Phase 1 design artifacts are created

**Verification**:

1. **Repository Structure Compliance**
   - ✅ frontend/ directory exists with docs/ subdirectory
   - ✅ backend/ directory exists with api/, ingestion/, services/ structure
   - ✅ Clean separation (no mixed concerns)

2. **Content Location Compliance**
   - ✅ All book Markdown in `frontend/docs/` (per constitution line 51, 196)

3. **Tech Stack Compliance**
   - ✅ pnpm (not npm/yarn)
   - ✅ Docusaurus for documentation
   - ✅ FastAPI for backend
   - ✅ Qdrant Cloud for vectors
   - ✅ OpenAI for embeddings and RAG

4. **RAG Architecture Compliance**
   - ✅ Strict RAG enforcement (no hallucinations) in API contract
   - ✅ Source citations in response model
   - ✅ Two query modes (full-book, selected-text) supported

5. **Data Model Compliance**
   - ✅ All entities from spec.md modeled
   - ✅ Validation rules enforce data integrity
   - ✅ Metadata schema supports book structure

**Result**: ✅ ALL GATES REMAIN PASSED

**Proceed to**: Phase 2 (Task Breakdown via `/sp.tasks` command)

---

## Execution Phases (Implementation Roadmap)

**Note**: Detailed task breakdown will be generated via `/sp.tasks`. The phases below provide high-level sequencing aligned with user input.

### Phase 1: Repository & Tooling

**Objective**: Initialize monorepo structure with proper tooling

**Key Activities**:
- Create `frontend/` and `backend/` directories
- Initialize pnpm workspace (optional: `pnpm-workspace.yaml`)
- Configure `.gitignore` for Node/Python
- Set up GitHub repository with branch protection
- Initialize Git submodules if needed

**Completion Criteria**:
- Directory structure matches Project Structure section
- `pnpm install` succeeds in frontend/
- `uv sync` succeeds in backend/
- Git repository configured with main branch

---

### Phase 2: Frontend Setup

**Objective**: Scaffold Docusaurus documentation site with minimalist UI

**Key Activities**:
- Run `npx create-docusaurus@latest frontend classic --typescript`
- Configure `docusaurus.config.js` (site title, tagline, GitHub Pages deployment)
- Apply minimalist theme (custom CSS, remove unnecessary sidebar items)
- Configure sidebar structure for 12 modules
- Create placeholder `docs/intro.md`

**Completion Criteria**:
- `pnpm run start` serves site on localhost:3000
- Sidebar navigation structure matches Book-Content-Details modules
- Minimalist UI applied (clean typography, no visual noise)
- Build succeeds (`pnpm run build`)

---

### Phase 3: Book Content Generation

**Objective**: Generate all Markdown chapters using Book-Content-Details.md as reference

**Key Activities**:
- Create content generation script (Python or Node.js)
- For each module (1-12):
  - Generate 3-5 chapters per module
  - Each chapter has four sections: Concepts, Architectures, Algorithms, Real-World
  - Maintain consistent terminology across chapters
  - Validate Markdown syntax and structure
- Store under `frontend/docs/`
- Update `sidebars.js` with generated content

**Completion Criteria**:
- 40-60 Markdown files generated in `frontend/docs/`
- Each file passes structure validation (four required sections)
- Content reads like professional technical book (not filler)
- Docusaurus site renders all chapters with navigation
- Total word count: 150k-200k words

**Quality Gate**: SC-007 (90% first-generation pass rate)

---

### Phase 4: Backend RAG System

**Objective**: Build FastAPI service with embedding generation and vector storage

**Key Activities**:
- Implement markdown parser (`backend/ingestion/markdown_parser.py`)
- Implement chunking algorithm (500-word chunks, 100-word overlap)
- Implement embedder (OpenAI API integration)
- Configure Qdrant client and create collection
- Implement ingestion script (`backend/scripts/ingest_content.py`)
- Run ingestion: Read `frontend/docs/`, generate embeddings, store in Qdrant
- Implement RAG service (query → retrieve → generate response)
- Implement API endpoints (POST /query, GET /health)
- Configure CORS middleware for GitHub Pages origin

**Completion Criteria**:
- All content embedded in Qdrant (~1,500-2,000 vectors)
- API endpoints functional and tested
- Response time <2s p95 (SC-002)
- RAG accuracy 90% on test queries (SC-003)
- Zero hallucinations detected (SC-004)

**Quality Gate**: FR-011 (enforce RAG-only responses)

---

### Phase 5: Chat UI Integration

**Objective**: Embed @openai/chatkit-react in Docusaurus frontend

**Key Activities**:
- Install @openai/chatkit-react in frontend
- Create chat component wrapper (`src/components/ChatBot/ChatInterface.tsx`)
- Implement text selection context capture
- Implement query mode toggle (full-book vs selected-text)
- Integrate chat component into Docusaurus layout (global or per-page)
- Connect chat widget to backend API (POST /query)
- Handle loading states and error messages
- Display source citations in chat responses

**Completion Criteria**:
- Chat widget visible on all documentation pages
- Users can submit queries and receive responses
- Selected-text mode captures highlighted passages
- Source citations link back to specific chapters/sections
- Response time <3s for 95% of queries (SC-002)
- 95% of selected-text queries focus exclusively on selection (SC-010)

**Quality Gate**: FR-016 through FR-022 (7 chatbot requirements)

---

### Phase 6: Deployment

**Objective**: Deploy frontend to GitHub Pages and validate end-to-end

**Key Activities**:
- Configure GitHub Actions workflow (`.github/workflows/deploy-frontend.yml`)
- Build production frontend bundle (`pnpm run build`)
- Deploy to GitHub Pages (gh-pages branch)
- Deploy backend to container platform (Railway/Render/Fly.io)
- Configure custom domain (optional)
- Update CORS policy for production domain
- Run end-to-end tests (query chatbot on deployed site)
- Monitor performance (First Contentful Paint, Time to Interactive)

**Completion Criteria**:
- Frontend accessible at `<username>.github.io/<repo>/` or custom domain
- Backend API accessible and health check passing
- Chatbot functional on deployed site
- Navigation <10s to any chapter (SC-001)
- System handles 100 concurrent users (SC-005)
- Uptime 99.5% (SC-009)

**Quality Gate**: All 10 success criteria from spec.md met

---

## Next Steps

1. **Immediate**: Execute Phase 0 research tasks (generate `research.md`)
2. **After Research**: Execute Phase 1 design tasks (generate `data-model.md`, `contracts/`, `quickstart.md`)
3. **After Design**: Run `/sp.tasks` to generate detailed task breakdown (`tasks.md`)
4. **After Tasks**: Run `/sp.implement` to execute implementation

---

## Risks and Mitigations (from Spec)

**Risk 1**: RAG responses may include inaccurate information if source content contains errors
- **Mitigation**: Rigorous technical review of all generated book content before ingestion (Phase 3 quality gate)

**Risk 2**: OpenAI API rate limits or service disruptions could impact chatbot availability
- **Mitigation**: Implement request queuing, caching for common queries, graceful degradation (documentation remains accessible)

**Risk 3**: Vector database costs may scale unpredictably with content volume and user queries
- **Mitigation**: Monitor usage metrics, implement query result caching, establish budget alerts (R3 research task addresses this)

**Risk 4**: Generated content may lack depth or technical accuracy required for professional audience
- **Mitigation**: Establish content quality rubrics, implement automated validation checks (FR-029), require expert review (SC-007: 90% pass rate)

**Risk 5**: Selected-text feature may not provide sufficient context for meaningful answers on isolated snippets
- **Mitigation**: Enforce minimum/maximum selection lengths (edge case handling: 20-2000 words), provide user guidance

---

## Architectural Decision Records (ADR Candidates)

Based on the planning process, the following decisions meet the three-part ADR significance test (Impact + Alternatives + Scope):

### ADR-001: Monorepo with Frontend/Backend Separation

**Impact**: Long-term consequences for deployment, scaling, and maintenance
**Alternatives**: Monolithic structure, separate repositories, microservices
**Scope**: Cross-cutting (affects all system components)

**Suggestion**: 📋 Architectural decision detected: Monorepo structure with frontend/backend separation for independent deployment and technology isolation. Document reasoning and tradeoffs? Run `/sp.adr monorepo-structure-decision`

---

### ADR-002: RAG-Only Response Strategy (No Generative Fallback)

**Impact**: Affects user experience when queries can't be answered from book content
**Alternatives**: Hybrid (RAG + generative), pure generative, fallback to external sources
**Scope**: Core feature design (chatbot behavior)

**Suggestion**: 📋 Architectural decision detected: Strict RAG enforcement with no hallucination fallback vs. hybrid approach allowing generative responses when book content insufficient. Document reasoning and tradeoffs? Run `/sp.adr rag-only-strategy`

---

### ADR-003: Static Site (GitHub Pages) vs. Server-Side Rendering

**Impact**: Performance, SEO, deployment complexity, hosting cost
**Alternatives**: Next.js (SSR), Gatsby (SSG), pure React SPA, Docusaurus (chosen)
**Scope**: Frontend architecture and deployment strategy

**Suggestion**: 📋 Architectural decision detected: Static site generation (Docusaurus) vs. server-side rendering for documentation. Document reasoning and tradeoffs? Run `/sp.adr static-vs-ssr-frontend`

---

**Note**: ADR creation requires user consent. Suggestions provided above for consideration during planning review.

---

**Planning Complete**: This plan is ready for Phase 0 research execution.
