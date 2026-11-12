# Dataset card

| Field | Value |
| --- | --- |
| Title | Team 20 Rada written Kiswahili and Sheng requests |
| Task | Track A single-label intent classification, ten official labels |
| Language | Written Kiswahili/Sheng with natural English code-switching; sw-KE metadata is a locale identifier, not a claim that Sheng and standard Kiswahili are identical |
| Collection | Voluntary scenario-based form; five batches of ten everyday situations; text only |
| Collection versions | Original 44 submissions / 386 answers; latest export 45 / 395; nine later answers outside the reviewed experiment |
| Accepted contributions | 324 human-authored records; 321 original retained workbook acceptances, two follow-up acceptances and one new friend-authored contribution |
| Splits | 213 train / 55 development / 56 final test; per-intent counts in reports/split_counts.csv |
| Review | Kathy workbook decisions; explicit human confirmations of competence/independence; follow-up decisions attributed separately to Hafswa |
| Transformations | Source/review matching, NFC/whitespace normalisation, documented exclusions and punctuation-only duplicate hold; original wording preserved |
| Rights | Private academic assessment sharing confirmed; public release not confirmed; no open-data licence assigned |
| Access | Separate private assessment package, with delivery instructions pending in DATA_ACCESS.md |
| Intended use | Research/teaching prototype recognising written assistant-request categories |
| External training | Selected MASSIVE 1.1 sw-KE training examples, CC BY 4.0; excluded from contribution count |

The ten labels are weather_query, datetime_query, alarm_set, calendar_set, calendar_query, lists_createoradd, lists_query, play_music, news_query and qa_definition.

The data does not represent all Sheng speakers. Convenience recruitment, English prompts, small scenario families, short context-dependent answers, one main reviewer and respondent overlap limit generalisation. No audio, speaker-identification, factual-answer or real-action capability is evaluated. Fifteen original rejection reasons are missing, and the final error analysis identifies debatable labels. The frozen result has not been revised in response to those errors.

Source versions, licences and transformation summaries are in SOURCE_LOG.csv. Detailed source/reviewer mapping stays in the private assessment evidence. Consent-form/version evidence should be retained privately; absence of personal identifiers is not permission for public release.
