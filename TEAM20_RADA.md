# Team 20 Sheng Intent

Track A intent classification for the Strathmore NLP Hub Datathon 2026.
Language: Kiswahili/Sheng code-switching, as stated by the team.

## Current result

The first run uses the organiser's character TF-IDF (2–5 grams) and logistic regression baseline.
Development accuracy: 0.7313; macro-F1: 0.6954 (rounded; exact saved metrics are authoritative).
Majority-class development macro-F1: 0.0213. These results use provisional labels and are exploratory.
No final test evaluation has been performed and no human review is asserted.

386 nonblank answers from 44 respondents; 42 respondents supplied answers.
Eight mechanical exclusions leave 378 preliminary candidates: 241 train, 67 development, 70 reserved.
Batches 1+2 train, Batch 3 development, Batches 4+5 reserved. Answers to a scenario remain together.
NFC and whitespace normalization preserve the natural wording; semantic quality remains a human decision.
No spelling standardization, translation, synthetic augmentation or label-driven rewriting is performed.

## Run locally

Use Python 3.10+ (tested here with Python 3.12). In PowerShell from this folder:

```
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe prepare_data.py --source "C:\path\to\Team 20 _ Sheng Form Responses.xlsx"
.\.venv\Scripts\python.exe train_preliminary.py
.\.venv\Scripts\python.exe -m streamlit run team20_app.py
```

Open the printed localhost URL. `Team20_Sheng.ipynb` provides the same steps in notebook form.
For Colab, privately upload the source code, starter-kit folder and workbook and adjust SOURCE.
Do not upload private files to a public notebook or repository.

## Outputs and next checkpoint

- `private/candidates.csv`: original and normalized text, source cells, provisional labels, flags and scenario groups.
- `private/review_decisions.csv`: reviewer handoff; preparation never overwrites an existing decision file.
- `private/mechanical_exclusions.csv` and `private/normalization_log.csv`: mechanical audit trail.
- `private/intake_audit.json`: source fingerprint and counts.
- `artifacts/preliminary/`: actual model, dev metrics, predictions, per-label report and confusion matrix.

Read REVIEW_GUIDE.md before review. Human decisions have not been applied yet. Final contribution export,
official validation, final training/evaluation and submission documentation require that next checkpoint.
The starter validator is intentionally not bypassed by marking candidate rows as reviewed or passing `--practice`.
Preliminary training is a separate clearly labelled experiment using the same baseline implementation.

After recorded review, verify minimums (15 train/5 dev/5 independently reviewed test per label),
resolve semantic groups, permissions and metadata, and export reviewed data to the kit schema.
Then use the organiser's `validate.py`, `train.py`, `evaluate.py` without `--practice`.
Freeze choices before final test evaluation. If reserved data no longer meets class minimums,
collect targeted human examples rather than padding or silently lowering the standard.

## Credit and limitations

Starter Kit v2 is included unchanged under `datathon-starter-kit/`; retain its code licence and attribution.
AI assistance (Codex): repository inspection, mechanical preparation code, preliminary pipeline,
notebook, demo and draft reviewer instructions. No AI-generated utterances were added.
Team members must check this work and document actual review/contributions before submission.
The model always chooses a known class, including for unsupported text; probabilities are uncalibrated.
Development data is small and provisional. Duplicate submissions by the same person cannot be established
from anonymous row codes. Cross-scenario semantic similarity still needs review.
Public-release consent is unresolved; private inputs and artifacts are git-ignored. Nothing has been published.
