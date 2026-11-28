---
name: tld-competitive-evidence
description: "Autonomously research and verify Riftbound mechanics, card identities, deck choices, matchup hypotheses, resources, scoring, prices and fictional competition scenes in The Last Draw. Use before technical prose or for game evidence audits."
---

# tld-competitive-evidence

Project scope: The Last Draw: A competitive TCG Novel (Teffa14/myriftnovel). Read current root AGENTS.md and live canonical sources before using this skill. This operational summary does not supersede them. Paths below are repository-root-relative, not relative to this SKILL.md.

## Required references
- 06_COMPETITIVE_ENGINE/SCENE_INTEGRITY.md
- 06_COMPETITIVE_ENGINE/AUTONOMOUS_PRODUCTION.md
- 06_COMPETITIVE_ENGINE/EVIDENCE/README.md
- 06_COMPETITIVE_ENGINE/EVIDENCE/STRATEGY_AND_NARRATION.md
- 06_COMPETITIVE_ENGINE/RIFTBOUND/README.md
- 06_COMPETITIVE_ENGINE/RIFTBOUND/sources.json
- 06_COMPETITIVE_ENGINE/EVIDENCE/JUDGE_CASES/README.md
- 01_RESEARCH/REFERENCE_LIBRARY/works/FTG/SOURCE_PRIORITY.md
- 01_RESEARCH/REFERENCE_LIBRARY/works/FTG/LEGEND_PROFILES.json
- 01_RESEARCH/REFERENCE_LIBRARY/works/FTG/CARD_CONTEXTS.json
- 01_RESEARCH/REFERENCE_LIBRARY/works/NLM/TRANSFER_PROTOCOL.md
- 01_RESEARCH/REFERENCE_LIBRARY/works/NLD/DECKBUILDING_PROTOCOL.md
- 06_COMPETITIVE_ENGINE/autonomous_evidence.js

## Evidence hierarchy
Determine story date, region and format. Consult FTG as primary dated strategic starting reference, NLM/NLD as general decision and deck-design reasoning, and official dated Riot rules, effective card text, errata, FAQ, bans and tournament rules for actual mechanics. Third-party decklists and sample counts are context/discovery, not rule authority. Distinguish new-rules, pre-ban and archive samples; no future data or extrapolated win rates. Resolve exact printing/identity and relevant corrected text; a catalog row is not legal proof. Keep both Master Yi Legends separate. No MTG rules imported.

## Verification scope
L0 narrative-only: verify concrete format/score facts, omit named unsupported effects. L1 bounded segment: specify plausible starting assumptions, legal action/response and resulting state; verify all relevant depicted effects and restrictions, not omitted history. L2 full replay: validate legal decklists and reachability, record draws/seed, all actions and states, timing, visibility and scoring from start to finish; actually execute or resolve a full supported ledger. G3-global is separate and incomplete. Do not claim a conditional transition is a full match.
Construct fictional play with both players' independent objectives, alternatives and counterplay. If drawing from a seed, freeze it before simulation; never reroll to force a result. Track score, locations, control vs occupation, resources and exact costs, readiness, modifiers, ownership, trigger order, priority, chain, target eligibility, combat, movement, scoring/final point and information boundaries. Test legal alternative only with support; distinguish conditional outcome and optimality.
Run autonomous_evidence.js with the story date and relevant tests, or execute equivalent scoped checks using available computation. Add negative cases and document what ran. Check market data's date/provider and distinguish hypothetical local purchase from observed price. No need for author logs, VOD or manual adjudication; retrieve independently or narrow unsupported claims.
Use FTG's matchup prompts as untested hypotheses. Apply NLM role/tempo/resource reasoning and NLD baseline/candidate, slot roles and access probabilities. Explicitly state assumptions; no fabricated matchups or reader claims.

## Output
Private competitive_replay.json (even for L1 conditional evidence), sources_used, scene_claims, premises, state/events, execution_report, unverified_claims and verdict. No public detailed private plot or full copied card texts. If evidence cannot substantiate a line, revise it or omit the technical assertion; preserve stakes and disclose scope.

## Cumulative protocol dependencies
- 08_CHAPTERS/PROTOCOL_REGISTRY.json
- 08_CHAPTERS/PROTOCOL_APPLICATION.md
- 08_CHAPTERS/PROTOCOL_COVERAGE_TEMPLATE.json

Resolve the live master register and apply every governing protocol cumulatively. Record private exact-version evidence, conditional applicability and real blockers; preserve approval, canon, scope and rights gates.
