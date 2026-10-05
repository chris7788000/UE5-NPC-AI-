# Validation for PocketDesk 1.0

## Completed

- **55 core checks:** calculator precedence, percentages, decimals, negative numbers, scientific notation, rejected expressions, safe website URLs, dates, times, Monday-first month grids, durations, clean state, duplicate records, unsupported versions, invalid record identifiers, and prototype fields.
- **187 DOM behavior and bridge checks:** notes, pinning and colours, trash recovery, task completion and editing, calendar plans and edits, contact search, phone keypad, calculator history, stopwatch and laps, timer completion, bookmark validation, themes and text size, favourites, escaped text, global search, backup restoration, persistence, each tool's DOM at four viewport configurations, and every Android interface action through a controlled test double.
- **Java compile:** Java 8 bytecode from the Java 17 compiler, against Android SDK Platform 35, converted by D8 for minimum API 26.
- **APK assembly and signing:** AAPT2 resources and assets, aligned package, verified APK signature schemes v2 and v3. Android 8+ supports these signature schemes.
- **Manifest inspection:** correct package, version, Android 8 minimum, Android 15 target, launcher activity, optional home activity, and three normal permissions. No internet, direct call, direct SMS, broad file, contacts, or camera permission.
- **Package contents:** compiled Android manifest, resources, all four local interface assets, DEX classes, and signature records.

The executed behavior tests use Happy DOM, not a rendered browser or a real Android runtime. The Android helper calls were inspected through a test double; the Java code itself was compile checked. DOM viewport cases verify the component structure can render at those configurations, not the absence of visual clipping.

## Not completed here

- The supplied Playwright test could not start Chromium within the environment. There was no rendered browser screenshot review.
- No physical Android device or Android emulator was available for testing.
- The Gradle/Android Studio build path is included, but the delivered APK used the independent SDK build.
- Real file picker permissions, camera contracts, audio codecs and range playback, system Clock intents, default-home selection, window insets, keyboard resize, and Samsung-specific intent handlers need a real-device check.

## Recommended device checks

1. Install and open on the Galaxy A72; repeat on the tablet if desired.
2. Open every tool in dark and light themes and at all three text sizes.
3. Rotate the device and open the keyboard on every form.
4. Create a note, close and reopen the app, then restore that note from Trash.
5. Save and restore a backup containing English, German, and Korean text.
6. Import photos with rotation metadata, pick audio, test audio seeking, and remove only app-private copies.
7. Use file selection and export, then reopen a recently chosen file.
8. Review the dialer and message app with prefilled values. No call or message is sent by PocketDesk.
9. Set alarms and timers through the phone Clock app and verify its background behavior.
10. Choose PocketDesk as the home app, then restore One UI Home.
