# Evaluation protocol — not completed

Do not infer relevance or effort improvement from unit tests. Real inference and human evaluation remain required.

Prepare 15 consented/licensed photos with license/source records, covering restaurant promotion, product, traditional celebration, professional portrait, friendly interaction atmosphere and cinematic travel. Add 3 transformed duplicate variants (resize, JPEG recompression, slight brightness change). Write one brief per scenario. Ask two human reviewers to judge relevance 0–2 (irrelevant/partial/strong), resolving disagreements. At least 24 photo/brief judgments, including negatives, are required; more are preferable. Never infer personal cultural identity or emotional state.

Record a CSV with `brief_id,photo_id,human_relevance,baseline_rank,gemma_rank,duplicate_truth_group,predicted_group,seconds`. The baseline is a technical/crop-only ranking using the same dimensions and no semantic claims; define tie order by upload order. Compare against the full pipeline using precision@3 (strong relevance / 3) and graded nDCG@3. Report per brief and macro mean; retain failed analyses as failures rather than dropping them. Use equal candidate sets and document every exclusion. This baseline is a proposed evaluation, not a measured retrieval system.

Effort: counterbalance manual versus assisted order across participants using matched collections. Record active task seconds, model waiting seconds, number of inspected images, selected relevant images and corrections. Report waiting separately and end-to-end; a slower local model may save clicks while increasing elapsed time. Do not claim savings without participants and measured values.

Duplicates: label pairwise positives/negatives and report precision/recall. Include resized, recompressed and brightness-altered images, plus visually similar distinct compositions. Record threshold sensitivity (4/6/8 bits). A single transformed-copy unit test is not grouping accuracy.

Hardware: record CPU/GPU, OS, Ollama version, model digest/quantization, GPU offload from `ollama ps`, VRAM/RAM peak, cold/warm run timings, photo counts/resolutions and timeout rate. Compare 896 vs 640 pixel inference and cache-hit second runs, while keeping all prompts identical. No RTX 4050 measurement is available in the current environment.

After filling actual judgments, run `python scripts/evaluate.py docs/judgments-template.csv --k 3` (copy/rename the template first). The evaluator refuses an empty template and reports per-brief and macro precision/nDCG. It does not invent labels or fetch models. Record failed Gemma runs separately in the report; this evaluator requires complete ranks for each included brief, so disclose exclusions explicitly.
