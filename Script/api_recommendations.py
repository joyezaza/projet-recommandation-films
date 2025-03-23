from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

app = Flask(__name__)

# Charger les données et créer la matrice utilisateur-film
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')
user_item_matrix = data.pivot_table(index='user_id', columns='movie_title', values='rating', fill_value=0)

# Entraîner le modèle Item-Item KNN avec les hyperparamètres optimaux
# Ici, nous utilisons n_neighbors=10, metric='manhattan' et algorithm='ball_tree'
knn = NearestNeighbors(n_neighbors=10, metric='manhattan', algorithm='ball_tree')
# Pour le filtrage Item-Item, nous transposons la matrice pour que chaque film soit représenté par
# les notes de tous les utilisateurs.
knn.fit(user_item_matrix.T.values)

def predict_rating(user_id, movie, user_item_matrix, knn, k=10):
    """
    Prédit la note d'un film pour un utilisateur donné via une approche Item-Item.
    Si l'utilisateur a déjà noté le film, retourne la note réelle.
    Sinon, calcule la moyenne des notes de ce même utilisateur sur des films similaires.
    """
    # Si déjà noté, retourner la note existante
    if user_item_matrix.loc[user_id, movie] != 0:
        return user_item_matrix.loc[user_id, movie]
    
    # Obtenir le vecteur du film (les notes de tous les utilisateurs)
    movie_vector = user_item_matrix.T.loc[movie].values.reshape(1, -1)
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
    return np.mean(ratings) if ratings else 0

def get_recommendations(user_id, user_item_matrix, knn, top_n=5):
    """
    Pour un utilisateur donné, prédit les notes pour les films non notés
    et retourne les top_n recommandations.
    """
    # Films que l'utilisateur n'a pas notés (note == 0)
    unrated_movies = user_item_matrix.columns[user_item_matrix.loc[user_id] == 0]
    predictions = {}
    for movie in unrated_movies:
        pred = predict_rating(user_id, movie, user_item_matrix, knn)
        predictions[movie] = pred
    # Trier les films par note prédite décroissante et prendre les top_n
    sorted_predictions = sorted(predictions.items(), key=lambda x: x[1], reverse=True)
    return sorted_predictions[:top_n]

@app.route('/recommendations', methods=['GET'])
def recommendations():
    """
    Endpoint qui attend un paramètre query 'userId' et retourne en JSON les recommandations.
    Exemple d'appel : http://localhost:5000/recommendations?userId=1
    """
    user_id = request.args.get('userId')
    if user_id is None:
        return jsonify({'error': 'Le paramètre userId est requis.'}), 400
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({'error': 'userId doit être un entier.'}), 400
    
    if user_id not in user_item_matrix.index:
        return jsonify({'error': f'userId {user_id} non trouvé dans la base.'}), 404

    recs = get_recommendations(user_id, user_item_matrix, knn, top_n=5)
    recommendations_list = [{'movie': movie, 'predicted_rating': round(score, 2)} for movie, score in recs]
    
    return jsonify({'userId': user_id, 'recommendations': recommendations_list})

if __name__ == '__main__':
    app.run(debug=True)
