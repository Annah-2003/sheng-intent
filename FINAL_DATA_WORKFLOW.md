# Turn review decisions into final data

This pipeline is ready before human review is complete. It does not create review decisions,
train a model, evaluate a test set, or publish responses. All outputs default to private/.

## 1. One-time setup

Copy finalize_config.example.json to private/finalize_config.json.
Set candidates_sha256 to the candidate snapshot's SHA-256, obtained with:

```
python -c "from finalize_data import digest; print(digest('private/candidates.csv'))"
```

Language sw-KE is a proposed primary code; confirm Kiswahili/Sheng variety in the dataset card
and set language_confirmed true only after the actual language decision.
Use the real source version (for example, the raw-export hash in intake_audit.json).
Record the actual assessment permission description and an existing private evidence file's path.
Do not mark permission or public release confirmed without checking the evidence.

Register actual reviewer codes under reviewers, for example using this STRUCTURE (not proof):

```json
{
  "YOUR_ACTUAL_CODE": {
    "competence_confirmed": true,
    "independence_checked": true,
    "authored_contributor_codes": []
  }
}
```

The array lists any respondent codes authored by this reviewer; it must reflect actual authorship.
An empty array must not be assumed simply because anonymous authors cannot be identified.
The row independence answer and registry must agree. Self-review requires the reviewer code to
equal the actual author code; test rows require an independent reviewer.

## 2. Check the current review

```
python finalize_data.py
```

Read private/readiness/readiness.json and class_counts.csv. A check may run at any review stage.
Pending/discussed/excluded rows are never counted as accepted. Every accepted row needs a final
label and verified review metadata. Exclusion/discussion decisions need a reviewer and reason.
The current empty review will show zero accepted examples and all class/split shortfalls.

The pipeline verifies reviewer-file source fields against candidates, so spreadsheet edits do not
silently rewrite the original data. Text corrections and mechanical-exclusion overrides need a
separate explicit adjudication before updating the candidate snapshot and review evidence.

related_group_override JOINs whole scenario groups with a common identifier. It never splits
one prompt family. A joined group crossing train/dev/reserved blocks export; resolve the split
before final training, never according to model scores. No automatic resplitting is performed.

## 3. Export after checks pass

```
python finalize_data.py --export private/final-v1
```

This runs the unmodified starter validator without --practice and publishes contribution.csv
plus a hashed manifest only if every gate passes. It requires 15 train/5 dev/5 independently
reviewed test examples per intent. Proposed reserved rows become test only in this validated export.
Existing output directories are refused, so use a new version name after deliberate changes.
Assessment permission clearance does not imply public-release permission.

The validator checks structure, not true fluency, consent or independent judgement.
Keep the reviewed data private until its release terms are resolved.

## 4. What follows later

Pass the validated contribution.csv to the organiser's training scripts. Choose improvements on
development data, then freeze model choices before final test evaluation. This pipeline deliberately
does not run any of those steps. The website is not deployed; no deployment action is performed here.
