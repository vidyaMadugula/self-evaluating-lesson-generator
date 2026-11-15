from app.nodes.evaluator import evaluate_lesson

bad_lesson = """
# Introduction to RAG

RAG is a programming language.
It is used only for creating websites.
RAG does not retrieve external information.
"""

result = evaluate_lesson(
    topic="Introduction to RAG",
    lesson=bad_lesson
)

print("\nEVALUATION RESULTS")
for check in [
    "accuracy",
    "beginner_friendly",
    "practical_examples",
    "jargon_explanation",
    "completeness",
    "teaching_flow"
]:
    print(check, ":", result[check])

print("\nOverall Result:", result["overall_result"])
print("Failed Checks:", result["failed_checks"])