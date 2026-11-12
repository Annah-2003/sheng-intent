# Model results and error analysis

The frozen **massive_50** model scored **43/56 correct (76.8% accuracy), macro-F1 0.7640** on its single final evaluation.
Majority comparator: 8.9% accuracy, macro-F1 0.0164.
The selected model fitted 213 team training records plus 500 upstream MASSIVE training records. No development or final-test records were fitted.

## Development comparison

| Condition | External training rows | Correct out of 55 | Accuracy | Macro-F1 |
| --- | ---: | ---: | ---: | ---: |
| baseline | 0 | 42 | 0.7636 | 0.7147 |
| massive_20 | 200 | 43 | 0.7818 | 0.7626 |
| massive_50 | 500 | 44 | 0.8000 | 0.7855 |

Three fixed conditions used the same classifier settings and development set. Highest development macro-F1 selected massive_50; exact ties prefer fewer external rows. Samples were nested and fixed with seed 42.
The development improvement is two more correct predictions than team-only training. It does not establish statistical significance, improvement in every category or a final-test improvement over the team-only classifier, which was not scored on final test.

## Final per-intent performance

| Intent | Test count | Precision | Recall | F1 |
| --- | ---: | ---: | ---: | ---: |
| weather_query | 6 | 0.750 | 0.500 | 0.600 |
| datetime_query | 6 | 0.857 | 1.000 | 0.923 |
| alarm_set | 5 | 1.000 | 0.800 | 0.889 |
| calendar_set | 5 | 0.600 | 0.600 | 0.600 |
| calendar_query | 6 | 0.625 | 0.833 | 0.714 |
| lists_createoradd | 5 | 1.000 | 0.600 | 0.750 |
| lists_query | 5 | 0.667 | 0.800 | 0.727 |
| play_music | 6 | 1.000 | 0.833 | 0.909 |
| news_query | 5 | 0.667 | 0.800 | 0.727 |
| qa_definition | 7 | 0.750 | 0.857 | 0.800 |

Each class contains only 5–7 test records. Accuracy is the fraction correct; macro-F1 averages F1 equally across intents. Weather and calendar creation are weakest (F1 0.600).

## Confusion matrix

Rows are reviewed labels; columns are predictions. The numeric order below matches reports/test.json.

| Actual / predicted | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 3 | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 2 | 0 |
| 2 | 0 | 6 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 3 | 0 | 0 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| 4 | 0 | 0 | 0 | 3 | 2 | 0 | 0 | 0 | 0 | 0 |
| 5 | 1 | 0 | 0 | 0 | 5 | 0 | 0 | 0 | 0 | 0 |
| 6 | 0 | 0 | 0 | 1 | 0 | 3 | 1 | 0 | 0 | 0 |
| 7 | 0 | 0 | 0 | 0 | 1 | 0 | 4 | 0 | 0 | 0 |
| 8 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 5 | 0 | 0 |
| 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 | 1 |
| 10 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 6 |

Order: 1 weather_query, 2 datetime_query, 3 alarm_set, 4 calendar_set, 5 calendar_query, 6 lists_createoradd, 7 lists_query, 8 play_music, 9 news_query, 10 qa_definition.

## Five observed disagreements

There were 13 final-test disagreements. Original wording remains in the private prediction file. Explanations below are plausible interpretations, not proven causal diagnoses. No gold label was changed after scoring.

| Record | Reviewed label | Prediction | What to examine |
| --- | --- | --- | --- |
| T20-R008-B5Q04 | calendar_set | calendar_query | A request to save a meeting was confused with reading a calendar. |
| T20-R010-B5Q01 | weather_query | news_query | A question about continuing rain was routed to news. |
| T20-R008-B5Q10 | qa_definition | calendar_set | A generic explanation request lacks a named concept; the reviewed definition label is debatable. |
| T20-R010-B5Q06 | lists_createoradd | calendar_set | A reminder to fetch items could be a scheduled reminder; this exposes a gold-label boundary concern. |
| T20-R043-B5Q08 | play_music | datetime_query | A recommendation request is not an explicit playback instruction, so its reviewed label is also debatable. |

Calendar creation was confused with calendar lookup twice; weather was confused with news twice. These counts come from the saved confusion matrix.

## Limits and next work

Convenience recruitment, English prompts, short context-dependent phrases, limited scenario families, one main reviewer and respondent overlap limit generalisation. Scenario grouping and punctuation checks do not prove semantic independence across scenarios. A passing structural validator does not establish perfect labels, consent evidence or naturalness.
The interface forces a known class for unsupported requests and its model probabilities are uncalibrated. No usability, accessibility, time-saving or community-access improvement has been measured. A future study should separately assess wording coverage, annotation consistency and user comprehension.
Keep the frozen experiment intact. Any annotation revision or new model comparison should be a separately declared experiment with a suitable evaluation plan.

## Reproducibility

Python 3.12.14; scikit-learn 1.7.2. Character TF-IDF 2–5 grams, logistic regression max_iter=1000, random_state=42.
Full metrics: reports/development.json and reports/test.json. Derived tables: per_intent_test.csv and confusion_matrix.csv. Frozen model/data hashes: models/freeze.json. External selection IDs: reports/external_selected_ids.csv. Private predictions and reviewed data are supplied only through the restricted assessment route.
The readiness and selection JSON files are pre-test snapshots; test.json plus freeze.json establish completion. Report generation reads saved outputs and does not predict again.
