"""Team 20's plain-language presentation of the trained Sheng classifier."""
from pathlib import Path
import html
import json
import pandas as pd
import joblib
import streamlit as st

ROOT = Path(__file__).resolve().parent
from src.common import INTENTS,sha

NAMES = dict(zip(INTENTS, [
    'Ask about the weather', 'Ask the time or date', 'Set an alarm',
    'Add something to a calendar', 'Check a calendar', 'Create a list or add to one',
    'Read a list', 'Play music', 'Get the news', 'Ask what a word means']))
SIMULATED = dict(zip(INTENTS, [
    'I would look up the weather forecast.', 'I would show the current time or date.',
    'I would ask you to confirm the alarm time.', 'I would ask for the event details before adding it.',
    'I would show your calendar.', 'I would ask which list and item to add.',
    'I would show the items on your list.', 'I would ask which song or playlist to play.',
    'I would show recent headlines.', 'I would ask which word you want explained.']))
SELECTION=ROOT/'models/selection.json'
selection=json.loads(SELECTION.read_text()) if SELECTION.exists() else {}
MODEL=ROOT/'models'/(selection.get('condition','untrained')+'.joblib')
METRICS=ROOT/'reports/development.json'
PHOTO=ROOT/'assets/kibera-craft.jpg'

st.set_page_config(page_title='Rada | Team 20', layout='wide')
st.markdown('''<style>
.stApp {background:#fffdf7;color:#172126;}
[data-testid="stHeader"] {background:#fffdf7;}
.block-container {max-width:1140px;padding-top:5rem;padding-bottom:3rem;}
h1,h2,h3,p,label {color:#172126;}
h1 {font-family:Arial,sans-serif!important;font-weight:800!important;font-size:clamp(2.7rem,6vw,4.6rem)!important;letter-spacing:-2.5px;line-height:1.07!important;}
h2,h3 {font-family:Arial,sans-serif!important;font-weight:700!important;letter-spacing:-.5px;}
.nav {display:flex;justify-content:space-between;gap:12px;align-items:baseline;border-bottom:2px solid #172126;padding-bottom:12px;margin-bottom:30px;flex-wrap:wrap;}
.logo {font:bold 32px Arial,sans-serif;letter-spacing:-2px;}.logo span {color:#275ca7;}
.team {font:13px Arial,sans-serif;color:#495861;}
.hello {display:inline-block;background:#f3d559;padding:6px 11px;font-size:14px;font-weight:700;transform:rotate(-2deg);margin:12px 0;}
.lead {font-size:20px;line-height:1.6;max-width:540px;color:#364b58;}
.answer {border-left:6px solid #275ca7;background:#ecf1f8;padding:20px 24px;margin-top:18px;}
.answer p {font-size:15px;margin:0;color:#374d5a;}.answer h3 {font-size:28px;margin:8px 0;color:#143d78;}
.small-note {font-size:14px;line-height:1.6;color:#52616a;}
.bottom {border-top:2px solid #172126;margin-top:35px;padding-top:15px;font-size:13px;color:#495861;}
[data-testid="stTextArea"] textarea {background:white!important;color:#172126!important;border:1px solid #697d89!important;border-radius:0!important;font-size:18px!important;}
[data-testid="stButton"] button {min-height:44px;border-radius:0!important;}
[data-testid="stButton"] button[kind="primary"] {background:#204f91!important;border-color:#204f91!important;}
[data-testid="stButton"] button[kind="primary"] p {color:white!important;}
[data-testid="stTabs"] button p {font-size:16px!important;}
[data-testid="stImage"] img {border-radius:0;}
@media(max-width:640px) {.block-container{padding:4.5rem 1.25rem 2rem;}h1{letter-spacing:-1px;}}
</style>''', unsafe_allow_html=True)
st.markdown('<div class="nav"><div class="logo">rada<span>.</span></div><div class="team">Team 20 · Strathmore NLP Datathon 2026</div></div>',unsafe_allow_html=True)
words,picture=st.columns([1,1.15],gap='large')
with words:
    st.markdown('<div class="hello">Sheng kwa assistant.</div>',unsafe_allow_html=True)
    st.title('Unauliza nini?')
    st.markdown('<p class="lead">You write a request in Sheng.<br>Rada guesses what you want to do.</p>',unsafe_allow_html=True)
    st.write('Ask for music, set an alarm, check the weather. We’re testing whether a model can recognise the request in the way you would actually say it.')
    st.caption('A class prototype by Team 20 · Written Kiswahili/Sheng · Final test completed.')
with picture:
    if PHOTO.exists():
        st.image(str(PHOTO),width='stretch')
        st.caption('Kibera, Nairobi · Paul Were Abura at Victorious Bones Crafts, 2017. Photo: Brian Otieno / Bryan Jaybee.')

try_it,results,about=st.tabs(['Try it','How it’s doing','About our project'])
if not MODEL.exists():
    st.info('The trained model is not available yet. See the project README for setup.')
    st.stop()

@st.cache_resource
def load_model(path,stamp):
    return joblib.load(path)
if sha(MODEL)!=selection.get('model_sha256'):
    st.error('Model and saved results do not match. Check the training run.');st.stop()
comparison=json.loads(METRICS.read_text(encoding='utf-8')) if METRICS.exists() else None
m=comparison['runs'][selection['condition']] if comparison else None
readiness=json.loads((ROOT/'reports/readiness.json').read_text())
if (not m or m['model_sha256']!=selection['model_sha256'] or
        comparison['reviewed_sha256']!=selection['reviewed_sha256'] or
        readiness['reviewed_sha256']!=selection['reviewed_sha256']):
    st.error('The model, data and displayed results belong to different runs. Refresh the verified development run.');st.stop()
pack=load_model(str(MODEL),MODEL.stat().st_mtime_ns)
final_path=ROOT/'reports/test.json'
final=json.loads(final_path.read_text()) if final_path.exists() else None
if final and (final['freeze']['model_sha256']!=selection['model_sha256'] or final['freeze']['reviewed_sha256']!=selection['reviewed_sha256']):
    st.error('Final results and the loaded model do not match.');st.stop()

with try_it:
    entry,guide=st.columns([1.6,1],gap='large')
    with entry:
        st.subheader('Say it how you’d say it.')
        st.write('Type what you would ask an assistant. Please leave out personal details.')
        text=st.text_area('Your request',placeholder='For example: Nichezee doba',height=115,key='request')
        if st.button('What am I asking?',type='primary',width='stretch'):
            if not text.strip():
                st.info('Type a request first.')
            else:
                probabilities=pack['model'].predict_proba([text])[0]
                label=pack['model'].classes_[probabilities.argmax()]
                st.markdown(f'<div class="answer"><p>Rada thinks you want to…</p><h3>{html.escape(NAMES[label])}</h3></div>',unsafe_allow_html=True)
                st.write('That’s the guess. This demo doesn’t actually play music, set alarms or carry out the request.')
                st.info('Simulated response: '+SIMULATED[label])
                with st.expander('See the model’s scores'):
                    st.write(f'Top score: {probabilities.max():.1%}. This is not a guarantee that the answer is right.')
                    st.caption('Technical name: uncalibrated model probability. The label used in our code is '+label+'.')
                    st.bar_chart({NAMES[k]:float(v) for k,v in zip(pack['model'].classes_,probabilities)},horizontal=True)
    with guide:
        st.subheader('What can it recognise?')
        st.write('Weather · Time and date · Alarms · Calendar events · Lists · Music · News · Word meanings')
        st.markdown('**Try changing the wording.** Does it still understand? Then try something it wasn’t trained to recognise.')
        st.caption('It has to pick one of ten categories, even when none fits. If it gets your request wrong, that’s a useful failure to discuss.')

with results:
    st.subheader('So, does it work?')
    if final:
        score=final['model'];n=final['test_size']
        st.write(f"On the final {n} test requests, Rada got **{round(score['accuracy']*n)}/{n} right ({score['accuracy']:.1%})**. These examples were kept out of training and model selection.")
        st.caption(f"Macro-F1: {score['macro_f1']:.3f}. The model that always picks the most common training category got {final['majority_baseline']['accuracy']:.1%} right. Each category has only 5–7 test examples; this does not establish performance across Nairobi or all Sheng speakers.")
        st.bar_chart({NAMES[k]:score['report'][k]['f1-score'] for k in score['label_order']},horizontal=True)
        st.download_button('Download final test results',final_path.read_bytes(),file_name='rada_final_test.json',mime='application/json')
        st.subheader('Earlier model comparison')
    if m:
        st.write(f"On {m['dev_rows']} check examples kept out of training, it matched Kathy’s reviewed labels about **{m['model']['accuracy']:.0%} of the time**.")
        remaining=len(readiness['shortfalls'])
        if remaining or not readiness['permission_for_assessment_confirmed']:
            st.warning(f'Development results only. {remaining} category/split minimums remain unresolved. Assessment permission is '+('confirmed.' if readiness['permission_for_assessment_confirmed'] else 'still being documented.')+' The final test has not been run.')
        else:
            st.info('These are development results used to choose a model. Final test results are reported separately.')
        st.write(f"This version learned from {m['team_train_rows']} team examples and {m['external_train_rows']} extra Kiswahili examples from MASSIVE. The separate final test contains {readiness['split_totals']['test']} team examples.")
        st.markdown('**Did the extra Kiswahili data help?**')
        labels={'baseline':'Our data only','massive_20':'Our data + 200 MASSIVE examples','massive_50':'Our data + 500 MASSIVE examples'}
        st.dataframe(pd.DataFrame([{'Training data':labels[name],'Correct guesses':f"{round(r['model']['accuracy']*r['dev_rows'])}/{r['dev_rows']}",'Accuracy':f"{r['model']['accuracy']:.1%}"} for name,r in comparison['runs'].items()]),hide_index=True)
        st.caption('Same model settings and same 55 development examples. The best run got two more right than the baseline; this small comparison does not establish final-test performance.')
        st.subheader('What we’re checking next')
        st.write('Final testing is complete. We’re now checking the interface and preparing an honest demonstration of successes and failures. Similar short phrases and context-dependent requests remain limitations.')
        with st.expander('How we measured it'):
            st.write('We use the organiser’s baseline: character TF-IDF and logistic regression. It learns useful patterns of letters from training examples, then uses them to choose one of ten request types.')
            st.write(f"Development accuracy: {m['model']['accuracy']:.4f}. Macro-F1: {m['model']['macro_f1']:.4f}. Majority baseline macro-F1: {m['majority_baseline']['macro_f1']:.4f}.")
            st.write('Accuracy is the share of correct guesses. Macro-F1 averages a score for each category, so common categories do not dominate. The majority baseline always guesses the most common training category.')
            st.bar_chart({NAMES[k]:m['model']['report'][k]['f1-score'] for k in m['model']['label_order']},horizontal=True)
            st.caption('Development F1 by category. Each category has only 5–7 check examples, so these scores can change a lot.')
            st.download_button('Download the results',METRICS.read_bytes(),file_name='rada_early_results.json',mime='application/json')

with about:
    st.subheader('What we wanted to find out')
    st.write('Can a small model tell what someone is asking for when they write in Kiswahili and Sheng? That’s the question behind Rada.')
    st.subheader('Where the words came from')
    st.write('We shared everyday situations in a form and asked people to write what they would naturally say to an assistant. Kathy reviewed the original 386 answers. The latest form export has nine additional answers that have not been included in this run. We did not collect audio.')
    st.write('This run uses 324 accepted answers: 213 for training, 55 for development and 56 reserved for final testing. Two original answers were accepted after follow-up review, and one new human-written response was added with permission. We held 24 edited answers, two pending answers, two non-answers and one punctuation-only duplicate; 34 were rejected. Original source files and decisions are preserved.')
    st.subheader('References')
    st.markdown('- [Photograph: Bone jewelers of Kibera 01](https://commons.wikimedia.org/wiki/File:Bone_jewelers_of_Kibera_01.jpg) — Brian Otieno / Bryan Jaybee, 2017. [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Displayed without edits.\n- Strathmore NLP Datathon Starter Kit v2 — the starting code and ten request categories.\n- [MASSIVE 1.1](https://huggingface.co/datasets/AmazonScience/massive) — extra Kiswahili training examples, selected from its training partition. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).')
    st.caption('Team contributions and external training examples are counted separately.')
    st.subheader('Who built it')
    st.write('Team 20 — Kathy Auma, Irene Gitau, Hafswa Sufi.')
    st.caption('The raw responses and review records are not included in this demo. Permission for public dataset release is still being clarified.')
st.markdown('<div class="bottom">Rada · Team 20 · A work in progress, with real mistakes to learn from.</div>',unsafe_allow_html=True)
