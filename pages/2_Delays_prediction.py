import streamlit as st
import pandas as pd
import joblib
import sidebar
from pathlib import Path

st.set_page_config(
    page_title="Delays Prediction",
    page_icon="🖥️",
    layout="wide",
)

df = pd.read_csv(
    "cleaned_dataset.csv",
    sep=";",
    engine="python",
    encoding="utf-8",
    encoding_errors="replace",
)

MODEL_PATH = "model.joblib"

sidebar.show()

if not Path(MODEL_PATH).exists():
    st.error("Modèle introuvable")
    st.stop()

artifact = joblib.load(MODEL_PATH)
model = artifact["model"]
profiles = artifact["route_profiles"]


st.title("PREDICTEUR DE RETARDS")

departure_stations = sorted(df["Departure station"].unique())

st.subheader("Trajet")
col_dep, col_arr = st.columns(2)
with col_dep:
    departure = st.selectbox("Gare de départ", departure_stations)

filtered_arrivals = sorted(
    df[df["Departure station"] == departure]["Arrival station"].unique()
)

with col_arr:
    arrival = st.selectbox("Gare d'arrivée", filtered_arrivals)

st.subheader("Période")
col1, col2 = st.columns(2)
with col1:
    year = st.number_input("Année", min_value=2018, max_value=2035, value=2026, step=1)
with col2:
    mois_fr = [
        "Janvier",
        "Février",
        "Mars",
        "Avril",
        "Mai",
        "Juin",
        "Juillet",
        "Août",
        "Septembre",
        "Octobre",
        "Novembre",
        "Décembre",
    ]
    mois_label = st.selectbox("Mois", mois_fr)
    month = mois_fr.index(mois_label) + 1

if st.button("Prédire le retard", type="primary", use_container_width=True):
    row = profiles[
        (profiles["Departure station"] == departure)
        & (profiles["Arrival station"] == arrival)
    ]

    if row.empty:
        st.warning("Ce trajet n'existe pas dans les données.")
    else:
        row = row.iloc[0]
        sample = pd.DataFrame(
            [
                {
                    "Service": row["Service"],
                    "Departure station": departure,
                    "Arrival station": arrival,
                    "Average journey time": row["Average journey time"],
                    "Number of scheduled trains": row["Number of scheduled trains"],
                    "Year": int(year),
                    "Month": int(month),
                    "Average delay of late trains at departure": row[
                        "Average delay of late trains at departure"
                    ],
                    "Average delay of all trains at departure": row[
                        "Average delay of all trains at departure"
                    ],
                    "Number of trains delayed at arrival": row[
                        "Number of trains delayed at arrival"
                    ],
                    "Average delay of late trains at arrival": row[
                        "Average delay of late trains at arrival"
                    ],
                }
            ]
        )[artifact["cat_cols"] + artifact["num_cols"]]

        if artifact["model_name"] == "xgboost_gpu":
            for c in artifact["cat_cols"]:
                sample[c] = sample[c].astype("category")

        pred = float(model.predict(sample)[0])
        minutes = int(pred)
        seconds = int(round((pred - minutes) * 60))
        if seconds == 60:
            minutes += 1
            seconds = 0

        st.metric(
            label=f"{departure} → {arrival} ({mois_label} {year})",
            value=f"{minutes} min {seconds:02d} s",
        )
        st.caption(
            "Estimation basée sur le profil historique de la ligne. Hors incidents exceptionnels."
        )
