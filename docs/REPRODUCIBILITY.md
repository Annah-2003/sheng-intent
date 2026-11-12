# Run and reproduce

## Open the saved demo

Use Python 3.12 from the project folder:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
python -m unittest discover -s tests -p test_public_app.py
```

The model is included. No API key, raw data or retraining is needed. requirements-lock.txt records the original environment; scikit-learn was 1.7.2.

## Check the private assessment files

Extract Team20_Complete.zip, then enter teams/team-20/:

```bash
python src/starter/validate.py --track intent --data data/contribution.csv
python -m unittest discover -s tests
```

data/contribution.csv and data/processed/reviewed.csv are identical. Their split column already assigns training, development and test. Do not split them again.

## Rebuild in a separate experiment

Keep the submitted copy unchanged. In a separate folder, copy src/, requirements and the permitted data/raw, data/review and data/external inputs. Create empty models/, reports/ and data/processed/ folders; do not copy the old model/results files. Run:

```bash
python -m src.prepare
python -m src.train
python -m src.evaluate
python -m src.report
```

Settings: character TF-IDF with 2–5 character sequences; logistic regression with max_iter=1000; seed 42. Development macro-F1 selects the model. The evaluation runs once and saves models/freeze.json. This is a reconstruction of a known experiment, not a new untouched test.

Original metrics remain in reports/development.json and reports/test.json. Readiness/selection files describe the earlier pre-test step; test.json and freeze.json record the final evaluation. Package hashes and the full source commit are in SUBMISSION_MANIFEST.json.
