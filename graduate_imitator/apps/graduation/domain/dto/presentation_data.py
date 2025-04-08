from dataclasses import dataclass
from typing import List
from pydantic import BaseModel


class PresentationData(BaseModel):
    topic: str
    goalAndTasks: str
    author: str
    slidesTitles: List