"""
Prediction Module
"""

import joblib


class Predictor:

    def __init__(self):

        self.model = joblib.load(
            "models/obesity_model.pkl"
        )

    def predict(self, input_df):

        prediction = self.model.predict(input_df)

        return prediction[0]