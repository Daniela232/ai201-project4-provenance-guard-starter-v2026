# Criterion 4 appeal trials — before

- run 2026-11-08 15:59
- each trial: 10 submissions, appeal each one, check GET /log shows an appeal entry with status under_review, then 1 appeal with a fake content_id
| Trial | Real appeals recorded | Fake id status | Fake id changed nothing |
|---|---|---|---|
| 1 | 10/10 | 404 | yes |
| 2 | 10/10 | 200 | NO |
| 3 | 10/10 | 200 | NO |


## Trial 1

- real appeals recorded: **10/10**
- fake id: status 404, appeal entries for it in the log: 0 -> OK

```json
[
  {
    "content_id": "c_1060ba3e0ada",
    "submit": 200,
    "appeal": 200,
    "status": "under_review",
    "in_log": true
  },
  {
    "content_id": "c_e3bf1037eaed",
    "submit": 200,
    "appeal": 200,
    "status": "under_review",
    "in_log": true
  },
  {
    "...": "8 more like these"
  }
]
```

Fake id response:

```json
{
  "error": "not_found",
  "message": "We couldn't find a submission with id c_fake000000."
}
```

## Trial 2

- real appeals recorded: **10/10**
- fake id: status 200, appeal entries for it in the log: 1 -> WRONG

```json
[
  {
    "content_id": "c_ff60f8cc629a",
    "submit": 200,
    "appeal": 200,
    "status": "under_review",
    "in_log": true
  },
  {
    "content_id": "c_4a4759208087",
    "submit": 200,
    "appeal": 200,
    "status": "under_review",
    "in_log": true
  },
  {
    "...": "8 more like these"
  }
]
```

Fake id response:

```json
{
  "content_id": "c_fake000000",
  "message": "Thanks, we got your appeal. A real person will review your writing, and the automatic result won't be used against you while that happens.",
  "status": "under_review"
}
```

## Trial 3

- real appeals recorded: **10/10**
- fake id: status 200, appeal entries for it in the log: 2 -> WRONG

```json
[
  {
    "content_id": "c_b07f691205dc",
    "submit": 200,
    "appeal": 200,
    "status": "under_review",
    "in_log": true
  },
  {
    "content_id": "c_ed3f1254b4cd",
    "submit": 200,
    "appeal": 200,
    "status": "under_review",
    "in_log": true
  },
  {
    "...": "8 more like these"
  }
]
```

Fake id response:

```json
{
  "content_id": "c_fake000000",
  "message": "Thanks, we got your appeal. A real person will review your writing, and the automatic result won't be used against you while that happens.",
  "status": "under_review"
}
```
