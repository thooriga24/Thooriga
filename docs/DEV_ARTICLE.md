---
title: "Thooriga: I wanted to help a bakery owner stop scrolling through the same cake photos"
published: false
tags: devchallenge, hf26challenge
---

*Submission for the Hacktoberfest 2026 Open-Source AI Challenge — Week 3, Slow and Steady.*

## What I Built

A small bakery owner can spend an evening perfecting a cake, take dozens of product photographs, and then face one last surprisingly tedious chore: finding the few photographs that actually work for an Instagram campaign. This was the problem that inspired **Thooriga**.

For a Halloween cake promotion, a brief might be: **“Find photos that clearly highlight the Halloween cake decorations and leave room for Instagram offer text.”** Instead of repeatedly scrolling through near-identical shots, the user gives Thooriga a small album and the exact purpose. It assesses candidates, groups near-duplicates, previews crop compatibility, and produces an explainable shortlist. The final creative choice remains with the person who took the photographs.

Thooriga targets small bakeries, cafés, shops and everyday creators who manage their own photos without a dedicated editor. The idea is not to automate creativity; it is to **automate the boring search around creativity**.

## Demo

- **Source:** Add the actual GitHub repository URL after publication.
- **Video:** Add a real recording of the implemented app analyzing permitted photos through a locally installed Gemma model.
- A separate 72-second *concept storyboard* is available with the release; it is **not** a record of live model inference and should only be shown as an introduction.
- The repository includes interface screenshots and a public-domain test image. The static GitHub Pages showcase can be published separately and **does not provide a hosted photo analysis service**.

A useful actual demo should show: upload, Halloween bakery creative brief, local model progress, shortlist with explainable results, restoration of a lower-ranked photo, user-defined ordering, and metadata-free export.

## Code

The repository includes React + TypeScript + Vite, FastAPI, a real Gemma/Ollama request adapter, Pillow/OpenCV image processing, ZIP export, tests, Windows/WSL setup scripts, and privacy/security documentation.

**GitHub:** `ADD_REAL_GITHUB_REPO_URL`

The entire project source is MIT-licensed; Google Gemma **weights** are open-weight and subject to their own terms. Model files are not copied into the repository.

## How I Built It

1. **Upload:** FastAPI checks file sizes and decoded image formats, corrects EXIF orientation, and keeps private processing copies in a temporary directory.
2. **Technical screening:** Pillow/OpenCV extract image dimensions and similarity fingerprints to identify near-duplicates; simple center-crop previews show how much image area different formats retain.
3. **Local open-weight AI:** the backend encodes reduced image data and sends it along with the user's specific creative brief to **Gemma 3 4B vision through Ollama at localhost**. It requests relevance/suitability on a transparent 0–4 rubric, with observable features and limitations.
4. **Validation:** Pydantic validates the structured response. Invalid model output or unreachable Ollama results in an error, never fake results.
5. **Shortlist:** 60% of the scoring weight is AI relevance, 25% AI suitability, 10% crop compatibility and 5% resolution. Near-duplicates are diversified so the strongest candidate of a group is recommended first. All lower-ranked options remain reviewable.
6. **Human review:** The user selects, compares, reorders and exports. Source files are unchanged; exported JPEG copies omit metadata.

The entire local service binds to `127.0.0.1` by default. This is deliberately not a public photo-upload API. The public GitHub Pages site is a documentation/showcase page only.

### Engineering decisions

- **Model choice:** A vision-capable Gemma 3 4B model instead of a text-only one, with resized inputs and sequential inference to limit VRAM demands.
- **Smaller scope:** 15-photo maximum batch, no accounts or cloud gallery, no automatic publishing.
- **Transparency:** Mood terms are subjective; the model cannot claim to know hidden emotions, identity, or anyone's true artistic preferences.
- **Privacy caveat:** Source files are stored temporarily until collection clear or normal shutdown, and a forced process crash may leave local temporary data. The loopback network request is enforced in code, but a full operating-system egress audit on the target laptop remains necessary.

## What I Tested

In the current release environment, **29 Python tests passed**, including request validation, image uploads, resized and brightness-modified duplicate detection, crop geometry, missing-model behavior, structured response contracts, local-only request configuration, safe exports, cancellation, ranking diversity, and cache/job lifecycle behavior. A source/branding release audit and TypeScript syntax parse also passed.

Previous Work-run documentation records frontend/browser tests, but the latest frontend install/build could not be rerun in this continuation because package registry access timed out and the offline npm cache was incomplete. Most importantly, **actual `gemma3:4b` image inference was not verified in the current execution environment**. Tests using fixtures do not count as live model evaluation.

**Measured human time saved:** not yet measured.  **Gemma relevance score / GPU timing:** not yet measured. Do not replace these fields with invented estimates. Run `python scripts/smoke_gemma.py` on a model-equipped laptop before claiming the project demonstrated image-dependent results.

## Why Does Open Innovation Matter?

The photos in an album may include product drafts, faces, home interiors, and personal moments. A local model means Thooriga can, after its weights are installed, keep photo processing on the user's computer rather than making a third-party hosted model upload mandatory. The source pipeline is open for inspection and improvement: the ranking rubric, duplicate logic, export and error handling are editable rather than hidden behind an opaque API.

This approach carries tradeoffs: a local model needs machine resources, real inference can be slower, and running locally alone is not an absolute security guarantee. Gemma's model license also remains distinct from Thooriga's MIT source license.

## The Lazy Payoff

The important number is not how many photos an AI can label. It is **how many photos a person no longer needs to inspect manually** to find suitable candidates. A fair experiment compares active human selection time with and without Thooriga on the same permissioned set, reports model waiting time separately, and checks whether human-preferred photos appear in the shortlist. The benchmark templates and methodology are included in `docs/BENCHMARK.md`.

The result we are pursuing is simple: less scrolling for a small business owner, while the owner keeps the final creative decision.

## What Comes Next

After live Gemma verification, the highest-value improvements are adjustable cropping, stronger accessibility testing, reliable large-album preselection, and an opt-in safe LAN/device experience. We deliberately deferred unrelated cloud databases, extra agents and sponsor integrations to keep the first release focused.

## My Agent Session

Previous Codex/Work iterations helped implement and test the application. If a real shareable session reference is available, link it here; don't invent an agent-session URL.

---

**Publication check:** Replace `ADD_REAL_GITHUB_REPO_URL`, add an actual working AI demo, verify latest build and remove this instruction section before publishing. Required DEV tags: `#devchallenge` `#hf26challenge`.
