"""
basic_usage.py — RazTint quick-start examples.

Run:
    python examples/basic_usage.py
"""

from raztint import (
    blue,
    bold,
    cyan,
    err,
    green,
    info,
    italic,
    ok,
    paint,
    red,
    redact,
    underline,
    warn,
    yellow,
)

# ── Colors ────────────────────────────────────────────────────────────────────
print(green("Success! The operation completed."))
print(red("Critical Error: Database not found."))
print(yellow("Warning: Disk space is running low."))
print(blue("Info: Connecting to remote host..."))
print(cyan("Pending: Waiting for worker..."))

# ── Styles ────────────────────────────────────────────────────────────────────
print(bold("This is bold text."))
print(italic("This is italic text."))
print(underline("This is underlined text."))

# ── Icons (auto-adapts: Nerd Font → Unicode → ASCII) ─────────────────────────
print(f"{ok()} File saved successfully.")
print(f"{err()} Connection failed.")
print(f"{info()} Analysis in progress...")
print(f"{warn()} Disk space low.")

# ── paint() — color + style + icon in one call ───────────────────────────────
print(paint("Done!", color="green", styles="bold"))
print(paint("Connection failed.", color="red", icon="err"))
print(paint("Alert", color="white", bg="red", styles=["bold", "underline"]))

# ── Intents — semantic presets ────────────────────────────────────────────────
print(paint("Deployment complete.", intent="success"))
print(paint("Invalid credentials.", intent="danger"))
print(paint("Waiting for worker...", intent="pending"))
print(paint("Cache miss — fetching from origin.", intent="debug"))

# ── Redaction ─────────────────────────────────────────────────────────────────
print(paint("password=supersecret api_key=ghp_abc123", intent="debug", redact=True))
print(redact("password=supersecret api_key=ghp_abc123"))
