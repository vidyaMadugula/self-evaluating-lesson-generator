
import json
from pathlib import Path

MEMORY_FILE = (
    Path(__file__).resolve().parents[2]
    / "memory"
    / "learning_memory.json"
)

# Improvement rules for recurring evaluation failures
IMPROVEMENT_RULES = {
    "accuracy": (
        "Ensure all explanations are factually correct. "
        "Do not make unsupported claims."
    ),
    
    "beginner_friendly": (
        "Use short sentences, simple English, and everyday comparisons. "
        "Do not assume technical knowledge."
    ),
    "practical_examples": (
        "Include at least one clear, realistic example and explain "
        "how it connects to the topic."
    ),
    "jargon_explanation": (
        "Explain every technical term in simple language when it first appears."
    ),
    "completeness": (
        "Cover what the topic is, why it is useful, and how it works."
    ),
    "teaching_flow": (
        "Arrange the lesson in a logical order, moving from basic concepts "
        "to explanations, examples, and summary."
    )
}


def load_learning_memory() -> dict:
    """Load persistent learning memory from JSON."""

    if not MEMORY_FILE.exists():
        return {
            "total_failed_evaluations": 0,
            "criteria": {}
        }

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {
            "total_failed_evaluations": 0,
            "criteria": {}
        }


def save_learning_memory(memory: dict) -> None:
    """Save learning memory to JSON."""

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4, ensure_ascii=False)


def record_failures(failed_checks: list) -> None:
    """Record failed evaluation criteria across application runs."""

    if not failed_checks:
        return

    memory = load_learning_memory()
    memory["total_failed_evaluations"] += 1

    for failure in failed_checks:
        criterion = failure["check"]
        reason = failure["reason"]

        if criterion not in memory["criteria"]:
            memory["criteria"][criterion] = {
                "failure_count": 0,
                "recent_reasons": [],
                "improvement_rule": IMPROVEMENT_RULES.get(
                    criterion,
                    "Improve this area in future lessons."
                )
            }

        criterion_memory = memory["criteria"][criterion]
        criterion_memory["failure_count"] += 1
        criterion_memory["recent_reasons"].append(reason)

        # Keep only the latest five reasons
        criterion_memory["recent_reasons"] = (
            criterion_memory["recent_reasons"][-5:]
        )

    save_learning_memory(memory)


def get_learning_guidelines() -> str:
    """Create guidelines from previously recorded failures."""

    memory = load_learning_memory()
    criteria = memory.get("criteria", {})

    if not criteria:
        return "No previous learning feedback is available."

    guidelines = []

    for criterion, details in criteria.items():
        count = details["failure_count"]
        rule = details["improvement_rule"]

        guidelines.append(
            f"- {criterion} (failed {count} times): {rule}"
        )

    return "\n".join(guidelines)
