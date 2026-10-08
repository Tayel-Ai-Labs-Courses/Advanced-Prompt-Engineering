# Assignment — Session 1 (Lessons 00–04)

**Foundations + first techniques.** This assignment proves you can do the one
thing this part of the course is about: turn a vague request into a prompt that
works, and explain *why* it works. No code required.

Covers: [Lesson 00](../lessons/00-what-is-a-language-model.md),
[01](../lessons/01-anatomy-of-a-prompt.md),
[02](../lessons/02-context-and-grounding.md),
[03](../lessons/03-examples-few-shot.md),
[04](../lessons/04-reasoning-chain-of-thought.md).

---

## Part 1 — Name the components (Lesson 01)

Take this weak prompt:

> "Write a reply to this customer."

List **which of the six components it's missing** (role, task, context, examples,
format, constraints) and what each missing one would add. One line each.

---

## Part 2 — Rewrite a real prompt (Lessons 01, 02)

Pick a **real** prompt you've actually used (work, study, personal). Rewrite it
using the six components. Your rewrite must include:

- [ ] A clear **role** and a one-verb **task**
- [ ] **Context** — the real facts, wrapped in delimiters (`<facts>…</facts>`)
- [ ] A **grounding** instruction ("answer only from the facts above")
- [ ] An **escape hatch** ("if it's not covered, say you're unsure — don't guess")

Hand in **both** the before and the after.

---

## Part 3 — Few-shot a style (Lesson 03)

Choose a task where tone or format matters (product blurbs, replies, summaries).
Write **two examples** of input → the exact output you'd be happy with, including
**one edge case**. Then show the full few-shot prompt. One paragraph: what did the
examples fix that instructions alone couldn't?

---

## Part 4 — Make it reason (Lesson 04)

Write one prompt for a task that needs **step-by-step reasoning** (a calculation
or a multi-condition decision). Show it with and without "work it out step by
step." Note any difference in the answer, and say in one line *why* the steps
help.

---

## Part 5 — Diagnose (Lesson 01 diagnostic)

Here are three failures. For each, name the **single missing component** and the
fix (use the diagnostic map from Lesson 01):

1. The model invented a price that isn't real. → ?
2. The answer is correct but the tone is completely wrong. → ?
3. You asked for JSON and got three paragraphs of prose. → ?

---

## How to hand in

Put your answers in one document (or markdown file) and submit where your
instructor tells you. There's no single right wording — you're graded on whether
each prompt has the right components and whether your *reasoning about why* is
sound.

**Self-check before you submit:** run the universal checklist at the bottom of
[`examples/weak-vs-good.md`](../examples/weak-vs-good.md) against your Part 2
rewrite. If it passes, you're done.

---

*Advanced Prompt Engineering — Tayel AI Labs.*
