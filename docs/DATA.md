# Data and annotation

324 accepted contributions: 213 training, 55 development, 56 test. All ten intents meet 15/5/5. Final test completed once: 43/56 correct, macro-F1 0.764. Public dataset release is unconfirmed.

## Task and language

Track A: classify a written Kiswahili/Sheng assistant request into one of ten fixed labels.
Natural code-switching and spelling variation are retained; there is no hidden translation step.

| Label | Meaning and boundary |
| --- | --- |
| weather_query | Ask about weather/forecast; news about a storm is not a forecast request |
| datetime_query | Ask the current time/date/day; exclude time-management advice |
| alarm_set | Ask to set an alarm; distinguish calendar event creation |
| calendar_set | Add an event/reminder to a calendar |
| calendar_query | Read an existing calendar/schedule |
| lists_createoradd | Create a list or add an item; distinguish reading a list |
| lists_query | Read an existing list |
| play_music | Start playback; a question about a song's author is not playback |
| news_query | Ask for news/headlines |
| qa_definition | Ask a word/concept's meaning; not unrestricted factual QA |

Require one clear requested action. Read the complete answer instead of labelling from one keyword
or using the survey prompt to supply missing intent. No rule automatically excludes someone for
self-reported low writing comfort. Pure English/variety boundary decisions should be documented
consistently by a competent human; no synthetic language is presented as original respondent text.

## Collection and review

The initial form export contained 44 submissions and 386 nonblank answers (two submissions had no answers).
The latest export contains 45 submissions and 395 nonblank answers. Kathy's reviewed workbook covers
the earlier 386-answer collection. Nine later answers are outside this run.

Source files are preserved as data/raw/responses.xlsx and data/review/workspace.xlsx, with review
decisions mapped by original response row and scenario ID, not the workbook's independent numbering.
The initial import hashes and original comparison remain in the preserved previous work.
Current metadata records the raw-export hash and current candidate snapshot hash.

Kathy's workbook records 350 accepted, 34 rejected and two needs_review entries. This experiment
uses 321 original workbook acceptances, two original answers accepted after Hafswa's independent follow-up review, and one friend-authored addition with permission. Held: 24 edits, two pending entries, two non-answers and one punctuation-only training duplicate. These holds are operator import decisions, not claims that
Kathy herself rejected them. Fifteen rejection reasons were not supplied; record this limitation
instead of inventing linguistic explanations.

Reviewer code T20-KATHY is assigned from the user's identification of Kathy as reviewer. The user
confirmed Kathy did not submit responses herself; this is recorded as the basis for independent review.
Original contributor row codes are pseudonyms, not proof of a unique person or a way to contact them.

Only Unicode NFC and whitespace normalization were applied to this retained subset. Meaning-changing
review edits were set aside. The latest source's profanity removal is retained with the source hash;
the original earlier export is preserved in previous work. data/review/changes.csv retains the audit mapping.

## Splits

Whole scenarios are grouped: Batches 1–2 train, Batch 3 development, Batches 4–5 reserved test.
Related paraphrases across scenarios still need competent review; exact duplicate checks alone cannot
establish semantic independence. The same respondent's different intents may cross splits, so this is
not an unseen-speaker evaluation. Anonymous submissions cannot rule out multiple responses by one person.

See reports/split_counts.csv. All ten intents meet 15 train / 5 dev / 5 test; total counts are 213 / 55 / 56. Total size alone does not satisfy the per-class rule.

The frozen test was scored once. Its text was inspected beforehand for source/review checks and exact
overlap exclusions; we do not claim nobody has ever read it.

## External data

MASSIVE 1.1, sw-KE. Source: https://huggingface.co/datasets/AmazonScience/massive
Official archive: https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.1.tar.gz
Licence: CC BY 4.0; actual archive licence retained under data/external/massive/LICENSE.txt.

The prepared pool contains 4,162 rows from the upstream TRAIN partition for the ten selected intents.
Preparation excluded seven exact team overlaps, 94 same-label duplicates and two conflicting-label
duplicate entries. Source IDs, partitions and source-group identifiers are retained in the pool.
Release/locale/file hashes are in data/external/massive/manifest.json. Selected IDs for the two
experiments are in reports/external_selected_ids.csv. No upstream dev/test rows are fitted.

The external rows have upstream labels, not Team-20 human review. They do not count toward the new
contribution target. The team-only baseline is reported separately, as the handbook requires.
Kiswahili is not equivalent to Sheng; some upstream examples are awkward/fragments. No guarantee of
naturalness or improvement is inferred from dataset size. Other Sheng resources were searched but
not used in these models; no existing reviewed ten-intent Sheng dataset was verified in that search.

## Permission and intended use

Participation was voluntary, text-only and restricted by the form checkbox to consenting adults.
The supplied introduction requested natural assistant expressions, discouraged identifying information,
and described an academic intent-classification dataset. It did not explicitly describe public release.
After an initially tentative answer, the user explicitly confirmed private judge sharing. This confirmation and the friend contributor's permission are recorded in private review metadata and permission.md. Keep actual form consent evidence available privately. Public-release permission remains false; source data and per-example predictions are excluded from the public repository.

Intended use: a small academic prototype. Not a production assistant, general Sheng understanding
benchmark, factual answer system, or authority about people depicted in the photograph.
