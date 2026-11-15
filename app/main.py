
import json
from pathlib import Path

from app.graph import lesson_graph


def main():
    initial_state = {
        "topic": "Introduction to RAG",
        "lesson": "",
        "evaluation": {},
        "feedback": [],
        "retry_count": 0,
        "max_retries": 2,
        "final_status": "",
        "rejection_log": []
    }

    print("\nStarting Self-Evaluating Lesson Generator...")

    result = lesson_graph.invoke(initial_state)

    # Create output directory
    output_dir = Path(__file__).resolve().parents[1] / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save final lesson
    (output_dir / "final_lesson.md").write_text(
        result["lesson"],
        encoding="utf-8"
    )

    # Save evaluation report
    evaluation_report = {
        "topic": result["topic"],
        "final_status": result["final_status"],
        "total_regenerations": result["retry_count"],
        "evaluation": result["evaluation"]
    }

    with open(
        output_dir / "evaluation_report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(evaluation_report, file, indent=4, ensure_ascii=False)

    # Save rejection log
    with open(
        output_dir / "rejection_log.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            result["rejection_log"],
            file,
            indent=4,
            ensure_ascii=False
        )

    print("\nOutput files saved successfully in:", output_dir)

    # Display results
    print("\n" + "=" * 50)
    print("FINAL RESULT")
    print("=" * 50)

    print("\nStatus:", result["final_status"])
    print("Total regenerations:", result["retry_count"])

    print("\nFinal lesson:")
    print(result["lesson"])

    print("\nFinal evaluation:")

    for criterion in [
        "accuracy",
        "beginner_friendly",
        "practical_examples",
        "jargon_explanation",
        "completeness",
        "teaching_flow"
    ]:
        check = result["evaluation"][criterion]
        print(f"\n{criterion}: {check['status']}")
        print("Reason:", check["reason"])

    print("\nRejection log:")
    print(result["rejection_log"])


if __name__ == "__main__":
    main()
