# Model results

These are DEVELOPMENT results on the same 55 reviewed examples, not final test scores.
The models were fitted on 213 Team 20 training examples, with fixed model settings.
Outstanding split minimums: 0.

| Condition | External training rows | Correct | Accuracy | Macro-F1 | Majority macro-F1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| baseline | 0 | 42 | 0.7636 | 0.7147 | 0.0226 |
| massive_20 | 200 | 43 | 0.7818 | 0.7626 | 0.0226 |
| massive_50 | 500 | 44 | 0.8000 | 0.7855 | 0.0226 |

Development-selected condition: **massive_50** (highest macro-F1; ties prefer fewer external rows).
This is a small-sample development comparison,
not proof that MASSIVE always helps Sheng or a claim of statistical significance.

## Per-intent development results

| Intent | Examples | Baseline F1 | Selected F1 |
| --- | ---: | ---: | ---: |
| weather_query | 6 | 0.800 | 0.800 |
| datetime_query | 5 | 0.889 | 0.750 |
| alarm_set | 7 | 0.875 | 1.000 |
| calendar_set | 6 | 1.000 | 0.833 |
| calendar_query | 6 | 0.000 | 0.600 |
| lists_createoradd | 5 | 0.667 | 0.571 |
| lists_query | 5 | 0.250 | 0.667 |
| play_music | 5 | 1.000 | 0.833 |
| news_query | 5 | 0.667 | 0.800 |
| qa_definition | 5 | 1.000 | 1.000 |

The selected condition has lower development F1 than the baseline for: datetime_query, calendar_set, lists_createoradd, play_music.
The overall improvement should not be described as an improvement in every intent.

## Observed development mistakes

11 development errors occurred. Up to five are indexed below; original text is in the private prediction CSV.
These are not final test errors. The expected labels are inherited from Kathy’s workbook and still deserve discussion for ambiguous fragments.

| Record | Reviewed label | Model prediction |
| --- | --- | --- |
| T20-R003-B3Q06 | lists_createoradd | lists_query |
| T20-R004-B3Q04 | calendar_set | play_music |
| T20-R004-B3Q05 | calendar_query | lists_query |
| T20-R005-B3Q02 | datetime_query | calendar_query |
| T20-R014-B3Q06 | lists_createoradd | calendar_set |

Possible explanations to discuss with the reviewer (not proven causal diagnoses):
- The list-creation vs list-reading boundary is difficult when a response only describes remembering a list.
- A presentation/reminder phrase was routed to music, showing weak coverage of some calendar wording.
- “Sato”/plans phrasing can be ambiguous without an explicit calendar request.
- The model can interpret a list of foods as another scheduled action instead of an instruction to add items.
- Some short expressions may not state a complete request; revisit the label rather than assume the model alone is wrong.

## Limits and remaining work

- Five-to-seven development examples per class; results are sensitive to individual errors.
- 24 edited, two pending, two non-answer entries and one punctuation-only training duplicate remain held.
- Punctuation-only team duplicates are checked; semantic near-paraphrase review is not automated proof of independence.
- Upstream MASSIVE labels/text can be imperfect and are not Team 20 reviewed contributions.
- Respondent identity/location was not collected; this is scenario-grouped, not unseen-speaker testing.
- Private assessment permission is recorded and split minimums pass. Public release is unconfirmed.
- Final test is complete; final submission evidence remains incomplete.

## Reproducibility

Python 3.12.14; scikit-learn 1.7.2. Random seed 42. Character TF-IDF 2–5 grams; logistic regression max_iter=1000.
Input/model hashes and exact reports: reports/development.json, reports/readiness.json and models/selection.json.
Selected external IDs: reports/external_selected_ids.csv. Dependencies: requirements-lock.txt.

## Final test

Frozen condition: **massive_50**. Evaluated once on 56 independently reviewed test records.
Correct: 43/56; accuracy: 0.7679; macro-F1: 0.7640.
Majority comparator accuracy: 0.0893; macro-F1: 0.0164.
No baseline-only final test comparison was run; the MASSIVE improvement claim is limited to development data.

| Intent | Test examples | F1 |
| --- | ---: | ---: |
| weather_query | 6 | 0.600 |
| datetime_query | 6 | 0.923 |
| alarm_set | 5 | 0.889 |
| calendar_set | 5 | 0.600 |
| calendar_query | 6 | 0.714 |
| lists_createoradd | 5 | 0.750 |
| lists_query | 5 | 0.727 |
| play_music | 6 | 0.909 |
| news_query | 5 | 0.727 |
| qa_definition | 7 | 0.800 |

13 actual final-test errors. Five examples below; all predictions remain private in reports/test_predictions.csv.

| Record | Reviewed label | Prediction |
| --- | --- | --- |
| T20-R008-B5Q04 | calendar_set | calendar_query |
| T20-R008-B5Q09 | news_query | qa_definition |
| T20-R008-B5Q10 | qa_definition | calendar_set |
| T20-R010-B5Q01 | weather_query | news_query |
| T20-R010-B5Q04 | calendar_set | calendar_query |

Calendar creation was confused with reading a calendar twice. Weather questions were confused with news twice. These are observed confusions, not proven causes.
Some gold labels remain debatable: a reminder to fetch items is labelled list addition, and a song recommendation is labelled playback. Keep the frozen results intact; disclose these concerns instead of relabelling after scoring.
Confusion matrix and full per-label precision/recall/support: reports/test.json. Frozen data/model hashes: models/freeze.json.
Test examples were inspected for provenance and overlap before scoring. This is not unseen-speaker testing or proof of broad Sheng comprehension.
