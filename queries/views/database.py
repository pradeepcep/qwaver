from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView, DeleteView
)

from queries.models import Database


class DatabaseListView(ListView):
    model = Database
    template_name = 'queries/database_list.html'
    context_object_name = 'databases'


class DatabaseCreateView(LoginRequiredMixin, CreateView):
    model = Database
    fields = ['title', 'host', 'port', 'database', 'user', 'password']

    def get_success_url(self):
        return reverse('database-list')


class DatabaseEditView(LoginRequiredMixin, UpdateView):
    model = Database
    fields = ['title', 'host', 'port', 'database', 'user', 'password']


class DatabaseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Database

    def get_success_url(self):
        return reverse('database-list')

    @staticmethod
    def test_func():
        return True
