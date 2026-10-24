# Deployment: public showcase + private local AI application

**Status of this delivery:** release assets and GitHub Pages workflow are prepared, but no account-backed hosting has been deployed or verified in this environment. No public application URL is claimed. The original application is **localhost-only** by design.

## Why two surfaces?

The full application accepts private photographs and talks to Ollama on `127.0.0.1:11434`. Deploying this backend unmodified to public hosting would break the localhost model connection and expose an unauthenticated, in-memory photo service. **Do not expose the current Vite development server, FastAPI app, or Ollama to the Internet.**

The `site/` folder is a truthful, no-upload public showcase: it explains and links to the local software, but does not pretend that Gemma inference runs on the hosted page.

## Publish the showcase on GitHub Pages (no compute hosting cost)

1. Create a **new** GitHub repository for this source if one does not already exist. Ensure you have the rights to redistribute the user-provided logo and bundled sample assets. Do not publish private photos, credentials, `.venv`, or model weights.
2. From the extracted `Thooriga` folder, authenticate Git with your account and push to the new repository's `main` branch:

   ```bash
   git init
   git add .
   git commit -m "Release Thooriga local photo curator"
   git branch -M main
   git remote add origin https://github.com/REPLACE_OWNER/REPLACE_REPO.git
   git push -u origin main
   ```

3. In the GitHub repository, open **Settings → Pages → Build and deployment → Source: GitHub Actions**.
4. Open **Actions** and run **Publish public project showcase** if the push did not automatically deploy it.
5. After Actions succeeds, open the reported `github-pages` environment URL and check the logo, mobile layout, navigation, and source link.
6. Do not publish the `.tech` category claim unless an eligible claimed domain has actually been connected and verified.

This workflow publishes `site/`, not the private AI application. The source remains downloadable through the repository.

## Local private deployment

Run the Windows or WSL steps in [SETUP.md](SETUP.md). On Windows, run `scripts/verify.ps1` after installing the dependencies and model. For Linux/WSL run `bash scripts/verify.sh`.

- UI: `http://127.0.0.1:5173`
- API: `http://127.0.0.1:8000/api/health`
- Ollama: `http://127.0.0.1:11434`

Only the local host can access the app. The browser UI is phone-responsive, but the phone cannot access the desktop's localhost remotely.

## If public hosted AI becomes a requirement later

That is a separate architecture and security project: a GPU-capable host for actual Gemma vision inference, HTTPS, authentication and tenant isolation, strict upload limits, safe file lifecycle, private data consent, anti-abuse limits, monitoring and billing, and published retention policies. It should not be done by forwarding port 11434 or by binding the existing app to `0.0.0.0`.

## Submission checklist

- [ ] GitHub repository exists with correct files and code license.
- [ ] User-provided logo's redistribution rights verified.
- [ ] GitHub Pages deployment action successful and URL manually tested.
- [ ] Real Gemma vision inference succeeds on the target laptop.
- [ ] Tests pass on the target laptop.
- [ ] Demo video includes real inference and human final selection.
- [ ] Measured results replace placeholders in DEV article.
- [ ] No invented host URLs or prize-category qualifications.

## Single-port production deployment on your laptop (actual app)

This option serves the **built React UI and the FastAPI API from the same local host and port**, instead of starting the Vite development server. Ollama remains a separate local inference process.

**Windows PowerShell**, after running setup and installing Gemma:

```powershell
Push-Location frontend
npm.cmd run build
Pop-Location
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-production.ps1
```

**Linux/WSL**:

```bash
(cd frontend && npm run build)
bash scripts/start-production.sh
```

Open `http://127.0.0.1:8000` and run the real app. The backend serves `frontend/dist` only when the production build already exists at process startup. Rebuild UI changes and restart the backend to update the production assets. This is a private local deployment and cannot be reached from unrelated phones or public Internet clients.
