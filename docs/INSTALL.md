# DroidGlass Installation & Setup Guide

This guide walks you through installing and configuring DroidGlass on Omarchy (Arch Linux + Hyprland).

---

## 1. Prerequisites

Install required packages via `pacman`:

```bash
sudo pacman -S android-tools scrcpy jq curl libnotify
```

Optional (for Wayland clipboard integration):
```bash
sudo pacman -S wl-clipboard
```

---

## 2. Enable Wireless ADB on Your Phone

1. Connect your Android phone to your laptop via USB cable.
2. Enable **USB Debugging** in Android Developer Options.
3. Open a terminal and enable TCP/IP mode on port 5555:
   ```bash
   adb tcpip 5555
   ```
4. Unplug the USB cable. DroidGlass will now automatically discover and connect to your phone over Wi-Fi.

---

## 3. Install DroidGlass

### A. Install CLI Binaries
```bash
install -m755 bin/droidglass bin/droidglassd bin/droidglass-clip ~/.local/bin/
# Create compatibility links for 'phone' and 'phone-clip'
ln -sf ~/.local/bin/droidglass ~/.local/bin/phone
ln -sf ~/.local/bin/droidglass-clip ~/.local/bin/phone-clip
```

### B. Configure Hyprland Window Rules
Append the window rules and keybindings to your Hyprland configuration (or `~/.config/hypr/hyprland.lua`):

```bash
cat hypr/phone-mirror.lua >> ~/.config/hypr/hyprland.lua
hyprctl reload
```

### C. Install Omarchy Bar Widget
If using Omarchy Shell:
```bash
omarchy plugin add https://github.com/<your-username>/droidglass --enable
```

---

## 4. Environment Variables (Optional)

Configure in your shell profile (e.g., `~/.bashrc` or `~/.profile`):

```bash
export PHONE_SERIAL="XXXXXXXX"        # Specific USB serial if multiple devices
export PHONE_NETBIRD_IP="100.112.x.y" # Mesh IP for cross-network mirroring
export PHONE_NTFY_TOPIC="your-topic"  # ntfy.sh topic for notifications & clipboard
```

---

## 5. Starting the State Daemon

To enable automatic screen hand-off (mirror wakes when physical phone sleeps, mirror parks when physical phone wakes):

```bash
droidglass daemon start
```

To enable it on login, add `droidglass daemon start` to your Hyprland autostart execs (`hyprland.conf` or `autostart.lua`):
```lua
o.exec("droidglass daemon start")
```
