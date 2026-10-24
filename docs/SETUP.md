# Installation and execution

Extract the complete project into a normal writable folder such as `C:\Projects\thooriga` or `~/projects/thooriga`. All commands below run from that folder. The package contains source code, tests, a bundled permitted sample photo, documentation, dependency locks, and scripts. Dependencies and model weights are installed separately; virtual environments and `node_modules` are machine-specific and are not part of the source package.

Use **Python 3.12**, **Node.js 22+ with npm**, and **Ollama**. The current code was exercised on Linux with Python 3.12.14 and Node 24.19.0. Native Windows and physical-phone execution have not been verified. Gemma vision inference has not been executed in this build environment.

## Windows 11 — recommended for the target laptop

Install Python 3.12 (including the `py` launcher), Node.js, and Ollama using their official installers. NVIDIA laptop drivers should be current. Restart the terminal after installation, then check:

```powershell
py -3.12 --version
node --version
npm.cmd --version
ollama --version
```

### 1. Install project dependencies once

```powershell
cd C:\Projects\thooriga
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup.ps1
```

`ExecutionPolicy Bypass` applies to that script process only; it does not change your persistent PowerShell policy. The script creates this project's `.venv` and runs the pinned Python install and `npm ci`. It does not download model weights.

Equivalent manual commands:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Push-Location frontend
npm.cmd ci
Pop-Location
```

### 2. Install and start the local model

```powershell
ollama pull gemma3:4b
ollama list
```

Ollama desktop normally starts its server automatically. If it is not running, open another terminal and keep this command running:

```powershell
ollama serve
```

A message that port 11434 is already in use often means Ollama is already serving. Check rather than starting a second server:

```powershell
Invoke-RestMethod http://127.0.0.1:11434/api/tags
```

### 3. Run backend — terminal A

```powershell
cd C:\Projects\thooriga
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-backend.ps1
```

Equivalent command:

```powershell
.\.venv\Scripts\python.exe -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log
```

### 4. Run frontend — terminal B

```powershell
cd C:\Projects\thooriga
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-frontend.ps1
```

Equivalent commands:

```powershell
cd frontend
npm.cmd run dev
```

Open [Thooriga](http://127.0.0.1:5173). Backend [health](http://127.0.0.1:8000/api/health) and [OpenAPI docs](http://127.0.0.1:8000/docs) are separate local endpoints. Keep all three processes available: Ollama, backend, frontend. Stop frontend/backend with Ctrl+C when finished.

## WSL / Linux alternative

Keep the project under the Linux home directory for better filesystem performance. Install Python 3.12, its `venv` support, Node.js 22+ and Ollama inside that same environment. Do not reuse a Windows-created `.venv` or `node_modules` in WSL, or a WSL-created environment from Windows.

```bash
cd ~/projects/thooriga
python3.12 --version
node --version
npm --version
bash scripts/setup.sh
ollama pull gemma3:4b
```

If Ollama is not already running as a service, start it in one terminal:

```bash
ollama serve
```

Run backend and frontend in two more terminals:

```bash
cd ~/projects/thooriga
bash scripts/start-backend.sh
```

```bash
cd ~/projects/thooriga
bash scripts/start-frontend.sh
```

Manual equivalents:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
(cd frontend && npm ci)
.venv/bin/python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000 --no-access-log
# Another terminal:
cd frontend
npm run dev
```

The inference adapter deliberately calls only `http://127.0.0.1:11434`. If you use WSL, run Ollama inside WSL too. Cross-environment Windows-to-WSL loopback behavior is not assumed. Do not expose Ollama or the application on `0.0.0.0`.

## First execution and model verification

1. Open the app and recheck local model status. `ollama list` must include exactly `gemma3:4b` unless you intentionally configured another tag.
2. Load the bundled public-domain NASA sample or 3–15 permitted photographs. The sample has no precomputed assessment.
3. Write a specific visual brief, choose the format and shortlist count, and start analysis.
4. Observe real progress. A 4B vision model may take minutes on a laptop; 6 GB VRAM does not guarantee full GPU offload. The default call timeout is 180 seconds per photo.
5. Confirm that explanations refer to actual image content. Inspect every recommendation and crop yourself.
6. Compare candidates, select favorites, reorder in Shortlist, then export. Inspect JPEG contents and archive ordering.
7. Clear the collection and stop the backend normally. Read [PRIVACY.md](../PRIVACY.md) for temporary-file and crash behavior.

A running UI or passing mocked tests does not establish real vision success. Record the checks in [NEXT_STEPS.md](NEXT_STEPS.md) before calling the AI pipeline verified.

## Tests and build

Windows, from the project root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
Push-Location frontend
npm.cmd test
npm.cmd run build
Pop-Location
```

WSL/Linux:

```bash
.venv/bin/python -m pytest -q
(cd frontend && npm test && npm run build)
```

`npm run build` performs TypeScript checking and writes static assets to `frontend/dist`. This project runs through the Vite development proxy locally; a build alone does not start the backend or make a standalone hosted site. See [RESULTS.md](RESULTS.md) for what has actually been executed.

## Optional configuration

`.env.example` is a reference and is **not loaded automatically**. Set variables in the backend terminal before starting it:

```powershell
$env:MAX_BATCH = '15'
$env:MAX_FILE_MB = '15'
$env:INFERENCE_TIMEOUT = '240'
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-backend.ps1
```

```bash
MAX_BATCH=15 MAX_FILE_MB=15 INFERENCE_TIMEOUT=240 bash scripts/start-backend.sh
```

Other settings include `OLLAMA_MODEL` and `DUP_THRESHOLD`. Keep the default small batch until you have measured memory use. Restart the backend after changing settings or replacing weights under the same model tag.

## Common issues

| Symptom | Check / action |
|---|---|
| Gemma offline | Run `ollama list`; verify `127.0.0.1:11434/api/tags`; pull `gemma3:4b`; recheck in the app. |
| Port already in use | Stop the earlier Thooriga server in its own terminal. Default API/frontend/Ollama ports are 8000/5173/11434. |
| `py -3.12` or `python3.12` missing | Install Python 3.12; Linux setup can use `THOORIGA_PYTHON=/path/to/python3.12 bash scripts/setup.sh`. |
| `.venv` belongs to another OS | Stop the app; remove only this project's `.venv`; rerun setup on the chosen OS. |
| Inference timeout | Reduce batch to 3 photos; check `ollama ps`, RAM/VRAM and other GPU applications; then increase `INFERENCE_TIMEOUT` if justified. |
| Invalid model output | Retry once with a clear brief; retain a redacted error report. Failed responses are not replaced with invented rankings. |
| Phone cannot open laptop localhost | Expected: the UI is responsive, but this MVP has no authenticated LAN access. `127.0.0.1` on a phone refers to the phone itself. |
| Dependencies fail to install | Confirm Python 3.12 and Node 22+, network access to package registries, and a writable project folder. Preserve lockfiles when reporting failures. |

## Updated logo, cancellation and verification

- `frontend/public/logo.png` and `frontend/public/favicon.png` now contain the user-supplied magenta/blue ring and black aperture (the PNG logo includes its original white background).
- Analysis has a **Cancel** button. Cancellation is cooperative: the currently executing local model request may finish before remaining photographs are skipped. Cancel does not alter original files.
- Adjustable `ASSESS_IMAGE_SIZE` controls the longest input side for vision requests, bounded to 256–896 pixels. Default 896. On a 6 GB GPU, try 640 only after measuring quality and latency, then rerun relevance tests.
- Active collections and cached assessments are bounded using `MAX_COLLECTIONS` (default 32) and `MAX_CACHE_ENTRIES` (default 250); these are local process limits, not persistent storage quotas.

One-command build/test checks after dependency installation:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\verify.ps1
```

```bash
bash scripts/verify.sh
```

Public **showcase-only** hosting instructions: [DEPLOYMENT.md](DEPLOYMENT.md). Do not publicly expose this localhost-only AI application.
