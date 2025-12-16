<!--
Sync Impact Report - Constitution Update

Version Change: 1.1.0 → 2.0.0 (MAJOR)

BREAKING CHANGES:
  - Principle I: "Content Authenticity" → "Content Generation & Book Authorship"
    - Book-Content-Details.md redefined from "source of truth" to "reference guide"
    - Agent must now GENERATE full book content (not just follow reference)
    - Content destination changed to frontend/docs/ (mandatory path)

Modified Principles:
  - I. Content Generation & Book Authorship - Complete redefinition (BREAKING)
    - Old: Strict constraint to Book-Content-Details.md
    - New: Reference guide for agent-authored content
  - Documentation Structure - Updated to specify frontend/ subdirectory

Added Sections:
  - Repository Structure (MANDATORY) in Technical Standards
    - frontend/ directory (Docusaurus + book content)
    - backend/ directory (RAG API + vector pipeline)
    - Clean architectural separation

Removed Sections: None

Templates Status:
  ✅ plan-template.md - Aligned (Constitution Check references this file)
  ✅ spec-template.md - Aligned (Content generation now explicit requirement)
  ✅ tasks-template.md - Aligned (Structure principles apply to both frontend/backend)

Follow-up TODOs:
  - All existing specs must be reviewed for compliance with new repository structure
  - Content generation strategy must be defined in next feature spec
-->

# Physical AI & Humanoid Robotics Documentation Book Constitution

## Core Principles

### I. Content Generation & Book Authorship (NON-NEGOTIABLE)

You MUST generate the complete technical book content as professional Markdown files.

**Source Material**:
- `Book-Content-Details.md` is a **reference guide ONLY**
- Use it to understand scope, structure, topics, and learning objectives
- DO NOT copy it verbatim
- Expand, structure, and formalize content professionally

**Content Requirements**:
- All chapters MUST be written as Markdown files under `frontend/docs/`
- Content MUST read like a real published technical book
- MUST be technically accurate and professionally written
- MUST have no filler content or vague explanations
- Each chapter MUST teach concrete, actionable knowledge
- Use reference guide as blueprint, not constraint

**Rules**:
- Generate full book content yourself based on reference guide
- Professional technical writing standards apply
- When uncertain about technical depth, ask for clarification
- Document significant content decisions in ADRs

**Rationale**: The goal is a complete, publication-quality technical book. The reference guide provides structure and scope, but the agent must author the actual content with professional rigor and technical depth.

### II. Spec-Driven Development (NON-NEGOTIABLE)

All implementation MUST be driven by Spec-Kit Plus specifications before code is written.

**Rules**:
- MUST create spec.md before writing any code
- MUST create plan.md for architectural decisions
- MUST create tasks.md with verifiable acceptance criteria
- Each major subsystem (Docs, RAG API, Vector DB, UI embedding) MUST have its own spec
- Specifications MUST be clear, modular, and verifiable

**Rationale**: Documentation-first workflow ensures all stakeholders agree on requirements before implementation. Prevents rework and creates audit trail for decisions.

### III. Modular Coherence

The book is a single unified product, not a collection of disconnected pages.

**Rules**:
- Each module MUST have a clear purpose and learning objective
- MUST use consistent terminology throughout all chapters
- Each module MUST include:
  - Conceptual explanation
  - Architecture or workflow diagrams (textual descriptions acceptable)
  - Working code examples (where relevant)
  - Clear connection to previous and next modules
- Avoid duplicating explanations across modules; reference instead

**Rationale**: Technical readers need a coherent narrative to build mental models. Inconsistent terminology and disconnected topics create confusion and reduce learning effectiveness.

### IV. Quality Over Quantity

No filler content. Every chapter must teach something concrete.

**Rules**:
- MUST prefer explicit steps, diagrams, and code over verbose prose
- MUST NOT include vague explanations or hand-waving
- Code examples MUST be complete and runnable (not pseudocode)
- Optimize for correctness, clarity, and long-term maintainability
- If content does not directly support learning objectives, remove it

**Rationale**: Technical professionals value their time. Dense, actionable content is more valuable than padded word count. Concrete examples build confidence and understanding.

### V. RAG-First Documentation Architecture

The embedded chatbot is a core feature, not an afterthought.

**Rules**:
- All content MUST be structured for retrieval-augmented generation (RAG)
- Chatbot MUST answer questions based on full book context
- Chatbot MUST support user-selected text context
- Chatbot MUST clearly distinguish between book-wide and selection-specific answers
- MUST use Retrieval-Augmented Generation (no hallucinated answers)
- RAG infrastructure specs MUST be created before chatbot implementation

**Rationale**: The chatbot transforms static documentation into an interactive learning experience. RAG architecture ensures accurate answers grounded in actual book content.

### VI. Tech Stack Adherence (NON-NEGOTIABLE)

Use only the specified technology stack unless explicitly approved deviation is documented.

**Mandatory Stack**:
- **Documentation & Build**: Docusaurus, GitHub Pages deployment
- **Package Managers**:
  - Frontend: pnpm (exclusively, no npm or yarn)
  - Backend: uv (exclusively, no pip or poetry)
- **Specification & Authoring**: Spec-Kit Plus, Claude Code CLI
- **RAG Chatbot**:
  - OpenAI Agents / ChatKit SDKs
  - FastAPI backend
  - Neon Serverless Postgres (metadata & chat history)
  - Qdrant Cloud Free Tier (vector storage)

**Rules**:
- MUST use pnpm for all frontend package management operations
- MUST use uv for all backend Python package management operations
- MUST NOT use npm or yarn commands for frontend
- MUST NOT use pip or poetry commands for backend
- MUST NOT substitute alternative technologies without documented ADR
- If tech stack component is unclear or blocking, invoke user for clarification
- Document all dependency versions in specs

**Rationale**: Consistency in technology stack ensures reproducible builds and maintainable codebase. Prevents integration issues and technical debt from ad-hoc technology choices.

### VII. Progressive Disclosure & Layered Learning

Assume reader is a technical developer but not familiar with this specific stack.

**Rules**:
- MUST introduce concepts before using them
- Early chapters MUST NOT assume knowledge from later chapters
- Complex topics MUST be broken into digestible layers
- Each chapter MUST build on previous knowledge explicitly
- Include "Prerequisites" section at chapter start when needed
- Provide links to foundational concepts when referencing advanced topics

**Rationale**: Even experienced developers need scaffolding when learning new domains. Progressive disclosure prevents cognitive overload and reduces drop-off rates.

### VIII. Test-Driven Documentation

All code examples and instructions must be verifiable.

**Rules**:
- Code examples MUST be tested and working before inclusion
- Setup instructions MUST be validated on clean environment
- Include expected outputs for commands and code
- Document known issues and workarounds
- Create runnable example repositories when appropriate
- Keep example code in sync with documentation during updates

**Rationale**: Broken examples destroy trust and waste learner time. Verified documentation ensures readers can follow along successfully and builds confidence in the material.

### IX. UI Minimalism

Documentation interface must prioritize clarity and function over decoration.

**Rules**:
- MUST use clean, minimal Docusaurus theme configuration
- Avoid unnecessary UI embellishments, animations, or decorative elements
- Focus on content readability and navigation efficiency
- Use whitespace effectively for visual breathing room
- Color palette MUST serve function (syntax highlighting, semantic meaning) not aesthetics
- MUST NOT add UI features that do not directly support learning objectives
- Custom CSS/styling requires justification tied to user need

**Rationale**: Minimalist UI reduces cognitive load and keeps focus on educational content. Unnecessary decoration distracts from learning and increases maintenance burden. Clean interfaces age better and perform faster.

## Technical Standards

### Repository Structure (MANDATORY)

The repository MUST follow this structure:

```
frontend/
├── docs/               # All book Markdown content
├── src/               # Docusaurus React components
├── static/            # Static assets
├── docusaurus.config.js
└── package.json

backend/
├── api/               # FastAPI conversation endpoints
├── ingestion/         # Vector embedding pipeline
├── models/            # Data models
├── services/          # RAG service logic
└── requirements.txt
```

**Rules**:
- MUST separate frontend (Docusaurus) from backend (RAG API)
- All book content MUST live in `frontend/docs/`
- Backend MUST be independently deployable
- Each subsystem has its own dependency management
- No mixing of frontend and backend code

**Rationale**: Clean separation enables independent scaling, deployment, and maintenance. Frontend can be statically deployed to GitHub Pages while backend runs as a service. This architecture supports the RAG chatbot integration without coupling concerns.

### Documentation Structure

- Use Docusaurus standard folder structure within `frontend/`
- One `.md` or `.mdx` file per page/section
- Keep chapters modular and independently deployable
- Use frontmatter metadata consistently (title, description, keywords)

### Content Formatting

- Use GitHub-Flavored Markdown (GFM)
- Code blocks MUST specify language for syntax highlighting
- Use admonitions (tip, warning, info, danger) for callouts
- Include alt text for all images and diagrams
- Maximum line length: 100 characters for prose (soft limit)

### Package Management

**Frontend (Node.js/JavaScript/TypeScript)**:
- **Required Tool**: pnpm only
- Use `pnpm install` (not `npm install` or `yarn install`)
- Use `pnpm add` for adding dependencies
- Use `pnpm run` for scripts
- Commit `pnpm-lock.yaml` (not `package-lock.json` or `yarn.lock`)
- Include `.npmrc` if pnpm-specific configuration needed

**Backend (Python)**:
- **Required Tool**: uv only
- Use `uv add <package>` to add dependencies (not `pip install` or `poetry add`)
- Use `uv add --dev <package>` for development dependencies
- Use `uv run <command>` to run scripts in the virtual environment
- Use `uv sync` to synchronize dependencies from pyproject.toml
- Dependencies managed in `pyproject.toml` (no requirements.txt files needed)
- Lock file `uv.lock` is automatically generated and should be committed
- Virtual environment created automatically at `.venv/`

### Code Standards

- **Python**: Follow PEP 8, use type hints, document with docstrings
- **JavaScript/TypeScript**: Follow ESLint rules, use JSDoc comments
- **FastAPI**: Use Pydantic models for validation, include OpenAPI examples
- **Configuration**: Use `.env` files for secrets, document all environment variables

### RAG Architecture Requirements

- Vector embeddings MUST use consistent model (specify in spec)
- Chunk size for document splitting MUST be optimized for retrieval (document in plan)
- Metadata schema MUST include: chapter, section, topic tags
- Chat history MUST be user-scoped with privacy controls
- Retrieval MUST log relevance scores for debugging

## Development Workflow

### Phase 1: Specification
1. Read `Book-Content-Details.md` thoroughly
2. For each feature/component, run `/sp.specify` to create spec.md
3. Review spec with user before proceeding
4. Create PHR for specification stage

### Phase 2: Architecture Planning
1. Run `/sp.plan` to generate plan.md with architecture decisions
2. Document significant decisions with `/sp.adr` (requires user consent)
3. Create data models, contracts, and quickstart guides
4. Validate against constitution principles
5. Create PHR for planning stage

### Phase 3: Task Breakdown
1. Run `/sp.tasks` to generate tasks.md
2. Organize tasks by user story/module
3. Mark parallel-executable tasks with [P]
4. Include acceptance criteria for each task
5. Create PHR for task generation stage

### Phase 4: Implementation
1. Run `/sp.implement` to execute tasks in order
2. Follow test-first approach when tests are specified
3. Commit after each completed task or logical group
4. Create PHRs for implementation milestones (red, green, refactor stages)

### Phase 5: Validation & Deployment
1. Test documentation locally with `pnpm run start`
2. Validate RAG chatbot with sample queries
3. Build production bundle with `pnpm run build`
4. Deploy to GitHub Pages
5. Verify deployment and chatbot functionality
6. Create PHR for deployment stage

### Human-as-Tool Strategy

Invoke user clarification when:
- **Ambiguous Requirements**: User intent unclear → Ask 2-3 targeted questions
- **Unforeseen Dependencies**: Discovery not in spec → Surface and ask prioritization
- **Architectural Uncertainty**: Multiple valid approaches with tradeoffs → Present options
- **Completion Checkpoints**: After major milestones → Summarize and confirm next steps
- **ADR Triggers**: Significant architectural decision detected → Suggest documentation, wait for consent

## Governance

### Amendment Procedure

1. Propose changes via user input or discovered needs
2. Document rationale and impact analysis
3. Update `.specify/memory/constitution.md` with versioned changes
4. Propagate changes to affected templates (plan, spec, tasks)
5. Increment version following semantic versioning
6. Create sync impact report
7. Commit with message: `docs: amend constitution to vX.Y.Z (<brief-description>)`

### Versioning Policy

- **MAJOR** (X.0.0): Backward incompatible governance/principle removals or redefinitions
- **MINOR** (0.X.0): New principle/section added or materially expanded guidance
- **PATCH** (0.0.X): Clarifications, wording, typo fixes, non-semantic refinements

### Compliance Review

- All PRs MUST verify compliance with constitution principles
- Complexity violations MUST be justified in plan.md Complexity Tracking table
- Specs MUST pass Constitution Check before implementation begins
- Regular audits to ensure adherence (monthly or per milestone)

### Authority Hierarchy

1. **This Constitution** (process, principles, and repository structure)
2. **Book-Content-Details.md** (reference guide for content scope and structure)
3. **Feature Specs** (specific requirements)
4. **Implementation Plans** (technical decisions)
5. **Tasks** (execution details)

When conflicts arise, higher authority takes precedence. The Constitution now supersedes the reference guide to enable agent-authored content generation. Escalate unresolvable conflicts to user.

### Prompt History Records (PHR)

- MUST create PHR after every user prompt (except `/sp.phr` itself)
- Capture verbatim user input (no truncation)
- Route by stage:
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- Fill all template fields (no unresolved placeholders)

### Architecture Decision Records (ADR)

- Suggest ADR when decision is:
  - High impact (long-term consequences)
  - Multiple alternatives considered
  - Cross-cutting (affects system design)
- Format: "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- MUST wait for user consent; NEVER auto-create ADRs

---

**Version**: 2.0.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16
