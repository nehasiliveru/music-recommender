import pickle as pkl
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

# Load environment variables from key.env
load_dotenv("key.env")

# Get credentials securely
SPOTIFY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")

# Authenticate with Spotify API
client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Custom CSS for styling
st.markdown("""
    <style>
    /* Set full black background */
    .stApp {
        background: linear-gradient(to right, #ffdde1, #cfd9df) !important;
        color: black;
    }
    
    /* Improve select box visibility */
    .stSelectbox > div > div > input {
        color: black !important;
        font-weight: bold;
    }

    /* Styled Recommendation Button */
    .stButton>button {
        background-color: #1DB954;
        color: white;
        border-radius: 25px;
        padding: 12px 28px;
        border: none;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0px 4px 10px rgba(30, 215, 96, 0.5);
        transition: all 0.3s ease-in-out;
    }

    /* Hover effect for button */
    .stButton>button:hover {
        background-color: #1ed760;
        color: white;
        transform: scale(1.05);
        box-shadow: 0px 6px 15px rgba(30, 215, 96, 0.7);
    }

    /* Styling recommendation cards */
    .recommendation-card {
        background-color: transparent !important;
        border-radius: 12px;
        padding: 10px;
        transition: transform 0.3s ease-in-out, background-color 0.3s;
        box-shadow: none;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* Fix song title positioning */
    .song-title {
        font-size: 18px;
        font-weight: bold;
        margin-top: 5px;
        color: black !important;
        background: none !important;
        padding: 0;
    }

    .recommendation-card:hover {
        transform: scale(1.07);
        background-color: #282828;
        box-shadow: 0px 4px 12px rgba(255, 255, 255, 0.2);
    }

    /* Responsive layout for recommendations */
    @media (max-width: 768px) {
        .recommendation-card {
            padding: 10px;
            margin-bottom: 10px;
        }
    }
    
    h1 {
        color: black !important;
    }

    /* Center align footer text */
    .footer {
        text-align: center;
        color: #b3b3b3;
        font-size: 12px;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)


def get_track_info(song_name, artist_name):
    """Get track info including cover URL and preview URL"""
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        preview_url = track["preview_url"]
        spotify_url = track["external_urls"]["spotify"]
        return album_cover_url, preview_url, spotify_url
    else:
        default_image = "https://i.postimg.cc/0QNxYz4V/social.png"
        return default_image, None, None

def recommend(song):
    """Get recommendations for a given song"""
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_info = []
    
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        song_name = music.iloc[i[0]].song
        cover_url, preview_url, spotify_url = get_track_info(song_name, artist)
        recommended_music_info.append({
            'name': song_name,
            'artist': artist,
            'cover_url': cover_url,
            'preview_url': preview_url,
            'spotify_url': spotify_url
        })
    
    return recommended_music_info

# App Header
st.title('🎵 Music Recommender System')
st.markdown("Discover new music based on your favorite songs!")

# Load data
music = pkl.load(open('df.pkl','rb'))
similarity = pkl.load(open('similarity.pkl','rb'))

# Search box with better styling
music_list = music['song'].values
selected_song = st.selectbox(
    "Search for a song:",
    music_list,
    index=0,
    help="Type or select a song from the dropdown"
)

# Recommendation button
if st.button('Get Recommendations', key='recommend_btn'):
    with st.spinner('Finding similar songs...'):
        recommendations = recommend(selected_song)
    
    st.success("Here are some recommendations you might like:")
    
    # Display recommendations in columns
    cols = st.columns(5)
    for idx, rec in enumerate(recommendations):
        with cols[idx]:
            with st.container():
                st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
                
                # Album cover - using use_container_width instead of use_column_width
                st.image(rec['cover_url'], use_container_width=True)
                
                # Song and artist info
                st.markdown(f'<p class="song-title">{rec["name"]}</p>', unsafe_allow_html=True)
                st.caption(f'by {rec["artist"]}')                
                # Spotify link
                if rec['spotify_url']:
                    st.markdown(f'[🎧 Open in Spotify]({rec["spotify_url"]})', unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #b3b3b3; font-size: 12px;">
    Powered by Spotify API | Music data from the dataset
    </div>
    """, unsafe_allow_html=True)