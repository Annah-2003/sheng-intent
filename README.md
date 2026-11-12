# Rada — Team 20

**Track A · Written Kiswahili and Sheng**

Kathy Auma · Irene Gitau · Hafswa Sufi

## The idea

People should be able to approach useful digital tools in the language they use. We wanted to see whether a small model could recognise everyday requests written in Kiswahili and Sheng, including mixed wording such as “Nichezee doba”.

Rada identifies ten request types, including music, weather, alarms, calendars and lists. This is an assessment prototype. It shows a predicted category and a simulated response; it does not perform real actions.

## Watch or try

- [Presentation and demo video folder](https://drive.google.com/drive/folders/1i1df1u6QQKMaxye50ZqwFpT_Ttq78b8a?usp=drive_link)
- [Live prototype](https://sheng-intent-3nkn9auhiujhbpwvvwirby.streamlit.app/)

## What we did

1. Asked people what they would say to an assistant in everyday situations.
2. Reviewed their wording and labels; kept **324 human-written examples**.
3. Used **213 for training, 55 for development and 56 for the final test**. Related scenario groups stayed together.
4. Compared our data alone with adding 200 or 500 Kiswahili training examples from MASSIVE. We selected the version with 500 additional examples.
5. Selected the best development version, froze it and ran the final test once.

The organiser kit supplied the ten labels and starting model. We contributed the collected data, review work, experiment and demonstration. MASSIVE examples are counted separately.

## Results and limits

**Final test: 43/56 correct — 76.8% accuracy, macro-F1 0.764.** Macro-F1 gives each category equal importance. Always guessing the most common training category gave 8.9% accuracy.

On development data, adding 500 MASSIVE examples increased correct predictions from 42/55 to 44/55. This is not a measured final-test improvement over the team-only model.

The sample is small. Some labels are debatable, some requests need context, and the same respondent can appear in different splits. Rada also forces unsupported requests into a known category. We have not measured real-world usability or improved access. [Results and five errors](docs/RESULTS.md).

## Run it

Use Python 3.12 from the project folder:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The saved model is included; no API key or retraining is needed. [Validation, training, evaluation and test commands](docs/REPRODUCIBILITY.md).

## Follow the project

| Step | Read or open | What it explains |
| --- | --- | --- |
| 1. Collect | [Original and later spreadsheets](docs/QUALITY_REPORT.md#from-the-form-to-the-final-dataset) | The responses we gathered. |
| 2. Review | [Original annotation guide](ANNOTATION_GUIDE.md) and [current status](docs/QUALITY_REPORT.md#how-the-original-guide-maps-to-this-submission) | The labelling rules and how the earlier guide maps to the finished experiment. |
| 3. Prepare | [Cleaning report](docs/QUALITY_REPORT.md), [source log](docs/SOURCE_LOG.csv), src/prepare.py | Human decisions, code checks and changes. |
| 4. Freeze the data | [Dataset card](docs/DATASET_CARD.md) and [assessment files](docs/DATA_ACCESS.md) | The final 324 records and their splits. |
| 5. Train and test | [Results and five errors](docs/RESULTS.md), reports/test.json, reports/confusion_matrix.csv | Model comparison, final scores and failures. |
| 6. Demonstrate | Video link above, app.py and [design explanation](docs/HCI_DESIGN.md) | What the prototype does and how the interaction works. |
| 7. Check contributions | [Team and AI-use statement](docs/TEAM.md) | Responsibilities and reused material. |
| 8. Run it | [Full commands](docs/REPRODUCIBILITY.md), src/, notebooks/, models/ | Installation, saved models and reconstruction. |

The original guide is preserved unchanged. Its dated snapshot is explained separately in the cleaning report; it is not silently rewritten to match later results.

## Team and credits

**Data Lead — Kathy Auma**

Coordinates collection, reviews the wording and intent labels, and maintains the review decisions.

**Model Lead — Hafswa Sufi**

Prepares the data and splits, trains and evaluates the model, and builds the demonstration interface.

**Documentation Lead — Irene Gitau**

Brings the report sections together and checks the sources, results, run instructions and submission checklist.

AI assistance and the team's contribution statement are recorded in [docs/TEAM.md](docs/TEAM.md).

Starter code retains its MIT notice. MASSIVE is CC BY 4.0; the photograph is CC BY-SA 4.0 with [credit](assets/PHOTO_CREDIT.md). The response dataset is shared for assessment through [the private team repository](https://github.com/Annah-2003/sheng-intent/tree/b1ab031b6357174afce8b8040b9abecc1e51797d/assessment); judges need access from its owner.

**Original team repository:** https://github.com/Annah-2003/sheng-intent

**Model and code version:** [529dabf21c605c65a022eb8069be2eee2cd494da](https://github.com/Annah-2003/sheng-intent/commit/529dabf21c605c65a022eb8069be2eee2cd494da)
