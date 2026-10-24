# Latest recovered release verification — October 24, 2026

| Check | Result in this continuation |
|---|---|
| Python backend tests | **29 passed** (Python 3.13.5, installed library versions in the container) |
| Python compileall | Passed |
| Release source/branding audit | Passed; application and showcase logo/favicon match |
| Previous Work snapshot backend tests | 24 passed in the earlier release; this supersedes that test count |
| Previous Work snapshot Vitest/build/browser | Results below are prior recorded checks, **not rerun here** |
| `npm ci` in this continuation | Could not complete: package registry access stalled, offline cache incomplete |
| Full fresh frontend Vitest/TypeScript/Vite build | **Not verified in this continuation**; new 8 regression tests added but unexecuted |
| Real `gemma3:4b` inference | **Not verified**; local Ollama model/runtime unavailable here |
| Human benchmark, privacy egress audit | **Not verified** |
| GitHub repo created and public Pages deployment | **Not done; account-side action required** |

Tests use fixture responses for Ollama API contracts. They are not evidence of successful live visual analysis. See `scripts/smoke_gemma.py` for a real-model smoke test that can be run on the target laptop.

---

## Historical Work-session test record (retained verbatim below)

# Executed checks and remaining verification

Latest redesign verification: 24 October 2026 (Asia/Kolkata). Host: Linux, Python 3.12.14, Node 24.19.0. No Ollama model or NVIDIA runtime is available in this environment.

| Check | Actual outcome |
|---|---|
| Backend pytest | 20 passed, 0 failed, 0 skipped; 1.30 seconds |
| Frontend Vitest utilities | 9 passed, 0 failed, 0 skipped; 6 ms test execution |
| TypeScript + Vite production build | Passed; Vite build 2.15 seconds |
| Dependency consistency | `pip check` passed on the installed environment |
| Server startup | Local FastAPI and Vite started successfully |
| Browser workflow | All 14 checks passed using real local API requests |
| Responsive viewports | 320×780, 390×844 and 768×1024: no horizontal overflow, privacy navigation works |
| Browser errors | No JavaScript page errors |
| Observed browser network | All 29 observed requests used the local app origin |
| PowerShell execution | Unverified: native Windows/PowerShell unavailable |
| Bash launcher scripts | Syntax checks passed; setup is provided for Python 3.12 |
| Real Gemma vision | Not run: Ollama/model absent |
| Relevance / effort / GPU performance | Not measured |
| Actual offline inference / packet audit | Not verified |

Backend tests exercise valid/invalid uploads, unsupported decoded formats, batch/byte limits, empty collections, whitespace briefs, resized/recompressed/slightly brightness-modified duplicate copies, ranking calculations, malformed model JSON, missing Ollama/timeouts, crop geometry, generated export names, path-ID rejection, metadata removal, origin/Host guards, collection deletion and public-domain sample decoding. Inference success is contract-tested with explicitly marked test fixtures, never shown as live results to application users.

Frontend utility tests cover upload validation, useful briefs, selection/restoration, deselection and immutable ordering. The production build performs strict TypeScript checking. A React Testing Library suite and separate ESLint configuration are not included.

## Browser evidence

`tests/browser_check.py` uses real uploads and the public-domain NASA sample; no AI responses are mocked. It verifies:

- Photo preview and decoded sample dimensions.
- Mode, output format and shortlist-size controls.
- Duplicate filter, search and upload/fit sorting.
- Side-by-side comparison.
- Selection, deselection, restoration and manual shortlist ordering.
- Downloaded ZIP content and order.
- Empty-brief validation and actual missing-model error display.
- Individual removal, collection clearing and sample reload.
- Responsive layout and privacy navigation at three narrow viewports.
- No JavaScript page errors or browser requests outside the local app origin.

Machine-readable details: `docs/browser-check-results.json`. Actual captures: `docs/desktop.png`, `docs/mobile.png`, `docs/library.png`. The library capture contains permitted sample photos without fabricated assessments. Browser observations are not an OS-level network audit and do not verify actual model execution.

The Dribbble reference returned HTTP 403. The implemented dark workspace direction is documented in `docs/DESIGN.md`; exact visual matching was not verified.

## Remaining acceptance checks

Follow `docs/NEXT_STEPS.md` in order:

1. Run actual Gemma 3 4B on permitted real photos on the target laptop.
2. Record model/runtime details, accurate visual interpretation, latency, memory and failures.
3. Complete human relevance judgments and baseline/Gemma evaluation.
4. Measure manual/assisted effort and duplicate precision/recall.
5. Verify disconnected inference and process-level network behavior.
6. Test native Windows setup, physical devices and accessibility.
7. Record the live demo and publish a real repository URL before submission.

No category qualification or effort-reduction claim is made. OpenCLIP, Sentry, subject-aware cropping, job cancellation, persistent collections, idle expiry, and authenticated remote/phone access remain unimplemented. Exact assessment cache hits avoid repeat calls; a changed brief still triggers fresh conditional vision assessment. Duplicate diversity penalties remain a simple upload-order heuristic.

---

## Current continuation: 24 October 2026 — uploaded-source recovery and release hardening

This section supersedes the earlier 20-test counts **for this revision only**. The earlier browser and frontend results remain historical evidence from the supplied archive; they were **not reproduced here**.

### Checks executed on this build environment

| Check | Result |
|---|---|
| Backend unit/integration-contract tests | **24 passed**, 0 failed (Python 3.13 environment with available FastAPI/Pillow/OpenCV dependencies; 0.65 seconds) |
| Backend modules | `compileall` completed successfully |
| React TSX source | Global TypeScript `transpileModule` parser reported **0 syntax diagnostics**; full `tsc`/Vite build **not performed** |
| User logo | Original uploaded image copied to `frontend/public/logo.png`, small `favicon.png` generated, and logo copied to static showcase |
| Public showcase | HTML parsed, image assets present and exact-byte match checked |
| Single-port local production serving | FastAPI `StaticFiles` + `/api/health` tested with a tiny **test-only static fixture**, both returned HTTP 200 |
| Browser testing in current sandbox | **Blocked by environment policy** for both loopback and file URLs; no current browser screenshots or real navigation results claimed |
| Frontend dependency install | **Not completed**: external package registry DNS/network unavailable here, so npm unit tests/build cannot be rerun |
| Actual Gemma 3 4B vision inference | **Not executed**: Ollama and model weights absent |
| Windows PowerShell/native machine | Not executed in this Linux environment |
| Human relevance benchmark, RTX 4050 latency and offline egress capture | Not executed; target-device verification required |
| GitHub Pages public deployment | Workflow and static site provided; **not deployed**, no publishing repository with write permission provided |

### Implemented changes

- Exact user-supplied aperture logo replaces the previous logo, with consistent favicon and brand text.
- Removed `ImageHash` dependency; self-contained perceptual hash implementation uses OpenCV's discrete cosine transform, Pillow resize, and Hamming comparison.
- Active collection limit (8), bounded in-memory inference cache (250), configurable image-input size (256–896 px), and cache invalidation after photo deletion.
- Cooperative cancel-after-current-image feature and Cancel control; duplicate IDs prohibited in export list.
- Added test isolation and four regression tests (quota, queued cancellation, repeated exports, hash robustness).
- Added a **single-port local production mode** that serves a built React frontend and FastAPI from `127.0.0.1:8000`; it was verified only with a fixture, not the complete frontend bundle.
- Added a truthful static public showcase, GitHub Pages publishing workflow, CI workflow, and deployment instructions. This **does not host private photo inference**.

### Required next verification steps

1. Run `scripts/verify.ps1` on Windows after setup and model installation (or `scripts/verify.sh` in WSL), recording full frontend results.
2. Run the live model on a known image and at least three distinct permitted photographs; inspect visual evidence and errors.
3. Run UI workflows with a real browser, including cancel after a current photo, duplicate filtering, shortlist, and metadata-free export.
4. Record actual relevance and effort benchmarks, test offline inference with network monitoring, and replace submission placeholders.
5. Push the source to a new authorized GitHub repository and check successful GitHub Pages action and visible branding before claiming a public URL.

**No live hosting, real image inference, numerical model performance, or competition eligibility has been claimed as verified by these environment-only checks.**
