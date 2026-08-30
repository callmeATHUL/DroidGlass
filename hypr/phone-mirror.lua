-- DroidGlass Hyprland Window Rules
-- scrcpy phone mirror: bare phone-shaped window, no chrome, rounded corners, dynamic opacity.
-- Append to ~/.config/hypr/hyprland.lua (Omarchy Lua config).

o.window({ class = "^scrcpy$", title = "droidglass" }, {
  float = true,
  border_size = 0,
  rounding = 16,
  no_shadow = false,
  shadow_range = 25,
  shadow_render_power = 3,
  opacity = "1.0 0.85", -- 1.0 when focused, 0.85 when unfocused
  pin = true,           -- Accessible across workspaces when summoned
  size = "380 820",     -- True phone aspect ratio
})

-- Animation curves for fluid sliding
o.animation("windowsIn", "1, 4, default, slide right")
o.animation("windowsOut", "1, 4, default, slide right")

-- Default Keybinds (bindings.lua):
-- o.bind("SUPER + SHIFT + P", "DroidGlass Mirror", "droidglass show")
-- o.bind("SUPER + SHIFT + N", "Clipboard to phone", "droidglass-clip")
