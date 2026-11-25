# Gravity Field — source reconciliation and scoped rule review

Reviewed 2026-11-25; US English; reference date 2026-11-28 (future as of review, recheck if rules change).

## Printing identity and discrepancy
- RAD-062/167, Gravity Field, is a Radiance gear. The official card image in Riot's Radiance FAQ shows the blue Mind domain symbol, 5 energy and 1 Mind power. The historical 2026-10-26 catalog row lists Calm; preserve it as a historical snapshot, but do not use that domain value in current deck analysis. The gallery-derived RiftRef record also conflicts with the official image (Calm title metadata and Mind type metadata). This finding is specific to this printing, not a global reconciliation.
- Primary official image: https://cmsassets.rgpub.io/sanity/images/dsfx7636/news_live/6b24a87fcddcbb9539bfdffcca8f0d233dd03b22-1848x1063.jpg
- Official paired card image for Charm and Gravity Field: https://cmsassets.rgpub.io/sanity/images/dsfx7636/news_live/12770ca50524b1b352be11e092d81ce05da2125b-1848x1063.jpg
- Charm OGN-043/298 is a Calm spell with base cost 1 energy and 1 Calm power. The paired image and FAQ corroborate the movement effect. Neither card appears on the November 23 Standard ban list.
- FAQ (October 26): https://playriftbound.com/en-us/news/organizedplay/radiance-rules-faq-and-clarifications/
- Errata: https://playriftbound.com/en-us/news/announcements/radiance-errata-updates/ ; https://playriftbound.com/en-us/news/rules-and-releases/riftbound-origins-card-errata/ ; repository errata index has no entry for either name.
- Official Rules Hub (November 23): https://playriftbound.com/en-us/rules-hub/

## Scoped claims reviewed
1. If an otherwise permitted Standard Move into the opponent's Gravity Field is declined because of its extra movement charge, the attempted move is cancelled, including exhaustion. The unit remains in its original state.
2. A player resolving Charm to move an opposing unit into a battlefield containing that player's own Gravity Field does not impose the movement charge on the opponent. The spell's ordinary costs, target eligibility, timing, and any other restrictions still apply. The resulting combat is outside this check.

These are independent bounded rule applications (FAQ-GF-01 and FAQ-GF-02), not a new replay or a claim of full deck legality. Keep distinct the moving actor and the unit controller.

## Executed checks
In-session execution of current repository JS through a JS runtime with in-memory equivalents for Node file loading, console and assertions: test_scoring_check.js reported 10 passing conditional tests; autonomous_evidence.js --test reported 15 passing scoped tests. The date-specific pack returned 2 deck candidates, 40 price references and 9 tactical candidates. These tests do not validate every named card interaction; the Charm distinction was checked separately against the official FAQ and paired card image. No complete game simulation, global catalog reconciliation, independent judge certification, or manuscript approval claimed.

No manuscript, exact retired expressions, or private plot details included.
