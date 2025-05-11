from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from .models import Thread, ThreadCategory, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .forms import CommentForm


class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/thread_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ThreadCategory.objects.all().prefetch_related('thread_set')
        context['grouped_threads'] = categories
        return context


class ThreadDetailView(FormMixin, DetailView):
    model = Thread
    template_name = 'forum/thread_detail.html'
    form_class = CommentForm

    
    def get_success_url(self):
        return reverse('forum:thread-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = self.object
        thread_category = thread.category        
        related_threads = Thread.objects.filter(category=thread_category).exclude(id=thread.id).order_by('?')[:4]
        context['related_threads'] = related_threads
        context['comments'] = Comment.objects.filter(thread=self.object).order_by('created_on')
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            comment = form.save(commit=False)
            comment.thread = self.object
            comment.author = request.user.profile
            comment.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)

class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    fields = ['title', 'category', 'entry', 'image']
    template_name = 'forum/thread_add.html'
    success_url = reverse_lazy('forum:threads-list')

    def form_valid(self, form):
        form.instance.author = self.request.user.profile

        # If your model uses User directly
        # form.instance.author = self.request.user

        return super().form_valid(form)    

class ThreadUpdateView(LoginRequiredMixin, UpdateView):
    model = Thread
    fields = ['title', 'category', 'entry', 'image']
    template_name = 'forum/thread_edit.html'
    success_url = reverse_lazy('forum:threads-list')
    