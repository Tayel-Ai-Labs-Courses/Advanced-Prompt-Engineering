# Lesson 00 — What a Language Model Actually Is

**Goal:** replace the magic with a mental model. Once you understand what the
model is doing, every prompting technique in this course stops being a trick and
starts being obvious.

## What you will learn

- What "predict the next word" really means
- Why the model has no memory between requests
- Why it invents facts, and what that tells you to do
- The four things this changes about how you prompt

*No code. Read it once, and the rest of the course will make sense.*

---

## It predicts text. That is the whole thing.

A language model was trained on an enormous amount of writing with one job:
given some text, guess what comes next. That is it. When you type a question, it
is not looking up an answer — it is continuing your text in the most probable
way, one piece at a time.

Type `The capital of Egypt is` and it continues with `Cairo`, because in
everything it read, that is what followed. Type `Write a poem about the sea` and
it continues with a poem, because that is what followed that kind of request.

> **The single most useful sentence in this course:** the model does not see
> *you*, your intent, or the real world. It sees **your text**, and it continues
> it. The prompt is the entire world it gets.

This is why a vague prompt gives a vague answer. You did not give it a vague
*request* — you gave it a vague *world to continue*, and it continued the most
average, most probable version of it.

---

## It has no memory

Between two separate conversations, the model remembers nothing. It did not
"learn" from your last chat. Each request starts blank, and the only thing it
knows is what is in the prompt *right now*.

Even inside one chat, the "memory" is an illusion: the app quietly resends the
earlier messages with each new one. The model re-reads the whole conversation
every single turn. Nothing is stored inside the model.

**Consequence:** if you want the model to know something — a fact, a rule, your
customer's name, yesterday's decision — it has to be in the prompt. "It should
know that" is not a plan. Lesson 02 is entirely about this.

---

## Why it makes things up ("hallucination")

Because its job is to produce *probable-looking text*, not *true text*. When it
does not have a fact, it does not stop — it generates the most plausible-sounding
continuation, and a plausible-sounding fake is exactly what "most probable text"
produces.

Ask it for the phone number of a shop it has never heard of, and it will not say
"I don't know." It will produce something shaped like a phone number, because
that is what follows the question in its training.

**Consequence:** the fix for hallucination is almost never "tell it to be
accurate." The fix is to *give it the facts* (Lesson 02, Lesson 09) and to *give
it permission to say "I don't know"* (Lesson 07). You cannot scold a text
predictor into knowing something it was never shown.

---

## Tokens: it reads in pieces, not words

The model does not read letters or whole words. It reads **tokens** — chunks
that are often a word, sometimes part of one. "Cairo" might be one token;
"Yirgacheffe" might be four. This matters for two reasons you will meet again:

1. **Cost and length are counted in tokens**, not words (Lesson 13). Longer
   prompts cost more and are slower.
2. **Arabic usually costs more tokens than English** for the same meaning,
   because the model was trained on far more English. The same sentence can be
   2–3× more tokens in Arabic. Good to know when you price a workflow.

You do not need to count tokens by hand. You need to know they exist, and that
shorter is cheaper.

---

## What this changes about how you prompt

Everything downstream follows from the four facts above:

| Because the model… | You should… | Taught in |
|---|---|---|
| continues your text, doesn't read your mind | spell out the task completely | Lesson 01 |
| knows only what's in the prompt | put the facts *in* the prompt | Lesson 02, 09 |
| produces plausible text, not true text | let it say "I don't know" | Lesson 07 |
| has no memory | resend what matters every time | Lesson 02, 08 |

---

## The one exercise

Take a request you would normally give an AI — anything. Before you send it, ask:
*"If a smart stranger read only this text, with no idea who I am or what I'm
doing, could they produce what I want?"*

If the answer is no, your prompt is not finished. That question is the entire job.

---

**Next:** [Lesson 01 — Anatomy of a Prompt](01-anatomy-of-a-prompt.md), the six
components that answer that question.
