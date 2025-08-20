from flask import Flask, request, jsonify, render_template
import requests
from sentence_transformers import SentenceTransformer, util
import numpy as np

app = Flask(__name__)

# Initialize the model for sentence embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')

# Fetch books from Google Books API
def fetch_books(query, max_results=10):
    api_url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={max_results}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Handle non-200 responses
        books = response.json().get('items', [])
        return [
            {
                "title": item['volumeInfo'].get('title', 'No Title'),
                "description": item['volumeInfo'].get('description', 'No Description'),
                "authors": item['volumeInfo'].get('authors', ['Unknown']),
                "image": item['volumeInfo'].get('imageLinks', {}).get('thumbnail', None),
                "url": item['volumeInfo'].get('infoLink', '#'),
                "type": item['volumeInfo'].get('printType', 'Book')
            }
            for item in books
        ]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return []

# Function to recommend books
# In recommend_books, you are sorting books and similarity pairs, but pass only the book details.
def recommend_books(user_query, books):
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    book_descriptions = [book['description'] for book in books]
    book_embeddings = model.encode(book_descriptions, convert_to_tensor=True)
    
    similarities = util.pytorch_cos_sim(query_embedding, book_embeddings).cpu().numpy()
    
    # Rank Books by Similarity (now extracting the book data from the tuple)
    recommendations = sorted(
        zip(books, similarities[0]), key=lambda x: x[1], reverse=True
    )
    
    # Pass only the book data
    return [book for book, _ in recommendations]  # only return books, ignoring the similarity scores


# Flask Routes
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            books = fetch_books(query)
            if books:
                # Get recommendations for the books fetched
                recommended_books = recommend_books(query, books)
                return render_template('index.html', books=recommended_books, query=query)
            else:
                return render_template('index.html', query=query, books=None)
        else:
            return render_template('index.html', books=[], query=None)
    return render_template('index.html')

@app.route('/api/search', methods=['POST'])
def search_api():
    data = request.json
    query = data.get('query', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400
    books = fetch_books(query)
    if books:
        recommended_books = recommend_books(query, books)
    return jsonify({'results': [book[0] for book in recommended_books]})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
