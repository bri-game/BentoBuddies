# Bento Buddies 0.1.0 — APK handoff

Status: playable QA APK, physically tested on Android. Not store-ready. Completed 2026-09-05.

## Exact delivered binary

- APK: `/Users/xiu/Desktop/dev/game/bento-buddies/releases/Bento-Buddies-0.1.0-QA.apk`
- SHA-256: `ce489a68d8e62d74729b1e06785a09bc21a963dc9994fd42080c6096dcd0a429`
- Size: 26,192,856 bytes (24.98 MiB).
- Package: `com.bentobuddies.game.qa`.
- Version: 0.1.0, versionCode 1.
- Variant: Gradle `assembleDebug`, optimized Cocos script export. Android Debug certificate, not release signing. Native socket inspector explicitly disabled in the local native bootstrap.
- ABI: arm64-v8a. Min SDK 21, target/compile SDK 36.
- Declared Android permissions: none. Offline permission inspection passed.
- APK signature verification v1/v2 and zipalign validation passed. Certificate SHA-256: `d7f58daf56eacb0b2080e9aea81f0c24cd65701bb99f5692294d2af2dc21ef6e`.

## Device and build

Physical Z2461 / P720F10, authorized serial 323952558406, Android 15, native 900×2030, density 400, gesture navigation mode 2. A temporary 900×1600 override was used to validate 16:9 and restored in a finally block. One physical device model tested; the second aspect ratio is not a second device.

Cocos Creator 3.8.8 export completed. Cocos CLI can exit 36 after successful export; current builder log reports completion and native Gradle assembly passed. JDK 17, SDK/build-tools 36, NDK 24.0.8215888, CMake 3.22.1. Dependencies resolved from the local Gradle cache with `--offline`.

## Automated gates

`npm test`: 807 checks passed, covering all 24 solutions, connected/nonoverlapping/in-bounds pieces, exact occupied area, actual puzzle structural uniqueness independent of authored arrangement, rotation equivalence, invalid-move atomicity, all three food rules, save corruption handling and validated unlocks. TypeScript no-emit check passed; skipLibCheck excludes known upstream Cocos declaration issues, not application source.

No exact-minimum or unique-solution claim. Difficulty wave labels are authored intent; retention and difficulty are not validated by a representative player sample.

## Physical interaction checks

| Scenario | Result | Evidence under artifacts/device |
|---|---|---|
| Exact APK install/update, launcher identity, cold launch | PASS | launcher.png, launch.png, package.txt |
| Vietnamese onboarding and help replay | PASS | tutorial-final.png, help-final.png |
| Drag from pantry into tray | PASS; egg at x2,y0 matched saved state | drag-result.png |
| Tap-select, rotate, tap-place | PASS across all 24 levels | level-01-packed.png, level-13-packed.png |
| Overlapping placement rejected without state mutation | PASS | overlap-rejected.png, save snapshots |
| Remove and undo, including return to empty board | PASS | removed.png, undo-restored.png |
| Incomplete serving and immediate retry | PASS | failure-final.png, retry.png |
| Full tray but ice touching soup rejected; no unlock | PASS; board retained for repair | cold-rule-failure.png, cold-invalid-highlight.png |
| Android Back, pause and confirmed reset | PASS after native key-dispatch fix | android-back-fixed.png, reset-confirm-final.png |
| Win, unlock and next-level transition | PASS, all 24 levels through real ADB touch input | final-state.json, level-24-win.png |
| Album stores actual arrangements; page navigation | PASS, 24 meals / 6 pages | album-final.png, album-page-two.png |
| Music and SFX switches, persisted across cold restart | PASS | settings-muted.png, settings-muted-persisted.png |
| Process force-stop/relaunch preserves album and settings | PASS, saved JSON compared | cold-relaunch.png |
| Home/background and resume | PASS, gameplay returns paused then continues | background-resume-paused.png, resumed-game.png |
| Densest level 24 and all combined rules | PASS | tall-dense-solved-final.png |
| 16:9 layout, touches, dense level solve and Back | PASS | short-16x9-dense-solved.png, short-16x9-pause.png |
| Physical resolution restored | PASS, 900×2030 | short-screen-qa.py finally block |
| Runtime crash scan after final pass | No fatal native/Java/JS signal in captured game-process log | gameplay-logcat.txt |

The final APK received replay coverage of all levels: 9–24 after the final native/UI correction, then 1–8 after a cold restart. Level 24 was also replayed at 16:9. Screenshots taken immediately after a gesture may show the preceding presentation frame; the final tall/short dense screenshots were captured after settling, and completion was independently checked against persisted album entries. SQLite checks poll for asynchronous storage flush rather than treating a stale read as failure.

## Issues found and fixed during QA

1. Offline debug build aborted while starting V8 inspector without network permission. Disabled inspector locally; did not add INTERNET permission.
2. Texture resource required `/texture` suffix; Sprite auto-size initially covered the home title. Corrected loading and explicit content size.
3. Multiline help shrank inside a single-line-height label. Label height now follows explicit line count.
4. Android Back did not reliably reach the game through the default Cocos key path. AppActivity now owns Back dispatch and the JS handler deduplicates it.
5. Dense tray shadow crowded the status message. Increased vertical separation; verified 16:9 and tall.

## Known gaps / delivery boundaries

- This is a 24-level offline QA build, not a release-signed Google Play submission. No store listing, AAB release or production key supplied.
- Daily challenges, food compression, dividers, live events, monetization and measured D1/D7 retention remain outside this delivery.
- One physical device/OS tested. The SurfaceFlinger latency query returned no usable frame history; no numerical FPS claim is made.
- Audio controls, saved state and Android playback activity were checked; subjective loudspeaker quality and onboarding comprehension need human playtesting.
- The connected phone is left at level 1 with the QA album/unlocks retained. A new install on a device without this package's data starts at level 1 with an empty album. No unrelated package was cleared or uninstalled.

## Sources and reproducibility

See README.md, docs/ACCEPTANCE.md, docs/CONTENT_REVIEW.md and docs/ART_PROVENANCE.md. Original cover illustration uses the built-in ImageGen tool and is saved at `assets/resources/art/picnic.png`; its exact prompt is in ART_PROVENANCE.md. Vector food/icon art and synthesized audio are project-owned reproducible code. Build and scoped device scripts are in tools/.
