# blog_app/forms.py
from django import forms
from .models import Post, Comment, Category

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class PostForm(forms.ModelForm):
    extra_images = forms.FileField(widget=MultipleFileInput(attrs={'multiple': True, 'class': 'form-control'}), required=False, label="Additional Images")

    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'video', 'tagged_users']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tagged_users': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Add a comment...'}),
        }