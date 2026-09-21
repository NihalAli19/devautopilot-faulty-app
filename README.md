# DevAutoPilot Faulty App

A deliberately constrained FastAPI service used as the safe target for the
[DevAutoPilot AI SRE](https://github.com/NihalAli19/DevAutoPilot_SREAgent) workflow.

The `/work` endpoint has an intentionally undersized concurrency gate. A burst of requests
queues behind one worker, creating the latency anomaly that DevAutoPilot detects, diagnoses,
and fixes through a **draft pull request**. The repository contains no production systems or
credentials and must never be used as a real deployment target.

## Run locally

```bash
python -m venv .venv
python -m pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8001
```

In another terminal, generate the incident:

```bash
python scripts/load_test.py --requests 20
```

The intentionally faulty version should show a p95 latency near the end of the serialized
request queue. The expected AI-generated fix is a small, reviewable change to
`MAX_CONCURRENT_WORKERS` in `app.py`.

## Safety boundary

- DevAutoPilot may create feature branches and draft pull requests.
- A human must review and merge every proposed patch.
- Reliability Guard rollback recommendations also require explicit human approval.
- CI must pass before `main` can accept a change.
