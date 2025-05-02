from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Article, ArticleCategory
from user_management.models import Profile

from .forms import ArticleForm


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ArticleCategory.objects.all
        context['user'] = Profile.objects.get(user=self.request.user)
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'blog/article_add.html'
    redirect_field_name = 'accounts/login'
    form_class = ArticleForm

    def form_valid(self, form):
        form.instance.author = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)
