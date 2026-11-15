
import app.graph as graph_module

evaluation_count = 0

def mock_evaluate_lesson(topic, lesson):
    global evaluation_count
    evaluation_count += 1

    checks = [
        "accuracy",
        "beginner_friendly",
        "practical_examples",
        "jargon_explanation",
        "completeness",
        "teaching_flow"
    ]

    result = {
        check: {
            "status": "PASS",
            "reason": "Check passed."
        }
        for check in checks
    }

    if evaluation_count == 1:
        result["practical_examples"] = {
            "status": "FAIL",
            "reason": "The lesson needs a clearer real-world example."
        }
        result["overall_result"] = "FAIL"
        result["failed_checks"] = [{
            "check": "practical_examples",
            "reason": "The lesson needs a clearer real-world example."
        }]
    else:
        result["overall_result"] = "PASS"
        result["failed_checks"] = []

    return result


# Replace the real evaluator temporarily for this test
graph_module.evaluate_lesson = mock_evaluate_lesson

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

result = graph_module.lesson_graph.invoke(initial_state)

print("\nRETRY TEST RESULTS")
print("=" * 40)
print("Final status:", result["final_status"])
print("Total regenerations:", result["retry_count"])
print("Evaluation calls:", evaluation_count)
print("Rejection log:", result["rejection_log"])
assert result["final_status"] == "PASS"
assert result["retry_count"] == 1
assert evaluation_count == 2

print("Retry test passed successfully!")
