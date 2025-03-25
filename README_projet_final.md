# 🌐 Système de Recommandation de Films - Projet Final

**Auteur : Joye Badou**  
**Produit Final Fonctionnel**

---

## 📑 Sommaire

- [Introduction](#introduction)
- [I. Phase de Collecte des Données](#i-phase-de-collecte-des-données)
- [II. Phase de Fiabilisation et Normalisation](#ii-phase-de-fiabilisation-et-normalisation)
- [III. Phase d’Analyse Exploratoire](#iii-phase-danalyse-exploratoire)
- [IV & V. Phase de Modélisation et d’Évaluation](#iv--v-phase-de-modélisation-et-dévaluation)
- [VI. Produit Final Fonctionnel et Déploiement](#vi-produit-final-fonctionnel-et-déploiement)
- [Conclusion](#conclusion)

---

## Introduction

Mon projet porte sur l’analyse et la modélisation des données MovieLens, une collection de plus de 100 000 notations réalisées par 943 utilisateurs sur environ 1 682 films. Bien que l'objectif initial fût d'exploiter le dataset complet de 33 millions de notations, la version 100k (plus maniable et accessible) a été retenue pour sa richesse tout en étant exploitable dans un environnement de développement standard.

Ce choix garantit un bon équilibre entre complexité, pertinence et rapidité d’analyse. L’étude se concentre sur les fichiers `movies` et `ratings`, en excluant notamment l’analyse des tags pour éviter une surcharge de complexité. Cette version simplifiée permet de mettre en œuvre un système de recommandation complet et pertinent.

---

## I. Phase de Collecte des Données

- Chargement des fichiers `ratings.csv`, `movies.csv`
- Vérification de la structure des fichiers (analyse des colonnes, types, valeurs)
- Nettoyage et renommage des colonnes si nécessaire
- Centralisation et fusion des données nettoyées dans `merged_final_data.csv`

_(Les détails des scripts et des résultats de cette section sont disponibles dans les blocs de code et résultats suivants du README)_

---

## II. Phase de Fiabilisation et Normalisation

Cette phase a pour but d'assurer la qualité et la cohérence des données en supprimant les doublons, les valeurs aberrantes ou inutiles, et en normalisant les colonnes clés.

- Nettoyage des fichiers `rating.csv` et `movie.csv`
- Suppression des doublons, outliers, notes extrêmes, colonnes inutiles, etc.
- Normalisation des notes (`rating_normalized`) entre 0 et 1
- Synchronisation des IDs entre les fichiers avant fusion finale

---

## III. Phase d’Analyse Exploratoire

Cette exploration vise à valider des hypothèses sur les comportements utilisateurs, la structure des films et les relations entre genres, en vue de construire des modèles de recommandation robustes.

### 1. Analyse des Films
- Films les plus notés
- Films les mieux notés (ayant plus de 50 notes)
- Films multi-genres vs mono-genre
- Nombre de genres par film

#### 📊 Graphiques produits (films)
- Nombre de films par année de sortie  
- Top 10 des films les plus notés  
- Top 10 des films les mieux notés  
- Top 10 des films avec le plus de genres  
- Distribution mono-genre vs multi-genres

_(Les commentaires détaillés se trouvent sous chaque graphique dans les sections précédentes du README)_

### 2. Analyse des Notes
- Distribution des notes  
- Moyenne des notes par film  
- Évolution des notes par année  
- Comparaison films anciens vs récents

#### 📊 Graphiques produits (notes)
- Histogramme des notes  
- Distribution du nombre de notes par film  
- Évolution des notes par année  
- Moyenne des notes films anciens vs récents

### 3. Analyse des Genres
- Nombre de films par genre  
- Note moyenne par genre  
- Évolution temporelle des genres `Sci-Fi` et `Drama`  
- Corrélations entre genres

#### 📊 Graphiques produits (genres)
- Barres horizontales : Nombre de films par genre  
- Barres horizontales : Note moyenne par genre  
- Courbe : évolution `Sci-Fi` et `Drama` par décennie  
- Heatmap des corrélations entre genres

_(Les résultats, commentaires et interprétations se trouvent sous chaque graphique)_

---

## IV & V. Phase de Modélisation et d’Évaluation

*(À compléter ici selon les modèles testés : User-User, Item-Item, Content-Based, Hybrid, etc.)*

---

## VI. Produit Final Fonctionnel et Déploiement

*(Description du script interactif, de l’API REST, et du guide d’utilisation à inclure ici)*

---

## Conclusion

Ce projet démontre la faisabilité de créer un système de recommandation efficace à partir de données MovieLens, en suivant une méthodologie claire : collecte, nettoyage, exploration, modélisation et déploiement. L’analyse détaillée a permis de valider plusieurs hypothèses utiles pour les recommandations personnalisées.

_(Tous les scripts, résultats et visualisations sont accessibles dans le dépôt GitHub)_
