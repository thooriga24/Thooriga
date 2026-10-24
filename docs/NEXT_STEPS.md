# Next steps: verify, measure, then improve

The application source and local workflow are delivered. Actual local Gemma inference, target-laptop performance, human relevance evaluation, and model egress auditing remain unverified. Follow this sequence before adding optional integrations.

## 1. Verify real Gemma vision on the target laptop

**Run:** Complete [SETUP.md](SETUP.md), install `gemma3:4b`, and use 3 permitted photos with clearly different subjects. Repeat with a resized duplicate and a 10–15 image collection.

```powershell
ollama --version
ollama list
ollama show gemma3:4b
ollama ps
Invoke-RestMethod http://127.0.0.1:8000/api/models/status
```

Record OS, CPU/GPU, installed model tag/digest, batch size, wall-clock duration, timeout count, observed RAM/VRAM and whether explanations refer accurately to visible contents. Do not publish private prompt text or photographs as evidence without permission.

**Done when:** Actual image-dependent assessments succeed, misleading explanations are recorded rather than hidden, the human can restore/reorder results, and exported copies open correctly.

## 2. Measure relevance and effort honestly

Prepare the permitted photo/brief pairs in [BENCHMARK.md](BENCHMARK.md). Keep human judgments independent of model rankings. Include negatives and cases where technical sharpness is not the goal.

Copy `docs/judgments-template.csv` to a new file, fill actual judgments and ranks, then run:

```powershell
.\.venv\Scripts\python.exe scripts\evaluate.py docs\judgments.csv --k 3
```

```bash
.venv/bin/python scripts/evaluate.py docs/judgments.csv --k 3
```

Separately record manual/assisted active time, model waiting time, photographs inspected, relevant selections, and duplicate corrections. Report failed model runs and exclusions. Do not treat mocked fixtures as relevance results.

**Done when:** Baseline and Gemma precision/nDCG values and limitations are documented from real judgments, with user-effort results presented separately.

## 3. Verify privacy on the laptop

Install dependencies and weights first. Disconnect outbound Internet or apply an outbound firewall rule while allowing loopback. Repeat real analysis and export while observing process traffic with Windows Resource Monitor or a local packet capture.

Verify that no image-processing connection leaves loopback, clear the collection, stop the backend normally, and check its temporary directory is removed. Document forced-shutdown leftovers separately. Existing automated loopback, metadata and cleanup tests are useful but do not replace this audit.

**Done when:** The exact runtime, firewall/capture procedure, duration and findings are recorded in `docs/RESULTS.md` without leaking image data.

## 4. Improve performance only after measuring

Measure cold/warm analysis and exact-cache repeats first. Compare 896-pixel inputs with a smaller setting on a development branch; re-evaluate visual relevance so speed does not hide quality loss. The current input-size setting lives in `backend/app.py`, not an environment variable.

Then consider reusable image captions/embeddings and OpenCLIP preselection. Keep Gemma's assessment material to final ranking, document candidate recall, and avoid loading both large models simultaneously on 6 GB VRAM without measuring memory. Brief changes currently require fresh conditional vision assessments unless the exact cache key matches.

**Done when:** Changes have measured latency/memory benefit and acceptable relevance, not just fewer model calls.

## 5. Refine curation and accessibility

Improve crop adjustment and subject-aware warnings without modifying originals. Evaluate duplicate thresholds on known positive and negative pairs; remove upload-order dependence in diversity scoring if measured results justify it. Add keyboard/screen-reader review, focus management, contrast checks and physical-device testing.

For a phone accessing the laptop, design authenticated, encrypted local access and a restrictive origin policy before opening network interfaces. Responsive layout support alone does not provide safe LAN hosting.

**Done when:** Users can inspect/edit crops, access controls work with keyboard and assistive tools, and any network access has an explicit security design.

## 6. Harden session lifetime and reliability

Add bounded collection/cache quotas, idle expiry, cancelable jobs, shutdown cleanup coverage, and regression tests for concurrent upload/analysis actions. If persistence is introduced, define the retention/deletion policy first; SQLite is sufficient for small local metadata.

**Done when:** Resource use remains bounded during long sessions, cancellation has clear behavior, and cleanup is verified after normal and abnormal exits.

## 7. Prepare a public release

Run the backend/frontend checks from [SETUP.md](SETUP.md), refresh real screenshots and test counts, record the live demo, update privacy/evaluation evidence, and review licenses for every bundled asset. Update `docs/DEV_ARTICLE.md` with actual model and benchmark results before publishing it. Add a genuine repository URL only after creating/publishing the repository.

The UI itself should remain free of event text, taglines, sponsor claims and benchmark claims. Keep submission material in documentation. Optional Sentry tracing is useful only after real multi-step execution works and privacy-preserving traces can be demonstrated.

## 8. Publish the privacy-safe public showcase

Use [DEPLOYMENT.md](DEPLOYMENT.md). This delivery contains a self-contained `site/` and GitHub Pages action. It is not a hosted photo-analysis application; visitors must run the full application locally for Gemma vision. No real hosting account was accessed during this revision. Before publishing, verify redistribution rights for the supplied logo.
