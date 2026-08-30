# LinkedIn post draft (post manually)

---

Apple shipped iPhone Mirroring with macOS Sequoia — your phone as a window on
your Mac, driven by mouse and keyboard, while the physical device stays dark.

I wanted that on Linux. So I built **DroidGlass** 🪟📱

Your Android phone appears on an Arch/Hyprland (Omarchy) desktop as a bare,
phone-shaped window — no title bar, no border. One click on a status-bar icon
summons or hides it. The phone's own screen stays off the whole time.

Under the hood:
• scrcpy for the low-latency mirror + input
• a Quickshell bar widget for the one-click toggle
• a Hyprland window rule that strips every pixel of chrome
• a `phone` CLI that auto-discovers the phone's wireless-adb IP when the
  network changes (cached IP → mesh VPN → parallel subnet scan)
• NetBird mesh VPN so it keeps working when laptop and phone are on
  different networks

It installs as an Omarchy plugin with one command:
`omarchy plugin add <repo-url> --enable`

The R&D doc in the repo maps every iPhone Mirroring capability against what's
possible with adb/scrcpy — notifications bridging and bidirectional clipboard
are next.

Repo: <link after publishing>

#linux #android #opensource #hyprland #omarchy #scrcpy #devtools

---

Notes for posting:
- Attach a short screen recording of the bar-icon toggle (omarchy capture) —
  motion sells this feature.
- Swap `<link after publishing>` for the GitHub URL.
