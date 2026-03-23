# Aktiv — AI-Guided Structured Learning System

Aktiv is a Streamlit prototype that enforces evidence-based study behavior through a locked, sequential learning cycle. Unlike general AI chatbots, Aktiv prevents passive consumption by requiring active user input at every stage before any AI feedback is shown.

---

## What This App Does

1. The user enters a topic or study material
2. The user must explain what they already know (minimum 50 characters)
3. AI evaluates the explanation — identifying what is correct, what is missing, and what is incorrect
4. AI generates 2–3 active recall questions targeting the identified gaps
5. The user answers all questions before any AI critique appears
6. AI provides corrective feedback per answer; user must acknowledge it via checkbox
7. User completes a structured reflection before the session closes

The structure is the product. No stage can be skipped. No free-form AI access exists.

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/aktiv.git
cd aktiv
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your API key

Create a file at `.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

> ⚠️ Never commit this file. Add `.streamlit/secrets.toml` to your `.gitignore`.

### 4. Run locally

```bash
streamlit run app.py
```

---

## Streamlit Community Cloud Deployment

1. Push this repository to GitHub (ensure `secrets.toml` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **New app** → select your repository and `app.py` as the entry point
4. Under **Advanced settings → Secrets**, add:

```toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

5. Click **Deploy**

---

## Project Structure

```
aktiv/
├── app.py              # UI + stage-gate logic only
├── prompts.py          # Three prompt-builder functions — no side effects
├── openai_client.py    # Single API call function with full error handling
├── requirements.txt    # streamlit, openai
└── README.md           # This file
```

---

## AI Tools Disclosure

This application was designed and built with the assistance of the following AI tools:

| Tool | Usage |
|------|-------|
| Claude (Anthropic) | System architecture planning, prompt engineering, code generation, code review |
| OpenAI GPT-4o-mini | Runtime AI evaluation, question generation, and answer critique within the app |

All code was reviewed, validated, and intentionally structured by the developer. AI-generated code was not used blindly — each component was verified against a locked implementation specification.

---

## Resources

- Roediger, H. L., & Karpicke, J. D. (2006). *Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention*. Psychological Science, 17(3), 249–255.
- Bjork, R. A. (1994). *Memory and metamemory considerations in the training of human beings*. In J. Metcalfe & A. Shimamura (Eds.), Metacognition. MIT Press.
- OpenAI API Documentation — https://platform.openai.com/docs
- Streamlit Documentation — https://docs.streamlit.io
- Streamlit Community Cloud — https://streamlit.io/cloud

---

## Data & Privacy

User inputs (topic, explanations, answers, reflections) are sent to the OpenAI API for processing during the session. No data is stored, logged, or persisted between sessions. Session state is cleared on browser refresh or when the user clicks "Study Another Topic."
