import logging

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from queries.models import Query, Parameter


class QueryListView(ListView):
    model = Query
    template_name = 'queries/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'queries'
    ordering = ['-date_created']
    paginate_by = 5


class UserQueryListView(ListView):
    logging.debug("UserQueryListView Log message")
    model = Query
    template_name = 'queries/user_queries.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'queries'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Query.objects.filter(author=user).order_by('-date_created')


class QueryDetailView(DetailView):
    model = Query

    def get_context_data(self, **kwargs):
        context = super(QueryDetailView, self).get_context_data(**kwargs)  # get the default context data
        context['params'] = Parameter.objects.filter(query=self.object)
        return context


class QueryCreateView(LoginRequiredMixin, CreateView):
    model = Query
    fields = ['title', 'database', 'query']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    # def get_context_data(self, **kwargs):
    #     context = super(QueryCreateView, self).get_context_data(**kwargs)  # get the default context data
    #     context['title'] = "Create"
    #     return context


class QueryEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Query
    fields = ['title', 'query']

    # def form_valid(self, form):
    #     form.instance.author = self.request.user
    #     return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QueryEditView, self).get_context_data(**kwargs)  # get the default context data
        context['title'] = "Edit"
        context['params'] = Parameter.objects.filter(query=self.object)
        return context

    def test_func(self):
        # query = self.get_object()
        # if self.request.user == query.author:
        #     return True
        # return False
        return True


class QueryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Query
    success_url = '/'

    def test_func(self):
        query = self.get_object()
        if self.request.user == query.author:
            return True
        return False

