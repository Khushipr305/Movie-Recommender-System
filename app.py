import streamlit as st
import pickle
import requests
import time

st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)
with st.sidebar:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/3418/3418886.png",
        width=120
    )

    st.title("🎥 About")

    st.write(
        "AI-powered movie recommendation system using "
        "content-based filtering and cosine similarity."
    )

    st.markdown("---")

    st.info(
        "Select a movie and get similar recommendations instantly."
    )

st.markdown("""
<style>
.main {
    background-color: #0E1117;
}

h1 {
    color: #FF4B4B;
    text-align: center;
    font-size: 5rem;
}

.stButton > button {
    background: linear-gradient(90deg, #FF512F, #DD2476);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 25px;
    font-weight: bold;
    width: 100%;
}

.stButton > button:hover {
    transform: scale(1.05);
    transition: 0.3s;
}

.movie-card {
    background-color: #1C1F26;
    padding: 15px;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 4px 10px rgba(255,75,75,0.3);
    transition: all 0.3s ease;
    cursor: pointer;
}

.movie-card:hover {
    transform: scale(1.08);
    box-shadow:
        0 0 10px rgba(229,9,20,0.5),
        0 0 20px rgba(229,9,20,0.4),
        0 0 30px rgba(229,9,20,0.3);
}

.stImage img {
    border-radius: 25px;
    transition: all 0.9s ease;
}

.stImage img:hover {
    transform: scale(1.75);
}

.movie-title {
    color: white;
    font-weight: bold;
    font-size: 20px;
    margin-top: 5px;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #0E1117;
    color: white;
    text-align: center;
    padding: 10px;
    font-size: 15px;
    border-top: 1px solid #333;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=9ce5a40833b3ace8565886d23890349a&language=en'.format(movie_id))
    timeout = 1
    data = response.json()

    if data.get('poster_path'):
        return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

    return "https://via.placeholder.com/300x450?text=Movie"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters

movies = pickle.load(open('movies.pkl', 'rb'))



similarity = pickle.load(open('similarity.pkl', 'rb'))

st.markdown("""
<h1>🎬 Movie Recommender System</h1>
""", unsafe_allow_html=True)

st.markdown(
    """
    <p style="
        text-align:center;
        color:#FFD700;
        font-size:28px;
        font-weight:bold;
        margin-top:-10px;
        margin-bottom:30px;
    ">
        Discover your next favorite movie 🎥
    </p>
    """,
    unsafe_allow_html=True
)

selected_movie_name = st.selectbox(
    'Select Movie Name',
    movies['title'].values
)

if st.button('✨ Recommend Movies'):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.header(names[0])
        st.image(posters[0])
    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])
    with col4:
        st.header(names[3])
        st.image(posters[3])
    with col5:
        st.header(names[4])
        st.image(posters[4])

start = time.time()
names, posters = recommend(selected_movie_name)
print("Time:", time.time() - start)


st.markdown("""
<div class="footer">
    © 2026 Khushi | Movie Recommender System | All Rights Reserved
</div>
""", unsafe_allow_html=True)

