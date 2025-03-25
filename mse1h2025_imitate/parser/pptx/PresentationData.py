from dataclasses import dataclass
from typing import List


@dataclass
class PresentationData:
    topic: str
    goalAndTasks: str
    author: str
    slidesTitles: List