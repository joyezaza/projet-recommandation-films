import pandas as pd

# Chargement du fichier rating.csv
ratings = pd.read_csv(r'C:\projet_work\Data-source\rating.csv')

# Aperçu des premières lignes
print("Aperçu des premières lignes :")
print(ratings.head(), "\n")

# Nombre total de lignes
nb_lignes = ratings.shape[0]
print(f"Nombre total de lignes : {nb_lignes}")

# Nombre de colonnes
nb_colonnes = ratings.shape[1]
print(f"Nombre de colonnes : {nb_colonnes}\n")

# Détection des notes aberrantes (outliers) dans 'rating'
Q1 = ratings['rating'].quantile(0.25)
Q3 = ratings['rating'].quantile(0.75)
IQR = Q3 - Q1
borne_inf = Q1 - 1.5 * IQR
borne_sup = Q3 + 1.5 * IQR
outliers = ratings[(ratings['rating'] < borne_inf) | (ratings['rating'] > borne_sup)]
nb_outliers = outliers.shape[0]
print(f"Nombre de notes aberrantes détectées (outliers) : {nb_outliers}\n")

# Valeurs manquantes par colonne
valeurs_manquantes = ratings.isna().sum()
print("Valeurs manquantes par colonne :")
print(valeurs_manquantes, "\n")

# Nombre total de valeurs manquantes
nb_total_manquantes = valeurs_manquantes.sum()
print(f"Nombre total de valeurs manquantes : {nb_total_manquantes}\n")

# Nombre d'entrées utilisateur (user_id) en double
nb_user_duplicates = ratings.duplicated(subset='user_id').sum()
print(f"Nombre d'entrées utilisateur (user_id) en double : {nb_user_duplicates}")

# Nombre d'entrées film (movie_id) en double
nb_movie_duplicates = ratings.duplicated(subset='movie_id').sum()
print(f"Nombre d'entrées film (movie_id) en double : {nb_movie_duplicates}")

# Nombre de lignes entièrement dupliquées
nb_total_duplicates = ratings.duplicated().sum()
print(f"Nombre de lignes entièrement dupliquées : {nb_total_duplicates}\n")

# Aperçu des entrées utilisateur en double
print("Aperçu des entrées utilisateur en double :")
print(ratings[ratings.duplicated(subset='user_id', keep=False)].sort_values('user_id').head(), "\n")

# Aperçu des entrées film en double
print("Aperçu des entrées film en double :")
print(ratings[ratings.duplicated(subset='movie_id', keep=False)].sort_values('movie_id').head())
