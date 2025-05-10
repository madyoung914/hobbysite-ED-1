from django.urls import reverse
from django.http import HttpResponseForbidden
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Article, ArticleCategory, Comment
from user_management.models import Profile

from .forms import ArticleForm, ArticleEditForm, CommentForm


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ArticleCategory.objects.all
        if self.request.user.is_authenticated:
            context['account'] = user=self.request.user.profile
        return context


class ArticleDetailView(FormMixin, DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.author = Profile.objects.get(user=self.request.user)
        comment.save()
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse("blog:article-detail", kwargs={"pk": self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(author=self.object.author)
        context['comments'] = Comment.objects.filter(article=self.object).reverse
        if self.request.user.is_authenticated:
            context['user'] = Profile.objects.get(user=self.request.user)
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'blog/article_form.html'
    redirect_field_name = 'accounts/login'
    form_class = ArticleForm

    def form_valid(self, form):
        form.instance.author = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'blog/article_form.html'
    redirect_field_name = 'accounts/login'
    form_class = ArticleEditForm

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['pk'] = self.kwargs['pk']
            return context

    def get_success_url(self):
        return reverse(
            'blog:article-detail',
            kwargs={'pk': self.object.pk}
            )
