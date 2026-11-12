# Assessment files in order

This folder is in the private team repository for authorised academic assessment. Do not copy it into the public organiser repository or change the repository to public with these files present.

| Stage | File | What it shows |
| --- | --- | --- |
| 1. Original collection | [Original responses](history/01_original_responses.xlsx) | Original 44 submissions and 386 nonblank answers. |
| 2. Later export | [Latest responses](data/raw/responses.xlsx) | 45 submissions and 395 answers. Nine later answers were not imported as reviewed contributions. |
| 3. First review version | [Review draft](history/03_review_draft.xlsx) | Earlier human review snapshot. |
| 4. Completed workbook | [Reviewed workbook](data/review/workspace.xlsx) | 350 accepted, 34 rejected and two pending before code holds and follow-up decisions. |
| 5. Import and checks | [Candidates](data/review/candidates.csv), [decisions](data/review/decisions.csv), [change log](data/review/changes.csv) | Original text, record mapping, human decisions and code holds. CSV files open in Excel. |
| 6. Final dataset | [contribution.csv](data/contribution.csv) | 324 accepted records with train/dev/test assignments. |
| 7. Saved predictions | [Development](reports/development_predictions.csv), [final test](reports/test_predictions.csv) | What the fitted models predicted; no final-test rerun. |

AI-assisted code converted/checks the records; humans supplied language and label decisions. Earlier conversion/import scripts are in historical-code/. Current code is ../src/prepare.py. Match records by original source row and scenario, not by the two workbooks' separate numbering.

For local private checks, copy this folder's data/ and reports/ contents alongside the project's app.py, then follow ../docs/REPRODUCIBILITY.md. Keep that combined copy private. The final dataset and selected model have not changed.

The repository owner must grant judges access. The coding assistant has push access but cannot invite collaborators to this repository.
