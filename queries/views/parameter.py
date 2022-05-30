from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from queries.models import Parameter


class ParameterCreateView(LoginRequiredMixin, CreateView):
    model = Parameter
    fields = ['name', 'default', 'template']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ParameterDetailView(DetailView):
    model = Parameter


class ParameterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Parameter
    fields = ['title', 'query']

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ParameterUpdateView, self).get_context_data(**kwargs)  # get the default context data
        context['title'] = "Update"
        return context

    def test_func(self):
        return True


class ParameterDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Parameter
    success_url = '/'

    @staticmethod
    def test_func():
        return True
