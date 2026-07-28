"""
showcase.py

Full showcase of RazTint capabilities.

Demonstrates:
- foreground and background colors
- text styles
- combined formatting
- semantic intents
- icon rendering
- intent overrides
- multi-segment output with reset=False
- secret redaction
- runtime configuration inspection

Run:
    python examples/showcase.py
"""

from raztint import paint, tint

# Foreground colors
print("--- Foreground colors ---")
for color in (
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
    "gray",
    "bright_red",
    "bright_green",
    "bright_yellow",
    "bright_blue",
    "bright_magenta",
    "bright_cyan",
    "bright_white",
):
    print(paint(f"  {color}", color=color))

# Background colors
print("\n--- Background colors ---")
for bg in (
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
):
    print(paint(f"  {bg}", bg=bg))

# Text styles
print("\n--- Styles ---")
print(paint("  bold", styles="bold"))
print(paint("  dim", styles="dim"))
print(paint("  italic", styles="italic"))
print(paint("  underline", styles="underline"))
print(paint("  strikethrough", styles="strikethrough"))
print(paint("  bold + underline", styles=["bold", "underline"]))

# Color + background + style combined
print("\n--- Combined: color + bg + styles ---")
print(paint("  Highlighted warning", color="yellow", bg="black", styles="bold"))
print(paint("  Critical alert", color="white", bg="red", styles=["bold", "underline"]))

# Icons via paint()
print("\n--- Icons via paint() ---")
for icon in ("ok", "err", "warn", "info"):
    print(paint(f"  icon={icon}", color="cyan", icon=icon))

# Intents semantic presets
print("\n--- Intents ---")
for intent in ("success", "error", "warning", "info", "pending", "debug"):
    print(paint(f"  {intent}: operation result", intent=intent))  # type: ignore[arg-type]

# Intent overrides explicit arg always wins
print("\n--- Intent overrides ---")
print(paint("  success intent, cyan color", intent="success", color="cyan"))
print(paint("  error intent, no icon", intent="error", icon=None))
print(paint("  warning intent, bold style", intent="warning", styles="bold"))

# paint() with reset=False for multi-segment lines
print("\n--- Concatenation with reset=False ---")
label = paint("  WARNING:", color="yellow", styles="bold", reset=False)
detail = paint(" Disk usage above 90%", color="red")
print(label + detail)

# Redaction
print("\n--- Redaction via paint() ---")
raw = "Connecting with password=hunter2 to https://user:secret@db.internal"
print(paint(f"  {raw}", intent="debug", redact=True))

# Runtime state
print("\n--- Runtime state ---")
print(f"  use_color : {tint.use_color}")
print(f"  icon_mode : {tint.icon_mode}")
