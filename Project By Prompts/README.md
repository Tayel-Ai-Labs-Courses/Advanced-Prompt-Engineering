# Project By Prompts

Projects built end to end by prompting an AI coding assistant — the course's
techniques applied to real, running software rather than to a single reply.

Each project here ships with its own notes file explaining how it works and
what broke along the way, so the folder reads as a worked example and not just
a code dump.

---

## Projects

### 🍕 `pizza-chatbot/`

A pizza-ordering chatbot for a restaurant website. Understands Arabic, English
and Franco-Arabic, takes an order from flavour to delivery address, and saves it
with a tracking number.

Covers the four ideas every task-oriented bot is built on:

| Concept | Where it lives |
|---|---|
| **Intents** — what the customer wants | `nlp.py` |
| **Entities** — the details in the sentence | `nlp.py` |
| **Slot filling** — asking only for what is missing | `dialog.py` |
| **Context** — the same word means different things | `dialog.py` |

Python standard library only. No pip, no framework, no build step.

```bash
cd pizza-chatbot
python3 app.py
# then open http://localhost:8000
```

Full walkthrough — including the three real bugs found while testing it and how
each was fixed — is in [`pizza-chatbot/NOTES.md`](pizza-chatbot/NOTES.md).
