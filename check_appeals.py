"""Criterion 4 check (I test appeals by hand with this, since run_eval.py only sends text).

    python check_appeals.py before results/appeals_<date>_before.md

Each trial: 10 submissions, appeal each one, check GET /log shows an appeal
entry with status under_review, then 1 appeal with a fake content_id.
"""
import json, sys, urllib.request, datetime as dt
U="http://127.0.0.1:5000"
label=sys.argv[1]; out=sys.argv[2]
def call(path, body=None):
    req=urllib.request.Request(U+path, data=None if body is None else json.dumps(body).encode(),
                               headers={"Content-Type":"application/json"})
    try: r=urllib.request.urlopen(req); return r.status, json.load(r)
    except urllib.error.HTTPError as e: return e.code, json.load(e)
TEXT=("I wrote this paragraph myself to test the appeal path. It has a few plain sentences, "
      "nothing fancy, and I just need a real content_id back so I can appeal it.")
lines=[f"# Criterion 4 appeal trials — {label}", "", f"- run {dt.datetime.now():%Y-%m-%d %H:%M}",
       "- each trial: 10 submissions, appeal each one, check GET /log shows an appeal entry with status under_review, then 1 appeal with a fake content_id", ""]
summary=[]
for t in (1,2,3):
    ok=0; detail=[]
    for i in range(1,11):
        st,sub=call("/submit", {"text":TEXT, "creator_id":f"appeal_{label}_t{t}_{i}"})
        cid=sub.get("content_id")
        ast,ap=call("/appeal", {"content_id":cid, "reasoning":"I wrote this myself."})
        log=call("/log?limit=400")[1]["entries"]
        logged=any(e.get("content_id")==cid and e.get("event")=="appeal" and e.get("status")=="under_review" for e in log)
        good = st==200 and ast==200 and ap.get("status")=="under_review" and logged
        ok+=good; detail.append({"content_id":cid,"submit":st,"appeal":ast,"status":ap.get("status"),"in_log":logged})
    before=len(call("/log?limit=100000")[1]["entries"])
    fst,fake=call("/appeal", {"content_id":"c_fake000000","reasoning":"test"})
    after=call("/log?limit=100000")[1]["entries"]
    fake_appeals=[e for e in after if e.get("content_id")=="c_fake000000" and e.get("event")=="appeal"]
    fake_ok = fst==404 and not fake_appeals
    summary.append((t,ok,fst,fake_ok))
    lines += [f"## Trial {t}", "", f"- real appeals recorded: **{ok}/10**",
              f"- fake id: status {fst}, appeal entries for it in the log: {len(fake_appeals)} -> {'OK' if fake_ok else 'WRONG'}", "",
              "```json", json.dumps(detail[:2]+[{"...":"8 more like these"}], indent=2), "```", "",
              "Fake id response:", "", "```json", json.dumps(fake, indent=2), "```", ""]
lines.insert(4, "| Trial | Real appeals recorded | Fake id status | Fake id changed nothing |\n|---|---|---|---|\n" +
             "\n".join(f"| {t} | {ok}/10 | {fst} | {'yes' if f else 'NO'} |" for t,ok,fst,f in summary) + "\n")
open(out,"w").write("\n".join(lines))
print("\n".join(f"trial {t}: {ok}/10, fake {fst}, unchanged={f}" for t,ok,fst,f in summary))
