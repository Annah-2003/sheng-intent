# Team 20 Sheng Intent Annotation Guide

**Project:** Rada, Team 20, Strathmore NLP Hub Datathon 2026  
**Task:** Single-label intent classification  
**Version:** 1.2, final submission update, 12 November 2026  
**Primary language:** Kiswahili/Sheng code-switching, as written by respondents  
**Unit:** One response to one collection scenario  
**Label set:** The ten intent labels in `taxonomy.csv`

**Submission status:** Our completed review workbook covers 386 original answers: 350 marked accepted, 34 rejected and two pending. After recorded holds, follow-up decisions and one new consented human answer, we used **324 records: 213 training, 55 development and 56 test**. Reviewer codes, review status and splits are present in our exported records. We recorded human confirmations of reviewer competence and independence; all 56 test records have independent-review status. The examples in this guide illustrate the rules and are not additional collected records.

We updated the status and file references after evaluation; we did not change the frozen dataset or test labels. Our [original version 1.1](docs/history/ANNOTATION_GUIDE_v1.1.md) remains available unchanged.

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
6. Record the reviewer code, independence from the author, decision, final label when accepted, and reason when needed in the review workspace and our [exported decisions](https://github.com/Annah-2003/sheng-intent/blob/main/assessment/data/review/decisions.csv).

### Five acceptance tests

Accept a response only when all five checks pass:

1. **Language fit:** it is plausible natural Kiswahili Sheng; formal grammar is not required.
2. **Intent clarity:** it expresses one actionable supported intent without needing the scenario prompt to supply missing meaning.
3. **Label accuracy:** the chosen label matches the text's actual request, even if it differs from the scenario's intended label.
4. **Non-duplication:** it is not an exact duplicate or an overly close variant that should be excluded or grouped to prevent leakage.
5. **Privacy and provenance:** it contains no identifiable private information, and its contributor/source can be traced internally.

## 3. Label inventory and boundaries

The examples below explain the label boundaries. They are illustrations, not claims of additional collected or independently approved gold records.

| Label | Assign when the response asks the assistant to… | Boundary / do not confuse with… | Illustration |
| --- | --- | --- | --- |
| `weather_query` | Give current or future weather information or a forecast. | Asking for a report about a storm that happened is `news_query`; general rain-related advice is not automatically weather. | “Kesho kutanyesha?” |
| `datetime_query` | Tell the current time, date or day. | Setting an alarm is `alarm_set`; asking for time-management advice is outside this label. | “Saa ngapi sasa?” |
| `alarm_set` | Set an alarm to ring at a time or under a clear wake-up condition. | Asking what time it is is `datetime_query`. Judge the requested action, not the presence of a time expression. A countdown-only request needs human review; the supplied taxonomy does not define a separate timer label. | “Niwekee alarm ya saa kumi na mbili.” |
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
- Do not include or repeat personal/sensitive details in notes unless strictly needed for review.

## 6. Review and disagreement resolution

Use pseudonymous reviewer codes, not names, in the decision file. Reviewers should disclose any responses they authored. A reviewer is independent of an author only when they did not write that response. Every final test example must have a competent reviewer who did not author it. Do not infer independence from an anonymous row code.

We do not have a separate documented 30-record pilot or a reviewer-agreement statistic in this submission. We do not claim those checks were completed. The recorded review covers the actual dataset: T20-KATHY reviewed 321 retained records, and T20-HAFSWA reviewed three follow-up records. Our reviewer registry records competence and independence confirmations. The original workbooks do not separately record every review date.

For each disagreement:

1. Preserve both initial decisions and concise rationales in our review log.
2. Discuss the requested action and the written label boundary, not which label seems more convenient for model balance.
3. If the disagreement is resolved, record the adjudicated label, reviewer code and reason; update this guide if the rule is reusable.
4. If it remains unclear, mark discuss or exclude with a reason. Do not force a label.
5. Recheck all earlier affected items after a boundary rule changes.

We retain the guide version, reviewer confirmations, decisions, holds and exclusions in the linked records. We do not report a double-review count or agreement score. Questions found after the final test are discussed in [our error analysis](docs/RESULTS.md), not used to relabel the frozen test.

## 7. Dataset and split safeguards

The response is the annotation unit, but related paraphrases must not leak across data splits. Review `scenario_id` groups and near-duplicate meanings across different scenarios; record a common `related_group_override` where appropriate. Keep each related group entirely in one split. Resolve grouping before final model selection and test evaluation, never in response to test mistakes.

Our original collection contained 386 answers from 44 submissions. The later export contains 395 answers from 45 submissions; nine later answers were not imported as reviewed contributions. The final accepted dataset contains 324 records.

| Split | Records | Scenario batches |
| --- | ---: | --- |
| Training | 213 | 1 and 2 |
| Development | 55 | 3 |
| Test | 56 | 4 and 5 |

Every intent meets the minimum of 15 training, five development and five test examples. We checked scenario-group separation and punctuation-only duplicates. The final CSV records each example's group and split. Respondents can occur in more than one split, and similar meanings across scenarios may still overlap; this is not an unseen-speaker evaluation.

All test records have independently_reviewed status. We selected the model using development results, froze the data/model and evaluated the final test once. We did not move groups or change labels in response to test errors. Per-intent counts are in [split_counts.csv](reports/split_counts.csv).

## 8. Required decision record

Our [decision file](https://github.com/Annah-2003/sheng-intent/blob/main/assessment/data/review/decisions.csv) retains the workbook decision and import action separately. The workbook uses accepted/rejected/needs_review; our code uses accept/exclude/discuss. Some workbook acceptances were held by the import checks rather than automatically retained. Only records with an accept decision enter the final contribution file.

| Field | Required record |
| --- | --- |
| `decision` | Exported status: `accept`, `exclude` or `discuss`; original workbook status stays in `workbook_decision`. |
| `final_label` | One canonical label for accepted rows. Excluded/held records retain their source label for tracing; they are not fitted. |
| `reviewer_code` | Pseudonymous code for the actual reviewer |
| `reviewer_independent_of_author` | `yes`, `no`, or `unknown`, based on actual knowledge |
| `reason` | Label rationale for changes, exclusion/discussion reason, or disagreement resolution as appropriate |
| `related_group_override` | Proposed grouping change for review; blank in this export. The final CSV records the actual `group_id`. |

We link original wording, source row/scenario, human decisions and code holds in [our cleaning report](docs/QUALITY_REPORT.md). We retain actual evidence and do not invent missing review reasons, dates or approvals.

## 9. Change log and review record

| Version | Date | Change |
| --- | --- | --- |
| 1.0 | 12 November 2026 | Initial project-specific guide. |
| 1.1 | 12 November 2026 | Expanded collection context, rules and earlier review snapshot. Preserved in docs/history/. |
| 1.2 | 12 November 2026 | Updated completed review evidence, final counts/splits, actual file paths and export terms. Rules and examples retained; no test labels changed. |

| Review item | Recorded status |
| --- | --- |
| Reviewer competence and independence | Human confirmations recorded in the reviewer registry for T20-KATHY and T20-HAFSWA. |
| Accepted review records | 321 attributed to T20-KATHY; three to T20-HAFSWA; all 56 test records independently reviewed. |
| Exact workbook review dates | Not separately recorded for every decision. |
| Holds and follow-up decisions | Recorded in the exported decisions and change log. |
| Separate 30-record pilot / agreement study | Not documented; no completion or agreement score claimed. |
| Remaining quality limits | Fifteen rejection reasons are missing, and some accepted labels remain debatable. See the quality report and actual errors. |
