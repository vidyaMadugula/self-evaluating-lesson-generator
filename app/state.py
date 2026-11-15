
from typing import TypedDict, Optional


class LessonState(TypedDict):
    topic: str
    lesson: str
    evaluation: dict
    feedback: list
    retry_count: int
    max_retries: int
    final_status: str
    rejection_log: list
