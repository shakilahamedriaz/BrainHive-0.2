BrainHive-AI: AI-Enhanced Django Blogging Platform
<div align="center">
<img src="https://www.google.com/search?q=https://i.imgur.com/5b803e.png" alt="BrainHive-AI Showcase" width="800"/>
</div>

<p align="center">
A sophisticated, full-stack blogging application built with Django and Python, supercharged with modern AI capabilities. BrainHive-AI provides a seamless user experience for content creation and consumption, augmented by an AI-powered summarizer and a knowledgeable RAG-based chatbot.
</p>

🚀 Core Features & Technical Highlights
This project demonstrates a comprehensive understanding of full-stack web development and the practical application of modern AI technologies.

Backend & Core Application
👤 Secure User Authentication: Full user lifecycle management including registration, login/logout, and profile management.

📝 Full CRUD Functionality: Robust implementation of Create, Read,Update, and Delete operations for blog posts, ensuring users have full control over their content.

🎨 Rich Text Editing: Integrated django-ckeditor to provide a powerful WYSIWYG editor for an enhanced writing experience.

🔍 Advanced Search & Filtering: Dynamic server-side search functionality combined with filtering by categories and tags for efficient content discovery.

💬 Interactive Comment & Like System: Real-time user engagement through a robust commenting and liking system.

📈 Database & ORM Mastery: Efficient data modeling and querying using the Django ORM with a relational SQLite database.

🤖 Artificial Intelligence Integration
✨ AI-Powered Summarization: Leverages the Groq API (with Llama 3) to automatically generate and save concise summaries for every blog post, triggered on model save. This demonstrates knowledge of background task processing and API integration.

🧠 Retrieval-Augmented Generation (RAG) Chatbot: A custom-built AI chatbot that answers user questions based only on the knowledge within the blog's articles. This is a key feature demonstrating advanced AI implementation skills.

💡 AI System Design: The RAG Chatbot
The chatbot is not a simple API call; it's a complete RAG pipeline that ensures answers are accurate and grounded in the provided content.

Indexing (index_posts.py): A custom Django management command processes all blog posts. It uses sentence-transformers to convert the text into numerical vector embeddings. These embeddings are stored in a highly efficient FAISS vector index.

Retrieval: When a user asks a question, the user's query is also converted into an embedding. The FAISS index is then searched to find the most semantically similar blog post chunks (the "context").

Augmentation & Generation: This retrieved context is then injected into a carefully crafted prompt that is sent to the Groq API's Llama 3 model. The model is instructed to formulate an answer strictly based on this context.

This RAG architecture is a powerful, industry-standard technique that prevents AI hallucinations and creates a truly knowledgeable assistant.

🛠️ Tech Stack
Category

Technology

Backend

Python, Django

Frontend

Tailwind CSS, Alpine.js

Database

SQLite 3

AI API

Groq (Llama 3 Model)

AI/ML Libs

sentence-transformers, faiss-cpu, beautifulsoup4

Tooling

django-ckeditor, django-widget-tweaks, python-dotenv

🚀 Local Setup and Installation
Follow these steps to get the project running on your local machine.

1. Prerequisites
Python 3.10+

Git

2. Setup Instructions
1. Clone the Repository

git clone [https://github.com/your-username/BrainHive-AI.git](https://github.com/your-username/BrainHive-AI.git)
cd BrainHive-AI

2. Create and Activate Virtual Environment

# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
Create a requirements.txt file by running pip freeze > requirements.txt in your current project. Then, another user can install the dependencies using:

pip install -r requirements.txt

4. Configure Environment Variables

Create a .env file in the project root.

Add your Groq API key:

GROQ_API_KEY=gsk_YourSecretApiKeyGoesHere

5. Prepare the Database

python manage.py migrate

6. Create an Admin User

python manage.py createsuperuser

7. Build the AI Chatbot Index
This is a critical step. Run the custom command to build the chatbot's knowledge base from the posts in your database (if you've added any via the admin panel).

python manage.py index_posts

8. Run the Server

python manage.py runserver

The application will be live at http://127.0.0.1:8000/.

👤 Author
Shakil Ahamed Riaz

GitHub: @shakilahamedriaz

LinkedIn: [shakilahamedriaz](https://www.linkedin.com/shakilahamedriaz)