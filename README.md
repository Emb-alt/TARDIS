# TARDIS — Prédiction des retards des trains SNCF

Modèle de régression qui prédit le **retard moyen à l'arrivée** (en minutes) d'un trajet SNCF à partir de ses caractéristiques. Le projet comprend un notebook d'entraînement et une application Streamlit pour utiliser le modèle.

## Aperçu

À partir d'un trajet (gare de départ, gare d'arrivée, année, mois), le modèle estime le retard moyen attendu. L'entraînement compare trois algorithmes scikit-learn, sélectionne le meilleur, et le sauvegarde dans un fichier `tardis_model.joblib` que l'application Streamlit charge pour faire des prédictions.

## Installation

Créer un environnement virtuel puis installer les dépendances :

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install scikit-learn pandas numpy matplotlib joblib jupyter streamlit
```

XGBoost est optionnel et n'est utilisé que comme challenger sur GPU :

```bash
pip install xgboost
```

## 1. Le notebook d'entraînement (`tardis_model.ipynb`)

### Données et cible

La cible prédite est `Average delay of all trains at arrival` (retard moyen à l'arrivée, en minutes). L'année 2020 est exclue de l'entraînement car le trafic réduit pendant la pandémie de COVID rend les retards non représentatifs.

### Features utilisées

Trois variables catégorielles : `Service`, `Departure station`, `Arrival station`.

Huit variables numériques : `Average journey time`, `Number of scheduled trains`, `Year`, `Month`, plus des mesures décrivant l'état du trafic au départ et à l'arrivée (`Average delay of late trains at departure`, `Average delay of all trains at departure`, `Number of trains delayed at arrival`, `Average delay of late trains at arrival`).

### Modèles comparés

Le notebook entraîne et compare trois modèles via un registre modulaire (`MODELS`), ce qui permet d'ajouter un nouvel algorithme simplement en ajoutant une entrée au dictionnaire :

| Modèle | Type |
|---|---|
| Ridge | Régression linéaire régularisée |
| RandomForest | Forêt d'arbres (bagging) |
| HistGradientBoosting | Boosting par histogrammes |

Chaque modèle est optimisé par `RandomizedSearchCV` avec une validation temporelle (`TimeSeriesSplit`), de sorte que la comparaison soit équitable. Une baseline (`DummyRegressor` qui prédit toujours la moyenne) sert de référence à battre.

Un challenger optionnel `XGBoost` sur GPU est testé si le boosting gagne : il ne remplace le modèle final que s'il obtient un meilleur score.

### Validation

Le découpage train/test est chronologique (80 % les plus anciens pour l'entraînement, 20 % les plus récents pour le test), afin de simuler une prédiction sur des mois non vus et d'éviter toute fuite du futur dans l'entraînement.

Les métriques rapportées sont le RMSE, le MAE et le R².

### Sauvegarde du modèle

La cellule de sauvegarde construit un dictionnaire `artifact` contenant le modèle entraîné, la liste des colonnes, les métriques, les hyperparamètres et surtout `route_profiles`. Ce dernier contient, pour chaque trajet, les moyennes historiques des features que l'utilisateur ne saisira pas (durée, nombre de trains, retards). Il est stocké dans le `.joblib` afin que l'application Streamlit n'ait pas besoin de recharger le CSV.

La sauvegarde est **manuelle** : on relance le notebook autant de fois qu'on veut, et on décommente la dernière ligne de la cellule pour écrire le fichier quand on est satisfait du résultat.

```python
# joblib.dump(artifact, MODEL_PATH)
# print(f'Sauvegardé dans {MODEL_PATH}')
```

### Lancer les notebooks

```bash
jupyter notebook tardis_model.ipynb
```

Puis exécuter toutes les cellules (Cell → Run All).

```bash
jupyter notebook tardis_eda.ipynb
```

Puis exécuter toutes les cellules (Cell → Run All).

### Lancer l'application

```bash
streamlit run tardis_dashboard.py
```

L'application s'ouvre dans le navigateur (par défaut `http://localhost:8501`). Le fichier `tardis_model.joblib` doit être présent dans le même dossier ; il faut donc avoir exécuté le notebook et sauvegardé le modèle au préalable.


## Notes

Le modèle s'appuie sur les caractéristiques de trafic du trajet (notamment les retards observés). Pour un mois futur, ces valeurs sont estimées à partir des moyennes historiques de la ligne ; le modèle fournit donc une estimation du retard typique d'un trajet à une période donnée, hors incidents exceptionnels (grèves, météo, pannes).
