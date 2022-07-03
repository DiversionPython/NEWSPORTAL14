from django import forms
from .models import Post, User



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'postCategory',
            'title',
            'text'
        ]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]


