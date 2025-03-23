import pandas as pd

# Chargement des fichiers nettoyés
movies = pd.read_csv(r'C:\projet_work\Data-source\movie_clean.csv')
ratings = pd.read_csv(r'C:\projet_work\Data-source\clean_rating.csv')

# Fusion des deux fichiers sur la colonne 'movie_id'
merged_data = pd.merge(ratings, movies, on='movie_id', how='inner')

# Vérification rapide après fusion
nb_lignes_fusionnees = merged_data.shape[0]
print(f"Nombre total de lignes après fusion : {nb_lignes_fusionnees}\n")

# Aperçu des 3 premières lignes fusionnées
print("Aperçu des 3 premières lignes après fusion :")
print(merged_data.head(3))

# Sauvegarde du fichier fusionné clairement nommé 'merged_data.csv'
merged_data.to_csv(r'C:\projet_work\Data-source\merged_data.csv', index=False)
