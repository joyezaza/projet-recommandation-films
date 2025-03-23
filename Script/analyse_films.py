import pandas as pd
import matplotlib.pyplot as plt

# Chargement des données
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')

# Conversion de la colonne date au format datetime
data['release_date'] = pd.to_datetime(data['release_date'])

# ----------------------------- Analyse Générale -----------------------------

# Nombre total de films uniques
total_films = data['movie_id'].nunique()
print(f"Nombre total de films : {total_films}")

# Répartition des films par année de sortie
films_par_annee = data[['movie_id', 'release_date']].drop_duplicates().groupby(data['release_date'].dt.year).count()['movie_id']
print("\nRépartition des films par année (10 premières lignes):")
print(films_par_annee.head(10))

# Graphique: Répartition des films par année
plt.figure(figsize=(10,5))
films_par_annee.plot(kind='bar', color='skyblue')
plt.title('Nombre de films par année de sortie')
plt.xlabel('Année de sortie')
plt.ylabel('Nombre de films')
plt.tight_layout()
plt.show()

# ----------------------------- Films populaires -----------------------------

# Top 10 films les plus notés
top_films_notes = data['movie_title'].value_counts().head(10)
print("\nTop 10 des films les plus notés:")
print(top_films_notes)

# Graphique: Top 10 films les plus notés
plt.figure(figsize=(10,5))
top_films_notes.plot(kind='barh', color='salmon')
plt.xlabel('Nombre de notes')
plt.ylabel('Titre du film')
plt.title('Top 10 des films les plus notés')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# ----------------------------- Films les mieux notés -----------------------------

# Calcul des films les mieux notés avec plus de 50 notes
ratings_stats = data.groupby('movie_title')['rating'].agg(['mean', 'count'])
films_mieux_notes = ratings_stats[ratings_stats['count'] > 50].sort_values('mean', ascending=False).head(10)
print("\nTop 10 des films les mieux notés (ayant plus de 50 notes):")
print(films_mieux_notes)

# Graphique: Top 10 des films les mieux notés
plt.figure(figsize=(10,5))
films_mieux_notes['mean'].plot(kind='barh', color='limegreen')
plt.xlabel('Note moyenne')
plt.ylabel('Titre du film')
plt.title('Top 10 des films les mieux notés (> 50 notes)')
plt.gca().invert_yaxis()
plt.xlim(3, 5)
plt.tight_layout()
plt.show()

# ----------------------------- Films multi-genres -----------------------------

genres = ['Action','Adventure','Animation',"Children's",'Comedy','Crime',
          'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',
          'Mystery','Romance','Sci-Fi','Thriller','War','Western']

# Calcul du nombre de genres par film
films_genres = data[['movie_id', 'movie_title'] + genres].drop_duplicates()
films_genres['nombre_genres'] = films_genres[genres].sum(axis=1)

# Top 10 films avec le plus de genres
films_multi_genres = films_genres.sort_values('nombre_genres', ascending=False).head(10)
print("\nTop 10 films multi-genres:")
print(films_multi_genres[['movie_title', 'nombre_genres']])

# Graphique: Films multi-genres
plt.figure(figsize=(10,5))
films_multi_genres.set_index('movie_title')['nombre_genres'].plot(kind='barh', color='orchid')
plt.xlabel('Nombre de genres')
plt.ylabel('Titre du film')
plt.title('Top 10 des films avec le plus de genres')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.show()

# ----------------------------- Distribution mono-genre vs multi-genres -----------------------------

films_genres_distribution = films_genres['nombre_genres'].apply(lambda x: 'Mono-genre' if x==1 else 'Multi-genres').value_counts()
print("\nDistribution films mono-genre vs multi-genres :")
print(films_genres_distribution)

# Graphique: Mono-genre vs multi-genres
plt.figure(figsize=(7,5))
films_genres_distribution.plot(kind='pie', autopct='%1.1f%%', colors=['gold','deepskyblue'], explode=[0, 0.05])
plt.title('Distribution des films mono-genre vs multi-genres')
plt.ylabel('')
plt.tight_layout()
plt.show()
