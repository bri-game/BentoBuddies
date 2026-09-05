#!/bin/bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
export ANDROID_SDK_ROOT=/Users/xiu/Library/Android/sdk
export ANDROID_HOME="$ANDROID_SDK_ROOT"
cd "$ROOT"
mkdir -p "$ROOT/artifacts" "$ROOT/releases"
npm test
set +e
/Applications/Cocos/Creator/3.8.8/CocosCreator.app/Contents/MacOS/CocosCreator --project "$ROOT" --build "configPath=$ROOT/build-configs/android-qa.json" > "$ROOT/artifacts/cocos-export.log" 2>&1
result=$?
set -e
if [ "$result" != 0 ] && [ "$result" != 36 ]; then exit "$result"; fi
if ! rg -q 'build Task.*Finished' "$ROOT/artifacts/cocos-export.log"; then exit 1; fi
cd "$ROOT/build/android-qa/proj"
./gradlew assembleDebug --offline --no-daemon --max-workers=6 > "$ROOT/artifacts/gradle.log" 2>&1
cd "$ROOT"
python3 tools/collect-apk.py
