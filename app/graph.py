
from langgraph.graph import StateGraph, START, END
from app.nodes.memory import record_failures
from app.state import LessonState
from app.nodes.generator import generate_lesson
from app.nodes.evaluator import evaluate_lesson


def generator_node(state: LessonState):
    lesson = generate_lesson(
        topic=state["topic"],
        feedback=state.get("feedback", []),
        previous_lesson=state.get("lesson", "")
    )

    return {
        "lesson": lesson
    }


def evaluator_node(state: LessonState):
    evaluation = evaluate_lesson(
        topic=state["topic"],
        lesson=state["lesson"]
    )
    if evaluation["overall_result"] == "FAIL":
        record_failures(evaluation["failed_checks"])

    return {
        "evaluation": evaluation
    }


def route_after_evaluation(state: LessonState):
    if state["evaluation"]["overall_result"] == "PASS":
        return "success"

    if state["retry_count"] >= state["max_retries"]:
        return "failed"

    return "retry"


def retry_node(state: LessonState):
    failed_checks = state["evaluation"]["failed_checks"]

    return {
        "feedback": failed_checks,
        "retry_count": state["retry_count"] + 1,
        "rejection_log": state.get("rejection_log", []) + [
            {
                "attempt": state["retry_count"] + 1,
                "failed_checks": failed_checks
            }
        ]
    }


def success_node(state: LessonState):
    return {
        "final_status": "PASS"
    }


def failed_node(state: LessonState):
    return {
        "final_status": "FAIL"
    }


builder = StateGraph(LessonState)

builder.add_node("generator", generator_node)
builder.add_node("evaluator", evaluator_node)
builder.add_node("retry", retry_node)
builder.add_node("success", success_node)
builder.add_node("failed", failed_node)

builder.add_edge(START, "generator")
builder.add_edge("generator", "evaluator")

builder.add_conditional_edges(
    "evaluator",
    route_after_evaluation,
    {
        "success": "success",
        "retry": "retry",
        "failed": "failed"
    }
)

builder.add_edge("retry", "generator")
builder.add_edge("success", END)
builder.add_edge("failed", END)

lesson_graph = builder.compile()
