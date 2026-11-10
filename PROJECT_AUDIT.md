# Team 20 audit against the datathon handbook

Audit date: 10 November 2026 (EAT).
Team: Kathy Auma, Irene Gitau, Hafswa Sufi.
Track A: ten-intent classification in Kiswahili/Sheng code-switching.

## Current position

We have a working preliminary model and a model-connected demo. We do not yet have a final
accepted dataset or a submission-ready package. No final test evaluation has been performed.
An interface refresh is not evidence of model improvement.

Evidence checked: the supplied handbook PDFs (especially Task/Worked Examples, Choose Your Task,
Build/Demonstrate and Marking/Submission), the starter validator/trainer/evaluator, the workbook-derived
candidate/review files, saved dev metrics, deployed model package, repository files and app source.
Local and packaged model bytes and dev metric bytes matched at audit time.

## What is done correctly

- Original workbook is untouched. Its SHA-256 is recorded in the private intake audit.
- 44 submissions, 42 with answers, yielded 386 nonblank responses.
- Original and normalized text, source cells, respondent row codes and scenario IDs are traceable privately.
- Only NFC and whitespace were normalized. No translation, slang rewriting or synthetic examples were added.
- Four duplicate entries and four explicit non-answers were mechanically excluded; reasons are logged.
- 378 provisional candidates remain: 241 train, 67 development and 70 reserved.
- Whole scenarios remain together: B1+B2 train, B3 development, B4+B5 reserved.
- The TF-IDF vectorizer and logistic regression are fitted on training rows only.
- Exact normalized duplicate checks and a majority-class comparator are included.
- Actual development accuracy is 0.731343; macro-F1 is 0.695444; majority macro-F1 is 0.021333.
- Per-label development F1, confusion matrix and predictions were saved locally.
- The app calls the saved model, displays early-result status and describes simulated actions honestly.
- Raw responses, reviewer files and response-level predictions were not added in our GitHub changes.
- The photo has a source, author, licence and unmodified-use attribution.
- AI assistance is recorded in TEAM20_RADA.md; it need not be part of the team-name line in the UI.

## Gaps and corrections

| Priority | Finding | What must happen |
| --- | --- | --- |
| First | All 386 reviewer decision fields are blank. No accepted dataset count is established. | A competent speaker checks naturalness and labels; record genuine decisions. Every final test row needs a reviewer who did not author it. Training/dev records also need the accepted review status required by the kit; independent review of all training rows is not mandatory. |
| First | Scenario labels are provisional. Some answers are reactions or descriptions, not assistant requests. | Judge the answer itself; exclude/adjudicate unclear or unsupported requests. Do not rewrite fragments into invented requests. |
| First | Each reserved intent has only seven candidates. Development classes have only 6–8 after mechanical exclusions. | After review, verify each label has at least 15 train, 5 dev and 5 test. More than two exclusions in a reserved class causes a shortfall under this split. Collect targeted human examples if necessary. |
| First | Exact duplicates are checked; semantic near-duplicates across scenarios are not yet adjudicated. | Reviewer groups related meanings/close paraphrases before the final split. Freeze group assignments before model choices and test evaluation. |
| First | Participation/18+ consent is recorded, but public-release scope is unresolved. | Record intended assessment/sharing permission and resolve dataset-release terms. Keep uncleared data private and arrange permitted judge access. |
| Required | No final contribution.csv in the kit's 15-field schema is present. Candidate files deliberately use pending statuses and reserved rather than test. | Apply real review decisions, provenance and permission evidence; export accepted rows with the official schema and final train/dev/test split. Never invent reviewer IDs or reviewed statuses to pass validation. |
| Required | Official final validate/train/evaluate workflow has not been completed on reviewed contribution data. | Run validate.py and train.py without --practice after review, choose settings on dev, freeze, then run evaluate.py once on test. The preliminary pack is separate and lacks the exact final kit package contract. |
| Required | Completed data plan, dataset card, source log, quality report, member-role evidence and final contribution/AI-use statement are missing. Blank kit templates are not completed deliverables. | Fill documents with verified facts, dates, actual member roles and record/commit evidence. Use TEAM20_RADA.md and this audit as starting material, not substitute claims. |
| Required | No documented 30-example pilot review was supplied. Collection already happened. | Document a review sample now and report the real sequence. Do not claim a pre-collection pilot occurred if it did not. |
| Required | Final test metrics and up to five actual test errors are not available. | Report accuracy, macro-F1, per-label F1/counts, confusion matrix and majority comparator after frozen evaluation. Development errors can guide work now but cannot be called test errors. |
| Required | Demo success/failure evidence and backup video are not completed. | Show three actual successes and two genuine failures/unsupported requests, with explanations; make the 2–3 minute backup recording accessible to judges. |
| Required | Final submission manifest, tag/full SHA and matching ZIP are not created. | Freeze the reviewed final state, package it, and follow the organiser-announced submission channel. A team repo link alone is not final hand-in. |
| Improve | The existing upstream repository tracks 15,917 virtual-environment files plus bytecode. Our .gitignore does not untrack files already committed. | Coordinate removal of generated environment files from version control in a separate change. The audit did not delete teammates' files or rewrite history. |
| Improve | The deployed model is a packaged snapshot; retraining writes to artifacts/preliminary, not rada/. | Deliberately replace the packaged model and matching metrics together after a verified run; do not assume the website automatically reflects a retrained local model. |

## Provisional class counts after mechanical exclusions

These are not accepted contribution counts.

| Label | Train | Dev | Reserved |
| --- | ---: | ---: | ---: |
| weather_query | 26 | 8 | 7 |
| datetime_query | 24 | 7 | 7 |
| alarm_set | 27 | 8 | 7 |
| calendar_set | 23 | 7 | 7 |
| calendar_query | 25 | 7 | 7 |
| lists_createoradd | 24 | 6 | 7 |
| lists_query | 23 | 6 | 7 |
| play_music | 23 | 6 | 7 |
| news_query | 23 | 6 | 7 |
| qa_definition | 23 | 6 | 7 |

Anonymous row codes cannot prove that each person submitted once. Respondent location and
community membership were not collected; the photo is contextual and does not identify respondents.
The final test has not been scored, although candidate texts were inspected during the data audit.

## External datasets: allowed, but not yet used

The current baseline uses Team 20 form responses only. Constructed starter practice rows and external
dataset rows were not mixed into training. MASSIVE is background for the organiser's intent taxonomy.

MASSIVE includes Kiswahili (sw-KE), not a dedicated Sheng locale. Its official dataset card lists CC BY 4.0.
A useful optional comparison would train on reviewed Team 20 training data plus relevant MASSIVE
Kiswahili training rows, then compare with the Team-20-only baseline on the same reviewed dev split.
An improvement is a hypothesis to test, not a reason to promise a higher score.

If we do that experiment:

1. Pin the exact release/source, locale and licence; filter to the ten supported labels.
2. Keep external rows in a separate file with original IDs and upstream split metadata.
3. Use the upstream training partition for additional training; keep upstream dev/test out of it.
4. Check overlap with our held-out groups. Preserve source-group relationships across localisations.
5. Keep the contribution-only baseline. Report the external-data run separately.
6. Do not count unchanged MASSIVE rows toward the 250 new accepted contributions.
7. Human localisation or new annotation may count only when changes, permissions, source IDs and competent review are documented; automatic translation alone does not count as human work.

AfriSenti is a sentiment dataset, so it is not a drop-in source for this ten-intent task. Common Voice
sentences would need suitable request content and new human labels; downloading more text alone adds no credit.

References:
- MASSIVE official repository: https://github.com/alexa/massive
- Publisher dataset card / locale list / licence: https://huggingface.co/datasets/AmazonScience/massive
- Supplied handbook: Track A task/split rules (Choose Your Task p1; Task and Worked Examples pp4–7),
  external-training rules (Task and Worked Examples p5), demo requirements (Build and Demonstrate p5),
  and documentation/freeze/submission requirements (Marking and Final Submission pp1–4).

## Recommended order from here

1. Reviewer decisions and permission/source evidence.
2. Accepted dataset, group-aware split and class-minimum check.
3. Official baseline; optional small development-only model comparison.
4. Freeze choices; one final test evaluation and real error analysis.
5. Complete documents, video, manifest, final commit/tag and matching ZIP.

The handbook deadline is 11 November 2026 at 11:59 p.m. EAT, unless organisers have issued an update.
Data quality and provenance together carry 50/100 marks; baseline/evaluation carries 15. Review and
evidence are the largest current gaps, rather than a lack of a large model or a more decorated website.
