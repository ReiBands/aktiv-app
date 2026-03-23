"""
prompts.py
----------
Pure prompt-builder functions. No imports, no side effects, no API calls.
Each function returns a fully-formed prompt string ready for the OpenAI API.
"""


def build_evaluation_prompt(topic: str, explanation: str) -> str:
    return f"""Evaluate the user's explanation of the following topic: {topic}

User's explanation:
{explanation}

Your tasks:
- Identify what the user understood correctly
- Identify missing concepts or gaps
- Identify any incorrect reasoning

Output format — use exactly these three labeled sections with bullet points:

Correct understanding:
- ...

Gaps/missing:
- ...

Incorrect reasoning:
- ...

Constraints:
- Do NOT explain the topic in full
- Do NOT provide new teaching content
- Only evaluate what the user wrote
- Keep output concise and structured"""


def build_questions_prompt(topic: str, evaluation_text: str) -> str:
    return f"""Topic: {topic}

Evaluation of the user's prior explanation:
{evaluation_text}

Using ONLY the gaps identified in the evaluation above, generate exactly 2-3 active recall questions.

Constraints:
- Questions must require explanation, reasoning, or reconstruction of knowledge
- Do NOT generate yes/no questions
- Do NOT generate multiple choice questions
- Do NOT generate simple definition-only questions
- Each question must require at least 2-3 sentences to answer properly
- Each question must be on its own line and clearly separable

Output format:
- Numbered list only (1., 2., 3.)
- One question per line
- No preamble, no additional text, no explanation after the list"""


def build_critique_prompt(topic: str, questions: list, answers: list) -> str:
    formatted_qa = ""
    for i, (question, answer) in enumerate(zip(questions, answers), 1):
        formatted_qa += f"Q{i}: {question}\nUser's answer: {answer}\n\n"

    return f"""Topic: {topic}

Evaluate each of the following question-answer pairs.

{formatted_qa.strip()}

For EACH answer provide:
- What is correct
- What is incomplete or incorrect
- ONE concise corrective sentence

Constraints:
- Do NOT re-teach the full concept
- Do NOT introduce new information beyond correcting the answer
- Do NOT expand into explanations or mini-lessons
- Keep feedback direct and corrective

Output format — use exactly this structure for each:

Q1:
Correct: ...
Incomplete/Incorrect: ...
Corrective note: ...

Q2: [same structure]
[Q3 if applicable]"""
