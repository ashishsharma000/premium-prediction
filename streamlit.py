import streamlit as st
import pickle
import pandas as pd

# Load model
with open('insurance_pipeline.pkl', 'rb') as f:
    model = pickle.load(f)

st.title("Insurance Premium Predictor 💰")

# Inputs
age = st.number_input("Age", min_value=1, max_value=100)
sex = st.selectbox("Sex", ["male", "female"])

height = st.number_input("Height (in meters)")
weight = st.number_input("Weight (in kg)")

children = st.number_input("Children", min_value=0)
smoker = st.selectbox("Smoker", ["yes", "no"])
region = st.selectbox("Region", ["southwest", "southeast", "northwest", "northeast"])

# Predict
if st.button("Predict"):
    
    # 🔥 Calculate BMI
    bmi = weight / (height ** 2)

    input_data = pd.DataFrame([{
        "age": age,
        "sex": sex,
        "bmi": bmi,
        "children": children,
        "smoker": smoker,
        "region": region
    }])

    prediction = model.predict(input_data)

    st.success(f"Estimated Premium: ₹ {round(prediction[0], 2)}")