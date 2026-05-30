# Aktiv

## Overview

Aktiv is an AI-guided structured learning system designed to combat passive studying. Traditional AI chatbots make it easy for students to consume information without demonstrating understanding. Aktiv enforces active participation through a locked learning workflow that requires explanation, retrieval, feedback, and reflection before a study session can be completed.

Built as a Streamlit prototype, Aktiv explores how AI can support evidence-based learning rather than simply providing answers.

---

## Problem

Modern AI tools make information more accessible than ever, but they often encourage passive consumption.

A student can ask an AI a question, receive an answer, and feel as though they understand the material without ever testing their knowledge. Research on active recall and retrieval practice suggests that learning improves when students are required to retrieve information from memory rather than repeatedly reviewing content.

The challenge was to design an AI-powered learning system that encourages active participation instead of passive consumption.

---

## Solution

Aktiv implements a structured, stage-gated learning workflow.

Rather than allowing unrestricted conversation with an AI, the application requires the learner to complete a series of mandatory steps before progressing.

The workflow follows the sequence:

1. Select a topic.
2. Explain existing understanding.
3. Receive AI-generated gap analysis.
4. Answer targeted active recall questions.
5. Receive corrective feedback.
6. Acknowledge feedback.
7. Complete reflection.

Each stage must be completed before the next becomes available.

The structure itself is the product.

---

## Features

* AI-powered knowledge gap detection
* Active recall question generation
* Structured answer evaluation
* Mandatory feedback acknowledgement
* Reflection-based session completion
* Session-based learning workflow
* Stateless architecture with no persistent user storage

---

## Architecture

### Tech Stack

* Python
* Streamlit
* OpenAI API

### Project Structure

```text
aktiv/
├── app.py
├── prompts.py
├── openai_client.py
├── requirements.txt
└── README.md
```

### System Flow

User Input

↓

Knowledge Explanation

↓

AI Gap Analysis

↓

Active Recall Questions

↓

Student Answers

↓

AI Feedback

↓

Reflection

↓

Session Completion

---

## Demo

### Walkthrough

[Insert GIF walkthrough here]

### Screenshots

[Insert screenshots here]

---

## Lessons Learned

### Learning Science Matters

One of the biggest insights from this project was realizing that AI-powered education is not primarily a model problem—it is often a workflow problem.

A highly capable model can still produce poor learning outcomes if students interact with it passively.

### Constraints Create Better Behavior

Many applications focus on giving users maximum flexibility. Aktiv explored the opposite idea: carefully designed constraints can improve engagement and learning outcomes.

### Simplicity Improves Reliability

Separating prompt generation, API interaction, and user interface logic made the application easier to maintain and debug.

---

## Future Improvements

### Current State

Aktiv currently functions as a proof-of-concept demonstrating a structured AI-guided learning workflow.

### Planned Improvements

* User accounts
* Session history
* Learning analytics dashboard
* Progress tracking over time
* Expanded study modes
* Support for uploaded course materials
* Personalized difficulty adjustment

### Long-Term Vision

The long-term goal is to evolve Aktiv into a learning platform that combines AI guidance with evidence-based educational practices. Rather than replacing traditional study methods, the system would act as a structured learning coach that encourages active recall, reflection, and long-term retention.

---

## AI Tools Disclosure

This project was developed with assistance from Claude and OpenAI tools for architecture planning, prompt engineering, implementation support, and code review.

All design decisions, validation, and final implementation choices were made by the developer.

---

## Data & Privacy

User inputs are sent to the OpenAI API during the active session for processing.

No user data is stored, persisted, or retained by the application.

Session data is cleared when the browser session ends or when a new study session begins.

---

## Resources

* Roediger & Karpicke (2006) — Test-Enhanced Learning
* Bjork (1994) — Memory and Metamemory Considerations
* OpenAI API Documentation
* Streamlit Documentation
