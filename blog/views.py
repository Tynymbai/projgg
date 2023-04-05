from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Post, Comment
from django.views.generic import DetailView, DeleteView, CreateView, ListView
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import FormView, FormMixin
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from .forms import SignUpForm, PostForm, CommentForm


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-pub_date']

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object)
        if self.request.user.is_authenticated:
            context['form'] = CommentForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            comment.image = form.instance
            return HttpResponseRedirect(reverse('post_detail', args=[str(post.id)]))
        else:
            return render(request, self.template_name, {'form': form})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'blog/login.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

class SignUpView(FormView):
    form_class = SignUpForm
    template_name = 'blog/signup.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)





def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', {'form': form})