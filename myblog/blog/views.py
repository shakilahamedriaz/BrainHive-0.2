from django.shortcuts import render,get_object_or_404, redirect
from .models import Post,Category,Tag,Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import PostForm, CommentForm, UpdateProfileForm
from django.db.models import Q 
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import numpy as np
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from groq import Groq
from dotenv import load_dotenv
import os 
from django.core.mail import send_mail
from .forms import SignupForm #for singup
from django.contrib import messages


# Add this new view function to your blog/views.py file

def home_view(request):
    # Fetch the 3 most recent posts to feature on the homepage
    featured_posts = Post.objects.all().order_by('-created_at')[:3]
    
    # Fetch all categories to display them
    categories = Category.objects.all()
    
    context = {
        'featured_posts': featured_posts,
        'categories': categories,
    }
    return render(request, 'blog/home.html', context)


def post_list(request):
    # category, tag, searching, pagination --> post dekhate hobe
    categoryQ = request.GET.get('category')
    tagQ = request.GET.get('tag')
    searchQ = request.GET.get('q')

    posts = Post.objects.all()

    if categoryQ:
        posts = posts.filter(category__name = categoryQ)
    if tagQ:
        posts = posts.filter(tag__name = tagQ)
    if searchQ:
        posts = posts.filter(
            Q(title__icontains = searchQ)
            | Q(content__icontains = searchQ)
            | Q(tag__name__icontains = searchQ)
            | Q(category__name__icontains = searchQ)
        ).distinct()

    # pagination
    paginator = Paginator(posts, 2) # per page 2 posts
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj" : page_obj,
        "categories" : Category.objects.all(),
        "tags" : Tag.objects.all(),
        'search_query' : searchQ,
        'category_query' : categoryQ,
        'tag_query' : tagQ,

    }
    return render(request, 'blog/post_list.html', context)

def post_details(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False) # database e save hobe na
            comment.post = post 
            comment.author = request.user
            comment.save() # database e save hobe
            return redirect('post_details',id=post.id)
    else:
        comment_form = CommentForm()
    
    comments = post.comment_set.all()
    is_liked = post.liked_users.filter(id=request.user.id).exists()
    like_count = post.liked_users.count()

    context = {
        'post' : post,
        'categories' : Category.objects.all(),
        'tag' : Tag.objects.all(),
        'comments' : comments,
        'comment_form' : comment_form,
        'is_liked' : is_liked,
        'like_count' : like_count
    }
    post.view_count +=1
    post.save()

    return render(request, 'blog/post_details.html', context)


@login_required
def like_post(request, id):
    post = get_object_or_404(Post, id=id)

    if post.liked_users.filter(id=request.user.id):
        post.liked_users.remove(request.user)
    else:
        post.liked_users.add(request.user)

    return redirect('post_details', id=post.id)
    

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()

    return render(request, 'blog/post_create.html', {'form' : form})

@login_required
def post_update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            #return HttpResponse("✅ Post updated successfully!")
            #redirect to the post details page
            return redirect('post_details', id=post.id)

    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_create.html', {'form' : form})

@login_required
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('post_list')


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            #sent confirmation email
            send_mail(
                'Welcome to BrainHive!',
                'Thank you for signing up for BrainHive. We hope you enjoy your experience!',
                'BrainHive Team <riaz35-995@diu.edu.bd>',  # Use the default from email
                [user.email],
                fail_silently=False,
            )
            # Add success message to be shown on login page
            messages.success(request, "✅ Signup successful! A confirmation email has been sent to your email address.")
            return redirect('login')  # This now works correctly


            return redirect('login')

    else:
        form = SignupForm()
    return render(request, 'user/signup.html', {'form' : form})



@login_required
def profile_view(request):
    section  = request.GET.get('section', 'profile')
    context = {'section' : section}

    if section == 'posts':
        posts = Post.objects.filter(author=request.user)
        context['posts'] = posts
    elif section == 'update':
        if request.method == 'POST':
            form = UpdateProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                return redirect('/profile?section=update')
        else:
            form = UpdateProfileForm(instance=request.user)

        context['form'] = form
    return render(request, 'user/profile.html', context)




# --- AI Chatbot Logic ---

# Load environment variables from .env file
load_dotenv()

# Load the chatbot's "brain" once when the server starts. This is much more efficient.
try:
    chatbot_index = faiss.read_index('blog_post_index.faiss')
    with open('blog_post_mapping.pkl', 'rb') as f:
        chatbot_mapping = pickle.load(f)
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    CHATBOT_IS_READY = True
    print("--- Chatbot brain successfully loaded. ---")
except Exception as e:
    CHATBOT_IS_READY = False
    print(f"--- Chatbot brain could not be loaded. Error: {e} ---")
    print("--- Please run 'python manage.py index_posts' to create the index files. ---")


# This is the new view for your chatbot page
def chatbot_view(request):
    answer = None
    question = ""

    if not CHATBOT_IS_READY:
        # Show a helpful message if the index files are missing
        answer = "The chatbot is not ready yet. The administrator needs to build the knowledge index first."
        return render(request, 'blog/chatbot.html', {'answer': answer, 'question': question})

    if request.method == 'POST':
        question = request.POST.get('question', '')

        if question:
            # 1. Convert the user's question into a numerical representation (embedding)
            question_embedding = embedding_model.encode([question])

            # 2. Search the FAISS index to find the 3 most relevant blog posts
            k = 3
            distances, indices = chatbot_index.search(np.array(question_embedding).astype('float32'), k)

            # 3. Get the actual text of those relevant posts to use as "context"
            relevant_texts = [chatbot_mapping['texts'][i] for i in indices[0]]
            context = "\n\n---\n\n".join(relevant_texts)

            # 4. Create a smart prompt for the Groq AI
            prompt = f"""
            You are "Brainy", a helpful AI assistant for the BrainHive.
            Your task is to answer the user's question based on the provided context from the BrainHive.
            You can use outside knowledge if the context match with the BrainHive's Articles.
            If the context does not contain the answer, you must say: "I'm sorry, I couldn't find information about that in the BrainHive! .
            Your Creator is "Shakil Ahamed Riaz"

            CONTEXT FROM BLOG POSTS:
            {context}

            USER'S QUESTION:
            {question}

            YOUR ANSWER:
            """
            
            try:
                # 5. Send the prompt to the Groq API and get the answer
                chat_completion = groq_client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-8b-8192",
                )
                answer = chat_completion.choices[0].message.content
            except Exception as e:
                answer = f"Sorry, there was an error communicating with the AI service. Please try again later. Error: {e}"

    # Render the page with the answer and the original question
    return render(request, 'blog/chatbot.html', {'answer': answer, 'question': question})
