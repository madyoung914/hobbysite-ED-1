from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Thread, ThreadCategory


class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/thread_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = ThreadCategory.objects.all().prefetch_related('thread_set')
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
