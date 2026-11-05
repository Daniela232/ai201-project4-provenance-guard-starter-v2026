# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. Real writers almost never get called AI

Of 10 pieces of writing I know a real person wrote (including plain, simple
writing like Ana's from my Milestone 1 notes), at most 1 gets the
high-confidence AI label. This has to hold in each of the 3 runs.

**Why this target:** Calling a real writer AI is the worst mistake this system
can make. Missing some AI text only costs the site a little, but a wrong
accusation costs the person a lot, so I only allow 1 in 10.

---

## 2. Clearly-AI and clearly-human text score far apart

My clearly_ai test text scores at least 0.3 higher (combined score) than my
clearly_human test text, in each of the 3 runs.

**Why this target:** A gap smaller than 0.3 is too close to be confident. If
the two obvious cases are that close, the system can't really tell them apart.

---

## 3. All three labels can actually show up

I submit 10 texts, and each of the three labels (high-confidence AI,
high-confidence human, unsure) shows up at least 2 times.

**Why this target:** If each label shows up at least twice, at least we know
it's working. Only one of each is not enough data to know it wasn't a fluke.

---

## 4. Appeals get recorded

When an appeal is sent with a real content_id, at least 9 out of 10 appeals
change the item's status to under_review and show up in GET /log. An appeal
with a content_id that doesn't exist gets an error back and changes nothing.

**Why this target:** Nothing is ever perfect, so I leave room for 1 out of 10 to
go wrong.

---

## 5. Bad input gets a clear error, not a crash

Every time, these get a 400 error with a message instead of crashing the
service:

- nothing entered, or only spaces
- a number (or anything that isn't words) instead of text, with a message
  telling the person to enter text
- text longer than 1500 words

**Why this target:** A clear error tells the writer what went wrong and what to
fix, so they don't get stuck and have to send a support ticket.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
