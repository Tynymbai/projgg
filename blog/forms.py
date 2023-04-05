from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from .models import Comment, Post


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user




class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'content', 'tags')

    def get_success_url(self):
        return reverse_lazy('post-list')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('content', 'image')
