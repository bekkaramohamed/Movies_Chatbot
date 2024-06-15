🎯 INTRODUCTION : 
The goal of this project is to create a conversational system that can recommend movies based on a reference film or a description provided by the user.

📋 OBJECTIVES : 

- Develop a chatbot that recommends movies based on user input.
- Utilize NLP techniques to process and understand user queries.
- Implement machine learning models to generate movie recommendations.

📂 DATASET : 
The dataset used is the Wikipedia Movie Plots dataset, which contains descriptions of 34,886 movies.

💻 Installation :
* Clone this repository by using git clone https://github.com/YOUR-USERNAME/https://github.com/bekkaramohamed/Movies_Chatbot
* Run pip install -r requirements.txt
* Run python app.py

💡 App functionality
* You can choose to provide the chatbot with a movie title or a description to get a recommendation for a similar movie.

🤖 Chatbot : 
![exemple](https://github.com/bekkaramohamed/Movies_Chatbot/assets/62758785/62b01d4f-9316-4e7f-a3b0-65ff31a74f13)

🚪 MAIN ROUTES : 

* Home Page (/)
The root route displays the chatbot interface, allowing users to interact with the recommendation system by specifying their movie preferences.

* Dataset Display (/dataset)
This route allows users to view the entire dataset used by the model, providing transparency on the data used for recommendations.

* Filter Extraction (/get_movie_filter)
This route retrieves the filter type (title or description) chosen by the user from a POST request. The description_extraction function extracts and returns the filter type.

* User Input Retrieval (/get_movie)
This route collects all user inputs, including the filter type, genre, year, and user query. These inputs are then used to generate movie recommendations via the generate_final_recommendation function.

📊 Diagram : 

![image](https://github.com/bekkaramohamed/Movies_Chatbot/assets/62758785/15c5df41-ba4c-4a33-ace4-05a88038fcd4)




