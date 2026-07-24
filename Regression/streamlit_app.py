"""
House Price Predictor - Streamlit UI

Run the Class_16_ML.ipynb notebook first so it saves these files in the
same folder as this script:
    best_house_price_model.pkl
    label_encoders.pkl
    standard_scaler_ohe.pkl
    ohe_columns.pkl

Then run:
    pip install streamlit joblib pandas scikit-learn
    streamlit run streamlit_app.py
"""

import joblib
import pandas as pd
import streamlit as st

st.set_page_config(page_title="House Price Predictor", page_icon="🏠", layout="centered")


@st.cache_resource
def load_artifacts():
    model = joblib.load("best_house_price_model.pkl")
    label_encoders = joblib.load("label_encoders.pkl")
    scaler = joblib.load("standard_scaler_ohe.pkl")
    ohe_columns = joblib.load("ohe_columns.pkl")
    return model, label_encoders, scaler, ohe_columns


model, label_encoders, scaler, ohe_columns = load_artifacts()
CATEGORICAL_COLS = list(label_encoders.keys())
CHOICES = {col: list(label_encoders[col].classes_) for col in CATEGORICAL_COLS}

st.title("🏠 House Price Predictor")
st.caption("Enter the property details and get an estimated price.")

col1, col2 = st.columns(2)

with col1:
    rooms = st.number_input("Rooms", min_value=1, value=4, step=1)
    site_area = st.number_input("Site Area (sqm)", min_value=0.0, value=250.0)
    built_area = st.number_input("Built Area (sqm)", min_value=0.0, value=150.0)
    years = st.number_input("Property Age (yrs)", min_value=0, value=8, step=1)
    cbd = st.number_input("Distance to CBD (km)", min_value=0.0, value=2.5)
    bus = st.number_input("Distance to Bus Station (km)", min_value=0.0, value=0.5)
    schools = st.number_input("Distance to Schools (km)", min_value=0.0, value=1.2)

with col2:
    material = st.selectbox("Construction Material", CHOICES["Construction_Materials"])
    typology = st.selectbox("Housing Typology", CHOICES["Housing_Typology"])
    grading = st.selectbox("Land Value Grading", CHOICES["Land_Value_Grading"])
    road = st.selectbox("Nearest Road Type", CHOICES["Type_of_Nearest_Road"])

if st.button("Estimate Price", type="primary", use_container_width=True):
    row = {
        "Number_of_Rooms": rooms,
        "Site_Area_sqm": site_area,
        "Built_Area_sqm": built_area,
        "Property_Years": years,
        "Construction_Materials": material,
        "Housing_Typology": typology,
        "Land_Value_Grading": grading,
        "Proximity_to_CBD_km": cbd,
        "Proximity_to_Bus_Station_km": bus,
        "Type_of_Nearest_Road": road,
        "Proximity_to_Schools_km": schools,
    }
    single_df = pd.DataFrame([row])

    encoded = pd.get_dummies(single_df, columns=CATEGORICAL_COLS, dtype=int)
    encoded = encoded.reindex(columns=ohe_columns, fill_value=0)

    X = scaler.transform(encoded)
    pred = model.predict(X)[0]

    st.success(f"Estimated Price: **{pred:,.0f} ETB**")
