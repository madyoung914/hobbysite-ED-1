from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Thread


class ThreadListView(ListView):
    model = Thread
    template_name = 'forum/post_list.html'


class ThreadDetailView(DetailView):
    model = Thread
    template_name = 'forum/post_detail.html'


class ThreadCreateView(DetailView):
    model = Thread
    template_name = 'forum/thread_add.html'


class ThreadUpdateView(DetailView):
    model = Thread
    template_name = 'forum/thread_edit.html'
