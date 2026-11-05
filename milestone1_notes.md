# Milestone 1 Notes: Tracing a Submission

These are my planning notes from before I built the scoring, the labels, or the appeal endpoint.

## 1. The path a submission takes

1. Someone sends a `POST /submit` request with JSON that has the `text` and their `creator_id`.
2. `app.py::submit` checks the input first. If the body isn't a JSON object, or the text is missing, empty, or not a string, it sends back a 400 error and stops there. This way the signals only ever get real text.
3. Signal one (`detector.py::model_signal`) runs the text through GPT-2 and checks how predictable the wording is. It gives back a `model_score` from 0 to 1, where higher means more likely AI.
4. Signal two (`stylometry.py::style_signal`) looks at the text's shape: how much sentence lengths vary, how many different words are used, and punctuation. It doesn't understand what the words mean. It also gives back a score from 0 to 1 (`style_score`), where higher means more likely AI.
5. `scoring.py::combine_signals` combines the two scores into one `combined_score`, a guess (`ai`, `human`, or `unsure`), and a confidence number.
6. `scoring.py::score_to_label` turns that number into the actual sentence the reader sees. There are three possible labels: high-confidence AI, high-confidence human, or unsure.
7. The service creates a `content_id`, writes everything to `logs/audit.jsonl` with status `decided` using `audit.py::log_decision`, and sends the same info back as JSON.

If the writer thinks the result is wrong, they can send a `POST /appeal` with their `content_id` and their reasoning. That gets saved in the log and the status changes to `under_review`.

## 2. The two signals

### Signal one: the model signal (detector.py)

**What it measures:** Perplexity, basically how surprised GPT-2 is by each next word. Low surprise turns into a high AI score.

**Why it might be different for humans vs. AI:** AI writing is made by choosing likely next words, so another language model finds it really predictable. People tend to make weirder, more personal word choices.

**What it can't see:** Being predictable doesn't mean something was written by AI. Plain writing with simple words and normal sentences can score as AI, like someone writing in their second language or a younger writer. AI text that uses unusual words could score as human. It also cuts off really long texts and can't score really short ones.

I actually saw this already in my first test. The clearly human example scored 0.445, which was more AI-like than the borderline example at 0.349. So signal one by itself got those two backwards.

### Signal two: the style signal (stylometry.py)

**What it measures:** How the text is shaped: sentence length variation, vocabulary variety (unique words compared to total words), and how much punctuation is used.

**Why it might be different for humans vs. AI:** AI writing usually has sentences that are all about the same medium length and a narrower vocabulary. Human writing is more uneven, like a really short sentence right next to a really long one, with dashes, colons, and quotes mixed in.

**What it can't see:** It can't actually read. Anything that changes the shape but not the meaning will change its score, like adding typos, splitting sentences up, or pasting in a quote. That's really easy for someone to do on purpose. It could also think formal human writing like essays or reports is AI, because those tend to have even sentences.

### Why use both

They get fooled by different things. Signal one gets fooled by word choice, and signal two gets fooled by the shape of the text. So I think something should only get a confident "AI" label if both signals agree.

## 3. Tracing a false positive

Say there's a writer named Ana who writes short personal essays in English, which is her second language. She sticks to words she's confident about and writes short, clear sentences that are around the same length. She submits an essay she wrote herself.

1. Her text passes the input check.
2. Signal one finds her writing really predictable since she uses common words in common orders, so it gives her something like 0.75. That's close to what the clearly AI example got (0.754).
3. Signal two sees similar-length sentences and a smaller vocabulary, so it also leans AI, maybe around 0.65.
4. Combined, she ends up around 0.70. Both signals agreed, but they were both wrong for the same reason: they took plain writing as a sign of AI.
5. If 0.70 falls in my high-confidence AI range, the site basically tells a real person that her writing was probably made by a machine. That's the worst mistake this system can make.
6. What she can do about it: her response included a `content_id`, so she can send a `POST /appeal` with that id and explain herself. Her item moves to `under_review` and a person looks at it instead of the detector.

**What this means for my thresholds:**

- The high-confidence AI range needs to start pretty high, above 0.70, so someone like Ana lands in "unsure" instead of getting called AI.
- The unsure range should be wide. Being unsure is a lot less harmful than wrongly accusing someone.
- Every label, even the AI one, should tell the writer how to appeal so they don't have to go looking for it.

All of Ana's numbers above are made up to show the idea. They're not real measurements.

## 4. Endpoint shapes

### POST /submit

**What goes in:**

| Field | Type | Required? | Notes |
|---|---|---|---|
| `text` | string | yes | Can't be empty or just spaces. Needs to be at least a few words because the detector needs 3+ tokens. |
| `creator_id` | string | no | Who wrote it. If it's missing it becomes `"unknown"`. |

**What comes back (200):**

| Field | Type | What it means |
|---|---|---|
| `content_id` | string | Unique id for the submission, like `c_b90a87297e0a`. You need it to appeal. |
| `guess` | string | `"ai"`, `"human"`, or `"unsure"` |
| `confidence` | number 0-1 | How sure the system is about the guess |
| `label` | string | The full sentence the reader sees |
| `model_score` | number 0-1 | Signal one. Higher = more AI-like |
| `style_score` | number 0-1 | Signal two. Higher = more AI-like |
| `combined_score` | number 0-1 | Both signals combined. Higher = more AI-like |

**Errors:**

| Status | error | When |
|---|---|---|
| 400 | `bad_request` | The body isn't a JSON object, or text is missing, empty, or not a string |
| 400 | `too_short` | The text is too short for the detector to score |

Errors always look like `{"error": "...", "message": "..."}`.

### POST /appeal

**What goes in:**

| Field | Type | Required? | Notes |
|---|---|---|---|
| `content_id` | string | yes | Has to match a `content_id` that `/submit` gave back |
| `reasoning` | string | yes | The writer's explanation. Can't be empty. |

**What comes back (200):**

| Field | Type | What it means |
|---|---|---|
| `content_id` | string | The item that got appealed |
| `status` | string | Always `"under_review"` |
| `message` | string | A plain-English confirmation telling the writer their appeal was received and a person will review it |

**Errors:**

| Status | error | When |
|---|---|---|
| 400 | `bad_request` | The body isn't a JSON object, or `content_id` or `reasoning` is missing or empty |
| 404 | `not_found` | There's no submission with that `content_id` in the log |

The appeal doesn't delete or change the original decision. It just gets added to the log as a new entry after it.
