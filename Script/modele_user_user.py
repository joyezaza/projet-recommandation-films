import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
import joblib

# Chargement et préparation des données
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')
user_item_matrix = data.pivot_table(index='user_id', columns='movie_title', values='rating', fill_value=0)

# Entraînement précis du modèle KNN User-User
model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10)
model_knn.fit(user_item_matrix.values)

# Sauvegarde claire du modèle entraîné
import joblib
import os

model_path = r'C:\projet_work\Data-source\user_user_knn_model.pkl'
pd.to_pickle(model_knn, model_path)

# ✅ Fonction de recommandation (corrigée et précise)
def recommander_films(user_id, matrice, model_knn, n_reco=5):
    user_index = matrice.index.get_loc(user_id)
    distances, indices = model_knn.kneighbors([matrice.iloc[user_index].values], n_neighbors=10)
    voisins = matrice.iloc[indices[0]]
    moyenne_voisins = voisins.mean(axis=0)
    
    deja_notes = matrice.iloc[user_index] > 0
    recommandations = moyenne_voisins[~deja_notes].sort_values(ascending=False).head(n_reco)
    return recommandations

# Exemple précis pour utilisateur ID=1
user_id = 1
recommandations = recommander_films(user_id, user_item_matrix, model_knn, n_reco=5)

print("\nModèle User-User KNN créé avec succès")
print(f"Recommandations finales pour l'utilisateur {user_id} :")
print(recommandations)
