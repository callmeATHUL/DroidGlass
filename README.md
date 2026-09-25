# DroidGlass

State-aware wireless Android phone control, screen mirroring, and desktop AI companion for [Omarchy](https://omarchy.org/) (Arch + Hyprland), inspired by macOS Sequoia's iPhone Mirroring.

The phone appears as a borderless, floating window with rounded corners and drop shadows that stays dark while you drive it from your desktop.

---

## What's in DroidGlass

### 1. State-Aware Phone Mirroring
- **Auto Screen Hand-off (`droidglassd`)**: The desktop mirror automatically awakens when you lock your physical phone, and smoothly steps aside into a special workspace when you pick up and turn on your phone.
- **Unified `droidglass` CLI**: Command suite for mirror toggling, UI automation, notifications, and clipboard sharing (with `phone` alias).
- **Hyprland Aesthetics**: 16px corner rounding, window shadows, focused vs. unfocused opacity levels (`1.0` / `0.85`), and smooth slide animations.
- **Stateful Bar Widget (`DroidGlassWidget.qml`)**: Dynamic Quickshell status bar indicator.

### 2. BigQuery AI/ML Desktop Companion (`droidglass bq ...`)
- **Clipboard SQL Evaluator (`SUPER + ALT + B`)**: Highlight or copy any BigQuery query to test syntax and calculate estimated bytes billed via dry-run with desktop alerts.
- **In-Database ML Pipelines**: Parameterized templates and CLI generators for `AI.FORECAST`, `AI.DETECT_ANOMALIES`, `AI.CLASSIFY`, and `VECTOR_SEARCH`.
- **Query Explainer & Optimizer**: Spot unpartitioned queries and anti-patterns with AI optimization advice.

---

## Quick Install

See [docs/INSTALL.md](docs/INSTALL.md) and [docs/BQ_AI.md](docs/BQ_AI.md) for full instructions.

```bash
# 1. Install and enable the Omarchy plugin
omarchy plugin add https://github.com/callmeATHUL/DroidGlass --enable

# 2. Optional: install the CLI wrappers globally
install -m755 bin/droidglass bin/droidglassd bin/droidglass-clip bin/bq-ai ~/.local/bin/
ln -sf ~/.local/bin/droidglass ~/.local/bin/phone
ln -sf ~/.local/bin/droidglass-clip ~/.local/bin/phone-clip

# 3. Add Hyprland window rules & keybindings
cat hypr/phone-mirror.lua >> ~/.config/hypr/hyprland.lua
cat hypr/bq-ai.lua >> ~/.config/hypr/hyprland.lua
hyprctl reload

# 4. Start state daemon (optional)
droidglass daemon start
```

The plugin itself is self-contained: its bar widget calls the bundled CLI from
the installed plugin directory. The global CLI installation is only needed if
you want to call `droidglass` or the `phone` compatibility aliases directly
from a terminal or Hyprland keybinding.

## Removal

Disable and remove the plugin with Omarchy, then remove only the optional CLI
files if you installed them:

```bash
~/.config/omarchy/plugins/droidglass.mirror/bin/droidglass daemon stop
omarchy plugin disable droidglass.mirror
omarchy plugin remove droidglass.mirror --yes
rm -f ~/.local/bin/droidglass ~/.local/bin/droidglassd \
  ~/.local/bin/droidglass-clip ~/.local/bin/bq-ai \
  ~/.local/bin/phone ~/.local/bin/phone-clip
```

If you added the rules or keybindings manually, remove those DroidGlass lines
from your user-owned Hyprland configuration before reloading it. The plugin
does not modify user configuration automatically.

---

## CLI Usage

### Phone Control
```bash
droidglass mirror                 # Toggle scrcpy screen mirror
droidglass show                   # Toggle visibility between active workspace and special:phone
droidglass find                   # Auto-discover Wi-Fi ADB IP
droidglass shot [out.png]         # Take screenshot
droidglass notifs                 # Dump recent notifications
droidglass ai "<task>"            # One-shot AI phone automation
```

### BigQuery AI Companion
```bash
droidglass bq sql "<prompt>"      # Natural language to BigQuery SQL
droidglass bq explain "<query>"   # Explain & optimize SQL query
droidglass bq forecast --table .. # Time-series forecasting (AI.FORECAST)
droidglass bq anomaly --table ..  # Anomaly detection (AI.DETECT_ANOMALIES)
droidglass bq classify --table .. # Zero-shot text classification (AI.CLASSIFY)
droidglass bq search --table ..   # Real-time vector search (VECTOR_SEARCH)
droidglass bq clip                # Evaluate clipboard SQL
```

---

## Documentation

- [Architecture & Protocol Design](docs/ARCHITECTURE.md)
- [Installation Guide](docs/INSTALL.md)
- [BigQuery AI Reference](docs/BQ_AI.md)
- [Apple Continuity Research](docs/RESEARCH.md)
