# Assignment — Session 2 (Lessons 05–10)

**From one good prompt to a system.** Session 1 was about writing a prompt that
works. This one is about building something you could put in front of a real
user: it knows who it is, it returns a shape software can read, it refuses to
invent, it runs in steps, it answers from your documents, and — if it acts — it
cannot do real damage.

Pick **one** assistant idea and carry it through all six parts. No code required;
parts 4–6 can be done on paper.

Covers: [Lesson 05](../lessons/05-roles-and-personas.md),
[06](../lessons/06-structured-output.md),
[07](../lessons/07-constraints-and-guardrails.md),
[08](../lessons/08-prompt-chaining-pipelines.md),
[09](../lessons/09-retrieval-rag.md),
[10](../lessons/10-agents-and-tools.md).

---

## Part 1 — Write a load-bearing role (Lesson 05)

Write the **system prompt** role for your assistant. It must answer all three:

- [ ] **Who are you?**
- [ ] **Who are you talking to?**
- [ ] **What do you optimise for?**

Then add the **one hard limit** that matters most in your domain.

In one line: name something your role does **not** do — a fact it still doesn't
know without context. (This is the trap most people fall into.)

---

## Part 2 — Force a schema (Lesson 06)

Pick a messy text you handle often (orders, enquiries, receipts, applications).

- [ ] Write the **exact JSON schema** you want back — keys and types.
- [ ] Add: *"Return ONLY the JSON, no prose."*
- [ ] Add a **missing-value rule** (`null`, never invent).
- [ ] Run it on **five real, varied inputs**, including one deliberately
      incomplete one.

Hand in the schema, the prompt, and the five outputs. Confirm it never invented a
value.

---

## Part 3 — Fit the five guardrails (Lesson 07)

Add all five to your assistant:

- [ ] An escape hatch — *"if unsure or not in the facts, don't guess"*
- [ ] A scope limit — what it will and won't discuss
- [ ] A rule against **the most dangerous invention in your domain**
      (prices? availability? medical or legal claims?)
- [ ] A fallback — escalate to a human / ask a question
- [ ] Grounding — *"answer only from the provided information"*

Then **attack your own assistant**: ask something off-topic, ask something the
facts don't cover, and try to get it to invent a promotion. Write down what it
did. If it invented anything, tighten the matching guardrail and try again.

---

## Part 4 — Split it into a chain (Lesson 08)

Take one overloaded prompt (yours or Part 2's) and redraw it as a **chain**:

- [ ] Draw the steps as boxes — **one job per box**
- [ ] State what **structured data** passes between each step
- [ ] Mark which steps could be **plain code** instead of a prompt
- [ ] Say which pattern it is: sequential, router, or map-reduce

One line: if the final output came out wrong, **which step would you test first,
and how?**

---

## Part 5 — Design the retrieval (Lesson 09)

You don't have to build it — designing it correctly is the skill.

- [ ] What documents would your assistant need?
- [ ] How would you **chunk** them, and why that size?
- [ ] For one real question, what should retrieval **fetch**?
- [ ] Write the final prompt: question + retrieved chunks + grounding rule

One line: name a question where **bad retrieval** would produce a confident wrong
answer — and say how you'd notice.

Also answer honestly: **does your case actually need RAG**, or would a simple
paste do? (The right answer is often "paste".)

---

## Part 6 — Draw the agent's safety model (Lesson 10)

If your assistant could use tools, list them in a table:

| Tool | Read-only or acts? | Reversible? | Needs human approval? |
|---|---|---|---|

- [ ] Mark every tool
- [ ] Circle the ones that **must** have a human confirmation before firing
- [ ] Write the one line that keeps retrieved content as **data, not
      instructions**
- [ ] Set a **step limit**

---

## How to hand in

One document with all six parts. You're graded on whether the pieces fit together
into something you'd actually deploy — not on wording.

**Self-check before you submit:** your assistant should now be able to (1) say who
it is, (2) return a machine-readable answer, (3) admit when it doesn't know, and
(4) be unable to do anything irreversible by itself. If any of those four fails,
you know which part to revisit.

---

*Advanced Prompt Engineering — Tayel AI Labs.*
