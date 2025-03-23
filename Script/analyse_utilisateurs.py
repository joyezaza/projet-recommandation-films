import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chargement des données
data = pd.read_csv(r'C:\projet_work\Data-source\merged_final_data.csv')

# ----------------------- Analyse Générale des Utilisateurs ------------------------

# Nombre total d’utilisateurs
total_users = data['user_id'].nunique()
print(f"Nombre total d'utilisateurs : {total_users}")

# Nombre moyen de notes par utilisateur
notes_par_utilisateur = data.groupby('user_id').size()
moyenne_notes_user = notes_par_utilisateur.mean().round(2)
print(f"\nNombre moyen de notes par utilisateur : {moyenne_notes_user}")

# ----------------------- Utilisateurs les plus actifs ------------------------

top_utilisateurs_actifs = notes_par_utilisateur.sort_values(ascending=False).head(10)
print("\nTop 10 utilisateurs les plus actifs :")
print(top_utilisateurs_actifs)

# Graphique: Top 10 utilisateurs les plus actifs
plt.figure(figsize=(10,5))
top_utilisateurs_actifs.plot(kind='bar', color='skyblue')
plt.title('Top 10 utilisateurs les plus actifs')
plt.xlabel('User ID')
plt.ylabel('Nombre de notes')
plt.tight_layout()
plt.show()

# ----------------------- Distribution du nombre de notes par utilisateur ------------------------

plt.figure(figsize=(10,5))
sns.histplot(notes_par_utilisateur, bins=50, kde=True, color='green')
plt.title('Distribution du nombre de notes par utilisateur')
plt.xlabel('Nombre de notes données')
plt.ylabel('Nombre d\'utilisateurs')
plt.tight_layout()
plt.show()

# ----------------------- Variance et Moyenne des notes par utilisateur ------------------------

stats_users = data.groupby('user_id')['rating'].agg(['mean','var'])
print("\nStatistiques (moyenne et variance) des notes par utilisateur (10 premiers) :")
print(stats_users.head(10))

# Graphique: Distribution des moyennes des notes par utilisateur
plt.figure(figsize=(10,5))
sns.histplot(stats_users['mean'], bins=30, kde=True, color='orange')
plt.title('Distribution des moyennes de notes par utilisateur')
plt.xlabel('Moyenne des notes')
plt.ylabel('Nombre d\'utilisateurs')
plt.tight_layout()
plt.show()

# Graphique: Distribution des variances des notes par utilisateur
plt.figure(figsize=(10,5))
sns.histplot(stats_users['var'].dropna(), bins=30, kde=True, color='red')
plt.title('Distribution des variances des notes par utilisateur')
plt.xlabel('Variance des notes')
plt.ylabel('Nombre d\'utilisateurs')
plt.tight_layout()
plt.show()
