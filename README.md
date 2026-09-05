# Bento Buddies

A warm, offline portrait Android packing puzzle in Vietnamese. Arrange food for Mơ the rabbit, Mật the bear and Cốm the frog, satisfy their preferences, then close the lid and save the bento in your picnic album.

## Current game: 0.3.0

- 108 levels across nine chapters, retaining the original 24 levels.
- Six rules: rice touches vegetables, ice avoids soup, strawberries touch the outer edge, marked cells require a specific food, locked pieces cannot rotate, and cookies stay inside the outer edge.
- Six board topology families, contextual tutorials, free undo/removal/reset, saved progress and an album.
- Original ImageGen backgrounds, button skins, icons, food, characters and logo; generated audio.
- No timer, ads, accounts, purchases or energy system.

## Open and validate

Open the project with **Cocos Creator 3.8.8**. Entry scene: `assets/scenes/Main.scene`.

The content tools use Node.js 26 (native TypeScript stripping and module hooks); no npm dependencies are required.

```sh
npm test
npm run content:generate
```

Tests validate all 108 solutions and reject geometric duplicates under rotation/reflection. An independent solver checks the campaign and pacing proxies. These checks do not claim unique solutions, optimal moves or human-calibrated difficulty. Generated reports go into the ignored `artifacts/` directory.

## Android QA build

Toolchain: JDK 17, Android SDK/API 36, build-tools 36.0.0, NDK 24.0.8215888 and CMake 3.22.1. Configure local toolchain paths in `build-configs/android-qa.json` and `tools/build-qa.sh` before building on another machine. The Gradle step runs offline and requires its dependencies to have been cached.

```sh
bash tools/build-qa.sh
```

QA package: `com.bentobuddies.game.qa`; version **0.3.0 (3)**; arm64-v8a; Android min 21 / target 36. The APK is debug-signed and is not store-ready. A separate store configuration reserves `com.bentobuddies.game`; no release key is included.

Build output is collected under `releases/` with SHA-256. APKs, engine caches, local device screenshots/logs and player-save fixtures are excluded from Git. Device scripts reference the original QA device and require adaptation and an authorized ADB connection before use.

## Design and evidence

- [108-level catalog](docs/LEVEL_CATALOG_108.md)
- [Campaign design and validation](docs/LEVELS_108.md)
- [QA report](docs/QA_CAMPAIGN_108.md)
- [Future development directions](docs/DEVELOPMENT_DIRECTIONS.md)
- [Art direction](docs/ART_V2.md) and [ImageGen prompts](docs/IMAGEGEN_V2_PROMPTS.json)

Historical reports refer to local APK/evidence paths that are not distributed in this repository. Physical QA used an Android 15 device, with original player progress restored after temporary test fixtures.
