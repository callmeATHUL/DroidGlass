-- Hyprland Lua Configuration for bq-desktop-ai
-- Append to ~/.config/hypr/hyprland.lua (Omarchy Lua config).

-- Global Hotkeys for BigQuery AI SQL Assistant:
-- SUPER + ALT + B: Evaluate / Dry-Run SQL in Clipboard
-- SUPER + ALT + S: Open interactive SQL prompt in terminal
o.bind("SUPER + ALT + B", "Evaluate Clipboard SQL with BigQuery AI", "bq-ai-clip")
o.bind("SUPER + ALT + S", "Open BigQuery AI Prompt", "foot -T 'BigQuery AI' -e bq-ai sql 'SELECT 1'")

-- Window rules for interactive popups
o.window({ title = "^BigQuery AI$" }, {
  float = true,
  border_size = 2,
  rounding = 12,
  size = "800 600",
})
