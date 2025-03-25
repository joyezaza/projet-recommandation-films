import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neighbors import NearestNeighbors
import numpy as np

# 🎨 Configuration du Dashboard
st.set_page_config(page_title="Dashboard Recommandation de Films", layout="wide")

# 📂 Chargement des données
DATA_PATH = "C:/projet_work/Data-source/merged_final_data.csv"
df = pd.read_csv(DATA_PATH)

# 📌1️⃣ Introduction & Objectifs
st.title("🎬 Dashboard - Système de Recommandation de Films")
st.markdown("""
### 🔹 **Objectifs du Projet**
Ce projet vise à **analyser** et **modéliser** un **système de recommandation de films** basé sur les notations des utilisateurs.  
L'objectif est de fournir des **recommandations personnalisées** en fonction des préférences des utilisateurs.

### 🔍 **Données utilisées**
Nous exploitons le dataset **MovieLens 100K**, contenant **100 000 notations** de **943 utilisateurs** sur **1 682 films**.

### 🔎 **Méthodes utilisées**
- **Analyse Exploratoire** : Étudier les tendances des notes et des films.
- **Modèles de Recommandation** : Filtrage **User-User KNN**, **Item-Item KNN**, et **Content-Based**.
- **Comparaison des performances** des modèles via **le RMSE**.
""")

# 📊 Navigation Sidebar
st.sidebar.title("🔍 Navigation")
section = st.sidebar.radio("📌 Choisissez une section :", ["📊 Analyse Exploratoire", "🎬 Recommandations", "📈 Performance des Modèles"])

# 📊 2️⃣ Analyse Exploratoire
if section == "📊 Analyse Exploratoire":
    st.header("📊 Analyse Exploratoire des Données")

    # 📂 **Descriptif des Données**
    with st.expander("📌 **Descriptif des Données**"):
        st.write("**Aperçu des données :**")
        st.dataframe(df.head(5))

        st.write("**Informations sur les colonnes :**")
        st.text(df.info())

        st.write("**Valeurs manquantes par colonne :**")
        st.write(df.isnull().sum())

    # 📊 **Visualisation des Données**
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔢 Distribution des Notes", 
        "📅 Films par Année", 
        "📌 Genres & Tendances",
        "👤 Activité des Utilisateurs"
    ])

    with tab1:
        st.subheader("📌 Distribution des Notes")
        fig, ax = plt.subplots(figsize=(8,5))
        sns.histplot(df["rating"], bins=5, kde=True, ax=ax, color="skyblue")
        plt.xlabel("Notes")
        plt.ylabel("Fréquence")
        st.pyplot(fig)

    with tab2:
        st.subheader("📌 Nombre de Films par Année")
        df["release_date"] = pd.to_datetime(df["release_date"], errors="coerce")
        df["year"] = df["release_date"].dt.year
        fig, ax = plt.subplots(figsize=(12,5))
        df["year"].value_counts().sort_index().plot(kind="bar", ax=ax, color="orange")
        plt.xlabel("Année")
        plt.ylabel("Nombre de Films")
        st.pyplot(fig)

    with tab3:
        st.subheader("📌 Heatmap des Corrélations entre Genres")
        genres = ['Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime',
                  'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
                  'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
        fig, ax = plt.subplots(figsize=(10,8))
        sns.heatmap(df[genres].corr(), annot=False, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    with tab4:
        st.subheader("📌 Nombre de Notes par Utilisateur")
        user_ratings = df["user_id"].value_counts()
        fig, ax = plt.subplots(figsize=(10,5))
        sns.histplot(user_ratings, bins=50, kde=True, ax=ax, color="purple")
        plt.xlabel("Nombre de Films Notés")
        plt.ylabel("Nombre d'Utilisateurs")
        st.pyplot(fig)

# 🎬 3️⃣ Recommandations Interactives
elif section == "🎬 Recommandations":
    st.header("🎬 Recommandations Personnalisées")

    user_id = st.number_input("🔹 **Entrez un User ID** :", min_value=1, max_value=1000, step=1)

    if st.button("🎥 Obtenir des Recommandations"):
        user_item_matrix = df.pivot_table(index="user_id", columns="movie_title", values="rating", fill_value=0)

        # Modèle Item-Item KNN
        knn = NearestNeighbors(n_neighbors=10, metric="manhattan", algorithm="ball_tree")
        knn.fit(user_item_matrix.T.values)

        # Fonction pour recommandations
        def get_recommendations(user_id, user_item_matrix, knn, top_n=5):
            unrated_movies = user_item_matrix.columns[user_item_matrix.loc[user_id] == 0]
            predictions = {}
            for movie in unrated_movies:
                pred = np.mean(user_item_matrix.loc[user_id])
                predictions[movie] = pred
            return sorted(predictions.items(), key=lambda x: x[1], reverse=True)[:top_n]

        recommendations = get_recommendations(user_id, user_item_matrix, knn)
        st.subheader(f"🎥 **Films Recommandés pour l'Utilisateur {user_id}** :")
        for movie, score in recommendations:
            st.write(f"🎬 {movie} (Score: {score:.2f})")

# 📈 4️⃣ Performance des Modèles
elif section == "📈 Performance des Modèles":
    st.header("📈 Comparaison des Modèles de Recommandation")

    # Comparaison des RMSE
    models = ["User-User KNN", "Item-Item KNN", "Content-Based", "Hybrid Content-User", "Hybrid Content-Item"]
    rmse_values = [1.112, 0.496, 1.266, 3.115, 2.370]  

    fig, ax = plt.subplots(figsize=(8,5))
    sns.barplot(x=models, y=rmse_values, ax=ax, palette="viridis")
    plt.xlabel("Modèles")
    plt.ylabel("RMSE (Erreur Moyenne)")
    plt.xticks(rotation=15)
    st.pyplot(fig)

    st.markdown("""
    📌 **Analyse des résultats :**
    - ✅ **Item-Item KNN est le plus performant** avec un **RMSE de 0.496**.
    - 📉 **Le modèle hybride Content-User est le moins performant** (RMSE = 3.115).
    - 🎯 **Les approches collaboratives donnent de meilleurs résultats** que le filtrage basé uniquement sur le contenu.
    """)
