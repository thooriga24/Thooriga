# Thooriga: fastest path to GitHub and the DEV submission

**Use the finished source ZIP, not the separately delivered concept storyboard.** Do not upload personal photographs, API keys, `.venv`, `node_modules` or model weights.

## 1. Push the source to a **new** GitHub repository

Create a new empty repository on GitHub called `Thooriga`, without initializing a README. Then extract the provided GitHub-ready ZIP, open a terminal **inside the `Thooriga` folder**, and run:

```powershell
git init
git add .
git commit -m "Build Thooriga privacy-first Gemma photo curator"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Thooriga.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your account name. If your intended name or URL differs, edit the remote accordingly. No repository or link is claimed to exist yet.

## 2. Enable public showcase

GitHub → repository **Settings → Pages → Source: GitHub Actions**. Then GitHub → **Actions → Publish public project showcase** → Run workflow (if not automatically triggered). Its URL will be reported by GitHub after successful deployment.

**This is a public project explanation page, NOT a live photo-upload or Gemma inference website.** Don't represent it as such in the submission.

## 3. Optional 1-command project verification on Windows

Install Python 3.12, Node 22+, and Ollama first. Open Windows PowerShell in the extracted folder:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup.ps1
ollama pull gemma3:4b
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
.\.venv\Scripts\python.exe .\scripts\smoke_gemma.py
```

The final command performs **real** visual assessment of a permitted NASA sample. A successful code test or mocking test alone does not verify Gemma. If the model call fails, don't claim the app's actual AI output was verified.

## 4. Submit your Week 3 DEV post

- Use the *Week 3: Slow and Steady* official submission template (not the Week 2 Side Hustle entry).
- Adapt `docs/DEV_ARTICLE.md` as a draft; add the real repository, source/demo URLs, and evidence of working AI if available.
- Required tags: `#devchallenge`, `#hf26challenge`.
- Use the accurate demo language: "local-first photo curation app using Gemma through Ollama". If you have no live test, mention the limitation. Do not invent a hosted app, results, or screenshot.

**Deadline:** October 25, 2026 at 11:59 PM Pacific time (approximately October 26 at 12:29 PM India time).

## 5. Where everything is

| What | File |
|---|---|
| Core backend | `backend/app.py` |
| React app | `frontend/src/main.tsx` |
| Automated tests | `tests/test_backend.py`, `frontend/src/utils.test.ts` |
| Complete setup | `docs/SETUP.md` |
| Privacy policy | `PRIVACY.md` |
| Attribution and terms | `THIRD_PARTY_NOTICES.md` |
| Competition checklist | `docs/HACKTOBERFEST_SUBMISSION.md` |
| DEV post draft | `docs/DEV_ARTICLE.md` |
| Public GitHub Pages workflow | `.github/workflows/pages.yml` |
| Continuous integration checks | `.github/workflows/ci.yml` |
| Results/remaining limitations | `RELEASE_STATUS.md`, `docs/RESULTS.md` |
