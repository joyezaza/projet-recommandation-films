import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import joblib

# Chargement des données
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')
movies = pd.read_csv(r'C:\projet_work\Data-source\clean_movie.csv')

genres = ['Action','Adventure','Animation',"Children's",'Comedy','Crime',
          'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',
          'Mystery','Romance','Sci-Fi','Thriller','War','Western']

# Matrice des genres (Content-Based)
movies_unique = movies.drop_duplicates(subset='movie_title').set_index('movie_title')
movie_genres_matrix = movies_unique[genres]

# Matrice film-utilisateur (Item-Item)
item_user_matrix = data.pivot_table(index='movie_title', columns='user_id', values='rating', fill_value=0)

# Chargement des modèles sauvegardés
model_knn_content = joblib.load(r'C:\projet_work\Model\hybrid_content_knn.pkl')
model_knn_item = joblib.load(r'C:\projet_work\Model\hybrid_item_knn.pkl')

# Fonction d’évaluation
def predire_notes_hybride_item(film, user_id, item_matrix, genre_matrix, model_knn_item, model_knn_content):
    if film not in genre_matrix.index or film not in item_matrix.index or user_id not in item_matrix.columns:
        return np.nan

    # Phase 1 : Films similaires (Content-Based)
    film_vector = genre_matrix.loc[film].values.reshape(1, -1)
    _, indices_film_content = model_knn_content.kneighbors(film_vector, n_neighbors=10)
    films_similaires_content = genre_matrix.index[indices_film_content.flatten()[1:]]

    # Phase 2 : Films similaires (Item-Item)
    film_vector = item_matrix.loc[film].values.reshape(1, -1)
    _, indices_film_item = model_knn_item.kneighbors(film_vector, n_neighbors=10)
    films_similaires_item = item_matrix.index[indices_film_item.flatten()[1:]]

    # Fusion : Notes des films similaires sur Item-Item et Content-Based
    films_similaires = list(set(films_similaires_content).union(set(films_similaires_item)))
    notes_similaires = item_matrix.loc[films_similaires, user_id].dropna()
    
    prediction = notes_similaires.mean() if not notes_similaires.empty else np.nan
    return prediction

# Évaluation RMSE
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

predictions, truths = [], []

for film, user_id, true_rating in test_data[['movie_title', 'user_id', 'rating']].itertuples(index=False):
    pred_rating = predire_notes_hybride_item(film, user_id, item_user_matrix, movie_genres_matrix, model_knn_item, model_knn_content)
    
    if not np.isnan(pred_rating):
        predictions.append(pred_rating)
        truths.append(true_rating)

# Calcul du RMSE
rmse = np.sqrt(mean_squared_error(truths, predictions))
print(f"\n🚀 RMSE du modèle Hybrid Content-Item KNN : {rmse:.3f}")
