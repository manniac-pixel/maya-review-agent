# Deployment Guide — Making the Agent Live

> Three live links for your Notion project: GitHub repo, Streamlit dashboard, and static report.

---

## What You'll Have When Done

| Link | What it shows | Platform |
|---|---|---|
| **GitHub Repo** | Source code, README, architecture | github.com |
| **Streamlit Dashboard** | Interactive findings explorer | streamlit.app (free) |
| **Static Report** | Read-only insights report + charts | GitHub Pages (free) |

---

## 1. GitHub Repo (5 minutes)

### Step 1: Create the repo

Go to [github.com/new](https://github.com/new) and create a new repository:

- **Name:** `maya-review-agent`
- **Description:** `AI-powered pipeline that scrapes 20,000+ fintech app reviews and turns them into ranked UX insights`
- **Visibility:** Public
- **Do NOT** initialize with README (we already have one)

### Step 2: Push your code

```bash
cd /Users/manpreetbhattee/Claude/Maya/maya-review-agent

# Initialize git (if not already)
git init

# Add everything
git add .

# Verify what's being committed (no .env, no .venv, no raw CSVs)
git status

# Commit
git commit -m "Initial commit: Maya Review Agent — AI-powered UX intelligence pipeline"

# Connect to GitHub
git remote add origin https://github.com/YOUR_USERNAME/maya-review-agent.git

# Push
git branch -M main
git push -u origin main
```

### Step 3: Verify

Visit your repo URL. You should see:
- Polished README with badges, pipeline diagram, usage docs
- All Python source files
- `Design 1/` folder with Notion docs
- `data/charts/` with the 9 visualization PNGs
- `data/` reports (insights report, brief, journey map)
- `streamlit_app.py`
- No `.env`, no `.venv`, no raw CSV data

### Your link
```
https://github.com/YOUR_USERNAME/maya-review-agent
```

---

## 2. Streamlit Dashboard (10 minutes)

### Step 1: Test locally first

```bash
pip install streamlit
streamlit run streamlit_app.py
```

This opens `http://localhost:8501` in your browser. Verify:
- Sidebar navigation works
- Charts display correctly
- All 7 pages render
- Dark Maya theme applied (green accent, navy background)

### Step 2: Deploy to Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Select:
   - **Repository:** `YOUR_USERNAME/maya-review-agent`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
5. Under **Advanced settings:**
   - **Python version:** 3.11
   - **Requirements file:** `requirements-streamlit.txt`
6. Click **"Deploy"**

Streamlit Cloud will:
- Clone your repo
- Install dependencies from `requirements-streamlit.txt`
- Launch the app
- Give you a public URL

### Step 3: Verify

The app should load with:
- Maya-themed dark UI (navy background, green accents)
- Dataset selector (All Reviews / 1-Star Only)
- 7 navigation pages
- All charts rendering from `data/charts/`

### Your link
```
https://YOUR_USERNAME-maya-review-agent.streamlit.app
```

### Troubleshooting

**Charts not showing?**
Make sure `data/charts/*.png` files are committed to git. Check that `.gitignore` doesn't exclude them.

**Data not loading?**
Make sure `data/final_insights.json` and `data/maya_insights_report.md` are committed.

**App crashes on load?**
Check the Streamlit Cloud logs. Most likely a missing file or import error.

---

## 3. Static Report Site — GitHub Pages (5 minutes)

### Option A: Quick — Use the README as the site

1. Go to your repo on GitHub
2. Click **Settings** > **Pages** (left sidebar)
3. Under **Source**, select:
   - **Branch:** `main`
   - **Folder:** `/ (root)`
4. Click **Save**
5. GitHub Pages will serve your `README.md` as a static site

### Your link
```
https://YOUR_USERNAME.github.io/maya-review-agent
```

### Option B: Better — Dedicated docs page

If you want the full insights report as a standalone page:

1. Create a `docs/` folder in your repo:

```bash
mkdir docs
cp data/maya_insights_report.md docs/index.md
cp -r data/charts docs/charts
```

2. Push to GitHub:

```bash
git add docs/
git commit -m "Add docs for GitHub Pages"
git push
```

3. In GitHub Settings > Pages, set:
   - **Branch:** `main`
   - **Folder:** `/docs`

4. The insights report is now live at:
```
https://YOUR_USERNAME.github.io/maya-review-agent
```

---

## 4. Add Links to Notion

Once all three are live, add them to your Notion master page:

### In the master page header

Add a **callout block** or **table** at the top:

| Resource | Link |
|---|---|
| Source Code | `https://github.com/YOUR_USERNAME/maya-review-agent` |
| Live Dashboard | `https://YOUR_USERNAME-maya-review-agent.streamlit.app` |
| Insights Report | `https://YOUR_USERNAME.github.io/maya-review-agent` |

### In Notion's page properties

If you're using a Notion database, add these as **URL properties:**
- `GitHub` → repo link
- `Live Demo` → Streamlit link
- `Report` → GitHub Pages link

---

## 5. Embedding in Notion

### Embed the Streamlit app directly

Notion supports embed blocks:

1. Type `/embed` in your Notion page
2. Paste your Streamlit URL: `https://YOUR_USERNAME-maya-review-agent.streamlit.app`
3. The dashboard will render inline in your Notion page

### Embed charts as images

For a cleaner look, you can also upload the chart PNGs directly:

1. Drag and drop `data/charts/priority_scores.png` into your Notion page
2. Repeat for other key charts
3. Add captions explaining each chart

---

## Checklist

- [ ] GitHub repo created and code pushed
- [ ] README displays correctly on GitHub
- [ ] `.env` is NOT in the repo (check!)
- [ ] Streamlit app tested locally
- [ ] Streamlit Cloud deployment successful
- [ ] GitHub Pages enabled
- [ ] All 3 links added to Notion master page
- [ ] Streamlit embed tested in Notion
- [ ] Shared with a friend to verify links work

---

## Quick Reference

| What | Command |
|---|---|
| Test Streamlit locally | `streamlit run streamlit_app.py` |
| Push updates | `git add . && git commit -m "update" && git push` |
| Streamlit redeploys | Automatic on push to main |
| GitHub Pages redeploys | Automatic on push to main |
