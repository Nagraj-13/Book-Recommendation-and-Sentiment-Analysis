
import streamlit as st
import requests
import json

st.set_page_config(page_title="Book & Sentiment API Explorer", layout="wide")

st.title("📚 Book Recommendation & Sentiment API Explorer")

# Sidebar: API base URL
base_url = st.sidebar.text_input("API Base URL", value="http://localhost:8001").rstrip('/')

# Create tabs for clear separation
tab1, tab2 = st.tabs(["🔍 Sentiment Analysis", "🤖 Book Recommendations"]);

# --- Sentiment Analysis Tab ---
with tab1:
    st.header("Sentiment Analysis")
    st.write("Use the sample inputs below or provide your own.")

    sentiment_mode = st.radio("Mode", ["Single Review", "Batch Reviews"], index=0)

    if sentiment_mode == "Single Review":
        sample = "I loved the book, it was fascinating and engaging."
        review = st.text_area(
            "Enter a single review:",
            value=sample,
            height=150
        )
        payload = {"review": review}
        endpoint = "/sentiment/single"
    else:
        sample = "The plot was predictable.\nGreat character development.\nToo slow at times."
        reviews_text = st.text_area(
            "Enter reviews (one per line):",
            value=sample,
            height=200
        )
        reviews = [r.strip() for r in reviews_text.splitlines() if r.strip()]
        payload = {"reviews": reviews}
        endpoint = "/sentiment/batch"

    if st.button("Analyze Sentiment"):
        url = f"{base_url}{endpoint}"
        try:
            with st.spinner("Calling Sentiment API..."):
                resp = requests.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                st.subheader("Response JSON")
                st.json(data)
            else:
                st.error(f"API returned status {resp.status_code}")
                st.text(resp.text)
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

# --- Book Recommendations Tab ---
with tab2:
    st.header("Book Recommendations")
    st.write("Choose a recommendation type and see sample payload below.")

    # Recommendation options
    RECS = {
        "Similar Books": ("/recommend/similar", "query", "1984"),
        "By Author": ("/recommend/author", "query", "George Orwell"),
        "By Genre": ("/recommend/genre", "query", "Dystopian"),
        "Related to Book": ("/recommend/related", "query", "Brave New World"),
        "User Preferred": ("/recommend/user_preferred", "titles", ["The Hobbit", "LOTR"]),
        "Content-based": ("/recommend/content_based", "query", "Coming-of-age tale"),
        "Collaborative": ("/recommend/collaborative", "titles", ["Dune", "Foundation"]),
        "Hybrid": ("/recommend/hybrid", "titles", ["Dune", "Ender's Game"]),
    }

    choice = st.selectbox("Recommendation Type", list(RECS.keys()))
    path, p_type, sample = RECS[choice]

    if p_type == "query":
        payload = {"query": st.text_input("Query", value=str(sample))}
    else:
        default = "\n".join(sample)
        titles_text = st.text_area("Titles (one per line):", value=default, height=150)
        titles = [t.strip() for t in titles_text.splitlines() if t.strip()]
        payload = {"titles": titles}

    if st.button("Get Recommendations"):
        url = f"{base_url}{path}"
        try:
            with st.spinner("Calling Recommendation API..."):
                resp = requests.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                st.subheader("Response JSON")
                st.json(data)
            else:
                st.error(f"API returned status {resp.status_code}")
                st.text(resp.text)
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
