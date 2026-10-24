# Hacktoberfest 2026 Week 3 submission checklist

**Challenge:** Open-Source AI Challenge, Week 3 — *Slow and Steady*. Submission deadline: **October 25, 2026, 11:59 PM Pacific**, approximately **October 26, 12:29 PM in India**. Always check the official contest page for any changes.

## What Thooriga solves

A small bakery owner may take dozens of product photographs, then repeatedly scroll through them to find the frames that best fit an Instagram promotion. Thooriga removes the mechanical parts of that selection process: local photo comparison, near-duplicate detection, purpose-aware Gemma assessment, and cropping previews. **The human still chooses the final photos.**

## Category to prioritize

**Best Use of Gemma:** The backend's `assess()` function sends actual downsampled image bytes and the specific user brief to a locally running `gemma3:4b` through Ollama. The structured assessment contributes 85% of the nominal ranking weighting (relevance 60%, suitability 25%), with cropping/resolution factors making up the remainder. An observable real run is still required to validate the intended behavior and sponsor claim.

There are **no live Sentry traces, Atlas retrieval, Render-hosted inference, or other partner integrations** in this release. Do not enter categories based only on ideas or tools mentioned in documentation.

## User-visible deliverables

- Working source package and CI workflow; no bundled model weights or runtime dependencies.
- Locally installable React/TypeScript UI and FastAPI API; browser layout and GitHub Pages public showcase.
- Unit and integration tests, screenshots of the UI, relevant privacy documentation.
- Optional **concept storyboard**, delivered separately from the source ZIP and labeled as illustrative rather than a product demo.
- Editable DEV article draft: [docs/DEV_ARTICLE.md](DEV_ARTICLE.md).

## Do these before publishing the DEV post

1. Create a **new** GitHub repository created within the challenge period; push and verify files, default branch, and CI status.
2. On a laptop with Ollama, run `ollama pull gemma3:4b`, start the app, and **verify a live image-dependent result**. Record model version, response time, visible image-dependent observation, and known limitations.
3. Take a screenshot or video recording of the real analysis—not solely the illustrative concept storyboard.
4. Measure manual active time vs assisted active time on a small permitted collection, documenting model wait time separately. If not done, say it was **not measured**.
5. Remove or rewrite claims in the DEV draft that don't match tested behavior, replace repository/demo placeholders, and publish with the official Week 3 template and required `#devchallenge` / `#hf26challenge` tags.

## No false success claims

The existence of a model API client and simulated tests **does not establish that Gemma was run successfully on the target laptop**. Do not claim verified vision performance, deployment, GitHub Actions success, or human evaluation without actual evidence.

## Hosting

The public GitHub Pages workflow deploys `site/`, a showcase **without upload/inference**. Running private Gemma vision from that public site is not implemented. The actual photo curation app runs locally via `scripts/start-production.ps1` after compiling the frontend.
