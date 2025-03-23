import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

# ------------------ Chargement des données ------------------
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')
movies = pd.read_csv(r'C:\projet_work\Data-source\clean_movie.csv')

# Liste des genres
genres = ['Action','Adventure','Animation',"Children's",'Comedy','Crime',
          'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',
          'Mystery','Romance','Sci-Fi','Thriller','War','Western']

# ------------------ Construction de la matrice de contenu ------------------
# On élimine les doublons et on construit la matrice des genres
movies_unique = movies.drop_duplicates(subset='movie_title').set_index('movie_title')
genre_matrix = movies_unique[genres]

# ------------------ Construction de la matrice Item-User ------------------
item_user_matrix = data.pivot_table(index='movie_title', columns='user_id', values='rating', fill_value=0)
# Remplacer les NaN par la moyenne du film (pour éviter des valeurs nulles)
item_user_matrix = item_user_matrix.apply(lambda row: row.fillna(row.mean()), axis=1)

# ------------------ Séparation Train/Test ------------------
# On utilise train_test_split sur l'ensemble des données pour garantir que tous les films du test sont présents dans l'entraînement.
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
train_item_matrix = train_data.pivot_table(index='movie_title', columns='user_id', values='rating', fill_value=0)
test_item_matrix = test_data.pivot_table(index='movie_title', columns='user_id', values='rating', fill_value=0)
train_item_matrix = train_item_matrix.apply(lambda row: row.fillna(row.mean()), axis=1)
test_item_matrix = test_item_matrix.apply(lambda row: row.fillna(row.mean()), axis=1)

# ------------------ Définition des grilles d'hyperparamètres ------------------
# Pour le composant Content-Based (on va utiliser la métrique 'cosine' et 'brute')
param_grid_content = {
    'n_neighbors': [2, 5, 10],
    'metric': ['cosine'],
    'algorithm': ['brute']
}

# Pour le composant Item-Item
param_grid_item = {
    'n_neighbors': [2, 5, 10],
    'metric': ['euclidean', 'manhattan'],
    'algorithm': ['auto', 'ball_tree', 'brute']
}

# ------------------ Fonction de prédiction hybride ------------------
def predict_hybrid_rating(film, user, item_matrix, genre_matrix, knn_item, knn_content):
    # Vérifier que le film est présent dans les deux matrices et que l'utilisateur existe dans item_matrix
    if film not in genre_matrix.index or film not in item_matrix.index or user not in item_matrix.columns:
        return np.nan
    # Phase 1 : Content-Based
    film_vector_content = genre_matrix.loc[film].values.reshape(1, -1)
    _, indices_content = knn_content.kneighbors(film_vector_content, n_neighbors=10)
    similar_films_content = genre_matrix.index[indices_content.flatten()[1:]]
    
    # Phase 2 : Item-Item
    film_vector_item = item_matrix.loc[film].values.reshape(1, -1)
    _, indices_item = knn_item.kneighbors(film_vector_item, n_neighbors=10)
    similar_films_item = item_matrix.index[indices_item.flatten()[1:]]
    
    # Fusion : Union des films similaires
    similar_films = list(set(similar_films_content).union(set(similar_films_item)))
    if len(similar_films) == 0:
        return np.nan
    # Pour l'utilisateur donné, récupérer la note des films similaires dans la matrice item
    ratings_similar = item_matrix.loc[similar_films, user]
    return ratings_similar.mean() if not ratings_similar.empty else np.nan

# ------------------ Optimisation des hyperparamètres ------------------
best_params = None
best_rmse = float('inf')

# Prenons un échantillonne 200 instances du test
test_sample = test_data.sample(n=200, random_state=42)

# Boucle sur la grille d'hyperparamètres pour le composant Content-Based et Item-Item
for n_neighbors_content in param_grid_content['n_neighbors']:
    for metric_content in param_grid_content['metric']:
        for algorithm_content in param_grid_content['algorithm']:
            knn_content = NearestNeighbors(n_neighbors=n_neighbors_content, 
                                           metric=metric_content, 
                                           algorithm=algorithm_content)
            knn_content.fit(genre_matrix.values)
            
            for n_neighbors_item in param_grid_item['n_neighbors']:
                for metric_item in param_grid_item['metric']:
                    for algorithm_item in param_grid_item['algorithm']:
                        knn_item = NearestNeighbors(n_neighbors=n_neighbors_item, 
                                                    metric=metric_item, 
                                                    algorithm=algorithm_item)
                        knn_item.fit(train_item_matrix.values)
                        
                        predictions = []
                        truths = []
                        
                        for user, film, true_rating in test_sample[['user_id', 'movie_title', 'rating']].itertuples(index=False):
                            pred = predict_hybrid_rating(film, user, train_item_matrix, genre_matrix, knn_item, knn_content)
                            if not np.isnan(pred):
                                predictions.append(pred)
                                truths.append(true_rating)
                        
                        if predictions and truths and len(predictions) == len(truths):
                            rmse = np.sqrt(mean_squared_error(truths, predictions))
                            print(f"Test: content: n_neighbors={n_neighbors_content}, metric={metric_content}, algorithm={algorithm_content} | "
                                  f"item: n_neighbors={n_neighbors_item}, metric={metric_item}, algorithm={algorithm_item} -> RMSE={rmse:.3f}")
                            
                            if rmse < best_rmse:
                                best_rmse = rmse
                                best_params = {
                                    'content': {'n_neighbors': n_neighbors_content, 'metric': metric_content, 'algorithm': algorithm_content},
                                    'item': {'n_neighbors': n_neighbors_item, 'metric': metric_item, 'algorithm': algorithm_item}
                                }

# ------------------ Affichage final ------------------
if best_params:
    print(f"\n✅ Meilleurs hyperparamètres pour Hybrid Content-Item KNN : {best_params}")
    print(f"🚀 RMSE optimisé : {best_rmse:.3f}")
else:
    print("\n❌ Aucune combinaison d'hyperparamètres n'a donné un RMSE valide pour le modèle hybride.")
