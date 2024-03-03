import streamlit as st
import pickle
import pandas as pd

# Load the movies DataFrame
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load the similarity matrix
similarity = pickle.load(open('movies_similar.pkl', 'rb'))

# HTML and CSS for the moving background with light blue color
background_html = """
<style>
    body {
        background-color: #ADD8E6; /* Light blue color */
        animation: slide 20s linear infinite;
    }

    @keyframes slide {
        0% {
            background-position-x: 0%;
        }
        100% {
            background-position-x: 100%;
        }
    }

    .content {
        color: white;
        text-align: center;
        padding: 20px;
    }
</style>
"""

# Display the HTML
st.markdown(background_html, unsafe_allow_html=True)

# Title of the web app
st.title('Movie Recommender System')

# Dropdown to select a movie
selected_movie_name = st.selectbox('', movies['Series_Title'])

# Function to recommend similar movies
def recommend(movie):
    movie_index = movies[movies['Series_Title'] == movie].index[0]
    distance = similarity[movie_index]
    movies_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    for i in movies_list:
        movie_name = movies.iloc[i[0]].Series_Title
        recommend_movies.append(movie_name)
    return recommend_movies

# Button to trigger the recommendation
if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    if recommendations:
        for index, name in enumerate(recommendations, start=1):
            st.header(f"{index}. {name}")
    else:
        st.write("No recommendations found.")
