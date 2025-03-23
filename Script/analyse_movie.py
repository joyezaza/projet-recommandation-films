import pandas as pd

# Chargement du fichier movie.csv
movies = pd.read_csv(r'C:\projet_work\Data-source\movie.csv')

# Nombre de lignes et de colonnes
nb_lignes, nb_colonnes = movies.shape
print(f"Nombre de lignes : {nb_lignes}")
print(f"Nombre de colonnes : {nb_colonnes}\n")

# Types des colonnes
print("Types des colonnes :")
print(movies.dtypes, "\n")

# Nombre de titres uniques
nb_titres_uniques = movies['movie_title'].nunique()
print(f"Nombre de titres uniques : {nb_titres_uniques}\n")

# Nombre de films par genre (y compris 'unknown')
genres = ['unknown', 'Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime',
          'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
          'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']

print("Nombre de films par genre :")
for genre in genres:
    nombre_genre = movies[genre].sum()
    print(f"{genre:<12} : {nombre_genre}")

# Dates de sortie manquantes
nb_dates_sortie_manquantes = movies['release_date'].isna().sum()
print(f"\nNombre de dates de sortie manquantes : {nb_dates_sortie_manquantes}")

# Dates de sortie vidéo manquantes
nb_dates_video_manquantes = movies['video_release_date'].isna().sum()
print(f"Nombre de dates de sortie vidéo manquantes : {nb_dates_video_manquantes}\n")

# Aperçu des trois premières lignes
print("Aperçu des trois premières lignes :")
print(movies.head(3))
