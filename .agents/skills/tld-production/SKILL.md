---
name: tld-production
description: "Orchestrate The Last Draw chapter production, revisions and approved-chapter close-out directly in ChatGPT and GitHub. Use for write the next chapter, continue the novel, revise a chapter, or resume production."
---

# tld-production

Project scope: The Last Draw: A competitive TCG Novel (Teffa14/myriftnovel). Read current root AGENTS.md and live canonical sources before using this skill. This operational summary does not supersede them. Paths below are repository-root-relative, not relative to this SKILL.md.

## Required references
- AGENTS.md
- 08_CHAPTERS/CHATGPT_PRODUCTION.md
- 08_CHAPTERS/PROMPTS/MASTER_AUTHOR_PROTOCOL.md
- 08_CHAPTERS/PROMPTS/RECURSIVE_DISTILLATION_PROMPT.md
- 08_CHAPTERS/PROMPTS/FINAL_EXECUTION_PROMPT.md
- 08_CHAPTERS/CHAPTER_PRODUCTION_PLAYBOOK.md
- 08_CHAPTERS/PRODUCTION_STATUS.json
- 09_EDITORIAL_QA/EDITORIAL_SYSTEM.md

## Execution
1. Run tld-repository to resolve current HEAD and inspect the entire inventory, all applicable files and relevant archive members. Load the referenced canonical instructions in full; this skill routes them rather than replacing them.
2. Determine the real production state. If an explicitly approved version is not fully registered, run tld-closeout first. If an unapproved candidate awaits approval, revise or deliver it; do not start the next chapter. Resolve the latest authoritative archive from current status, never from remembered version numbers.
3. Run tld-continuity, then tld-chapter-planning. For technical content run tld-competitive-evidence, for shop or community scenes apply tld-prose's community rules. Select only necessary research mechanisms; invoke tld-source-distillation if new source ingestion is requested.
4. Draft the actual chapter using tld-prose, then tld-editorial-review and tld-originality. Repair defects and rerun affected checks on exact delivered bytes. Keep private artifacts outside public Git.
5. Deliver the complete candidate and separate report. Stop at explicit literary approval. Once approval is provided, tld-closeout locks and registers the exact version, checks the new archive and commits public-safe status via tld-repository.
6. If asked about publishing or income use tld-publication separately. Neither approval nor skill activation authorizes publication, monetization, or a contract.

## Required evidence and stop conditions
Return actual deliverables, source revision, private version/hash when appropriate, checks executed, evidence level and limitations. No Codex handoff, fake background activity, fabricated results, or asking the author to adjudicate rules. G3-global incompleteness is not a blanket blocker; narrow unsupported technical detail per G3-scene. Missing prior approved archive, unresolved material continuity/originality defects, and absent explicit approval are real gates. A skill invocation never changes approval status by itself.

AD-0017: load 02_STYLE_BIBLE/LITERARY_CRAFT_PROTOCOL.md and current author directives, canonical prompts and all governing protocols at intake. Record actual applicability or blockers; do not drop any earlier mandate. Route craft work through tld-prose, tld-editorial-review, tld-source-distillation when ingesting new evidence, and tld-originality/closeout. Preserve all existing gates.
