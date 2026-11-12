# Running and reconstructing the experiment

## Run the saved app

Use Python 3.12 at the project root:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
python -m unittest discover -s tests -p test_public_app.py
```

No private response data or API key is needed to run the saved app. The actual model files are in models/. selection.json identifies massive_50, and freeze.json records model/data hashes. requirements-lock.txt records the original environment, including scikit-learn 1.7.2; the model must be loaded only from trusted project artifacts.

## Inspect the submitted results

reports/test.json contains final accuracy, macro-F1, per-label precision/recall/F1/support, confusion matrix and majority comparator. reports/development.json contains the fixed three-condition comparison. The notebook inspects saved outputs without retraining. Test predictions and data are restricted assessment materials.

reports/readiness.json and models/selection.json are pre-test snapshots; their test_evaluated=false fields describe that earlier step. The existence and matching hashes of models/freeze.json and reports/test.json establish completed final evaluation. Do not edit original metric snapshots to manufacture a different history.

## Validate private assessment inputs

Overlay the private assessment package at this project root, then run:

```bash
python src/starter/validate.py --track intent --data data/contribution.csv
python -m unittest discover -s tests -p test_project.py
```

data/contribution.csv is a byte-identical export of data/processed/reviewed.csv. Its split column defines all three partitions. Do not randomly split it again. Both filenames are supplied privately because the preparation/reproduction scripts expect the processed path.

## Reconstruct training separately

Keep the submitted frozen directory intact. Create a new experiment directory containing app.py, src/, requirements, and the permitted data/raw, data/review and data/external inputs; do not copy existing models/ or reports/. Create empty models/, reports/ and data/processed/ directories in that new experiment, then run:

```bash
python -m src.prepare
python -m src.train
python -m src.evaluate
python -m src.report
```

prepare verifies the unchanged raw and review snapshots before exporting data. train fits baseline, massive_20 and massive_50 using seed 42, character TF-IDF 2–5 grams and logistic regression max_iter=1000. Only training examples are fitted; development macro-F1 selects the winner. evaluate rechecks evidence and writes a freeze before scoring test. It refuses repeat evaluation or changed evidence. Model serialization hashes may depend on environment; compare provenance/settings and predictions rather than claiming cross-platform byte identity.

This reconstruction reproduces the historical experiment, not a new untouched evaluation. Do not tune using its known test results. Package file hashes and exact source commit are recorded in SUBMISSION_MANIFEST.json.
