import pandas as pd
import numpy as np

# Chargement du fichier rating.csv
ratings = pd.read_csv(r'C:\projet_work\Data-source\rating.csv')

# Suppression des lignes entièrement doublées
nb_doublons = ratings.duplicated().sum()
ratings_clean = ratings.drop_duplicates()
print(f"Nombre de lignes entièrement doublées supprimées : {nb_doublons}")

# Suppression de la colonne timestamp
ratings_clean = ratings_clean.drop(columns=['timestamp'])

# Suppression des films ayant moins de 3 notes
film_counts = ratings_clean['movie_id'].value_counts()
films_a_supprimer = film_counts[film_counts < 3].index
nb_films_supprimes = len(films_a_supprimer)
ratings_clean = ratings_clean[~ratings_clean['movie_id'].isin(films_a_supprimer)]
print(f"Nombre de films supprimés (moins de 3 notations) : {nb_films_supprimes}")

# Suppression des utilisateurs ayant noté moins de 3 films
user_counts = ratings_clean['user_id'].value_counts()
users_a_supprimer = user_counts[user_counts < 3].index
nb_users_supprimes = len(users_a_supprimer)
ratings_clean = ratings_clean[~ratings_clean['user_id'].isin(users_a_supprimer)]
print(f"Nombre d'utilisateurs supprimés (moins de 3 notes) : {nb_users_supprimes}")

# Suppression des utilisateurs ayant un nombre excessif de films notés (seuil 99e percentile)
user_counts_updated = ratings_clean['user_id'].value_counts()
seuil_99 = np.percentile(user_counts_updated, 99)
users_excessifs = user_counts_updated[user_counts_updated > seuil_99].index
nb_users_excessifs_supprimes = len(users_excessifs)
ratings_clean = ratings_clean[~ratings_clean['user_id'].isin(users_excessifs)]
print(f"Nombre d'utilisateurs supprimés (nombre excessif de notations, seuil 99e percentile) : {nb_users_excessifs_supprimes}")

# Suppression des utilisateurs ayant une variance des notes < 0.1
user_variances = ratings_clean.groupby('user_id')['rating'].var()
users_variance_faible = user_variances[user_variances < 0.1].index
nb_users_variance_supprimes = len(users_variance_faible)
ratings_clean = ratings_clean[~ratings_clean['user_id'].isin(users_variance_faible)]
print(f"Nombre d'utilisateurs supprimés (variance des notes < 0.1) : {nb_users_variance_supprimes}")

# Suppression des films ayant uniquement des notes à 5.0 ou 1.0
film_notes_unique = ratings_clean.groupby('movie_id')['rating'].nunique()
films_notes_uniques = film_notes_unique[film_notes_unique == 1].index

films_notes_uniques_extremes = []
for film_id in films_notes_uniques:
    note_unique = ratings_clean[ratings_clean['movie_id'] == film_id]['rating'].iloc[0]
    if note_unique in [1.0, 5.0]:
        films_notes_uniques_extremes.append(film_id)

nb_films_notes_extremes_supprimes = len(films_notes_uniques_extremes)
ratings_clean = ratings_clean[~ratings_clean['movie_id'].isin(films_notes_uniques_extremes)]
print(f"Nombre de films supprimés (uniquement notes à 1.0 ou 5.0) : {nb_films_notes_extremes_supprimes}")

# Création d'une colonne rating_normalized (normalisation Min-Max)
min_rating = ratings_clean['rating'].min()
max_rating = ratings_clean['rating'].max()
ratings_clean['rating_normalized'] = (ratings_clean['rating'] - min_rating) / (max_rating - min_rating)

# Résumé final après nettoyage
nb_lignes_finales = ratings_clean.shape[0]
print(f"\nNombre total de lignes restantes après nettoyage : {nb_lignes_finales}")

# Aperçu des 3 premières lignes finales après nettoyage
print("\nAperçu des 3 premières lignes après nettoyage :")
print(ratings_clean.head(3))

# Sauvegarde du fichier nettoyé
ratings_clean.to_csv(r'C:\projet_work\Data-source\clean_rating.csv', index=False)
