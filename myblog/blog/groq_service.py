import os
from groq import Groq
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# Load environment variables from .env file
load_dotenv()

def get_ai_summary(post_content_html):
    """
    Generates a summary for a blog post using the Groq API.
    """
    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        # Clean the HTML content to get plain text
        soup = BeautifulSoup(post_content_html, 'html.parser')
        plain_text_content = soup.get_text(separator=' ', strip=True)

        # Create the prompt for the AI
        prompt = f"""
        You are an expert blog summarizer. Based on the following blog post content, please provide a concise, engaging summary of 2-3 sentences that captures the main points.

        Blog Post Content:
        "{plain_text_content}"

        Summary:
        """

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama3-8b-8192", # Using a fast and capable model
        )

        summary = chat_completion.choices[0].message.content
        return summary.strip()

    except Exception as e:
        print(f"Error generating summary: {e}")
        return None