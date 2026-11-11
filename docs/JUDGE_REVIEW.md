# Internal assessment against the handbook

11 November 2026. This is a critical internal review, not an organiser score. Basis: supplied handbook, Marking and Final Submission and Build and Demonstrate, current source, review records and saved model outputs.

The project is a credible small prototype. A winning submission is not established. The largest risks are quality of intent labels, narrow language coverage and incomplete hand-in evidence, rather than the choice of classifier.

| Criterion | Weight | Assessment and likely deductions |
| --- | ---: | --- |
| Data quality and annotation | 30 | Human review is traceable and disputed edits are held. However, accepted fragments sometimes depend on the collection prompt. For example, a reminder to fetch items is labelled list addition, a song recommendation is labelled playback, and a request to explain an unspecified thing is labelled definition. Fifteen original rejection reasons are missing. The annotation rule requiring a clear request does not consistently match retained examples. This is the biggest substantive weakness. |
| Provenance, ethics and rights | 20 | Source IDs, hashes, original files, external partitions/licence, photo credit and AI disclosure exist. Independent review and private assessment consent are based partly on the user's confirmations; these are not a substitute for retaining actual consent-form evidence. Public data release is unconfirmed. Keep data restricted and provide judges private access. |
| Contribution coverage and balance | 15 | 324 contributions meet the total and every per-intent 15/5/5 minimum. External rows are counted separately. Five scenario batches produce narrow wording and repeated short expressions; meeting counts does not demonstrate rich Sheng coverage. Code-switching is legitimate, but the claimed variety and inclusion boundaries must be explained consistently. |
| Baseline and evaluation | 15 | Fixed baseline and two external additions were compared on development only; the selected model was frozen and tested once. Test accuracy 43/56 = 76.8%, macro-F1 0.764; majority accuracy 8.9%. Full metrics/confusion are saved. Only 5–7 test examples per intent, respondent overlap and unresolved cross-scenario semantic similarity limit the strength of the result. MASSIVE helped on development; no claim it improved final-test performance is supported by a baseline-only test comparison. |
| Reproducibility and documentation | 10 | Hash checks, dependencies, notebook and seven automated checks exist. Frozen artifacts deliberately refuse retraining. A fresh-run reproduction route must distinguish original experiment reconstruction from viewing the frozen result. Data/models/reports are Git-ignored, so a normal push alone will omit what judges need. Final commit/tag, matching ZIP, permitted artifact access and manifest are still outstanding. Stale draft descriptions must be checked by Irene. |
| Demonstration and teamwork | 10 | The interface calls the actual selected model and shows honest limitations/results. It still needs the required three successes, two failures/unsupported inputs, accessible 2–3 minute recording and actual member-role evidence. A labelled simulated response/action should be made explicit; stating a predicted intent alone may not satisfy that demonstration bullet. Website styling carries little credit on its own. |

## How a strict judge could challenge us

- “Does the text itself express this intent, or did you use the survey question to infer it?” Some examples do not cleanly answer this challenge.
- “Did all close paraphrases stay together?” Scenario IDs and punctuation checks are useful, but are not proof of semantic separation across different scenarios.
- “What exactly did MASSIVE improve?” Development accuracy rose from 42/55 to 44/55; macro-F1 from 0.715 to 0.785. The final selected model scored 43/56. Do not describe these as a measured final-test uplift.
- “Can I run your exact submission?” A public code link without the permitted artifacts, instructions and recorded frozen version is insufficient.
- “Can each member explain their work?” AI assistance is substantial and must be disclosed. Each member should be able to explain the collection, labels, split, baseline and failures in plain language.

## Priorities before hand-in

1. Preserve the frozen data/model/results. Do not change labels, splits or settings to improve this now-observed test score. Document any newly noticed label problem as a limitation; any later revised experiment needs its own declared evaluation plan.
2. End-user check the interface and add a clearly labelled simulated action/response for the demo if absent. No real alarm/calendar integration is required.
3. Irene should reconcile every count and claim with reports/readiness.json, reports/development.json and reports/test.json; complete the source/consent evidence, member contributions and quality report.
4. Provide judges restricted access to required data/artifacts. Check the ignored directories when packaging. Do not publish raw responses/review evidence.
5. Record the required demo; freeze the final code commit/tag and matching ZIP; complete the manifest and use the official submission channel. A GitHub push is not the hand-in.

No numeric total is assigned: the complete final package and demo do not yet exist, and language-quality judgement requires the human reviewers. The rubric's data quality and sourcing criteria together carry 50 marks; they deserve more attention than further cosmetic work.
