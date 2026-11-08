# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-08 16:14
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c_78b44cc87d1f` | unsure | 0.051 || BROKE |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c_71a8dae53893` | unsure | 0.177 || BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c_b9fa676d64a4` | unsure | 0.400 || BROKE |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c_4a93bd42613f` | unsure | 0.276 || BROKE |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c_c9d3074e27fe` | unsure | 0.161 || BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c_38c354ca87a0` | unsure | 0.046 || BROKE |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c_85aa7d816989` | unsure | 0.065 || BROKE |
| EV08 | evasion | signal one: text below the token window | 200 | `c_950fff26d1d9` | unsure | 0.123 || BROKE |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `c_a469d564bf4e` | unsure | 0.508 || BROKE |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c_ffbaaf40e63b` | ai | 0.725 || HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c_1738cf9f3d41` | unsure | 0.367 || HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `c_70b9a701cb0a` | unsure | 0.539 || HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `c_1378efde01f9` | ai | 0.655 || BROKE |
| FP04 | false_positive | a student essay written to a rubric | 200 | `c_fcd0cb39751c` | ai | 0.663 || BROKE |
| FP05 | false_positive | technical documentation written by a person | 200 | `c_1e4c1e36f8b5` | unsure | 0.566 || HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `c_40f51fdf505a` | unsure | 0.556 || HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c_05a84c7298ae` | unsure | 0.190 || HELD |
| FP08 | false_positive | very short genuine human submission | 200 | `c_7d02a5f9e8d0` | unsure | 0.123 || HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c_5fc90f105f45` | unsure | 0.222 || BROKE |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c_01f818004c98` | unsure | 0.047 || BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c_61b7a79ed7bc` | unsure | 0.429 || BROKE |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c_bf0101312075` | unsure | 0.089 || HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `c_0d001c903029` | unsure | 0.142 || HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c_f72c5e412a47` | unsure | 0.316 || HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — || HELD |
| MF02 | malformed | text is a single character | 400 | `—` | — | — || HELD |
| MF03 | malformed | text is control characters | 200 | `c_0bbcfbb0f232` | unsure | 0.100 || HELD |
| MF04 | malformed | text is only punctuation | 200 | `c_37fbc8429504` | unsure | 0.094 || HELD |
| MF05 | malformed | text is a very long single word | 200 | `c_eca3ab0b03dd` | ai | 0.798 || BROKE |
| MF06 | malformed | text is emoji only | 200 | `c_e09ba9aa4c8c` | unsure | 0.298 || HELD |
| MF07 | malformed | text is right-to-left script | 200 | `c_1624e8987bc7` | unsure | 0.253 || HELD |
| MF08 | malformed | text is 60,000 characters | 400 | `—` | — | — || HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — || HELD |
| RQ02 | malformed | no creator_id | 200 | `c_f773a40ce3a7` | unsure | 0.020 || HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — || HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — || HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — || HELD |
| RQ06 | malformed | creator_id is an object | 200 | `c_742877a91b84` | unsure | 0.075 || HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — || HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — || HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — || HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — || HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — || HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — || HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_841dd4259f73` | unsure | 0.086 || HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_f465505f445a` | unsure | 0.086 || HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_a4bf53bff92f` | unsure | 0.086 || HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_548e77cf53cf` | unsure | 0.086 || HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_c0b3bd341bbb` | unsure | 0.086 || HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_6c62bc0c1e11` | unsure | 0.086 || HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_19341f98e142` | unsure | 0.086 || HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_480271cd8041` | unsure | 0.086 || HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_dc310430b9a2` | unsure | 0.086 || HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_370c551b6216` | unsure | 0.086 || HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — || HELD |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c_78b44cc87d1f",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.0512,
  "model_score": 0.1635,
  "style_score": 0.9388,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c_71a8dae53893",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.1774,
  "model_score": 0.5943,
  "style_score": 0.583,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "c_b9fa676d64a4",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.4002,
  "model_score": 0.6662,
  "style_score": 0.7339,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c_4a93bd42613f",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.276,
  "model_score": 0.6114,
  "style_score": 0.9405,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "c_c9d3074e27fe",
  "creator_id": "attacker_EV05",
  "guess": "unsure",
  "confidence": 0.161,
  "model_score": 0.3212,
  "style_score": 0.5178,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "c_38c354ca87a0",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.0456,
  "model_score": 0.5727,
  "style_score": 0.4728,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "c_85aa7d816989",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.0646,
  "model_score": 0.5862,
  "style_score": 0.2845,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "c_950fff26d1d9",
  "creator_id": "attacker_EV08",
  "guess": "unsure",
  "confidence": 0.1226,
  "model_score": 0.2452,
  "style_score": 1.0,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "c_a469d564bf4e",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5084,
  "model_score": 0.7042,
  "style_score": 0.8041,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "c_ffbaaf40e63b",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.7254,
  "model_score": 0.9792,
  "style_score": 0.7463,
  "label": "This looks like it was written by AI. If you wrote this yourself, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "c_1738cf9f3d41",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.3666,
  "model_score": 0.6175,
  "style_score": 0.7491,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "c_70b9a701cb0a",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.5386,
  "model_score": 0.7387,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "c_1378efde01f9",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "confidence": 0.655,
  "model_score": 0.8051,
  "style_score": 0.8498,
  "label": "This looks like it was written by AI. If you wrote this yourself, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "c_fcd0cb39751c",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.6626,
  "model_score": 0.8329,
  "style_score": 0.8297,
  "label": "This looks like it was written by AI. If you wrote this yourself, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "c_1e4c1e36f8b5",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.5662,
  "model_score": 0.8005,
  "style_score": 0.7657,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c_40f51fdf505a",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.5562,
  "model_score": 0.8814,
  "style_score": 0.6748,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "c_05a84c7298ae",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.1898,
  "model_score": 0.8816,
  "style_score": 0.4982,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c_7d02a5f9e8d0",
  "creator_id": "attacker_FP08",
  "guess": "unsure",
  "confidence": 0.1232,
  "model_score": 0.3223,
  "style_score": 0.924,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "c_5fc90f105f45",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.2218,
  "model_score": 0.4625,
  "style_score": 0.7594,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "c_01f818004c98",
  "creator_id": "attacker_PI02",
  "guess": "unsure",
  "confidence": 0.0472,
  "model_score": 0.2044,
  "style_score": 0.7012,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c_61b7a79ed7bc",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.4294,
  "model_score": 0.5943,
  "style_score": 0.8351,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c_bf0101312075",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.0886,
  "model_score": 0.4998,
  "style_score": 0.5888,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "c_0d001c903029",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.1422,
  "model_score": 0.6401,
  "style_score": 0.5021,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c_f72c5e412a47",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.3162,
  "model_score": 0.5583,
  "style_score": 0.7579,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "c_0bbcfbb0f232",
  "creator_id": "attacker_MF03",
  "guess": "unsure",
  "confidence": 0.1,
  "model_score": 0.0,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "c_37fbc8429504",
  "creator_id": "attacker_MF04",
  "guess": "unsure",
  "confidence": 0.0944,
  "model_score": 0.0112,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "c_eca3ab0b03dd",
  "creator_id": "attacker_MF05",
  "guess": "ai",
  "confidence": 0.7976,
  "model_score": 0.9976,
  "style_score": 0.8,
  "label": "This looks like it was written by AI. If you wrote this yourself, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "BROKE"
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "c_e09ba9aa4c8c",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.2984,
  "model_score": 0.9969,
  "style_score": 0.6,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c_1624e8987bc7",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.2532,
  "model_score": 0.9064,
  "style_score": 0.6,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 200,
  "content_id": "c_f773a40ce3a7",
  "creator_id": null,
  "guess": "unsure",
  "confidence": 0.0198,
  "model_score": 0.2395,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 200,
  "content_id": "c_742877a91b84",
  "creator_id": {
    "id": "x"
  },
  "guess": "unsure",
  "confidence": 0.0754,
  "model_score": 0.0492,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "c_841dd4259f73",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0856,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c_f465505f445a",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0856,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c_a4bf53bff92f",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0856,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c_548e77cf53cf",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0856,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "c_c0b3bd341bbb",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0856,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "c_6c62bc0c1e11",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0856,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "c_19341f98e142",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0856,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "c_480271cd8041",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0856,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "c_dc310430b9a2",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0856,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "c_370c551b6216",
  "creator_id": "attacker_flood",
  "guess": "unsure",
  "confidence": 0.0856,
  "model_score": 0.0287,
  "style_score": 0.8,
  "label": "We couldn't get an accurate read on this one, so we can't say whether a person or AI wrote it. This is not an accusation. If you have questions, you can appeal and a real person will review it.",
  "error": null,
  "verdict": "HELD"
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```
