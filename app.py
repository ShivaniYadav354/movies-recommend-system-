

import streamlit as st
import pickle
import pandas as pd
import requests

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


#new
st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

#new


#new
# 2. PRO 3D & GLASSMORPHISM CSS
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #FFD700;
        text-shadow: 0 0 10px rgba(255, 215, 0, 0.5); /* Glowing yellow effect */
        
    }
    .movie-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
        min-height: 350px;
    }
    .movie-card:hover {
        transform: translateY(-10px) scale(1.05);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        border: 1px solid rgba(0, 255, 255, 0.3);
    }
    /* Targets the label text of the Selectbox */
    .stSelectbox label p {
        color: #FFFFFF !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.5); /* Soft white glow */
        font-family: 'Montserrat', sans-serif;
    }

    /* Targets the text inside the box (the selected movie) */
    .stSelectbox div[data-baseweb="select"] > div {
        color: red !important;
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 10px;
    }
    .movie-title {
        font-family: 'Montserrat', sans-serif !important;
        color: white  !important; /* Forces pure white */
        font-size: 16px !important;
        font-weight: 700 !important;
        /* Layered shadow for a soft neon glow */
        text-shadow: 0 0 5px #fff, 
                     0 0 10px #fff, 
                     0 0 20px #22d3ee; /* Light blue outer glow */
        line-height: 1.3;
        margin-top: 10px;
        display: block;
    }
    /* Custom Button Style */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #ff00cc, #3333ff);
        color: white;
        border-radius: 25px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    
    
    
    
    /* 1. ANIMATION FOR SMOOTH LOAD */
    @keyframes mainFadeIn {
        0% { opacity: 0; transform: scale(0.98); filter: blur(10px); }
        100% { opacity: 1; transform: scale(1); filter: blur(0); }
    }

    /* 2. THE BACKGROUND & CENTER GLOW */
    .stApp {
        background: radial-gradient(circle at center, #302b63 0%, #0f0c29 70%, #050505 100%);
        animation: mainFadeIn 1.8s ease-out;
        color: white;
    }

    /* 3. GLOWING CENTER OVERLAY (The 'Effect' you want) */
    .center-glow {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 600px;
        height: 600px;
        background: radial-gradient(circle, rgba(255, 0, 204, 0.15) 0%, rgba(51, 51, 255, 0) 70%);
        z-index: -1;
        pointer-events: none;
    }

    /* 4. GLOWING WHITE TITLES */
    .movie-title {
        font-family: 'Montserrat', sans-serif !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        text-align: center !important;
        text-shadow: 0 0 10px #fff, 0 0 20px rgba(255,255,255,0.5) !important;
        margin-top: 10px;
        display: block;
    }

    /* 5. 3D CARD HOVER */
    .movie-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .movie-card:hover {
        transform: translateY(-15px) scale(1.03);
        box-shadow: 0 15px 45px rgba(0, 0, 0, 0.8), 0 0 20px rgba(0, 210, 255, 0.3);
        border: 1px solid rgba(0, 210, 255, 0.5);
    }
    

    
    
    </style>
    """, unsafe_allow_html=True)





#new



def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=15947b846c83a28c2188dcc4128dff2a&language=en-US"
    response = requests.get(url)
    data = response.json()

    if data.get('poster_path') is None:
        return "https://via.placeholder.com/300x450?text=No+Poster"

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

#new

st.sidebar.title("🎥 Movie Recommender")
st.sidebar.markdown("""
Discover movies similar to your favorite ones  
Built using **Machine Learning & TMDB API**
""")

#new




def recommend (movie):
    movies_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movies_index]
    movies_list= sorted(list(enumerate(distance)) , reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies =[]
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters



movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

@st.cache_resource
def compute_similarity(movies):
    cv = CountVectorizer(max_features=5000, stop_words='english')
    vectors = cv.fit_transform(movies['tags']).toarray()
    return cosine_similarity(vectors)

similarity = compute_similarity(movies)







#new

st.markdown(
    "<h1 style='text-align: center;'>🎬 Movies Recommender System</h1>",
    unsafe_allow_html=True
)
st.markdown("<hr>", unsafe_allow_html=True)

#new


Selected_movie_name = st.selectbox(
    "🎞️ Select a movie you like",
    movies['title'].values
)

if st.button("✨ Recommend Movies"):
    # 1. Create the placeholder
    placeholder = st.empty()

    # 2. Show the centered text and blur
    placeholder.markdown("""
        <div class="blur-overlay">
            <div style="text-align: center;">
                <div style="font-size: 70px; margin-bottom: 20px; animation: spin 2s linear infinite;">🎬</div>
                <div class="loading-text">Finding best recommendations for you...</div>
            </div>
        </div>
        <style>
            @keyframes spin {
                from { transform: rotate(0deg); }
                to { transform: rotate(360deg); }
            }
        </style>
    """, unsafe_allow_html=True)

    # 3. Call your logic (Python waits here while the blur is visible)
    try:
        names, posters = recommend(Selected_movie_name)
    finally:
        placeholder.empty()


        cols = st.columns(5)
    for i in range(len(names)):
        with cols[i]:
            st.markdown(f"""
                    <div class="movie-card">
                        <img src="{posters[i]}" style="width:100%; border-radius:10px;">
                        <p class="movie-title">{names[i]}</p>
                    </div>
                """, unsafe_allow_html=True)



#new
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;'>Made with ❤️ using Streamlit & Machine Learning</p>",
    unsafe_allow_html=True
)
#new