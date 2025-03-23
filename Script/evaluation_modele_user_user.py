import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Chargement des données
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')

# Création matrice user-item
user_item_matrix = data.pivot_table(index='user_id', columns='movie_title', values='rating', fill_value=0)

# Split précis en train/test
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Matrices train/test
train_matrix = train_data.pivot_table(index='user_id', columns='movie_title', values='rating', fill_value=0)
test_matrix = test_data.pivot_table(index='user_id', columns='movie_title', values='rating', fill_value=0)

# Modèle KNN entraîné précisément
model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10)
model_knn.fit(train_matrix.values)

# Fonction prédiction corrigée
def predire_notes(user_id, film, train_matrix, model_knn):
    if user_id not in train_matrix.index or film not in train_matrix.columns:
        return np.nan
    user_index = train_matrix.index.get_loc(user_id)
    distances, indices = model_knn.kneighbors([train_matrix.iloc[user_index].values], n_neighbors=10)
    voisins = train_matrix.iloc[indices[0]]
    prediction = voisins[film][voisins[film] > 0].mean()
    return prediction if not np.isnan(prediction) else np.nan

# Évaluation RMSE corrigée précisément
predictions = []
truths = []

for user_id, film in test_data[['user_id', 'movie_title']].itertuples(index=False):
    true_rating = test_matrix.loc[user_id, film]
    pred_rating = predire_notes(user_id, film, train_matrix, model_knn)
    
    if not np.isnan(pred_rating):
        predictions.append(pred_rating)
        truths.append(true_rating)

# Calcul final du RMSE
mse = mean_squared_error(truths, predictions)
rmse = np.sqrt(mse)

print(f"\n🚀 RMSE précis du modèle User-User KNN : {rmse:.3f}")
