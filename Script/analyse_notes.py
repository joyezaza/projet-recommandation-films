import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des données
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')

# ----------------------- Analyse Générale des Notes ------------------------

# Nombre total de notes
total_notes = data.shape[0]
print(f"Nombre total de notes dans la base : {total_notes}")

# Statistiques descriptives des notes
stats_notes = data['rating'].describe()
print("\nStatistiques descriptives des notes :")
print(stats_notes)

# Histogramme de la distribution des notes
plt.figure(figsize=(8,5))
sns.histplot(data['rating'], bins=5, kde=True)
plt.title('Distribution des notes utilisateurs')
plt.xlabel('Notes')
plt.ylabel('Fréquence')
plt.tight_layout()
plt.show()

# ----------------------- Nombre moyen de notes par film ------------------------

notes_par_film = data.groupby('movie_id').size()
moyenne_notes_film = notes_par_film.mean().round(2)
print(f"\nNombre moyen de notes par film : {moyenne_notes_film}")

# Graphique: Distribution du nombre de notes par film
plt.figure(figsize=(8,5))
sns.histplot(notes_par_film, bins=30, kde=True, color='lightcoral')
plt.title('Distribution du nombre de notes par film')
plt.xlabel('Nombre de notes')
plt.ylabel('Nombre de films')
plt.tight_layout()
plt.show()

# ----------------------- Corrélation entre Année et Note ------------------------

# Convertir release_date en datetime
data['release_date'] = pd.to_datetime(data['release_date'])
data['release_year'] = data['release_date'].dt.year

# Note moyenne par année
note_par_annee = data.groupby('release_year')['rating'].mean()

print("\nNote moyenne des films par année (10 premières lignes):")
print(note_par_annee.head(10))

# Graphique: Évolution des notes moyennes par année
plt.figure(figsize=(12,5))
note_par_annee.plot(marker='o', linestyle='-', color='teal')
plt.title('Évolution de la note moyenne des films par année')
plt.xlabel('Année de sortie')
plt.ylabel('Note moyenne')
plt.grid(True)
plt.tight_layout()
plt.show()

# ----------------------- Films anciens vs récents ------------------------

# Créer deux catégories de films : anciens (avant 1980), récents (1980 et après)
data['age_group'] = data['release_year'].apply(lambda x: 'Ancien (<1980)' if x < 1980 else 'Récent (>=1980)')
notes_age_group = data.groupby('age_group')['rating'].mean()

print("\nNote moyenne des films selon ancienneté :")
print(notes_age_group)

# Graphique: Moyenne des notes films anciens vs récents
plt.figure(figsize=(7,5))
notes_age_group.plot(kind='bar', color=['orange','dodgerblue'])
plt.title('Note moyenne : films anciens vs récents')
plt.ylabel('Note moyenne')
plt.xlabel('Catégorie de film')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()
