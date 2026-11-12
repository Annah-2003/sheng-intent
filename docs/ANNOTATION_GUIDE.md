# Annotation guide

Updated 12 November 2026 from the guide pushed to the team main branch (4d2e4c0b) and the frozen review evidence. This is a post-evaluation documentation reconciliation, not a claim that the final guide was approved before collection or that test labels were changed.

## Task and decision

Assign one of the ten supported intents to the action expressed by the response. Read the actual request; the survey scenario must not supply a missing action. Preserve natural code-switching, spelling and diacritics. Informality alone is not a reason to reject an answer.

Accept a plausible, single-intent request with traceable source and suitable permission. Exclude confirmed non-answers, identifying content, unsupported requests, duplicates or unclear competing actions; record a reason. Hold unresolved language or label judgements for a competent human. Keep originals and proposed corrections distinguishable; do not rewrite an answer into a different request to reach a class minimum.

The workbook uses accepted/rejected/needs_review; the imported decision file uses accept/exclude/discuss plus import_action to distinguish mechanical holds. Reviewer identity, independence from the author, final label and adjudication reason must be traceable. All test records have independently_reviewed status based on the supplied workbook and subsequent explicit human confirmations.

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


## Ambiguous boundaries

- Adding a calendar event differs from reading one; setting a ringing alarm differs from either.
- Creating or adding to a list differs from reading its contents. A reminder to fetch items may instead be a calendar request and deserves explicit adjudication.
- Music playback differs from asking for a song recommendation or its author.
- A forecast differs from news about rain. A topic word alone does not decide the label.
- Generic “explain this” fragments may not establish a word-definition request without context.

The illustrations above came from a drafted guide; they are not additional collected contributions or independently approved gold records. A documented 30-record pilot is not available, and no reviewer-agreement statistic is claimed. Some accepted frozen records do not cleanly meet these boundaries; see QUALITY_REPORT.md and RESULTS.md. We disclose that inconsistency and keep the observed final test intact rather than retrospectively relabelling it for a better score.
