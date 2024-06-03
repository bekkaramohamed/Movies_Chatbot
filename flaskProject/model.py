from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

import spacy

nlp = spacy.load('en_core_web_sm')

# Chargement du modèle BERT
modelBert = SentenceTransformer('all-MiniLM-L6-v2')


def find_k_films_bert_similarity_with_user_desc(model, dataset, plot, k=5):
    # Encodage du plot du film référence
    reference_embedding = model.encode([plot])

    # Maintenant on doit essayer de trouver les k films les plus proches selon les embeddings
    # Liste pour stocker les informations des k films les plus similaires
    top_k_movies_info = []

    for line in dataset.index:
        # Récupération des embeddings des plots
        plot_embedding = dataset.loc[line, 'Plot_Embedding']
        plot_embedding = np.fromstring(plot_embedding[1:-1], sep=' ')

        # Calcul de la similarité cosine entre la référence et le plot du film
        similarity_score = cosine_similarity(reference_embedding, plot_embedding.reshape(1, -1))[0][0]

        # Stockage des informations des films et du score de similarité
        movie_info = {
            'Title': dataset.loc[line, 'Title'],
            'Genre': dataset.loc[line, 'Genre'],
            'Director': dataset.loc[line, 'Director'],
            'Release Year': dataset.loc[line, 'Release Year'],
            'Similarity Score': similarity_score
        }

        # Ajout des films dans la liste
        top_k_movies_info.append(movie_info)

    # Tri de la liste par scores de similarité décroissants et récupération des k films avec le score le plus élevé
    top_k_movies_info = sorted(top_k_movies_info, key=lambda x: x['Similarity Score'], reverse=True)[:k]

    # Affichage des films dans la console
    # Pour le debugage
    # print(top_k_movies_info)

    # Renvoi des k films à recommander
    return top_k_movies_info
