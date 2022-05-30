from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView
)

from queries.models import Database


class DatabaseListView(ListView):
    model = Database
    template_name = 'queries/database_list.html'
    context_object_name = 'databases'


class DatabaseCreateView(LoginRequiredMixin, CreateView):
    model = Database
    fields = ['title', 'host', 'port', 'database', 'user', 'password']


class DatabaseUpdateView(LoginRequiredMixin, UpdateView):
    model = Database
    fields = ['title', 'host', 'port', 'database', 'user', 'password']
