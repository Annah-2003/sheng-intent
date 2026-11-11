# MASSIVE preparation for Team 20

This is an optional external-training experiment, not part of the contribution count.
The organiser's baseline remains trained on Team 20 contribution training rows only.

## Preparation completed on 11 November 2026

The complete official archive was recovered after an interrupted download, checked for its expected
40,251,390-byte length, and decompressed successfully with gzip CRC verification.
Its SHA-256 is recorded in MASSIVE_PREPARATION.json. The actual release licence was inspected and retained.

4,162 external training rows remain after excluding 7 exact team-text overlaps, 94 repeated same-label
entries and 2 conflicting-label duplicates. Counts: alarm 173; calendar query 564; calendar set 804;
date/time 311; create/add list 169; read list 197; news 494; music 630; definition 267; weather 553.
Both balanced samples were created: 200 rows (20/intent) and 500 rows (50/intent).

Overlap checking used an overlap-only union of the latest 395 form answers and 386 review-workspace
texts (417 unique normalized texts). This union is not a training dataset and does not approve edited
review responses. Repeat checks against the final adjudicated contribution dataset before fitting.

Spot-checking shows that upstream labels/text are not perfect: some time/date entries are fragments.
Review a small sample across categories before relying on an external-data comparison.
Preparation and comparison software tests passed. Only temporary synthetic software fixtures were
used in the comparison integration test; no real team model was retrained and no final test was scored.

## Source

Publisher: Amazon Science. Release: MASSIVE 1.1. Locale: sw-KE (Kiswahili, not a dedicated Sheng locale).
Official archive: https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.1.tar.gz
Publisher code/source explanation: https://github.com/alexa/massive
Dataset card and citation: https://huggingface.co/datasets/AmazonScience/massive
Data licence: CC BY 4.0; the licence from the actual archive is retained with prepared data.

## Prepare reproducibly

Download the archive from the official URL to private/external/massive/amazon-massive-dataset-1.1.tar.gz.
Then, from the project root:

```
python prepare_massive.py --archive private/external/massive/amazon-massive-dataset-1.1.tar.gz --output private/external/massive/prepared-v1 --team-data private/candidates.csv
```

The script reads only the Kiswahili member and licence from the archive (never extracts arbitrary paths).
It selects upstream training rows for our ten exact labels, retains IDs and partitions, checks blank/contact
text, removes normalized duplicates and excludes conflicting-label duplicate groups.
Exact overlap with the supplied team snapshot is excluded. This must be repeated with FINAL reviewed
team data: candidate overlap checking alone is not final leakage clearance.

Outputs:
- training_pool.csv: the filtered ten-intent external pool.
- train_20_per_intent.csv: 200 balanced external examples, if every class has 20.
- train_50_per_intent.csv: 500 balanced external examples, if every class has 50.
- manifest.json: source hashes, counts, exclusions and sample fingerprints.
- exclusions.csv and LICENSE.txt: audit and licence evidence.

Sampling uses a fixed seed (42); the smaller sample is nested in the larger one.
No external rows are added to contribution.csv, and no model is trained or promoted by preparation.
The generated data/archive remain local and git-ignored under private/.

## Comparison after reviewed data is ready

1. Validate the reviewed Team 20 contribution.csv with the official validator without --practice.
2. Re-check all external candidates against the full final team dataset for exact and close-paraphrase/source overlap.
3. A: train the organiser baseline on Team 20 training rows only.
4. B: use the same model settings with Team 20 training rows plus 20 external examples per intent.
5. C: optionally compare 50 external examples per intent, if time allows.
6. Score all conditions on exactly the same Team 20 development split; save per-label results and genuine errors.
7. Freeze the selected condition and settings before final test evaluation. Keep all upstream and team test
   rows out of training and model selection. No improvement is guaranteed.

The development-only comparison runner is prepared (do not run before reviewed export exists):

```
python compare_massive.py --data private/final-v1/contribution.csv --external private/external/massive/prepared-v1 --output private/experiments/massive-v1
```

It requires the final-data pipeline's matching manifest and the official validator to pass, repeats exact
overlap checks against all final team texts, and saves all three conditions without touching deployment
artifacts. It cannot prove semantic independence; complete the source/near-duplicate checks first.

Use original source IDs to keep localizations of the same MASSIVE source together if another locale is ever added.
Do not call upstream labels Team-20-independent review or call external unchanged rows new contributions.

## What the handbook says

Task and Worked Examples (provided PDF numbered (3)), page 5: external unchanged training material may be
useful, must stay outside the contribution file, does not count toward the target, and must be reported separately.
Choose Your Task (PDF numbered (1)), page 1: MASSIVE can be used for a supported locale; unchanged rows
are reference/training material, not new contributions. Source IDs, permissions and split relationships matter.

## Why the other Sheng resources were not plugged in

The search found translation, synthetic language-model, sentiment and phishing resources, not a verified
ten-intent assistant dataset. Some individual utterances may fit, but would need source/licence checks and
human intent labels. See SHENG_DATASET_SEARCH.md. This is a bounded search finding, not a claim that no
aligned Sheng dataset exists anywhere.
