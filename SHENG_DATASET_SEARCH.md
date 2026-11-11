# Sheng dataset search for Team 20

Searched 10 November 2026. This is a research shortlist, not an import manifest.
No external training data was added, no social posts were scraped in bulk, and no model was retrained.
Sizes and licences below are publisher claims unless explicitly described as checked.
Searches covered Hugging Face, GitHub, ACL Anthology, Zenodo and Lanfrica, following secondary leads to primary sources where possible.

## Main conclusion

Sheng resources exist, but none inspected supplies our ten assistant-intent labels ready for training.
Translation, sentiment, phishing and language-model data cannot simply be concatenated with our labelled requests.
Our character-TF-IDF/logistic-regression pipeline needs a suitable request plus an intent label for each training row.

## Sources inspected

| Source | What was found | Terms/access checked | Fit for Rada |
| --- | --- | --- | --- |
| [EgesaWO/Eng2sheng](https://huggingface.co/datasets/EgesaWO/Eng2sheng) | Viewer shows about 4,050 English–Sheng pairs. Visible samples are Bible narratives, not assistant requests. | Apache-2.0 metadata; underlying source provenance still merits review. | Vocabulary/background; low priority for direct intent training. |
| [EgesaWO/Sheng_sml](https://huggingface.co/datasets/EgesaWO/Sheng_sml) | About 1,040 translation pairs, visibly overlapping Eng2sheng samples. | Apache-2.0 metadata. | Do not assume these two datasets are independent; check duplicates before combining. |
| [LughaGen Multilingual African Corpus](https://huggingface.co/datasets/LughaGen-Organization/LughaGen-Multilingual-African-Corpus) | Publisher reports 189,834 synthetic Sheng rows within the Swahili totals. Sheng is created by rule-based vocabulary insertion into parallel text, with reported manual quality control. | CC BY-SA 4.0 metadata. Files are gated; conditions require user review. Underlying sources have separate terms. | Possible exploratory candidate pool, not verified human contribution data and not already intent-labelled. |
| [BlakHasan/sheng-augmented-collection](https://huggingface.co/datasets/BlakHasan/sheng-augmented-collection/blob/main/README.md) | Publisher reports 7,926 translation and 209,930 monolingual rows, mixing existing seeds, synthetic material and Shengilia scraping. Includes origin fields. | No single clear blanket licence established from the card; source-specific terms must be checked. | Larger does not mean independent or higher-quality. Do not bulk import; inspect individual sources first. |
| [Maxyelow/kenyan-code-switch-instruct-50k](https://huggingface.co/datasets/Maxyelow/kenyan-code-switch-instruct-50k) | Claimed 50,000 instruction/response pairs; grammar correction, translation, technical explanation and cultural dialogue. Visible previews repeat content. | Apache-2.0 metadata. Naturalness/human authorship and claimed linguistic guarantees were not independently verified. | Some request-like text is visible, but not our label scheme. Count unique useful utterances, not nominal rows. Low priority until audited. |
| [Sheng-Sentiment-Base](https://github.com/okech-christopher/sheng-sentiment-base) | README advertises a dictionary with 75+ slang mappings, preprocessing and sentiment rules. | Repository states MIT. The specific dictionary file was not retrieved during this search. | A promising vocabulary-reference lead for the reviewer. Not a ready-made assistant-intent dataset; claims need file-level verification. |
| [Sheng Dictionary](https://github.com/Abdullahi254/sheng-dictionary) | README describes a seed script with 100+ words, definitions and examples, plus a submission website. | README states MIT for the repository; live community-submitted content rights were not independently checked. | Another reviewer vocabulary resource. A word definition alone is not a labelled user request. |
| [RideKE paper](https://aclanthology.org/2024.wassa-1.19.pdf) | Peer-reviewed work on Kenyan code-switched ride-hailing sentiment/emotion. | The paper-linked [repository](https://github.com/NEtori21/Ride_hailing_project) currently shows only a README. Downloadable data and its licence were not verified. | Relevant research context, unsuitable for immediate ingestion. |
| [Sheng Mental Health Dataset](https://zenodo.org/records/14637639) | Zenodo description says conversations were generated with GPT-4 and translated into Sheng. It lists Strathmore University as a related person, not proof of authorship or endorsement. | No usable licence text established from the rendered record. | Synthetic, off-task and unclear terms: exclude from the current plan. |
| [Sheng-English Phishing Corpus listing](https://lanfrica.com/en/record/a-sheng-phishing-corpus-for-low-resource-cybersecurity-nlp) | Secondary listing reports 9,970 ham/phishing texts, assembled from transcriptions/social/web sources. | Listing says CC BY-NC 4.0. Linked Zenodo record 17431164 could not be retrieved; primary verification incomplete. | Park this lead; no download/reuse recommendation without primary provenance review. Wrong task labels regardless. |

## Practical next experiment

1. Keep the Team-20-only baseline as the reference.
2. First compare a small, controlled addition of [MASSIVE Kiswahili](https://huggingface.co/datasets/AmazonScience/massive) training rows for the same ten intents. It has the correct task labels; Sheng collections generally do not.
3. Use dictionaries to identify vocabulary gaps with the fluent reviewer, not to replace whole utterances with hidden English translations or to assign labels from isolated keywords.
4. If external Sheng sentences are selected, accept only genuinely suitable requests after provenance/licence checks and human intent/naturalness review. Preserve source IDs and flag synthetic origin honestly.
5. Keep external rows and experiments separate from new human contributions. Do not turn synthetic text into claimed human contribution data.
6. Compare on the same development split, inspect per-intent changes, and keep the reserved final test out of tuning.

More general Sheng text does not automatically teach our supervised model which words mean which actions.
Reviewing diverse natural requests may be more useful than adding thousands of unrelated narratives.
We can test the hypothesis; no accuracy improvement is promised.
