# DroidGlass Architecture & System Design

DroidGlass bridges Android devices into Omarchy (Arch Linux + Hyprland) with an experience modeled after Apple’s macOS Sequoia iPhone Mirroring.

---

## 1. High-Level System Overview

```
+-----------------------------------------------------------------------------------+
|                              Omarchy (Arch + Hyprland)                             |
|                                                                                   |
|  [Quickshell Bar Widget] <-> [droidglass CLI] <-> [droidglassd State Daemon]       |
|                                                          │                        |
|                                                          │ Hyprland IPC Dispatch  |
|                                                          ▼                        |
|  [scrcpy Floating Window] <───────────────────── [special:phone Workspace]        |
+-----------------------------------------------------------------------------------+
                                         │  ADB over Wi-Fi / NetBird Mesh
                                         │  Event Logcat Stream
                                         ▼
+-----------------------------------------------------------------------------------+
|                              Physical Android Device                              |
|  [Screen Off / Idle] <──────────────────────────> [User Pick Up / Screen On]      |
+-----------------------------------------------------------------------------------+
```

---

## 2. Core Subsystems

### A. State-Aware Hand-off Engine (`droidglassd`)
* **Event Listening**: Directly taps into Android's event log stream via `adb shell logcat -b events -v raw` to receive broadcast intents (`SCREEN_ON`, `SCREEN_OFF`, `screen_toggled`) in real time with zero battery-draining polling.
* **Hyprland Window Management**:
  - `SCREEN_OFF`: Automatically summons the `scrcpy` mirror to the active workspace and focuses it.
  - `SCREEN_ON`: Silently parks the `scrcpy` window into `special:phone`, yielding control back to the physical device.

### B. Wireless Autodiscovery & Multi-Network Transport
1. **Cache Layer**: Checks `$XDG_CACHE_HOME/droidglass-wifi-ip` for sub-second reconnection.
2. **Mesh VPN Layer**: Supports NetBird/Tailscale mesh IP (`PHONE_NETBIRD_IP`) to connect across remote networks.
3. **Subnet Probing**: Performs parallel background socket scans on port `5555` across the local `/24` subnet.

### C. Seamless Windowing (Hyprland Lua Integration)
* **Borderless Aesthetics**: Target `^scrcpy$` with `border_size = 0`, `rounding = 16`, and drop shadows.
* **Dynamic Opacity**: `1.0` when focused on the phone; subtle `0.85` opacity when focused on code or browser.
* **Special Workspace Park**: Uses `special:phone` workspace as a parking shelf for immediate summon/dismiss.

### D. Clipboard & Notification Forwarding
* **Clipboard Sync**: `droidglass-clip` coordinates copy/paste across Wayland (`wl-paste`/`wl-copy`) and Android via ntfy.sh or ADB broadcast.
* **Desktop Notifications**: `droidglassd` parses incoming notification events and emits desktop notifications via `notify-send`.

---

## 3. Comparison with Apple Continuity

| Capability | Apple iPhone Mirroring (macOS 15) | DroidGlass (Omarchy + Android) |
| :--- | :--- | :--- |
| **Transport** | AWDL (Apple Wireless Direct Link) | Wi-Fi ADB + NetBird Mesh VPN |
| **Screen Off Mirroring** | Compositor Virtual Output | `scrcpy --turn-screen-off` |
| **State-Aware Hand-off** | Built-in OS subsystem | `droidglassd` logcat event daemon |
| **Summon / Dismiss** | Dock / Notification click | `special:phone` workspace toggle / Bar widget |
| **Multi-Network Support** | Proximity only (BLE + AWDL) | Works anywhere over VPN/Mesh |
| **AI Automation** | Siri / Apple Intelligence | `droidglass ai "<prompt>"` via LLM |
