# TARDIS — SNCF Train Delay Prediction

A regression model that predicts the **average arrival delay** (in minutes) for an SNCF journey based on its characteristics. The project includes a training notebook and a Streamlit application to use the model.

## Overview

Given a journey (departure station, arrival station, year, month), the model estimates the expected average delay. Training compares three scikit-learn algorithms, selects the best one, and saves it to `tardis_model.joblib`, which the Streamlit app loads to make predictions.

## Installation

Create a virtual environment and install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install scikit-learn pandas numpy matplotlib joblib jupyter streamlit
```

XGBoost is optional and only used as a GPU challenger:

```bash
pip install xgboost
```

## 1. Training Notebook (`tardis_model.ipynb`)

### Data and Target

The predicted target is `Average delay of all trains at arrival` (in minutes). The year 2020 is excluded from training because reduced traffic during the COVID pandemic makes delays unrepresentative.

### Features Used

Three categorical variables: `Service`, `Departure station`, `Arrival station`.

Eight numerical variables: `Average journey time`, `Number of scheduled trains`, `Year`, `Month`, plus measurements describing traffic conditions at departure and arrival (`Average delay of late trains at departure`, `Average delay of all trains at departure`, `Number of trains delayed at arrival`, `Average delay of late trains at arrival`).

### Models Compared

The notebook trains and compares three models via a modular registry (`MODELS`), making it easy to add a new algorithm by simply adding an entry to the dictionary:

| Model | Type |
|---|---|
| Ridge | Regularized linear regression |
| RandomForest | Ensemble of trees (bagging) |
| HistGradientBoosting | Histogram-based boosting |

Each model is tuned with `RandomizedSearchCV` using time-series cross-validation (`TimeSeriesSplit`) for a fair comparison. A baseline (`DummyRegressor` always predicting the mean) serves as the reference to beat.

An optional `XGBoost` GPU challenger is tested if boosting wins: it only replaces the final model if it achieves a better score.

### Validation

The train/test split is chronological (oldest 80% for training, most recent 20% for testing) to simulate prediction on unseen months and prevent future data leakage.

Reported metrics are RMSE, MAE, and R².

### Saving the Model

The save cell builds an `artifact` dictionary containing the trained model, the list of columns, metrics, hyperparameters, and most importantly `route_profiles`. The latter holds, for each route, the historical averages of features the user will not enter (journey time, number of trains, delays). It is stored in the `.joblib` file so the Streamlit app does not need to reload the CSV.

Saving is **manual**: re-run the notebook as many times as needed, then uncomment the last line of the save cell to write the file when satisfied with the result.

```python
# joblib.dump(artifact, MODEL_PATH)
# print(f'Saved to {MODEL_PATH}')
```

### Running the Notebooks

```bash
jupyter notebook tardis_model.ipynb
```

Then run all cells (Cell → Run All).

```bash
jupyter notebook tardis_eda.ipynb
```

Then run all cells (Cell → Run All).

### Running the App

```bash
streamlit run tardis_dashboard.py
```

The app opens in the browser (default `http://localhost:8501`). The `tardis_model.joblib` file must be present in the same folder — you need to have run the notebook and saved the model beforehand.

## Notes

The model relies on traffic characteristics of the journey (notably observed delays). For a future month, these values are estimated from the historical averages of the route; the model therefore provides an estimate of the typical delay for a journey at a given period, excluding exceptional events (strikes, weather, breakdowns).
