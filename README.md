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

## Required files

| Material | Where to find it |
| --- | --- |
| Contribution data, splits and review evidence | [Restricted access instructions](docs/DATA_ACCESS.md) |
| Annotation rules | [Annotation guide](docs/ANNOTATION_GUIDE.md) |
| Sources and permissions | [Source log](docs/SOURCE_LOG.csv) and docs/licenses/ |
| Dataset summary | [Dataset card](docs/DATASET_CARD.md) |
| Cleaning and review checks | [Quality report](docs/QUALITY_REPORT.md) |
| Team contributions and AI use | [Team statement](docs/TEAM.md) |
| Results and confusion matrix | [Results](docs/RESULTS.md), reports/test.json and reports/confusion_matrix.csv |
| Model and code | models/, src/, notebooks/ and app.py |
| Design explanation | [Human-centred approach](docs/HCI_DESIGN.md) |

## Team and credits

**Data Lead — Kathy Auma**

Coordinates collection, reviews the wording and intent labels, and maintains the review decisions.

**Model Lead — Hafswa Sufi**

Prepares the data and splits, trains and evaluates the model, and builds the demonstration interface.

**Documentation Lead — Irene Gitau**

Brings the report sections together and checks the sources, results, run instructions and submission checklist.

AI assistance and the team's contribution statement are recorded in [docs/TEAM.md](docs/TEAM.md).

Starter code retains its MIT notice. MASSIVE is CC BY 4.0; the photograph is CC BY-SA 4.0 with [credit](assets/PHOTO_CREDIT.md). The response dataset is shared privately for assessment.

**Original team repository:** https://github.com/Annah-2003/sheng-intent

**Model and code version:** [529dabf21c605c65a022eb8069be2eee2cd494da](https://github.com/Annah-2003/sheng-intent/commit/529dabf21c605c65a022eb8069be2eee2cd494da)
