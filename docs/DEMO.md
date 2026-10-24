# Reproducible demo and short video script

Use 6–15 photographs you own or have explicit permission to process. For a public recording, obtain permission for people and location details. No private photographs or precomputed rankings are bundled. The app includes an optional public-domain NASA photo, with provenance in `backend/samples/ATTRIBUTION.md`; use it for a one-photo smoke test, not a relevance benchmark. Repository test graphics are synthetic image-processing fixtures, not a real-photo AI benchmark.

0–15s: "This is Thooriga. A bakery owner can take dozens of photos of one cake. Finding a few useful promotional frames takes repetitive inspection."

15–35s: Upload your permitted bakery collection with a duplicate. Show previews and describe "Chocolate cake photographs with warm light and space for a 20% offer." Select Story and three frames.

35–60s: Start local Gemma. Show actual progress; if editing out waiting, disclose the measured duration. Do not record a successful AI result until real inference has run. Show observations and crop warnings; explain scores aren't beauty ratings.

60–80s: Compare two photos, restore a lower result, choose favorites, reorder in Shortlist. "The model helps search. I make the creative decision."

80–95s: Export, inspect the ZIP, clear collection. "No automatic publishing; local model execution after installation."

Screenshots: `docs/desktop.png` and `docs/mobile.png` capture the real empty UI using Chromium if browser verification has completed. They do not depict AI recommendations. The browser integration script uploads only a synthetic fixture and expects a missing-model error in this environment.


## Halloween bakery story asset

A separately provided 72-second concept storyboard illustrates the bakery-owner pain point using a Halloween cake promotion. It is not a recording of real model inference or the implemented application. Keep it labeled as a concept/intro if reusing it. For judging technical execution, show the real running studio, Gemma response, and user-controlled export instead.
