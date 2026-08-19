# AI Obesity Risk Analytics

An end-to-end machine learning application for estimating **population-level obesity prevalence** from demographic, socioeconomic, geographic, and survey characteristics.

The project combines **PySpark ETL, Scikit-learn, Random Forest Regression, and Streamlit** into a complete workflow from raw survey data to an interactive prediction dashboard.

> **Important:** This system estimates aggregate population prevalence. It is not an individual medical-risk predictor, diagnostic tool, or clinical decision-support system.

---

## Overview

Most machine-learning projects stop after model training and evaluation. This project extends the workflow into an interactive application:

```text
CDC BRFSS Data
      ↓
PySpark ETL
      ↓
Structural Cleaning
      ↓
Scikit-learn Preprocessing Pipeline
      ↓
Random Forest Regressor
      ↓
Serialized Model Pipeline
      ↓
Service Layer
      ↓
Streamlit Dashboard
      ↓
Population-Level Prevalence Estimate
```

Users can configure a population profile and receive an estimated prevalence percentage through the dashboard.

---

## Key Features

- Population-level obesity prevalence estimation
- PySpark-based data ingestion and structural ETL
- Missing-value handling and feature preparation
- One-hot encoding for categorical variables
- Scikit-learn `ColumnTransformer` and pipeline-based preprocessing
- Random Forest regression
- Persisted preprocessing + model pipeline using Joblib
- Decoupled service layer for inference
- Custom Streamlit dashboard
- Population profile visualization
- ML pipeline visualization
- Input validation before inference

---

## Dataset

The project uses data derived from the **CDC Behavioral Risk Factor Surveillance System (BRFSS)**.

### Main data

- Raw file: `obesity.csv`
- Format: CSV
- Raw dataset size: approximately 42 MB
- Target: `Data_Value`
- Target meaning: percentage prevalence for the selected survey metric and population

### Important features

- Year
- Location / State
- Age
- Education
- Sex
- Income
- Race / Ethnicity
- Question / Survey Metric
- Data_Value

The dataset contains additional identifiers, metadata, confidence-limit fields, and survey-related columns that are removed during structural cleaning where appropriate.

---

## Data Processing

Initial structural processing is performed with **PySpark** in:

```text
spark/etl.py
```

The ETL workflow includes:

1. Loading the raw CSV into a Spark DataFrame
2. Inspecting schema and missing values
3. Profiling columns
4. Removing duplicate rows
5. Removing unused identifier and metadata columns
6. Exporting a cleaned structural baseline

The resulting data is then used by the Python/Scikit-learn ML workflow.

### Missing-value handling

The machine-learning preprocessing pipeline handles missing values using:

- **Median imputation** for numeric features
- **Most-frequent-value imputation** for categorical features

Categorical features are then transformed using:

```text
OneHotEncoder(handle_unknown="ignore")
```

No log transformation, scaling, or explicit outlier-removal pipeline is used in the final ML workflow.

---

## Machine Learning Pipeline

The prediction model is a:

**Random Forest Regressor**

### Training configuration

- Train/test split: **80/20**
- `n_estimators`: 100
- `random_state`: 42
- `n_jobs`: -1

The preprocessing and model are encapsulated inside a single Scikit-learn pipeline.

Conceptually:

```text
Input Features
      ↓
ColumnTransformer
      ├── Numeric → Imputation
      └── Categorical → Imputation → One-Hot Encoding
      ↓
Random Forest Regressor
      ↓
Predicted Prevalence
```

This approach ensures that training and inference use the same transformation logic and reduces the risk of inconsistent feature preparation.

---

## Model Performance

Evaluation was performed on the held-out 20% test set.

| Metric | Result |
|---|---:|
| R² | **0.87** |
| MAE | **2.50 percentage points** |
| RMSE | **3.70 percentage points** |

Because this is a **regression problem**, classification metrics such as accuracy, precision, recall, F1-score, and confusion matrices are not applicable.

---

## Application Architecture

The application separates the user interface, business logic, and machine-learning inference.

```text
                    Streamlit UI
                       app.py
                         │
                         ▼
                Service Layer
        ┌─────────────────────────────┐
        │ predictor_service.py        │
        │ data_service.py             │
        └─────────────────────────────┘
                         │
                         ▼
                 ML Inference
                    ml/predict.py
                         │
                         ▼
             Saved Pipeline (.pkl)
        ┌─────────────────────────────┐
        │ Imputation                  │
        │ One-Hot Encoding            │
        │ Random Forest Regressor     │
        └─────────────────────────────┘
                         │
                         ▼
             Prevalence Prediction
                         │
                         ▼
                  Streamlit UI
```

### Runtime flow

1. User selects population characteristics.
2. Streamlit validates the required inputs.
3. The service layer receives the selections.
4. Survey metadata is resolved through the data service.
5. Inputs are converted into a model-ready Pandas DataFrame.
6. The saved Scikit-learn pipeline performs preprocessing.
7. The Random Forest model generates the prevalence estimate.
8. The result is returned to the UI.
9. The dashboard displays the prediction and population profile.

---

## Dashboard

The Streamlit application provides:

### Analysis Parameters

Users can configure:

- Age Group
- Sex
- Race / Ethnicity
- Education
- Income
- State
- Year
- Question / Survey Metric

### Prediction & Analytics

The result area displays:

- Predicted obesity prevalence
- Visual percentage indicator
- Population Profile
- Selected demographic and socioeconomic characteristics
- ML Pipeline Overview

The interface is designed to make the ML workflow understandable without requiring the user to interact directly with Python code.

---

## Project Structure

```text
AI-Powered-Obesity-Risk-Analytics/
│
├── app.py
│
├── services/
│   ├── predictor_service.py
│   └── data_service.py
│
├── ml/
│   ├── train.py
│   └── predict.py
│
├── spark/
│   └── etl.py
│
├── models/
│   └── obesity_model.pkl
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── requirements.txt
└── README.md
```

---

## Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Core application and ML development |
| **PySpark** | Data ingestion and structural ETL |
| **Pandas** | Model-ready tabular data handling |
| **Scikit-learn** | Preprocessing and machine learning |
| **Random Forest** | Regression model |
| **Streamlit** | Interactive web application |
| **Joblib** | Model pipeline serialization |

---

## Engineering Highlights

### 1. End-to-end ML workflow

The project connects data ingestion, preprocessing, training, model persistence, inference, and visualization instead of treating model training as the final step.

### 2. Pipeline encapsulation

The preprocessing components and Random Forest estimator are stored together in a Scikit-learn pipeline.

This means inference uses the same transformation logic as training without manually reproducing feature mappings in the service layer.

### 3. Separation of concerns

The repository separates:

```text
ETL       → spark/
ML        → ml/
Services  → services/
UI        → app.py
Models    → models/
```

This makes the application easier to reason about and extend.

### 4. PySpark + Scikit-learn workflow

PySpark is used for initial structural data processing, while the reduced dataset is passed into the Pandas/Scikit-learn workflow for feature engineering and model training.

### 5. Product-oriented ML interface

The model is exposed through an interactive dashboard rather than requiring users to execute notebook cells or Python scripts manually.

---

## Limitations

This project is a portfolio/engineering implementation and has several limitations.

- Geographic state information is represented through categorical encoding and does not explicitly model spatial relationships.
- Year is handled as a feature rather than through a dedicated time-series approach.
- The Random Forest hyperparameters were not extensively tuned.
- Median/mode imputation is simple and may not capture complex missing-data patterns.
- The prediction represents population-level prevalence and should not be interpreted as an individual's medical risk.
- Model performance is dependent on the underlying survey data and selected features.

---

## Running the Application

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd AI-Powered-Obesity-Risk-Analytics
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Streamlit

```bash
streamlit run app.py
```

The application will open in your browser.

---

## Data & Model Files

Large raw datasets should not be committed directly to the repository.

If the raw BRFSS dataset is required for reproducing the ETL workflow, obtain it from the appropriate public CDC data source and place it in the expected project data directory.

The trained model pipeline is stored separately from the training code so the Streamlit application can perform inference without retraining the model on every launch.

---

## Future Improvements

Potential next steps include:

- Hyperparameter optimization
- More sophisticated missing-data strategies
- Temporal feature engineering
- Geographic/spatial feature engineering
- Model comparison with additional regression algorithms
- Explainability using feature importance or SHAP
- Automated model evaluation and retraining
- Containerized deployment
- Cloud deployment and CI/CD

---

## Disclaimer

This project is intended for **educational, portfolio, and machine-learning engineering purposes**.

It estimates aggregate population-level prevalence from survey data. It is **not a medical diagnostic system and should not be used to make individual healthcare decisions**.
