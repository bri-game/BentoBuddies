# 108-box campaign acceptance

Player thesis: I found a thoughtful arrangement that satisfies several small wishes. Pressure comes from spatial reasoning, orientation and interacting placement constraints. No timers, lives or paid hints.

Preserve the first 24 levels byte-for-byte as level objects so existing albums remain valid. Add 84 reproducibly generated and curated levels, grouped into seven new 12-level chapters. Use an authored valid solution for every level; reject rotation/reflection/recolor duplicates. Avoid claiming unique solutions or human-calibrated difficulty.

New mechanics: target cells require the pictured food; ribbon-locked pieces cannot rotate but can move/remove/undo; cookies in center-rule levels must lie entirely away from the outside edge. Introduce each alone before combining. Vary rectangular dimensions, notches, interior obstacles and disconnected compartments. At most eight pieces, board at most 6×5 for phone readability.

Chapter plan: 1–12 first picnics; 13–24 familiar wishes; 25–36 named places; 37–48 fixed orientation; 49–60 protected cookies; 61–72 compartments; 73–84 coordinated wishes; 85–96 constrained packing; 97–108 mastery picnic. New chapters follow introduce/vary/combine/pressure/mastery/recovery beats rather than monotonic size growth. Mechanics are remembered and taught contextually; help lists precise current rules.

Gates: independent placement replay and all-rule evaluation for all 108; exact area/connectivity/bounds/schema; geometric novelty; teach-before-combine; planned recovery beats; old-save migration opens level 25 for completed old campaign; paged level map/album; Android original/new rules and dense layouts; preserve ImageGen visual language with existing generated lock, food, star and panel assets.

## Implemented validation and pacing

Final content contains 108 levels and 84 new packing geometries, with 11 rectangular boards, 24 notches, 18 stair-shaped exclusions, 17 corner exclusions, 7 interior holes and 7 split boards among the additions. Coverage across the campaign: rice 47, cold 44, edge 30, target 43, fixed 29, center 33. All additions have distinct geometry even when rule labels, food colors and fixed-orientation flags are removed before D4 fingerprinting.

The generator screens candidates with an independent deterministic placement search. New introduction/recovery beats require at most 45 search nodes; pressure beats require at least 30 in the first three new chapters and 100 later; mastery beats require at least 80 early and 300 later. These are reproducible design proxies, not claims about human completion time. Every new target/fixed/center restriction must admit a geometrically complete wrong arrangement when that restriction is relaxed, so the restriction is not merely decorative.

`npm test` runs 6,396 rule, schema, geometry, solution, atomic-move and migration checks, then independently solves all 108 boards and records 15 wrong-hypothesis witnesses. No unique-solution or optimal-move claims are made. `tools/base-levels-24.json` freezes legacy content; `tools/generate-levels.mjs` reproduces the campaign. Detailed per-level metrics are in `LEVEL_CATALOG_108.md` and `artifacts/v3/campaign-analysis.json`.
