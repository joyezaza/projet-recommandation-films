import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Chargement des données
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')
movies = pd.read_csv(r'C:\projet_work\Data-source\clean_movie.csv')

genres = ['Action','Adventure','Animation',"Children's",'Comedy','Crime',
          'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',
          'Mystery','Romance','Sci-Fi','Thriller','War','Western']

# Suppression des doublons avant création de la matrice genre
movies_unique = movies.drop_duplicates(subset='movie_title').set_index('movie_title')

# Matrice genre sans doublons
movie_genres_matrix = movies_unique[genres]

# Entraînement du modèle KNN Content-Based
model_knn_content = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10)
model_knn_content.fit(movie_genres_matrix.values)

# Split train/test
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

#  Fonction
def predire_notes_content(user_id, film, train_data, genres_matrix, model_knn):
    films_notes_user = train_data[train_data['user_id'] == user_id].groupby('movie_title')['rating'].mean()

    if film not in genres_matrix.index:
        return np.nan

    film_vector = genres_matrix.loc[film].values.reshape(1, -1)
    distances, indices = model_knn.kneighbors(film_vector, n_neighbors=10)
    films_similaires = genres_matrix.index[indices.flatten()[1:]]

    notes_similaires = films_notes_user[films_notes_user.index.isin(films_similaires)]
    
    pred_rating = notes_similaires.mean() if not notes_similaires.empty else np.nan
    return pred_rating

#  Évaluation avec RMSE
predictions, truths = [], []

for user_id, film, true_rating in test_data[['user_id', 'movie_title', 'rating']].itertuples(index=False):
    pred_rating = predire_notes_content(user_id, film, train_data, movie_genres_matrix, model_knn_content)
    if not np.isnan(pred_rating):
        predictions.append(pred_rating)
        truths.append(true_rating)

# Calcul du RMSE
rmse = np.sqrt(mean_squared_error(truths, predictions))

print(f"\n RMSE du modèle Content-Based KNN : {rmse:.3f}")
