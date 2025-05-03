from django.shortcuts import get_object_or_404, redirect
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.urls import reverse, reverse_lazy

from .models import Article, Profile, Comment
from .forms import CommentForm, ArticleForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ArticleListView(ListView):
    model = Article
    template_name = 'wiki/article_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            profile = get_object_or_404(Profile, user=user)
            user_articles = Article.objects.filter(author=profile)
            other_articles = Article.objects.exclude(author=profile)
        else:
            user_articles = Article.objects.none()
            other_articles = Article.objects.all()

        articles_by_category = {}
        for article in other_articles:
            category = article.category #gets the category
            if category not in articles_by_category: #checks if category was already stated
                articles_by_category[category] = [] #creates new list for a new category if category was not already stated
            articles_by_category[category].append(article)

        context['user_articles'] = user_articles
        context['articles_by_category'] = articles_by_category
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'wiki/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()

        related_articles = Article.objects.filter(
            category=article.category
        ).exclude(pk=article.pk)[:2]  # gets the first 2 results

        comments = Comment.objects.filter(article=article).order_by('-created_on')

        # provides comments only if user is authenticated
        if self.request.user.is_authenticated:
            context['form'] = CommentForm()

        context['related_articles'] = related_articles
        context['comments'] = comments

        return context

    def post(self, request, *args, **kwargs):
        article = self.get_object()  
        profile = get_object_or_404(Profile, user=request.user) 
        form = CommentForm(request.POST)

        if form.is_valid():  
            comment = form.save(commit=False)  # doesnt save yet
            comment.article = article  
            comment.author = profile  
            comment.save()  
            
            return self.get(request, *args, **kwargs) 

        else:  
            context = self.get_context_data(comment_form=form) 
            return self.render_to_response(context) 


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'wiki/article_form.html'
    fields = ['title', 'entry', 'category', 'header_image']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create a new article'
        return context
    
    def form_valid(self, form):
        profile = get_object_or_404(Profile, user=self.request.user) 
        form.instance.author = profile
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('wiki:article-detail', kwargs={'pk': self.object.pk})


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'wiki/article_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update article'
        return context

    def get_success_url(self):
        return reverse_lazy('wiki:article-detail', kwargs={'pk': self.object.pk})
