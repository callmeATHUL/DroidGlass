# DroidGlass R&D — chasing macOS iPhone Mirroring on Linux

DroidGlass is an attempt to give Omarchy (Arch + Hyprland) the experience Apple
ships as **iPhone Mirroring** (macOS Sequoia 15 + iOS 18): your phone as a
first-class window on the desktop, driven by mouse/keyboard, while the physical
device stays locked and dark.

## What Apple ships (the benchmark)

Per Apple's documentation and hands-on coverage:

- Wireless mirror of the iPhone into a phone-shaped Mac window; the iPhone
  itself stays locked while being driven.
- Phone notifications and Live Activities land in the Mac's Notification
  Center (marked with an iPhone badge) even when the mirror window is closed,
  as long as the phone is on.
- Drag and drop of files/photos both directions between Mac and iPhone apps
  (added in macOS 15.1 / iOS 18.1).
- Requirements: Apple silicon or T2 Mac, iOS 18, same Apple ID with 2FA —
  a tightly coupled, single-vendor trust chain.

## What DroidGlass does today (v0.1)

| iPhone Mirroring capability | DroidGlass status | Mechanism |
| --- | --- | --- |
| Phone-shaped, chrome-less desktop window | ✅ | scrcpy `--window-borderless` + Hyprland rule (`^scrcpy$`: float, border 0, rounding, opaque) |
| Physical screen dark while driving | ✅ | scrcpy `--turn-screen-off --stay-awake --power-off-on-close` |
| Summon/dismiss from the desktop shell | ✅ | Quickshell bar widget → `phone show` (special-workspace park/summon) |
| Wireless, survives network hops | ✅ | wifi adb + IP autodiscovery (cache → mesh VPN IP → parallel subnet scan of :5555) |
| Works across networks (not just same wifi) | 🟡 | NetBird mesh: laptop side done, phone joins via NetBird app; `NETBIRD_IP` slot in the CLI |
| Phone notifications on desktop | 🟡 partial | `phone notifs` dumps them on demand; push channel exists via ntfy (used laptop→phone today, reversible) |
| Clipboard laptop → phone | ✅ | `phone-clip` via ntfy tap-to-copy |
| Clipboard phone → laptop | ❌ | scrcpy syncs Android→PC clipboard inside the mirror only |
| Drag & drop files both ways | ❌ | scrcpy supports drop-to-push (file → `/sdcard/Download`); no reverse drag |
| Device stays *locked* while driven | ❌ | adb control requires unlocked session; Apple does this below the lock layer |
| One-vendor trust pairing | n/a | our trust root is adb pairing + mesh VPN identity instead of Apple ID |

## Known gaps / bug log

- **Doze lockout (observed on moto g56 5G, Android 16, MTK):** after
  `--turn-screen-off`, the panel can enter a doze state where
  `input keyevent WAKEUP` reports `mWakefulness=Awake` yet `mScreenState=OFF`
  and screencaps come back black; only a physical power press recovers it.
  Mitigation candidates: drop `--turn-screen-off` on MTK devices, or issue
  `svc power stayon true` *before* screen-off and re-probe.
- **Leftover scrcpy virtual display:** a killed scrcpy session can leave a
  `Virtual display: "scrcpy"` in SurfaceFlinger that confuses default-display
  `screencap`. Clears when the server process dies.
- Widget click depends on `phone` being on the shell's PATH.

## Roadmap (parity order)

1. **Notification bridge** — persistent desktop notifications from the phone
   (Android side: ntfy or a notification-listener companion; desktop side:
   already have the ntfy→notify-send stream). Closes the biggest gap.
2. **Mesh-first transport** — prefer `NETBIRD_IP` automatically once the phone
   joins the mesh; drop the subnet scan to a fallback.
3. **Bidirectional clipboard** — poll scrcpy's clipboard sync + ntfy channel.
4. **Drag & drop** — scrcpy already accepts file drops (push to Download);
   surface it; investigate reverse direction via `adb pull` + a drop-out shelf.
5. **App-per-window** — scrcpy 3.x `--new-display` + `--start-app` can run a
   single Android app in its own desktop window (something Apple doesn't do).

## Sources

- [Apple Support — iPhone Mirroring: Use your iPhone from your Mac](https://support.apple.com/en-us/120421)
- [9to5Mac — Hands-on with iPhone Mirroring (iOS 18 / macOS Sequoia)](https://9to5mac.com/2024/06/25/hands-on-iphone-mirroring-with-ios-18-and-macos-sequoia-video/)
- [iDropNews — iPhone Mirroring gets drag and drop in iOS 18.1 / macOS 15.1](https://www.idropnews.com/news/iphone-mirroring-gets-drag-and-drop-in-latest-ios-181-and-macos-151-betas/223588/)
- [Intego — How to use iPhone Mirroring and iPhone Notifications on Mac](https://www.intego.com/mac-security-blog/how-to-use-iphone-mirroring-and-iphone-notifications-on-mac-and-why-you-should/)
