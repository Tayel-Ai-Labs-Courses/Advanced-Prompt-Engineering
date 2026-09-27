# System Maps & Pipelines

How real prompt systems are actually wired. Each map below is a complete,
buildable design — the kind of thing you'd sketch for a client before writing a
line of anything. They reuse the techniques from the lessons; the lesson number
is noted where a piece comes from.

Read these to see how single prompts combine into systems, and to have a diagram
you can adapt for your own projects.

---

## 0. The atom: one prompt

Before the systems, the unit they're built from. Every box in every diagram below
is one of these.

```mermaid
flowchart LR
    IN["Input<br/>(user msg / data)"] --> PR["Prompt<br/>role + task + context<br/>+ format + constraints"]
    PR --> LLM["Model"]
    LLM --> OUT["Output<br/>(prose or structured)"]
```
*Built from Lessons 01–07. Everything else is these, wired together.*

---

## 1. Support bot (grounded Q&A)

The most common first product. Answers customer questions from *your* facts,
escalates when it can't. No memory of the business — the facts are injected.

```mermaid
flowchart TD
    U["Customer question"] --> SC{"In scope?<br/>(our topics)"}
    SC -->|No| DEC["Politely decline,<br/>steer back"]
    SC -->|Yes| G["Build prompt:<br/>question + relevant facts<br/>+ grounding rule"]
    KB[("Business facts:<br/>menu, hours, policies")] --> G
    G --> M["Model"]
    M --> CK{"Answer covered<br/>by the facts?"}
    CK -->|Yes| A["Send answer"]
    CK -->|No| ESC["'Let me check' →<br/>escalate to human"]
```
*Lessons 02 (grounding), 07 (scope + escape hatch). Add RAG (map 3) when the facts
outgrow a single paste.*

---

## 2. Router → specialists (one inbox, many jobs)

When one channel receives many *kinds* of request, classify first, then send each
to a specialised prompt. Each branch is simpler and safer than one prompt trying
to do everything.

```mermaid
flowchart TD
    IN["Incoming message"] --> R["Router prompt<br/>→ { type }  (JSON)"]
    R -->|complaint| C["Apology + escalation<br/>specialist"]
    R -->|question| Q["Grounded Q&A<br/>(map 1)"]
    R -->|order| O["Order extraction<br/>→ JSON → system"]
    R -->|other| H["Hand to human"]
    C --> OUT["Response / action"]
    Q --> OUT
    O --> OUT
    H --> OUT
```
*Lessons 06 (JSON routing), 08 (router pattern). The router is a cheap small-model
call (Lesson 13).*

---

## 3. RAG pipeline (answers from a big knowledge base)

When the facts are too large to paste, retrieve only the relevant pieces per
question. Two phases: prepare the documents once, then answer each query.

```mermaid
flowchart TD
    subgraph PREP["Prepare once (and on every doc update)"]
        D["Documents"] --> CH["Split into chunks"]
        CH --> EM["Embed each chunk"]
        EM --> VS[("Vector store")]
    end
    subgraph QUERY["Per question"]
        Q["Question"] --> EQ["Embed question"]
        EQ --> RT["Retrieve nearest chunks"]
        VS --> RT
        RT --> BP["Build prompt:<br/>question + chunks + grounding"]
        BP --> M["Model"]
        M --> A["Grounded answer<br/>or 'I'll check'"]
    end
```
*Lesson 09. Quality lives in the retrieval half — get the right chunks and the
prompt half is easy.*

---

## 4. Agent loop (the model takes actions)

When the task needs steps and tools, not one answer. The model thinks, calls a
tool, reads the result, and repeats — with hard limits and a human gate on
anything irreversible.

```mermaid
flowchart TD
    G["Goal"] --> T["THINK: next step?"]
    T --> DEC{"Need a tool?"}
    DEC -->|No| F["Final answer"]
    DEC -->|Yes| RISK{"Irreversible?<br/>(money, send, delete)"}
    RISK -->|Yes| HU["Human confirms"] --> ACT
    RISK -->|No| ACT["ACT: call tool<br/>(structured request)"]
    ACT --> OBS["OBSERVE: tool result<br/>(treated as DATA)"]
    OBS --> LIM{"Step limit hit?"}
    LIM -->|Yes| STOP["Stop, report"]
    LIM -->|No| T
```
*Lessons 10 (loop, tools), 12 (results are data, not instructions), 13 (step
limit caps cost).*

---

## 5. Content factory (draft → refine → format)

A sequential chain that produces polished, on-brand content at volume. Each stage
does one job; a human approves at the end.

```mermaid
flowchart LR
    BRIEF["Brief + brand facts"] --> D1["Draft<br/>(strong model)"]
    D1 --> D2["Critique against<br/>brand rules"]
    D2 --> D3["Revise using<br/>the critique"]
    D3 --> D4["Format + translate<br/>(AR + EN)"]
    D4 --> HR["Human approves"]
    HR --> PUB["Publish"]
```
*Lessons 04 (critique = reasoning), 08 (sequential chain), 05 (brand role). The
critique step catches most quality problems before a human sees the draft.*

---

## 6. Evaluation harness (how you know any of it works)

This wraps *any* of the systems above. It's what turns "looks good" into a number,
and what protects you when you change a prompt or the model updates.

```mermaid
flowchart TD
    PROMPT["Prompt / pipeline<br/>version N"] --> RUN["Run on every eval input"]
    ES[("Eval set:<br/>real inputs + expected")] --> RUN
    RUN --> SCORE["Score each output"]
    SCORE --> RULES["Rule checks<br/>(format, no invented facts)"]
    SCORE --> JUDGE["Model-as-judge<br/>(tone, accuracy)"]
    RULES --> AGG["Aggregate → score"]
    JUDGE --> AGG
    AGG --> GATE{"Beats current<br/>version?"}
    GATE -->|Yes| SHIP["Ship it"]
    GATE -->|No| FIX["Fix, re-run"] --> RUN
    PROD["Production failures"] -.->|"add as new cases"| ES
```
*Lesson 11. The dotted line is the flywheel: every real failure becomes a permanent
test, and the growing eval set is your moat (Lesson 14).*

---

## How they compose

Real products stack these. A mature support system is often:

```mermaid
flowchart LR
    A["2. Router"] --> B["3. RAG<br/>(for questions)"]
    A --> C["4. Agent<br/>(for orders/bookings)"]
    B --> D["6. Eval harness<br/>wraps everything"]
    C --> D
    E["12. Security layer<br/>guards every input"] --> A
```

Start with **one** map — usually map 1 — get it reliable with map 6, and add the
others only when a real need appears. Complexity you don't need is cost and risk,
not sophistication.
