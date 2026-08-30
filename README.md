# DroidGlass

State-aware wireless Android phone control and screen mirroring for [Omarchy](https://omarchy.org/) (Arch + Hyprland), inspired by macOS Sequoia's iPhone Mirroring.

The phone appears as a borderless, floating window with rounded corners and drop shadows that stays dark while you drive it from your desktop.

---

## What's New in v0.2.0

- **State-Aware Screen Hand-off (`droidglassd`)**: The desktop mirror automatically awakens when you lock your physical phone, and smoothly steps aside into a special workspace when you pick up and turn on your phone.
- **Unified `droidglass` CLI**: Comprehensive command suite for mirror toggling, UI automation, notifications, and clipboard sharing (with `phone` alias).
- **Refined Hyprland Aesthetics**: 16px corner rounding, window shadow, focused vs. unfocused opacity levels (`1.0` / `0.85`), and smooth slide animations.
- **Stateful Quickshell Widget**: Dynamic status bar indicator reflecting active mirroring vs. standby state.

---

## Features

- **`droidglass` CLI** (aliased to `phone`):
  - `droidglass mirror` — Start/stop the scrcpy mirror (screen stays off, awake on desktop).
  - `droidglass show` / `hide` — Toggle mirror between active workspace and `special:phone`.
  - `droidglass daemon {start|stop|status}` — Manage event-driven state hand-off daemon.
  - `droidglass find` — Auto-discover phone's Wi-Fi ADB IP (cache $\to$ NetBird mesh $\to$ parallel subnet scan).
  - `droidglass shot | tap | type | key | open | app | notifs | pull | push | battery | ping`
  - `droidglass notify <title> <msg>` — Push a notification to the phone via ntfy.sh.
  - `droidglass-clip [sync|watch]` — Synchronize clipboard between laptop and phone.
  - `droidglass ai "<task>"` — Hand phone control to an AI agent for one-shot automation.
- **Bar widget** (`DroidGlassWidget.qml`) — Status bar icon with click-to-summon toggle.
- **Hyprland rule** (`hypr/phone-mirror.lua`) — Floats the window with zero border, custom rounding, and smart opacity.

---

## Quick Install

See [docs/INSTALL.md](docs/INSTALL.md) for full instructions.

```bash
# 1. Install CLI tools
install -m755 bin/droidglass bin/droidglassd bin/droidglass-clip ~/.local/bin/
ln -sf ~/.local/bin/droidglass ~/.local/bin/phone
ln -sf ~/.local/bin/droidglass-clip ~/.local/bin/phone-clip

# 2. Add Hyprland window rules
cat hypr/phone-mirror.lua >> ~/.config/hypr/hyprland.lua && hyprctl reload

# 3. Start state daemon
droidglass daemon start
```

---

## Architecture & Design

Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/RESEARCH.md](docs/RESEARCH.md) for an in-depth breakdown of the event orchestration engine, protocol layers, and comparison with Apple's Continuity stack.
