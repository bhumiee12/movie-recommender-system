import pandas as pd
import requests
import pickle

# Your TMDB API Key (this is the public key you're using in app.py too)
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

def fetch_movie_details(movie_id):
    """Fetch genres from TMDB API for a given movie ID."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()

    # Extract genre names from API response
    genres = [genre['name'] for genre in data.get('genres', [])]
    print(f"Fetched genres for movie_id {movie_id}: {genres}")
    return genres

# Step 1: Load movies dataset
print("Reading tmdb_5000_movies.csv...")
movies = pd.read_csv('tmdb_5000_movies.csv')
print(f"Loaded {len(movies)} movies.")

# Step 2: Fetch genres for each movie
print("Fetching genres for each movie (this may take a while)...")
movies['genres'] = movies['id'].apply(fetch_movie_details)

# Step 3: Keep only relevant columns and save as pickle
movies = movies[['id', 'title', 'genres']].rename(columns={'id': 'movie_id'})

# Save to pickle file for app.py to use
movies.to_pickle('movie_list_with_genres.pkl')

print("✅ Successfully saved 'movie_list_with_genres.pkl' with genres included.")
