"""Write the actual development results into one stable report document."""
import json
import pandas as pd
from src.common import ROOT

def report():
    result=json.loads((ROOT/'reports/development.json').read_text())
    state=json.loads((ROOT/'reports/readiness.json').read_text())
    lines=['# Model results','',
        f"These are DEVELOPMENT results on the same {state['split_totals']['dev']} reviewed examples, not final test scores.",
        f"The models were fitted on {state['split_totals']['train']} Team 20 training examples, with fixed model settings.",
        f"Outstanding split minimums: {len(state['shortfalls'])}.",
        'No real final test predictions were made.','',
        '| Condition | External training rows | Correct | Accuracy | Macro-F1 | Majority macro-F1 |',
        '| --- | ---: | ---: | ---: | ---: | ---: |']
    for name,r in result['runs'].items():
        s=r['model'];b=r['majority_baseline']
        lines.append(f"| {name} | {r['external_train_rows']} | {round(s['accuracy']*r['dev_rows'])} | {s['accuracy']:.4f} | {s['macro_f1']:.4f} | {b['macro_f1']:.4f} |")
    winner=result['selected_condition']
    chosen=result['runs'][winner]['model']
    lines+=['',f'Development-selected condition: **{winner}** (highest macro-F1; ties prefer fewer external rows).',
        'This is a small-sample development comparison,',
        'not proof that MASSIVE always helps Sheng or a claim of statistical significance.','',
        '## Per-intent development results','',
        '| Intent | Examples | Baseline F1 | Selected F1 |','| --- | ---: | ---: | ---: |']
    for label in chosen['label_order']:
        lines.append(f"| {label} | {int(chosen['report'][label]['support'])} | {result['runs']['baseline']['model']['report'][label]['f1-score']:.3f} | {chosen['report'][label]['f1-score']:.3f} |")
    worse=[label for label in chosen['label_order'] if chosen['report'][label]['f1-score']<result['runs']['baseline']['model']['report'][label]['f1-score']]
    lines+=['','The selected condition has lower development F1 than the baseline for: '+', '.join(worse)+'.',
            'The overall improvement should not be described as an improvement in every intent.']
    predictions=pd.read_csv(ROOT/'reports/development_predictions.csv')
    errors=predictions[(predictions.condition==winner)&predictions.label.ne(predictions.prediction)]
    lines+=['','## Observed development mistakes','',
        f'{len(errors)} development errors occurred. Up to five are indexed below; original text is in the private prediction CSV.',
        'These are not final test errors. The expected labels are inherited from Kathy’s workbook and still deserve discussion for ambiguous fragments.','',
        '| Record | Reviewed label | Model prediction |','| --- | --- | --- |']
    for _,r in errors.head(5).iterrows():lines.append(f'| {r.record_id} | {r.label} | {r.prediction} |')
    lines+=['','Possible explanations to discuss with the reviewer (not proven causal diagnoses):',
        '- The list-creation vs list-reading boundary is difficult when a response only describes remembering a list.',
        '- A presentation/reminder phrase was routed to music, showing weak coverage of some calendar wording.',
        '- “Sato”/plans phrasing can be ambiguous without an explicit calendar request.',
        '- The model can interpret a list of foods as another scheduled action instead of an instruction to add items.',
        '- Some short expressions may not state a complete request; revisit the label rather than assume the model alone is wrong.',
        '', '## Limits and remaining work','',
        '- Five-to-seven development examples per class; results are sensitive to individual errors.',
        '- 24 edited, two pending, two non-answer entries and one punctuation-only training duplicate remain held.',
        '- Punctuation-only team duplicates are checked; semantic near-paraphrase review is not automated proof of independence.',
        '- Upstream MASSIVE labels/text can be imperfect and are not Team 20 reviewed contributions.',
        '- Respondent identity/location was not collected; this is scenario-grouped, not unseen-speaker testing.',
        '- Private assessment permission is recorded and split minimums pass. Public release is unconfirmed.',
        '- Final test and submission evidence remain incomplete.',
        '', '## Reproducibility','',
        f"Python {result['python']}; scikit-learn {result['sklearn']}. Random seed 42. Character TF-IDF 2–5 grams; logistic regression max_iter=1000.",
        'Input/model hashes and exact reports: reports/development.json, reports/readiness.json and models/selection.json.',
        'Selected external IDs: reports/external_selected_ids.csv. Dependencies: requirements-lock.txt.',
        '', '## Final test','', '**NOT RUN.** Do not report development metrics as final test performance.',
        'The current prepared data pass the structural and recorded-permission gates. The one guarded final evaluation is still pending.']
    test_path=ROOT/'reports/test.json'
    if test_path.exists():
        final=json.loads(test_path.read_text());score=final['model'];n=final['test_size']
        start=lines.index('## Final test')
        lines=lines[:start]+['## Final test','',
            f"Frozen condition: **{final['selected_condition']}**. Evaluated once on {n} independently reviewed test records.",
            f"Correct: {round(score['accuracy']*n)}/{n}; accuracy: {score['accuracy']:.4f}; macro-F1: {score['macro_f1']:.4f}.",
            f"Majority comparator accuracy: {final['majority_baseline']['accuracy']:.4f}; macro-F1: {final['majority_baseline']['macro_f1']:.4f}.",
            'No baseline-only final test comparison was run; the MASSIVE improvement claim is limited to development data.','',
            '| Intent | Test examples | F1 |','| --- | ---: | ---: |']
        for label in score['label_order']:
            r=score['report'][label];lines.append(f"| {label} | {int(r['support'])} | {r['f1-score']:.3f} |")
        mistakes=pd.read_csv(ROOT/'reports/test_predictions.csv');mistakes=mistakes[mistakes.label.ne(mistakes.prediction)]
        lines+=['',f'{len(mistakes)} actual final-test errors. Five examples below; all predictions remain private in reports/test_predictions.csv.','',
            '| Record | Reviewed label | Prediction |','| --- | --- | --- |']
        for _,r in mistakes.head(5).iterrows():lines.append(f'| {r.record_id} | {r.label} | {r.prediction} |')
        lines+=['','Calendar creation was confused with reading a calendar twice. Weather questions were confused with news twice. These are observed confusions, not proven causes.',
            'Some gold labels remain debatable: a reminder to fetch items is labelled list addition, and a song recommendation is labelled playback. Keep the frozen results intact; disclose these concerns instead of relabelling after scoring.',
            'Confusion matrix and full per-label precision/recall/support: reports/test.json. Frozen data/model hashes: models/freeze.json.',
            'Test examples were inspected for provenance and overlap before scoring. This is not unseen-speaker testing or proof of broad Sheng comprehension.']
        lines=[line for line in lines if line!='No real final test predictions were made.']
        lines=[line.replace('- Final test and submission evidence remain incomplete.','- Final test is complete; final submission evidence remains incomplete.') for line in lines]
    (ROOT/'docs/RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('Updated docs/RESULTS.md from saved development outputs.')

if __name__=='__main__':report()
