# Team 20 Sheng Intent Annotation Guide

**Project:** Rada, Team 20, Strathmore NLP Hub Datathon 2026  
**Task:** Single-label intent classification  
**Version:** 1.1, updated from Team 20's *Sheng in Context* collection and review snapshot  
**Primary language:** Kiswahili/Sheng code-switching, as written by respondents  
**Unit:** One response to one collection scenario  
**Label set:** The ten intent labels in `taxonomy.csv`

> **Evidence status (11 November 2026 snapshot):** Team documentation reports that the reviewer did not submit form responses, and that the review workspace contains 350 accepted, 34 rejected and 2 needs_review decisions. However, reviewer codes, review_status and splits were not populated in the workspace, and the report says competence in the specific Sheng variety still needs confirmation. Treat these as reported workflow facts, not verified completed independent review. The local Kiswahili/Sheng examples in this guide are proposed illustrations; they are not claimed as reviewer-approved examples.

## 1. Purpose and scope

Assign the label that best describes the action the respondent asks an assistant to perform. Rada predicts one of ten request types; it does not carry out the request. Annotate the response itself, not the scenario prompt, respondent identity, or what you think the person probably meant.

Use this guide for Team 20's Track A intent task only. Sentiment and semantic-slot annotation are out of scope. The project elicited written requests through a Google Form with five batches of ten everyday scenarios, one scenario per intent in each batch. Contributors could leave answers blank and were invited to use their usual Kiswahili/Sheng, including natural Kiswahili-English code-switching. The prompts were written in English, so prompt-induced translation phrasing is a known limitation: assess whether each response sounds plausible in natural Kiswahili Sheng, not whether it resembles a translation or formal grammar. This is scenario elicitation, not a sample of spontaneous speech or actual assistant use. Preserve the respondent's wording, spelling, diacritics, slang, punctuation and word order. Do not translate or silently correct it.

## 2. Annotation decision

For every non-empty candidate, make one decision using the review workspace's decision terms:

- **accepted** — the response passes the five acceptance tests below and expresses one sufficiently clear supported request; record exactly one label.
- **rejected** — it fails for a documented reason, such as duplicate, ambiguous, incomplete, identifying, or unsupported content. State the specific reason. Do not reject merely for informal spelling or unfamiliar Sheng.
- **needs_review** — a linguistic or label judgement cannot yet be supported; leave the final label empty pending adjudication and record the question to resolve.

Do not force an in-scope label onto an unsupported request, a statement, a reaction, a fragment with no recoverable action, or a response with competing actions. Do not invent or repair an utterance. Record the original text and a concise reason for every rejected or needs_review decision. If a minimal transcription correction is genuinely necessary, preserve the original, propose the correction and reason, and obtain a separate adjudication before changing the candidate snapshot.

### Decision sequence

1. Read the response as written. Read its scenario only to understand collection context; the scenario cannot supply an action absent from the response.
2. Ask: **What does the speaker want the assistant to do now?** Look at the requested action, not a shared topic word.
3. Check the ten definitions and the boundary examples below.
4. If exactly one supported action is clear, accept it with that label.
5. If no supported action is clear, or multiple actions compete, mark needs_review (or rejected when the reason is clear, such as a confirmed duplicate) and explain why.
6. Record the reviewer code, independence from the author, decision, final label when accepted, and reason when needed in the review workspace and final `private/review_decisions.csv` export.

### Five acceptance tests

Accept a response only when all five checks pass:

1. **Language fit:** it is plausible natural Kiswahili Sheng; formal grammar is not required.
2. **Intent clarity:** it expresses one actionable supported intent without needing the scenario prompt to supply missing meaning.
3. **Label accuracy:** the chosen label matches the text's actual request, even if it differs from the scenario's intended label.
4. **Non-duplication:** it is not an exact duplicate or an overly close variant that should be excluded or grouped to prevent leakage.
5. **Privacy and provenance:** it contains no identifiable private information, and its contributor/source can be traced internally.

## 3. Label inventory and boundaries

The Kiswahili illustrations below are working illustrations. They must be checked by a competent speaker for naturalness and intended meaning before being used as gold examples.

| Label | Assign when the response asks the assistant to… | Boundary / do not confuse with… | Working illustration (needs fluent review) |
| --- | --- | --- | --- |
| `weather_query` | Give current or future weather information or a forecast. | Asking for a report about a storm that happened is `news_query`; general rain-related advice is not automatically weather. | “Kesho kutanyesha?” |
| `datetime_query` | Tell the current time, date or day. | Setting an alarm is `alarm_set`; asking for time-management advice is outside this label. | “Saa ngapi sasa?” |
| `alarm_set` | Set an alarm to ring at a time or under a clear wake-up condition. | Asking what time it is is `datetime_query`. A timer or countdown is not covered by this label unless the taxonomy owner confirms it belongs here. | “Niwekee alarm ya saa kumi na mbili.” |
| `calendar_set` | Add an event or scheduled reminder to a calendar. | Asking what is already scheduled is `calendar_query`; setting a ringing alarm is `alarm_set`. | “Weka meeting yangu ya Ijumaa kwa calendar.” |
| `calendar_query` | Read or check existing calendar events or schedule. | Adding a new event is `calendar_set`. | “Leo niko na meeting gani?” |
| `lists_createoradd` | Create a list or add an item to an existing list. | Reading/listing items is `lists_query`. If create-versus-add is not clear but list modification is, this shared label still applies. | “Ongeza maziwa kwa shopping list.” |
| `lists_query` | Read the contents of an existing list. | Adding an item or creating a list is `lists_createoradd`. | “Niko na nini kwa shopping list?” |
| `play_music` | Start or play music. | Asking who sang, wrote or produced a song is not a playback request. | “Nichezee ngoma.” |
| `news_query` | Provide news, headlines or a report about events. | Asking what the weather will be is `weather_query`. | “Nipe habari za leo.” |
| `qa_definition` | Explain the meaning of a word or concept. | A general factual question is outside this label unless it asks what something means. | “Neno ‘democracy’ inamaanisha nini?” |

Only the ten canonical strings above are valid final labels. Use the friendly wording in the app for people-facing display, not as replacement labels in the data.

## 4. Important boundary cases

| Response | Decision | Why |
| --- | --- | --- |
| “Mvua?” | discuss | A topic word alone does not show whether the speaker wants a forecast, news, or something else. |
| “Nipe habari kuhusu mvua iliyonyesha jana.” | accept: `news_query` | The requested action is to give news/report information; a weather word does not decide the label. |
| “Je, kutakuwa na mvua kesho?” | accept: `weather_query` | The speaker asks for a forecast. |
| “Waaah” | discuss | A reaction does not state a supported request. |
| “Nataka kupanga time yangu vizuri.” | discuss | This is a statement about time management, not a request for the current date/time. |
| “Niambie saa, halafu weka alarm.” | discuss | Two supported actions compete in one response; do not pick one arbitrarily. |
| “Cheza wimbo wa Sauti Sol.” | accept: `play_music` | The requested action is playback. |
| “Nani aliimba huu wimbo?” | discuss | It asks a factual question not represented by the ten labels. |
| “Calendar yangu iko aje?” | accept: `calendar_query` only if a fluent reviewer confirms it naturally asks to read existing events; otherwise discuss. | Do not assume an ambiguous local phrase has one meaning. |

These are guide examples, not claims that the same phrases occur in the collected dataset. The project report gives two prompt-boundary illustrations: “Next week napresent” may be understandable but does not explicitly ask to create a calendar event; “Ati?” alone does not clearly ask for a definition. Treat both as needs_review/rejected unless a reviewer can establish a clear supported request from the response itself. Add examples from actual reviewed responses only when release/assessment permissions allow, and keep private evidence out of public files where required.

## 5. Language and text handling

- Preserve code-switching and natural local wording. English words in a Sheng/Kiswahili response do not make it invalid.
- Do not treat unfamiliar spelling, slang, dialect, diacritics, expressive punctuation or a language choice as an error by itself.
- Do not translate, normalize vocabulary, replace slang, or rewrite a fragment into a complete request.
- Existing preparation applies NFC Unicode normalization and whitespace normalization for processing. Those mechanical changes do not certify fluency or meaning; consult the original response when judging it.
- If a reviewer cannot confidently understand the response or its language variety, choose discuss and seek a competent speaker. Record disagreement rather than silently standardizing the text.
- Do not include or repeat personal/sensitive details in notes unless strictly needed for private adjudication.

## 6. Review and disagreement resolution

Use pseudonymous reviewer codes, not names, in the decision file. Reviewers should disclose any responses they authored. A reviewer is independent of an author only when they did not write that response. Every final test example must have a competent reviewer who did not author it. Do not infer independence from an anonymous row code.

The project completion plan calls for an auditable **30-record review pilot (three records from each intent)**. Select varied items within each label, including code-switching and uncertain cases. Record which records were selected and the selection method. Have a second competent speaker independently annotate the pilot where feasible, then compare decisions. Log initial decisions, disagreement, resolution and any guide change. Because collection has already happened, describe this as a post-collection review pilot, not a pre-collection pilot. The supplied project report says this auditable pilot table still needs to be documented; do not claim it is complete unless the review table exists.

For each disagreement:

1. Preserve both initial decisions and concise rationales in the private review log.
2. Discuss the requested action and the written label boundary, not which label seems more convenient for model balance.
3. If the disagreement is resolved, record the adjudicated label, reviewer code and reason; update this guide if the rule is reusable.
4. If it remains unclear, mark discuss or exclude with a reason. Do not force a label.
5. Recheck all earlier affected items after a boundary rule changes.

Record the guide version/date, reviewer competence confirmation, independence checks, number of items double-reviewed, disagreements, resolutions and exclusions. Do not claim a review, fluent check or agreement statistic unless it actually happened and is documented.

## 7. Dataset and split safeguards

The response is the annotation unit, but related paraphrases must not leak across data splits. Review `scenario_id` groups and near-duplicate meanings across different scenarios; record a common `related_group_override` where appropriate. Keep each related group entirely in one split. Resolve grouping before final model selection and test evaluation, never in response to test mistakes.

The supplied collection snapshot reports 386 non-empty candidate messages from 44 form submissions (54 of 440 possible responses were blank). It reports 350 marked accepted, 34 rejected and 2 needs_review, but explicitly says reviewer codes and split assignments are missing and that the required review_status field must be restored. These are current spreadsheet statuses, not validated accepted-data counts. An earlier project workflow had provisional scenario-batch splits; the newer collection report says no train/dev/test values are populated in the connected review workspace. Therefore do not describe any split as final until it is actually assigned and checked. The minimum is 250 accepted records and at least 25 per intent (15 train, 5 dev, 5 test); the team's optional target is 300 (18/6/6 per intent). Use stratified, group-aware splits so close variants stay together. Every test item needs documented independent review. A contributor-held-out subset can be reported as an additional robustness check only if the required class counts remain feasible.

## 8. Required decision record

Use `private/review_decisions.csv`; do not commit or publish it by default. For each candidate, complete the applicable fields:

| Field | Required record |
| --- | --- |
| `decision` | `accepted`, `rejected`, or `needs_review` (match the live review workspace; map carefully to any export schema) |
| `final_label` | Exactly one canonical label for accepted rows; blank otherwise |
| `reviewer_code` | Pseudonymous code for the actual reviewer |
| `reviewer_independent_of_author` | `yes`, `no`, or `unknown`, based on actual knowledge |
| `reason` | Label rationale for changes, exclusion/discussion reason, or disagreement resolution as appropriate |
| `related_group_override` | Shared identifier for semantically related paraphrases requiring the same split group; blank if none identified |

Keep the source text, collection provenance, permission evidence and reviewer log linked through the private workflow. Do not invent source rights, reviewer claims, language validation, counts, results, consent scope, or contribution statements.

## 9. Change log and sign-off

| Version | Date | Change | Status |
| --- | --- | --- | --- |
| 1.0 | 12 November 2026 | Drafted from the Team 20 intent taxonomy, app, collection workflow and review requirements. | Project-specific draft. |
| 1.1 | 12 November 2026 | Added the reported five-batch scenario collection design, English-prompt limitation, five acceptance tests, live decision terms, 30-record post-collection pilot requirement, and 11 November review/split status. | Updated from the *Sheng in Context* evidence snapshot; reviewer identifiers, competence confirmation, decisions and split validation remain to be evidenced. |

| Reviewer check | Record actual value |
| --- | --- |
| Reviewer independence | Project report says reviewer did not submit responses; verify and record in review registry |
| Reviewer code and language variety/competence | Not populated/confirmed in the evidence snapshot |
| Date checked | Review workspace evidence still required |
| Wording/examples changed and reason | Record from the auditable 30-record pilot |
| Final approval for annotation use | Pending documented pilot, reviewer metadata and adjudication |

