---
name: omarchy-plugin-development
description: >-
  Guide and reference for developing, packaging, testing, and contributing Omarchy plugins
  and Quickshell bar widgets. Use when creating new Omarchy shell plugins, building QML widgets,
  validating manifests, or writing Hyprland Lua integration rules.
---

# Omarchy Plugin Development & Contribution Guide

Omarchy plugins extend the desktop shell (built on Quickshell + Hyprland) with status bar widgets, custom actions, and daemon integrations.

---

## 1. Plugin Manifest Schema (`manifest.json`)

Every plugin must have a `manifest.json` at its repository root:

```json
{
  "schemaVersion": 1,
  "id": "author.pluginname",
  "name": "Plugin Display Name",
  "version": "0.1.0",
  "author": "Author Name",
  "description": "Brief description of plugin capabilities",
  "kinds": [
    "bar-widget"
  ],
  "entryPoints": {
    "barWidget": "PluginWidget.qml"
  },
  "barWidget": {
    "displayName": "Plugin Display Name",
    "description": "Tooltip and settings description",
    "category": "Custom",
    "allowMultiple": false
  }
}
```

---

## 2. Quickshell Bar Widget Development (`.qml`)

Omarchy bar widgets are written in QtQuick / QML using Omarchy's design tokens:

```qml
import QtQuick
import Quickshell
import qs.Commons
import qs.Ui

BarWidget {
  id: root
  moduleName: "author.pluginname"

  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  // Custom reactive states
  property int stateCode: 0

  BarIconButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: root.stateCode === 1 ? "\uf10b" : "\uf3cd" // FontAwesome / Nerd Font icon
    slotSize: Style.bar.statusSlot
    fontSize: Style.font.caption
    tooltipText: "Widget Action Description"
    
    // Execute shell commands via Omarchy bar runtime
    onPressed: if (root.bar) root.bar.run("my-cli-command show")
  }
}
```

---

## 3. Hyprland Integration Rules (`hypr/rules.lua`)

Omarchy uses a Lua-based configuration layer (`~/.config/hypr/hyprland.lua`):

```lua
-- Floating Window Rules
o.window({ class = "^app_class$", title = "app_title" }, {
  float = true,
  border_size = 0,
  rounding = 16,
  no_shadow = false,
  shadow_range = 25,
  opacity = "1.0 0.85",
  pin = true,
})

-- Keybindings
o.bind("SUPER + SHIFT + X", "Action Description", "my-command action")
```

---

## 4. CLI Validation & Contribution Workflow

1. **Validate Plugin Structure**:
   ```bash
   omarchy plugin validate .
   ```
2. **Local Testing**:
   ```bash
   # Add directly from local path or git URL
   omarchy plugin add https://github.com/<user>/<repo> --enable
   ```
3. **Repository Conventions**:
   - `bin/`: CLI binaries and background daemons.
   - `hypr/`: Window rules and keybinding snippets.
   - `docs/`: Installation, Architecture, and Usage guides.
   - `manifest.json`: Root metadata.
