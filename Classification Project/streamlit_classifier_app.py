"""
SMS Spam Classifier - Streamlit UI (best model only)

Run train_classifiers.py first (needs SMSSpamCollection) to produce
best_model.pkl and results_summary.csv in the same folder as this script.

Then:
    pip install streamlit pandas joblib
    streamlit run streamlit_classifier_app.py
"""

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="SMS Spam Classifier", page_icon="📩", layout="centered")


@st.cache_resource
def load_model():
    return joblib.load("best_model.pkl")


bundle = load_model()
model = bundle["model"]
vectorizer = bundle["vectorizer"]
label_map = bundle["label_map"]
metrics = bundle["metrics"]

st.title("📩 SMS Spam Classifier")
st.caption(
    f"Using **{bundle['algorithm']}** + **{bundle['vectorizer_name']}** "
    f"(F1: {metrics['F1 Score']}, Accuracy: {metrics['Accuracy']})"
)

message = st.text_area(
    "Message", placeholder="Type or paste an SMS message here...", height=120
)

if st.button("Classify", type="primary", use_container_width=True):
    if not message.strip():
        st.warning("Enter a message first")
    else:
        X = vectorizer.transform([message]).astype("float32")
        pred = model.predict(X)[0]
        label = label_map[int(pred)]

        if label == "spam":
            st.error("🚨 SPAM")
        else:
            st.success("✅ HAM (not spam)")

        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)[0]
            st.caption(f"Confidence: {proba[int(pred)] * 100:.1f}%")
        elif hasattr(model, "decision_function"):
            score = model.decision_function(X)[0]
            st.caption(f"Decision score: {score:.3f}")

st.divider()
st.caption("Try one of these:")
examples = [
    "Congratulations! You've won a free ticket to Bahamas, call now to claim!",
    "Hey, are we still on for lunch tomorrow?",
    "URGENT: Your account has been suspended, verify now at bit.ly/xyz",
]
for ex in examples:
    st.code(ex, language=None)
