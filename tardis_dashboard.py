import streamlit as st
import pandas as pd
import sidebar
from matplotlib import pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Home", page_icon="🚂", layout="wide")

df = pd.read_csv(
    "cleaned_dataset.csv", sep=";", encoding="utf-8", encoding_errors="replace"
)

start_year, end_year = sidebar.show(show_slider=True)

filtered_df = df[(df["Year"] <= end_year) & (df["Year"] >= start_year)]

total_trains = int(filtered_df["Number of scheduled trains"].sum())
total_cancelled = int(filtered_df["Number of cancelled trains"].sum())
avg_delay = round(filtered_df["Average delay of late trains at arrival"].mean(), 1)
pct_punctual = round(
    100
    - (
        filtered_df["Number of trains delayed at arrival"].sum()
        / filtered_df["Number of scheduled trains"].sum()
        * 100
    ),
    1,
)
total_lines = (
    filtered_df[["Departure station", "Arrival station"]].drop_duplicates().shape[0]
)

st.title("Train Analysis & Retard Detection Intelligence System™")
st.caption("Projet fait par Antoine B. Eric M. & Emir B.")

st.divider()

st.subheader("À propos")
st.markdown(f"""
TARDIS est une plateforme analytique développée pour l'étude des retards des trains grandes lignes en France, à partir des données ouvertes publiées par **SNCF Voyageurs**.
 
Le périmètre couvre **{start_year}-{end_year}**, soit **{f"{total_trains:,}".replace(",", " ")} trains programmés** sur **{total_lines} liaisons** entre **{df["Departure station"].nunique()} gares** françaises.
 
La plateforme propose des outils d'exploration interactive, d'analyse statistique et de prédiction par intelligence artificielle pour anticiper les perturbations.
""")

st.divider()

st.subheader("Quelques chiffres clés")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Trains programmés",
    f"{total_trains:,}".replace(",", " "),
    help=f"Sur la période {start_year}-{end_year}",
)
col2.metric(
    "Trains annulés",
    f"{total_cancelled:,}".replace(",", " "),
    delta=f"{round(total_cancelled / total_trains * 100, 1)} % du total",
    delta_color="inverse",
)
col3.metric(
    "Retard moyen",
    f"{avg_delay} min",
    help="Retard moyen des trains en retard à l'arrivée",
)
col4.metric(
    "Taux de ponctualité", f"{pct_punctual} %", help="Trains arrivés sans retard"
)
col5.metric("Lignes couvertes", total_lines, help="Paires départ/arrivée uniques")

st.markdown(
    "<p style='text-align:center; color:#94a3b8; font-size:0.875rem;'>Pour plus de précisions, dirigez vous vers le <a href='/Dashboard' target='_self'>Dashboard</a>.</p>",
    unsafe_allow_html=True,
)

st.divider()

if "tab" not in st.session_state:
    st.session_state.tab = "Services"

row1 = st.columns(2)
row2 = st.columns(2)

with row1[0]:
    if st.button("Services", use_container_width=True):
        st.session_state.tab = "Services"

with row1[1]:
    if st.button("Retards", use_container_width=True):
        st.session_state.tab = "Retards"

with row2[0]:
    if st.button("Évolution annuelle", use_container_width=True):
        st.session_state.tab = "Évolution annuelle"

with row2[1]:
    if st.button("Top 15 gares", use_container_width=True):
        st.session_state.tab = "Top 15 gares"

if st.session_state.tab == "Services":
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    x = (
        filtered_df["Service"].isin(["National"]).sum(),
        filtered_df["Service"].isin(["International"]).sum(),
    )
    y = ["Trains Nationaux", "Trains Internationaux"]
    ax1.pie(x, labels=y, colors=["yellow", "black"])
    ax1.set_title("Répartition des trains")
    st.pyplot(fig1)

elif st.session_state.tab == "Retards":
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    x = (
        filtered_df["Pct delay due to external causes"].mean(),
        filtered_df["Pct delay due to infrastructure"].mean(),
        filtered_df["Pct delay due to traffic management"].mean(),
        filtered_df["Pct delay due to rolling stock"].mean(),
        filtered_df["Pct delay due to station management and equipment reuse"].mean(),
        filtered_df[
            "Pct delay due to passenger handling (crowding, disabled persons, connections)"
        ].mean(),
    )
    labels = [
        "Causes externes",
        "Infrastructure",
        "Gestion du trafic",
        "Matériel roulant",
        "Gestion des gares",
        "Passagers",
    ]
    colors = ["#3B82F6", "#10B981", "#F59E0B", "#8B5CF6", "#06B6D4", "#EC4899"]
    ax2.pie(
        x, labels=labels, colors=colors, autopct="%1.1f%%", textprops={"fontsize": 9}
    )
    ax2.set_title("Causes des retards")
    st.pyplot(fig2)

elif st.session_state.tab == "Évolution annuelle":
    fig3, ax3 = plt.subplots(figsize=(10, 4))
    y1 = df.groupby("Year")["Number of scheduled trains"].sum()
    y2 = df.groupby("Year")["Number of cancelled trains"].sum()
    result = y1 - y2
    ax3.bar(result.index, result.values, color="black", width=0.6)
    ax3.set_title("Nombre de trains par année")
    ax3.set_xlabel("Année")
    ax3.set_ylabel("Nombre de trains")
    st.pyplot(fig3)

elif st.session_state.tab == "Top 15 gares":
    trains_by_station = (
        filtered_df.groupby("Departure station")["Number of scheduled trains"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
    )
    fig5, ax5 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=trains_by_station.values, y=trains_by_station.index, ax=ax5)
    for i, value in enumerate(trains_by_station.values):
        ax5.text(value + 1, i, f"{int(value)}", va="center", fontsize=10)
    ax5.set_xlabel("Nombre de trains programmés")
    ax5.set_ylabel("Stations")
    ax5.set_title("Top 15 des stations")
    st.pyplot(fig5)

st.divider()

st.markdown(
    """
<style>
.footer {
    background-color: #2F2F2F !important;
    color: white !important;
    padding: 40px 20px;
    margin-top: 50px;
    font-size: 14px;
    border-radius: 8px;
}
.footer-container {
    display: flex;
    flex-wrap: wrap;
    gap: 40px;
    max-width: 1100px;
    margin: auto;
    justify-content: space-between;
}
.footer-column {
    min-width: 200px;
    flex: 1;
}
.footer-column h4 {
    font-size: 15px;
    margin-bottom: 12px;
    font-weight: 700;
    color: white !important;
}
.footer-column p, .footer-column a {
    margin: 6px 0;
    color: #d1d5db !important;
    cursor: pointer;
    text-decoration: none;
    display: block;
}
.footer-column p:hover, .footer-column a:hover {
    text-decoration: underline;
    color: white !important;
}
.footer-bottom {
    border-top: 1px solid #555;
    margin-top: 30px;
    padding-top: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 12px;
}
.footer-small {
    color: #9ca3af !important;
    font-size: 12px;
}
.footer-logos {
    display: flex;
    gap: 15px;
    align-items: center;
}
</style>

<div class="footer">
    <div class="footer-container">
        <div class="footer-column">
            <h4>BESOIN D'AIDE</h4>
            <p>Questions fréquentes</p>
            <p>Faire une réclamation ↗</p>
            <p>Par téléphone au 3635</p>
            <p class="footer-small">Tous les jours de 8h00 à 20h00</p>
        </div>
        <div class="footer-column">
            <h4>INFORMATIONS LÉGALES</h4>
            <p>Conditions générales</p>
            <p>Cookies</p>
            <p>Mentions légales</p>
            <p>Plan du site</p>
        </div>
    </div>
</div>
""",
    unsafe_allow_html=True,
)
