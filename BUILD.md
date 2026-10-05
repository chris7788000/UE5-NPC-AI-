# Build or update PocketDesk

The ready-to-install APK is supplied separately. These steps are for editing and rebuilding.

## Android Studio

1. Extract the project ZIP.
2. Open the **PocketDesk** project folder in Android Studio.
3. Use JDK 17. Install Android SDK Platform 35 and Build Tools 35.0.0.
4. Let Gradle sync. The wrapper uses Gradle 8.9 and the Android plugin uses 8.7.3.
5. Use **Build → Build APK(s)**, or run `./gradlew assembleDebug`.
6. The APK is in `app/build/outputs/apk/debug/`.

On Windows, use `gradlew.bat assembleDebug`.

No third-party runtime libraries are needed. The Gradle build has not been executed in this environment; the independent SDK build below was used for the delivered APK.

## Independent SDK build

The included `build_local.py` uses the SDK's AAPT2, D8, Zipalign, and APK signer directly.

```bash
python3 build_local.py --sdk /absolute/path/to/android-sdk --output /absolute/path/to/PocketDesk.apk
```

It requires Python 3, a Java 17 runtime with the `jdk.compiler` module, SDK Platform 35, and Build Tools 35.0.0. `--java` accepts the Java executable path. When a system Java installation needs extra shared-library search paths, supply those through `LD_LIBRARY_PATH`.

## Future updates

Keep `com.pocketdesk.app` as the application ID and keep the included personal signing certificate. Increase `versionCode` in `app/build.gradle` and the source manifest for each update. Keep the two version names in agreement. Using the same certificate allows Android to install an update over this APK and keep app data.

The personal certificate's alias is `pocketdesk`; its store and key password is `pocketdesk-local-build`. The key is included to make personal future builds reproducible. For a publicly distributed app, use your own private release signing workflow.

The saved-data format uses version `1`. If it changes, add a migration and backup migration rather than resetting the user's data. Photos and audio records are separate from the JSON document.

## Tests

```bash
node tests/core.test.cjs
```

The behavior test uses Happy DOM 20.0.8 and runs trusted project code in a simulated DOM:

```bash
npm install --no-save happy-dom@20.0.8
node tests/behavior.test.mjs
```

It verifies user actions and data, not rendered geometry or Android hardware behavior.

The optional Playwright test serves the assets and exercises UI flows and viewport sizing:

```bash
npm install --no-save playwright
npx playwright install chromium
python3 -m http.server 8765 --directory app/src/main/assets
```

In a second terminal, from the project folder:

```bash
mkdir -p qa
node tests/ui.test.cjs
```

`POCKETDESK_TEST_URL` can override the server URL and `POCKETDESK_BROWSER` can select a Chromium executable. This script was supplied but not completed here because Chromium could not start within the environment.

## Android smoke test

On a real phone or emulator, install the APK, open every tool, rotate the screen, open the keyboard on forms, import/export a backup, select photos/audio/files, try music seeking, review phone/message intents, and choose and restore the home app. Test the phone's alarm and timer apps for background alerts. Check audio pauses when the app becomes hidden and that notes survive closing and reopening.
