import pandas as pd

# Chargement des fichiers nettoyés
movies = pd.read_csv(r'C:\projet_work\Data-source\movie_clean.csv')
ratings = pd.read_csv(r'C:\projet_work\Data-source\clean_rating.csv')

# Vérifier les movie_id dans ratings non présents dans movies
movies_in_ratings_not_in_movies = ratings[~ratings['movie_id'].isin(movies['movie_id'])]
nb_movies_absents_dans_movies = movies_in_ratings_not_in_movies['movie_id'].nunique()
print(f"Nombre de movie_id présents dans ratings mais absents dans movies : {nb_movies_absents_dans_movies}")

# Afficher ces movie_id sans correspondance dans movies
print("\nListe des movie_id présents dans ratings mais absents dans movies :")
print(movies_in_ratings_not_in_movies['movie_id'].unique())

# Vérifier les movie_id dans movies non présents dans ratings
movies_not_in_ratings = movies[~movies['movie_id'].isin(ratings['movie_id'])]
nb_movies_absents_dans_ratings = movies_not_in_ratings['movie_id'].nunique()
print(f"\nNombre de movie_id présents dans movies mais absents dans ratings : {nb_movies_absents_dans_ratings}")

# Afficher ces movie_id sans correspondance dans ratings
print("\nListe des movie_id présents dans movies mais absents dans ratings :")
print(movies_not_in_ratings['movie_id'].unique())
