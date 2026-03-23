# Design Rationale — Aktiv

## Why Structured Learning Over Chatbot Design

Most AI tools optimize for information delivery. When a student asks an AI to explain a concept, the AI explains it. When a student asks for help with homework, the AI helps. This interaction pattern is frictionless by design — and that frictionlessness is the problem.

Research in cognitive science consistently shows that retrieval practice (actively recalling information) produces significantly stronger long-term retention than re-reading or passive review (Roediger & Karpicke, 2006). Desirable difficulty — the idea that making learning harder in the right ways improves outcomes — is one of the most robust findings in learning science (Bjork, 1994).

Aktiv was designed around a single principle: **the structure is the product**. The AI is not the value. The forced sequence is the value. By requiring the student to produce knowledge before receiving feedback, the system turns a passive AI query into an active learning event.

---

## Ethical Design Decisions

### 1. Input Before Output (Prevents Passive Consumption)
**Decision:** No AI response is shown until the user has submitted their own explanation.  
**Implementation:** Stage 1 is a hard gate. The evaluation prompt does not fire until the explanation field passes minimum-length validation. There is no way to reach Stage 2 without completing Stage 1.  
**Ethical reasoning:** This design choice prevents the primary harm of AI in education — students receiving answers without engaging cognitively. The effort required before feedback creates a learning event, not just an information transaction.

### 2. Gap-Targeted Questions (Active Recall, Not Generic Quiz)
**Decision:** Recall questions are generated from the evaluation's identified gaps, not from the topic in general.  
**Implementation:** The questions prompt receives the full evaluation output as context and is explicitly constrained to use only the gaps section.  
**Ethical reasoning:** Generic topic questions would allow students to answer from prior knowledge without confronting what they actually don't know. Gap-targeting forces the student to address their specific misunderstandings.

### 3. Acknowledgment Checkpoint (Prevents Passive Skipping)
**Decision:** The feedback screen requires a checkbox acknowledgment before the Continue button appears.  
**Implementation:** `st.session_state.acknowledged` is set by the checkbox; the Continue button is conditionally rendered only when this is True.  
**Ethical reasoning:** Without this checkpoint, a student could receive AI feedback and immediately advance without reading it. The checkbox is a lightweight but meaningful attention gate.

### 4. No Free-Form AI Access (Prevents Over-Reliance)
**Decision:** There is no "ask AI anything" input anywhere in the application.  
**Implementation:** The app uses only `st.text_area` and `st.text_input` for structured user input. No `st.chat_input` or `st.chat_message` components are used.  
**Ethical reasoning:** Unrestricted AI access in a learning context encourages shortcut-seeking behavior. By removing the free-form interface entirely, the system makes the structured path the only path.

### 5. Mandatory Reflection (Metacognitive Enforcement)
**Decision:** The session cannot be marked complete without submitting both reflection fields.  
**Implementation:** Stage 5 is only reachable after Stage 4 validation passes. Stage 5 itself has a guard that checks for non-empty reflection state.  
**Ethical reasoning:** Metacognition — thinking about what you know and don't know — is a critical component of effective learning. Making it mandatory, not optional, ensures the student ends every session with a calibrated self-assessment.

### 6. Transparent Feedback Structure
**Decision:** AI output uses labeled sections (Correct / Gaps / Incorrect) rather than free-form prose.  
**Implementation:** Prompts specify exact output format and constrain the AI from explaining topics or introducing new content.  
**Ethical reasoning:** Structured feedback is more honest and easier to act on than vague commentary. Labeled sections make it immediately clear to the student what they got right and what they need to revisit.

---

## Mitigation Strategies

| Risk | Mitigation |
|------|-----------|
| Student pastes AI-generated explanation into Stage 1 | Character minimum forces some effort; AI evaluation will identify shallow or generic content and label it accordingly in the gaps section |
| AI generates overly explanatory feedback (lecture mode) | All three prompts include explicit constraints: "Do NOT explain the topic in full," "Do NOT re-teach the concept" |
| Student clicks through without reading feedback | Checkbox acknowledgment gate at Stage 3 requires active engagement before advancing |
| App crashes on API failure | `get_completion()` wraps all API calls in try/except and returns a readable string; error string blocks stage advance |
| Student refreshes to skip stages | All state lives in `st.session_state`; session refresh resets to Stage 0 (this is a feature, not a bug — no partial state can be exploited) |
| Questions are too easy or generic | Questions prompt is chained to evaluation output and constrained to use only identified gaps; yes/no and definition-only questions are explicitly prohibited |

---

## Future Considerations and Scalability

### Near-Term Improvements
- **Spaced repetition integration:** Store session topics and schedule re-testing after 24 hours, 1 week, 1 month following the Ebbinghaus forgetting curve
- **Progress tracking:** Allow users to create accounts and view their learning history across topics
- **Material upload:** Allow PDF or document upload as the study material instead of manual text input
- **Difficulty calibration:** Adjust question complexity based on the quality of the user's prior explanation

### Scalability Considerations
- The current architecture is intentionally stateless (no database, no auth). Adding persistence would require a backend (e.g., Supabase, Firebase) and user authentication
- The OpenAI API cost per session is approximately 3 calls × ~500 tokens = ~1,500 tokens per session. At scale, batching or caching common topic evaluations could reduce cost
- The prompt logic in `prompts.py` is fully isolated — swapping to a different model provider (Anthropic Claude, Google Gemini) requires only changes to `openai_client.py`

### Broader Ethical Considerations
- **Access equity:** API costs create a barrier. A production version should consider subsidized access for students who cannot afford API fees
- **Bias in evaluation:** The AI evaluator may reflect training biases when assessing explanations on politically or culturally contested topics. Human review should supplement AI feedback in sensitive domains
- **Dependency risk:** If OpenAI's API is unavailable, the system fails. A fallback to a locally-run model (e.g., via Ollama) would improve resilience
- **Evaluation validity:** The AI's assessment of "correctness" is not authoritative. Students should be made aware that AI feedback should be cross-referenced with course materials and instructors

---

## Learning Science References

- Roediger, H. L., & Karpicke, J. D. (2006). Test-Enhanced Learning: Taking Memory Tests Improves Long-Term Retention. *Psychological Science*, 17(3), 249–255.
- Bjork, R. A. (1994). Memory and metamemory considerations in the training of human beings. In J. Metcalfe & A. Shimamura (Eds.), *Metacognition: Knowing about knowing*. MIT Press.
- Brown, P. C., Roediger, H. L., & McDaniel, M. A. (2014). *Make It Stick: The Science of Successful Learning*. Harvard University Press.
