from django.db import models
from django.contrib.auth.models import User

# Category model to organize posts into categories
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

# Tag model to add tags to posts
class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

# Post model for blog posts
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Track when post is updated
    categories = models.ManyToManyField(Category, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)  # Location of the travel
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)  # Track likes

    def __str__(self):
        return self.title

    # Custom method to count total likes
    def total_likes(self):
        return self.likes.count()

# Comment model for post comments
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # Track when comment is updated

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'

# Profile model for additional user information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)  # Optional personal website

    def __str__(self):
        return self.user.username
