import streamlit as st
import pandas as pd
import re
import os
import base64
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Konfigurasi halaman
st.set_page_config(
    page_title="Penelusuran Artikel Hewan",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS Modern dengan Background Dinamis


def _encode_image(path):
    """Encode image file to base64 data URL."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"url('data:image/jpeg;base64,{data}')"
    return None


# Pre-load kedua background
_bg_search = _encode_image("templates/assets/background.jpg")
_bg_results = _encode_image("templates/assets/background2.jpg")

# Pre-load logo


def _encode_logo(path):
    """Encode logo to base64 for inline display."""
    if os.path.exists(path):
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{data}"
    return None


_logo_data = _encode_logo("templates/assets/logo.png")

# Fallback gradient jika gambar tidak ditemukan
_gradient_fallback = "linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%)"

# Initialize session state EARLY
if 'page' not in st.session_state:
    st.session_state.page = 1
if 'search_performed' not in st.session_state:
    st.session_state.search_performed = False

# Pilih background berdasarkan state
if st.session_state.search_performed:
    _current_bg = _bg_results if _bg_results else _gradient_fallback
else:
    _current_bg = _bg_search if _bg_search else _gradient_fallback

st.markdown(f"""
<style>
    /* Import Poppins Font */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* CSS Variables */
    :root {{
        --primary-orange: #FF6B35;
        --secondary-orange: #FF8C42;
        --accent-coral: #FF7F50;
        --glass-white: rgba(255, 255, 255, 0.25);
        --glass-border: rgba(255, 255, 255, 0.18);
        --text-dark: #2D2D3A;
        --text-medium: #4A4A5C;
        --text-light: #6E6E80;
    }}
    
    /* Animations */
    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(30px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translateY(0px); }}
        50% {{ transform: translateY(-8px); }}
    }}
    
    @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    
    @keyframes pulseGlow {{
        0%, 100% {{ box-shadow: 0 8px 40px rgba(255, 107, 53, 0.2); }}
        50% {{ box-shadow: 0 8px 60px rgba(255, 107, 53, 0.35); }}
    }}
    
    /* App Background */
    .stApp {{
        background: {_current_bg} no-repeat center center fixed;
        background-size: cover;
        font-family: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
        min-height: 100vh;
    }}
    
    /* Very subtle overlay - let background shine */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            180deg, 
            rgba(0, 0, 0, 0.15) 0%, 
            rgba(0, 0, 0, 0.1) 50%,
            rgba(0, 0, 0, 0.2) 100%
        );
        pointer-events: none;
        z-index: 0;
    }}
    
    /* Main Header - Premium Glassmorphism */
    .main-header {{
        text-align: center;
        padding: 3.5rem 3rem;
        margin-bottom: 2.5rem;
        background: rgba(255, 255, 255, 0.15);
        border-radius: 32px;
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            inset 0 0 0 1px rgba(255, 255, 255, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.25);
        position: relative;
        z-index: 1;
        animation: fadeInUp 0.8s ease-out;
        overflow: hidden;
    }}
    
    .main-header::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 200%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
        animation: shimmer 3s ease-in-out infinite;
    }}
    
    .main-header::after {{
        content: '';
        position: absolute;
        bottom: 0;
        left: 50%;
        transform: translateX(-50%);
        width: 80%;
        height: 3px;
        background: linear-gradient(90deg, transparent, #FF6B35, #FF8C42, transparent);
        border-radius: 2px;
    }}
    
    .main-title {{
        font-family: 'Poppins', sans-serif;
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 50%, #FF7F50 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.75rem;
        letter-spacing: -1px;
        line-height: 1.1;
        text-shadow: 0 4px 30px rgba(255, 107, 53, 0.3);
        position: relative;
    }}
    
    .main-subtitle {{
        font-size: 1.15rem;
        color: rgba(255, 255, 255, 0.9);
        font-weight: 400;
        letter-spacing: 0.5px;
        line-height: 1.6;
        text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }}
    
    .logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 0.5rem;
    }}
    
    .logo-container img {{
        max-height: 100px;
        width: auto;
        transition: transform 0.3s ease;
    }}
    
    .logo-container img:hover {{
        transform: scale(1.05);
    }}
    
    /* Search Box - Premium Glassmorphism */
    .stTextInput {{
        position: relative;
    }}
    
    .stTextInput > div {{
        background: transparent !important;
    }}
    
    .stTextInput > div > div {{
        background: rgba(255, 255, 255, 0.12) !important;
        border-radius: 24px !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.15),
            inset 0 0 0 1px rgba(255, 255, 255, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        padding: 0.25rem !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    
    .stTextInput > div > div:hover {{
        background: rgba(255, 255, 255, 0.18) !important;
        border-color: rgba(255, 107, 53, 0.3) !important;
        box-shadow: 
            0 12px 40px rgba(0, 0, 0, 0.2),
            0 0 0 1px rgba(255, 107, 53, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.25) !important;
    }}
    
    .stTextInput > div > div:focus-within {{
        background: rgba(255, 255, 255, 0.22) !important;
        border-color: rgba(255, 107, 53, 0.5) !important;
        box-shadow: 
            0 12px 48px rgba(255, 107, 53, 0.2),
            0 0 0 3px rgba(255, 107, 53, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.3) !important;
    }}
    
    .stTextInput > div > div > input {{
        background: transparent !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 1.1rem 1.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        font-family: 'Poppins', sans-serif !important;
        color: #FFFFFF !important;
        box-shadow: none !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput > div > div > input::placeholder {{
        color: rgba(255, 255, 255, 0.5) !important;
        font-weight: 400 !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        box-shadow: none !important;
        outline: none !important;
    }}
    
    /* Radio Button - Glassmorphism */
    .stRadio > label {{
        color: rgba(255, 255, 255, 0.8);
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }}
    
    .stRadio > div {{
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 16px;
        padding: 1rem 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        transition: all 0.3s ease;
    }}
    
    .stRadio > div:hover {{
        border-color: rgba(255, 107, 53, 0.4);
        background: rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(255, 107, 53, 0.1);
    }}
    
    .stRadio > div label {{
        color: rgba(255, 255, 255, 0.95) !important;
        font-weight: 500;
        font-size: 0.95rem;
    }}
    
    /* Button - Premium Gradient */
    .stButton > button {{
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 50%, #FF7F50 100%);
        background-size: 200% 200%;
        color: #FFFFFF;
        border: none;
        border-radius: 20px;
        padding: 1.1rem 2.5rem;
        font-size: 1.05rem;
        font-weight: 600;
        font-family: 'Poppins', sans-serif;
        letter-spacing: 1px;
        box-shadow: 
            0 8px 30px rgba(255, 107, 53, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
        position: relative;
        overflow: hidden;
        animation: pulseGlow 3s ease-in-out infinite;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.6s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px) scale(1.02);
        box-shadow: 
            0 12px 40px rgba(255, 107, 53, 0.5),
            0 4px 15px rgba(0, 0, 0, 0.2);
        background-position: right center;
    }}
    
    .stButton > button:hover::before {{
        left: 100%;
    }}
    
    .stButton > button:active {{
        transform: translateY(-1px) scale(1.01);
    }}
    
    /* Result Cards - True Glassmorphism */
    .result-card {{
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 24px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.12),
            inset 0 0 0 1px rgba(255, 255, 255, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .result-card::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: linear-gradient(180deg, #FF6B35, #FF8C42, #FF7F50);
        border-radius: 4px 0 0 4px;
        opacity: 0;
        transition: opacity 0.4s ease;
    }}
    
    .result-card:hover {{
        transform: translateY(-6px);
        background: rgba(255, 255, 255, 0.18);
        border-color: rgba(255, 107, 53, 0.3);
        box-shadow: 
            0 20px 50px rgba(0, 0, 0, 0.2),
            0 0 0 1px rgba(255, 107, 53, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.4);
    }}
    
    .result-card:hover::before {{
        opacity: 1;
    }}
    
    .result-title {{
        color: #FFFFFF;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.6rem;
        letter-spacing: -0.3px;
        transition: all 0.3s ease;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }}
    
    .result-title:hover {{
        color: #FF8C42;
    }}
    
    .result-content {{
        color: rgba(255, 255, 255, 0.8);
        font-size: 0.95rem;
        line-height: 1.75;
        margin-bottom: 1rem;
    }}
    
    .result-meta {{
        color: #6B6B80;
        font-size: 0.85rem;
        font-weight: 500;
    }}
    
    .result-score {{
        background: linear-gradient(135deg, rgba(255, 107, 53, 0.15), rgba(255, 140, 66, 0.15));
        color: #FF8C42;
        padding: 0.5rem 1rem;
        border-radius: 10px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
        border: 1px solid rgba(255, 107, 53, 0.2);
        font-family: 'JetBrains Mono', monospace;
    }}
    
    /* Image Styling */
    .result-image {{
        border-radius: 14px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.05);
    }}
    
    /* Links - Orange Accent */
    a {{
        color: #FF6B35;
        text-decoration: none;
        transition: all 0.2s ease;
        font-weight: 500;
    }}
    
    a:hover {{
        color: #FF8C42;
        text-decoration: none;
    }}
    
    /* Stats Box - Glassmorphism */
    .stats-box {{
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(20px) saturate(180%);
        -webkit-backdrop-filter: blur(20px) saturate(180%);
        border-radius: 20px;
        padding: 1.75rem 2.5rem;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.1),
            inset 0 0 0 1px rgba(255, 255, 255, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.18);
        position: relative;
        z-index: 1;
        animation: fadeInUp 0.6s ease-out;
    }}
    
    .stats-box h3 {{
        font-size: 1.35rem;
        margin-bottom: 0.4rem;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.2px;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }}
    
    .stats-box p {{
        font-size: 0.95rem;
        color: rgba(255, 255, 255, 0.75);
        font-weight: 400;
    }}
    
    /* Divider - Subtle */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            rgba(255, 255, 255, 0.08) 20%, 
            rgba(255, 255, 255, 0.08) 80%, 
            transparent 100%);
        margin: 1.5rem 0;
    }}
    
    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Streamlit elements override */
    .stMarkdown {{
        position: relative;
        z-index: 1;
    }}
    
    .block-container {{
        position: relative;
        z-index: 1;
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }}
    
    /* Column styling */
    [data-testid="column"] {{
        position: relative;
        z-index: 1;
        animation: fadeInUp 0.5s ease-out;
    }}
    
    /* Image container - Glassmorphism */
    [data-testid="stImage"] {{
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 
            0 8px 32px rgba(0, 0, 0, 0.25),
            inset 0 0 0 1px rgba(255, 255, 255, 0.1);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }}
    
    [data-testid="stImage"]:hover {{
        transform: scale(1.02);
        box-shadow: 0 12px 36px rgba(0, 0, 0, 0.4);
        border-color: rgba(255, 107, 53, 0.2);
    }}
    
    /* Scrollbar - Minimal Dark */
    ::-webkit-scrollbar {{
        width: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(15, 15, 20, 0.5);
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: rgba(255, 107, 53, 0.3);
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(255, 107, 53, 0.5);
    }}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .main-title {{
            font-size: 2rem;
        }}
        .main-subtitle {{
            font-size: 0.95rem;
        }}
        .main-header {{
            padding: 2rem 1.5rem;
            border-radius: 18px;
        }}
        .result-card {{
            padding: 1.25rem;
            border-radius: 16px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# Inisialisasi stemmer Sastrawi


@st.cache_resource
def load_stemmer():
    factory = StemmerFactory()
    return factory.create_stemmer()


stemmer = load_stemmer()

# Load data


@st.cache_data
def load_data():
    df = pd.read_csv("cleaned_hewania_articles_tokenized.csv")
    df.fillna("", inplace=True)
    df["combined"] = df["Judul_Cleaned"] + " " + df["Content_Cleaned"]
    return df


df = load_data()

# Load stopwords


@st.cache_data
def load_stopwords():
    with open("stopword.txt", "r") as file:
        return set(file.read().splitlines())


stopwords = load_stopwords()

# Fungsi preprocessing


def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\d+", "", text)
    tokens = text.split()
    tokens = [word for word in tokens if word not in stopwords]
    return " ".join(tokens)

# Fungsi untuk melakukan stemming pada query


def stem_query(query):
    return stemmer.stem(query)

# Fungsi Cosine Similarity


def get_cosine_similarity(query, top_n=30):
    query = preprocess_text(query)
    query = stem_query(query)
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([query] + df["combined"].tolist())
    cosine_sim = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    results = []
    for idx, cosine_score in enumerate(cosine_sim):
        if cosine_score > 0:
            results.append({
                "index": idx,
                "title": df.loc[idx, "Judul"],
                "link": df.loc[idx, "Link"],
                "date": df.loc[idx, "Tanggal"],
                "content": df.loc[idx, "Content"][:200] + "...",
                "image": df.loc[idx, "Image URL"],
                "score": cosine_score,
            })

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:top_n]

# Fungsi Jaccard Similarity


def get_jaccard_similarity(query, top_n=30):
    query = preprocess_text(query)
    query = stem_query(query)
    query_tokens = set(query.split())

    results = []
    for idx, row in df.iterrows():
        doc_tokens = set(preprocess_text(row["combined"]).split())
        intersection = len(query_tokens & doc_tokens)
        union = len(query_tokens | doc_tokens)
        jaccard_score = intersection / union if union != 0 else 0

        if jaccard_score > 0:
            results.append({
                "index": idx,
                "title": row["Judul"],
                "link": row["Link"],
                "date": row["Tanggal"],
                "content": row["Content"][:200] + "...",
                "image": row["Image URL"],
                "score": jaccard_score,
            })

    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:top_n]


# Header with logo from assets
_logo_html = f'<img src="{_logo_data}" alt="Logo" style="height: 100px; margin-bottom: 1rem; filter: drop-shadow(0 4px 20px rgba(255, 107, 53, 0.3));">' if _logo_data else '🐱 🐾 🐶'

st.markdown(f"""
<div class="main-header">
    <div class="logo-container">{_logo_html}</div>
    <p class="main-subtitle">Mesin pencari artikel hewan peliharaan dengan teknologi Machine Learning</p>
</div>
""", unsafe_allow_html=True)

# Search Interface
col1, col2, col3 = st.columns([1, 3, 1])

with col2:
    query = st.text_input(
        "Pencarian", placeholder="Cari artikel tentang hewan peliharaan...", label_visibility="collapsed")

    col_algo1, col_algo2 = st.columns(2)
    with col_algo1:
        algorithm = st.radio(
            "Pilih Algoritma Pencarian:",
            options=["Cosine Similarity", "Jaccard Similarity"],
            index=0,
            horizontal=True
        )

    search_button = st.button("Cari Artikel", use_container_width=True)

# Perform Search
if search_button and query:
    st.session_state.search_performed = True
    st.session_state.page = 1
    st.session_state.query = query
    st.session_state.algorithm = algorithm

# Display Results
if st.session_state.search_performed and 'query' in st.session_state:
    query = st.session_state.query
    algorithm = st.session_state.algorithm

    # Get results
    if algorithm == "Cosine Similarity":
        all_results = get_cosine_similarity(query)
        algo_name = "Cosine"
    else:
        all_results = get_jaccard_similarity(query)
        algo_name = "Jaccard"

    total_results = len(all_results)

    # Stats
    st.markdown(f"""
    <div class="stats-box">
        <h3>Ditemukan {total_results} hasil untuk "{query}"</h3>
        <p>Menggunakan algoritma {algorithm}</p>
    </div>
    """, unsafe_allow_html=True)

    if total_results > 0:
        # Pagination
        per_page = 5
        total_pages = (total_results + per_page - 1) // per_page
        page = st.session_state.page

        start = (page - 1) * per_page
        end = min(start + per_page, total_results)
        results = all_results[start:end]

        # Display results
        for result in results:
            col_img, col_content = st.columns([1, 2])

            with col_img:
                try:
                    st.image(result["image"],
                             use_container_width=True, caption="")
                except:
                    st.image(
                        "https://via.placeholder.com/400x300?text=No+Image", use_container_width=True)

            with col_content:
                st.markdown(f"""
                <div style="padding: 0.5rem;">
                    <h3 style="color: #FFFFFF; font-size: 1.35rem; font-weight: 600; margin-bottom: 0.6rem; letter-spacing: -0.3px; text-shadow: 0 2px 8px rgba(0,0,0,0.2);">
                        <a href="{result['link']}" target="_blank" style="color: inherit; text-decoration: none; transition: color 0.3s ease;">{result['title']}</a>
                    </h3>
                    <p style="color: rgba(255, 255, 255, 0.8); line-height: 1.75; font-size: 0.95rem; margin-bottom: 1rem;">{result['content']}</p>
                    <div style="display: flex; align-items: center; flex-wrap: wrap; gap: 0.75rem;">
                        <span style="background: rgba(255, 255, 255, 0.2); color: #FFFFFF; padding: 0.5rem 1.1rem; border-radius: 12px; font-size: 0.9rem; font-weight: 600; border: 1px solid rgba(255, 255, 255, 0.3); backdrop-filter: blur(15px); box-shadow: 0 4px 15px rgba(0,0,0,0.15); text-shadow: 0 1px 3px rgba(0,0,0,0.2);">
                            📅 {result['date']}
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                score_percent = result['score'] * 100
                st.markdown(f"""
                <div style="margin-top: 1rem;">
                    <span style="background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%); color: #FFFFFF; padding: 0.6rem 1.25rem; border-radius: 14px; font-weight: 700; font-size: 0.9rem; display: inline-block; font-family: 'JetBrains Mono', monospace; box-shadow: 0 4px 20px rgba(255, 107, 53, 0.35);">
                        ⚡ {algo_name}: {score_percent:.2f}%
                    </span>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("---")

        # Pagination controls
        col_prev, col_info, col_next = st.columns([1, 2, 1])

        with col_prev:
            if page > 1:
                if st.button("⬅️ Sebelumnya", use_container_width=True):
                    st.session_state.page -= 1
                    st.rerun()

        with col_info:
            st.markdown(
                f"<div style='text-align: center; color: #FFFFFF; font-weight: 600; padding: 0.9rem 1.5rem; background: rgba(255, 255, 255, 0.15); border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.2); backdrop-filter: blur(15px); box-shadow: 0 4px 20px rgba(0,0,0,0.1);'>📄 Halaman {page} dari {total_pages}</div>", unsafe_allow_html=True)

        with col_next:
            if page < total_pages:
                if st.button("Selanjutnya ➡️", use_container_width=True):
                    st.session_state.page += 1
                    st.rerun()
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background: rgba(255, 255, 255, 0.12); border-radius: 24px; backdrop-filter: blur(20px); border: 1px solid rgba(255, 255, 255, 0.18); position: relative; z-index: 1; box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔍</div>
            <h2 style="color: #FFFFFF; font-weight: 600; font-size: 1.4rem; margin-bottom: 0.75rem; text-shadow: 0 2px 8px rgba(0,0,0,0.2);">Tidak ada hasil ditemukan</h2>
            <p style="color: rgba(255, 255, 255, 0.75); font-size: 1rem;">Coba gunakan kata kunci yang berbeda atau ubah algoritma pencarian</p>
        </div>
        """, unsafe_allow_html=True)

# Footer with glassmorphism styling
st.markdown("""
<div style="text-align: center; padding: 2rem 2.5rem; margin-top: 3rem; background: rgba(255, 255, 255, 0.1); border-radius: 24px; backdrop-filter: blur(20px); position: relative; z-index: 1; border: 1px solid rgba(255, 255, 255, 0.15); box-shadow: 0 8px 32px rgba(0,0,0,0.1);">
    <p style="font-size: 1rem; color: rgba(255, 255, 255, 0.9); font-weight: 500; margin-bottom: 0.5rem;">✨ Dibuat dengan Streamlit • Powered by Information Retrieval ✨</p>
    <p style="font-size: 0.9rem; color: rgba(255, 255, 255, 0.6);">© 2025 PETite - Pencarian Artikel Hewan Peliharaan</p>
</div>
""", unsafe_allow_html=True)
