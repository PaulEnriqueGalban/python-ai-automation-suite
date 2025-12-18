import time
from typing import Callable, TypeVar

T = TypeVar("T")

def retry(
    fn: Callable[[], T],
    *,
    attempts: int = 3,
    base_sleep_sec: float = 0.25,
    max_sleep_sec: float = 2.0,
    on_error: Callable[[Exception, int], None] | None = None,
) -> T:
    """Simple exponential backoff retry helper."""
    last_err: Exception | None = None
    for i in range(1, attempts + 1):
        try:
            return fn()
        except Exception as e:  # noqa: BLE001
            last_err = e
            if on_error:
                on_error(e, i)
            if i == attempts:
                break
            sleep = min(max_sleep_sec, base_sleep_sec * (2 ** (i - 1)))
            time.sleep(sleep)
    assert last_err is not None
    raise last_err
