from flask import Flask, render_template, request
import pandas as pd
# Import des fonctions et variables des autres fichiers python
from filters import description_or_title
from functions import generate_final_recommendation
from model import modelBert

wiki_movie = pd.read_csv("wiki_movie_plots_embedding.csv")
app = Flask(__name__)


# route qui permet d'afficher la page 'index.html' qui contient le chatbot
@app.route('/')
def index():
    return render_template('index.html')


# route qui permet d'afficher la page 'dataset.html' qui contient un simple affichage du datset entier
@app.route('/dataset')
def data():
    return render_template('dataset.html', dataset=wiki_movie)


# route qui permet de récuperer le type de filtre choisi par l'utilisateur (titre ou description)
@app.route("/get_movie_filter", methods=["GET", "POST"])
def description_extraction():
    # Recuperation de la variable 'filter'
    query_filter = request.form["filter"]
    # Fonction qui extrait "description" ou "titre"
    query_filter = description_or_title(query_filter)
    return query_filter


# route qui permet de récuperer l'ensemble des entrées de l'utilisateur
@app.route("/get_movie", methods=["GET", "POST"])
def film():
    query_filter = request.form["filter"]
    genre = request.form["genre"]
    year = request.form["year"]
    query = request.form["query"]
    # Pour le debugage
    print(query_filter)
    print(genre)
    print(year)
    print(query)

    # Envoie des variables à la fonction generate_final_recommendation afin de filtrer et trouver des recomandations
    recommandation = generate_final_recommendation(modelBert, wiki_movie, query_filter, genre, year, query)

    # Recperation de la recommandations dans l'html pour affichage
    return recommandation


if __name__ == '__main__':
    app.run(debug=True)
