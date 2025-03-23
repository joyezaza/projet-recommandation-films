import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split, KFold

# Chargement des données
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')

# Création de la matrice film-utilisateur (Item-Item)
item_user_matrix = data.pivot_table(index='movie_title', columns='user_id', values='rating', fill_value=0)

# Remplacer les NaN par la moyenne du film pour éviter des zéros problématiques
item_user_matrix = item_user_matrix.apply(lambda row: row.fillna(row.mean()), axis=1)

# Définition de la grille d'hyperparamètres à tester
param_grid = {
    'n_neighbors': [2, 5, 10],
    'metric': ['cosine', 'euclidean', 'manhattan'],
    'algorithm': ['auto', 'ball_tree', 'brute']
}

# Initialisation des meilleurs paramètres
best_params = None
best_rmse = float('inf')

#  Séparation des données avec train_test_split pour garantir que tous les films du test sont dans train
train_data, test_data = train_test_split(data, test_size=0.2, random_state=42)
train_matrix = train_data.pivot_table(index='movie_title', columns='user_id', values='rating', fill_value=0)
test_matrix = test_data.pivot_table(index='movie_title', columns='user_id', values='rating', fill_value=0)

# Vérification des données avant optimisation
print("\n Vérification des données avant optimisation...\n")
print(f" Taille train_matrix : {train_matrix.shape}, test_matrix : {test_matrix.shape}")

films_test = set(test_matrix.index)
films_train = set(train_matrix.index)
films_communs = films_test.intersection(films_train)

print(f" Nombre total de films dans test_matrix : {len(films_test)}")
print(f" Nombre total de films dans train_matrix : {len(films_train)}")
print(f" Films en commun entre train et test : {len(films_communs)}")

if len(films_communs) == 0:
    print("\n❌ Aucun film du test_set n'est présent dans train_set !\n")

# Limiter les tests à un sous-ensemble de 200 films pour accélérer le traitement
test_matrix_sample = test_matrix.sample(n=200, random_state=42)
print(f" Films sélectionnés pour l'optimisation : {test_matrix_sample.shape[0]}")

# Boucle de validation croisée sur les hyperparamètres
for n_neighbors in param_grid['n_neighbors']:
    for metric in param_grid['metric']:
        for algorithm in param_grid['algorithm']:
            # Pour la métrique 'cosine', n'utiliser que 'brute'
            if metric == 'cosine' and algorithm != 'brute':
                continue

            knn = NearestNeighbors(n_neighbors=n_neighbors, metric=metric, algorithm=algorithm)
            print(f"\n Test de : n_neighbors={n_neighbors}, metric={metric}, algorithm={algorithm}")
            
            # Entraînement sur la matrice train
            knn.fit(train_matrix.values)

            predictions = []
            truths = []

            # Boucle sur l'échantillon réduit de test
            for movie, user in test_matrix_sample.stack().index:
                if movie in train_matrix.index and user in train_matrix.columns:
                    try:
                        distances, indices = knn.kneighbors(
                            [train_matrix.loc[movie].values],
                            n_neighbors=min(n_neighbors, len(train_matrix))
                        )
                        # Exclure le film courant (premier voisin)
                        films_similaires = train_matrix.index[indices.flatten()[1:]]
                        notes_moyennes = train_matrix.loc[films_similaires, user].mean()

                        if not np.isnan(notes_moyennes):
                            predictions.append(notes_moyennes)
                            truths.append(test_matrix.loc[movie, user])
                    except Exception as e:
                        continue

            # Calcul du RMSE pour cette configuration si possible
            if predictions and truths and len(predictions) == len(truths):
                current_rmse = np.sqrt(mean_squared_error(truths, predictions))
                print(f"RMSE pour cette configuration : {current_rmse:.3f}")
                if current_rmse < best_rmse:
                    best_rmse = current_rmse
                    best_params = {'n_neighbors': n_neighbors, 'metric': metric, 'algorithm': algorithm}

# Affichage final des meilleurs hyperparamètres et du RMSE optimisé
if best_params:
    print(f"\n Meilleurs hyperparamètres trouvés pour Item-Item KNN : {best_params}")
    print(f" RMSE optimisé : {best_rmse:.3f}")
else:
    print("\n❌ Aucune combinaison d'hyperparamètres n'a donné un RMSE valide.")
