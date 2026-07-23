"""
Data Service

Loads dropdown values and state mappings.
"""

import pandas as pd


class DataService:

    def __init__(self):

        self.df = pd.read_csv(
            "data/processed/clean_data.csv"
        )

    def get_unique(self, column):

        values = self.df[column].dropna().unique()

        return sorted(values.tolist())

    def get_state_abbreviation(self, location_desc):

        row = self.df[
            self.df["LocationDesc"] == location_desc
        ].iloc[0]

        return row["LocationAbbr"]
    
    def get_question_details(self, question):

        row = self.df[
            self.df["Question"] == question
        ].iloc[0]

        return {

            "Class": row["Class"],

            "Topic": row["Topic"],

            "Datasource": row["Datasource"],

            "Data_Value_Unit": row["Data_Value_Unit"],

            "Data_Value_Type": row["Data_Value_Type"]

        }