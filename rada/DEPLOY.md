# Share Rada with the team

This branch adds Rada without replacing the existing starter demo or training scripts.
The app entry point is `team20_app.py` at the repository root.

In Streamlit Community Cloud, choose this repository and branch `training-data`,
set the main file to `team20_app.py`, and choose Python 3.12 in advanced settings.
Use a private app and explicitly invite team viewers.

Run locally from the repository root:

```
python -m pip install -r requirements.txt
python -m streamlit run team20_app.py
```

The tracked `rada/model.joblib` is the Team 20 preliminary model, trained with scikit-learn 1.7.2.
Only load this trusted model. `rada/dev_metrics.json` contains preliminary development scores.
No raw responses, predictions containing response text, reviewer records, or consent evidence are included.
The final test has not been evaluated. Final model replacement requires recorded human review.

Photo credit and licence: `rada/assets/PHOTO_CREDIT.md`.
Training/review instructions: `TEAM20_RADA.md` and `REVIEW_GUIDE.md`.

The existing repository already tracks a virtual environment and bytecode. This branch leaves those
existing files untouched; they are not dependencies for cloud deployment. The new ignore rules prevent
additional local environments/private files from being added.

