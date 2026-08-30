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
# 1. Install CLI tools
install -m755 bin/droidglass bin/droidglassd bin/droidglass-clip bin/bq-ai ~/.local/bin/
ln -sf ~/.local/bin/droidglass ~/.local/bin/phone
ln -sf ~/.local/bin/droidglass-clip ~/.local/bin/phone-clip

# 2. Add Hyprland window rules & keybindings
cat hypr/phone-mirror.lua >> ~/.config/hypr/hyprland.lua
cat hypr/bq-ai.lua >> ~/.config/hypr/hyprland.lua
hyprctl reload

# 3. Start state daemon
droidglass daemon start
```

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
