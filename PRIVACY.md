# Privacy & security

## Data flow

Browser → local FastAPI (`127.0.0.1:8000`) → local Ollama (`127.0.0.1:11434`). Browser assets and Lucide icons are bundled, with system fonts and no remote image references. No analytics, training pipeline, automatic backup or publication exists. HTTPX disables environment proxies for Ollama calls. Model installation and dependency installation require Internet.

Uploads are decoded, EXIF orientation applied, and processing copies saved as JPEG under Python's system temporary directory, `thooriga-<random>/<random collection>/<random photo>.jpg`. Metadata is omitted from processing copies and exports. Selected source files on the user's computer are never modified. JPEG conversion loses transparency and can change color; exports are copies, not byte-identical originals.

The browser stores collection capability IDs only in memory. Briefs, assessments and cache stay in backend memory. Clearing a collection removes its processing directory and jobs, and clears assessment cache. Individual removal deletes its processing copy. Normal server shutdown removes the temporary root. Browser close alone does not delete backend files. Crashes, forced shutdowns, OS swap, filesystem recovery, browser caches, or external backups may retain data. After stopping all Thooriga processes, remove stale `thooriga-*` temporary folders if needed. No claim of secure erasure is made.

## Protections and scope

Random IDs are mapped server-side, never joined from arbitrary client paths. Allowed decoded formats: JPEG/PNG/WebP; batch default 15, per-file default 15 MB, decoded pixel limit 24 million. Wrong origin and Host headers are rejected; allowed frontend origins are localhost only. Export names are generated, metadata removed, ZIP contents never use upload filenames. Access logs should remain disabled. Errors don't include filenames, prompt contents or image bytes.

Single-user local application: there is no authentication, TLS, persistent storage, or multi-user isolation. Local malicious processes can access the API. Global session collections/jobs/cache are not an unlimited-service architecture; clear unused collections and restart periodically. Multipart parsing happens before endpoint checks, so this is not a hardened Internet upload service. Inference cannot be canceled mid-call; timeout bounds a single call. Do not bind to all interfaces.

## Verification

Automated tests inspect the exact loopback model URL, resized image payload, export metadata, safe filenames, unknown path IDs, wrong origins/hosts, and cleanup. Browser checks exercise the real local HTTP application. These are design/contract checks, **not an outbound packet audit**. Real Gemma offline operation and OS-level egress have not been verified here.

For a laptop privacy audit: preinstall weights and dependencies; close unrelated apps; record process/network baselines using Resource Monitor or Wireshark; disconnect outbound Internet or enforce outbound firewall blocks while allowing localhost; run an analysis and export; check no image processing connection leaves loopback. Record model digest, runtime versions, firewall rules, capture duration and result in `docs/RESULTS.md`. Do not publish photo bytes or prompt contents in captures or traces.
