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

# Matrice utilisateur-film (User-User)
user_item_matrix = data.pivot_table(index='user_id', columns='movie_title', values='rating', fill_value=0)

# Modèle Content-Based
model_knn_content = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10)
model_knn_content.fit(movie_genres_matrix.values)

# Modèle User-User
model_knn_user = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10)
model_knn_user.fit(user_item_matrix.values)

# Sauvegarde des modèles
joblib.dump(model_knn_content, r'C:\projet_work\Model\hybrid_content_knn.pkl')
joblib.dump(model_knn_user, r'C:\projet_work\Model\hybrid_user_knn.pkl')

# Fonction de recommandation hybride
def recommander_films_hybride(user_id, film, user_matrix, genre_matrix, model_knn_user, model_knn_content, n_reco=5):
    if film not in genre_matrix.index or user_id not in user_matrix.index:
        return "Utilisateur ou film non trouvé."

    # Phase 1 : Recommandation Content-Based (Films similaires)
    film_vector = genre_matrix.loc[film].values.reshape(1, -1)
    _, indices_film = model_knn_content.kneighbors(film_vector, n_neighbors=10)
    films_similaires = genre_matrix.index[indices_film.flatten()[1:]]

    # Phase 2 : Recommandation User-User (Utilisateurs similaires)
    user_vector = user_matrix.loc[user_id].values.reshape(1, -1)
    _, indices_user = model_knn_user.kneighbors(user_vector, n_neighbors=10)
    users_similaires = user_matrix.index[indices_user.flatten()[1:]]

    # Fusion des recommandations : Films similaires notés par utilisateurs similaires
    films_recommandes = user_matrix.loc[users_similaires][films_similaires].mean().sort_values(ascending=False).head(n_reco)

    return films_recommandes

#  Exemple de recommandation hybride
user_id = 1
titre_film = "Star Wars (1977)"
recommandations = recommander_films_hybride(user_id, titre_film, user_item_matrix, movie_genres_matrix, model_knn_user, model_knn_content)
print("\nModèle Hybrid-Content-user recommandation créé avec succès")
print(f"\n Films recommandés à l'utilisateur {user_id} en hybride avec '{titre_film}':")
print(recommandations)
