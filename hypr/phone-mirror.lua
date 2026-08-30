-- scrcpy phone mirror: bare phone-shaped window, no chrome, fully opaque.
-- Append to ~/.config/hypr/hyprland.lua (Omarchy Lua config).
o.window({ class = "^scrcpy$" }, {
  float = true,
  border_size = 0,
  no_shadow = true,
  rounding = 14,
  opacity = "1.0 1.0",
  tag = "-default-opacity",
})

-- Optional keybinds (bindings.lua):
-- o.bind("SUPER + SHIFT + P", "Phone mirror", "phone show")
-- o.bind("SUPER + SHIFT + N", "Clipboard to phone", "phone-clip")
