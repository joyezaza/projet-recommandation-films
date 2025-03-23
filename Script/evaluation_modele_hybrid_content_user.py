import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import joblib

# 🔹 **Chargement des données**
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')
movies = pd.read_csv(r'C:\projet_work\Data-source\clean_movie.csv')

genres = ['Action','Adventure','Animation',"Children's",'Comedy','Crime',
          'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',
          'Mystery','Romance','Sci-Fi','Thriller','War','Western']

# 🔹 **Matrice des genres (Content-Based)**
movies_unique = movies.drop_duplicates(subset='movie_title').set_index('movie_title')
movie_genres_matrix = movies_unique[genres]

# 🔹 **Matrice utilisateur-film (User-User)**
user_item_matrix = data.pivot_table(index='user_id', columns='movie_title', values='rating', fill_value=0)

# 🔹 **Chargement des modèles sauvegardés**
model_knn_content = joblib.load(r'C:\projet_work\Model\hybrid_content_knn.pkl')
model_knn_user = joblib.load(r'C:\projet_work\Model\hybrid_user_knn.pkl')

# ✅ **Fonction d’évaluation**
def predire_notes_hybride(user_id, film, user_matrix, genre_matrix, model_knn_user, model_knn_content):
    if film not in genre_matrix.index or user_id not in user_matrix.index:
        return np.nan

    # 🔹 **Phase 1 : Films similaires (Content-Based)**
    film_vector = genre_matrix.loc[film].values.reshape(1, -1)
    _, indices_film = model_knn_content.kneighbors(film_vector, n_neighbors=10)
    films_similaires = genre_matrix.index[indices_film.flatten()[1:]]

    # 🔹 **Phase 2 : Utilisateurs similaires (User-User)**
    user_vector = user_matrix.loc[user_id].values.reshape(1, -1)
    _, indices_user = model_knn_user.kneighbors(user_vector, n_neighbors=10)
    users_similaires = user_matrix.index[indices_user.flatten()[1:]]

    # 🔹 **Fusion : Notes des utilisateurs similaires sur films similaires**
    notes_similaires = user_matrix.loc[users_similaires, films_similaires].mean()
    prediction = notes_similaires.mean() if not notes_similaires.empty else np.nan

    return prediction

# ✅ **Évaluation RMSE**
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

predictions, truths = [], []

for user_id, film, true_rating in test_data[['user_id', 'movie_title', 'rating']].itertuples(index=False):
    pred_rating = predire_notes_hybride(user_id, film, user_item_matrix, movie_genres_matrix, model_knn_user, model_knn_content)
    
    if not np.isnan(pred_rating):
        predictions.append(pred_rating)
        truths.append(true_rating)

# 🔹 **Calcul du RMSE**
rmse = np.sqrt(mean_squared_error(truths, predictions))
print(f"\n🚀 RMSE du modèle Hybrid Content-User KNN : {rmse:.3f}")
