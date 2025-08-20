# Create a detailed README
echo "# Book Recommendation App

A Flask web application that provides intelligent book recommendations using Google Books API and AI-powered semantic similarity.

## Features
- 🔍 Search books using Google Books API
- 🤖 AI-powered recommendations using sentence transformers
- 🌐 Web interface and REST API
- 📚 Semantic similarity matching

## Installation
\`\`\`bash
git clone https://github.com/pio8900/e-lib.git
cd e-lib
pip install -r requirements.txt
python app.py
\`\`\`

## Usage
- Web: http://localhost:5000
- API: POST to /api/search with {\"query\": \"search term\"}

## Technologies
- Flask
- SentenceTransformers
- Google Books API
- HTML/CSS" > README.md

# Commit and push the updated README
git add README.md
git commit -m "Add comprehensive README"
git push
