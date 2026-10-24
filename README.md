# Thooriga

A local photo curation workspace for small businesses and creators. Upload a small collection, write a specific brief, ask local Gemma vision to assess each photograph, then compare, select, reorder and export the final images yourself.

The dark workspace follows the requested Lark-inspired direction, with the supplied black camera-aperture artwork and magenta-to-blue ring. The interface has no event branding. The reference page returned HTTP 403; the exact composition was not inspected. See [design notes](docs/DESIGN.md). The source and documentation are bundled in the project folder; dependencies and model weights are installed separately.

For this continuation, see [release status](RELEASE_STATUS.md). The latest backend verification passed **29 tests**; full Windows/frontend/Gemma re-verification is still required.

## Start here

Read **[Installation and execution](docs/SETUP.md)** for complete Windows 11 PowerShell and WSL commands, prerequisites, manual equivalents, configuration and troubleshooting.

### Windows 11 quick start

Install Python 3.12 with its `py` launcher, Node.js 22+ and Ollama. From the extracted project folder:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup.ps1
ollama pull gemma3:4b
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-backend.ps1
```

Keep the backend running. In another terminal, from the same project folder:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-frontend.ps1
```

Ollama desktop usually serves automatically; otherwise run `ollama serve` in another terminal. Open [Thooriga](http://127.0.0.1:5173), [API health](http://127.0.0.1:8000/api/health), or [API docs](http://127.0.0.1:8000/docs).

### WSL / Linux quick start

Install Python 3.12, Node.js 22+ and Ollama **inside the same environment**:

```bash
bash scripts/setup.sh
ollama pull gemma3:4b
# Start Ollama if it is not already serving, in another terminal:
ollama serve
```

Start each application server in its own terminal:

```bash
bash scripts/start-backend.sh
```

```bash
bash scripts/start-frontend.sh
```

Do not share `.venv` or `node_modules` between Windows and WSL. Ollama is deliberately accessed only at `127.0.0.1:11434`. The scripts resolve their project directory, so they do not depend on the terminal's current directory after invocation.

## Implemented workflow

- JPEG/PNG/WebP validation, previews, removal, a configurable 15-photo batch limit and a permitted public-domain sample photo.
- A custom brief, six selection modes, output formats, and sequential Ollama/Gemma vision requests with validated Pydantic assessments.
- Real progress/error states, duplicate groups, technical indicators, explainable ranking and centered crop previews.
- Human comparison, selection/restoration, manual order and metadata-stripped ZIP export. Original source files remain unchanged.
- Local temporary processing, collection deletion and responsive phone/laptop layouts.

**Actual Gemma vision inference has not been run in this build environment.** Ollama and an NVIDIA runtime are absent. Integration success/error contracts are tested using clearly identified fixtures, and unavailable-model behavior is visible. No live relevance results, effort savings, target-laptop latency, or category qualification is claimed. Follow [the verification steps](docs/NEXT_STEPS.md) on the laptop before treating the AI workflow as verified.

## Tests

Windows:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
Push-Location frontend
npm.cmd test
npm.cmd run build
Pop-Location
```

Linux:

```bash
.venv/bin/python -m pytest -q
(cd frontend && npm test && npm run build)
```

The frontend build includes TypeScript checking. Browser integration requires Playwright/Chromium and both servers; see [actual test results](docs/RESULTS.md) and the script's environment requirements. PowerShell scripts have not been executed on native Windows in this environment.

## Folder guide

| Path | Contents |
|---|---|
| `backend/` | FastAPI, image processing, Ollama adapter, ranking and export |
| `frontend/` | React/TypeScript application, local assets and npm lockfile |
| `tests/` | Backend tests and browser workflow verification |
| `scripts/` | Windows/Linux setup and start scripts; benchmark evaluator |
| `docs/` | Setup, next steps, architecture, results, evaluation and demo material |
| `requirements.txt` | Pinned Python dependencies |
| `.env.example` | Configuration reference; not automatically loaded |
| `PRIVACY.md` | Data flow, retention, protections and verified limits |

## Local operation and limitations

Gemma 3 4B runs through Ollama with 896-pixel image inputs, sequential calls, a 4096-token context and a default 180-second timeout per photo. Exact image/brief/mode/format/model combinations are cached in memory. A changed brief requires a fresh conditional assessment. Full GPU fit in 6 GB VRAM is not assumed. OpenCLIP and Sentry are not included.

Crops are centered rather than subject-aware. Mood and suitability are subjective; scores are not beauty ratings. A responsive phone layout does not make the laptop reachable from a separate phone: this MVP binds to localhost and has no authenticated LAN deployment. Do not expose Vite, FastAPI or Ollama publicly.

Temporary copies are removed on collection deletion or normal backend shutdown; a crash can leave files behind. Browser close alone does not delete backend processing files. See [PRIVACY.md](PRIVACY.md).

## Public hosting and deployment

The included `site/` contains an optional static public showcase, and `.github/workflows/pages.yml` can publish it to GitHub Pages after you push the repository. **The actual photo-analysis application remains private and localhost-only; no public inference service is provided or claimed.** See [DEPLOYMENT.md](docs/DEPLOYMENT.md). No live URL has been verified.

## New October 24 release additions

- Near-duplicate ranking now retains the strongest image from each group, then fills the shortlist with alternatives; upload order no longer decides which near-duplicate is penalized.
- File digest values are no longer exposed in browser-facing photo metadata; HTTP API responses include no-store/nosniff headers.
- Historical job records are bounded and terminal records are pruned as needed, with regression coverage.
- Added `scripts/smoke_gemma.py` to run actual vision inference on the attributed NASA sample (an optional laptop-only check, not simulated scoring).
- Added `CONTRIBUTING.md`, `SECURITY.md`, `THIRD_PARTY_NOTICES.md`, release audit, Week 3 submission checklist and a separately delivered concept storyboard.

## Improvements in the earlier revision

- Replaced the previous aperture artwork with the exact image supplied in this conversation and generated a matching favicon.
- Removed the separate ImageHash runtime dependency by implementing OpenCV-based 64-bit perceptual hashing.
- Added bounded assessment caching and active-collection limits, an `ASSESS_IMAGE_SIZE` tuning option, and cooperative cancellation between photos.
- Reject repeated photo IDs in one export and clear private cached assessments after photo deletion.
- Added a deployment guide and one-command post-setup verification scripts.

## Documentation

- [Hacktoberfest submission checklist](docs/HACKTOBERFEST_SUBMISSION.md)
- [Open-source attribution and model license limits](THIRD_PARTY_NOTICES.md)
- [Contributing](CONTRIBUTING.md) and [security notes](SECURITY.md)

- [Complete setup and execution](docs/SETUP.md)
- [Deployment and hosted showcase](docs/DEPLOYMENT.md)
- [Next improvements and verification sequence](docs/NEXT_STEPS.md)
- [Architecture and API](docs/ARCHITECTURE.md)
- [Privacy and deletion](PRIVACY.md)
- [Benchmark methodology](docs/BENCHMARK.md)
- [Actual test results and limitations](docs/RESULTS.md)
- [Demo script](docs/DEMO.md)
- [Submission article draft](docs/DEV_ARTICLE.md)
- [Design and logo provenance](docs/DESIGN.md)
- [Sample photograph attribution](backend/samples/ATTRIBUTION.md)

Application source: MIT. Gemma weights have separate Google Gemma terms; review and accept those terms before use. Local open-weight execution and an inspectable source pipeline support reproducibility and community improvements, without implying unrestricted model licensing or perfect privacy.

## Packaging the complete source

Run `python scripts/package.py ../thooriga-delivery` to create a clean `Thooriga/` folder, ZIP, and SHA256 manifest outside the source tree. Choose a new destination if a delivery already exists. The package includes all source, lockfiles, scripts, assets, tests and documentation; virtual environments, node_modules, caches, secrets and model weights are excluded. Install dependencies using the included setup scripts.

## Single-port local production launch

For a streamlined private release, build the React frontend with `(cd frontend && npm run build)` and start `scripts/start-production.ps1` (Windows) or `scripts/start-production.sh` (Linux). The compiled UI and FastAPI API will both be served at `http://127.0.0.1:8000` while Gemma remains on local Ollama. This does **not** expose any private photographs to public hosting.
