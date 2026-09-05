# Bento Buddies 0.3.0 — 108-level campaign

APK: `/Users/xiu/Desktop/dev/game/bento-buddies/releases/Bento-Buddies-0.3.0-QA.apk`.
SHA-256: `ea5186204eb4b5fe0282c85c08a68717b1c8858abb6015bee712d41631203fcb`.
Package `com.bentobuddies.game.qa`, version 0.3.0 (3), arm64-v8a, Gradle Debug / Android Debug signed; min SDK 21, target SDK 36; 35,148,297 bytes. Playable QA APK, not store-ready.

## Scope

108 campaign levels, including 24 unchanged legacy levels and 84 new geometrically distinct additions. Three new mechanics: food-specific target cells, fixed orientation, and all cookie cells kept off the outside edge. Six board topology families, nine paginated chapters, remembered contextual rule tutorials, persistent target badges, fixed-piece feedback, expanded album/progression counts. Existing ImageGen artwork reused for consistent visual treatment.

## Automated validation

- TypeScript no-emit compilation passed.
- 6,396 assertions passed: schema/bounds, exact cover, connected pieces, rotation behavior, every stored solution, semantic and geometry-only D4 duplicate rejection, target/center independent checks, fixed orientation, failed-move atomicity, save corruption, old campaign migration, mechanic introductions and recovery beats.
- Independent deterministic search solved 108/108 within 100,000 nodes each; none capped. No uniqueness or optimal-move claim.
- Fifteen complete but rule-invalid witness boards found by relaxing a rule, demonstrating plausible wrong hypotheses.
- Generator screening enforces documented solver-based pacing proxies and verifies each new restriction can affect a complete arrangement. Human difficulty is not yet calibrated.
- Cocos export, offline Gradle build, signature verification, zip alignment, package/version and offline permission inspection passed. See `artifacts/v3/apk-inspection.txt`.

## Physical device evidence

Z2461 / P720F10, serial 323952558406, Android 15, native 900×2030, density 400, gesture navigation. Installed as an update; user save backed up before temporary QA fixtures and restored exactly after every pass. Temporary fixture copies affect only this game's SQLite save and are removed from device temporary storage afterward. Native resolution restored after short-screen checks.

The campaign pass entered full solutions by touch and observed saved wins for levels 25, 37, 49, 61, 78, 90, 102, 107 and 108. Levels 25/37/49/61 were first tested before final title/help-text refinements; the exact final APK was then installed and levels 78/90/102/107/108 replayed. Rule/content geometry is unchanged between those APKs. Final APK additionally tests fixed-piece drag, remove and undo on level 37.

Verified incomplete/wrong-rule feedback: complete wrong-food target packing at 25 and complete edge-touching cookie packing at 49 both fail without unlocking. Fixed rotation attempt at 37 leaves orientation zero while allowing movement. Verified legacy album retains 24 entries and unlocks 25, paginated maps through chapter 9, final 108 victory and album navigation, multi-rule help, and Android Back/reset during retries.

Screenshots under `artifacts/v3/device/`: `intro-25`, `intro-37`, `intro-49`, `wrong-rule-25`, `wrong-rule-49`, `fixed-rotation-feedback`, `packed-78`, `packed-90`, `combined-help`, `win-108`, `map-108`, `fixed-drag`, `fixed-undo`, `short-dense-97`, `short-four-rules-help`, `short-map`, `user-progress-restored`. A solved level-97 save fixture is used for short-screen layout inspection; this is not counted as a touch solution replay.

One initial dense-level assertion read persisted state before the latest placement was processed; the later screenshot already showed the correct piece. The QA harness now waits for the exact piece placement before proceeding. An initial short-screen capture ran before startup completed and showed the menu; it was discarded and repeated with startup/state verification. These failures are not counted as successful gameplay evidence.

## Limits

Representative physical replay, not 108 manual device completions. All 108 have independent automated solutions. One physical device with two aspect ratios; no broad hardware matrix, sustained frame-time benchmark, retention study or fresh-player difficulty calibration. No production signing/store submission. Existing user album, in-progress board, audio settings and progression are preserved rather than cleared for a destructive fresh-install test.

Follow-up design options are in `DEVELOPMENT_DIRECTIONS.md`; per-level catalog and solver metrics are in `LEVEL_CATALOG_108.md`.
