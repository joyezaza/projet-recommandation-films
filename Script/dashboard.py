import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import NearestNeighbors
import numpy as np
import os

# 🎨 Configuration du Dashboard
st.set_page_config(page_title="Dashboard Recommandation de Films", layout="wide")

# 📂 Chargement des données avec chemin relatif
DATA_PATH = os.path.join(os.path.dirname(__file__), "../Data-source/merged_final_data.csv")

# Vérifier si le fichier existe avant de le charger
if os.path.exists(DATA_PATH):
    df = pd.read_csv(DATA_PATH)
else:
    st.error(f"❌ Fichier introuvable : `{DATA_PATH}`. Vérifiez votre dépôt GitHub.")
    st.stop()

# 📌 **Barre de Navigation**
st.sidebar.title("🔍 Navigation")
page = st.sidebar.radio("📌 Choisissez une section :", [
    "🏠 Accueil & Objectifs",
    "📊 Présentation des Données",
    "🛠 Nettoyage des Données",
    "📈 Analyse Exploratoire",
    "🎬 Recommandations",
    "🚀 Performance des Modèles"
])

# 🏠 **1️⃣ Accueil & Objectifs**
if page == "🏠 Accueil & Objectifs":
    st.title("🎬 Dashboard - Système de Recommandation de Films")
    
    st.markdown("""
    ### 🔹 **Objectifs du Projet**
    Ce projet vise à **analyser** et **modéliser** un **système de recommandation de films** basé sur les notations des utilisateurs.  
    L'objectif est de fournir des **recommandations personnalisées** en fonction des préférences des utilisateurs.

    ### 🔍 **Données utilisées**
    - **MovieLens 100K** : **100 000 notations**, **943 utilisateurs**, **1 682 films**.

    ### 🔎 **Méthodes utilisées**
    - **Analyse Exploratoire** : Étudier les tendances des notes et des films.
    - **Modèles de Recommandation** : Filtrage **User-User KNN**, **Item-Item KNN**, et **Content-Based**.
    - **Comparaison des performances** des modèles via **le RMSE**.
    """)

# 📊 **2️⃣ Présentation des Données**
elif page == "📊 Présentation des Données":
    st.header("📊 Présentation des Données")

    with st.expander("📌 **Données Movies**"):
        st.write("**Nombre de lignes :** 1682 | **Nombre de colonnes :** 24")
        st.write("**Exemple de données :**")
        st.dataframe(df.head())

        st.write("""
        - **Genres les plus courants :**  
          - 🎭 Drama (725 films)  
          - 😂 Comedy (505 films)  
          - 🔥 Action / Thriller (251 films chacun)  
          - ❓ Genres rares : Fantasy (22 films), Western (27 films)
        - **Nombre de titres uniques :** 1664  
        - **Dates de sortie manquantes :** 1  
        """)

    with st.expander("📌 **Données Ratings**"):
        st.write("**Nombre total de lignes :** 100 000 | **Nombre de colonnes :** 4")
        st.write("""
        - **Notes aberrantes détectées :** 6 110  
        - **Nombre d’utilisateurs ayant donné plusieurs notes :** 99 057  
        - **Films ayant plusieurs notes :** 98 318  
        - **Valeurs manquantes :** 0  
        """)

# 🛠 **3️⃣ Nettoyage des Données**
elif page == "🛠 Nettoyage des Données":
    st.header("🛠 Nettoyage des Données")
    st.write("Nous avons appliqué plusieurs étapes de nettoyage avant d'exploiter les données.")

    with st.expander("📌 **Principales étapes du nettoyage**"):
        st.write("""
        1️⃣ **Suppression des valeurs manquantes**
        2️⃣ **Conversion des types de données (dates, entiers, etc.)**
        3️⃣ **Filtrage des notes aberrantes**
        4️⃣ **Fusion des fichiers movies.csv et ratings.csv**
        """)

    st.write("**Aperçu des données nettoyées :**")
    st.dataframe(df.head())

# 📈 **4️⃣ Analyse Exploratoire**
elif page == "📈 Analyse Exploratoire":
    st.header("📈 Analyse Exploratoire")

    tab1, tab2, tab3, tab4 = st.tabs(["🔢 Notes", "📅 Films par Année", "📌 Genres", "👤 Utilisateurs"])

    with tab1:
        st.subheader("📌 Distribution des Notes")
        fig, ax = plt.subplots(figsize=(8,5))
        sns.histplot(df["rating"], bins=5, kde=True, ax=ax, color="skyblue")
        plt.xlabel("Notes")
        plt.ylabel("Fréquence")
        st.pyplot(fig)

    with tab2:
        st.subheader("📌 Nombre de Films par Année")
        df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
        fig, ax = plt.subplots(figsize=(12,5))
        df["year"].value_counts().sort_index().plot(kind="bar", ax=ax, color="orange")
        st.pyplot(fig)

    with tab3:
        st.subheader("📌 Heatmap des Genres")
        genres = ['Action', 'Adventure', 'Drama', 'Comedy', 'Thriller']
        fig, ax = plt.subplots(figsize=(10,8))
        sns.heatmap(df[genres].corr(), annot=False, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    with tab4:
        st.subheader("📌 Nombre de Notes par Utilisateur")
        user_ratings = df["user_id"].value_counts()
        fig, ax = plt.subplots(figsize=(10,5))
        sns.histplot(user_ratings, bins=50, kde=True, ax=ax, color="purple")
        st.pyplot(fig)

# 🎬 **5️⃣ Recommandations**
elif page == "🎬 Recommandations":
    st.header("🎬 Recommandations Personnalisées")

    user_id = st.number_input("🔹 **Entrez un User ID** :", min_value=1, max_value=1000, step=1)

    if st.button("🎥 Obtenir des Recommandations"):
        user_item_matrix = df.pivot_table(index="user_id", columns="movie_title", values="rating", fill_value=0)
        knn = NearestNeighbors(n_neighbors=10, metric="manhattan", algorithm="ball_tree")
        knn.fit(user_item_matrix.T.values)

        def get_recommendations(user_id, user_item_matrix, knn, top_n=5):
            unrated_movies = user_item_matrix.columns[user_item_matrix.loc[user_id] == 0]
            predictions = {movie: np.mean(user_item_matrix.loc[user_id]) for movie in unrated_movies}
            return sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:top_n]

        recommendations = get_recommendations(user_id, user_item_matrix, knn)
        for movie, score in recommendations:
            st.write(f"🎬 {movie} (Score: {score:.2f})")

# 🚀 **6️⃣ Performance des Modèles**
elif page == "🚀 Performance des Modèles":
    st.header("🚀 Comparaison des Modèles de Recommandation")

    models = ["User-User KNN", "Item-Item KNN", "Content-Based", "Hybrid Content-User", "Hybrid Content-Item"]
    rmse_values = [1.112, 0.496, 1.266, 3.115, 2.370]  

    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x=models, y=rmse_values, ax=ax, palette="viridis")
    plt.xticks(rotation=15)
    st.pyplot(fig)
