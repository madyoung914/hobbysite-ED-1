from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'