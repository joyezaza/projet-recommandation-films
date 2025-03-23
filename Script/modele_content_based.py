import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import joblib

# Chargement des données
movies = pd.read_csv(r'C:\projet_work\Data-source\clean_movie.csv')

# Sélection des colonnes de genres uniquement
genres = ['Action','Adventure','Animation',"Children's",'Comedy','Crime',
          'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',
          'Mystery','Romance','Sci-Fi','Thriller','War','Western']

movie_genres_matrix = movies.set_index('movie_title')[genres]

# Entraînement du modèle KNN Content-Based (cosine)
model_knn_content = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10)
model_knn_content.fit(movie_genres_matrix.values)

# Sauvegarde du modèle
model_path = r'C:\projet_work\Model\content_based_knn_model.pkl'
joblib.dump(model_knn_content, model_path)

# Fonction de recommandation basée sur contenu (genres)
def recommander_films_par_genres(titre_film, matrice_genres, model_knn, n_reco=5):
    if titre_film not in matrice_genres.index:
        return "Film non trouvé."

    film_index = matrice_genres.index.get_loc(titre_film)
    distances, indices = model_knn.kneighbors([matrice_genres.iloc[film_index].values], n_neighbors=n_reco + 1)
    recommandations = matrice_genres.index[indices.flatten()[1:]]
    
    return recommandations

# Exemple d'utilisation pour le film "Star Wars (1977)"
titre_film = "Star Wars (1977)"
recommandations = recommander_films_par_genres(titre_film, movie_genres_matrix, model_knn_content, n_reco=5)

print("\nModèle Content_based_recommandation créé avec succès")
print(f"\n🎬 Films similaires recommandés à '{titre_film}' (Content-Based) :")
print(recommandations)
