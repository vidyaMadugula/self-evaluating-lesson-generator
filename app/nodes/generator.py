
from langchain_core.messages import SystemMessage, HumanMessage
from app.llm import generator_llm as llm
from app.prompts.generator_prompt import GENERATOR_PROMPT
from app.nodes.memory import get_learning_guidelines


def generate_lesson(
    topic: str,
    feedback: list = None,
    previous_lesson: str = ""
) -> str:

    feedback_text = ""

    if feedback:
        feedback_text = f"""
        The previous lesson failed these checks:

        {feedback}

        Correct these specific problems in the new lesson.
        """

    learning_guidelines = get_learning_guidelines()

    human_prompt = f"""
    Topic: {topic}

    Previous evaluation feedback:
    {feedback_text}

    Learning guidelines from previous runs:
    {learning_guidelines}

    Previous lesson:
    {previous_lesson}

    Create the complete lesson now.
    """

    response = llm.invoke([
        SystemMessage(content=GENERATOR_PROMPT),
        HumanMessage(content=human_prompt)
    ])

    return response.content
