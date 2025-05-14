from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, FormMixin
from .models import Thread, ThreadCategory, Comment
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from .forms import CommentForm
from .models import Profile


class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/thread_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = ThreadCategory.objects.all()
        related_categories = categories.prefetch_related('thread_set')
        context['grouped_threads'] = related_categories

        if self.request.user.is_authenticated:
            made_threads = self.request.user.profile.threads.all()
            context['made_threads'] = made_threads
        return context


class ThreadDetailView(FormMixin, DetailView):
    model = Thread
    template_name = 'forum/thread_detail.html'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('forum:thread-detail',
                            kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        thread = self.object
        thread_category = thread.category
        related_threads = Thread.objects.filter(
            category=thread_category).exclude(id=thread.id).order_by('?')[:4]
        context['related_threads'] = related_threads
        context['comments'] = Comment.objects.filter(
            thread=self.object).order_by('created_on')
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        thread = self.get_object()
        profile = get_object_or_404(Profile, user=request.user)
        comment_id = request.POST.get('comment_id')

        if comment_id:
            comment = get_object_or_404(
                Comment,
                id=comment_id,
                thread=thread
            )

            if comment.author == profile:
                comment.entry = request.POST.get('entry', comment.entry)
                comment.save()

            return redirect('forum:thread-detail', pk=thread.pk)

        else:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.thread = thread
                comment.author = profile
                comment.save()
                return redirect('forum:thread-detail', pk=thread.pk)

            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)


class ThreadCreateView(LoginRequiredMixin, CreateView):
    model = Thread
    fields = ['title', 'category', 'entry', 'image']
    template_name = 'forum/thread_add.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.profile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            'forum:thread-detail',
            kwargs={'pk': self.object.pk}
        )


class ThreadUpdateView(LoginRequiredMixin, UpdateView):
    model = Thread
    fields = ['title', 'category', 'entry', 'image']
    template_name = 'forum/thread_edit.html'

    def get_success_url(self):
        return reverse_lazy(
            'forum:thread-detail',
            kwargs={'pk': self.object.pk}
        )
