import logging

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from queries.models import Query, Parameter

pagination_count = 10


class QueryListView(ListView):
    model = Query
    template_name = 'queries/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'queries'
    ordering = ['-date_created']
    paginate_by = pagination_count


class QuerySearchView(ListView):
    model = Query
    template_name = 'queries/home.html'
    context_object_name = 'queries'
    paginate_by = pagination_count

    def get_queryset(self):
        s = self.request.GET.get('s')
        if len(s) > 0:
            words = s.split()
            # https://stackoverflow.com/questions/20222457/django-building-a-queryset-with-q-objects
            # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#q-objects
            q = Q(title__contains=words[0]) | Q(description__contains=words[0])
            for word in words[1:]:
                q &= Q(title__contains=word) | Q(description__contains=word)
            queries = Query.objects.filter(q).order_by('-date_created')
            return queries
        else:
            return Query.objects.all().order_by('-date_created')


class UserQueryListView(ListView):
    model = Query
    template_name = 'queries/user_queries.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'queries'
    paginate_by = pagination_count

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
    fields = ['title', 'database', 'description', 'query']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QueryCreateView, self).get_context_data(**kwargs)  # get the default context data
        context['title'] = "Create"
        return context


class QueryEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Query
    fields = ['title', 'database', 'description', 'query']

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


class QueryCloneView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Query
    fields = ['title', 'database', 'description', 'query']
    template_name = 'queries/query_form.html'

    def get_object(self, queryset=None):
        query = get_object_or_404(Query, id=self.kwargs.get('pk'))
        clone = Query.objects.create(
            title=query.title,
            database=query.database,
            description=query.description,
            query=query.query,
            author=self.request.user
        )
        clone.save()
        params = Parameter.objects.filter(query=query)
        for param in params:
            param_clone = Parameter.objects.create(
                user=self.request.user,
                query=clone,
                name=param.name,
                default=param.default,
                template=param.template
            )
            param_clone.save()
        return clone

    def get_context_data(self, **kwargs):
        context = super(QueryCloneView, self).get_context_data(**kwargs)  # get the default context data
        context['title'] = "Clone"
        context['is_clone'] = True
        context['params'] = Parameter.objects.filter(query=self.object)
        return context

    def test_func(self):
        return True
