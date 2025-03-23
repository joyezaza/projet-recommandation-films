import pandas as pd

# 📌 Chemins des fichiers d'entrée et de sortie
u_data_path = r"C:\projet_work\Data-source\u.data"
u_item_path = r"C:\projet_work\Data-source\u.item"
ratings_output_path = r"C:\projet_work\Data-source\rating.csv"
movies_output_path = r"C:\projet_work\Data-source\movie.csv"

# 📌 Conversion de u.data en rating.csv
def convert_u_data_to_csv(input_path, output_path):
    try:
        # Chargement des données avec les colonnes appropriées
        column_names = ['user_id', 'movie_id', 'rating', 'timestamp']
        u_data = pd.read_csv(input_path, sep='\t', names=column_names, header=None)
        
        # Enregistrement dans un fichier CSV
        u_data.to_csv(output_path, index=False)
        print(f"✅ Conversion de {input_path} en {output_path} réussie.")
    except Exception as e:
        print(f"❌ Erreur lors de la conversion de {input_path} : {e}")

# 📌 Conversion de u.item en movie.csv
def convert_u_item_to_csv(input_path, output_path):
    try:
        # Chargement des données avec les colonnes appropriées
        column_names = [
            'movie_id', 'movie_title', 'release_date', 'video_release_date', 'IMDb_URL',
            'unknown', 'Action', 'Adventure', 'Animation', "Children's", 'Comedy', 'Crime',
            'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery',
            'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'
        ]
        u_item = pd.read_csv(input_path, sep='|', names=column_names, encoding='latin-1', header=None)
        
        # Enregistrement dans un fichier CSV
        u_item.to_csv(output_path, index=False)
        print(f"✅ Conversion de {input_path} en {output_path} réussie.")
    except Exception as e:
        print(f"❌ Erreur lors de la conversion de {input_path} : {e}")

# 📌 Exécution des conversions
convert_u_data_to_csv(u_data_path, ratings_output_path)
convert_u_item_to_csv(u_item_path, movies_output_path)
