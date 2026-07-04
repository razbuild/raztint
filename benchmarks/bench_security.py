import pyperf
from raztint.security import Redactor

def benchmark_masking_redaction_performance():
    redactor = Redactor()
    # A dummy sensitive log trace structure
    sensitive_log = "ERROR: user_token='secret_abc123' password='my_password_99' failed connection stream."
    
    for _ in range(50):
        redactor.redact_credentials(sensitive_log)

if __name__ == "__main__":
    runner = pyperf.Runner()
    runner.bench_func("raztint_security_redaction", benchmark_masking_redaction_performance)
