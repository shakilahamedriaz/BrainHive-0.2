import os
import numpy as np
import faiss
import pickle
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer
from blog.models import Post

class Command(BaseCommand):
    help = 'Generates and saves a searchable index of all blog posts for the AI chatbot.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('--- Starting AI Chatbot Indexing ---'))

        posts = Post.objects.all()
        if not posts:
            self.stdout.write(self.style.WARNING('No posts found in the database. Nothing to index.'))
            return

        # 1. Load a powerful model to understand text meaning
        self.stdout.write('Step 1/4: Loading the sentence-transformer model (all-MiniLM-L6-v2)...')
        model = SentenceTransformer('all-MiniLM-L6-v2')

        # 2. Prepare the text from all your posts
        self.stdout.write('Step 2/4: Cleaning and preparing text from all posts...')
        post_texts = []
        post_ids = []
        for post in posts:
            # Clean HTML tags from the RichTextField content
            soup = BeautifulSoup(post.content, 'html.parser')
            clean_text = post.title + ". " + soup.get_text(strip=True) # Combine title and content
            post_texts.append(clean_text)
            post_ids.append(post.id)
        
        # 3. Generate numerical representations (embeddings) for all posts
        self.stdout.write(f'Step 3/4: Generating AI embeddings for {len(post_texts)} posts...')
        embeddings = model.encode(post_texts, show_progress_bar=True)

        # 4. Create and save a super-fast FAISS index
        self.stdout.write('Step 4/4: Building and saving the FAISS index...')
        embedding_dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(embedding_dim)
        index.add(np.array(embeddings).astype('float32'))

        # Define where to save the files (in your project's main directory)
        index_path = 'blog_post_index.faiss'
        mapping_path = 'blog_post_mapping.pkl'
        
        faiss.write_index(index, index_path)
        
        # Save a mapping file to remember which text belongs to which ID
        with open(mapping_path, 'wb') as f:
            pickle.dump({'ids': post_ids, 'texts': post_texts}, f)

        self.stdout.write(self.style.SUCCESS(f'\n--- Indexing Complete! ---'))
        self.stdout.write(self.style.SUCCESS(f'Successfully created an index for {index.ntotal} posts.'))
        self.stdout.write(self.style.SUCCESS(f'Files saved: {index_path} and {mapping_path}'))
