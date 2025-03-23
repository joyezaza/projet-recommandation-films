import pandas as pd

# Chargement du fichier movie.csv
movies = pd.read_csv(r'C:\projet_work\Data-source\movie.csv')

# Suppression des lignes avec dates de sortie manquantes
movies_clean = movies.dropna(subset=['release_date'])

# Suppression des colonnes demandées ('video_release_date', 'unknown', 'IMDb_URL')
movies_clean = movies_clean.drop(columns=['video_release_date', 'unknown', 'IMDb_URL'])

# Suppression des lignes entièrement dupliquées en gardant une seule occurrence
movies_clean = movies_clean.drop_duplicates(keep='first')

# Afficher le bilan après nettoyage
nb_lignes_finales = movies_clean.shape[0]
print(f"Nombre de lignes après nettoyage : {nb_lignes_finales}\n")

# Aperçu des trois premières lignes après nettoyage
print("Aperçu des 3 premières lignes après nettoyage :")
print(movies_clean.head(3))

# Sauvegarder le fichier nettoyé (optionnel mais recommandé)
movies_clean.to_csv(r'C:\projet_work\Data-source\movie_clean.csv', index=False)
