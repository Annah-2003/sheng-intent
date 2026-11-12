"""Describe saved metrics without fitting a model or predicting a test example."""
import csv
import json
from src.common import ROOT

def report():
    development=json.loads((ROOT/'reports/development.json').read_text())
    final=json.loads((ROOT/'reports/test.json').read_text())
    score=final['model'];n=final['test_size'];labels=score['label_order']
    lines=['# Model results and error analysis','',
        f"The frozen **{final['selected_condition']}** model scored **{round(score['accuracy']*n)}/{n} correct ({score['accuracy']:.1%} accuracy), macro-F1 {score['macro_f1']:.4f}** on its single final evaluation.",
        f"Majority comparator: {final['majority_baseline']['accuracy']:.1%} accuracy, macro-F1 {final['majority_baseline']['macro_f1']:.4f}.",
        'The selected model fitted 213 team training records plus 500 upstream MASSIVE training records. No development or final-test records were fitted.','',
        '## Development comparison','',
        '| Condition | External training rows | Correct out of 55 | Accuracy | Macro-F1 |',
        '| --- | ---: | ---: | ---: | ---: |']
    for name,run in development['runs'].items():
        s=run['model'];lines.append(f"| {name} | {run['external_train_rows']} | {round(s['accuracy']*run['dev_rows'])} | {s['accuracy']:.4f} | {s['macro_f1']:.4f} |")
    lines+=['','Three fixed conditions used the same classifier settings and development set. Highest development macro-F1 selected massive_50; exact ties prefer fewer external rows. Samples were nested and fixed with seed 42.',
        'The development improvement is two more correct predictions than team-only training. It does not establish statistical significance, improvement in every category or a final-test improvement over the team-only classifier, which was not scored on final test.','',
        '## Final per-intent performance','',
        '| Intent | Test count | Precision | Recall | F1 |',
        '| --- | ---: | ---: | ---: | ---: |']
    rows=[]
    for label in labels:
        r=score['report'][label];row=[label,int(r['support']),r['precision'],r['recall'],r['f1-score']];rows.append(row)
        lines.append(f"| {label} | {int(r['support'])} | {r['precision']:.3f} | {r['recall']:.3f} | {r['f1-score']:.3f} |")
    lines+=['','Each class contains only 5–7 test records. Accuracy is the fraction correct; macro-F1 averages F1 equally across intents. Weather and calendar creation are weakest (F1 0.600).','',
        '## Confusion matrix','',
        'Rows are reviewed labels; columns are predictions. The numeric order below matches reports/test.json.','',
        '| Actual / predicted | '+' | '.join(str(i+1) for i in range(len(labels)))+' |',
        '| --- | '+' | '.join('---:' for _ in labels)+' |']
    for i,row in enumerate(score['confusion_matrix']):lines.append('| '+str(i+1)+' | '+' | '.join(map(str,row))+' |')
    lines+=['','Order: '+', '.join(f'{i+1} {label}' for i,label in enumerate(labels))+'.','',
        '## Five observed disagreements','',
        'There were 13 final-test disagreements. Original wording remains in the private prediction file. Explanations below are plausible interpretations, not proven causal diagnoses. No gold label was changed after scoring.','',
        '| Record | Reviewed label | Prediction | What to examine |','| --- | --- | --- | --- |',
        '| T20-R008-B5Q04 | calendar_set | calendar_query | A request to save a meeting was confused with reading a calendar. |',
        '| T20-R010-B5Q01 | weather_query | news_query | A question about continuing rain was routed to news. |',
        '| T20-R008-B5Q10 | qa_definition | calendar_set | A generic explanation request lacks a named concept; the reviewed definition label is debatable. |',
        '| T20-R010-B5Q06 | lists_createoradd | calendar_set | A reminder to fetch items could be a scheduled reminder; this exposes a gold-label boundary concern. |',
        '| T20-R043-B5Q08 | play_music | datetime_query | A recommendation request is not an explicit playback instruction, so its reviewed label is also debatable. |','',
        'Calendar creation was confused with calendar lookup twice; weather was confused with news twice. These counts come from the saved confusion matrix.','',
        '## Limits and next work','',
        'Convenience recruitment, English prompts, short context-dependent phrases, limited scenario families, one main reviewer and respondent overlap limit generalisation. Scenario grouping and punctuation checks do not prove semantic independence across scenarios. A passing structural validator does not establish perfect labels, consent evidence or naturalness.',
        'The interface forces a known class for unsupported requests and its model probabilities are uncalibrated. No usability, accessibility, time-saving or community-access improvement has been measured. A future study should separately assess wording coverage, annotation consistency and user comprehension.',
        'Keep the frozen experiment intact. Any annotation revision or new model comparison should be a separately declared experiment with a suitable evaluation plan.','',
        '## Reproducibility','',
        f"Python {development['python']}; scikit-learn {development['sklearn']}. Character TF-IDF 2–5 grams, logistic regression max_iter=1000, random_state=42.",
        'Full metrics: reports/development.json and reports/test.json. Derived tables: per_intent_test.csv and confusion_matrix.csv. Frozen model/data hashes: models/freeze.json. External selection IDs: reports/external_selected_ids.csv. Private predictions and reviewed data are supplied only through the restricted assessment route.',
        'The readiness and selection JSON files are pre-test snapshots; test.json plus freeze.json establish completion. Report generation reads saved outputs and does not predict again.']
    (ROOT/'docs/RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    for name,headers,data in [('per_intent_test.csv',['intent','test_count','precision','recall','f1'],rows),
        ('confusion_matrix.csv',['actual_intent']+labels,[[label]+row for label,row in zip(labels,score['confusion_matrix'])])]:
        with (ROOT/'reports'/name).open('w',newline='',encoding='utf-8') as f:
            writer=csv.writer(f);writer.writerow(headers);writer.writerows(data)
    print('Wrote results narrative and derived metric tables from saved outputs; no model inference.')

if __name__=='__main__':report()
