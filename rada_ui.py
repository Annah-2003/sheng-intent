"""Team 20's plain-language presentation of the trained Sheng classifier."""
from pathlib import Path
import html
import json
import sys
import joblib
import streamlit as st

ROOT = Path(__file__).resolve().parent
if (ROOT / 'datathon-starter-kit').exists():
    sys.path.insert(0, str(ROOT / 'datathon-starter-kit'))
from core import INTENTS

NAMES = dict(zip(INTENTS, [
    'Ask about the weather', 'Ask the time or date', 'Set an alarm',
    'Add something to a calendar', 'Check a calendar', 'Create a list or add to one',
    'Read a list', 'Play music', 'Get the news', 'Ask what a word means']))
DEPLOY = ROOT / 'rada' if (ROOT / 'rada').exists() else ROOT
MODEL = DEPLOY / 'model.joblib' if (DEPLOY / 'model.joblib').exists() else ROOT / 'artifacts/preliminary/model.joblib'
METRICS = DEPLOY / 'dev_metrics.json' if (DEPLOY / 'dev_metrics.json').exists() else ROOT / 'artifacts/preliminary/dev_metrics.json'
PHOTO = DEPLOY / 'assets/kibera-craft.jpg'

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
    st.caption('A class project by Team 20. Still being tested and checked by a fluent speaker.')
with picture:
    if PHOTO.exists():
        st.image(str(PHOTO),use_container_width=True)
        st.caption('Kibera, Nairobi · Paul Were Abura at Victorious Bones Crafts, 2017. Photo: Brian Otieno / Bryan Jaybee.')

try_it,results,about=st.tabs(['Try it','How it’s doing','About our project'])
if not MODEL.exists():
    st.info('The trained model is not available yet. See the project README for setup.')
    st.stop()

@st.cache_resource
def load_model(path,stamp):
    return joblib.load(path)
pack=load_model(str(MODEL),MODEL.stat().st_mtime_ns)
m=json.loads(METRICS.read_text(encoding='utf-8')) if METRICS.exists() else None

with try_it:
    entry,guide=st.columns([1.6,1],gap='large')
    with entry:
        st.subheader('Say it how you’d say it.')
        st.write('Type what you would ask an assistant. Please leave out personal details.')
        text=st.text_area('Your request',placeholder='For example: Nichezee doba',height=115,key='request')
        if st.button('What am I asking?',type='primary',use_container_width=True):
            if not text.strip():
                st.info('Type a request first.')
            else:
                probabilities=pack['model'].predict_proba([text])[0]
                label=pack['model'].classes_[probabilities.argmax()]
                st.markdown(f'<div class="answer"><p>Rada thinks you want to…</p><h3>{html.escape(NAMES[label])}</h3></div>',unsafe_allow_html=True)
                st.write('That’s the guess. This demo doesn’t actually play music, set alarms or carry out the request.')
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
    if m:
        st.write(f"On {m['dev_rows']} check examples from our collected responses, kept out of training, it matched the current labels about **{m['model']['accuracy']:.0%} of the time**.")
        st.warning('These are early results. A fluent reviewer still needs to check the answers and labels. We have not run the final test.')
        st.write(f"We used {m['train_rows']} examples to train it. The {m['dev_rows']} examples above help us find problems and choose improvements. Another 70 examples are set aside for later.")
        st.subheader('What we’re checking next')
        st.write('Some responses describe a situation rather than ask for anything. We need to remove unclear answers, check the labels, and make sure similar wording isn’t being used to both teach and test the model.')
        with st.expander('How we measured it'):
            st.write('We use the organiser’s baseline: character TF-IDF and logistic regression. It learns useful patterns of letters from training examples, then uses them to choose one of ten request types.')
            st.write(f"Development accuracy: {m['model']['accuracy']:.4f}. Macro-F1: {m['model']['macro_f1']:.4f}. Majority baseline macro-F1: {m['majority_baseline']['macro_f1']:.4f}.")
            st.write('Accuracy is the share of correct guesses. Macro-F1 averages a score for each category, so common categories do not dominate. The majority baseline always guesses the most common training category.')
            st.bar_chart({NAMES[k]:m['model']['report'][k]['f1-score'] for k in m['model']['label_order']},horizontal=True)
            st.caption('Development F1 by category. Each category has only 6–8 check examples, so these scores can change a lot.')
            st.download_button('Download the results',METRICS.read_bytes(),file_name='rada_early_results.json',mime='application/json')

with about:
    st.subheader('What we wanted to find out')
    st.write('Can a small model tell what someone is asking for when they write in Kiswahili and Sheng? That’s the question behind Rada.')
    st.subheader('Where the words came from')
    st.write('We shared everyday situations in a form and asked people to write what they would naturally say to an assistant. We received 44 submissions and 386 written answers. We did not collect audio.')
    st.write('We kept the original wording and logged small spacing changes. Eight repeated or clearly unusable entries were left out of the first run. A fluent reviewer will help us decide what belongs in the final dataset.')
    st.subheader('References')
    st.markdown('- [Photograph: Bone jewelers of Kibera 01](https://commons.wikimedia.org/wiki/File:Bone_jewelers_of_Kibera_01.jpg) — Brian Otieno / Bryan Jaybee, 2017. [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Displayed without edits.\n- Strathmore NLP Datathon Starter Kit v2 — the starting code and ten request categories.\n- [MASSIVE dataset](https://github.com/alexa/massive) — background for the organiser’s label scheme; no MASSIVE examples were used to train this version.')
    st.caption('Training data in this version: Team 20’s collected form responses only.')
    st.subheader('Who built it')
    st.write('Team 20 — Kathy Auma, Irene Gitau, Hafswa Sufi.')
    st.caption('The raw responses and review records are not included in this demo. Permission for public dataset release is still being clarified.')
st.markdown('<div class="bottom">Rada · Team 20 · A work in progress, with real mistakes to learn from.</div>',unsafe_allow_html=True)
