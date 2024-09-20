from django.contrib import admin
from .models import Category, Tag, Post, Comment, Profile

# Admin configuration for Category model
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # Show category name and slug in the list
    prepopulated_fields = {'slug': ('name',)}  # Auto-populate slug based on name
    search_fields = ['name']  # Add search functionality for categories

# Admin configuration for Tag model
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')  # Show tag name and slug in the list
    prepopulated_fields = {'slug': ('name',)}  # Auto-populate slug based on name
    search_fields = ['name']  # Add search functionality for tags

# Admin configuration for Comment model
class CommentInline(admin.TabularInline):  # Inline model to show comments in the post admin
    model = Comment
    extra = 0  # No extra blank comments
    fields = ['author', 'content', 'created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

# Admin configuration for Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'total_likes')  # Show post info and likes
    list_filter = ('author', 'categories', 'tags', 'created_at')  # Filter by author, categories, tags, and date
    search_fields = ['title', 'content', 'author__username']  # Add search functionality for posts
    prepopulated_fields = {'slug': ('title',)}  # Auto-populate slug based on title
    inlines = [CommentInline]  # Show comments in the post admin
    readonly_fields = ['created_at', 'updated_at']  # Read-only fields
    filter_horizontal = ('categories', 'tags', 'likes')  # Horizontal filter for M2M fields

    # Custom method to show total likes in the list view
    def total_likes(self, obj):
        return obj.likes.count()
    total_likes.short_description = 'Total Likes'

# Admin configuration for Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'created_at', 'updated_at')  # Show comment info
    list_filter = ('author', 'post', 'created_at')  # Filter by author, post, and date
    search_fields = ['content', 'author__username', 'post__title']  # Add search functionality for comments
    readonly_fields = ['created_at', 'updated_at']  # Read-only fields

# Admin configuration for Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'website')  # Show user and website
    search_fields = ['user__username', 'bio']  # Add search functionality for profiles
    readonly_fields = ['user']  # Read-only user field
