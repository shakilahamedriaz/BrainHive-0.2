# 🧠 BrainHive: AI-Enhanced Knowledge Sharing Platform

![Built with Django](https://img.shields.io/badge/Built%20with-Django-092E20?style=for-the-badge&logo=django)
![Frontend - Tailwind CSS & Alpine.js](https://img.shields.io/badge/Frontend-TailwindCSS%20%26%20Alpine.js-06B6D4?style=for-the-badge&logo=tailwindcss)
![AI - Groq & LLaMA 3](https://img.shields.io/badge/AI-Groq%20%26%20LLaMA%203-FF4400?style=for-the-badge&logo=openai)
![Database - PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?style=for-the-badge&logo=postgresql)

BrainHive is a cutting-edge, community-driven web application designed to revolutionize knowledge sharing through intelligent AI integration. It combines robust full-stack engineering with advanced AI capabilities to deliver a seamless and insightful user experience, making knowledge discoverable, digestible, and contextually relevant.

---

## 📋 Table of Contents

* [✨ Features](#-features)
* [🤖 AI-Powered Intelligence Layer](#-ai-powered-intelligence-layer)
    * [AI Summarization Engine](#ai-summarization-engine)
    * [Meet "Brainy" – BrainHive AI Assistant](#meet-brainy--brainhive-ai-assistant)
* [🛠️ Tech Stack](#%EF%B8%8F-tech-stack)
* [🚀 Getting Started](#-getting-started)
    * [Prerequisites](#prerequisites)
    * [Installation](#installation)
    * [Running the Application](#running-the-application)
* [📂 Project Structure](#-project-structure)
* [🤝 Contributing](#-contributing)
* [📄 License](#-license)
* [📞 Contact](#-contact)

---

## ✨ Features

BrainHive is built as a scalable and secure platform, offering a comprehensive set of features for efficient knowledge management:

* **Full-Stack Django Architecture:** A robust and secure backend providing a solid foundation.
* **Secure User Authentication & Profile Management:** Ensures data privacy and personalized user experiences.
* **Content Management System (CMS):**
    * Full CRUD (Create, Read, Update, Delete) operations for knowledge posts.
    * Rich text editing capabilities powered by `django-ckeditor`.
* **Fast Search & Filtering:** Efficiently find content using keywords, tags, and categories.
* **Responsive UI:** A modern and adaptive user interface designed with Tailwind CSS and Alpine.js for optimal viewing across all devices.

---

## 🤖 AI-Powered Intelligence Layer

AI is not just an add-on in BrainHive; it's a fundamental component that transforms how users interact with shared knowledge.

### AI Summarization Engine

Every knowledge post uploaded to BrainHive is automatically summarized, enhancing discoverability and clarity at scale.

* **Model Used:** `llama3-8b-8192`
* **Trigger:** Summarization is automatically triggered during the save lifecycle of each post, ensuring that summaries are always up-to-date and available immediately upon content creation.

### Meet "Brainy" – BrainHive AI Assistant

"Brainy" is a custom-built, RAG (Retrieval-Augmented Generation)-based AI assistant designed to provide real-time, context-aware answers strictly grounded in the platform's content.

**How Brainy Works:**

1.  **Indexing:** Content is processed and indexed using `Sentence-Transformers` for semantic understanding and `FAISS` for efficient similarity search.
2.  **Semantic Retrieval:** When a user queries Brainy, the system semantically retrieves the most relevant chunks of information from the indexed platform content.
3.  **Grounded Response Generation:** The retrieved information is then fed to Groq’s LLaMA 3 8B model, which generates accurate and contextually relevant responses, ensuring answers are always grounded in the platform's knowledge base.

---

## 🛠️ Tech Stack

* **Backend:**
    * Python
    * Django
    * Django REST Framework (for API endpoints, if applicable)
    * PostgreSQL (Database)
    * Celery (for asynchronous tasks like summarization, if applicable)
* **Frontend:**
    * HTML5
    * Tailwind CSS
    * Alpine.js
* **AI/ML:**
    * Groq API (for LLaMA 3 8B model)
    * Hugging Face `Sentence-Transformers`
    * FAISS (Facebook AI Similarity Search)
* **Deployment:** (Specify if known, e.g., Docker, Nginx, Gunicorn, AWS/GCP/Azure)

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following installed:

* Python 3.9+
* pip (Python package installer)
* Git
* PostgreSQL (or another database system compatible with Django)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/BrainHive.git](https://github.com/your-username/BrainHive.git)
    cd BrainHive
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Note: You will need to create a `requirements.txt` file by running `pip freeze > requirements.txt` after installing all necessary packages like Django, djangorestframework, django-ckeditor, psycopg2-binary, groq, sentence-transformers, faiss-cpu, etc.)*

4.  **Set up environment variables:**
    Create a `.env` file in the root directory of the project and add your configuration.
    ```env
    SECRET_KEY='your_django_secret_key'
    DEBUG=True
    DATABASE_URL='postgres://user:password@host:port/database_name'
    GROQ_API_KEY='your_groq_api_key'
    # Add any other necessary environment variables (e.g., for email, cloud storage)
    ```

5.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Create a superuser (optional, for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

7.  **Initialize AI models/indexes (if required):**
    * Depending on your implementation, you might need to run a command to generate initial embeddings or set up FAISS indexes.
    * For example: `python manage.py build_faiss_index` (replace with your actual command)

### Running the Application

1.  **Start the Django development server:**
    ```bash
    python manage.py runserver
    ```

2.  **Access the application:**
    Open your web browser and navigate to `http://127.0.0.1:8000/`.

---

## 📂 Project Structure

```text
BrainHive/
├── brainhive_project/         # Main Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                      # Core app (e.g., base models, utilities)
├── accounts/                  # User authentication and profiles
├── posts/                     # Knowledge posts, categories, tags
├── search/                    # Search functionality
├── ai_assistant/              # Brainy AI assistant logic, RAG implementation
├── templates/                 # HTML templates
├── static/                    # Static files (CSS, JS, images)
├── media/                     # User-uploaded media
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── .env.example               # Example environment variables
└── README.md                  # This file

```
---

## 🤝 Contributing

We welcome contributions to BrainHive! If you have suggestions for improvements, new features, or bug fixes, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
*(Note: You will need to create a `LICENSE` file in your repository.)*

---

## 📞 Contact

For feedback, collaboration opportunities, or general inquiries, feel free to connect:

* **GitHub:** [https://github.com/your-username/BrainHive](https://github.com/your-username/BrainHive) (Replace `your-username` with your actual GitHub username)
* **Live Demo Walkthrough (YouTube):** [https://lnkd.in/gRvcTrzJ](https://lnkd.in/gRvcTrzJ)
* **Live Site:** Coming Soon!

---

Thank you for exploring BrainHive!
