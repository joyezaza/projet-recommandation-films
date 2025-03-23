import pandas as pd

# Chargement des données
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')

# Création de la matrice User-Item
user_item_matrix = data.pivot_table(index='user_id', columns='movie_title', values='rating').fillna(0)

# Sauvegarde de la matrice
user_item_matrix.to_csv(r'C:\projet_work\Data-source\user_item_matrix.csv')

print("Matrice User-Item créée avec succès.")
