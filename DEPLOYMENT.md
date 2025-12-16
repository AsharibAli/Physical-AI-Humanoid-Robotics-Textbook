# Deployment Guide

**Physical AI & Humanoid Robotics Interactive Textbook**

This guide walks you through deploying the frontend to GitHub Pages and the backend to Railway, and connecting them correctly in production.

---

## Table of Contents

1. [Deployment Architecture](#deployment-architecture)
2. [Prerequisites](#prerequisites)
3. [Phase 1: Prepare for Deployment](#phase-1-prepare-for-deployment)
4. [Phase 2: Backend Deployment (Railway)](#phase-2-backend-deployment-railway)
5. [Phase 3: Frontend Deployment (GitHub Pages)](#phase-3-frontend-deployment-github-pages)
6. [Phase 4: Connect Frontend and Backend](#phase-4-connect-frontend-and-backend)
7. [Phase 5: Verification](#phase-5-verification)
8. [Troubleshooting](#troubleshooting)

---

## Deployment Architecture

```
Production Environment
══════════════════════════════════════════════════════════════

┌────────────────────────────────────────────────────────────┐
│                    End Users (Global)                       │
└────────────────┬───────────────────────┬───────────────────┘
                 │                       │
                 │ Static Assets         │ API Requests
                 ▼                       ▼
    ┌────────────────────────┐  ┌──────────────────────────┐
    │   GitHub Pages          │  │   Railway (Container)    │
    │   (Static Hosting)      │  │   (Backend API)          │
    │                         │  │                          │
    │   - Docusaurus Build    │  │   - FastAPI Server       │
    │   - HTML/CSS/JS         │  │   - RAG Service          │
    │   - ChatKit Widget      │  │   - Docker Container     │
    │                         │  │                          │
    │   URL: username.github  │  │   URL: *.railway.app     │
    │        .io/repo-name/   │  │                          │
    └─────────────────────────┘  └──────────┬───────────────┘
                                            │
                                  ┌─────────┴──────────┐
                                  │                    │
                         ┌────────▼────────┐  ┌───────▼───────┐
                         │  OpenAI API     │  │  Qdrant Cloud │
                         │  - Embeddings   │  │  - Vector DB  │
                         │  - GPT-4        │  │  - Similarity │
                         └─────────────────┘  └───────────────┘
```

**Key Components**:
- **Frontend**: GitHub Pages (free, static hosting)
- **Backend**: Railway (containerized, auto-scaling)
- **Vector DB**: Qdrant Cloud (managed, free tier)
- **AI Services**: OpenAI API (pay-as-you-go)

---

## Prerequisites

Before starting deployment, ensure you have:

### 1. Accounts Created
- [ ] **GitHub account** (for GitHub Pages) - [Sign up](https://github.com/join)
- [ ] **Railway account** (for backend hosting) - [Sign up](https://railway.app/)
- [ ] **Qdrant Cloud account** (for vector database) - [Sign up](https://cloud.qdrant.io/)
- [ ] **OpenAI API account** (for embeddings/chat) - [Sign up](https://platform.openai.com/)

### 2. Local Development Working
- [ ] Backend runs locally (`http://localhost:8000`)
- [ ] Frontend runs locally (`http://localhost:3000`)
- [ ] ChatKit integration tested and working
- [ ] Qdrant collection populated with content

### 3. Git Repository
- [ ] Code pushed to GitHub repository
- [ ] Repository is public (for GitHub Pages free tier)
- [ ] All changes committed

### 4. API Keys Ready
- [ ] OpenAI API key (with credits)
- [ ] Qdrant Cloud URL and API key
- [ ] Keys stored securely (not in code)

---

## Phase 1: Prepare for Deployment

### Step 1: Create Production Environment Files

#### Backend Production Environment

Create `backend/.env.production` (DO NOT commit this file):

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-proj-your-actual-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# Qdrant Configuration
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-api-key-here
QDRANT_COLLECTION_NAME=textbook_chapters

# Application Configuration
ENVIRONMENT=production
DEBUG=False
ALLOWED_ORIGINS=https://yourusername.github.io
RATE_LIMIT_PER_MINUTE=60
PORT=8000
```

**IMPORTANT**: Replace placeholders with actual values:
- `yourusername` → Your GitHub username
- `your-actual-key-here` → Your OpenAI API key
- `your-cluster.qdrant.io` → Your Qdrant cluster URL
- `your-qdrant-api-key-here` → Your Qdrant API key

### Step 2: Create Backend Dockerfile

Create `backend/Dockerfile`:

```dockerfile
# Use official Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install uv package manager
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Expose port (Railway will inject $PORT)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:8000/api/v1/health', timeout=5)"

# Run the application
CMD ["uv", "run", "uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Step 3: Create Backend .dockerignore

Create `backend/.dockerignore`:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.*
*.env

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.mypy_cache/

# Logs
*.log

# Git
.git/
.gitignore

# Documentation
README.md
docs/
tests/
```

### Step 4: Test Backend Docker Build Locally

```bash
cd backend

# Build the Docker image
docker build -t physical-ai-backend .

# Test run (optional)
docker run -p 8000:8000 --env-file .env.production physical-ai-backend

# Test health endpoint
curl http://localhost:8000/api/v1/health
```

If successful, stop the container with `Ctrl+C`.

---

## Phase 2: Backend Deployment (Railway)

### Step 1: Create Railway Project

1. Go to https://railway.app/dashboard
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub account
5. Select your repository: `Physical-AI-Humanoid-Robotics-Textbook`

### Step 2: Configure Railway Deployment

1. Railway will auto-detect your Dockerfile
2. Set **Root Directory**: `backend`
3. Click **"Add variables"** to set environment variables

### Step 3: Add Environment Variables

Add the following environment variables in Railway dashboard:

| Variable Name | Value |
|--------------|-------|
| `OPENAI_API_KEY` | `sk-proj-your-actual-key` |
| `OPENAI_MODEL` | `gpt-4o-mini` |
| `OPENAI_EMBEDDING_MODEL` | `text-embedding-ada-002` |
| `QDRANT_URL` | `https://your-cluster.qdrant.io:6333` |
| `QDRANT_API_KEY` | `your-qdrant-api-key` |
| `QDRANT_COLLECTION_NAME` | `textbook_chapters` |
| `ENVIRONMENT` | `production` |
| `DEBUG` | `False` |
| `ALLOWED_ORIGINS` | `https://yourusername.github.io` |
| `RATE_LIMIT_PER_MINUTE` | `60` |
| `PORT` | `8000` |

**Note**: Replace placeholders with your actual values.

### Step 4: Deploy Backend

1. Click **"Deploy"**
2. Wait for deployment to complete (2-5 minutes)
3. Monitor deployment logs for errors

### Step 5: Generate Railway Domain

1. Once deployed, click **"Settings"** → **"Networking"**
2. Click **"Generate Domain"**
3. Copy your backend URL (e.g., `https://physical-ai-backend-production.up.railway.app`)

### Step 6: Verify Backend Deployment

Test your deployed backend:

```bash
# Replace with your actual Railway URL
export BACKEND_URL=https://physical-ai-backend-production.up.railway.app

# Health check
curl $BACKEND_URL/api/v1/health

# Expected: {"status":"healthy"}

# Test RAG query
curl -X POST $BACKEND_URL/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is ROS 2?", "top_k": 3}'
```

If both tests succeed, your backend is deployed correctly!

---

## Phase 3: Frontend Deployment (GitHub Pages)

### Step 1: Update Backend URL in Frontend

Edit `frontend/docusaurus.config.ts` and find the custom fields section:

```typescript
customFields: {
  backendApiUrl: process.env.BACKEND_API_URL || 'https://your-backend.railway.app',
},
```

Or create `frontend/.env.production`:

```env
BACKEND_API_URL=https://physical-ai-backend-production.up.railway.app
```

Replace with your actual Railway URL from Phase 2, Step 5.

### Step 2: Update ALLOWED_ORIGINS in Backend

Go back to Railway dashboard:

1. Click your backend service
2. Click **"Variables"**
3. Update `ALLOWED_ORIGINS` to:
   ```
   https://yourusername.github.io
   ```
   Replace `yourusername` with your actual GitHub username

4. Click **"Save"**
5. Railway will automatically redeploy

### Step 3: Build Frontend for Production

```bash
cd frontend

# Install dependencies (if not already done)
pnpm install

# Build for production
pnpm build
```

This creates an optimized production build in `frontend/build/`.

### Step 4: Configure GitHub Pages

#### Option A: Deploy via GitHub Actions (Recommended)

1. Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches:
      - main
    paths:
      - 'frontend/**'
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'

      - name: Setup pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build website
        env:
          BACKEND_API_URL: ${{ secrets.BACKEND_API_URL }}
        run: pnpm build

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: frontend/build

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

2. Add GitHub Secret:
   - Go to repository **Settings** → **Secrets and variables** → **Actions**
   - Click **"New repository secret"**
   - Name: `BACKEND_API_URL`
   - Value: `https://your-backend.railway.app`
   - Click **"Add secret"**

3. Enable GitHub Pages:
   - Go to repository **Settings** → **Pages**
   - Source: **GitHub Actions**
   - Save

4. Trigger Deployment:
   ```bash
   git add .github/workflows/deploy.yml
   git commit -m "feat: add GitHub Pages deployment workflow"
   git push origin main
   ```

5. Monitor deployment at **Actions** tab in GitHub

#### Option B: Manual Deployment

```bash
cd frontend

# Set Git user for deployment
export GIT_USER=yourusername

# Deploy
USE_SSH=false pnpm deploy
```

### Step 5: Verify Frontend Deployment

1. Visit your GitHub Pages URL:
   ```
   https://yourusername.github.io/Physical-AI-Humanoid-Robotics-Textbook/
   ```

2. Check that the site loads correctly

3. Open browser DevTools (F12) → Console

4. Look for any errors (should be none)

---

## Phase 4: Connect Frontend and Backend

### Step 1: Update CORS Configuration

Your backend's `ALLOWED_ORIGINS` should already include your GitHub Pages URL. Verify in Railway:

```
ALLOWED_ORIGINS=https://yourusername.github.io
```

### Step 2: Test ChatKit Integration

1. Open your deployed frontend
2. Click the **chat widget** (bottom-right corner)
3. Open browser DevTools → **Network** tab
4. Send a test message: "What is ROS 2?"
5. Verify:
   - Request to `/api/chatkit/session` succeeds
   - No CORS errors in console
   - Response is displayed in chat

### Step 3: Check for Errors

**Common Issues**:

- **CORS Error**: Update `ALLOWED_ORIGINS` in Railway
- **404 Not Found**: Check backend URL in frontend config
- **500 Server Error**: Check Railway logs for backend errors

---

## Phase 5: Verification

### Production Checklist

- [ ] Backend health endpoint responds: `GET https://your-backend.railway.app/api/v1/health`
- [ ] Frontend loads: `https://yourusername.github.io/repo-name/`
- [ ] Navigation works (all chapters accessible)
- [ ] ChatKit widget opens
- [ ] ChatKit can send messages
- [ ] RAG responses work (answers based on textbook)
- [ ] Source citations are displayed
- [ ] No CORS errors in browser console
- [ ] No 404 or 500 errors

### End-to-End Test

1. **Visit Frontend**:
   ```
   https://yourusername.github.io/Physical-AI-Humanoid-Robotics-Textbook/
   ```

2. **Navigate** to a chapter (e.g., Module 1 → Chapter 1)

3. **Open ChatKit** (chat icon, bottom-right)

4. **Ask Question**: "Explain ROS 2 nodes"

5. **Verify Response**:
   - Response is relevant to textbook content
   - Citations include chapter references
   - No generic/hallucinated information

6. **Test Text Selection** (if implemented):
   - Highlight text in chapter
   - Ask question about selection
   - Verify context-aware response

---

## Troubleshooting

### Backend Issues

#### Issue: Railway build fails

**Error**: `Dockerfile not found` or `Build failed`

**Solution**:
1. Verify `backend/Dockerfile` exists
2. Check Railway **Root Directory** is set to `backend`
3. Ensure `pyproject.toml` and `uv.lock` are committed

#### Issue: Backend starts but crashes

**Error**: `Application startup failed` in Railway logs

**Solution**:
1. Check Railway logs: Click service → **Deployments** → **View Logs**
2. Common causes:
   - Missing environment variables (check all are set)
   - Invalid `OPENAI_API_KEY` or `QDRANT_API_KEY`
   - Qdrant collection doesn't exist
3. Fix issues and redeploy

#### Issue: Health check fails

**Error**: `Health check timeout` or `503 Service Unavailable`

**Solution**:
```bash
# Check Railway logs for startup errors
# Ensure backend is fully started before health check runs

# Test health endpoint manually
curl https://your-backend.railway.app/api/v1/health
```

### Frontend Issues

#### Issue: GitHub Pages shows 404

**Error**: "404 - File not found" on GitHub Pages

**Solution**:
1. Verify GitHub Pages is enabled: **Settings** → **Pages**
2. Check build succeeded: **Actions** tab
3. Ensure `frontend/build/` directory was created locally
4. Verify `baseUrl` in `docusaurus.config.ts`:
   ```typescript
   baseUrl: '/Physical-AI-Humanoid-Robotics-Textbook/',
   ```

#### Issue: Frontend loads but no content

**Error**: Blank page or missing chapters

**Solution**:
1. Check browser console for errors
2. Verify build completed successfully
3. Check `frontend/docs/` has content
4. Rebuild and redeploy:
   ```bash
   pnpm build
   git add frontend/build
   git commit -m "fix: rebuild frontend"
   git push
   ```

### CORS Issues

#### Issue: CORS policy error

**Error**: `Access to fetch at 'https://backend.railway.app' has been blocked by CORS policy`

**Solution**:
1. Update `ALLOWED_ORIGINS` in Railway:
   ```
   https://yourusername.github.io
   ```
2. Ensure no trailing slash: ~~`https://yourusername.github.io/`~~
3. Redeploy backend (Railway auto-redeploys on variable change)
4. Clear browser cache and test again

### ChatKit Issues

#### Issue: ChatKit doesn't open

**Error**: Chat widget doesn't appear or doesn't respond to clicks

**Solution**:
1. Check browser console for JavaScript errors
2. Verify `@openai/chatkit-react` is installed:
   ```bash
   cd frontend
   pnpm list @openai/chatkit-react
   ```
3. Check `frontend/src/components/ChatBot/ChatKitWrapper.tsx` exists
4. Verify ChatKit component is imported in Docusaurus config

#### Issue: ChatKit opens but can't send messages

**Error**: Messages fail to send or timeout

**Solution**:
1. Check Network tab for failed requests
2. Verify backend URL is correct in frontend config
3. Test backend `/api/chatkit/session` endpoint:
   ```bash
   curl -X POST https://your-backend.railway.app/api/chatkit/session
   ```
4. Check Railway logs for backend errors

### RAG Issues

#### Issue: Responses are empty or generic

**Error**: ChatKit responds but doesn't cite textbook sources

**Solution**:
1. Verify Qdrant collection has data:
   - Log into Qdrant Cloud dashboard
   - Check collection `textbook_chapters` exists
   - Verify collection has vectors (should show count)
2. If empty, run ingestion script:
   ```bash
   cd backend
   uv run python scripts/ingest_content.py
   ```
3. Check OpenAI API key has credits
4. Review backend logs for RAG service errors

---

## Monitoring & Maintenance

### Set Up Uptime Monitoring

Use a free service like [UptimeRobot](https://uptimerobot.com/) to monitor your backend:

1. Sign up for free account
2. Add monitor:
   - Type: **HTTP(s)**
   - URL: `https://your-backend.railway.app/api/v1/health`
   - Interval: **5 minutes**
3. Set up email alerts

### Monitor Costs

**Railway**:
- Free tier: $5 credit/month
- Monitor usage: Railway dashboard → **Usage**
- Estimate: ~$1-3/month for low traffic

**Qdrant Cloud**:
- Free tier: 1GB storage
- Monitor: Qdrant dashboard → **Cluster metrics**

**OpenAI API**:
- Pay per token
- Monitor: OpenAI dashboard → **Usage**
- Set spending limits: **Settings** → **Billing** → **Usage limits**

### Update Deployment

**Backend Updates**:
```bash
# Make changes to backend code
git add backend/
git commit -m "feat: update backend feature"
git push

# Railway auto-deploys on push to main
```

**Frontend Updates**:
```bash
# Make changes to frontend code
git add frontend/
git commit -m "feat: update frontend content"
git push

# GitHub Actions auto-deploys on push to main
```

---

## Summary

**Deployment Flow**:

1. ✅ **Prepare**: Create Dockerfile, `.env.production`, test locally
2. ✅ **Deploy Backend**: Railway → Set env vars → Generate domain
3. ✅ **Deploy Frontend**: GitHub Pages → Configure actions → Deploy
4. ✅ **Connect**: Update CORS, test ChatKit integration
5. ✅ **Verify**: End-to-end testing, monitoring setup

**URLs**:
- **Frontend**: `https://yourusername.github.io/repository-name/`
- **Backend**: `https://your-backend.railway.app`
- **Qdrant**: `https://your-cluster.qdrant.io:6333`

**Next Steps**:
- Set up custom domain (optional)
- Configure CI/CD for automated testing
- Add analytics (Google Analytics, Plausible)
- Set up error tracking (Sentry)

---

**Congratulations!** Your Physical AI & Humanoid Robotics textbook is now live! 🎉

**Share your deployment**:
- Tweet your deployed site
- Share in learning communities
- Gather feedback from users
- Iterate and improve

For questions or issues, open an issue on GitHub or consult the documentation.
