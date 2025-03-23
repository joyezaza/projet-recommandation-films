import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des données
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')

# Conversion date de sortie en datetime
data['release_date'] = pd.to_datetime(data['release_date'])
data['release_year'] = data['release_date'].dt.year

genres = ['Action','Adventure','Animation',"Children's",'Comedy','Crime',
          'Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',
          'Mystery','Romance','Sci-Fi','Thriller','War','Western']

# ----------------------- Nombre de films par genre ------------------------

nb_films_genre = {genre: data[data[genre]==1]['movie_id'].nunique() for genre in genres}
nb_films_genre_series = pd.Series(nb_films_genre).sort_values(ascending=False)

print("Nombre de films par genre :")
print(nb_films_genre_series)

# Graphique: nombre de films par genre
plt.figure(figsize=(12,6))
sns.barplot(y=nb_films_genre_series.index, x=nb_films_genre_series.values, palette='mako')
plt.xlabel('Nombre de films')
plt.ylabel('Genre')
plt.title('Nombre de films par genre')
plt.tight_layout()
plt.show()

# ----------------------- Notes moyennes par genre ------------------------

note_genres = {genre: data[data[genre]==1]['rating'].mean() for genre in genres}
note_genres_series = pd.Series(note_genres).sort_values(ascending=False)

print("\nNote moyenne par genre :")
print(note_genres_series)

# Graphique: note moyenne par genre
plt.figure(figsize=(12,6))
sns.barplot(y=note_genres_series.index, x=note_genres_series.values, palette='viridis')
plt.xlabel('Note moyenne')
plt.ylabel('Genre')
plt.title('Note moyenne par genre')
plt.xlim(3,5)
plt.tight_layout()
plt.show()

# ----------------------- Évolution des genres dans le temps ------------------------

# Exemple : évolution du genre "Sci-Fi" et "Drama" par décennie
data['decade'] = (data['release_year']//10)*10
genres_temps = data.groupby('decade')[['Sci-Fi','Drama']].sum()

print("\nÉvolution des genres 'Sci-Fi' et 'Drama' par décennie :")
print(genres_temps)

# Graphique : Évolution temporelle
genres_temps.plot(kind='line', marker='o', figsize=(10,5))
plt.title('Évolution des genres Sci-Fi et Drama par décennie')
plt.xlabel('Décennie')
plt.ylabel('Nombre de films')
plt.grid(True)
plt.tight_layout()
plt.show()

# ----------------------- Corrélation entre genres ------------------------

correlation_genres = data[genres].corr()

print("\nCorrélation entre genres (extrait) :")
print(correlation_genres.head())

# Graphique: heatmap des corrélations
plt.figure(figsize=(14,10))
sns.heatmap(correlation_genres, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Heatmap des corrélations entre genres')
plt.tight_layout()
plt.show()
