import pickle
import streamlit as st
import requests
import pandas as pd

# Fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path', '')
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return ""

# Fetch movie trailer
def fetch_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    videos = data.get('results', [])

    for video in videos:
        if video['site'].lower() == 'youtube' and video['type'].lower() == 'trailer':
            return f"https://www.youtube.com/watch?v={video['key']}"

    return None  # No trailer found

# Recommend movies
def recommend(movie, genre_filter=None):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_trailers = []

    for i in distances[1:]:
        movie_data = movies.iloc[i[0]]
        movie_id = movie_data.movie_id
        movie_title = movie_data.title
        movie_genres = movie_data.genres

        # Apply genre filter if selected
        if genre_filter and not any(g in genre_filter for g in movie_genres):
            continue

        recommended_movie_names.append(movie_title)
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_trailers.append(fetch_trailer(movie_id))

        if len(recommended_movie_names) == 5:
            break

    return recommended_movie_names, recommended_movie_posters, recommended_movie_trailers


# Streamlit UI
st.header('🎥 Movie Recommender System ')

# Load data (Make sure `prepare_data.py` created this correctly)
movies = pickle.load(open('movie_list_with_genres.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Collect all genres
all_genres = set()
for genres in movies['genres']:
    all_genres.update(genres)

# Genre filter in sidebar
genre_filter = st.multiselect(
    "Filter by Genre (Optional)",
    sorted(list(all_genres))
)

# Movie selection dropdown
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Show recommendations
if st.button('Show Recommendations'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_trailers = recommend(selected_movie, genre_filter)

    if recommended_movie_names:
        cols = st.columns(5)
        for idx, (name, poster, trailer) in enumerate(zip(recommended_movie_names, recommended_movie_posters, recommended_movie_trailers)):
            with cols[idx]:
                st.text(name)
                st.image(poster)
                if trailer:
                    st.markdown(f"[🎬 Watch Trailer](<{trailer}>)", unsafe_allow_html=True)
                else:
                    st.write("Trailer Not Available")
    else:
        st.warning("No recommendations found matching your genre filter.")
