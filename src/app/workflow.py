import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import requests

from .logger import setup_logger
from .utils import retry

log = setup_logger("workflow")

@dataclass
class Report:
    job_id: str
    item_count: int
    total_duration_sec: int
    avg_duration_sec: float
    api_check_ok: bool

def _api_health_check(timeout_sec: float = 3.0) -> bool:
    r = requests.get("https://httpbin.org/status/200", timeout=timeout_sec)
    return r.status_code == 200

def run_workflow(input_path: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    data: dict[str, Any] = json.loads(Path(input_path).read_text(encoding="utf-8"))

    items = data.get("items", [])
    durations = [int(it.get("duration_sec", 0)) for it in items]
    total = sum(durations)
    avg = (total / len(durations)) if durations else 0.0

    api_ok = False
    try:
        api_ok = retry(
            _api_health_check,
            attempts=2,
            on_error=lambda e, i: log.warning("API check failed (attempt %s): %s", i, e),
        )
    except Exception:
        api_ok = False

    report = Report(
        job_id=str(data.get("job_id", "unknown")),
        item_count=len(items),
        total_duration_sec=total,
        avg_duration_sec=round(avg, 2),
        api_check_ok=bool(api_ok),
    )

    out_path = output_dir / "report.json"
    out_path.write_text(json.dumps(asdict(report), indent=2), encoding="utf-8")
    log.info("Wrote report: %s", out_path)
    return out_path
