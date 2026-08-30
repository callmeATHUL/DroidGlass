# DroidGlass

Wireless Android phone control and screen mirroring for [Omarchy](https://omarchy.org/)
(Arch + Hyprland), built on `adb` + `scrcpy` + a Quickshell bar widget.

The phone shows up as a bare, phone-shaped floating window — no title bar, no
border — that you can hide and summon from a status-bar icon. The physical
phone screen stays dark while you drive it from the laptop.

## Features

- **`phone` CLI** — one command for everything:
  - `phone mirror` — start/stop the scrcpy mirror (borderless, phone screen off,
    stays awake, screen powers off when you close it)
  - `phone show` — toggle mirror visibility: hides into a special workspace,
    summons it back on top; launches it if not running
  - `phone find` — auto-discover the phone's wifi-adb IP: cached IP → mesh VPN
    IP → parallel subnet scan of port 5555. No hardcoded IP; survives network hops.
  - `phone shot | tap | type | key | open | app | notifs | pull | push | battery | ping`
  - `phone notify <title> <msg>` — push a notification to the phone via ntfy.sh
  - `phone ai "<task>"` — hand the phone to `claude -p` for one-shot AI driving
- **Bar widget** (`omarchy-plugin/`) — a phone icon in the Omarchy/Quickshell bar;
  click = show/hide the mirror
- **Hyprland rule** (`hypr/phone-mirror.lua`) — floats the scrcpy window with
  zero border, light rounding, full opacity: it reads as a phone, not a window
- **`phone-clip`** — send the laptop clipboard to the phone as a tap-to-copy
  ntfy notification

## Requirements

`android-tools` (adb), `scrcpy`, `jq`, `curl`, a phone with wireless adb enabled
(`adb tcpip 5555` once over USB). Optional: a NetBird/Tailscale-style mesh so
adb works across networks — put the phone's mesh IP in `NETBIRD_IP` inside `bin/phone`.

## Install

The repo is a valid Omarchy shell plugin (`omarchy plugin validate .` passes),
so the bar widget installs straight from git:

```bash
omarchy plugin add https://github.com/<you>/droidglass --enable
```

Then the CLI and window rule:

```bash
install -m755 bin/phone bin/phone-clip ~/.local/bin/
cat hypr/phone-mirror.lua >> ~/.config/hypr/hyprland.lua && hyprctl reload
```

Configure via env (e.g. in `~/.profile`):

```bash
export PHONE_SERIAL=XXXXXXXX        # USB serial, optional (wifi works without it)
export PHONE_NTFY_TOPIC=your-topic  # ntfy.sh topic for notify / phone-clip
```

## Notes

- The scrcpy window class is plain `scrcpy` — the Hyprland rule matches `^scrcpy$`.
- `--turn-screen-off` can leave some devices (seen on a Moto MTK) in a doze state
  that ignores `adb input keyevent WAKEUP`; a physical power-button press clears it.
- Wireless adb IP changes with DHCP/network; `phone find` handles rediscovery.
