from dataclasses import dataclass
from typing import Callable


@dataclass
class Aggreg:
    column: str
    stat: Callable[[list], float]
