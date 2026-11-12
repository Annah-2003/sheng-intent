# Rada — requests in the words we use

**Team 20 · Track A · Written Kiswahili and Sheng**

Kathy Auma · Irene Gitau · Hafswa Sufi

## Why we built it

People should be able to approach useful digital tools in language they are comfortable using. Requiring a particular English command can turn a simple task into a problem of guessing what the system will accept. Our longer-term motivation is to make the benefits of assistant technology more approachable, so language is less of a barrier to participation and opportunity.

We started with a smaller, testable question: **can a lightweight model identify an everyday request when a person writes it in their own Kiswahili/Sheng wording?** Recognising the request is one step towards an assistant that could act on it. Rada currently classifies ten request types; it does not execute actions.

Our evidence comes from scenario-based text collection, not an access survey or a community-wide usability study. The responses showed the practical challenge: code-switching, spelling variation, and short phrases that sometimes depend on context. We have not measured improved access, saved time or the needs of all Sheng speakers. [Design rationale and evidence limits](docs/HCI_DESIGN.md).

## What we contributed

- Collected and retained **324 human-authored contributions**, with source and review decisions traced privately.
- Compared our-data-only training with two bounded additions of upstream Kiswahili data on the same development set.
- Built a model-connected assessment demo with plain request names, labelled simulated responses and visible uncertainty.
- Preserved real failures and ambiguous labels rather than presenting an always-correct assistant.

The ten labels and baseline approach come from the organiser kit. MASSIVE supplies external training examples. Those reused materials are credited separately; external examples do not count as our contributions.

## Try or watch

- **Website:** https://sheng-intent-3nkn9auhiujhbpwvvwirby.streamlit.app/
- **Presentation/demo video:** VIDEO_LINK_TO_ADD — recorded; viewable link still required before submission.

This is an assessment prototype for judges and the team to inspect the classifier, not a deployed assistant service. Type a request, click **What am I asking?**, and read the predicted request type. The simulated response shows what an assistant might ask or do next. No music, alarm, calendar or external action is executed. The interface is restored to the version used for the team's recorded demonstration.

## Data and review

We elicited responses through five batches of ten everyday scenarios. The original 44 submissions produced 386 nonblank answers. A later export has 45 submissions and 395 answers; nine later answers were not imported as reviewed contributions. After documented exclusions, holds, two follow-up review decisions and one consented human addition, the frozen contribution contains **324 records**.

| Split | Records | Purpose |
| --- | ---: | --- |
| Training | 213 | Fit the model |
| Development | 55 | Compare the three fixed conditions |
| Final test | 56 | Evaluate the selected frozen model once |

Every intent meets 15 training / 5 development / 5 test examples. Scenario families stay together. Different answers by a respondent may cross splits, so this is not unseen-speaker testing. Punctuation-only duplicates are checked; semantic independence across scenarios is not fully established.

Kathy's review was imported using original row/scenario references. Reviewer independence and competence are recorded from human confirmations. Follow-up decisions are attributed to Hafswa, not retroactively to Kathy. Read [annotation guide](docs/ANNOTATION_GUIDE.md), [dataset card](docs/DATASET_CARD.md) and [quality report](docs/QUALITY_REPORT.md).

**Data access:** public redistribution is not confirmed. The public ZIP excludes response data and per-example predictions. The separate **Team20_Assessment_Private.zip** contains the contribution, source/review evidence and reconstruction inputs for the permitted restricted assessment route. Its accessible location and organiser access instructions must be added to [the access note](docs/DATA_ACCESS.md) before hand-in. Do not upload that private ZIP to the public repository.

## Results

The selected model was trained on 213 team examples plus 500 MASSIVE sw-KE training examples. It scored **43/56 correct (76.8% accuracy), macro-F1 0.764** on the final test. A majority-class comparator scored 8.9% accuracy. Each test category contains only 5–7 examples.

| Training condition | Correct on development | Macro-F1 |
| --- | ---: | ---: |
| Team data only | 42/55 | 0.715 |
| Team data + 200 MASSIVE examples | 43/55 | 0.763 |
| Team data + 500 MASSIVE examples | 44/55 | 0.785 |

This supports a development improvement, not a measured final-test gain over the team-only model. Final per-intent results, confusion matrix and majority comparison are in [reports/test.json](reports/test.json). [Results and error analysis](docs/RESULTS.md) explain the limitations, including weather/calendar confusion and debatable reviewed labels. No labels, splits or model settings were changed after viewing final-test outcomes.

## Run the project

Python 3.12 was used. From the project root:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
python -m unittest discover -s tests -p test_public_app.py
python scripts/check_submission.py
```

The saved models and aggregate reports are included. No API key or training is needed to use the demo. The app checks hashes to connect the displayed results to the selected model. The submission checker reports missing links; use --strict when making the final hand-in. See [reproduction instructions](docs/REPRODUCIBILITY.md) for validation, reconstruction, commands and private inputs. The completed experiment intentionally refuses overwriting its freeze. Dependencies: requirements.txt and requirements-lock.txt.

## Team contributions and assistance

Kathy supplied human review and collection/review documentation. Hafswa coordinated data preparation, follow-up decisions, model experiments, interface and repository work with substantial AI assistance. A further annotation guide was pushed through GitHub account Annah-2003 and has been reconciled with the frozen experiment. Irene's final combined-documentation and checking work needs member confirmation. All three participated in the recorded presentation, according to the team's update. [Contribution and AI-use statement](docs/TEAM.md).

## Submission materials

| Required item | File or access route |
| --- | --- |
| Contribution dataset and splits | Private assessment ZIP: data/contribution.csv; hash and access note in docs/DATA_ACCESS.md |
| Annotation guide | docs/ANNOTATION_GUIDE.md |
| Source log and terms | docs/SOURCE_LOG.csv; docs/licenses/; assets/PHOTO_CREDIT.md |
| Dataset card | docs/DATASET_CARD.md |
| Quality and review evidence | docs/QUALITY_REPORT.md; private assessment data/review/ |
| Contribution and AI disclosure | docs/TEAM.md |
| Actual evaluation | docs/RESULTS.md; reports/development.json; reports/test.json |
| Runnable code and environment | app.py; src/; notebooks/; requirements.txt |
| Trained artifacts | models/; frozen hashes in models/freeze.json |
| Video | VIDEO_LINK_TO_ADD |
| Original team repository and version | https://github.com/Annah-2003/sheng-intent — exact package source SHA is in SUBMISSION_MANIFEST.json |

## Final hand-in

Extended deadline: **12 November 2026, 23:59 EAT**. Copy the public project into **teams/team-20/** in a fork of https://github.com/OmondiKevin/sces-nlp-hub-datathon-2026. Change only that folder and open one normal PR titled **Team 20 | Final submission**. The open PR URL is the receipt. A website or original-repository link alone is not submission. See docs/SUBMISSION.md.

## Rights and attribution

Organiser helpers retain MIT notices in src/starter/ and LICENSE_CODE.txt. MASSIVE retains CC BY 4.0. The contextual photograph retains CC BY-SA 4.0; it does not depict our respondents or imply their endorsement. Team response data is restricted to confirmed academic/assessment use, with public release unconfirmed. No blanket open-data or original-code licence is asserted for material the team has not cleared. Full terms are in the source log.
