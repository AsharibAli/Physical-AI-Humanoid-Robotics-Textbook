# Physical AI & Humanoid Robotics Interactive Textbook

An interactive technical textbook platform combining comprehensive documentation (Docusaurus) with an AI-powered chatbot (RAG-based Q&A) for learning Physical AI and Humanoid Robotics.

## Overview

This platform provides:
- **Comprehensive Documentation**: 12 modules covering ROS 2, simulation (Gazebo/Unity), NVIDIA Isaac, and Vision-Language-Action (VLA) systems
- **AI-Powered Q&A**: RAG-based chatbot answers questions with strict adherence to book content (no hallucinations)
- **Interactive Learning**: Text selection mode for targeted questions about specific passages
- **Clean, Minimalist UI**: Optimized for technical reading with low visual noise

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Browser                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────┐         ┌────────────────────────┐   │
│  │  Docusaurus Site    │◄────────│  ChatKit Widget        │   │
│  │  (Static Content)   │         │  (@openai/chatkit)     │   │
│  │  - Book Chapters    │         │                        │   │
│  │  - Navigation       │         └────────┬───────────────┘   │
│  │  - Search           │                  │                    │
│  └─────────────────────┘                  │ API Calls          │
│                                           │                    │
└───────────────────────────────────────────┼────────────────────┘
                                            │
                                            ▼
                          ┌─────────────────────────────────┐
                          │   Backend API (FastAPI)          │
                          │   - Session Management           │
                          │   - Tool Handlers                │
                          └──────────┬─────────────┬─────────┘
                                     │             │
                    ┌────────────────┘             └──────────────┐
                    ▼                                             ▼
          ┌──────────────────┐                        ┌──────────────────┐
          │  OpenAI API      │                        │  Qdrant Cloud    │
          │  - Embeddings    │                        │  - Vector Search │
          │  - Chat (GPT-4)  │                        │  - Similarity    │
          └──────────────────┘                        └──────────────────┘
```

### Frontend
- **Framework**: Docusaurus 3.1.1 (React-based static site generator)
- **Package Manager**: pnpm 8.x (mandatory - no npm/yarn)
- **Runtime**: Node.js 18+
- **Chat UI**: @openai/chatkit-react 1.4.0
- **Language**: TypeScript 5.3.3
- **Deployment**: GitHub Pages (static hosting)
- **Location**: `frontend/`

### Backend
- **Framework**: FastAPI 0.109.0+ (Python ASGI web framework)
- **Package Manager**: uv (mandatory - no pip/poetry)
- **Runtime**: Python 3.11+
- **Vector Store**: Qdrant Cloud (free tier)
- **Embeddings**: OpenAI text-embedding-ada-002
- **Chat Model**: OpenAI gpt-4o-mini
- **Deployment**: Containerized (Railway/Render/Fly.io)
- **Location**: `backend/`

### Data Flow
1. **User asks question** → ChatKit widget captures input
2. **ChatKit calls** → Backend `/api/chatkit/session` endpoint
3. **Backend invokes** → `search_textbook` tool with query
4. **RAG Service**:
   - Generates embedding via OpenAI API
   - Searches Qdrant vector database for relevant chunks
   - Retrieves top-k similar textbook sections
5. **Response Generation** → GPT-4 synthesizes answer from retrieved context
6. **ChatKit displays** → Answer with source citations to user

### Content Structure
- **Book Structure**: 12 modules × 3-5 chapters = ~40-60 Markdown files
- **Total Length**: ~150,000-200,000 words
- **Format**: Four required sections per chapter: Concepts, Architectures, Algorithms, Real-World Considerations
- **Storage**: All content in `frontend/docs/` as Markdown files

## Quick Start

### Prerequisites

- **Node.js**: 18+ LTS
- **Python**: 3.11+
- **pnpm**: 8.x (`npm install -g pnpm`)
- **uv**: Latest version ([installation guide](https://github.com/astral-sh/uv#installation))
  ```bash
  # Install uv
  curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/macOS
  # Windows: irm https://astral.sh/uv/install.ps1 | iex
  ```
- **Qdrant Cloud**: Free tier account (https://cloud.qdrant.io)
- **OpenAI API**: API key (https://platform.openai.com/api-keys)

---

### Part 1: Backend Setup (Start This First)

#### Step 1: Navigate to Backend Directory

```bash
cd backend
```

#### Step 2: Create Environment File

```bash
# Copy the example file
cp .env.example .env
```

#### Step 3: Configure Environment Variables

Open `.env` and add the following:

```env
# OpenAI Configuration (REQUIRED)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Qdrant Configuration (REQUIRED)
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
QDRANT_COLLECTION_NAME=textbook_chapters

# Server Configuration
ENVIRONMENT=development
DEBUG=True
ALLOWED_ORIGINS=http://localhost:3000
RATE_LIMIT_PER_MINUTE=60
```

**How to get these values:**

1. **OPENAI_API_KEY**:
   - Go to https://platform.openai.com/api-keys
   - Create a new API key
   - Copy the key (starts with `sk-proj-` or `sk-`)

2. **QDRANT_URL** and **QDRANT_API_KEY**:
   - **Option A (Cloud - Recommended)**:
     - Go to https://cloud.qdrant.io
     - Create a free cluster
     - Copy the cluster URL and API key from the dashboard
   - **Option B (Local Docker)**:
     ```bash
     docker run -p 6333:6333 qdrant/qdrant
     # Use: QDRANT_URL=http://localhost:6333
     # No API key needed for local
     ```

#### Step 4: Install Dependencies

```bash
uv sync
```

This installs all Python dependencies including FastAPI, OpenAI SDK, Qdrant Client, and more.

#### Step 5: Start Backend Server

```bash
uv run python -m backend.api.main
```

**Expected output:**
```
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

#### Step 6: Verify Backend is Running

Open a new terminal and test:

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Expected response:
# {"status":"healthy"}
```

**Backend API Endpoints**:
- `GET /api/v1/health` - Health check
- `POST /api/v1/query` - RAG query endpoint
- `POST /api/chatkit/session` - Create ChatKit session
- `POST /api/chatkit/refresh` - Refresh ChatKit session

---

### Part 2: Frontend Setup

#### Step 1: Navigate to Frontend Directory

```bash
cd frontend
```

#### Step 2: Install Dependencies

```bash
pnpm install
```

#### Step 3: Start Frontend Development Server

```bash
pnpm start
```

**Expected output:**
```
[SUCCESS] Docusaurus website is running at: http://localhost:3000/Physical-AI-Humanoid-Robotics-Textbook/
```

#### Step 4: Open in Browser

Navigate to: **http://localhost:3000/Physical-AI-Humanoid-Robotics-Textbook/**

---

### Part 3: Verify Integration

#### Test 1: Backend Health Check

```bash
curl http://localhost:8000/api/v1/health
```

**Expected**: `{"status":"healthy"}`

#### Test 2: Create ChatKit Session

```bash
curl -X POST http://localhost:8000/api/chatkit/session
```

**Expected**:
```json
{
  "client_secret": "sk_session_...",
  "session_id": "session_...",
  "expires_at": 1734567890
}
```

#### Test 3: End-to-End Chat Test

1. Open http://localhost:3000/Physical-AI-Humanoid-Robotics-Textbook/
2. Click the **chat widget** (bottom-right corner)
3. Type a question: "What is ROS 2?"
4. Verify:
   - ChatKit opens and initializes
   - Response is displayed
   - Citations are included

---

### Configuration Checklist

**Backend (.env file)**:
- [ ] `OPENAI_API_KEY` set with valid OpenAI API key
- [ ] `QDRANT_URL` set with Qdrant cluster URL
- [ ] `QDRANT_API_KEY` set (if using Qdrant Cloud)
- [ ] Backend server running on http://localhost:8000

**Frontend**:
- [ ] Dependencies installed (`pnpm install`)
- [ ] Dev server running on http://localhost:3000

**ChatKit Integration**:
- [ ] Session creation endpoint working
- [ ] RAG service connected
- [ ] Qdrant vector database accessible

---

### Common Issues

**Issue: "OpenAI API key not found"**

**Solution**: Ensure `.env` file exists in `backend/` directory with `OPENAI_API_KEY=sk-...`

**Issue: "Cannot connect to Qdrant"**

**Solution**:
- Check `QDRANT_URL` is correct
- Verify Qdrant cluster is running
- Check `QDRANT_API_KEY` if using cloud

**Issue: ChatKit won't open**

**Solution**:
- Check browser console for errors
- Verify backend session endpoint returns valid response
- Ensure both backend and frontend servers are running

---

### Development URLs

- **Backend**: http://localhost:8000
- **Frontend**: http://localhost:3000/Physical-AI-Humanoid-Robotics-Textbook/
- **API Docs**: http://localhost:8000/docs (FastAPI auto-generated)

---

### Next Steps

Once local development is working:
- **Deploy**: See [DEPLOYMENT.md](./DEPLOYMENT.md) for production deployment guide
- **Customize**: Modify ChatKit configuration in `backend/api/routes/chatkit.py`
- **Content**: Add or update textbook content in `frontend/docs/`

## Project Structure

```
Physical-AI-Humanoid-Robotics-Textbook/
├── frontend/
│   ├── docs/                    # Book Markdown content (40-60 chapters)
│   ├── src/
│   │   ├── components/ChatBot/  # Chat UI components
│   │   ├── theme/               # Docusaurus theme customization
│   │   └── css/custom.css       # Minimalist styling
│   ├── docusaurus.config.js
│   ├── sidebars.js
│   └── package.json
│
├── backend/
│   ├── api/                     # FastAPI application
│   ├── ingestion/               # Embedding pipeline
│   ├── services/                # RAG service logic
│   ├── models/                  # Pydantic models
│   ├── config/                  # Configuration
│   ├── scripts/                 # CLI utilities
│   └── requirements.txt
│
├── .specify/                    # Spec-Kit Plus framework
├── specs/                       # Feature specifications
├── history/                     # Prompt history records
└── README.md
```

## Development Workflow

1. **Specification**: Feature specs in `specs/001-system-architecture/spec.md`
2. **Planning**: Implementation plan in `specs/001-system-architecture/plan.md`
3. **Tasks**: Task breakdown in `specs/001-system-architecture/tasks.md`
4. **Implementation**: Follow task order (Setup → Foundation → Content → Backend → Frontend → Integration → Deployment)

## Key Features

- **RAG-Only Responses**: Strict enforcement - all answers traceable to book sections
- **Source Citations**: Every response includes chapter/section references
- **Text Selection Mode**: Highlight passages for focused questions
- **Minimalist Design**: Clean typography, optimized readability
- **Performance**: <3s response time, handles 100 concurrent users
- **Quality**: 90% content accuracy, zero hallucinations

## Technology Stack

### Mandated Stack (Constitutional Requirements)

**Frontend**:
- Docusaurus 3.1.1 (React-based static site generator)
- pnpm 8.x (package manager - no npm/yarn allowed)
- TypeScript 5.3.3
- @openai/chatkit-react 1.4.0 (chat interface)
- Node.js 18+

**Backend**:
- FastAPI 0.109.0+ (Python ASGI framework)
- uv (package manager - no pip/poetry allowed)
- Python 3.11+
- Qdrant Cloud (vector database)
- OpenAI API (embeddings + chat)
- Pydantic 2.6.0+ (data validation)
- Uvicorn (ASGI server)

**Infrastructure**:
- GitHub Pages (frontend static hosting)
- Railway/Render/Fly.io (backend containerized deployment)
- Qdrant Cloud Free Tier (managed vector database)

**Development**:
- Spec-Kit Plus (specification framework)
- Claude Code CLI (AI-assisted development)

### Success Criteria
- **SC-001**: Navigation <10 seconds to any chapter
- **SC-002**: Chatbot response <3 seconds for 95% of queries
- **SC-003**: 90% RAG accuracy on ground truth questions
- **SC-004**: Zero hallucinations detected (RAG-only responses)
- **SC-005**: 100 concurrent users without degradation
- **SC-009**: 99.5% uptime

## Documentation

- **Specification**: `specs/001-system-architecture/spec.md`
- **Implementation Plan**: `specs/001-system-architecture/plan.md`
- **Task Breakdown**: `specs/001-system-architecture/tasks.md`
- **Constitution**: `.specify/memory/constitution.md`

## Contributing

This project follows Spec-Driven Development (SDD) via Spec-Kit Plus:
1. All features start with a specification (`/sp.specify`)
2. Architecture planning precedes implementation (`/sp.plan`)
3. Tasks are generated from specs (`/sp.tasks`)
4. Implementation follows task order (`/sp.implement`)
