# Deployment Guide

Deploy the Physical AI & Humanoid Robotics Textbook to production in 3 simple steps.

## Prerequisites

- **GitHub account** (for frontend hosting)
- **Railway account** (for backend hosting) - [Sign up](https://railway.app/)
- **OpenAI API key** - [Get key](https://platform.openai.com/api-keys)
- **Qdrant Cloud account** - [Sign up](https://cloud.qdrant.io/)

---

## 1. Deploy Backend (Railway)

### Setup Railway Project

1. Go to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select: `Physical-AI-Humanoid-Robotics-Textbook`
4. Set **Root Directory**: `backend`

### Add Environment Variables

In Railway dashboard, add these variables:

```env
OPENAI_API_KEY=sk-proj-your-key-here
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
QDRANT_URL=https://your-cluster.qdrant.io:6333
QDRANT_API_KEY=your-qdrant-key
QDRANT_COLLECTION_NAME=textbook_chapters
ENVIRONMENT=production
DEBUG=False
ALLOWED_ORIGINS=https://yourusername.github.io
RATE_LIMIT_PER_MINUTE=60
PORT=8000
```

**Important**: Replace placeholders with your actual values.

### Deploy & Get URL

1. Click **"Deploy"** and wait (~2-5 minutes)
2. Go to **Settings** → **Networking** → **Generate Domain**
3. Copy your backend URL (e.g., `https://your-backend.up.railway.app`)

### Verify Backend

```bash
curl https://your-backend.up.railway.app/api/v1/health
# Expected: {"status":"healthy","components":{...}}
```

---

## 2. Deploy Frontend (GitHub Pages)

### Enable GitHub Pages

1. Go to your repository **Settings** → **Pages**
2. Under **"Build and deployment"**, set **Source**: `GitHub Actions`
3. Save

### Add Backend URL Secret (Optional)

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **"New repository secret"**
   - Name: `BACKEND_API_URL`
   - Value: Your Railway backend URL
3. Click **"Add secret"**

### Trigger Deployment

**Option A: Automatic** (recommended)
- Push any change to `frontend/` directory on `main` branch

**Option B: Manual**
1. Go to **Actions** tab
2. Click **"Deploy to GH Pages"** workflow
3. Click **"Run workflow"** → Select `main` → **"Run workflow"**

### Wait for Deployment

- Deployment takes ~2-3 minutes
- Monitor progress in **Actions** tab
- Once complete, your site will be live at:
  ```
  https://yourusername.github.io/Physical-AI-Humanoid-Robotics-Textbook/
  ```

---

## 3. Connect Frontend & Backend

### Update CORS on Railway

1. Go to Railway → Your backend service → **Variables**
2. Update `ALLOWED_ORIGINS` with your GitHub Pages URL:
   ```
   https://yourusername.github.io
   ```
   (Replace `yourusername` with your GitHub username)
3. Click **"Save"** (Railway auto-redeploys)

---

## Verification

### Check Deployment

- ✅ Backend health: `curl https://your-backend.up.railway.app/api/v1/health`
- ✅ Frontend loads: Visit `https://yourusername.github.io/Physical-AI-Humanoid-Robotics-Textbook/`
- ✅ ChatKit widget appears (bottom-right corner)
- ✅ Send test message: "What is ROS 2?"
- ✅ Verify response cites textbook content

### End-to-End Test

1. Visit your deployed site
2. Navigate to any chapter
3. Open ChatKit widget
4. Ask: "Explain Physical AI"
5. Verify response is relevant with citations

---

## Troubleshooting

### Backend Issues

**Build fails:**
- Check Railway logs: Service → **Deployments** → **View Logs**
- Verify all environment variables are set correctly

**Health check fails:**
```bash
curl https://your-backend.up.railway.app/api/v1/health
```
Check Railway logs for startup errors.

### Frontend Issues

**404 on GitHub Pages:**
- Go to **Settings** → **Pages** and verify source is `GitHub Actions`
- Check **Actions** tab for build errors

**CORS errors:**
- Update `ALLOWED_ORIGINS` in Railway to match your GitHub Pages URL
- Ensure no trailing slash: `https://yourusername.github.io` ✓
- Clear browser cache and retry

**ChatKit doesn't work:**
1. Open browser DevTools (F12) → Console
2. Check for errors
3. Verify backend URL is accessible
4. Test backend endpoint manually

---

## Update Deployment

### Update Backend
```bash
git add backend/
git commit -m "update backend"
git push
# Railway auto-deploys
```

### Update Frontend
```bash
git add frontend/
git commit -m "update content"
git push
# GitHub Actions auto-deploys
```

---

## URLs & Resources

**Your Deployment:**
- Frontend: `https://yourusername.github.io/Physical-AI-Humanoid-Robotics-Textbook/`
- Backend: `https://your-backend.up.railway.app`
- Backend API Docs: `https://your-backend.up.railway.app/docs`

**Dashboards:**
- Railway: https://railway.app/dashboard
- Qdrant Cloud: https://cloud.qdrant.io/
- OpenAI: https://platform.openai.com/usage

---

**🎉 Congratulations! Your textbook is now live!**

For issues, check the [GitHub repository](https://github.com/AsharibAli/Physical-AI-Humanoid-Robotics-Textbook) or open an issue.
