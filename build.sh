#!/usr/bin/env bash
# Exit immediately on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Apply database migrations first
echo "Running database migrations..."
python manage.py migrate

# Build FAISS vector index (must come after data is loaded)
echo "Building FAISS index..."
python manage.py index_posts

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input
