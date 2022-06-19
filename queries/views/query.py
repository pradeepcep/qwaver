import re

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

from queries.models import Query, Parameter, Database
from queries.views import get_org_databases, user_can_access_query
from queries.views.access import user_can_access_database

pagination_count = 10


class QueryListView(LoginRequiredMixin, ListView):
    model = Query
    template_name = 'queries/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'queries'
    ordering = ['-date_created']
    paginate_by = pagination_count

    def get_queryset(self):
        # https://stackoverflow.com/questions/9410647/how-to-filter-model-results-for-multiple-values-for-a-many-to-many-field-in-djan
        queries = Query.objects.filter(database_id__in=get_org_databases(self)).order_by('-date_created')
        return queries

    def get_context_data(self, **kwargs):
        context = super(QueryListView, self).get_context_data(**kwargs)  # get the default context data
        context['result_count'] = len(self.object_list)
        return context


class QuerySearchView(LoginRequiredMixin, ListView):
    model = Query
    template_name = 'queries/home.html'
    context_object_name = 'queries'
    paginate_by = pagination_count

    def get_queryset(self):
        s = self.request.GET.get('s')
        databases = get_org_databases(self)
        if s is not None and len(s) > 0:
            words = s.split()
            # https://stackoverflow.com/questions/20222457/django-building-a-queryset-with-q-objects
            # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#q-objects
            q = Q(database_id__in=databases)
            for word in words:
                q &= Q(title__contains=word) | Q(description__contains=word)
            queries = Query.objects.filter(q).order_by('-date_created')
            return queries
        else:
            return Query.objects.filter(database_id__in=databases).order_by('-date_created')

    def get_context_data(self, **kwargs):
        context = super(QuerySearchView, self).get_context_data(**kwargs)  # get the default context data
        # TODO: is there a way to not have to call get_queryset again?
        context['result_count'] = len(self.get_queryset())
        return context


class UserQueryListView(LoginRequiredMixin, ListView):
    model = Query
    template_name = 'queries/user_queries.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'queries'
    paginate_by = pagination_count

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        databases = get_org_databases(self)
        q = Q(database_id__in=databases)
        q &= Q(author=user)
        return Query.objects.filter(q).order_by('-date_created')


class QueryDetailView(LoginRequiredMixin, DetailView):
    model = Query

    def get_object(self, queryset=None):
        user = self.request.user
        query = get_object_or_404(Query, id=self.kwargs.get('pk'))
        user_can_access_query(user, query)
        return query

    def get_context_data(self, **kwargs):
        context = super(QueryDetailView, self).get_context_data(**kwargs)  # get the default context data
        context['params'] = Parameter.objects.filter(query=self.object)
        return context


class QueryCreateView(LoginRequiredMixin, CreateView):
    model = Query
    fields = ['title', 'database', 'description', 'query']

    # https://stackoverflow.com/questions/47363190/from-the-view-how-do-i-pass-custom-choices-into-a-forms-choicefield
    # https://stackoverflow.com/questions/5666505/how-to-subclass-djangos-generic-createview-with-initial-data
    def get_form(self, *args, **kwargs):
        user = self.request.user
        form = super().get_form(*args, **kwargs)
        form.fields['database'].queryset = get_org_databases(self)
        most_recent_database = user.profile.most_recent_database
        if most_recent_database is not None:
            form.fields['database'].initial = most_recent_database
        return form

    def form_valid(self, form):
        user = self.request.user
        database = get_object_or_404(Database, pk=form.instance.database.id)
        user_can_access_database(user, database)
        form.instance.author = user
        # updating user's profile so their default database is the one just used
        self.request.user.profile.most_recent_database = form.instance.database
        self.request.user.profile.save()
        # creating any parameters
        param_strings = set(re.findall(r'\\{(.*?)\\}', form.instance.query))
        for param_string in param_strings:
            new_parameter = Parameter(
                user=user,
                query=form.instance,
                name=param_string,
                default=""
            )
            new_parameter.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QueryCreateView, self).get_context_data(**kwargs)  # get the default context data
        context['title'] = "Create"
        return context


class QueryEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Query
    fields = ['title', 'database', 'description', 'query', 'active', 'public']

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['database'].queryset = get_org_databases(self)
        return form

    def form_valid(self, form):
        self.request.user.profile.most_recent_database = form.instance.database
        self.request.user.profile.save()
        # creating any parameters
        param_strings = set(re.findall(r'\{(.*?)\}', form.instance.query))
        # retrieve currently created params
        params = Parameter.objects.filter(query=form.instance)
        # delete any params not represented by param_strings
        for param in params:
            if param.name not in param_strings:
                param.delete()
        # creating params not represented in param_strings
        for param_string in param_strings:
            if not any(param.name == param_string for param in params):
                new_parameter = Parameter(
                    user=self.request.user,
                    query=form.instance,
                    name=param_string,
                    default=""
                )
                new_parameter.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QueryEditView, self).get_context_data(**kwargs)  # get the default context data
        context['title'] = "Edit"
        context['params'] = Parameter.objects.filter(query=self.object)
        return context

    def test_func(self):
        user = self.request.user
        query = self.get_object()
        user_can_access_query(user, query)
        return True


class QueryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Query
    success_url = '/'

    def test_func(self):
        user = self.request.user
        query = self.get_object()
        user_can_access_query(user, query)
        if self.request.user == query.author:
            return True
        return False


class QueryCloneView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Query
    fields = ['title', 'database', 'description', 'query']
    template_name = 'queries/query_form.html'

    def get_object(self, queryset=None):
        user = self.request.user
        query = get_object_or_404(Query, id=self.kwargs.get('pk'))
        user_can_access_query(user, query)
        clone = Query.objects.create(
            title=query.title,
            database=query.database,
            description=query.description,
            query=query.query,
            author=user
        )
        clone.save()
        params = Parameter.objects.filter(query=query)
        for param in params:
            param_clone = Parameter.objects.create(
                user=user,
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
        user = self.request.user
        query = self.get_object()
        user_can_access_query(user, query)
        return True
