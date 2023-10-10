import streamlit as st
import pandas as pd
import pickle
import requests

#imdb url
tmdb_url = "https://api.themoviedb.org/3/movie/movie_id?language=en-US"
tmdb_poster_base = "https://image.tmdb.org/t/p/w500/"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyN2FhYzE3MTE1OGQ3NThjZDljN2E0MmExYzcxYmM0NSIsInN1YiI6IjYxYjk3ZWZkODczZjAwMDA0MmI2NjE1NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.96Pvnhh3nS2D4jAx4RSO3OglzWBSEf8FYmPahvKwSAU"
}

# fetch posters
def fetch_posters(movie_id):
    new_url = tmdb_url.replace("movie_id", str(movie_id))
    response = requests.get(new_url, headers=headers)
    data = response.json()
    return  tmdb_poster_base + data['poster_path']


# recommend movies, fetch top 5 similar movies
def recommend_movies(movie):
    index = movies_df[movies_df["title"] == movie].index[0]
    distances = similarity[index]
    rec_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:10]

    recommended_movies = []
    movie_posters = []
    for item in rec_movies:
        recommended_movies.append(movies_df.iloc[item[0]].title)
        movie_posters.append(fetch_posters(movies_df.iloc[item[0]].movie_id))
    return recommended_movies, movie_posters

# make movie dictionary from file pickle file
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies_df = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

selected_movie = st.selectbox(
    "Search for a movie...",
    movies_df["title"].values
)

if st.button("Recommend"):
    movies, posters = recommend_movies(selected_movie)

    img_row = 3
    col1, col2, col3 = st.columns(img_row)
    for idx, (movie, poster) in enumerate(zip(movies, posters)):
        if idx % img_row == 0:
            with col1:
                st.text(movie)
                st.image(poster)
        elif idx % img_row == 1:
            with col2:
                st.text(movie)
                st.image(poster)
        else:
            with col3:
                st.text(movie)
                st.image(poster)