import streamlit as st
import joblib
import numpy as np
import pandas as pd
import requests

def main():
    st.title('Obesity Prediction App')

    gender = st.radio("Gender", ["Male", "Female"])
    age = st.number_input("Age", 0, 120)
    height = st.number_input("Height (in meters)", 0.0, 3.0)
    weight = st.number_input("Weight (in kg)", 0.0, 300.0)
    family_history_overweight = st.radio("Family History of Overweight", ["Yes", "No"])
    high_calorie_food = st.radio("High Calorie Food Consumption", ["Yes", "No"])
    vegetable_freq = st.slider("Vegetable Consumption Frequency (per week)", 0, 30)
    main_meals_per_day = st.slider("Main Meals per Day", 1, 10)
    snack_freq = st.selectbox("Snack Frequency", ["No", "Sometimes", "Frequently", "Always"])
    smoke = st.radio("Do you smoke?", ["Yes", "No"])
    water_intake = st.slider("Water Intake (liters/day)", 0.0, 10.0, step=0.1)
    calorie_monitoring = st.radio("Do you monitor your calorie intake?", ["Yes", "No"])
    physical_activity = st.slider("Physical Activity (hours/day)", 0.0,24.0, step=0.1)
    tech_time = st.slider("Technology Use Time (hours/day)", 0.0, 24.0, step=0.5)
    alcohol_freq = st.selectbox("Alcohol Consumption", ["No", "Sometimes", "Frequently", "Always"])
    transport_mode = st.selectbox("Transportation Mode", [
        "Walking", "Bike", "Motorbike", "Automobile", "Public Transportation"
    ])

    data = {
        "gender": gender,
        "age": int(age),
        "height": float(height),
        "weight": float(weight),
        "family_history_overweight": family_history_overweight,
        "high_calorie_food": high_calorie_food,
        "vegetable_freq": float(vegetable_freq),
        "main_meals_per_day": float(main_meals_per_day),
        "snack_freq": snack_freq,
        "smoke": smoke,
        "water_intake": float(water_intake),
        "calorie_monitoring": calorie_monitoring,
        "physical_activity": float(physical_activity),
        "tech_time": float(tech_time),
        "alcohol_freq": alcohol_freq,
        "transport_mode": transport_mode
    }

    df = pd.DataFrame([data])

    def format_prediction(pred):
        mapping = {
        "insufficient_weight": "Underweight",
        "normal_weight": "Normal Weight",
        "overweight_level_i": "Overweight Level I",
        "overweight_level_ii": "Overweight Level II",
        "obesity_type_i": "Obesity Type I",
        "obesity_type_ii": "Obesity Type II",
        "obesity_type_iii": "Obesity Type III"
        }
        return mapping.get(pred, pred)

    if st.button('Predict Obesity Level'):
        result = make_prediction(data)
        formatted = format_prediction(result)
        st.success(f'Predicted Obesity Level: {formatted}')

def make_prediction(features):
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=features)
        prediction = response.json()["prediction"]
        return prediction
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    main()
