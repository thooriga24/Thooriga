# Open-source dependencies and model terms

**Application source:** MIT, see [LICENSE](LICENSE).

**AI weights:** `gemma3:4b` is an **open-weight** Google Gemma model and is not redistributed in this repository. Its use is subject to the separate [Gemma terms](https://ai.google.dev/gemma/terms). The Ollama runtime and model must be installed separately.

**Third-party software (not relicensed by the project's MIT license):**

- React and React DOM: UI runtime.
- Vite, TypeScript, Vitest, Tailwind CSS and `@tailwindcss/vite`: build, styling, and tests.
- Lucide React: interface icon assets.
- FastAPI, Starlette, Uvicorn, Pydantic, HTTPX and python-multipart: API, validation, and Ollama communication.
- Pillow, NumPy and OpenCV: local image decoding, cropping, similarity, and quality indicators.
- Pytest: backend unit testing.

Pinned dependencies are listed in `requirements.txt` and `frontend/package-lock.json`. Each upstream package retains its own copyright and license. Review the installed distributions' licenses before redistribution; **dependencies and model weights are not bundled** in the source ZIP.

**Bundled sample photograph:** the NASA-derived `astronaut.png` is a public-domain sample with provenance documented in [backend/samples/ATTRIBUTION.md](backend/samples/ATTRIBUTION.md).

**Logo and branding:** the aperture image was supplied by the user. See [frontend/public/BRAND.md](frontend/public/BRAND.md); confirm redistribution rights before publishing the repository.

**Concept video:** An optional `Thooriga_Concept_Storyboard.mp4` is delivered separately from the source repository. It was recovered from a prior project deliverable and is a storyboard, **not a screen recording of verified Gemma inference**. Review image/music permissions before reusing it in a public announcement.
