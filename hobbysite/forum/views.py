from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Thread, ThreadCategory
from django.db.models import Prefetch


class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/thread_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            user_profile = self.request.user.profile
            user_threads = Thread.objects.filter(author = user_profile)
            other_threads = Thread.objects.exclude(author = user_profile)
        else:
            user_threads = Thread.objects.none()
            other_threads = Thread.objects.all()         

        categories = ThreadCategory.objects.all().prefetch_related(
            Prefetch('thread_set', queryset = other_threads)
        )

        context['user_threads'] = user_threads
        context['grouped_threads'] = categories
        return context


class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'forum/thread_detail.html'


class ThreadCreateView(DetailView):
    model = Thread
    template_name = 'forum/thread_add.html'


class ThreadUpdateView(DetailView):
    model = Thread
    template_name = 'forum/thread_edit.html'
