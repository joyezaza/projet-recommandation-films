import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# Chargement des données
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')

# Split précis en train/test
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)

# Matrices item-user (train et test)
train_matrix = train_data.pivot_table(index='movie_title', columns='user_id', values='rating', fill_value=0)
test_matrix = test_data.pivot_table(index='movie_title', columns='user_id', values='rating', fill_value=0)

# Entrainement du modèle
model_knn_item = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10)
model_knn_item.fit(train_matrix.values)

# Fonction prédiction Item-Item
def predire_notes_item(film, user_id, train_matrix, model_knn):
    if film not in train_matrix.index or user_id not in train_matrix.columns:
        return np.nan
    
    film_index = train_matrix.index.get_loc(film)
    distances, indices = model_knn.kneighbors([train_matrix.iloc[film_index].values], n_neighbors=10)
    voisins = train_matrix.iloc[indices[0]]
    prediction = voisins[user_id][voisins[user_id] > 0].mean()
    
    return prediction if not np.isnan(prediction) else np.nan

# Évaluation RMSE précise
predictions, truths = [], []

for film, user_id in test_data[['movie_title', 'user_id']].itertuples(index=False):
    true_rating = test_matrix.loc[film, user_id]
    pred_rating = predire_notes_item(film, user_id, train_matrix, model_knn_item)

    if not np.isnan(pred_rating):
        predictions.append(pred_rating)
        truths.append(true_rating)

# Calcul précis RMSE
mse = mean_squared_error(truths, predictions)
rmse = np.sqrt(mse)

print(f"\n🚀 RMSE précis du modèle Item-Item KNN : {rmse:.3f}")
