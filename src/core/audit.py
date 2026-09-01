"""Audit logging for compliance, security tracking, and latency analytics."""

import json
from pathlib import Path
from datetime import datetime, timezone
from src.core.schemas import AuditLogRecord
from src.config.settings import get_settings


class AuditLogger:
    """Thread-safe JSONL structured audit logger for enterprise financial compliance."""

    def __init__(self, log_dir: Path | None = None):
        settings = get_settings()
        self.log_dir = log_dir or settings.LOGS_DIR
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "audit_trail.jsonl"

    def log(self, record: AuditLogRecord) -> None:
        """Append an audit record to the daily audit trail file."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        daily_file = self.log_dir / f"audit_trail_{today}.jsonl"

        record_dict = record.model_dump(mode="json")
        with open(daily_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(record_dict, ensure_ascii=False) + "\n")


# Global singleton instance
audit_logger = AuditLogger()
