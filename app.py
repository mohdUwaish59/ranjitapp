from flask import Flask, request, jsonify
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import pandas as pd
import random

# Load serialized model components
vectorizer = joblib.load('vectorizer.pkl')
vectors = joblib.load('vectors.pkl')
similarity = joblib.load('similarity.pkl')

app = Flask(__name__)


# Sample data for song names, artists, and genres
song_names = ["Shape of You", "Bohemian Rhapsody", "Thriller", "Billie Jean", "Stairway to Heaven",
              "Hotel California", "Rolling in the Deep", "Imagine", "Smells Like Teen Spirit", "Hey Jude",
              "Like a Rolling Stone", "Bohemian Like You", "Waterloo Sunset", "A Day in the Life", "Brown Sugar",
              "Sympathy for the Devil", "American Pie", "Good Vibrations", "What's Going On", "Wish You Were Here"]
artists = ["Ed Sheeran", "Queen", "Michael Jackson", "Michael Jackson", "Led Zeppelin",
           "Eagles", "Adele", "John Lennon", "Nirvana", "The Beatles",
           "Bob Dylan", "The Dandy Warhols", "The Kinks", "The Beatles", "The Rolling Stones",
           "The Rolling Stones", "Don McLean", "The Beach Boys", "Marvin Gaye", "Pink Floyd"]
genres = ["Pop", "Rock", "Pop", "Reverbe", "Rock",
          "Slow", "Pop", "Rock", "Grunge", "Rock",
          "Rock", "Rock", "Lofi", "Rock", "Rock",
          "Jazz", "Rock", "Pop", "R&B", "Jazz"]

# Generate dataset
data = []
for i in range(100):
    user_id = f"User_{i+1}"
    playlist = random.sample(list(zip(song_names, artists, artists, artists, genres)), 5)  # Shuffle the song data for each user
    for song_name, artist1, artist2, artist3, genre in playlist:
        data.append([user_id, song_name, artist1, artist2, artist3, genre])

# Create DataFrame
columns = ['userId', 'songname', 'artist1', 'artist2', 'artist3', 'genre']
df1 = pd.DataFrame(data, columns=columns)

# Save DataFrame to CSV
df1.to_csv('user_playlist_data.csv', index=False)
# Function to remove spaces from artist names
def remove_spaces(name):
    if isinstance(name, str):
        return ''.join(name.split())
    else:
        return ''

# Remove spaces from artist names
for col in ['artist1', 'artist2', 'artist3']:
    df1[col] = df1[col].apply(remove_spaces)

# Concatenating artist columns and genre for each user
df_grouped = df1.groupby('userId').agg({
    'songname': ' '.join,  # Take the first occurrence of songname
    'artist1': ' '.join,
    'artist2': ' '.join,
    'artist3': ' '.join,
    'genre': ' '.join  # Take the first occurrence of genre
}).reset_index()

# Concatenating columns into 'tags'
df_grouped['tags'] = df_grouped[['songname', 'artist1', 'artist2', 'artist3', 'genre']].apply(' '.join, axis=1)

# Selecting only 'userId' and 'tags' columns
new_df = df_grouped[['userId', 'tags']]


# Recommendation endpoint
@app.route("/recommendations", methods=["POST"])
def get_recommendations():
    # Get user_tags from the request body
    user_tags = request.json.get("user_tags", "")

    # Transform user_tags into vector using the loaded vectorizer
    user_vector = vectorizer.transform([user_tags]).toarray()

    # Calculate cosine similarity between user_vector and vectors
    user_similarity = cosine_similarity(user_vector, vectors)

    # Get indices of top similar users
    top_users_indices = user_similarity.argsort()[0][::-1][:10]

    # Get userIds and similarity scores of top similar users
    similar_users = [{"userId": new_df.iloc[i].userId, "similarity_score": user_similarity[0][i]} for i in top_users_indices]

    return jsonify({"recommendations": similar_users})

if __name__ == "__main__":
    app.run(debug=True)
