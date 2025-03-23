# 🌐 Système de Recommandation de Films - Projet Final

**Auteur : Joye Badou**Produit Final Fonctionnel

---

## ✉️ Table des Matières

- [Introduction](#introduction)
- [Phase I : Collecte des Données](#phase-i--collecte-des-données)
- [Phase II : Fiabilisation & Normalisation](#phase-ii--fiabilisation--normalisation)
- [Phase III : Analyse Exploratoire (EDA)](#phase-iii--analyse-exploratoire-eda)
- [Phase IV/V : Modélisation & Évaluation](#phase-ivv--modélisation--évaluation)
- [Phase VI : Produit Final Fonctionnel](#phase-vi--produit-final-fonctionnel)
- [Guide d'Utilisation](#guide-dutilisation)
- [Conclusion](#conclusion)

---

## 📄 Introduction

Ce projet repose sur l'analyse du dataset **MovieLens 100k** afin de construire un système de recommandation performant.

**Objectif :** Prévoir les films que les utilisateurs apprécieront, à l'aide d'approches comme le filtrage collaboratif, les modèles basés sur le contenu, et des modèles hybrides.

---

## 📊 Phase I : Collecte des Données

**Fichiers sources :** `u.data` et `u.item` transformés en `rating.csv` et `movie.csv`

**Actions :**

- Chargement et conversion des fichiers via script Python
- Structure des fichiers vérifiée
- Stockage dans HDFS (Hadoop)

**Extrait de code :**

```python
u_data = pd.read_csv("u.data", sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])
u_data.to_csv("rating.csv", index=False)
```

---

## ✅ Phase II : Fiabilisation & Normalisation

**rating.csv :**

- Suppression des doublons, timestamps, utilisateurs/films peu actifs
- Normalisation des notes via Min-Max

**movie.csv :**

- Suppression des colonnes inutiles (`IMDb_URL`, `video_release_date`, `unknown`)
- Nettoyage des dates et des doublons

**Fusion finale :** `rating_clean.csv` + `movie_clean.csv` → `merged_final_data.csv`

---

## 🧰 Phase III : Analyse Exploratoire (EDA)

### Films :

- Répartition par année, popularité
- Top films notés & mieux notés
- Distribution mono-genre / multi-genres

**Graphiques à insérer :**

![Répartition par année](EDA/films_par_annee.png)  
![Top films notés](EDA/top_films.png)

### Notes :

- Distribution des notes
- Moyenne par année
- Ancien vs Récent

**Graphiques :**

![Distribution des notes](EDA/distribution_notes.png)

### Genres :

- Nombre de films par genre
- Moyenne des notes par genre
- Corrélations entre genres

**Graphiques :**

![Heatmap des genres](EDA/heatmap_genres.png)

### Utilisateurs :

- Moyenne et variance des notes
- Utilisateurs les plus actifs

---

## 📊 Phase IV/V : Modélisation & Évaluation

**Algorithme utilisé :** KNN (k plus proches voisins)

### Modèles :

- **User-User KNN** → RMSE = 1.11
- **Item-Item KNN** → RMSE = 1.03 (**Meilleur**)
- **Content-Based** → Basé sur les genres
- **Hybride** (Content + User / Item)

### Optimisation :

- Recherche des meilleurs hyperparamètres
- Meilleur modèle final : `Item-Item KNN` avec `k=10`, `distance=manhattan`

---

## 🛠️ Phase VI : Produit Final Fonctionnel

### 💻 Interface en ligne de commande (CLI)

```bash
python recommandations_interactives.py
```

> L'utilisateur entre son `userId` et reçoit des recommandations personnalisées.

### 💾 API RESTful avec Flask

```bash
python api_recommendations.py
```

Accès via navigateur:[http://127.0.0.1:5000/recommendations?userId=20](http://127.0.0.1:5000/recommendations?userId=20)

---

## 📖 Guide d'utilisation

### ⚡ Prérequis

```bash
pip install pandas numpy flask scikit-learn
```

- Les données doivent être dans `C:\projet_work\Data-source\`

### 🔹 Scripts disponibles :

- `recommandations_interactives.py`
- `api_recommendations.py`

---

## 📅 Conclusion

Ce projet démontre qu'un modèle **Item-Item KNN** est efficace pour recommander des films. L'utilisation d'une **analyse exploratoire poussée**, combinée à l'évaluation par RMSE, a permis d'aboutir à une solution robuste.

Prochaines étapes : tests d'algorithmes plus complexes (SVD, deep learning, etc.)

---

## 🔗 Lien GitHub

**➜** [https://github.com/joyebadou/mon-projet-recommandation](https://github.com/joyebadou/mon-projet-recommandation)

---

**✉ Contact :** [joye@support.badou](mailto:joye@support.badou)
