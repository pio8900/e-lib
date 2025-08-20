# e-lib
# Book Recommendation App
A Flask web application that recommends books using Google Books API and sentence transformers for semantic similarity.
## Features
- Search books using Google Books API
- AI-powered book recommendations based on user queries
- Web interface and REST API endpoints

## Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`

## Usage
- Web interface: Navigate to `http://localhost:5000`
- API endpoint: POST to `/api/search` with JSON payload `{"query": "your search"}`
