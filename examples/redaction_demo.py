"""
redaction_demo.py

Showcase of RazTint secret masking capabilities.

Demonstrates:
- built-in redaction rules
- standalone redact()
- redaction during paint()
- URL credential masking
- token and key masking
- custom MaskRule definitions

Run:
    python examples/redaction_demo.py
"""

from raztint import DEFAULT_RULES, MaskRule, paint, redact


def section(title: str) -> None:
    print()
    print(f"--- {title} ---")


def main() -> None:
    section("Default rules")

    for rule in DEFAULT_RULES:
        print(f"{rule.name:<20} {rule.pattern}")

    section("Standalone redact()")

    raw = (
        "password=supersecret "
        "api_key=ghp_abc123xyz "
        "token=xoxb-123456789 "
        "url=https://admin:secret@db.internal"
    )

    print("Before:")
    print(raw)

    print("\nAfter:")
    print(redact(raw))

    section("Redaction with paint()")

    print(
        paint(
            "Authentication failed token=ghp_secret123456",
            intent="error",
            redact=True,
        )
    )

    print(
        paint(
            "Connecting to postgres://user:password@db.internal",
            intent="debug",
            redact=True,
        )
    )

    section("Custom rules")

    rules = [
        MaskRule(
            r"SECRET-\d+",
            "internal_secret",
            "SECRET-***",
        ),
        MaskRule(
            r"myapp_[A-Za-z0-9]{32}",
            "application_token",
            "myapp_****",
        ),
    ]

    custom = (
        "Deploying with SECRET-12345 and token=myapp_abcdefghijklmnopqrstuvwxyz123456"
    )

    print("Before:")
    print(custom)

    print("\nAfter:")
    print(redact(custom, rules=rules))

    print(
        "\n"
        + paint(
            "Custom redaction through paint() SECRET-999",
            intent="warning",
            redact=True,
            redact_rules=rules,
        )
    )


if __name__ == "__main__":
    main()
