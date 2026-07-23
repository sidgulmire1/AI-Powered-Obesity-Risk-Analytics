"""
Model Training Module

Loads cleaned dataset, preprocesses it using a Pipeline,
trains a Random Forest model,
evaluates performance,
and saves the complete pipeline.
"""

import os
import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


class ModelTrainer:

    def __init__(self, data_path):

        self.data_path = data_path

        self.df = None

        self.model = None

        self.X_train = None
        self.X_test = None

        self.y_train = None
        self.y_test = None

    # ==========================================================
    # LOAD DATA
    # ==========================================================

    def load_data(self):

        self.df = pd.read_csv(self.data_path)

        print("\nDataset Loaded Successfully")
        print(self.df.shape)

    # ==========================================================
    # PREPARE DATA
    # ==========================================================

    def prepare_data(self):

        target = "Data_Value"

        self.df = self.df.dropna(subset=[target])

        X = self.df.drop(columns=[target])

        y = self.df[target]

        categorical_columns = X.select_dtypes(
            include=["object", "string"]
        ).columns

        numeric_columns = X.select_dtypes(
            exclude=["object", "string"]
        ).columns

        numeric_transformer = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(strategy="median")
                )
            ]
        )

        categorical_transformer = Pipeline(
            steps=[
                (
                    "imputer",
                    SimpleImputer(strategy="most_frequent")
                ),
                (
                    "encoder",
                    OneHotEncoder(
                        handle_unknown="ignore"
                    )
                )
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "num",
                    numeric_transformer,
                    numeric_columns
                ),
                (
                    "cat",
                    categorical_transformer,
                    categorical_columns
                )
            ]
        )

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        self.model = Pipeline(
            steps=[
                (
                    "preprocessor",
                    preprocessor
                ),
                (
                    "model",
                    RandomForestRegressor(
                        n_estimators=100,
                        random_state=42,
                        n_jobs=-1
                    )
                )
            ]
        )

        print("\nTrain Test Split Completed")

    # ==========================================================
    # TRAIN
    # ==========================================================

    def train(self):

        print("\nTraining Started...\n")

        self.model.fit(
            self.X_train,
            self.y_train
        )

        print("Training Completed")

    # ==========================================================
    # EVALUATE
    # ==========================================================

    def evaluate(self):

        predictions = self.model.predict(
            self.X_test
        )

        mae = mean_absolute_error(
            self.y_test,
            predictions
        )

        mse = mean_squared_error(
            self.y_test,
            predictions
        )

        rmse = mse ** 0.5

        r2 = r2_score(
            self.y_test,
            predictions
        )

        print("\nModel Performance")
        print("-" * 40)
        print(f"MAE  : {mae:.3f}")
        print(f"RMSE : {rmse:.3f}")
        print(f"R²   : {r2:.3f}")

    # ==========================================================
    # SAVE MODEL
    # ==========================================================

    def save_model(self):

        os.makedirs(
            "models",
            exist_ok=True
        )

        joblib.dump(
            self.model,
            "models/obesity_model.pkl"
        )

        print("\nPipeline Saved Successfully")
        print("models/obesity_model.pkl")


if __name__ == "__main__":

    trainer = ModelTrainer(
        "data/processed/clean_data.csv"
    )

    trainer.load_data()

    trainer.prepare_data()

    trainer.train()

    trainer.evaluate()

    trainer.save_model()