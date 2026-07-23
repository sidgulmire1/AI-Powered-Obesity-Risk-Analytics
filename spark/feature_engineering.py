"""
Feature Engineering Module

Loads cleaned dataset, performs feature engineering
and saves ML-ready dataset.
"""

import joblib
import os

import pandas as pd

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder


class FeatureEngineering:

    def __init__(self, input_path):

        self.input_path = input_path

        self.df = None

    # ==========================================================
    # LOAD DATA
    # ==========================================================

    def load_data(self):

        self.df = pd.read_csv(self.input_path)

        print("\nClean Dataset Loaded Successfully")

        print(self.df.shape)

    # ==========================================================
    # REMOVE MISSING TARGET
    # ==========================================================

    def remove_missing_target(self):

        before = len(self.df)

        self.df = self.df.dropna(subset=["Data_Value"])

        after = len(self.df)

        print(f"\nRows Removed : {before-after}")

    # ==========================================================
    # HANDLE MISSING VALUES
    # ==========================================================

    def handle_missing_values(self):
        
        # Remove columns that contain only missing values
        self.df = self.df.dropna(axis=1, how="all")

        categorical_columns = self.df.select_dtypes(
            include=["object", "string"]
        ).columns

        numeric_columns = self.df.select_dtypes(
            exclude=["object", "string"]
        ).columns

        num_imputer = SimpleImputer(
            strategy="median"
        )

        cat_imputer = SimpleImputer(
            strategy="most_frequent"
        )

        self.df[numeric_columns] = num_imputer.fit_transform(
            self.df[numeric_columns]
        )

        self.df[categorical_columns] = cat_imputer.fit_transform(
            self.df[categorical_columns]
        )

        print("\nMissing Values Handled")

    # ==========================================================
    # ENCODE FEATURES
    # ==========================================================

    def encode_features(self):

        categorical_columns = self.df.select_dtypes(
            include=["object", "string"]
        ).columns

        categorical_columns = categorical_columns.drop(
            "Data_Value",
            errors="ignore"
        )

        encoder = OneHotEncoder(
            sparse_output=False,
            handle_unknown="ignore"
        )

        encoded = encoder.fit_transform(
            self.df[categorical_columns]
        )

        os.makedirs("artifacts", exist_ok=True)

        joblib.dump(
            encoder,
            "artifacts/encoder.pkl"
        )

        encoded_df = pd.DataFrame(
            encoded,
            columns=encoder.get_feature_names_out(categorical_columns),
            index=self.df.index
        )

        self.df = self.df.drop(
            columns=categorical_columns
        )

        self.df = pd.concat(
            [
                self.df.reset_index(drop=True),
                encoded_df.reset_index(drop=True)
            ],
            axis=1
        )

        print("\nCategorical Features Encoded")

        print(self.df.shape)
    # ==========================================================
    # SAVE
    # ==========================================================

    def save_feature_data(self):

        output = "data/processed/feature_data.csv"

        self.df.to_csv(

            output,

            index=False

        )

        print("\nFeature Dataset Saved")

        print(output)


if __name__ == "__main__":

    feature = FeatureEngineering(

        "data/processed/clean_data.csv"

    )

    feature.load_data()

    feature.remove_missing_target()

    feature.handle_missing_values()

    feature.encode_features()

    feature.save_feature_data()

    print("\nFeature Engineering Completed Successfully.")