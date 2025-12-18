from dataclasses import dataclass
import os
from pathlib import Path

@dataclass(frozen=True)
class AppConfig:
    input_path: Path
    output_dir: Path

def load_config() -> AppConfig:
    input_path = Path(os.getenv("INPUT_PATH", "examples/sample_input.json"))
    output_dir = Path(os.getenv("OUTPUT_DIR", "output"))
    return AppConfig(input_path=input_path, output_dir=output_dir)
