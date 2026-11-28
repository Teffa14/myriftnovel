---
name: tld-editorial-review
description: "Perform developmental, structural, psychological, technical, line and natural-prose review of exact-version The Last Draw chapter candidates; execute metrics, revision diffs and evidence checks without fake quality scores."
---

# tld-editorial-review

Project scope: The Last Draw: A competitive TCG Novel (Teffa14/myriftnovel). Read current root AGENTS.md and live canonical sources before using this skill. This operational summary does not supersede them. Paths below are repository-root-relative, not relative to this SKILL.md.

## Required references
- 04_CHARACTERS/DEVELOPMENT_REQUIREMENTS.md
- 08_CHAPTERS/CHAPTER_PRODUCTION_PLAYBOOK.md
- 09_EDITORIAL_QA/EDITORIAL_SYSTEM.md
- 09_EDITORIAL_QA/CH0001_REVISION_BENCHMARKS.json
- 02_STYLE_BIBLE/STYLE.md
- 01_RESEARCH/REFERENCE_LIBRARY/works/WNG/EDITORIAL_MECHANISMS.md
- 06_COMPETITIVE_ENGINE/SCENE_INTEGRITY.md

## Review and revise
Retrieve exact candidate and authorized prior revision. First pass: structure, reader promise, scene causality, stakes, character psychology/agency, voice, pacing, emotional consequence, accessibility and actual technical correctness. Three lenses: reader (comprehension and anticipation), editor (promise, pacing, evidence), author (mechanism and alternatives). Distinguish predicted reaction from measured reader response.
Then line-edit for repeated openings, contrast formulas, gestures, cognitive verbs, vague summaries, redundant explanation, uniform rhythm, artificial banter and continuity errors. Keep strong existing passages; fix material defects rather than regenerating indiscriminately. Naturalness and precision trump detector scores. Recheck disputed technical statements via tld-competitive-evidence and state via tld-continuity.
Use consistent declared tokenization on exact clean manuscript bytes (exclude heading, author note, editorial material; distinguish scene separators). Record SHA-256, words, distinct normalized forms, paragraph count/mean/median/distribution, sentence estimate, dialogue estimator, repeated starts, frequent words, internal repeated 5-grams and scene allocations. Measure diffs across actual revisions; no fabricated measurements or stale metrics. Historical CH0001 diagnostics and rubric targets are not quotas. Use actual evidence for provisional scores, distinguish same-agent review from independent review, no invented readers or claims of authorship.
Run tld-originality on final candidate, rerun affected checks after edits, and require zero unresolved critical rule/continuity/originality defects before recommending acceptance. A score is not author approval.

## Output
Private editorial_review.md, clean chapter_final.md candidate, exact-byte metrics, revision diff, qa_report.md, explicit unresolved issues, and review verdict. Deliver complete chapter separately; do not automatically publish, approve or continue.

AD-0007: apply the character-specific CD requirements and cross-character gates in 04_CHARACTERS/DEVELOPMENT_REQUIREMENTS.md; record evidence and status for actual developments, justified omissions and deferred requirements. Preserve historical baseline scores, approved history and active private author directions.

AD-0009: review temporal narration under 02_STYLE_BIBLE/STYLE.md and 09_EDITORIAL_QA/EDITORIAL_SYSTEM.md. Audit precise time references, spelled-out times, exact durations, clock-check repetition and time-led paragraph openings. Justify necessary anchors, revise redundant ones, and revalidate private chronology without changing approved prose. Counts are diagnostic only.

AD-0013: review against 02_STYLE_BIBLE/TLD_VOICE_METHOD.md, using 02_STYLE_BIBLE/voice_audit.py on exact text where available. Record meaningful stylistic decisions and comparable evidence before/after; preserve intentional dialogue, recurring motifs and technical details. Detector findings are not proof of authorship. Do not certify literary improvement from counts alone.

AD-0014-A01: for CH15–19 review the concrete incoming and outgoing causal links, local reward, continuity and order/deletion test in PILOT_20.md; require material contribution to CH20 without forced outcomes or cliffhangers. Distinguish provisional candidate developments from approved history.

AD-0017: apply 02_STYLE_BIBLE/LITERARY_CRAFT_PROTOCOL.md; record exact private passage evidence for experiential depth and meaningful revisions, evaluate alternatives when appropriate, preserve protected facts and all prior checks. No technique-count score or fabricated reader response.
