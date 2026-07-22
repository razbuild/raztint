"""
basic_usage.py RazTint quick-start examples.

Run:
    python examples/basic_usage.py
"""

from raztint import err, info, ok, paint, redact, warn

# Color and style via paint()
print(paint("Success! The operation completed.", color="green"))
print(paint("Critical Error: Database not found.", color="red"))
print(paint("Warning: Disk space is running low.", color="yellow"))
print(paint("Info: Connecting to remote host...", color="blue"))
print(paint("Pending: Waiting for worker...", color="cyan"))
print(paint("This is bold text.", styles="bold"))
print(paint("This is italic text.", styles="italic"))
print(paint("This is underlined text.", styles="underline"))

# Icons (auto-adapts: Nerd Font → Unicode → ASCII) 
print(f"{ok()} File saved successfully.")
print(f"{err()} Connection failed.")
print(f"{info()} Analysis in progress...")
print(f"{warn()} Disk space low.")

# paint() — color + style + icon in one call
print(paint("Done!", color="green", styles="bold"))
print(paint("Connection failed.", color="red", icon="err"))
print(paint("Alert", color="white", bg="red", styles=["bold", "underline"]))

# Intents — semantic presets
print(paint("Deployment complete.", intent="success"))
print(paint("Invalid credentials.", intent="danger"))
print(paint("Waiting for worker...", intent="pending"))
print(paint("Cache miss fetching from origin.", intent="debug"))

# Redaction
print(paint("password=supersecret api_key=ghp_abc123", intent="debug", redact=True))
print(redact("password=supersecret api_key=ghp_abc123"))
