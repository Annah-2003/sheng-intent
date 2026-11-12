# Annotation guide

Read what the person wrote and identify the action they requested. The scenario explains the collection context; it must not supply an action missing from the answer. Keep natural code-switching, spelling and diacritics.

| Label | Use it for |
| --- | --- |
| weather_query | Asking about weather or a forecast |
| datetime_query | Asking the time, day or date |
| alarm_set | Setting an alarm |
| calendar_set | Adding a calendar event or scheduled reminder |
| calendar_query | Checking an existing calendar |
| lists_createoradd | Creating a list or adding an item |
| lists_query | Reading an existing list |
| play_music | Starting music playback |
| news_query | Asking for news or headlines |
| qa_definition | Asking what a word or concept means |

Accept a natural response with one clear supported intent, a correct label and a traceable source. Reject confirmed duplicates, identifying details, unsupported requests and non-answers. Hold uncertain cases for human review. Record the decision, reviewer code, label and reason.

Watch these boundaries: adding versus reading a calendar/list; weather forecasts versus news; music playback versus song recommendations; and word definitions versus vague “explain this” requests.

Some accepted labels remain debatable; see RESULTS.md. This guide was updated after evaluation from the earlier team guide and review records. We did not change the frozen test labels. A documented 30-example pilot and reviewer-agreement study are not available.
