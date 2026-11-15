# Self-Evaluating Lesson Content Generator

An AI-powered application that generates beginner-friendly educational lessons, evaluates their quality using a structured rubric, and regenerates content when it does not meet the required standards.

## Problem Statement

Large Language Models (LLMs) can generate educational content quickly, but the generated content may contain factual errors, unclear explanations, missing examples, or unsuitable language for beginners.

This project addresses that problem by implementing a self-evaluation workflow. Instead of accepting the first generated lesson, the application evaluates it against predefined quality criteria and attempts to improve it using evaluator feedback.

## Project Objectives

- Generate complete educational lessons using an LLM.
- Create content suitable for students who have completed 12th grade and have no technical background.
- Evaluate generated lessons using a structured evaluation rubric.
- Identify weaknesses and provide specific improvement feedback.
- Regenerate lessons when evaluation fails, subject to a maximum retry limit.
- Maintain persistent learning memory across application runs.
- Save the final lesson, evaluation report, and rejection history.

## Architecture

The application follows a workflow-based architecture using LangGraph.

```text
                 User Topic
                     |
                     v
              Lesson Generator
                     |
                     v
               AI Evaluator
                     |
                     v
              PASS or FAIL?
                 /       \
               PASS      FAIL
                |          |
                v          v
          Final Lesson   Check Retry Limit
                            |
                      +-----+-----+
                      |           |
                  Retry Left   Limit Reached
                      |           |
                      v           v
                  Regenerate   Final Failure
                      |
                      v
                  AI Evaluator
```

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application development |
| LangChain | LLM integration and structured interactions |
| LangGraph | Workflow orchestration and conditional routing |
| Pydantic | Structured evaluation output |
| Large Language Model | Lesson generation and evaluation |
| JSON | Persistent learning memory and evaluation logs |

## How It Works

### 1. Lesson Generation

The generator receives a topic and creates a complete lesson using a predefined prompt.

The generated lesson includes:

- Lesson title
- Learning objectives
- Topic explanation
- Importance and benefits
- Step-by-step working process
- Real-world examples
- Key terms and explanations
- Summary

The generator uses simple English, short sentences, and relatable examples.

### 2. Lesson Evaluation

The evaluator independently reviews the generated lesson against six criteria.

| Evaluation Criterion | Description |
|---|---|
| Accuracy | Checks whether the information is factually correct. |
| Beginner Friendliness | Checks whether the content is understandable to beginners. |
| Practical Examples | Checks whether relevant real-world examples are included. |
| Jargon Explanation | Checks whether technical terms are explained clearly. |
| Completeness | Checks whether the lesson covers what, why, and how. |
| Teaching Flow | Checks whether the lesson follows a logical sequence. |

Each criterion receives a PASS or FAIL result with an explanation.

The evaluator also provides specific feedback for failed criteria.

### 3. Retry and Regeneration

If the lesson fails evaluation:

1. The evaluator identifies the failed criteria.
2. Specific feedback is passed to the generator.
3. The generator creates an improved version.
4. The evaluator checks the regenerated lesson.
5. The workflow continues until the lesson passes or the retry limit is reached.

The application allows a maximum of two regeneration attempts.

### 4. Persistent Learning Memory

The application maintains persistent learning memory using a JSON file.

It stores:

- Total failed evaluations.
- Failure counts for individual criteria.
- Recent reasons for failures.
- Predefined improvement guidelines for each criterion.

During future generation runs, these guidelines are provided to the generator to help avoid previously identified weaknesses.

This allows feedback from earlier runs to influence subsequent lesson generation.

### 5. Output Generation

The application saves the following files inside the `outputs/` directory:

| File | Description |
|---|---|
| `final_lesson.md` | Final generated educational lesson. |
| `evaluation_report.json` | Final evaluation results and application status. |
| `rejection_log.json` | History of rejected attempts and their failed criteria. |

## Project Structure

```text
self-evaluating-lesson-generator/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── graph.py
│   ├── state.py
│   │
│   ├── nodes/
│   │   ├── generator.py
│   │   ├── evaluator.py
│   │   └── memory.py
│   │
│   ├── prompts/
│   │   ├── generator_prompt.py
│   │   └── evaluator_prompt.py
│   │
│   └── schemas/
│       └── evaluation.py
│
├── memory/
│   └── learning_memory.json
│
├── outputs/
│   ├── final_lesson.md
│   ├── evaluation_report.json
│   └── rejection_log.json
│
├── tests/
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### Prerequisites

- Python 3.10 or later.
- An API key for the configured LLM provider.
- Git.

### 1. Clone the Repository

```bash
git clone <your-github-repository-url>
cd self-evaluating-lesson-generator
```

### 2. Create a Virtual Environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root.

Add the API key and model configuration required by your LLM implementation.

Example:

```env
GOOGLE_API_KEY=your_api_key_here
```

Use the actual environment variable names expected by your application. Never commit API keys or secrets to GitHub.

### 5. Run the Application

```powershell
python -m app.main
```

The application generates a lesson, evaluates it, performs regeneration if necessary, and saves the results in the `outputs/` directory.

## Testing

The project includes tests for the evaluation and retry workflows.

Run the evaluator test:

```powershell
python -m app.test_evaluator
```

This test checks whether the evaluator can identify problems in an intentionally poor-quality lesson.

Run the retry test:

```powershell
python -m app.test_retry
```

This test verifies that the workflow can reject an initial lesson, pass feedback to the generator, and successfully complete after regeneration.

Run the main application:

```powershell
python -m app.main
```

This tests the complete generation and evaluation workflow.

## Example Evaluation Result

The application evaluates a lesson using the six predefined criteria.

Example:

```text
Final Status: PASS

Accuracy: PASS
Beginner Friendliness: PASS
Practical Examples: PASS
Jargon Explanation: PASS
Completeness: PASS
Teaching Flow: PASS

Total Regenerations: 0
```

If an evaluation fails, the application records the failed criteria and their explanations in the rejection log.

## Future Improvements

- Use an independent evaluator model to reduce shared-model evaluation bias.
- Add more detailed factual verification using trusted reference materials.
- Dynamically identify recurring failure patterns and generate new improvement guidelines.
- Add support for multiple educational topics and difficulty levels.
- Introduce automated evaluation datasets and regression testing.
- Improve evaluation consistency using human-reviewed benchmark lessons.

## Conclusion

The Self-Evaluating Lesson Content Generator demonstrates how LLMs can be combined with structured evaluation and workflow orchestration to improve generated educational content.

By integrating lesson generation, rubric-based evaluation, feedback-driven regeneration, and persistent learning memory, the application provides a practical approach to building more reliable AI-powered educational tools.