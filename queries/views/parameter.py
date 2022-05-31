from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from queries.models import Parameter, Query


class ParameterCreateView(LoginRequiredMixin, CreateView):
    model = Parameter
    fields = ['name', 'default', 'template']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.query = Query.objects.get(pk=self.kwargs['query_id'])
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ParameterCreateView, self).get_context_data(**kwargs)  # get the default context data
        context['query'] = Query.objects.get(pk=self.kwargs['query_id'])
        return context


class ParameterDetailView(DetailView):
    model = Parameter


class ParameterEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Parameter
    fields = ['name', 'default', 'template']

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ParameterEditView, self).get_context_data(**kwargs)  # get the default context data
        context['title'] = "Update"
        context['query'] = self.object.query
        return context

    def test_func(self):
        return True


class ParameterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Parameter

    def get_success_url(self):
        return reverse('query-detail', args=[self.object.query.id])

    @staticmethod
    def test_func():
        return True
