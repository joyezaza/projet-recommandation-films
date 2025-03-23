import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

# Chargement des données et création de la matrice utilisateur-film
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')
# Création de la matrice : lignes = user_id, colonnes = movie_title, valeurs = rating (0 si non noté)
user_item_matrix = data.pivot_table(index='user_id', columns='movie_title', values='rating', fill_value=0)

# Construction du modèle Item-Item KNN.
# Ici, nous utilisons les hyperparamètres optimaux trouvés : 
# n_neighbors = 10, metric = 'manhattan', algorithm = 'ball_tree'.
# Pour l'item-item, chaque film est représenté par les notes de tous les utilisateurs.
# Nous transposons la matrice pour avoir les films en lignes.
knn = NearestNeighbors(n_neighbors=10, metric='manhattan', algorithm='ball_tree')
knn.fit(user_item_matrix.T.values)

def predict_rating(user_id, movie, user_item_matrix, knn, k=10):
    """
    Prédit la note de 'movie' pour 'user_id' en utilisant une approche Item-Item.
    Si l'utilisateur a déjà noté le film, retourne la note réelle.
    Sinon, calcule la moyenne des notes de ce même utilisateur pour des films similaires.
    """
    # Si l'utilisateur a déjà noté ce film, retourner la note réelle.
    if user_item_matrix.loc[user_id, movie] != 0:
        return user_item_matrix.loc[user_id, movie]
    
    # Obtenir le vecteur du film (les notes de tous les utilisateurs)
    movie_vector = user_item_matrix.T.loc[movie].values.reshape(1, -1)
    # Trouver les k voisins les plus proches pour ce film
    distances, indices = knn.kneighbors(movie_vector, n_neighbors=k)
    # Récupérer les titres des films voisins
    similar_movies = user_item_matrix.T.index[indices.flatten()]
    # Exclure le film courant
    similar_movies = [m for m in similar_movies if m != movie]
    
    # Récupérer les notes que l'utilisateur a données à ces films
    ratings = []
    for m in similar_movies:
        r = user_item_matrix.loc[user_id, m]
        if r != 0:
            ratings.append(r)
    # Si l'utilisateur a noté certains films similaires, retourner la moyenne, sinon 0
    return np.mean(ratings) if ratings else 0

def get_recommendations(user_id, user_item_matrix, knn, top_n=5):
    """
    Pour un utilisateur donné, prédit les notes des films non notés et retourne les top_n recommandations.
    """
    # Liste des films que l'utilisateur n'a pas notés (note = 0)
    unrated_movies = user_item_matrix.columns[user_item_matrix.loc[user_id] == 0]
    predictions = {}
    for movie in unrated_movies:
        pred = predict_rating(user_id, movie, user_item_matrix, knn)
        predictions[movie] = pred
    # Trier par note prédite décroissante et retourner les top_n films
    sorted_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    return sorted_predictions[:top_n]

# --- Script interactif ---
user_input = input("Entrez votre userId: ")
try:
    user_id = int(user_input)
except ValueError:
    print("UserId invalide. Veuillez entrer un entier.")
    exit()

if user_id not in user_item_matrix.index:
    print("UserId non trouvé dans la base de données.")
    exit()

# Obtenir et afficher les recommandations pour l'utilisateur
recommendations = get_recommendations(user_id, user_item_matrix, knn, top_n=5)
print(f"\n🎬 Recommandations pour l'utilisateur {user_id}:")
for movie, score in recommendations:
    print(f"{movie}: note prédite {score:.2f}")
