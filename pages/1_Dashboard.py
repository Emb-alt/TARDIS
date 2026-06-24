import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sidebar

st.set_page_config(
    page_title="Tableau de bord",
    page_icon="📊",
    layout="wide",
)

sidebar.show()

df = pd.read_csv(
    "cleaned_dataset.csv",
    sep=";",
    engine="python",
    encoding="utf-8",
    encoding_errors="replace",
)

st.title("TABLEAU DE BORD")

departure_stations = sorted(df["Departure station"].unique())

departure = st.selectbox("Gare de départ :", departure_stations)

filtered_arrivals = sorted(
    df[df["Departure station"] == departure]["Arrival station"].unique()
)

arrival = st.selectbox("Gare d'arrivée :", filtered_arrivals)

filtered_df = df[
    (df["Departure station"] == departure)
    & (df["Arrival station"] == arrival)
]

mean_by_year = filtered_df.groupby("Year")["Number of scheduled trains"].mean()

mean_by_year_delay = filtered_df.groupby("Year")[
    "Average delay of late trains at departure"
].mean()

if st.button("Générer les graphiques", width="stretch"):

    years = mean_by_year.index
    values = mean_by_year.values

    plt.style.use("_mpl-gallery")

    # ===== Graphique barres =====
    fig, ax = plt.subplots(figsize=(8, 5))

    bars = ax.bar(years, values, edgecolor="white")

    for bar in bars:
        height = bar.get_height()

        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 2,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=10,
        )

    ax.set(
        xlim=(2017.5, 2025.5),
        xticks=np.arange(2018, 2026),
        ylim=(0, max(values) + 30),
        yticks=np.linspace(0, max(values), 9),
    )

    ax.set_xlabel("Années")
    ax.set_ylabel("Nombre de trains")
    ax.set_title("Nombre de trains programmés par année")

    # ===== Graphique ligne =====
    fig1, ax1 = plt.subplots(figsize=(8, 5))

    sns.lineplot(
        x=mean_by_year_delay.index,
        y=mean_by_year_delay.values,
        marker="o",
        color="black",
        ax=ax1,
    )

    ax1.set_xlabel("Années")
    ax1.set_ylabel("Retard moyen au départ (minutes)")
    ax1.set_title("Retard moyen des trains au départ")

    st.pyplot(fig)
    st.pyplot(fig1)