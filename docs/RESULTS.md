# Results and errors

**Final test: 43 of 56 correct (76.8% accuracy), macro-F1 0.764.** Macro-F1 gives each intent equal importance. The majority comparator scored 8.9% accuracy and 0.0164 macro-F1.

## Choosing the model

All versions used the same 213 team training examples and 55 development examples.

| Added MASSIVE training examples | Correct on development | Macro-F1 |
| ---: | ---: | ---: |
| 0 | 42/55 | 0.715 |
| 200 | 43/55 | 0.763 |
| 500 | 44/55 | 0.785 |

We selected the 500-example version using development macro-F1, then tested it once on the reserved set. The two extra correct development predictions are not proof of a final-test improvement over team-only training.

## Final results by intent

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

Full precision/recall/F1: reports/per_intent_test.csv. Confusion matrix: reports/confusion_matrix.csv (rows are reviewed labels; columns are predictions). Full metrics and majority comparison: reports/test.json.

## Five actual errors

There were 13 disagreements with the reviewed labels. These are possible explanations, not proven causes. Our [test predictions](https://github.com/Annah-2003/sheng-intent/blob/main/assessment/reports/test_predictions.csv) include the original wording.

| Record | Reviewed intent → prediction | What we learned |
| --- | --- | --- |
| T20-R008-B5Q04 | calendar_set → calendar_query | Saving a meeting was confused with checking a calendar. |
| T20-R010-B5Q01 | weather_query → news_query | A question about continuing rain was routed to news. |
| T20-R008-B5Q10 | qa_definition → calendar_set | A vague explanation request lacks the word to define; its reviewed label is debatable. |
| T20-R010-B5Q06 | lists_createoradd → calendar_set | A reminder to fetch items could mean a scheduled reminder, not list addition. |
| T20-R043-B5Q08 | play_music → datetime_query | A song recommendation is not an explicit playback request, so its reviewed label is also debatable. |

## Limits

Each intent has only 5–7 test examples. Some phrases need context, similar wording may cross scenarios, and respondents may occur in different splits. The scores measure agreement with reviewed labels, not general Sheng understanding or interface usability. Unsupported requests still receive a category, and model scores are not guarantees.
The data, labels, splits and model remain unchanged after the final test. Any future corrections need a separate experiment.
