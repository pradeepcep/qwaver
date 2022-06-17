from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView, DeleteView
)

from queries.models import Database
from queries.views.access import get_org_databases


class DatabaseListView(ListView):
    model = Database
    template_name = 'queries/database_list.html'
    context_object_name = 'databases'

    def get_queryset(self):
        # https://stackoverflow.com/questions/9410647/how-to-filter-model-results-for-multiple-values-for-a-many-to-many-field-in-djan
        queries = Database.objects.filter(pk__in=get_org_databases(self))
        return queries


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

    def test_func(self):
        user_can_access_database(self.request.user, self.get_object())
        return True
