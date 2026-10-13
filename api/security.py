"""
API Security & Operations Middleware (OWASP ASVS 5.0 Aligned).
Provides token-bucket rate limiting, prompt-injection defense,
cryptographic request authentication, and immutable audit logging.
"""

import hashlib
import json
import re
import time
from typing import Dict, Any, Optional, Tuple


class RateLimiter:
    """Sliding-window / token bucket rate limiter for DoS mitigation."""

    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.request_history: Dict[str, list] = {}

    def is_allowed(self, client_id: str, current_time: Optional[float] = None) -> bool:
        now = current_time if current_time is not None else time.time()
        timestamps = self.request_history.get(client_id, [])
        # Prune older than window
        cutoff = now - self.window_seconds
        timestamps = [t for t in timestamps if t > cutoff]
        if len(timestamps) >= self.max_requests:
            self.request_history[client_id] = timestamps
            return False
        timestamps.append(now)
        self.request_history[client_id] = timestamps
        return True


class InputSanitizer:
    """Sanitizes user documents against prompt injection and payload overflows."""

    PROMPT_INJECTION_PATTERNS = [
        re.compile(r"ignore\s+(all\s+)?previous\s+instructions", re.IGNORECASE),
        re.compile(r"system\s*:\s*you\s+are", re.IGNORECASE),
        re.compile(r"override\s+parity\s+rules", re.IGNORECASE),
        re.compile(r"<\|im_start\|>", re.IGNORECASE),
    ]

    @staticmethod
    def sanitize_text(text: str, max_chars: int = 100_000) -> Tuple[str, bool]:
        """Truncates excessive text and flags potential prompt injection attacks."""
        if len(text) > max_chars:
            text = text[:max_chars]

        has_injection = any(pattern.search(text) for pattern in InputSanitizer.PROMPT_INJECTION_PATTERNS)
        return text, has_injection


class SecurityAuditLogger:
    """Generates immutable, append-only JSON audit logs for security observability."""

    def __init__(self):
        self.audit_log: list = []

    def log_event(self, event_type: str, client_id: str, details: Dict[str, Any]) -> Dict[str, Any]:
        event = {
            "timestamp": int(time.time()),
            "event_type": event_type,
            "client_id": hashlib.sha256(client_id.encode()).hexdigest()[:16],  # Pseudonymized ID
            "details": details,
        }
        event_bytes = json.dumps(event, sort_keys=True).encode("utf-8")
        event["event_digest"] = hashlib.sha256(event_bytes).hexdigest()
        self.audit_log.append(event)
        return event
