from django import forms
from .models import Post, Comment, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'categories', 'tags', 'image', 'location']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'website']
        widgets = {
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us about yourself', 'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'placeholder': 'Enter your website URL', 'class': 'form-control'}),
        }
        labels = {
            'bio': 'Biography',
            'profile_picture': 'Profile Picture',
            'website': 'Website',
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address', 'class': 'form-control'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'form-control'}),
        }
        labels = {
            'username': 'Username',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email
