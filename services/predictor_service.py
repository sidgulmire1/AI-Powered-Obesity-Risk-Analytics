"""
Prediction Service

Receives UI inputs,
builds the dataframe,
calls Predictor.
"""

import pandas as pd

from ml.predict import Predictor
from services.data_service import DataService


class PredictionService:

    def __init__(self):

        self.predictor = Predictor()

        self.data_service = DataService()

    def predict(
        self,
        year,
        location_abbr,
        location_desc,
        question,
        age,
        education,
        sex,
        income,
        race
    ):

        question_info = self.data_service.get_question_details(
            question
        )

        data = {

            "YearStart": [year],
            "YearEnd": [year],

            "LocationAbbr": [location_abbr],
            "LocationDesc": [location_desc],

            "Datasource": [question_info["Datasource"]],

            "Class": [question_info["Class"]],

            "Topic": [question_info["Topic"]],

            "Question": [question],

            "Data_Value_Unit": [
                question_info["Data_Value_Unit"]
            ],

            "Data_Value_Type": [
                question_info["Data_Value_Type"]
            ],

            "Total": ["Total"],

            "Age(years)": [age],

            "Education": [education],

            "Sex": [sex],

            "Income": [income],

            "Race/Ethnicity": [race],

            "GeoLocation": ["Unknown"],

            "StratificationCategory1": ["Total"],

            "Stratification1": ["Total"]

        }

        input_df = pd.DataFrame(data)

        prediction = self.predictor.predict(input_df)

        return prediction