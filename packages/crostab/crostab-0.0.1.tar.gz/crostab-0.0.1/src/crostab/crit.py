from dataclasses import dataclass
from typing import Callable


@dataclass
class Crit:
    column: str
    crit: Callable[[object], bool]
