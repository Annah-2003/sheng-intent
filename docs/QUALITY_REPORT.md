# Cleaning and review report

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
