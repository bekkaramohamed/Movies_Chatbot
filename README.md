🎬 MOVIE RECOMMENDATION CHATBOT PROJECT

🎯 INTRODUCTION
The goal of this project is to create a conversational system that can recommend movies based on a reference film or a description provided by the user.


📋 OBJECTIVES
The main objectives of this project are:

Develop a chatbot that recommends movies based on user input.
Utilize NLP techniques to process and understand user queries.
Implement machine learning models to generate movie recommendations.

💻 TECHNOLOGY STACK
Google Colab: Used as the development environment for running Python code and Jupyter notebooks.
Flask: Used to create the web interface for the chatbot.

📂 DATASET
The dataset used is the Wikipedia Movie Plots dataset, which contains descriptions of 34,886 movies. The columns include:

Release Year: Year of release
Title: Title of the movie
Origin/Ethnicity: Origin of the movie
Director: Director(s) of the movie
Cast: Main actors and actresses
Genre: Genre(s) of the movie
Wiki Page: URL of the Wikipedia page
Plot: Detailed description of the movie plot
🔍 DATA PREPROCESSING
The preprocessing steps include:

Special Character Removal: Remove non-alphanumeric characters.
Lowercasing: Convert all text to lowercase.
Stop Words Removal: Remove common words that do not add value.
Lemmatization: Convert words to their base forms.
Tokenization: Split text into meaningful tokens.
BERT Embeddings: Encode movie descriptions using the BERT model to generate vector representations.
Preprocessing was essential for the application of Word2Vec, as this model cannot directly process strings. Word2Vec requires a representation in the form of a list of single-character tokens for each document.

To improve the quality of our data, we implemented a preprocessing step by creating an additional column named 'Plot_embedding'. This column contains the movie descriptions encoded using the BERT model. The purpose of this approach was to generate vector representations for each description. These representations were used to calculate similarities between descriptions.

📝 PROJECT OVERVIEW
The project focuses on movie recommendation, where the chatbot suggests movies similar to the description or reference given by the user. To achieve this, it is essential to create vector representations for each movie in the dataset. This section discusses two models used for creating these embeddings: Word2Vec and BERT.

🔡 WORD2VEC
Model Training:

python
Copier le code
model = Word2Vec(plot_tokenized, vector_size=100, window=5, sg=0, negative=5, min_count=1, workers=4)
Loads and trains the Word2Vec model on tokenized movie descriptions.
Key parameters include vector size, context window, model type (Skip-Gram), negative sampling, minimum word frequency, and the number of worker threads.
The model is saved using model.save().
Similarity Calculation:

Model_similarity(myModel, tokens1, tokens2): This function calculates the similarity between two lists of tokens using the Word Mover's Distance (WMD) with Word2Vec.
Movie Recommendation:

get_top_k_similar_movies_from_reference(myModel, dataset, reference_line, k=5): Extracts the tokenized description from the reference and calculates similarity scores between the reference and other movies in the dataset. It then sorts and returns the top k most similar movies.

🧠 BERT
Loading NLP Models:

nlp = spacy.load('en_core_web_sm'): Loads SpaCy's NLP model for text processing.
modelBert = SentenceTransformer('all-MiniLM-L6-v2'): Loads the pre-trained SentenceTransformer model for sentence embeddings.
Similarity Calculation:

find_k_films_bert_similarity_with_user_desc(model, dataset, user_desc, k=5): Encodes the user's description using the SentenceTransformer model and calculates cosine similarity between the reference and each movie plot in the dataset. It then sorts and returns the top k most similar movies.
👤 USER INPUT PROCESSING
To process user input (either movie description or title), the following steps are taken:

Retrieve variables from the user interface:

query_filter, genre, year, and query.
Filter the dataset using functions from filters.py:

description_or_title(user_prompt): Determines if the input is a description or a title.
filter_by_reference_title(dataset, user_title_ref): Filters dataset by movie title.
filter_by_genre_film(dataset, user_genre_ref_list): Filters dataset by movie genres.
filter_by_year(dataset, operator, year): Filters dataset by release year.
filter_between_two_dates(dataset, list_of_dates): Filters dataset by a range of years.
get_information_operator_and_year_from_prompt(dataset, user_prompt): Extracts comparison operator and year from user prompt.
extract_user_prompt_information(dataset, user_description): Extracts relevant information from a user-provided description.
🏆 RECOMMENDATION FORMULATION
For text generation, the GPT-2 model is used due to its ability to generate coherent and semantically rich text. The function generate_response_with_gpt2 handles this task, taking the GPT-2 model, tokenizer, and maximum length as parameters.

The function generate_final_recommendation(bert_model, gpt2_model, dataset, filter, genre, year, user_query) generates personalized movie recommendations using BERT and GPT-2 models. The process involves:

Defining a filtered dataset based on user parameters.
Finding the most similar movies based on either a title or description.
Formatting the results and using GPT-2 to generate a contextualized response for the user.


Flask Application : 
![image](https://github.com/bekkaramohamed/Movies_Chatbot/assets/62758785/7c6dd629-e2ea-480f-9200-0640eb87120f)

By Reference Title :
![image](https://github.com/bekkaramohamed/Movies_Chatbot/assets/62758785/adefd544-4239-43e2-8372-ca9aecca41c0)
![image](https://github.com/bekkaramohamed/Movies_Chatbot/assets/62758785/09209ea2-8845-46af-8c38-73891b66231e)


By Description : 
![image](https://github.com/bekkaramohamed/Movies_Chatbot/assets/62758785/1244d3a8-6c87-41aa-b85c-4431a34f0ccf)
![image](https://github.com/bekkaramohamed/Movies_Chatbot/assets/62758785/c25e8be2-9d50-4fe2-ac19-d7d0466f7ea5)
![image](https://github.com/bekkaramohamed/Movies_Chatbot/assets/62758785/7d268005-c135-4871-b4fb-31853fca68d4)



🌐 FLASK APPLICATION
Our Flask application uses HTML templates (in the templates folder) to display chatbot messages and integrates CSS and images (in the static folder) for styling. The app.py file connects these HTML templates to the Python code, which contains our model and various filtering and recommendation generation functions.

🚪 MAIN ROUTES

![image](https://github.com/bekkaramohamed/Movies_Chatbot/assets/62758785/9372cfdc-772b-4a1a-ab11-aed28c6d479c)

Home Page (/)
The root route displays the chatbot interface, allowing users to interact with the recommendation system by specifying their movie preferences.

Dataset Display (/dataset)
This route allows users to view the entire dataset used by the model, providing transparency on the data used for recommendations.

Filter Extraction (/get_movie_filter)
This route retrieves the filter type (title or description) chosen by the user from a POST request. The description_extraction function extracts and returns the filter type.

User Input Retrieval (/get_movie)
This route collects all user inputs, including the filter type, genre, year, and user query. These inputs are then used to generate movie recommendations via the generate_final_recommendation function.

Using Flask provides a smooth user experience, allowing users to interact with the chatbot and receive personalized movie recommendations based on their preferences.


Diagram : 

![image](https://github.com/bekkaramohamed/Movies_Chatbot/assets/62758785/8d9b37e8-a4bd-4aba-afb5-325ec0fbe72c)

