# Bento Buddies 0.2.0 — ImageGen art update

Delivered APK: `/Users/xiu/Desktop/dev/game/bento-buddies/releases/Bento-Buddies-0.2.0-QA.apk`.
Package `com.bentobuddies.game.qa`, version 0.2.0 (2), Gradle Debug / Android Debug signed, arm64-v8a, min SDK 21, target SDK 36. This is a playable QA APK, not a store release.
SHA-256: `5d2b2b761ccc19803d111a3c2b1b393fa63f2dd9f1eda1c5ce5d81dc9647736b`.

Original ImageGen assets replace all button skins, action icons, backgrounds, logo, launcher icon, ingredient illustrations and three friend portraits. UI panels, wooden tray, pantry cards and scrapbook album use generated textures. Runtime Vietnamese labels and board geometry remain crisp; gameplay rules, levels, touch rectangles and save format are unchanged. Prompts: `IMAGEGEN_V2_PROMPTS.json`; atlas sources preserved, extraction recorded in `assets/resources/art/v2/atlas.json`.

Validation: TypeScript no-emit compile; 807 rule/content/save assertions including all 24 level solutions; Cocos export; offline Gradle build; APK signatures, alignment, package/version and offline permission inspection passed.

Physical device: Z2461 / P720F10, serial 323952558406, Android 15, portrait 900×2030, density 400, gesture navigation. Installed as an update without clearing data. Observed menu, level map, ordinary play, incomplete-board failure/retry, level 1 victory, onboarding/help, pause/Back, album, and music/SFX toggle controls. Replayed dense level 24 by touch; visually verified victory and independently compared persisted current board with level 24's exact authored solution. Verified restart preserves save and all 24 existing QA album entries. Checked home and dense solved layout at temporary 900×1600, restored native 900×2030. No clipped essential controls in reviewed images.

One initial automation run was invalidated because another game took foreground; discarded its dense-screen evidence and repeated with a foreground guard. Production Cocos export omits console gameplay messages, so a console-log assertion was unsuitable; acceptance uses reviewed win screenshots plus exact current-board persistence instead. The replay helper now checks current board before accepting an already-completed level, preventing old album entries from creating false positives.

Evidence: `artifacts/v2/device/` (home-final, play-empty, failed, level-01-win, dense-empty, dense-win, level-map, album, settings, short-home, short-dense, verified-result.json). Static inspection: `artifacts/v2/apk-inspection.txt`. Final cosmetic change only lowers the bear portrait by 20 design pixels; final APK install and gameplay smoke evidence use final-packed/final-win screenshots.

Limits: this update replays levels 1 and 24 rather than all 24 on-device (all 24 were played in the previous version and still pass automated validation). No new-user retention study, subjective speaker assessment, or sustained frame-time benchmark. Existing QA progression is retained; fresh unlock and destructive save-reset testing were not repeated for this art-only update.
