# Rada — Team 20

Kathy Auma · Irene Gitau · Hafswa Sufi

Strathmore NLP Hub Datathon 2026, Track A. Rada recognises ten kinds of written Kiswahili/Sheng assistant requests. It predicts an intent and shows a simulated response; it does not perform real actions.

## Results

324 accepted contributions: **213 training, 55 development, 56 final test**. Every intent meets the required 15/5/5 minimums. Private assessment permission is recorded; public dataset release is unconfirmed.

The selected model uses 213 team examples plus 500 MASSIVE Kiswahili training examples. Selected on development macro-F1, then evaluated once on the frozen test: **43/56 correct (76.8% accuracy), macro-F1 0.764**. Majority comparator accuracy: 8.9%. The measured MASSIVE improvement is on development only, not a baseline-only final-test comparison.

See [results](docs/RESULTS.md), [data and annotation](docs/DATA.md), [team and AI assistance](docs/TEAM.md) and [critical review](docs/JUDGE_REVIEW.md).

## Run the website

Python 3.12 is recommended. From the repository root:

```
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit Community Cloud settings: select the branch containing this version, use **app.py** as the main file, and select Python 3.12 in Advanced settings. requirements.txt is at the repository root. The website needs no API keys, raw dataset or retraining.

The app loads models/selection.json and verifies its model hash against the saved development and final results. It uses the same frozen model as the reported test.

## Project layout

| Folder | Purpose |
| --- | --- |
| src/ | Preparation, fixed training comparisons, guarded final evaluation and report generation; organiser helpers under starter/ |
| notebooks/ | One notebook for inspecting the frozen run or reconstructing a separate experiment |
| data/ | Private assessment data; excluded from public Git |
| models/ | Three fitted classifiers, selected-model metadata and frozen model/data hashes |
| reports/ | Public aggregate metrics, counts, validation and selected external source IDs |
| docs/ | Annotation, sources, results, contribution disclosure and submission checklist |
| assets/ | Licensed photograph and attribution |
| tests/ | Public app/artifact checks and private assessment checks |

Raw responses, reviewer records, external pool and per-example predictions remain local/private. Give judges the required cleared assessment files through the permitted restricted route. The public code repository alone is not the complete assessment package.

## Checks and reproduction

Public deployment checks:

```
python -m unittest discover -s tests -p test_public_app.py
```

The private checks additionally require the assessment data and predictions:

```
python -m unittest discover -s tests -p test_project.py
```

Dependencies are in requirements.txt; requirements-lock.txt records the original environment. Model settings: character TF-IDF 2–5 grams, logistic regression max_iter=1000, seed 42. See reports/development.json for all three conditions.

models/freeze.json prevents preparation, training or evaluation from overwriting the completed experiment. To reproduce training, use a separate copy with the permitted private inputs and no pre-existing model/final-result artifacts; run python -m src.prepare, python -m src.train, then python -m src.evaluate once. Keep the submitted frozen version intact and do not tune using its observed test outcomes. The notebook does not automatically score a test.

## Submission status

The repository is prepared for Streamlit deployment. Deployment, recording, final member sign-off, submission tag/ZIP/manifest and official hand-in confirmation remain separate tasks. See docs/SUBMISSION.md. A GitHub push is not the official submission.

## Credit

Baseline and unchanged helpers: Strathmore NLP Datathon Starter Kit v2, MIT notice in src/starter/LICENSE_CODE.txt. MASSIVE: CC BY 4.0; photograph: CC BY-SA 4.0 with credit in assets/PHOTO_CREDIT.md. AI assistance is disclosed in docs/TEAM.md. No AI-written utterances were counted as human contributions.
