# Review Team 20 candidates

Open `private/review_decisions.csv` in Excel or a private sheet. Keep this file private.
These are candidates, not accepted contributions. Review each answer on its own meaning.

Fill these columns:

| Column | What to record |
| --- | --- |
| decision | accept, exclude, or discuss |
| final_label | One of the ten labels below for accepted items |
| reviewer_code | A pseudonymous code for the actual fluent reviewer |
| reviewer_independent_of_author | yes only when reviewer did not author the response; otherwise no or unknown |
| reason | Explain exclusions, disagreements, and label changes |
| related_group_override | Shared group for semantically close paraphrases across scenarios, if found |

Never replace an unclear response with an invented request. If a minor transcription correction is necessary,
record the original, proposed correction and reason separately for adjudication before export.
Do not remove someone solely because they selected “not comfortable”: assess the actual language.
Preserve natural slang, code-switching, diacritics and expressive punctuation.

| Label | Requested action |
| --- | --- |
| weather_query | Ask about weather or a forecast |
| datetime_query | Ask the current time, date or day |
| alarm_set | Set an alarm |
| calendar_set | Add an event or scheduled reminder |
| calendar_query | Read an existing schedule/event |
| lists_createoradd | Create a list or add an item |
| lists_query | Read an existing list |
| play_music | Start music playback |
| news_query | Ask for news/headlines |
| qa_definition | Ask the meaning of a word/concept |

Use `discuss` for statements, fragments, repetitions, unclear requests or questionable language variety.
The prompt helps explain collection history, but cannot supply missing intent to the model.
For example, “Waaah” alone cannot establish a time query. A request for time-management advice is not datetime_query.
An unfamiliar time expression is not automatically wrong. Alarm/timer boundaries should follow the organiser guide.

Mechanical exclusions remain visible for audit. Duplicate entries do not count twice.
All final test items need competent independent review. A respondent row code is a pseudonym,
not proof that a person submitted once. The reviewer must disclose whether they contributed any answers.

The proposed holdout has only seven raw examples per intent. If fewer than five survive in an intent,
collect targeted independently authored examples and group them before modelling; do not move examples
based on model mistakes, pad counts, or pretend a small holdout meets the rules.

Participation consent is recorded. Public-release scope still needs clarification; do not publish raw responses,
review evidence or consent metadata by default.
