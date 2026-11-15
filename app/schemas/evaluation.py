from typing import Literal
from pydantic import BaseModel, Field


class RubricCheck(BaseModel):
    status: Literal["PASS", "FAIL"] = Field(
        description="Must be either PASS or FAIL"
    )
    reason: str = Field(
        description="Explain why the lesson passed or failed"
    )


class EvaluationResult(BaseModel):
    accuracy: RubricCheck
    beginner_friendly: RubricCheck
    practical_examples: RubricCheck
    jargon_explanation: RubricCheck
    completeness: RubricCheck
    teaching_flow: RubricCheck
    feedback: list[str] = Field(
        description="Specific corrections required for failed checks"
    )