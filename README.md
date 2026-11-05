# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** Perplexity, basically how surprised GPT-2 is by each
next word (`detector.py::model_signal`). Low surprise turns into a high AI
score, from 0 to 1.

**Why that might differ between human and AI writing:** AI writing is made by
choosing likely next words, so another language model finds it really
predictable. People tend to make weirder, more personal word choices.

**What it can't see:** Being predictable doesn't mean something was written by
AI. Plain writing with simple words and normal sentences can score as AI, like
someone writing in their second language or a younger writer. AI text that
uses unusual words could score as human. It also cuts off really long texts
and can't score really short ones.

### Signal two — the style signal

**What it measures:** The shape of the text, without reading it
(`stylometry.py::style_signal`). Three things, each turned into a 0-1 "how AI
does this look" number and then averaged:

| Measure | What it is | Which way is AI | Weight |
|---|---|---|---|
| Sentence length spread | std dev of sentence lengths / mean | low spread = AI | 0.4 |
| Punctuation density | commas, dashes, semicolons, colons, quotes, brackets, ! and ? per word | low density = AI | 0.4 |
| Vocab variety | average unique-words ratio over 40-word windows | **high** variety = AI | 0.2 |

**Why that might differ between human and AI writing:** AI writing usually has
sentences that are all about the same medium length and not much interesting
punctuation. Human writing is more uneven, like a really short sentence right
next to a really long one, with dashes, colons, and quotes mixed in.

The vocab one surprised me. I expected AI to have a narrower vocabulary, but on
my test texts it was the opposite: clearly_ai scored 0.94 and clearly_human
scored 0.83. The formal AI text keeps using new "big" words, and the casual
human text repeats small words like "I", "and", "she". So I flipped it to match
what I saw, and gave it the smallest weight because three texts isn't a lot of
proof.

**What it can't see:** It can't actually read. Anything that changes the shape
but not the meaning will change its score, like adding typos, splitting
sentences up, adding dashes, or pasting in a quote. That's really easy for
someone to do on purpose. It also has a problem with short text: a single
plain sentence has no punctuation and every word is unique, so "Just one
sentence here." gets a style score of 0.8.

### The combining rule

**The rule:** Average the two signals. If they're more than 0.3 apart, they
disagree, so I pull the average halfway back toward 0.5 (unsure). This way
something only gets a confident "AI" score if both signals agree, and one
signal can never get someone accused by itself. That comes straight from my
Milestone 1 notes, where calling a real writer AI is the worst mistake the
system can make.

**The numbers:** (all in `config.py`)

- `WEIGHT_MODEL_SIGNAL = 0.5`, `WEIGHT_STYLE_SIGNAL = 0.5`
- `DISAGREEMENT_GAP = 0.3`: more than this apart counts as disagreeing
- `DISAGREEMENT_PULL = 0.5`: how far toward 0.5 the score gets pulled (halfway)

So `combined = avg`, or if `|model - style| > 0.3` then
`combined = avg + (0.5 - avg) * 0.5`.

Confidence (in the response) is how far the combined score is from the
middle: `abs(combined - 0.5) * 2`. 0.5 is confidence 0, and 0 or 1 is
confidence 1.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**
My clearly_human text. Signal one gave it 0.445 (kind of a shrug, leaning a
little AI) and signal two gave it 0.057 (very human). That's a 0.39 gap, so my
rule kicks in. The plain average would be 0.25, and my rule pulls it to 0.375.
That moves a real human toward "unsure", which is the cost of this rule. I'm ok
with it because "unsure" hurts a lot less than a wrong accusation.

**My four test inputs:**

| Input | model | style | gap | combined |
|---|---|---|---|---|
| clearly AI | 0.754 | 0.831 | 0.08 | 0.793 |
| clearly human | 0.445 | 0.057 | 0.39 | 0.375 |
| plain human writing (Ana-style) | 0.876 | 0.800 | 0.08 | **0.838** |
| lightly-edited AI | 0.759 | 0.787 | 0.03 | 0.773 |

**The big problem:** the plain human text scored *higher* than the clearly AI
text. This is exactly the Ana case from my Milestone 1 notes. Both signals
think plain, simple writing looks like AI, so they agree, and my disagreement
rule can't help because it only kicks in when they disagree. No threshold can
fix this either: any line that labels clearly AI (0.79) as AI would also label
the plain human text (0.84) as AI. I'm leaving it as is and writing it down,
because it's the most important thing for next unit's testing to hit.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

Milestone 3 version: only signal one is wired in, so `style_score` is still
null and the guess, confidence, and label are placeholders. I'll replace this
with the full run once the second signal and the labels are done.

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "The importance of effective time management cannot be overstated in today'"'"'s fast-paced work environment. Professionals who develop strong organizational habits are better positioned to meet deadlines and reduce stress. There are several key strategies that can help individuals improve their productivity.", "creator_id": "daniela"}'
```

```json
{
  "confidence": 0.5,
  "content_id": "c_d29a52c2699c",
  "guess": "unsure",
  "label": "not built yet",
  "model_score": 0.8033,
  "style_score": null
}
```

The log entry for it (`curl "http://127.0.0.1:5000/log?limit=1"`):

```json
{
  "count": 1,
  "entries": [
    {
      "combined_score": null,
      "content_id": "c_d29a52c2699c",
      "creator_id": "daniela",
      "guess": "unsure",
      "label": "not built yet",
      "model_score": 0.8033,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-11-05T01:23:08+00:00"
    }
  ]
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
