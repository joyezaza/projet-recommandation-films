import pandas as pd

# Chargement initial des données nettoyées
movies = pd.read_csv(r'C:\projet_work\Data-source\movie_clean.csv')
ratings = pd.read_csv(r'C:\projet_work\Data-source\clean_rating.csv')

# --- Nettoyage ratings : suppression des movie_id sans correspondance ---
ratings_final = ratings[ratings['movie_id'].isin(movies['movie_id'])]
nb_lignes_supprimees_rating = ratings.shape[0] - ratings_final.shape[0]
print(f"Lignes supprimées de ratings (movie_id sans correspondance) : {nb_lignes_supprimees_rating}")

# --- Nettoyage movies : suppression des films sans notation ---
movies_final = movies[movies['movie_id'].isin(ratings_final['movie_id'])]
nb_films_supprimes_movie = movies.shape[0] - movies_final.shape[0]
print(f"Films supprimés dans movies (aucune notation associée) : {nb_films_supprimes_movie}\n")

# Vérification rapide des résultats finaux
print(f"Nombre final de lignes dans ratings : {ratings_final.shape[0]}")
print(f"Nombre final de films dans movies : {movies_final.shape[0]}\n")

# --- Fusion immédiate des deux fichiers nettoyés ---
merged_final_data = pd.merge(ratings_final, movies_final, on='movie_id', how='inner')

# Vérification rapide après fusion finale
print(f"Nombre total de lignes après fusion : {merged_final_data.shape[0]}\n")
print("Aperçu des 3 premières lignes fusionnées :")
print(merged_final_data.head(3))

# Sauvegarde définitive des fichiers nettoyés finaux et fusionnés
movies_final.to_csv(r'C:\projet_work\Data-source\clean_movie.csv', index=False)
ratings_final.to_csv(r'C:\projet_work\Data-source\clean_rating.csv', index=False)
merged_final_data.to_csv(r'C:\projet_work\Data-source\merged_final_data.csv', index=False)
