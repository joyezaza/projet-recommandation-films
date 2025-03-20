README

---

Système de Recommandation de Films
 Introduction
Ce projet vise à développer un système de recommandation de films basé sur le dataset MovieLens 100K. Il intègre plusieurs approches de filtrage collaboratif et basé sur le contenu, avec des modèles hybrides pour optimiser la précision des recommandations. L'objectif est de fournir une solution complète, depuis la collecte et la préparation des données jusqu'au déploiement d'une API RESTful et d'un script interactif.

I. Phase de Collecte des Données
- Chargement des fichiers :
  Fichiers source : `ratings.csv`, `movies.csv`, etc.
- Vérification de la structure : 
  Description détaillée des données contenues dans `movie.csv` et `rating.csv`.
- Centralisation :
   Stockage des données dans un système structuré (HDFS).

II. Phase de Fiabilisation et Normalisation
- Nettoyage des données :
  Traitement et suppression des doublons, gestion des valeurs manquantes et aberrantes dans `rating.csv` et `movie.csv`.
- Fusion : 
  Intégration des données nettoyées en un fichier unique, `merged_final_data.csv`, qui servira de base pour l'analyse et la modélisation.

III. Phase d’Analyse Exploratoire
- Analyse des Films :  
   Étude du nombre total de films, répartition par année et par genre, et identification des films populaires et multi-genres.
- Analyse des Notes :
   Exploration des distributions des notations et des tendances globales.
- Analyse des Genres :
  Évaluation de la répartition des genres, des notes moyennes par genre, et des corrélations entre genres.
- Analyse des Utilisateurs :  
  Analyse de l'activité des utilisateurs et de leurs préférences à travers la distribution des notes et des interactions.

IV. Phase de Modélisation et d’Évaluation
- Préparation des Données :
   Construction de la matrice utilisateur-film pour la modélisation.
- Implémentation de KNN pour le Filtrage Collaboratif :  
  Modèle User-User :** Création et évaluation avec calcul du RMSE.
  Modèle Item-Item :** Création et évaluation, avec une performance optimale obtenue (RMSE ≈ 0.496).
- Modèle Basé sur le Contenu : 
   Utilisation des genres pour créer un modèle Content-Based, avec évaluation de ses performances.
- Modèles Hybrides :  
  - Hybrid Content-User : Combinaison des similarités utilisateurs et des caractéristiques de contenu.
  - Hybrid Content-Item :Fusion de la similarité basée sur le contenu et du filtrage collaboratif entre films.
- Optimisation des Hyperparamètres :  
  Tests et validation croisée pour déterminer les meilleures configurations pour chaque modèle, afin d'améliorer les performances.

V. Produit Final Fonctionnel et Déploiement
- Script Interactif : 
  Un script Python permettant à un utilisateur de saisir son userId et d'obtenir des recommandations personnalisées.
- API RESTful :  
  Une API développée avec Flask, offrant un point d'accès dynamique aux recommandations.
- Guide d'Utilisation :
  - Documentation détaillée pour aider les utilisateurs à exploiter le système.
- Publication sur GitHub : 
  - Le code source et la documentation complète sont disponibles dans le dépôt GitHub.

Conclusion
Ce projet a démontré la faisabilité et l'efficacité d'un système de recommandation de films, tout en validant les hypothèses selon lesquelles des utilisateurs aux notations similaires partagent des goûts proches, et que les genres constituent un indicateur fiable de similarité entre films. Le modèle Item-Item KNN a émergé comme le plus performant, bien que les approches hybrides offrent des pistes prometteuses pour de futures optimisations. Le projet fournit une base solide pour déployer une solution complète destinée à améliorer l'expérience utilisateur dans la découverte de films, et ouvre la voie à des améliorations ultérieures, notamment par l'exploration de techniques d'apprentissage automatique.

---
