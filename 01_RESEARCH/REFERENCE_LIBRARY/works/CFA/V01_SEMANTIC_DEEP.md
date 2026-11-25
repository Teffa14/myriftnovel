# CFA V01 — contextual semantic indexing and scene review
2026-11-25. Source: same user-provided EPUB as V01_ANALYSIS.md. SHA-256 1fa0b9f81e210e0519ec32957960c4d6795e8d75dedb1682af83f006c2269c7c. No source text stored in Git. NDM v1.0. Scope: exhaustive automatic paragraph indexing, sampled qualitative review in all 61 explicit separator-delimited blocks, and 16 additional paragraph audit selections. CH01 was previously read in full. Not a complete human-level semantic review of every paragraph; do not certify chapters or volume.
 
## Reproducible execution
Python reads 17 XHTML narrative files in OPF spine, groups prologue and chapters 1–7, preserves § as a boundary, excludes blank paragraphs and § from token count. Each paragraph has chapter-local ID, exact XHTML path and original p ordinal, SHA-256, token/quote/question/exclamation counts, name mentions from a limited list, first-person pronoun count, 12 regex lexicon indicators, context cluster and candidate role tags. Neighboring paragraphs within the same separator block form context; TF-IDF unigrams/bigrams (min_df=3, max_df=.8, max_features=10000), 32 SVD components, L2 normalization, KMeans 18 clusters, n_init=10, seed 42. Explained variance 0.0883: low-dimensional clustering is exploratory and not equivalent to narrative semantics. No semantic embedding model or POS/parser used. No original sentences stored in output archive. Cluster top terms are aggregate short lexical signals.
 
## Verified structural totals
| Unit | Paragraphs | Separator blocks |
|---|---:|---:|
| Prologue |107|4|
| CH01 |86|1|
| CH02 |212|5|
| CH03 |162|3|
| CH04 |1010|17|
| CH05 |315|6|
| CH06 |743|18|
| CH07 |333|7|
| Total |2968|61|
79,988 tokens, 17,673 quoted tokens. 2,525 paragraphs have one or more candidate flags; 443 unclassified by rules, not empty of narrative function. Categories overlap, not a partition. Paragraph prevalence: cognition 342, decision 302, contrast 635, causal 439, conditional 228, emotion 104, conflict 227, social 152, resources 419, exposition 195, temporal 523, uncertainty 514. Tests actually executed: all 2,968 (unit, paragraph) keys unique; sum of tokens 79,988; scene map exactly matches 61 distinct separator IDs; archive integrity zipfile.testzip returns None; Git blob exact match. 
## Qualitative scene map
Archive scene_review.tsv maps all 61 blocks to a candidate function and unresolved question, based on samples from each block's beginning, middle, end and selected high-marker paragraphs. This is block-level sample review, not exhaustive scene reading. The boundaries are editorial separators, not guaranteed individual dramatic scenes. Compare ranges in scenes.csv. No automatic label has been individually approved. 
- Prologue S01–S04: escalation, reframing as observed fiction, reversal, past dominance revised by later context. Distinguish narrated media outcome from current world outcome.
- CH01 S01: anomaly, identity recognition, experiment, cost, survival commitment. Fully read in earlier turn; no complete independent QA.
- CH02 S01–S05: social reaction establishes question; analepsis returns to prior planning; independent interpretation after public behavior. Mundane needs create contrast.
- CH03 S01–S03: subordinate and protagonist interpret encounter differently; longitudinal escalation of interpersonal friction; training method needs revision. Do not treat devotion as consent.
- CH04 S01–S17: institution and stakes, entry and negotiation, rewind to capability test (S04–S06), return to present negotiation (S07), cascading interpretation, technical instruction, unknown variable, relationship and obligations, emergency at exit (S17). Sample evidence, not full combat reconstruction.
- CH05 S01–S06: public crisis initially from civilians and allies, then earlier emergency message revisited (S03) and parallel root-cause objective (S04); social consequences and repair (S05–S06). Distinguish narrative ordering from chronological ordering.
- CH06 S01–S18: new recruitment goal, delegation, travel and specialist ecosystem; remote perspectives (S04, S11) and independent motives, apprenticeship conflict, public institutional reaction (S15), demonstration announced at close (S18). Do not infer outcome.
- CH07 S01–S07: threat from opposing perspective, confrontation, emotional retrospective (S03), return to ongoing crisis (S04), partial resolution and renewed threat. No claim of closed volume arc.
 
## Additional mechanisms (C09–C12)
Evidence-supported candidate refinements, not independent certified mechanisms. C09 delayed explanation via structured analepsis (CH02 S01–S02; CH04 S03–S07); C10 evidence-driven reallocation (CH04 S05–S06); C11 parallel response with delayed chronological alignment (CH04 S17, CH05 S01–S04); C12 backstory inserted at pressure point to reframe stake (CH07 S02–S04). Crosslinks to existing M84/M87/M89/M52/M132/G10/M88. Two original blocks CB05–CB06. Avoid copying plot order, wording or fictional mechanisms. In physical TCG, legal replay, POV boundaries, credible finances and consent remain mandatory.
 
## Audit and limitations
AUDIT_16.tsv documents eight flag-positive and eight unclassified paragraphs, one of each per unit, random.Random(42) selection from CSV order. All eight unclassified examples contain meaningful narrative functions, showing false negatives of marker approach. Flagged examples often contain incomplete or misleading categories (e.g. discourse 'so' not causal; mention of battle not active combat). No representative accuracy, precision/recall or inter-rater agreement estimated. All paragraphs remain automatic_unverified. No full human-level review of 2,968 paragraphs, POS analysis, reader test, or complete chapter certification. The output enables targeted review; it does not substitute for reading.
 
## Artifact
CFA_V01_semantic.zip (179343 bytes; SHA-256 99f0d316e09d37cc4f227520a20dea1e930e21d6383fc718631581db3116f88f; Git blob 925e9a736e76d80a3b29da98ff3e29d863c8d77a). Six files: paragraphs.csv, scenes.csv, scene_review.tsv, clusters.json, method.json, semantic.py. Run: python semantic.py /path/to/volume.epub output_dir. Generated private review excerpts are not in archive.