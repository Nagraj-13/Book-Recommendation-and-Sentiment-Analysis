#!/usr/bin/env python3
"""
logistic.py

A production‑ready training pipeline for book‑review sentiment classification
using Logistic Regression. Reads cleaned CSV, vectorizes text, trains, evaluates,
and saves the model artifact.

Usage:
    python logistic.py --sample-size 10000
"""

import argparse
import logging
import os
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

# Constants
DATA_PATH = Path("../Datasets/cleaned_data/cleaned_data.csv")
MODEL_PATH = Path("../Models")
MODEL_NAME = "logreg_sentiment.pkl"

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


def load_data(path: Path, sample_size: int = None) -> pd.DataFrame:
    """Load cleaned data and optionally sample."""
    if not path.exists():
        logger.error(f"Data file not found: {path}")
        sys.exit(1)

    df = pd.read_csv(path)
    logger.info(f"Loaded {len(df):,} rows from {path}")

    if sample_size is not None and sample_size < len(df):
        df = df.sample(sample_size, random_state=42)
        logger.info(f"Sampled down to {len(df):,} rows")

    # Expecting 'clean_reviews' and 'Sentiment' columns
    if 'clean_reviews' not in df.columns:
        if 'review' in df.columns:
            df['clean_reviews'] = df['review'].astype(str).str.lower()
            logger.info("Derived 'clean_reviews' from 'review' column")
        else:
            logger.error("No column 'clean_reviews' or 'review' found in data")
            sys.exit(1)

    if 'Sentiment' not in df.columns:
        logger.error("No target column 'Sentiment' found in data")
        sys.exit(1)

    return df[['clean_reviews', 'Sentiment']].dropna()


def build_pipeline() -> Pipeline:
    """Construct the sklearn Pipeline."""
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            max_features=10_000,
            ngram_range=(1, 2),
            strip_accents="unicode",
            lowercase=True,
            stop_words="english"
        )),
        ("clf", LogisticRegression(
            solver="liblinear",
            C=1.0,
            max_iter=1000,
            random_state=42
        )),
    ])
    return pipeline


def train_and_evaluate(
    df: pd.DataFrame,
    test_size: float = 0.2,
    random_state: int = 42
):
    """Split data, train pipeline, and print evaluation metrics."""
    X = df['clean_reviews']
    y = df['Sentiment']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        stratify=y,
        random_state=random_state
    )
    logger.info(f"Train/test split: {len(X_train):,}/{len(X_test):,}")

    pipeline = build_pipeline()
    logger.info("Starting model training...")
    pipeline.fit(X_train, y_train)
    logger.info("Training complete.")

    # Evaluation
    logger.info("Evaluating on test set...")
    preds = pipeline.predict(X_test)
    acc = accuracy_score(y_test, preds)
    logger.info(f"Test Accuracy: {acc:.4f}")

    logger.info("Classification Report:")
    logger.info("\n" + classification_report(y_test, preds))

    cm = confusion_matrix(y_test, preds, labels=pipeline.classes_)
    logger.info("Confusion Matrix:")
    logger.info(f"\nClasses: {pipeline.classes_}\n{cm}")

    return pipeline


def save_model(pipeline: Pipeline, model_dir: Path, model_name: str):
    """Persist the trained pipeline to disk."""
    model_dir.mkdir(parents=True, exist_ok=True)
    dest = model_dir / model_name
    joblib.dump(pipeline, dest)
    logger.info(f"Model saved to {dest}")


def parse_args():
    parser = argparse.ArgumentParser(description="Train sentiment classifier")
    parser.add_argument(
        "--sample-size",
        type=int,
        default=None,
        help="Number of samples to draw from dataset for training"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    df = load_data(DATA_PATH, sample_size=args.sample_size)
    pipeline = train_and_evaluate(df)
    save_model(pipeline, MODEL_PATH, MODEL_NAME)


if __name__ == "__main__":
    main()
