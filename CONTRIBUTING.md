# Contributing to Thooriga

Thooriga is an MIT-licensed, local-first photo discovery assistant. Contributions are welcome—particularly improvements that reduce tedious photo searching **without replacing the creator's final judgment**.

## Start with a reproducible change

1. Read [README.md](README.md), [PRIVACY.md](PRIVACY.md), and [docs/SETUP.md](docs/SETUP.md).
2. Create a branch and use permitted/synthetic photos in tests. **Never commit someone else's personal photographs, EXIF location data, access tokens, or model weights.**
3. Add regression tests for bugs and compare relevance/latency before claiming model improvements.
4. Run `python -m pytest -q` and `(cd frontend && npm ci && npm test && npm run build)` in an environment with dependencies available.
5. Open a pull request describing behavior, privacy impact, and any inference or evaluation constraints.

## Priorities

- Better photo retrieval and diversity of the shortlist, especially when near-duplicates have different quality.
- Human-controlled export, adjustable crops, meaningful keyboard navigation, cancellation, and bounded storage.
- More reliable structured Gemma assessments with measured success/failure reporting.
- Accessible small-screen layout and privacy-first performance improvements.

## AI and evaluation policy

- Gemma model outputs must never be presented as ground truth about people, cultural identity, hidden feelings, or artistic value.
- No invented accuracy numbers, fabricated trace screenshots, or canned AI answers labeled as live inference.
- Do not upload private photos to issue trackers or public CI. Use synthetic test images or appropriately licensed public samples.
- Model weights are **not** covered by the app's MIT license; follow Google Gemma's separate terms.

## Responsible disclosure

Please see [SECURITY.md](SECURITY.md). The current backend is designed for localhost; internet-facing deployment needs authentication, isolation, abuse prevention and a new privacy design.
