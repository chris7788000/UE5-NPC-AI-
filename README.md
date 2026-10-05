# PocketDesk

A small Android-style home and toolkit with simple English. Java 8 Android shell, local HTML/CSS/JavaScript interface, no runtime libraries or network permission.

The app can be opened normally or selected as Android's home app. It is an application, not an Android firmware image.

See `PocketDesk-Start.md` for the user's installation and feature guide. See `BUILD.md` for development.

## Structure

| Path | Purpose |
| --- | --- |
| `app/src/main/java/com/pocketdesk/app/MainActivity.java` | Local WebView host, Android intents, file picker, media copies, device details, native persistence. |
| `app/src/main/assets/index.html` | App shell and document security policy. |
| `app/src/main/assets/style.css` | Responsive layouts, themes, accessible sizes, and colours. |
| `app/src/main/assets/app.js` | Working home screen and toolkit. |
| `app/src/main/assets/core.js` | Safe calculator parser, validated state, URLs, dates, and time helpers. |
| `app/src/main/AndroidManifest.xml` | Launcher entry, optional home entry, and normal permissions. |
| `signing/pocketdesk-personal.p12` | Certificate used for this personal APK and later updates. |
| `tests/` | Core tests, DOM behavior tests, and Playwright layout test script. |
| `PocketDesk-Preview.html` | Standalone browser preview with the same interface. |

## Data and Android integration

The interface stores a versioned JSON document through a small Java bridge into app-private SharedPreferences. It has a 350 ms save delay while typing and flushes on navigation, page hiding, and Android pause. Failed saves produce a visible error. The Java bridge accepts documents only up to the app's configured bound. The interface cleans all restored state and rejects unsupported versions.

Photos and audio are kept as separate private files. Photo imports decode with sampling, apply EXIF orientation, and write JPEG copies. Audio imports stream into bounded private files. Recent external file selections retain only metadata and their selected content URI.

The WebView loads only a fixed local HTTPS origin. A local response handler serves an asset allowlist and validated media filenames, including byte-range audio responses. File access, content access, mixed content, new windows, and external WebView navigation are disabled. A Content Security Policy blocks external resources, inline app scripts, and connections. Websites are opened through the device's browser using HTTP(S) only.

Contacts, calendar entries, task lists, and notifications/reminders are not connected to system databases. The app opens the phone's existing contacts, calendar, alarm, timer, dialer, message, camera, and settings screens when requested. Calls and messages are reviewed in those apps. No direct call, SMS-send, broad storage, contacts-read, or camera permission is requested.

## Limits

The toolkit provides a local recent-tools list, not the OS task switcher. It does not implement a full notification shade, lock screen, app store, package installer, wallpaper manager for the real OS, or background music service. System settings shortcuts open Android's real screens. Background alarms and timers are delegated to the phone's Clock app.

Media playback and Android intents depend on installed phone apps and codecs. Installed applications are queried through the launcher-intent visibility declaration rather than broad package access. UI state has explicit record and size limits; media imports are limited to 120 items with a 100 MB per-audio-file bound.

## Validation

See `TESTING.md` for executed checks and outstanding real-device and visual checks. The standalone build compiled against Android API 35 and produced a verified APK signed for the supported Android 8+ range.
