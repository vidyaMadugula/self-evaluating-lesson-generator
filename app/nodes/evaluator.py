
from langchain_core.messages import SystemMessage, HumanMessage
import time

from app.llm import evaluator_llm as llm
from app.schemas.evaluation import EvaluationResult
from app.prompts.evaluator_prompt import EVALUATOR_PROMPT


def evaluate_lesson(topic: str, lesson: str) -> dict:
    start_time = time.time()
    print("\nEvaluation started...")

    evaluator = llm.with_structured_output(
        EvaluationResult,
        method="json_mode"
    )

    response = evaluator.invoke([
        SystemMessage(content=EVALUATOR_PROMPT),
        HumanMessage(content=f"""
Topic: {topic}

Evaluate this lesson:

{lesson}
""")
    ])

    print(
        f"\nEvaluation completed in "
        f"{time.time() - start_time:.2f} seconds"
    )

    result = response.model_dump()

    checks = [
        "accuracy",
        "beginner_friendly",
        "practical_examples",
        "jargon_explanation",
        "completeness",
        "teaching_flow"
    ]

    failed_checks = []

    for check in checks:
        if result[check]["status"] != "PASS":
            failed_checks.append({
                "check": check,
                "reason": result[check]["reason"]
            })

    result["overall_result"] = (
        "PASS" if not failed_checks else "FAIL"
    )

    result["failed_checks"] = failed_checks

    return result
