import streamlit as st
import sidebar

st.set_page_config(page_title="Delays Prediction", layout="wide")

sidebar.show()

st.title("A PROPOS")

st.markdown("""
## Projet de Data Science SNCF

TARDIS est un projet de Data Science développé autour des données historiques de retards ferroviaires de la SNCF.

---

### Objectif principal

Analyser les performances du réseau ferroviaire français afin de :

- Comprendre les causes des retards  
- Identifier des tendances dans le trafic  
- Prédire les perturbations futures grâce au Machine Learning  

---

### Approche

Le projet combine :
- Analyse de données
- Visualisation
- Modélisation prédictive

""")

st.markdown("""
# Technologies utilisées

## Data Science
- Python
- Pandas
- NumPy
- Scikit-Learn

## Visualisation
- Matplotlib
- Seaborn

## Web App
- Streamlit
""")
