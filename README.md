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

Provenance Guard is a small backend a writing site could plug in. You send it
text, and it sends back a guess (AI, human, or unsure), how confident it is, a
plain-English label for the reader, and a `content_id` the writer can use to
appeal.

1. Someone sends a `POST /submit` request with JSON that has the `text` and
   their `creator_id`.
2. `app.py::submit` checks the input first. If the body isn't a JSON object,
   the text is missing, empty, or not a string, or it's over 1500 words, it
   sends back a 400 error and stops there. This way the signals only ever get
   real text.
3. Signal one (`detector.py::model_signal`) runs the text through GPT-2 and
   checks how predictable the wording is. It gives back a `model_score` from 0
   to 1, where higher means more likely AI.
4. Signal two (`stylometry.py::style_signal`) looks at the text's shape: how
   much sentence lengths vary, how many different words are used, and
   punctuation. It doesn't understand what the words mean. It also gives back
   a score from 0 to 1 (`style_score`), where higher means more likely AI.
5. `scoring.py::combine_signals` combines the two scores into one
   `combined_score`. If the two signals disagree by more than 0.3, the score
   gets pulled toward 0.5 (unsure).
6. `scoring.py::score_to_label` turns that number into the actual sentence the
   reader sees. There are three possible labels: high-confidence AI,
   high-confidence human, or unsure.
7. The service creates a `content_id`, writes everything to
   `logs/audit.jsonl` with status `decided` using `audit.py::log_decision`, and
   sends the same info back as JSON.

If the writer thinks the result is wrong, they can send a `POST /appeal` with
their `content_id` and their reasoning. That gets saved in the log and the
status changes to `under_review`.

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

> **Correction (unit 8):** the "plain human writing (Ana-style)" text in this
> table wasn't actually written by a person. Claude wrote it to imitate the
> Ana example from my notes, and I didn't catch that when I labeled it. So it
> getting a high AI score doesn't prove a false positive. The real evidence came
> in unit 8: FP03 in the attack set (a non-native English speaker writing
> carefully) got the AI label with a combined score of 0.83, and one piece of my
> own speech got 0.71.

---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | below 0.40 | This looks like it was written by a person. If you think something is wrong with this result, you can still appeal. |
| unsure | 0.40 to 0.70 | We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it. |
| high-confidence AI | above 0.70 | This looks like it was written by AI. If you wrote this yourself, you can appeal and a real person will review it. |

The ranges come from `config.py` (`HUMAN_THRESHOLD = 0.40`, `AI_THRESHOLD = 0.70`)
and the label text lives in `scoring.py::score_to_label`. I checked that all
three can actually show up: clearly_ai got 0.793 (AI), clearly_human got 0.375
(human), and borderline got 0.432 (unsure).

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

It's not an accurate read, so it's an unsure label. I didn't want it to sound
like we're accusing anyone, because the person reading it might have written
every word.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

This is my Ana-style test text (plain writing from someone whose second
language is English). It's a real false positive, which is why I used it for
the appeal.

> **Correction (unit 8):** this text was written by Claude to imitate Ana's
> style, not by a real person, so it isn't a real false positive. The submit,
> appeal, and log steps below still show the endpoints working the way they
> should.

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I moved to this city two years ago. At first it was hard for me. I did not know many people and my English was not very good. I worked in a small restaurant in the kitchen. The work was hard but the people were kind to me. My manager helped me with my English every day. Now I can talk with customers and I feel more confident. I am proud of how much I learned. I want to study nursing next year.", "creator_id": "ana"}'
```

```json
{
  "combined_score": 0.8382,
  "confidence": 0.6764,
  "content_id": "c_2ef3eab8e336",
  "guess": "ai",
  "label": "This looks like it was written by AI. If you wrote this yourself, you can appeal and a real person will review it.",
  "model_score": 0.8764,
  "style_score": 0.8
}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c_2ef3eab8e336", "reasoning": "I wrote this myself about my own life. English is my second language so I use simple words."}'
```

```json
{
  "content_id": "c_2ef3eab8e336",
  "message": "Thanks, we got your appeal. A real person will review your writing, and the automatic result won't be used against you while that happens.",
  "status": "under_review"
}
```

An appeal with an id that doesn't exist gets a 404 and nothing is logged:

```json
{
  "error": "not_found",
  "message": "We couldn't find a submission with id c_doesnotexist."
}
```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=2"
```

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.8382,
      "content_id": "c_2ef3eab8e336",
      "creator_id": "ana",
      "guess": "ai",
      "label": "This looks like it was written by AI. If you wrote this yourself, you can appeal and a real person will review it.",
      "model_score": 0.8764,
      "status": "decided",
      "style_score": 0.8,
      "timestamp": "2026-11-05T01:35:58+00:00"
    },
    {
      "content_id": "c_2ef3eab8e336",
      "creator_id": "ana",
      "event": "appeal",
      "reasoning": "I wrote this myself about my own life. English is my second language so I use simple words.",
      "status": "under_review",
      "timestamp": "2026-11-05T01:35:58+00:00"
    }
  ]
}
```

The original decision is still there, and the appeal is added right after it
with status `under_review`.

---

## How I Used AI

**Moment 1**

- *What I asked for:* Help writing my five acceptance criteria.
- *What came back:* Claude said it couldn't write them for me because the
  brief says not to, so instead it asked me one question per area (false
  positives, score spread, label coverage, appeals, bad input). After I
  answered, it pointed out which ones someone else couldn't check: I'd said
  "none or maybe 3" for false positives, which is two targets, my "max 3
  sentences" limit would have rejected all three of my own test texts, and
  "8 out of 10" for appeals meant I was ok with losing 2 writers' appeals.
- *What I changed:* I picked 1 in 10 for false positives, made the length
  limit 1500 words, went to 9 out of 10 for appeals, and changed criterion 3
  from "each label at least once" to "at least 2 times" because one of each
  isn't enough data. All the numbers are mine.

**Moment 2**

- *What I asked for:* For Claude to explain the three ways I could combine my
  two signals so I could pick one.
- *What came back:* A plain average, a "disagreement means unsure" rule, and a
  weighted average leaning on one signal, each run on my real test scores. It
  showed the trade-offs, like leaning on the style signal gives the cleanest
  split but it's the easiest one to fool with typos or dashes.
- *What I changed:* I picked rule 2, the disagreement rule, because it matches
  what I wrote in Milestone 1 about only calling something AI if both signals
  agree. I accepted that it pushes some real human writing toward "unsure".

**Moment 3 (unit 8)**

- *What I asked for:* Help diagnosing why 7 of my 10 evasion attacks landed
  in "unsure". Claude gave me possible causes at different stages without
  saying which one was right, and I picked the combining rule, since most of
  them had a big gap between the two signals.
- *What came back:* Claude checked my answer against the numbers. It made a
  table of what a plain 50/50 average would have done, and my rule only
  changed the result for 1 of the 9 (EV04). In the rest, one signal had
  already been fooled, so they would have been "unsure" anyway.
- *What I changed:* I changed my diagnosis to "mostly the signals getting
  fooled" (signal one by typos, short text, and injections, signal two by
  punctuation padding and odd sentence lengths) and kept the table in my
  README as proof.

**Moment 4 (unit 8)**

- *What I asked for:* Help setting up my criterion 1 test, which needs 10
  pieces of my own writing.
- *What came back:* Before using anything, Claude pointed out that the
  "Ana-style plain human" text in my unit 7 README was actually written by
  Claude to imitate the Ana example, and that my README called it a real
  false positive.
- *What I changed:* I added correction notes in the unit 7 sections instead
  of deleting what I wrote, and used my own writing (my SPE21 speech and HUM
  300 paper) for criterion 1 so the test is real.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 10 per minute, 200 per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

I went with 10 a minute and 200 a day because it doesn't take that long. A real
writer who submits, edits, and resubmits a few times in a row won't hit the
limit, and if they ever do they only wait a minute. A script trying to map my
thresholds with 1000 variations gets cut off after 10 a minute and 200 a day,
so it would take at least 5 days instead of a few minutes.

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

Per `creator_id`. If a request has no usable `creator_id`, it counts against
the caller's address instead. The weakness is that `creator_id` is just
something the caller types in, so a script could send a different one every
time and never hit the limit.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```
$ python run_attacks.py --flood 15
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429

5 of 15 were rate limited.
```

The rejections show up in the log too (`GET /log`):

```json
{
  "creator_id": "flood_tester",
  "event": "rejected",
  "limit": "10 per 1 minute",
  "reason": "rate_limited",
  "status": "rejected",
  "timestamp": "2026-11-08T20:36:56+00:00"
}
```

And a request my own route refuses (empty text) gets logged as a rejection
too, with `audit.log_rejection`:

```json
{
  "creator_id": "m1_logcheck",
  "event": "rejected",
  "reason": "empty_text",
  "status": "rejected",
  "status_code": 400,
  "timestamp": "2026-11-08T20:37:06+00:00"
}
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

Full output: `results/attack_run_2026-11-08_1543_before.md` (from
`run_attacks.py::main`). The run was against my unit 7 system with rate limiting
on.

**How I marked them:**

- evasion and prompt injection on AI text: BROKE if the AI text didn't get the
  AI label. I counted "unsure" as broke too, because the AI text still got
  past the AI label, even if it never reached "human".
- false positive (real human writing): BROKE if it got the AI label.
- malformed: BROKE if it crashed, or if junk got a confident label.
- flood: HELD if the limit kicked in and the rejections got logged.

**Totals: 15 broke, 41 held.**

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 3 | 7 |
| false_positive | 8 | 3 | 5 |
| prompt_injection | 6 | 4 | 2 |
| malformed | 20 | 19 | 1 |
| flood_same_creator | 12 | 12 | 0 |
| **total** | **56** | **41** | **15** |

| ID | Family | Targeting | Status | Guess | model | style | Verdict |
|---|---|---|---|---|---|---|---|


Notes:

- Nothing crashed. Every malformed request got a 400 or a normal answer, never a 500.
- PI05 tried to inject fake fields into the audit log. It didn't work: the log
  is still valid JSON on every line and the fake `"guess": "human"` stayed
  inside the text.
- PI04 tried to make the label hostile with a `<script>` tag. My labels are fixed
  sentences, so the text can't change them.
- RQ06 sent `creator_id` as an object and it got logged as `"unknown"`.
- The flood rows went 200 ×10, then 429 ×2, and both 429s are in the log.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

Three real writers called AI (FP03, FP04, FP02), junk called AI (MF05), two
evasions that slipped into unsure (EV01, EV08), an injection that slipped
into unsure (PI02), the log injection that didn't work (PI05), a request my
route refused (RQ03, text was a number), and a rate-limit rejection from the
flood rows.

```json
{"combined_score": 0.8275, "content_id": "c_34dfbaef303a", "creator_id": "attacker_FP03", "guess": "ai", "label": "This looks like it was written by AI. If you wrote this yourself, you can appeal and a real person will review it.", "model_score": 0.8051, "status": "decided", "style_score": 0.8498, "timestamp": "2026-11-08T20:43:10+00:00"}
{"combined_score": 0.8313, "content_id": "c_e597a2fa17a2", "creator_id": "attacker_FP04", "guess": "ai", "label": "This looks like it was written by AI. If you wrote this yourself, you can appeal and a real person will review it.", "model_score": 0.8329, "status": "decided", "style_score": 0.8297, "timestamp": "2026-11-08T20:43:10+00:00"}
{"combined_score": 0.7693, "content_id": "c_188fd46546c6", "creator_id": "attacker_FP02", "guess": "ai", "label": "This looks like it was written by AI. If you wrote this yourself, you can appeal and a real person will review it.", "model_score": 0.7387, "status": "decided", "style_score": 0.8, "timestamp": "2026-11-08T20:43:10+00:00"}
{"combined_score": 0.8988, "content_id": "c_cf6188eacfbb", "creator_id": "attacker_MF05", "guess": "ai", "label": "This looks like it was written by AI. If you wrote this yourself, you can appeal and a real person will review it.", "model_score": 0.9976, "status": "decided", "style_score": 0.8, "timestamp": "2026-11-08T20:43:12+00:00"}
{"combined_score": 0.5256, "content_id": "c_0ff5d6127890", "creator_id": "attacker_EV01", "guess": "unsure", "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.", "model_score": 0.1635, "status": "decided", "style_score": 0.9388, "timestamp": "2026-11-08T20:43:08+00:00"}
{"combined_score": 0.5613, "content_id": "c_c8864c48bad2", "creator_id": "attacker_EV08", "guess": "unsure", "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.", "model_score": 0.2452, "status": "decided", "style_score": 1.0, "timestamp": "2026-11-08T20:43:09+00:00"}
{"combined_score": 0.4764, "content_id": "c_1c084023c39c", "creator_id": "attacker_PI02", "guess": "unsure", "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.", "model_score": 0.2044, "status": "decided", "style_score": 0.7012, "timestamp": "2026-11-08T20:43:11+00:00"}
{"combined_score": 0.5711, "content_id": "c_415944f89d4e", "creator_id": "attacker_PI05", "guess": "unsure", "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.", "model_score": 0.6401, "status": "decided", "style_score": 0.5021, "timestamp": "2026-11-08T20:43:11+00:00"}
{"creator_id": "attacker_RQ03", "event": "rejected", "reason": "not_text", "status": "rejected", "status_code": 400, "text_type": "int", "timestamp": "2026-11-08T20:43:13+00:00"}
{"creator_id": "attacker_flood", "event": "rejected", "limit": "10 per 1 minute", "reason": "rate_limited", "status": "rejected", "timestamp": "2026-11-08T20:43:14+00:00"}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

FP03, "a non-native English speaker writing carefully". This is basically Ana
from my Milestone 1 notes, and my system did exactly what I was afraid of. It
got model 0.81 and style 0.85, combined 0.83, and the label said:

> This looks like it was written by AI. If you wrote this yourself, you can
> appeal and a real person will review it.

The text:

> I want to describe my experience of the first month in this country. The weather was very different from my home. I did not expect the rain to continue for so many days. My colleagues were kind and they helped me to find an apartment. I am still learning the words that people use in the office. Sometimes I do not understand the jokes. But I am happy that I came here and I think it was a good decision for my family.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labeled high-confidence AI | at most 1 of 10, every run | 1/10 | 1/10 | 1/10 | MET |
| 2. clearly_ai minus clearly_human (combined) | at least 0.30, every run | 0.41 | 0.41 | 0.41 | MET |
| 3. Each label shows up out of 10 texts | every label at least 2 times | AI 2, unsure 7, human 1 | AI 2, unsure 7, human 1 | AI 2, unsure 7, human 1 | MISSED |
| 4. Real appeals recorded, fake id gets an error and changes nothing | at least 9 of 10, and fake id refused | 10/10, fake 404 | 10/10, fake **200** | 10/10, fake **200** | MISSED |
| 5. Bad input gets a 400, not a crash | 7 of 7, every time | 7/7 | 7/7 | 7/7 | MET |

All three runs came out the same for every criterion. That's expected, since
nothing in either signal is random.

How I ran them: criteria 1, 2, 3 and 5 are in `scenarios.py` and ran with
`python run_eval.py --label before` (output: `results/run_2026-11-08_1559_before.md`).
Criterion 4 can't be tested by sending text alone, so I tested it with
`python check_appeals.py before results/appeals_2026-11-08_before.md`. It
submits 10 texts, appeals each one, checks `GET /log` shows the appeal, then
sends one appeal with a fake id.

My own writing for criterion 1 is 3 pieces from my SPE21 speech and 7 from my
HUM 300 final paper, no AI help. For criterion 3, 7 texts come from the class
samples and my speech, and 3 are parts of a few sentences I wrote about my day.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

Criterion 1, the one piece of my writing that got the AI label (`run_eval.py::main`,
trial 1). It's the "arriving in New York" part of my speech. Combined score is
0.71, just over my 0.70 line:

```json
{
  "status": 200,
  "guess": "ai",
  "model_score": 0.8325,
  "style_score": 0.5927,
  "sent": "I was shocked by what I saw, when I got out of the airplane. All these"
}
```

Criterion 2 (`run_eval.py::main`, trial 1). Combined: 0.79 vs 0.38, gap 0.41.

```json
[
  {
    "status": 200,
    "guess": "ai",
    "model_score": 0.7544,
    "style_score": 0.8314,
    "sent": "The importance of effective time management cannot be overstated in to"
  },
  {
    "status": 200,
    "guess": "human",
    "model_score": 0.4445,
    "style_score": 0.0568,
    "sent": "I didn't sleep. Not properly, anyway — I lay there listening to the bo"
  }
]
```

Criterion 3, the only text that got the human label (`run_eval.py::main`, trial 1).
None of my own day writing got it, all three were unsure:

```json
[
  {
    "status": 200,
    "guess": "human",
    "model_score": 0.4445,
    "style_score": 0.0568,
    "sent": "I didn't sleep. Not properly, anyway — I lay there listening to the bo"
  },
  {
    "status": 200,
    "guess": "unsure",
    "model_score": 0.7401,
    "style_score": 0.5102,
    "sent": "Today , I woke up at around 7:40am and layed in bed for about 10 minut"
  },
  {
    "status": 200,
    "guess": "unsure",
    "model_score": 0.214,
    "style_score": 0.8,
    "sent": "there they served us lunch about 3 hours in and now im waiting here un"
  }
]
```

Criterion 4 (`check_appeals.py`, trial 2). The fake id that should have been
refused got recorded as an appeal. The log lines for it:

```json
{"timestamp": "2026-11-08T20:59:42+00:00", "creator_id": "unknown", "event": "rejected", "status": "rejected", "reason": "appeal_unknown_content_id", "content_id": "c_fake000000", "status_code": 404}
{"timestamp": "2026-11-08T20:59:43+00:00", "content_id": "c_fake000000", "creator_id": "unknown", "event": "appeal", "status": "under_review", "reasoning": "test"}
{"timestamp": "2026-11-08T20:59:44+00:00", "content_id": "c_fake000000", "creator_id": "unknown", "event": "appeal", "status": "under_review", "reasoning": "test"}
```

Criterion 5 (`run_eval.py::main`, trial 1), all 7 bad bodies got a 400:

```json
[
  {
    "status": 400,
    "sent": "(empty text)"
  },
  {
    "status": 400,
    "sent": "     "
  },
  {
    "status": 400,
    "sent": "{\"creator_id\": \"eval_bad_missing\"}"
  },
  {
    "status": 400,
    "sent": "{\"text\": null, \"creator_id\": \"eval_bad_null\"}"
  },
  {
    "...": "3 more, all 400"
  }
]
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

**How I decided each verdict**

1. **MET.** 1 of my 10 pieces got the AI label in all three runs, and my
   target was at most 1. It's a close call though: that piece (the "arriving
   in New York" part of my speech) scored 0.71, right over my 0.70 line.
2. **MET.** The gap was 0.41 in all three runs, and the target was at least 0.30.
3. **MISSED.** The human label showed up only 1 time out of 10, in every run.
   The target was at least 2 for every label.
4. **MISSED.** All 10 real appeals were recorded every run, but the fake id
   got accepted in runs 2 and 3. My criterion says a fake id gets an error and
   changes nothing, and it has to hold every run.
5. **MET.** 7 of 7 bad inputs got a 400 in all three runs, no crashes.

**Diagnosis 1: real human writing called AI (FP02, FP03, FP04, FP05, FP06, and my
speech piece for criterion 1)**

Stage: **signal one and signal two, both.** These were formal, careful, or
plain writing: a formal register, a non-native speaker writing carefully, a
student essay to a rubric, tech docs, a template. Signal one gave them 0.74 to
0.88 because careful writing uses common words in common orders, so GPT-2
finds it predictable. Signal two gave them 0.67 to 0.85 because that kind of
writing has even sentence lengths and not much dash or semicolon punctuation,
which is exactly what my style signal reads as AI. Both signals made the same
mistake for the same reason, so they agreed, and my disagreement rule only
steps in when they disagree. My speech piece is the same thing in a smaller
way: model 0.83, style 0.59, combined 0.71.

**Diagnosis 2: AI text slipping into "unsure" (EV01, EV02, EV04, EV05, EV06,
EV07, EV08, PI01, PI02)**

Stage: **mostly the signals getting fooled, and the combining rule for one of
them.** I first thought it was my combining rule, but when I checked what a
plain 50/50 average would have done, it only changed the result for 1 of 9:

| Attack | model | style | Rule kicked in? | Plain average | Label without my rule |
|---|---|---|---|---|---|
| EV04 | 0.61 | 0.94 | yes | 0.78 | AI |
| EV01 (typos) | 0.16 | 0.94 | yes | 0.55 | unsure |
| EV08 (short) | 0.25 | 1.00 | yes | 0.62 | unsure |
| EV07 (punctuation padding) | 0.59 | 0.28 | yes | 0.44 | unsure |
| PI02 | 0.20 | 0.70 | yes | 0.45 | unsure |
| EV02 (broken-up sentences) | 0.59 | 0.58 | no | 0.59 | unsure |
| EV05 (heavy editing) | 0.32 | 0.52 | no | 0.42 | unsure |
| EV06 (one long, one short sentence) | 0.57 | 0.47 | no | 0.52 | unsure |
| PI01 | 0.46 | 0.76 | no | 0.61 | unsure |

- **Signal one** got fooled in EV01, EV08, PI01 and PI02. Typos, a very short
  text, and the injection sentences stuck on the front all make GPT-2 more
  "surprised", so its score dropped even though the text is AI. The injections
  didn't work as instructions (nothing in my system reads instructions), they
  worked because the extra sentences changed the statistics.
- **Signal two** got fooled in EV07 and EV06. Padding with punctuation raises my
  punctuation density, and one very long sentence next to a very short one
  raises the sentence length spread, and both of those read as human to it.
- In EV02 and EV05, both signals came down to the middle together.
- **The combining rule** only decided EV04. Without it, EV04 would have been
  labeled AI.

**Diagnosis 3: criterion 3, only one "human" label**

Stage: **signal two.** The only text that got the human label was
clearly_human, with a style score of 0.06. My three "my day" pieces got style
scores of 0.51, 0.62 and 0.80. They're short, and part 3 is one sentence.
Short text has hardly any sentence length spread (one sentence gets 0.5 by my
own rule), not much punctuation, and almost every word is unique, which my
vocab measure reads as AI. So my style signal keeps pushing short, casual
human writing up toward the middle, and it almost never gets below 0.40.

**Diagnosis 4: criterion 4, the fake appeal id**

Stage: **the route (`app.py::appeal`).** In unit 8 Milestone 1 I started
logging rejected appeals with `audit.log_rejection`, and that entry includes
the `content_id`. `/appeal` checks whether a submission exists by asking "is
there any log entry with this id?" (`audit.entries_for`). The first time a
fake id is sent, there isn't one, so it gets a 404, but the 404 itself writes
a log entry with that id. The second time, `/appeal` finds that rejection
entry, thinks the submission exists, and records the appeal. So a fake id
gets refused once and accepted every time after that.

**Diagnosis 5: MF05, junk called AI**

Stage: **the route.** MF05 is a single "word" that's 60,000 characters long. My
length check counts words (max 1500) and this is 1 word, so it went straight
to the signals. Signal one gave it 0.998 and signal two 0.8, so it got the
high-confidence AI label for something that isn't writing at all.

**The pattern**

Most of my failures come from the two signals, not from the combining rule or
the labels. Both signals read *the shape of plain writing* as AI: predictable
words for signal one, even sentences and little punctuation for signal two.
That one problem explains the false positives (careful human writing looks
like AI to both) and criterion 3 (short casual writing never gets low enough
to be called human). It works the other way for evasions: anything that
messes up the shape, like typos, punctuation, or odd sentence lengths, pulls
one signal down and the AI text lands in unsure. The two route bugs (the fake
appeal id and MF05) are separate, smaller problems.

---

## The Improvement

**What I changed:** One line in `config.py`: `AI_THRESHOLD` went from 0.70 to
0.80. Now the high-confidence AI label only shows up above 0.80, and the
unsure band is 0.40 to 0.80. Nothing else changed: same signals, same
weights, same combining rule, same label text.

**Which diagnosis pointed at it:** Diagnosis 1. Five real human texts
(FP02-FP06) got the AI label with combined scores between 0.77 and 0.83, and
one piece of my own speech got 0.71. In my Milestone 1 notes I said calling a
real writer AI is the worst mistake this system can make, so I went after
that one. The real fix would be in the signals, since they both read plain
writing as AI, but that's a much bigger change and I wouldn't be able to tell
which part of it helped. Moving the threshold is one change I can measure.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

Full output: `results/attack_run_2026-11-08_1614_after.md`. Same rules for
held and broke as before. Every score came out exactly the same as the before
run (the signals aren't random), so only the labels moved.

| Family | Before: held / broke | After: held / broke |
|---|---|---|
| evasion | 3 / 7 | 1 / 9 |
| false_positive | 3 / 5 | **6 / 2** |
| prompt_injection | 4 / 2 | 3 / 3 |
| malformed | 19 / 1 | 19 / 1 |
| flood_same_creator | 12 / 0 | 12 / 0 |
| **total** | **41 / 15** | **41 / 15** |

What changed between the two runs (the other 50 came out the same):

| ID | What it is | combined | Before | After |
|---|---|---|---|---|
| FP02 | human, formal register | 0.77 | ai (BROKE) | unsure (HELD) |
| FP05 | human, technical docs | 0.78 | ai (BROKE) | unsure (HELD) |
| FP06 | human, formal template | 0.78 | ai (BROKE) | unsure (HELD) |
| EV03 | AI with a pasted quote | 0.70 | ai (HELD) | unsure (BROKE) |
| EV09 | AI with a human opening paragraph | 0.75 | ai (HELD) | unsure (BROKE) |
| PI03 | AI with a "note to the reviewer" | 0.71 | ai (HELD) | unsure (BROKE) |

Still broken after: FP03 (0.83) and FP04 (0.83) are still called AI, and the
only AI attack still caught is EV10.

**My five criteria, after** (`run_eval.py --label after` →
`results/run_2026-11-08_1614_after.md`, appeals → `results/appeals_2026-11-08_after.md`)

| Criterion | Target | Before (runs 1/2/3) | After (runs 1/2/3) | Verdict before → after |
|---|---|---|---|---|
| 1. My own writing labeled AI | at most 1 of 10 | 1, 1, 1 | 0, 0, 0 | MET → MET |
| 2. clearly_ai minus clearly_human | at least 0.30 | 0.41, 0.41, 0.41 | 0.41, 0.41, 0.41 | MET → MET |
| 3. Each label at least 2 of 10 | every label ≥ 2 | AI 2, unsure 7, human 1 (all 3 runs) | AI **0**, unsure 9, human 1 (all 3 runs) | MISSED → MISSED (worse) |
| 4. Appeals recorded, fake id refused | ≥ 9 of 10 + fake refused | 10/10, fake refused only in run 1 | 10/10, fake accepted in all 3 | MISSED → MISSED |
| 5. Bad input gets a 400 | 7 of 7 | 7/7 ×3 | 7/7 ×3 | MET → MET |

Criterion 4 got worse only because the fake id from the before run was still
in the log, so it was accepted from the first try. That's the same bug from
Diagnosis 4, not something the threshold did. Criterion 2 measures the gap in
scores, not labels, so it didn't move, even though clearly_ai now gets
"unsure" instead of "AI".

**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->

It helped with the thing I cared about most, and it made the other side
worse by exactly the same amount. Real writers called AI in the attack set
went from 5 to 2, and my own writing went from 1 in 10 to 0. But 3 AI texts
that used to get caught now get "unsure" (EV03, EV09, PI03), so the total
broken stayed at 15. Criterion 3 also got worse: now not even clearly_ai gets
the AI label, so the AI label showed up 0 times out of 10. So it didn't make
the system better overall, it moved who pays for the mistakes, from real
writers to the site letting more AI text through. For a writing site I think
that's the right direction, but it's a trade, not a fix.

---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

Why I stopped on all of these: the brief only allows one change in unit 8, so
the threshold was my one change. Everything below is what I'd do next, in the
order I'd do it.

1. **Criterion 4, the fake appeal id (route).** This is the first thing I'd
   fix because it's a real bug and it's easy. `/appeal` should only count a
   `decided` entry as proof that a submission exists, not any entry with that
   `content_id`. That way a rejected appeal can't make a fake id look real.
   I didn't fix it because it wasn't my one change.

2. **FP03 and FP04 still called AI, and criterion 1 was close (signals one and
   two).** Raising the threshold more would fix these two but lose even more AI
   text. The real problem is that both signals read careful, plain writing as
   AI. I'd look at signal two first: the vocab measure (which I already flipped
   in unit 7 based on only three texts) and how it treats short text. I stopped
   because changing a signal is a bigger change and needs its own before and
   after.

3. **Criterion 3, the human label almost never shows up, and now the AI label
   doesn't show up either (signal two + my threshold).** Short casual writing
   gets style scores of 0.5-0.8, so it can't get below 0.40. I'd fix signal
   two's short-text handling (one sentence gets 0.5 for spread, and every word
   being unique reads as AI). The AI label disappearing is the cost of my
   threshold change, so I'd only get it back by making the signals separate
   better, not by moving the line back.

4. **Evasions and injections landing in unsure (EV01-EV09, PI01-PI03; signals
   one and two).** Typos, a pasted quote, an added human paragraph, or extra
   sentences on top all pull one signal down. I'd probably accept most of
   these. They land in "unsure", not "human", so nobody gets a "this is
   human" stamp on AI text, and with my threshold at 0.80 that's partly on
   purpose.

5. **MF05, a 60,000-character single word called AI (route).** I'd add a
   character limit next to the 1500-word limit, and maybe reject text that has
   no real words in it. Small fix, I stopped because of the one-change rule.

**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

I'd go with fewer wrong accusations, like my 0.80 threshold does, because
being told your own writing was made by a machine hurts a real person a lot
more than some AI text slipping through hurts the site. The ones who pay for
it are the site and its readers, who will see more AI writing labeled
"unsure" instead of caught, and honest writers competing with it.


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
