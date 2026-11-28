---
name: tld-continuity
description: "Retrieve and verify the authoritative private manuscript archive, track timeline, character knowledge, money, objects, relationships and obligations, and check provisional narrative changes before writing or approving The Last Draw."
---

# tld-continuity

Project scope: The Last Draw: A competitive TCG Novel (Teffa14/myriftnovel). Read current root AGENTS.md and live canonical sources before using this skill. This operational summary does not supersede them. Paths below are repository-root-relative, not relative to this SKILL.md.

## Required references
- 08_CHAPTERS/PRODUCTION_STATUS.json
- 02_STYLE_BIBLE/ORIGINALITY/STATUS.json
- 07_CONTINUITY/CANON.md
- 07_CONTINUITY/NARRATIVE_MEMORY_PROTOCOL.md
- 03_STORY_BIBLE/IDENTITY_AND_SETTING.md
- 03_STORY_BIBLE/WORLD.md
- 04_CHARACTERS/CHARACTER_SYSTEM.md
- 04_CHARACTERS/RELATIONSHIPS.md
- 05_PLOT_ARCHITECTURE/ARCS.md
- 05_PLOT_ARCHITECTURE/SUBPLOTS.md

## Preflight
Resolve the latest authoritative private archive and any required sidecar from current status and canon. Retrieve the exact Library entry, not an older archive or a guessed path. Materialize authorized bytes when needed, inspect safe ZIP paths, run the included tools/check_future.py --verify-only and tools/validate_continuity.py continuity_registry.json in their proper archive context. Verify manifest and all approved chapter hashes, including supplements. Do not assume missing history is empty or reconstruct a lost original.
Load relevant approved records and abstract usage summaries. Separate story time from publication order, occurrence from recollection, observation from belief, and established facts from proposals. Do not feed retired language into generation.

## Scene and candidate ledger
Track stable entity/event IDs, date/time/timezone and location, POV, who knows what and how, financial balances/transactions, possessions and deck ownership, clothes/injuries, work/travel schedules, personal motives, relationships, promises, memories, setups/payoffs and open questions. Keep unknowns unknown. Write provisional source-located deltas as the candidate develops.
Run structural validation and semantic review against relevant prior records. Check money arithmetic, dates, time feasibility, referential integrity, character knowledge, first meetings, state transitions, obligations and contradictions. Repair actual defects without silently retconning canon.
Do not promote provisional records until explicit author approval of exact bytes; hand off to tld-closeout.

## Output
Private preflight record, verified archive identity, relevant state constraints and candidate continuity_delta.json. Report real blockers if inaccessible; no public detailed state or spoilers. Structural pass is not semantic certification.

## Cumulative protocol dependencies
- 08_CHAPTERS/PROTOCOL_REGISTRY.json
- 08_CHAPTERS/PROTOCOL_APPLICATION.md
- 08_CHAPTERS/PROTOCOL_COVERAGE_TEMPLATE.json

Resolve the live master register and apply every governing protocol cumulatively. Record private exact-version evidence, conditional applicability and real blockers; preserve approval, canon, scope and rights gates.
