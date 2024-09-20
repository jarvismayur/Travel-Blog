from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Post, Comment, Profile, Category, Tag
from django.contrib.auth.models import User
from .forms import PostForm, CommentForm, ProfileForm,CustomUserCreationForm

# Display a list of all posts
def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'blog/post_list.html', {'posts': posts})

# View the details of a single post
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all().order_by('created_at')
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.save()
            return HttpResponseRedirect(reverse('post_detail', args=[slug]))
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'comment_form': comment_form,
    }
    return render(request, 'blog/post_detail.html', context)

# Like a post
@login_required
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_detail', args=[slug]))

# Display user profile
@login_required
def user_profile(request, username):
    profile = None
    try:
        # Try to get the profile by username
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        # If profile not found, display the logged-in user's profile
        user = get_object_or_404(User, username=username)
        
    return render(request, 'blog/user_profile.html', {'profile': profile, 'user':user})

# Edit user profile
@login_required
def edit_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'blog/edit_profile.html', {'form': form})

# Create or edit a post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save categories and tags
            return redirect('post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})


# Signup view
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #login(request, user)  # Log the user in after signup
            return redirect('post_list')  # Redirect to homepage after signup
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/signup.html', {'form': form})


@login_required
def add_or_edit_profile(request):
    # Check if the user already has a profile
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        # If profile exists, bind form to existing instance; else create new
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user  # Assign the logged-in user
            profile.save()
            return redirect('user_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)  # Prepopulate form if profile exists

    return render(request, 'blog/edit_profile.html', {'form': form})


