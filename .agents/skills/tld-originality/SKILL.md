---
name: tld-originality
description: "Apply NDM 2.0 originality screening to The Last Draw drafts against every approved chapter and supplement, lexical fingerprints, retired expressions and semantic usage signatures. Use before acceptance, revisions or recursive distillation."
---

# tld-originality

Project scope: The Last Draw: A competitive TCG Novel (Teffa14/myriftnovel). Read current root AGENTS.md and live canonical sources before using this skill. This operational summary does not supersede them. Paths below are repository-root-relative, not relative to this SKILL.md.

## Required references
- 02_STYLE_BIBLE/ORIGINALITY/PROTOCOL.md
- 02_STYLE_BIBLE/ORIGINALITY/STATUS.json
- 02_STYLE_BIBLE/ORIGINALITY/repetition_check.py
- 02_STYLE_BIBLE/ORIGINALITY/test_repetition_check.py
- 08_CHAPTERS/PROMPTS/RECURSIVE_DISTILLATION_PROMPT.md
- 08_CHAPTERS/CHAPTER_PRODUCTION_PLAYBOOK.md

## Before generation
Use tld-continuity to verify authoritative archive and hashes. Load abstract functions and usage summaries only for drafting; retired distinctive language is comparison-only, never a phrase bank. No missing-history shortcut.
## Candidate audit
Run repetition_check.py and the archive's future guard in their documented context against all approved units, including supplements. Run negative/regression checks where relevant. Analyze internal repetition and exact/near lexical flags; manually check short distinctive phrasing, near paraphrases, metaphors, descriptions, jokes, gestures, dialogue cadence, opening/closing beats, conflict/choice/payoff sequence and semantic scene signatures against full usage index. Recent chapters deserve special attention without ignoring older units. Distinguish allowed proper names, card/rules terms, common language and deliberate motifs with explicit local justification.
Repair material reuse by fresh realization, not synonym swaps or punctuation changes. Do not impose awkward word bans. Retest candidate after changes. Do not claim exhaustive external-source originality or semantic certification from lexical checks. Keep retired spans, fingerprints and detailed evidence private; do not expose earlier prose in public commit.
## Gate
Produce repetition_report.json, semantic_review.md and local exception ledger with exact candidate hash, coverage, flags, resolutions and limitations. No unresolved material reuse; author approval still required. G6 also requires actual post-approval close-out by tld-closeout; a draft audit alone cannot pass the full gate.

## Cumulative protocol dependencies
- 08_CHAPTERS/PROTOCOL_REGISTRY.json
- 08_CHAPTERS/PROTOCOL_APPLICATION.md
- 08_CHAPTERS/PROTOCOL_COVERAGE_TEMPLATE.json
- 02_STYLE_BIBLE/LITERARY_CRAFT_PROTOCOL.md
- 01_RESEARCH/REFERENCE_LIBRARY/LITERARY_CRAFT_REFERENCES.md

Resolve the live master register and apply every governing protocol cumulatively. Record private exact-version evidence, conditional applicability and real blockers; preserve approval, canon, scope and rights gates.
