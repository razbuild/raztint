import pyperf

from raztint.security.masking import redact


def benchmark_masking_redaction_performance():
    # A dummy sensitive log trace structure
    sensitive_log = "ERROR: user_token='secret_abc123' password='my_password_99' failed connection stream."
    for _ in range(50):
        redact(sensitive_log)


if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.bench_func(
        "raztint_security_redaction", benchmark_masking_redaction_performance
    )
