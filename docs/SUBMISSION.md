# Submission checklist

Handbook deadline: 11 November 2026, 23:59 EAT, unless organisers announce a change.

| Criterion | Marks | Current evidence |
| --- | ---: | --- |
| Data quality/review | 30 | 324 accepted contributions; human decisions traced to source; held records preserved privately; ambiguous labels disclosed |
| Provenance/ethics | 20 | Source hashes, external licence and private-assessment permission recorded; public release unconfirmed; AI disclosure drafted |
| Coverage/balance | 15 | 213 train / 55 development / 56 test; every intent meets 15/5/5 |
| Baseline/evaluation | 15 | Three development comparisons; selected model frozen; one final test: 43/56, accuracy 76.8%, macro-F1 0.764 |
| Reproducibility/docs | 10 | Source, dependencies, notebook, hashes and aggregate outputs available; final sign-off/package still pending |
| Demo/teamwork | 10 | Actual model-connected interface, labelled simulated responses; end-user check, recording and member evidence still pending |

## Remaining team actions

- End-user check the website. Choose three actual successes and two real failures/unsupported requests and explain them.
- Record a 2–3 minute backup demo and verify access from another account/device.
- Irene: reconcile documents with the saved reports; complete the quality report, source/consent evidence and actual member contributions/AI-use sign-off. See JUDGE_REVIEW.md for substantive limitations.
- Deploy the prepared app on Streamlit Community Cloud using app.py and Python 3.12, then verify the shared link. Local operation plus the recording remains a backup.
- Provide judges restricted access to the cleared contribution dataset, source/review evidence and required artifacts. Public Git deliberately excludes private data and per-example predictions.
- Freeze the final code commit/tag, record the full SHA, create a matching ZIP and manifest (team/language, URLs, counts, licences, metric locations, run instructions, recording and known limitations).
- Submit via the organiser-announced official channel and retain confirmation. A push to a personal or team repository is not the hand-in.

Do not change the frozen model, labels or splits to improve the observed final-test score. models/freeze.json records its hashes. Later revised experiments must be separate and explicit.
