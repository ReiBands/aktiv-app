"""
app.py
------
Main Streamlit application. Owns all UI rendering and stage-gate logic.
No prompt strings. No API logic. No business logic.
All state lives in st.session_state.
"""

import streamlit as st
from prompts import (
    build_evaluation_prompt,
    build_questions_prompt,
    build_critique_prompt,
)
from openai_client import get_completion

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Aktiv — Structured Learning",
    page_icon="🧠",
    layout="centered",
)

# ─────────────────────────────────────────────
# CUSTOM CSS — Clean academic aesthetic
# No chat UI. Form-based, structured, intentional.
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #F7F5F0;
    color: #1a1a1a;
}

h1, h2, h3 {
    font-family: 'DM Serif Display', serif;
    color: #1a1a1a;
}

.stage-header {
    font-family: 'DM Serif Display', serif;
    font-size: 1.6rem;
    margin-bottom: 0.2rem;
    color: #1a1a1a;
}

.stage-sub {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 1.5rem;
    font-weight: 300;
}

.constraint-notice {
    background: #FFF8E7;
    border-left: 3px solid #C9A84C;
    padding: 0.75rem 1rem;
    border-radius: 0 6px 6px 0;
    font-size: 0.88rem;
    color: #5a4a1a;
    margin-bottom: 1.2rem;
}

.eval-block {
    background: #FFFFFF;
    border: 1px solid #E0DDD6;
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}

.eval-block h4 {
    font-family: 'DM Serif Display', serif;
    font-size: 1rem;
    margin-bottom: 0.4rem;
    color: #1a1a1a;
}

.section-label {
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #888;
    margin-bottom: 0.5rem;
}

.data-notice {
    font-size: 0.8rem;
    color: #999;
    text-align: center;
    margin-top: 2rem;
    border-top: 1px solid #E0DDD6;
    padding-top: 1rem;
}

.progress-indicator {
    font-size: 0.75rem;
    color: #aaa;
    text-align: right;
    margin-bottom: 1.5rem;
    letter-spacing: 0.05em;
}

.stTextArea textarea {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem;
    background: #FFFFFF;
    border: 1px solid #D0CCC4;
    border-radius: 6px;
}

.stButton > button {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    background-color: #1a1a1a;
    color: #F7F5F0;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1.5rem;
    transition: background 0.2s;
}

.stButton > button:hover {
    background-color: #333;
    color: #F7F5F0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE INITIALIZATION
# All keys initialized explicitly with defaults.
# ─────────────────────────────────────────────
defaults = {
    "stage": 0,
    "topic": "",
    "prior_explanation": "",
    "evaluation_text": "",
    "recall_questions": [],
    "user_answers": [],
    "critique_text": "",
    "acknowledged": False,
    "reflection_clear": "",
    "reflection_unclear": "",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def parse_questions(raw: str) -> list:
    """
    Parse numbered questions from AI output.
    Keeps only lines starting with a digit and period (1., 2., 3.).
    Returns clean question strings stripped of leading number.
    """
    lines = raw.strip().split("\n")
    questions = []
    for line in lines:
        line = line.strip()
        if line and len(line) > 2 and line[0].isdigit() and line[1] == ".":
            question = line[2:].strip()
            if question:
                questions.append(question)
    return questions


def is_error_response(text: str) -> bool:
    """Check if the AI returned a fallback error string."""
    return text.startswith("Error generating response") or \
           text.startswith("API key not configured")


def reset_session():
    """Explicitly reset every session_state key to its default value."""
    st.session_state.stage = 0
    st.session_state.topic = ""
    st.session_state.prior_explanation = ""
    st.session_state.evaluation_text = ""
    st.session_state.recall_questions = []
    st.session_state.user_answers = []
    st.session_state.critique_text = ""
    st.session_state.acknowledged = False
    st.session_state.reflection_clear = ""
    st.session_state.reflection_unclear = ""


def show_progress(current: int, total: int = 5):
    stages = ["Topic", "Prior Knowledge", "Recall", "Feedback", "Reflection", "Complete"]
    st.markdown(
        f'<div class="progress-indicator">Step {current + 1} of {total + 1} — {stages[current]}</div>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
# APP HEADER
# ─────────────────────────────────────────────
st.markdown("# Aktiv")
st.markdown(
    '<div class="stage-sub">A structured learning system that enforces active recall before feedback.</div>',
    unsafe_allow_html=True
)
st.markdown("---")


# ─────────────────────────────────────────────
# STAGE 0 — TOPIC ENTRY
# ─────────────────────────────────────────────
if st.session_state.stage == 0:
    show_progress(0)
    st.markdown('<div class="stage-header">What do you want to study?</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="stage-sub">Enter a topic, concept, or paste study material below.</div>',
        unsafe_allow_html=True
    )

    topic_input = st.text_input(
        "Topic or study material",
        placeholder="e.g. The causes of World War I, Photosynthesis, Newton's Laws...",
        label_visibility="collapsed"
    )

    if st.button("Begin →", key="stage0_submit"):
        if not topic_input.strip():
            st.warning("Please enter a topic before continuing.")
        else:
            st.session_state.topic = topic_input.strip()
            st.session_state.stage = 1
            st.rerun()


# ─────────────────────────────────────────────
# STAGE 1 — PRIOR KNOWLEDGE
# ─────────────────────────────────────────────
elif st.session_state.stage == 1:
    show_progress(1)
    st.markdown('<div class="stage-header">What do you already know?</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="stage-sub">Topic: <strong>{st.session_state.topic}</strong></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="constraint-notice">'
        '🔒 <strong>You must attempt this before the system provides any feedback.</strong> '
        'No AI output will appear until you submit your explanation.'
        '</div>',
        unsafe_allow_html=True
    )

    explanation = st.text_area(
        "Before any feedback appears, write everything you already know about this topic.",
        height=200,
        placeholder="Write your explanation here. Be as thorough as you can — this is what the system will evaluate.",
        key="explanation_input"
    )

    if st.button("Submit Explanation →", key="stage1_submit"):
        if len(explanation.strip()) < 50:
            # P6: clear inline warning on validation failure
            st.warning(
                f"Your explanation is too short ({len(explanation.strip())} characters). "
                "Please write at least 50 characters before continuing."
            )
        else:
            st.session_state.prior_explanation = explanation.strip()

            with st.spinner("Evaluating your explanation..."):
                # AI Call #1 — Evaluation
                eval_prompt = build_evaluation_prompt(
                    st.session_state.topic,
                    st.session_state.prior_explanation
                )
                evaluation_text = get_completion(eval_prompt)

                if is_error_response(evaluation_text):
                    st.error(evaluation_text)
                    st.stop()

                st.session_state.evaluation_text = evaluation_text

                # AI Call #2 — Questions (chained from evaluation output)
                questions_prompt = build_questions_prompt(
                    st.session_state.topic,
                    st.session_state.evaluation_text
                )
                raw_questions = get_completion(questions_prompt)

                if is_error_response(raw_questions):
                    st.error(raw_questions)
                    st.stop()

                parsed = parse_questions(raw_questions)

                if not parsed:
                    st.error("Could not parse recall questions. Please try again.")
                    st.stop()

                st.session_state.recall_questions = parsed

            st.session_state.stage = 2
            st.rerun()


# ─────────────────────────────────────────────
# STAGE 2 — QUESTIONS + ANSWERS
# ─────────────────────────────────────────────
elif st.session_state.stage == 2:
    show_progress(2)
    st.markdown('<div class="stage-header">Your Evaluation</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="stage-sub">Here is how the system assessed your prior explanation.</div>',
        unsafe_allow_html=True
    )

    # Display evaluation output
    with st.container():
        st.markdown(
            f'<div class="eval-block">{st.session_state.evaluation_text}</div>',
            unsafe_allow_html=True
        )

    # P3: Mandatory visual separator between evaluation and questions
    st.divider()

    st.markdown('<div class="stage-header">Active Recall Questions</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="stage-sub">These questions target the gaps in your explanation. '
        'Answer each one fully — aim for at least 2–3 sentences per answer.</div>',
        unsafe_allow_html=True
    )

    answers = []
    for i, question in enumerate(st.session_state.recall_questions, 1):
        st.markdown(f'<div class="section-label">Question {i} (based on gaps in your explanation)</div>', unsafe_allow_html=True)
        st.markdown(f"**{question}**")
        answer = st.text_area(
            f"Your answer to Question {i}",
            height=130,
            key=f"answer_{i}",
            label_visibility="collapsed",
            placeholder="Write your answer here..."
        )
        answers.append(answer)
        st.markdown("")

    if st.button("Submit Answers →", key="stage2_submit"):
        # Validate each answer individually, flag only short ones
        all_valid = True
        for i, answer in enumerate(answers, 1):
            if len(answer.strip()) < 30:
                st.warning(
                    f"Answer {i} is too short ({len(answer.strip())} characters). "
                    "Please write at least 30 characters."
                )
                all_valid = False

        if all_valid:
            st.session_state.user_answers = [a.strip() for a in answers]

            with st.spinner("Reviewing your answers..."):
                # AI Call #3 — Critique
                critique_prompt = build_critique_prompt(
                    st.session_state.topic,
                    st.session_state.recall_questions,
                    st.session_state.user_answers
                )
                critique_text = get_completion(critique_prompt)

                if is_error_response(critique_text):
                    st.error(critique_text)
                    st.stop()

                st.session_state.critique_text = critique_text

            st.session_state.stage = 3
            st.rerun()


# ─────────────────────────────────────────────
# STAGE 3 — FEEDBACK ON YOUR ANSWERS
# ─────────────────────────────────────────────
elif st.session_state.stage == 3:
    # P5: Guard — redirect if required state is missing
    if not st.session_state.critique_text:
        st.warning("Missing required data. Returning to previous stage.")
        st.session_state.stage = 2
        st.rerun()

    show_progress(3)
    st.markdown('<div class="stage-header">Feedback on Your Answers</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="stage-sub">Review the corrective feedback for each of your answers.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="eval-block">{st.session_state.critique_text}</div>',
        unsafe_allow_html=True
    )

    st.markdown("")

    # Checkbox must be checked before Continue button renders
    acknowledged = st.checkbox(
        "I have read and understood the feedback",
        key="ack_checkbox"
    )
    st.session_state.acknowledged = acknowledged

    if acknowledged:
        if st.button("Continue to Reflection →", key="stage3_advance"):
            st.session_state.stage = 4
            st.rerun()


# ─────────────────────────────────────────────
# STAGE 4 — REFLECTION
# ─────────────────────────────────────────────
elif st.session_state.stage == 4:
    # P5: Guard — redirect if required state is missing
    if not st.session_state.critique_text or not st.session_state.acknowledged:
        st.warning("Missing required data. Returning to previous stage.")
        st.session_state.stage = 3
        st.rerun()

    show_progress(4)
    st.markdown('<div class="stage-header">Reflect on What You Learned</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="stage-sub">This is the final required step. Answer both prompts honestly.</div>',
        unsafe_allow_html=True
    )

    st.markdown("**What do you now understand that you did not understand before?**")
    reflection_clear = st.text_area(
        "Reflection 1",
        height=130,
        key="reflection_clear_input",
        label_visibility="collapsed",
        placeholder="Describe what has become clearer through this exercise..."
    )

    st.markdown("")
    st.markdown("**What still feels unclear, incomplete, or uncertain?**")
    reflection_unclear = st.text_area(
        "Reflection 2",
        height=130,
        key="reflection_unclear_input",
        label_visibility="collapsed",
        placeholder="Be honest about what you still don't fully understand..."
    )

    if st.button("Complete Session →", key="stage4_submit"):
        valid = True
        if len(reflection_clear.strip()) < 30:
            st.warning(
                f"First reflection is too short ({len(reflection_clear.strip())} characters). "
                "Please write at least 30 characters."
            )
            valid = False
        if len(reflection_unclear.strip()) < 30:
            st.warning(
                f"Second reflection is too short ({len(reflection_unclear.strip())} characters). "
                "Please write at least 30 characters."
            )
            valid = False

        if valid:
            st.session_state.reflection_clear = reflection_clear.strip()
            st.session_state.reflection_unclear = reflection_unclear.strip()
            st.session_state.stage = 5
            st.rerun()


# ─────────────────────────────────────────────
# STAGE 5 — SESSION COMPLETE
# ─────────────────────────────────────────────
elif st.session_state.stage == 5:
    # P5: Guard — redirect if required reflection state is missing
    if not st.session_state.reflection_clear or not st.session_state.reflection_unclear:
        st.warning("Missing required data. Returning to previous stage.")
        st.session_state.stage = 4
        st.rerun()

    show_progress(5)
    st.markdown('<div class="stage-header">Session Complete</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="stage-sub">You completed a full active learning cycle on: '
        f'<strong>{st.session_state.topic}</strong></div>',
        unsafe_allow_html=True
    )

    st.success("You engaged with all four stages: explanation → recall → feedback → reflection.")

    st.markdown("---")
    st.markdown("**What you now understand more clearly:**")
    st.markdown(
        f'<div class="eval-block">{st.session_state.reflection_clear}</div>',
        unsafe_allow_html=True
    )

    st.markdown("**What still feels unclear:**")
    st.markdown(
        f'<div class="eval-block">{st.session_state.reflection_unclear}</div>',
        unsafe_allow_html=True
    )

    st.markdown("")
    if st.button("Study Another Topic →", key="stage5_reset"):
        # P4: Explicit per-key reset — every key set to its default
        reset_session()
        st.rerun()

    # Data notice — visible at end of every session
    st.markdown(
        '<div class="data-notice">'
        'Your responses were sent to OpenAI for processing. No data is stored.'
        '</div>',
        unsafe_allow_html=True
    )
