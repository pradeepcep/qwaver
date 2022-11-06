import datetime
import re

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from queries.common.access import user_can_access_database, get_most_recent_database
from queries.models import Query, Parameter, Database, UserSearch, QueryComment, Result, Value, QueryVersion
from queries.views import get_org_databases, user_can_access_query

pagination_count = 12


# The main view of the app.
# This handles the signup-flow
class QueryListView(ListView):
    model = Query
    template_name = 'queries/query_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'queries'
    ordering = ['-date_created']
    paginate_by = pagination_count

    def get(self, *args, **kwargs):
        # not registered
        if not self.request.user.is_authenticated:
            return render(self.request, 'queries/about.html')
        # no org
        elif self.request.user.profile.selected_organization is None:
            return redirect('organization-create')
        # no database
        elif len(get_org_databases(self)) == 0:
            return redirect('database-create')
        # no query
        elif not Query.objects.filter(database_id__in=get_org_databases(self)).exists():
            return redirect('query-create')
        return super(QueryListView, self).get(*args, **kwargs)

    def get_queryset(self):
        # https://stackoverflow.com/questions/9410647/how-to-filter-model-results-for-multiple-values-for-a-many-to-many-field-in-djan
        # queries = Query.objects.filter(database_id__in=get_org_databases(self)).order_by('-run_count', '-date_created')
        queries = Query.objects.filter(database_id__in=get_org_databases(self))\
            .order_by('-last_run_date', '-date_created')
        return queries

    def get_context_data(self, **kwargs):
        context = super(QueryListView, self).get_context_data(**kwargs)  # get the default context data
        days_ago = timezone.now() - datetime.timedelta(days=2)
        user = self.request.user
        searches = UserSearch.objects\
            .filter(user=user, organization=user.profile.selected_organization, timestamp__gt=days_ago)\
            .values('search')\
            .annotate(dcount=Count('search'))\
            .order_by()[:10]
        context['recent_searches'] = [d['search'] for d in searches]
        context['result_count'] = len(self.object_list)
        # if we're in signup flow
        if not Query.objects.filter(database_id__in=get_org_databases(self)).exists():
            context['is_setup'] = True
        return context


class QuerySearchView(LoginRequiredMixin, ListView):
    model = Query
    template_name = 'queries/query_list.html'
    context_object_name = 'queries'
    paginate_by = pagination_count

    def get_queryset(self):
        s = self.request.GET.get('s')
        databases = get_org_databases(self)
        if s is not None and len(s) > 0:
            # saving query
            user = self.request.user
            org = user.profile.selected_organization
            UserSearch.objects.create(user=user, organization=org, search=s)
            # performing search
            words = s.split()
            # https://stackoverflow.com/questions/20222457/django-building-a-queryset-with-q-objects
            # https://docs.djangoproject.com/en/4.0/ref/models/querysets/#q-objects
            q = Q(database_id__in=databases)
            for word in words:
                q &= Q(title__contains=word) | Q(description__contains=word) | Q(query__contains=word)
            queries = Query.objects.filter(q).order_by('-last_run_date', '-date_created')
            return queries
        else:
            return Query.objects.filter(database_id__in=databases).order_by('-run_count', '-date_created')

    def get_context_data(self, **kwargs):
        context = super(QuerySearchView, self).get_context_data(**kwargs)  # get the default context data
        context['result_count'] = len(self.object_list)
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
        context = super(QueryDetailView, self).get_context_data(**kwargs)
        recent_results = Result.objects.filter(query=self.object, user=self.object.author)\
            .order_by('-last_view_timestamp', '-timestamp')[:10]
        # TODO: use the above but watch out for None/empty list
        most_recent_result = Result.objects.filter(query=self.object, user=self.object.author)\
            .order_by('-timestamp').first()
        params = list(Parameter.objects.filter(query=self.object))
        # pre-populating parameter values
        if most_recent_result is not None:
            values = list(Value.objects.filter(result=most_recent_result))
            for param in params:
                for x in values:
                    if x.parameter_name == param.name:
                        param.default = x.value
        context['params'] = params
        # getting historic results
        results = []
        for result in recent_results:
            line = {'result': result}
            values = list(Value.objects.filter(result=result).order_by('parameter_name'))
            line['values'] = values
            results.append(line)
        context['results'] = results
        # getting comments on queries
        context['comments'] = QueryComment.objects.filter(query=self.object).order_by('-timestamp')
        return context


class QueryCreateView(LoginRequiredMixin, CreateView):
    model = Query
    # fields = ['title', 'database', 'description', 'query']
    fields = ['title', 'database', 'query']

    # https://stackoverflow.com/questions/47363190/from-the-view-how-do-i-pass-custom-choices-into-a-forms-choicefield
    # https://stackoverflow.com/questions/5666505/how-to-subclass-djangos-generic-createview-with-initial-data
    def get_form(self, *args, **kwargs):
        user = self.request.user
        form = super().get_form(*args, **kwargs)
        form.fields['database'].queryset = get_org_databases(self)
        most_recent_database = get_most_recent_database(self)
        if most_recent_database is None:
            databases = get_org_databases(self)
            most_recent_database = databases[0]
        if most_recent_database is not None:
            form.fields['database'].initial = most_recent_database
        return form

    def form_valid(self, form):
        user = self.request.user
        database = get_object_or_404(Database, pk=form.instance.database.id)
        query = form.instance
        user_can_access_database(user, database)
        form.instance.author = user
        response = super().form_valid(form)
        # updating user's profile so their default database is the one just used
        # self.request.user.profile.most_recent_database = form.instance.database
        self.request.user.profile.save()
        # creating any parameters specified by
        # getting all values in the string between two curly braces
        param_strings = set(re.findall(r'\{(.*?)\}', form.instance.query))
        for param_string in param_strings:
            new_parameter = Parameter(
                user=user,
                query=self.object,
                name=param_string,
                default=""
            )
            new_parameter.save()
        # saving this as the first version
        version = QueryVersion(
            query=query,
            version_number=query.version_number,
            query_text=query.query,
            user=user
        )
        version.save()
        return response

    def get_context_data(self, **kwargs):
        context = super(QueryCreateView, self).get_context_data(**kwargs)
        context['title'] = "Create"
        return context


class QueryEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Query
    # fields = ['title', 'database', 'description', 'query']
    fields = ['title', 'database', 'query']

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        user_can_access_query(self.request.user, form.instance)
        form.fields['database'].queryset = get_org_databases(self)
        return form

    def form_valid(self, form):
        user = self.request.user
        query = form.instance
        # getting all parameter strings between curly braces
        param_strings = set(re.findall(r'\{(.*?)\}', form.instance.query))
        # retrieve currently created params
        params = Parameter.objects.filter(query=query)
        # delete any params not represented by param_strings
        for param in params:
            if param.name not in param_strings:
                param.delete()
        # creating params not represented in param_strings
        for param_string in param_strings:
            if not any(param.name == param_string for param in params):
                new_parameter = Parameter(
                    user=self.request.user,
                    query=query,
                    name=param_string,
                    default=""
                )
                new_parameter.save()
        # retrieve latest version, if the SQL is the different, create new version
        latest_version = QueryVersion.objects.filter(query=query, version_number=query.version_number).first()
        # None means this query was made before versioning was a feature
        # so let's create a version
        if latest_version is None:
            latest_version = QueryVersion(
                query=query,
                query_text=self.object.query,
                user=self.object.author
            )
            latest_version.save()

        if 'query' in form.changed_data:
            new_version_number = latest_version.version_number + 1
            form.instance.version_number = new_version_number
            form.save()
            new_version = QueryVersion(
                query=query,
                version_number=new_version_number,
                query_text=query.query,
                user=user,
                comment="",  # TODO: add this field to edit view
            )
            new_version.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QueryEditView, self).get_context_data(**kwargs)  # get the default context data
        context['title'] = "Edit"
        context['params'] = Parameter.objects.filter(query=self.object)
        return context

    def test_func(self):
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

    def form_valid(self, form):
        user_can_access_query(self.request.user, form.instance)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(QueryCloneView, self).get_context_data(**kwargs)  # get the default context data
        context['title'] = "Clone"
        context['is_clone'] = True
        context['params'] = Parameter.objects.filter(query=self.object)
        return context

    def test_func(self):
        return True
