__author__ = 'Hoyeung Wong'

from dataclasses import dataclass
from typing import Callable


@dataclass
class Curt:
    head: int or None
    tail: int or None
    abstract: Callable or None
