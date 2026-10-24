# Security and privacy scope

## Supported deployment

The local FastAPI API, frontend, and Ollama model are intended to run on the **same trusted laptop**. The API binds to `127.0.0.1` and contains **no internet-facing authentication**. Do not expose the backend, Ollama, or Vite dev server on a public network. GitHub Pages hosts only a no-upload project showcase.

## Reporting

Do not publish exploit examples containing private photos or personal data. Report an issue with a minimal synthetic reproduction. For sensitive security issues, use private GitHub security reporting if enabled by the repository owner.

## Threats and limits

Decoded content checks and upload-size/image-pixel limits help guard against invalid images and resource exhaustion. Random collection IDs do not replace authentication. Source photos are copied into a temporary directory, with cleanup on collection deletion or a normal backend shutdown; abnormal termination can leave files behind. Running the app on a shared or compromised computer does not guarantee confidentiality. Exported JPGs have EXIF metadata stripped, but visible content may itself be sensitive.

The inference adapter sends photographs to Ollama on loopback and disables inherited HTTP proxies. A complete network audit is a separate, not-yet-verified test on the target laptop. Run it before describing the system as proven offline/private in a public competition post.
