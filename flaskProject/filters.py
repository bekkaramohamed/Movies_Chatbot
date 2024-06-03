import re
import spacy

nlp = spacy.load('en_core_web_sm')


# FILTRE PAR DESCRIPTION OU TITRE DE REFERENCE
def description_or_title(user_prompt):
    # savoir si l'utilisateur va rentrer une description ou un titre de réference
    # avec regex

    if re.search(r'\btitle\b', user_prompt) or re.search(r'\breference\b', user_prompt):
        return "title"
    elif re.search(r'\bdescription\b', user_prompt):
        return "description"


# FILTRE PAR TITRE DE REFERENCE

def filter_by_reference_title(dataset, user_title_ref):
    matching_titles = dataset[dataset['Title'].str.contains(user_title_ref, case=False)]
    matching_ids = []

    if not matching_titles.empty:
        matching_ids = matching_titles['Unnamed: 0'].tolist()
        print(f"Film exist in dataset. IDs: {matching_ids}")
        # Tu peux accéder aux informations sur les films correspondants dans matching_titles
    else:
        print("Film doesn't exist in the dataset")

    return matching_ids[0]


# FILTRE PAR GENRE
def filter_by_genre_film(dataset, user_genre_ref_list):
    # Lister les genres qui sont disponibles dans le dataset
    genres_available = dataset['Genre'].unique().tolist()

    genre_list = user_genre_ref_list.split(',')
    for genre in genre_list:
        if genre in genres_available:
            filtered_dataset = dataset[dataset['Genre'].str.contains(genre, case=False)]
            return filtered_dataset
        else:
            return dataset


# FILTRE PAR DATE
def filter_by_year(dataset, operator, year):
    subset = dataset
    if operator == '=':
        subset = dataset[dataset['Release Year'] == year]
    elif operator == '>':
        subset = dataset[dataset['Release Year'] > year]
    elif operator == '<':
        subset = dataset[dataset['Release Year'] < year]
    return subset


def filter_between_two_dates(dataset, list_of_dates):
    # On trie la liste des dates qui contient deux dates
    list_of_dates = sorted(list_of_dates)
    print(list_of_dates)
    subset = dataset[(dataset['Release Year'] >= list_of_dates[0]) & (dataset['Release Year'] <= list_of_dates[1])]
    return subset


def get_information_operator_and_year_from_prompt(dataset, user_prompt):
    filtered_data = dataset
    # Variables qui vont nous permettre de filtrer notre dataset
    year_list = []
    doc = nlp(user_prompt)

    for ent in doc.ents:
        if ent.label_ == 'DATE':
            # Si la phrase contient "between", extrait les années individuelles
            if 'between' in ent.text:
                # Utilise une expression régulière pour extraire les années
                years = re.findall(r'\b\d+\b', ent.text)
                year_list.extend(map(int, years))
            else:
                # Sinon, ajoute simplement l'année à la liste
                year_list.append(int(ent.text))

    # pour debugage
    print("Identified dates:")
    print(year_list)

    # Utiliser les regex pour déterminer l'opérateur à utiliser
    if re.search(r'\b(?:released|directed) in\b', user_prompt) and len(year_list) == 1:
        operator = '='
        filtered_data = filter_by_year(dataset, operator, year_list[0])

    elif re.search(r'\bafter\b', user_prompt) and len(year_list) == 1:
        operator = '>'
        filtered_data = filter_by_year(dataset, operator, year_list[0])

    elif re.search(r'\bbefore\b', user_prompt) and len(year_list) == 1:
        operator = '<'
        filtered_data = filter_by_year(dataset, operator, year_list[0])

    elif re.search(r'\bbetween\b', user_prompt) and len(year_list) == 2:
        filtered_data = filter_between_two_dates(dataset, year_list)

    return filtered_data
