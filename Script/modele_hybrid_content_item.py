import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import joblib

# Chargement des données
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')
movies = pd.read_csv(r'C:\projet_work\Data-source\clean_movie.csv')

# Définition des genres
genres = ['Action','Adventure','Animation',"Children's",'Comedy','Crime',
          'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',
          'Mystery','Romance','Sci-Fi','Thriller','War','Western']

# Matrice des genres (Content-Based)
movies_unique = movies.drop_duplicates(subset='movie_title').set_index('movie_title')
movie_genres_matrix = movies_unique[genres]

# Matrice film-utilisateur (Item-Item)
item_user_matrix = data.pivot_table(index='movie_title', columns='user_id', values='rating', fill_value=0)

# Vérifier si `Star Wars (1977)` est bien dans les matrices
print(f"'Star Wars (1977)' dans Content-Based : {'Star Wars (1977)' in movie_genres_matrix.index}")
print(f"'Star Wars (1977)' dans Item-Item : {'Star Wars (1977)' in item_user_matrix.index}")

# Modèle Content-Based
model_knn_content = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10)
model_knn_content.fit(movie_genres_matrix.values)

# Modèle Item-Item
model_knn_item = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10)
model_knn_item.fit(item_user_matrix.values)

# Sauvegarde des modèles
joblib.dump(model_knn_content, r'C:\projet_work\Model\hybrid_content_knn.pkl')
joblib.dump(model_knn_item, r'C:\projet_work\Model\hybrid_item_knn.pkl')

# Fonction de recommandation hybride (Content + Item)
def recommander_films_hybride_item(film, item_matrix, genre_matrix, model_knn_item, model_knn_content, n_reco=5):
    if film not in genre_matrix.index or film not in item_matrix.index:
        return "Film non trouvé."

    # Phase 1 : Recommandation Content-Based (Films similaires en genre)
    film_vector = genre_matrix.loc[film].values.reshape(1, -1)
    _, indices_film_content = model_knn_content.kneighbors(film_vector, n_neighbors=10)
    films_similaires_content = genre_matrix.index[indices_film_content.flatten()[1:]]

    # Phase 2 : Recommandation Item-Item (Films similaires par notes des utilisateurs)
    film_vector = item_matrix.loc[film].values.reshape(1, -1)
    _, indices_film_item = model_knn_item.kneighbors(film_vector, n_neighbors=10)
    films_similaires_item = item_matrix.index[indices_film_item.flatten()[1:]]

    # Fusion améliorée des recommandations
    films_similaires_content = set(films_similaires_content)
    films_similaires_item = set(films_similaires_item)

    films_recommandes = list(films_similaires_content.union(films_similaires_item))[:n_reco]

    return films_recommandes if films_recommandes else ["Aucune recommandation trouvée."]

# Exemple de recommandation hybride
titre_film = "Star Wars (1977)"
recommandations = recommander_films_hybride_item(titre_film, item_user_matrix, movie_genres_matrix, model_knn_item, model_knn_content)

print("\nModèle Hybrid-Content-Item recommandation créé avec succès")
print(f"\n Films recommandés avec le modèle hybride Content-Item pour '{titre_film}':")
print(recommandations)
