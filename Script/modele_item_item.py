import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Chargement des données
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')

# Matrice item-user (transpose user-item pour item-item)
item_user_matrix = data.pivot_table(index='movie_title', columns='user_id', values='rating', fill_value=0)

# Entraînement précis du modèle KNN Item-Item (cosine)
model_knn_item = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=10)
model_knn_item.fit(item_user_matrix.values)

# Sauvegarde claire du modèle Item-Item
import joblib
model_path = r'C:\projet_work\Model\item_item_knn_model.pkl'
joblib.dump(model_knn_item, model_path)

# ✅ Fonction de recommandation Item-Item
def recommander_films_similaires(titre_film, matrice, model_knn, n_reco=5):
    if titre_film not in matrice.index:
        return "Film non trouvé."

    film_index = matrice.index.get_loc(titre_film)
    distances, indices = model_knn.kneighbors([matrice.iloc[film_index].values], n_neighbors=n_reco + 1)

    recommandations = matrice.index[indices.flatten()[1:]]  # exclure le film recherché
    return recommandations

# Exemple précis d'utilisation pour le film "Star Wars (1977)"
titre_film = "Star Wars (1977)"
recommandations = recommander_films_similaires(titre_film, item_user_matrix, model_knn_item, n_reco=5)

print("\nModèle Item-Item KNN créé avec succès")
print(f"\n🎬 Films similaires recommandés pour '{titre_film}':")
print(recommandations)
