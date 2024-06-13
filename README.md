💻 Installation :
* Clone this repository by using git clone https://github.com/YOUR-USERNAME/https://github.com/bekkaramohamed/Movies_Chatbot
* Run pip install -r requirements.txt
* Run python app.py

💡 App functionality
* You can choose to upload a file from the folder 'image_a_detectee', and you will get the output in the file 'image_detectee'
* You can choose to run in live streaming with your webcam to detect real time waste

🎯 INTRODUCTION : 
The goal of this project is to create a conversational system that can recommend movies based on a reference film or a description provided by the user.

📋 OBJECTIVES : 

- Develop a chatbot that recommends movies based on user input.
- Utilize NLP techniques to process and understand user queries.
- Implement machine learning models to generate movie recommendations.

📂 DATASET : 
The dataset used is the Wikipedia Movie Plots dataset, which contains descriptions of 34,886 movies.

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




