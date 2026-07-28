"""
file_processor.py

A simulated file-processing CLI built with RazTint.

Demonstrates real-world usage patterns:
- staged CLI workflows
- status messages and progress reporting
- success, warning, and error output
- secret-safe logging with redaction
- processing summaries
- combining icons with semantic formatting

Run:
    python examples/file_processor.py
"""

import time

from raztint import err, info, ok, paint, warn


def header(text: str) -> None:
    print()
    print(paint(f"  {text}", color="bright_white", styles="bold"))
    print(paint("  " + "─" * len(text), color="gray"))


def step(label: str, detail: str = "") -> None:
    sep = f"  {detail}" if detail else ""
    print(f"  {paint(label, styles='dim')}{sep}")


def success(msg: str) -> None:
    print(f"  {ok()} {paint(msg, color='green')}")


def failure(msg: str) -> None:
    print(f"  {err()} {paint(msg, color='red', styles='bold')}")


def warning(msg: str) -> None:
    print(f"  {warn()} {paint(msg, color='yellow')}")


def status(msg: str) -> None:
    print(f"  {info()} {paint(msg, color='blue')}")


# Simulated processing logic

FILES = [
    {"name": "report_q1.csv", "size_kb": 128, "status": "ok"},
    {"name": "data_export.json", "size_kb": 2048, "status": "ok"},
    {"name": "corrupt_file.bin", "size_kb": 0, "status": "error"},
    {"name": "archive_2024.tar", "size_kb": 8192, "status": "ok"},
    {"name": "temp_upload.tmp", "size_kb": 512, "status": "warn"},
]

CONFIG = {
    "output_dir": "/tmp/processed",
    "api_key": "sk-abc123secret",  # will be redacted in logs
    "db_url": "postgres://user:pass@db.internal/prod",
}


def run() -> None:
    header("File Processor v1.0")
    status("Initialising…")

    # Log config do not include raw secrets in log payloads
    config_log = (
        f"output_dir={CONFIG['output_dir']}  api_key=[REDACTED]  db_url=[REDACTED]"
    )
    print(paint(f"     Config: {config_log}", intent="debug", redact=True, icon=None))
    time.sleep(0.2)

    header("Validating input files")
    validated, skipped = 0, 0

    for f in FILES:
        if f["size_kb"] == 0:
            failure(f"{f['name']}  - empty file, skipping")
            skipped += 1
        elif f["status"] == "warn":
            warning(f"{f['name']}  - unexpected extension (.tmp)")
            validated += 1
        else:
            step(f"{f['name']}", f"  {paint(str(f['size_kb']) + ' KB', styles='dim')}")
            validated += 1

    time.sleep(0.1)

    header("Processing")
    processed, errors = 0, 0

    for f in FILES:
        if f["size_kb"] == 0:
            continue
        time.sleep(0.05)
        if f["status"] == "error":
            failure(f"Failed to process {f['name']}")
            errors += 1
        else:
            success(f"Processed {f['name']}")
            processed += 1

    header("Summary")
    col_w = 20

    def row(label: str, value: str, color: str) -> None:
        print(f"  {label:<{col_w}}{paint(value, color=color, styles='bold')}")

    row("Files validated:", str(validated), "green")
    row("Files processed:", str(processed), "green")
    row("Skipped (empty):", str(skipped), "yellow")
    row("Errors:", str(errors), "red" if errors else "green")
    row("Output directory:", CONFIG["output_dir"], "cyan")

    print()
    if errors == 0:
        print(f"  {ok()} {paint('All files processed successfully.', styles='bold')}")
    else:
        msg = paint(f"{errors} file(s) failed — check logs above.", color="red")
        print(f"  {err()} {msg}")
    print()


if __name__ == "__main__":
    run()
