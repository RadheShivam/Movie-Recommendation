import streamlit as st
import pickle
import pandas as pd
import requests

# Fetch the TMDB API key from Streamlit secrets
tmdb_api_key = st.secrets["api_keys"]["tmdb_api_key"]


# Function to fetch the poster for a given movie ID
def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={tmdb_api_key}')
    data = response.json()

    return 'https://image.tmdb.org/t/p/w500' + data['poster_path']


# Updated recommendation function to fetch titles and posters
def recommend(movie):
    # Get the index of the selected movie
    movie_index = movies[movies['title'] == movie].index[0]

    # Get the similarity distances for the movie
    distances = similarity_matrix[movie_index]

    # Get top 5 similar movies (excluding the movie itself)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        # Append the movie title
        recommended_movies.append(movies.iloc[i[0]]['title'])

        # Get the movie ID from the movies DataFrame
        movie_id = movies.iloc[i[0]]['id']

        # Fetch and append the movie poster
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster


# Load movies and similarity matrix from pickle files
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity_matrix = pickle.load(open('similarity_matrix.pkl', 'rb'))

# Streamlit app UI
st.title('Movie Recommender System')

# Extract the 'title' values from the `movies` DataFrame and pass it to the selectbox
selected_movie_name = st.selectbox(
    "Select a movie:",
    movies['title'].values
)

# Recommend movies when the button is pressed
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])

st.write(f"You selected: {selected_movie_name}")
