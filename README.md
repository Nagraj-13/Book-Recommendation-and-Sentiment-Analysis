# Book Recommendation & Sentiment Analysis Dashboard

A unified system providing:

* **Sentiment Analysis API**: Analyze single or batch text reviews using custom-trained sentiment models.
* **Book Recommendation API**: Generate book recommendations via content‑based, collaborative, and hybrid methods, as well as genre/author-based searches.
* **Streamlit Dashboard**: Interactive UI to explore both APIs side by side.
* **Launcher Script**: One‑click parallel startup for backend services and dashboard.

---

## 🚀 Features

1. **Custom Sentiment Models**

   * **Single-review analysis**: Classify sentiment label and confidence score.
   * **Batch analysis**: Process multiple reviews in one call.

2. **Recommendation Engine**

   * **Similar books**: Find titles closely matching a query.
   * **Author & genre filters**: List by author or top picks in a genre.
   * **Related recommendations**: Suggest books related to a given title.
   * **Content‑based**: Recommend based on user‑provided keywords or descriptions.
   * **Collaborative**: Leverage purchase history lists.
   * **Hybrid**: Combine content and collaborative strategies.

3. **Streamlit UI**

   * Two tabs: Sentiment Analysis & Book Recommendations.
   * Pre‑filled sample inputs.
   * Real‑time JSON response viewing.

4. **Simple Launcher**

   * Starts API server(s) and dashboard in parallel.
   * Aggregates logs with process prefixes.

---

## 📋 Requirements

* Python 3.9+
* Virtual environment (`venv` or `virtualenv`)
* Dependencies defined in `requirements.txt`:

  ```text
  fastapi
  uvicorn
  pydantic
  streamlit
  requests
  python-dotenv
  sklearn          # sentiment model deps
  pandas           # sentiment model deps
  ```

---

## ⚙️ Installation & Setup

1. **Clone repository**

   ```bash
   git clone https://github.com/your-org/book-sentiment-dashboard.git
   cd book-sentiment-dashboard
   ```

2. **Create & activate virtual env**

   ```bash
   python -m venv .venv
   # Windows
   .\.venv\Scripts\activate
   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**

   * Copy `.env.example` to `.env`
   * Fill any required keys (e.g. database URL, model paths)

   ```ini
   # .env
   SENTIMENT_MODEL_PATH=models/sentiment.pkl
   RECOMMENDER_MODEL_PATH=models/recommender.pkl
   ```

---

## 📂 Directory Structure

```
├── app.py                # Streamlit dashboard
├── launcher.py           # Parallel startup script
├── backend/
│   ├── main.py           # FastAPI entrypoint
│   ├── models/
│   │   ├── sentiment_model.py
│   │   └── recommendation_model.py
│   └── core/
│       ├── sentiment.py  # sentiment inference logic
│       └── util/
│           └── recommender.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🏃‍♂️ Usage

### 1. Launch Services

Run the launcher to start both backend and dashboard:

```bash
python launcher.py
```

### 2. Streamlit Dashboard

In a separate shell (if not using launcher), start:

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

### 3. API Only

Start only the backend API:

```bash
uvicorn backend.main:app --reload --port 8001
```

---

## 📡 API Endpoints

Base URL: `http://localhost:8001`

### Sentiment Analysis

* **POST** `/sentiment/single`
  Request body:

  ```json
  { "review": "I loved the book!" }
  ```

  Response:

  ```json
  {
    "review": "I loved the book!",
    "label": "POSITIVE",
    "score": 0.98,
    "error": null
  }
  ```

* **POST** `/sentiment/batch`
  Request body:

  ```json
  { "reviews": ["Great read.", "Too long."] }
  ```

  Response:

  ```json
  {
    "results": [
      { "review": "Great read.", "label": "POSITIVE", "score": 0.93 },
      { "review": "Too long.",   "label": "NEGATIVE", "score": 0.85 }
    ]
  }
  ```

### Book Recommendations

All endpoints accept JSON and return a list of book objects:

```json
{
  "title": "1984",
  "author": "George Orwell",
  "genre": "Dystopian",
  "description": "A cautionary tale...",
  "publication_year": 1949,
  "rating": 4.2
}
```

| Endpoint                             | Body Example                            |
| ------------------------------------ | --------------------------------------- |
| **POST** `/recommend/similar`        | `{ "query": "1984" }`                   |
| **POST** `/recommend/author`         | `{ "query": "George Orwell" }`          |
| **POST** `/recommend/genre`          | `{ "query": "Fantasy" }`                |
| **POST** `/recommend/related`        | `{ "query": "Brave New World" }`        |
| **POST** `/recommend/user_preferred` | `{ "titles": ["Dune","Foundation"] }`   |
| **POST** `/recommend/content_based`  | `{ "query": "space opera epic" }`       |
| **POST** `/recommend/collaborative`  | `{ "titles": ["Dune","Foundation"] }`   |
| **POST** `/recommend/hybrid`         | `{ "titles": ["Dune","Ender's Game"] }` |

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/...`)
3. Commit your changes
4. Push and open a PR

---

## 📜 License

MIT © Your Name
