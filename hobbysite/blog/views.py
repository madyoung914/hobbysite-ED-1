from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect

from .models import Article, ArticleCategory, Comment, ImageGallery
from user_management.models import Profile

from .forms import ArticleForm, CommentForm, ImageGalleryForm


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ArticleCategory.objects.all
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
            context['user_articles'] = Article.objects.filter(
                author=self.request.user.profile)
            context['other_articles'] = Article.objects.exclude(
                author=self.request.user.profile)
        else:
            context['other_articles'] = Article.objects.all()
        return context


class ArticleDetailView(FormMixin, DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        article = self.get_object()
        profile = get_object_or_404(Profile, user=request.user)
        comment_id = request.POST.get('comment_id')
        if comment_id:
            comment = get_object_or_404(
                Comment,
                id=comment_id,
                article=article
            )
            if comment.author == profile:
                comment.entry = request.POST.get('entry', comment.entry)
                comment.save()
            return redirect('blog:article-detail', pk=article.pk)
        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article
                comment.author = profile
                comment.save()
                return redirect('blog:article-detail', pk=article.pk)
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
    
    def get_success_url(self):
        return reverse_lazy("blog:article-detail", kwargs={"pk": self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_articles'] = Article.objects.filter(
            author=self.object.author
        ).exclude(pk=self.object.pk)[:2]
        context['comments'] = Comment.objects.filter(
            article=self.object
        ).order_by('-created_on')
        if self.request.user.is_authenticated:
            context['profile'] = Profile.objects.get(user=self.request.user)
        context['images'] = ImageGallery.objects.filter(article=self.object)
        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'blog/article_form.html'
    redirect_field_name = 'accounts/login'
    form_class = ArticleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Create a new article'
        return context

    def form_valid(self, form):
        form.instance.author = Profile.objects.get(user=self.request.user)
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    template_name = 'blog/article_form.html'
    redirect_field_name = 'accounts/login'
    form_class = ArticleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        context['form_title'] = 'Update article'
        return context

    def get_success_url(self):
        return reverse_lazy(
            'blog:article-detail',
            kwargs={'pk': self.object.pk}
        )


class ImageGalleryView(LoginRequiredMixin, CreateView):
    model = ImageGallery
    fields = ['image', 'description']
    template_name = 'blog/image_gallery.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Upload Image'
        context['article'] = get_object_or_404(Article, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        form.instance.article = get_object_or_404(
            Article, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:article-detail',
            kwargs={'pk': self.kwargs['pk']}
        )


class ImageGalleryUpdateView(LoginRequiredMixin, UpdateView):
    model = ImageGallery
    form_class = ImageGalleryForm
    template_name = 'blog/image_gallery.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_title'] = 'Update Image'
        image_instance = self.get_object()
        context['article'] = image_instance.article
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'blog:article-detail',
            kwargs={'pk': self.object.article.pk}
        )
