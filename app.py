import streamlit as st
import pandas as pd

from services.predictor_service import PredictionService
from services.data_service import DataService

st.set_page_config(
    page_title="AI Powered Obesity Risk Analytics",
    page_icon="🏥",
    layout="wide"
)

service = PredictionService()
data_service = DataService()

st.write("✅ Services Loaded")

st.title("🏥 AI Powered Obesity Risk Analytics")

st.write("✅ UI Loaded")

st.markdown(
    "Predict obesity prevalence using Machine Learning."
)

year = st.number_input(
    "Year",
    min_value=2011,
    max_value=2030,
    value=2023
)

location_desc = st.selectbox(
    "State",
    data_service.get_unique("LocationDesc")
)

location_abbr = data_service.get_state_abbreviation(
    location_desc
)

question = st.selectbox(
    "Question",
    data_service.get_unique("Question")
)

age = st.selectbox(
    "Age Group",
    data_service.get_unique("Age(years)")
)

education = st.selectbox(
    "Education",
    data_service.get_unique("Education")
)

sex = st.selectbox(
    "Sex",
    data_service.get_unique("Sex")
)

income = st.selectbox(
    "Income",
    data_service.get_unique("Income")
)

race = st.selectbox(
    "Race / Ethnicity",
    data_service.get_unique("Race/Ethnicity")
)

if st.button("Predict"):

    st.write("✅ Predict Button Clicked")

    prediction = service.predict(

        year,
        location_abbr,
        location_desc,
        question,
        age,
        education,
        sex,
        income,
        race

    )

    st.write(prediction)

    st.success(
        f"Predicted Obesity Percentage : {prediction:.2f}%"
    )