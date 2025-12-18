from .config import load_config
from .workflow import run_workflow
from .logger import setup_logger

log = setup_logger("main")

def main() -> int:
    cfg = load_config()
    out = run_workflow(cfg.input_path, cfg.output_dir)
    log.info("Done. Output: %s", out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
