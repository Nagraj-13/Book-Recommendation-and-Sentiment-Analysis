import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

st.set_page_config(
    page_title="Book Reviews EDA Dashboard",
    layout="wide"
)

@st.cache_data
def load_data():
    # Adjust filenames/paths if needed
    df = pd.read_csv("./Datasets/cleaned_data/cleaned_data.csv")        # from sentiment_analysis.ipynb

    return df

# Load dataset
data = load_data()

# --- Add any derived columns if missing ---
if 'clean_reviews' not in data:
    data['clean_reviews'] = data['review/text'].str.lower()
if 'word_count' not in data:
    data['word_count'] = data['clean_reviews'].str.split().apply(len)
if 'compound' not in data or 'Sentiment' not in data:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    vader = SentimentIntensityAnalyzer()
    data['compound'] = data['clean_reviews'].apply(lambda t: vader.polarity_scores(t)['compound'])
    data['Sentiment'] = data['compound'].apply(
        lambda x: 'positive' if x >= 0.05 else 'negative' if x < -0.05 else 'neutral'
    )

st.title("📊 Book Reviews EDA & Visualization")

# Sidebar filters
st.sidebar.header("🔎 Filters")
sentiments = st.sidebar.multiselect(
    "Sentiment",
    options=data['Sentiment'].unique(),
    default=data['Sentiment'].unique()
)
min_words, max_words = st.sidebar.slider(
    "Review Length (words)",
    int(data['word_count'].min()),
    int(data['word_count'].max()),
    (int(data['word_count'].quantile(0.05)), int(data['word_count'].quantile(0.95)))
)
genre_options = data['categories'].unique().tolist()
selected_genres = st.sidebar.multiselect("Genre", genre_options, default=genre_options)

# Apply filters
mask = (
    data['Sentiment'].isin(sentiments) &
    data['word_count'].between(min_words, max_words) &
    data['categories'].isin(selected_genres)
)
df = data[mask]

# Layout: 2 rows x 2 cols
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# 1. Sentiment Distribution Pie
with col1:
    st.subheader("Sentiment Distribution")
    counts = df['Sentiment'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(
        counts,
        labels=counts.index,
        autopct='%1.1f%%',
        explode=[0.05]*len(counts),
        startangle=90
    )
    ax.axis('equal')
    st.pyplot(fig)

# 2. Genre Distribution Bar
with col2:
    st.subheader("Top Genres by Count")
    top_genres = df['categories'].value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=top_genres.values, y=top_genres.index, ax=ax)
    ax.set_xlabel("Number of Reviews")
    st.pyplot(fig)

# 3. Review Length Distribution
with col3:
    st.subheader("Review Length Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df['word_count'], bins=30, kde=True, ax=ax)
    ax.set_xlabel("Word Count")
    st.pyplot(fig)

# 4. Average Sentiment Score by Genre
with col4:
    st.subheader("Avg. Sentiment Score by Genre")
    avg_score = df.groupby('categories')['compound'].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=avg_score.values, y=avg_score.index, ax=ax)
    ax.set_xlabel("Average Compound Score")
    st.pyplot(fig)

st.markdown("---")

# 5. Top N Most Loved Books
st.subheader("🏆 Top 10 Most Loved Books")
avg_book = df.groupby('Title')['compound'].mean().sort_values(ascending=False).head(10)
fig, ax = plt.subplots(figsize=(6,4))
sns.barplot(x=avg_book.values, y=avg_book.index, ax=ax)
ax.set_xlabel("Average Compound Score")
st.pyplot(fig)

# 6. WordCloud for Positive vs Negative
st.subheader("🧠 WordCloud Comparison")

col5, col6 = st.columns(2)
for sentiment, colw in zip(['positive','negative'], [col5, col6]):
    with colw:
        st.markdown(f"**{sentiment.title()} Reviews**")
        text = " ".join(df[df['Sentiment']==sentiment]['clean_reviews'])
        wc = WordCloud(width=400, height=200, background_color='white').generate(text)
        fig, ax = plt.subplots(figsize=(5,3))
        ax.imshow(wc, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)

st.markdown("---")
st.subheader("📄 Sample Filtered Reviews")
st.dataframe(df[['Title','categories','Sentiment','compound','word_count']].sample(10))
