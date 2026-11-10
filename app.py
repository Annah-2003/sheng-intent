from pathlib import Path

import joblib
import streamlit as st

from core import FRIENDLY, extract


TRACKS = ("intent", "sentiment", "semantic")

st.set_page_config(page_title="Sheng Intent Demo", page_icon="🌍")
st.title("Sheng Intent Demo")
st.write(
    "Try a sentence with a locally trained model. Predictions are demonstrations, "
    "not confirmed actions or a substitute for human review."
)

track = st.selectbox("Task", TRACKS, format_func=str.title)
model_path = Path("artifacts") / track / "model.joblib"

if not model_path.exists():
    st.info(
        f"No {track} model was found at `{model_path}`. Train the selected task first; "
        "see `NEXT_STEPS.md` for the project workflow."
    )
    st.stop()

# Only load model files created by your team and kept in this project.
pack = joblib.load(model_path)
if pack["track"] != track:
    raise ValueError(
        f"The model at {model_path} is for {pack['track']!r}, not {track!r}. "
        "Train the selected task or restore its matching model artifact."
    )

if pack["practice"]:
    st.warning(
        "Practice mode: this model was trained on constructed English teaching "
        "examples. Its predictions do not demonstrate Sheng performance."
    )

st.caption(f"Model language: {pack['language']}")

with st.form("prediction_form"):
    text = st.text_area(
        "Enter one sentence",
        placeholder="Type a sentence in the model's training language",
        height=120,
    )
    submitted = st.form_submit_button("Predict")

if submitted:
    if not text.strip():
        st.info("Enter a sentence before predicting.")
    else:
        model = pack["model"]
        prediction = model.predict([text])[0]
        probabilities = model.predict_proba([text])[0]
        ranked = sorted(
            zip(model.classes_, probabilities),
            key=lambda item: item[1],
            reverse=True,
        )

        heading = (
            "Predicted sentiment"
            if track == "sentiment"
            else "Predicted intent"
            if track == "intent"
            else "Predicted action"
        )
        st.subheader(heading)
        st.write(FRIENDLY.get(prediction, prediction))
        st.caption(f"Model probability (uncalibrated): {max(probabilities):.1%}")

        st.markdown("**Top candidate labels**")
        for label, probability in ranked[:3]:
            st.write(f"{FRIENDLY.get(label, label)} — {probability:.1%}")

        if track == "semantic":
            st.markdown("**Extracted slots**")
            st.json({"intent": prediction, "slots": extract(text, pack["slot_memory"])})
            st.caption(
                "The baseline only matches surface values seen in training. "
                "Unseen values may be missed; no external action is performed."
            )
        elif track == "intent":
            st.info("This is a simulated route only. No external action was performed.")
        else:
            st.info(
                "This is a sentence-level opinion label, not emotion detection, "
                "sarcasm understanding, or a diagnosis."
            )

st.caption(
    "This demo makes no external API calls; text is processed by the server running Streamlit."
)
