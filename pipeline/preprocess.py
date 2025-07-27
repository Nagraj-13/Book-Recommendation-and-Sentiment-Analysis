import pandas as pd
import os
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Paths
DATA_PATH = "../Datasets/cleaned_data/cleaned_data.csv"
PROCESSED_DATA_PATH = "../Datasets/cleaned_data/preprocessed_data.csv"
VECTORIZER_PATH = "../Models/tfidf_vectorizer.joblib"

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', str(text).lower())
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def preprocess_and_save():
    print("[INFO] Loading raw data...")
    df = pd.read_csv(DATA_PATH)

    if 'review/text' not in df.columns:
        raise ValueError("Missing 'review/text' column in input data.")

    print("[INFO] Cleaning text data...")
    df['clean_text'] = df['review/text'].apply(clean_text)

    print("[INFO] Encoding sentiment labels...")
    df['label'] = df['Sentiment'].map({
        'positive': 1,
        'negative': 0
    })

    # Drop rows with null labels (e.g. neutral or missing)
    df = df.dropna(subset=['label'])

    print("[INFO] Vectorizing text with TF-IDF...")
    vectorizer = TfidfVectorizer(max_features=5000)
    X = vectorizer.fit_transform(df['clean_text'])
    y = df['label'].astype(int)

    print(f"[INFO] Saving preprocessed data to {PROCESSED_DATA_PATH}")
    X_df = pd.DataFrame(X.toarray())
    X_df['label'] = y.values
    X_df.to_csv(PROCESSED_DATA_PATH, index=False)

    print(f"[INFO] Saving TF-IDF vectorizer to {VECTORIZER_PATH}")
    joblib.dump(vectorizer, VECTORIZER_PATH)

    print("[INFO] Preprocessing complete.")

if __name__ == "__main__":
    preprocess_and_save()
