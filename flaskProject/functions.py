from transformers import GPT2LMHeadModel, GPT2Tokenizer
from filters import filter_by_genre_film, filter_by_reference_title, get_information_operator_and_year_from_prompt
from model import find_k_films_bert_similarity_with_user_desc

import spacy
import re

nlp = spacy.load('en_core_web_sm')

# Chargement du modèle GPT-2 pré-entraîné et le tokenizer
model_name = "gpt2"
tokenizerGPT2 = GPT2Tokenizer.from_pretrained(model_name)
modelGPT2 = GPT2LMHeadModel.from_pretrained(model_name)


# Fonction d'extraction des informations données par l'utilisateurs
# Si l'utilisateur skip le filtrage par genre et année
# On essaye de récupérer le genre et l'année à partir d'expressions régulières
def extract_user_prompt_information(dataset, user_description):
    # Recupéartion des genres uniques dataset
    genres_available = dataset['Genre'].unique()
    doc = nlp(user_description)

    movie_info = {
        'Title': None,
        'Genres': [],
        'Release Year': None
    }

    for ent in doc.ents:
        print(f"Entité: {ent.text}, Catégorie: {ent.label_}")

        if ent.label_ == 'FILM' or ent.label_ == 'PERSON':
            movie_info['Title'] = ent.text

    # Utiliser l'expression régulière pour extraire le genre
    for genre in genres_available:
        if re.search(fr'\b{re.escape(genre.lower())}\b', user_description, flags=re.IGNORECASE):
            movie_info['Genres'].append(genre)

    # Utiliser l'expression régulière pour extraire l'année
    annee_match = re.search(r'\b(19[0-9][0-9]|200[0-9]|201[0-7])\b', user_description)
    if annee_match:
        movie_info['Release Year'] = annee_match.group()

    return movie_info


# Formulation de la réponse avec GPT-2
# Récupération du prompt (= les k films), du model gpt2 et du tokenizer
def generate_response_with_gpt2(prompt, model, tokenizer, max_length=1000):
    # Tokeniser le prompt
    input_ids = tokenizer.encode(prompt, return_tensors="pt", max_length=max_length, truncation=True)

    # Créer l'attention mask
    attention_mask = input_ids.clone()
    attention_mask[
        # Mettre à 1 tous les tokens qui ne sont pas des tokens de remplissage (padding)
        attention_mask != tokenizer.pad_token_id] = 1
    # Générer la réponse
    output = model.generate(
        input_ids, max_length=max_length, num_beams=5, no_repeat_ngram_size=2, top_k=50,
        top_p=0.95, temperature=0.6, pad_token_id=tokenizer.eos_token_id, attention_mask=attention_mask)
    # Décoder la réponse
    generated_response = tokenizer.decode(output[0], skip_special_tokens=True)

    return generated_response


# Fonction principale qui permet de faire tout le filtrage et d'extraire les films recommandés
# Récupération de toute les informations données par l'utilisateur (filtre, genre, year, user_query)
def generate_final_recommendation(bert_model, dataset, filtre, genre, year, user_query):
    # Filtrage notre dataset par rapport au user_prompt
    # genre --> year --> titre ou description
    recommended_movies = []
    filtered_dataset = dataset

    # Si l'utilisateur a skip les 2 questions de genre et d'année
    # Appel de la fonction extract_user_prompt_information pour essayer de filtrer le dataset
    if genre == "" and year == "":
        user_desc_info = extract_user_prompt_information(dataset, user_query)
        # Pour le debugage
        print(user_desc_info)

        # Partie des filtres du dataset
        # Filtrage du dataset par rapport aux genres identifiés dans extract_user_prompt_information
        if user_desc_info['Genres'] is not None:
            for genres_identified in user_desc_info['Genres']:
                filtered_dataset = filter_by_genre_film(dataset, genres_identified)

        # Ce filtre ok Valide

    # Si le filtre d'année n'est pas vide
    # Appel de la fonction get_information_operator_and_year_from_prompt pour filtrer par rapport à l'année
    if year != "":
        filtered_dataset = get_information_operator_and_year_from_prompt(dataset, year)

    # Si le filtre de genre n'est pas vide
    # Appel de la fonction filter_by_genre_film pour filtrer par rapport au genre
    if genre != "":
        filtered_dataset = filter_by_genre_film(filtered_dataset, genre)

    # Fin de la partie des filtres
    # Recupérer les k films les plus proches de la descriptions utilisateur

    # Si l'utilisateur choisi de trouver des films par un titre de référence
    # On cherche dans le dataset le film correspondant
    # Si le film est trouver on récupère son ID sinon on renvoi un message d'excuse
    if filtre == "title":
        movie_id = filter_by_reference_title(dataset, user_query)
        if movie_id == "":
            return "Sorry, we can't find a movie"

        # Récupération du plot du film
        # Appel à la fonction find_k_films_bert_similarity_with_user_desc avec ce plot (movie_plot) pour l'embedding
        movie_plot = dataset.loc[movie_id, 'Plot']
        recommended_movies = find_k_films_bert_similarity_with_user_desc(bert_model, filtered_dataset, movie_plot, k=5)

    # Si l'utilisateur choisi de trouver des films par une description
    # Appel à la fonction find_k_films_bert_similarity_with_user_desc avec la descr user (user_query) pour l'embedding
    elif filtre == "description":
        recommended_movies = find_k_films_bert_similarity_with_user_desc(bert_model, filtered_dataset, user_query, k=5)

    # Une fois les k films trouvés
    # Formater les recommandations pour GPT-2
    formatted_recommendations = ", ".join([film['Title'] for film in recommended_movies])

    # Soumettre la description avec les recommandations à GPT-2 et extraire la réponse générée
    generated_response = generate_response_with_gpt2(f"Watch movies like {formatted_recommendations}", modelGPT2,
                                                     tokenizerGPT2)

    # Pour le débugage
    print(str(recommended_movies))

    # Retourne la recommandation génerée
    return generated_response
