# Criterion 4 appeal trials — after

- run 2026-11-08 16:14
- each trial: 10 submissions, appeal each one, check GET /log shows an appeal entry with status under_review, then 1 appeal with a fake content_id
| Trial | Real appeals recorded | Fake id status | Fake id changed nothing |
|---|---|---|---|
| 1 | 10/10 | 200 | NO |
| 2 | 10/10 | 200 | NO |
| 3 | 10/10 | 200 | NO |


## Trial 1

- real appeals recorded: **10/10**
- fake id: status 200, appeal entries for it in the log: 3 -> WRONG

```json
[
  {
    "content_id": "c_66ed9d07e2ca",
    "submit": 200,
    "appeal": 200,
    "status": "under_review",
    "in_log": true
  },
  {
    "content_id": "c_f4852ce3e018",
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

## Trial 2

- real appeals recorded: **10/10**
- fake id: status 200, appeal entries for it in the log: 4 -> WRONG

```json
[
  {
    "content_id": "c_f35abd466e82",
    "submit": 200,
    "appeal": 200,
    "status": "under_review",
    "in_log": true
  },
  {
    "content_id": "c_bcda818dcbe3",
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
- fake id: status 200, appeal entries for it in the log: 5 -> WRONG

```json
[
  {
    "content_id": "c_596558913848",
    "submit": 200,
    "appeal": 200,
    "status": "under_review",
    "in_log": true
  },
  {
    "content_id": "c_3278ff5d9c5b",
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
