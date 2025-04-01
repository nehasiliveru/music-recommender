# Music Recommendation System 🎵
This project is a Music Recommendation System that utilizes Natural Language Processing (NLP) and Machine Learning to suggest similar songs based on lyrics. 
The system processes song lyrics, cleans the text, and applies TF-IDF vectorization and cosine similarity to find relevant song recommendations.

Features:
Text Preprocessing: Converts lyrics to lowercase, removes special characters, and applies stemming.
TF-IDF Vectorization: Transforms lyrics into numerical vectors for similarity comparison.
Cosine Similarity: Measures the similarity between songs based on their lyrics.
Recommendation Function: Retrieves the top similar songs for a given input song.

Dataset:
The project uses a dataset of song lyrics from kaggle (Spotify_millsongdata).

Usage:
Preprocess the text data.
Generate TF-IDF vectors and compute similarity scores.
Use the recommender function to get song suggestions.

Dependencies:
Python
Pandas
NLTK
Scikit-learn
Pickle (for model storage)
