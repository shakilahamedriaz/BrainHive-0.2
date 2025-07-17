from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from .groq_service import get_ai_summary # Import our new function


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 
    

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag)
    view_count = models.PositiveBigIntegerField(default=0)
    liked_users = models.ManyToManyField(User, related_name='liked_posts')

    # Add this new field for the AI summary
    summary = models.TextField(blank=True, null=True, help_text="AI-generated summary.")

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Check if the content has changed or if the summary is empty
        if self.pk: # if the post already exists
            old_post = Post.objects.get(pk=self.pk)
            if old_post.content != self.content or not self.summary:
                # Content changed or summary is missing, generate a new one
                self.summary = get_ai_summary(self.content)
        elif not self.summary: # if it's a new post
             self.summary = get_ai_summary(self.content)

        super().save(*args, **kwargs) # Call the original save method


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post= models.ForeignKey(Post, on_delete=models.CASCADE)
