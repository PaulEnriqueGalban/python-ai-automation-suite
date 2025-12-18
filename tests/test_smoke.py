from pathlib import Path
import json
from src.app.workflow import run_workflow

def test_run_workflow_creates_report(tmp_path: Path) -> None:
    input_path = tmp_path / "input.json"
    input_path.write_text(json.dumps({"job_id": "t1", "items": [{"duration_sec": 5}, {"duration_sec": 10}]}))
    out_path = run_workflow(input_path, tmp_path / "out")
    assert out_path.exists()
    data = json.loads(out_path.read_text())
    assert data["job_id"] == "t1"
    assert data["item_count"] == 2
    assert data["total_duration_sec"] == 15
