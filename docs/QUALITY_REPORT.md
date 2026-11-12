# Cleaning and review report

## How the original guide maps to this submission

The [original guide](../ANNOTATION_GUIDE.md) is restored unchanged from commit 4d2e4c0b. Its status notes describe an earlier workbook snapshot, not the final export. Reviewer codes, review status and splits are recorded in the exported decisions and final CSV; the completed experiment uses 324 records, not all 350 workbook acceptances. The proposed 30-record pilot is not claimed as completed.

| Earlier guide reference | Current file |
| --- | --- |
| taxonomy.csv | [Original label taxonomy](../taxonomy.csv) |
| private/review_decisions.csv | The exported decisions linked in step 5 below |
| Final accepted records and splits | contribution.csv linked in step 6 below |

## From the form to the final dataset

These links open files in Annah's **private** repository. Judges need GitHub access from the repository owner. Excel files can be downloaded; CSV files also open in Excel.

| Stage | File | What changed |
| --- | --- | --- |
| 1. Original responses | [First form export](https://github.com/Annah-2003/sheng-intent/blob/b1ab031b6357174afce8b8040b9abecc1e51797d/assessment/history/01_original_responses.xlsx) | 44 submissions with 386 answers. |
| 2. Later responses | [Latest form export](https://github.com/Annah-2003/sheng-intent/blob/b1ab031b6357174afce8b8040b9abecc1e51797d/assessment/data/raw/responses.xlsx) | 45 submissions with 395 answers; the nine later answers were not included in this reviewed experiment. |
| 3. Review in progress | [First review sheet](https://github.com/Annah-2003/sheng-intent/blob/b1ab031b6357174afce8b8040b9abecc1e51797d/assessment/history/03_review_draft.xlsx) | Earlier human accept/reject/pending decisions. |
| 4. Completed workbook | [Completed review sheet](https://github.com/Annah-2003/sheng-intent/blob/b1ab031b6357174afce8b8040b9abecc1e51797d/assessment/data/review/workspace.xlsx) | 350 accepted, 34 rejected and two pending before the code holds and follow-up decisions. |
| 5. Code checks and decisions | [Candidates](https://github.com/Annah-2003/sheng-intent/blob/b1ab031b6357174afce8b8040b9abecc1e51797d/assessment/data/review/candidates.csv), [decisions](https://github.com/Annah-2003/sheng-intent/blob/b1ab031b6357174afce8b8040b9abecc1e51797d/assessment/data/review/decisions.csv), [change log](https://github.com/Annah-2003/sheng-intent/blob/b1ab031b6357174afce8b8040b9abecc1e51797d/assessment/data/review/changes.csv) | Record matching, human decisions, edited-answer holds and duplicate checks. |
| 6. Final model data | [contribution.csv](https://github.com/Annah-2003/sheng-intent/blob/b1ab031b6357174afce8b8040b9abecc1e51797d/assessment/data/contribution.csv) | 324 accepted records with training/development/test already assigned. |
| 7. What the model predicted | [Final test predictions](https://github.com/Annah-2003/sheng-intent/blob/b1ab031b6357174afce8b8040b9abecc1e51797d/assessment/reports/test_predictions.csv) | The saved 56-record test, including correct and wrong predictions. |

The [conversion script](https://github.com/Annah-2003/sheng-intent/blob/b1ab031b6357174afce8b8040b9abecc1e51797d/assessment/historical-code/prepare_data.py) made candidate rows and initial scenario labels for human review. The [review-import script](https://github.com/Annah-2003/sheng-intent/blob/b1ab031b6357174afce8b8040b9abecc1e51797d/assessment/historical-code/import_kathy_review.py) matched the workbook to source records. The current [preparation code](../src/prepare.py) applies the recorded decisions and checks the final file. This was **AI-assisted coding, with human language and label decisions**. The earlier scripts are preserved as history, not a replacement for the current run instructions.

Use the original source row and scenario to trace an answer. The form and review workbook have different numbering. The original files and final dataset were not overwritten.

## What was kept

The original workbook covered 386 answers: 350 marked accepted, 34 rejected and two pending. Our final file contains 321 retained workbook acceptances, two originals accepted after follow-up review and one new consented human answer: **324 in total**.

| Left out | Count |
| --- | ---: |
| Workbook rejections | 34 |
| Edited answers still held | 24 |
| Pending decisions | 2 |
| Non-answers | 2 |
| Punctuation-only training duplicate | 1 |

The nine later-export answers were not imported as reviewed contributions. Fifteen original rejection reasons are missing; we did not invent them.

## How we checked it

- Matched each answer by original form row and scenario, rather than assuming the two spreadsheets used the same numbering.
- Preserved original wording and logged edits/holds separately.
- Recorded reviewer codes and human confirmations of competence and independence. All test records have independent-review status.
- Checked repeated text, scenario separation, contact patterns and class counts. All ten intents meet 15/5/5.
- Ran the organiser validator and code checks. Saved file hashes identify the exact data and models.
- Used only MASSIVE's training partition and checked exact overlap with team data.

Some accepted answers have unclear intent boundaries. Similar meanings across scenarios may still overlap, and there was one main reviewer. The validator checks structure, not language quality. The final errors and these limits are reported in RESULTS.md. No model setting, label or split was changed after the final test.
