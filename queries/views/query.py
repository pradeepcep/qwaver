import datetime
import os
import re

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q, Count
from django.http import HttpResponse
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
from queries.common.common import get_referral
from queries.common.components import users_recent_results
from queries.models import Query, Parameter, Database, UserSearch, QueryComment, Result, Value, QueryVersion
from queries.views import get_org_databases, user_can_access_query
from queries.views.menus import query_ordering_most_run, query_ordering_recently_added, query_ordering_recently_viewed

pagination_count = 12


# The main view of the app.
# This handles the signup-flow
class QueryListView(ListView):
    model = Query
    template_name = 'queries/query_list.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'queries'
    ordering = ['-date_created']
    paginate_by = pagination_count

    def dispatch(self, request, *args, **kwargs):
        # tracking referral visits
        # getting if the ref code was previously set or if defined in URL
        ref_code = self.kwargs.get('ref_code') or request.session.get('ref_code')
        referral = get_referral(ref_code)
        if referral is not None:
            referral.visit_count += 1
            referral.save()
            request.session['ref_code'] = ref_code
        # not registered
        if not request.user.is_authenticated:
            return render(request, 'queries/static/index.html')
        # no org
        elif request.user.profile.selected_organization is None:
            return redirect('organization-create')
        # no database
        elif len(get_org_databases(self)) == 0:
            return redirect('database-create')
        # no query
        elif not Query.objects.filter(database_id__in=get_org_databases(self)).exists():
            return render(request, 'queries/start.html')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # https://stackoverflow.com/questions/9410647/how-to-filter-model-results-for-multiple-values-for-a-many-to-many-field-in-djan
        # queries = Query.objects.filter(database_id__in=get_org_databases(self)).order_by('-run_count', '-date_created')
        queries = Query.objects.filter(database_id__in=get_org_databases(self))
        queries = order_queries(queries, self.request.user)
        return queries

    def get_context_data(self, **kwargs):
        context = super(QueryListView, self).get_context_data(**kwargs)  # get the default context data
        days_ago = timezone.now() - datetime.timedelta(days=2)  # searches back for 2 days
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

    def get(self, *args, **kwargs):
        s = self.request.GET.get('s')
        if s == 'dml':
            return render(self.request, 'queries/easter.html', {})
        if s == 'synthblast':
            return redirect("https://synthblast.com")
        return super(QuerySearchView, self).get(*args, **kwargs)

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
            queries = Query.objects.filter(q)
            queries = order_queries(queries, self.request.user)
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
        most_recent_result = Result.objects.filter(query=self.object, user=self.request.user)\
            .order_by('-timestamp').first()
        params = list(Parameter.objects.filter(query=self.object))
        # pre-populating parameter values and constructing API URL
        api_params = f"?api_key={self.request.user.profile.api_key}"
        if most_recent_result is not None:
            values = list(Value.objects.filter(result=most_recent_result))
            for param in params:
                for x in values:
                    if x.parameter_name == param.name:
                        param.default = x.value
                        api_params += f"&{param.name}={x.value}"
        else:
            for param in params:
                api_params += f"&{param.name}=[{param.name} value]"
        context['params'] = params
        # historic results
        context['results'] = users_recent_results(query=self.object, user=self.request.user)
        context['comments'] = QueryComment.objects.filter(query=self.object).order_by('-timestamp')
        # constructing API URL


        context['api_url'] = f"http://{self.request.get_host()}/api/{self.object.id}/{api_params}"
        # updating query
        query = self.object
        query.last_viewed = timezone.now()
        query.save()
        return context


class QueryCreateView(LoginRequiredMixin, CreateView):
    model = Query
    # fields = ['title', 'database', 'description', 'query']
    fields = ['title', 'database', 'query']

    # https://stackoverflow.com/questions/47363190/from-the-view-how-do-i-pass-custom-choices-into-a-forms-choicefield
    # https://stackoverflow.com/questions/5666505/how-to-subclass-djangos-generic-createview-with-initial-data
    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        form.fields['database'].queryset = get_org_databases(self)
        form.fields['database'].initial = get_most_recent_database(self)
        return form

    def form_valid(self, form):
        user = self.request.user
        database = get_object_or_404(Database, pk=form.instance.database.id)
        query = form.instance
        query.last_viewed = timezone.now()
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
            version_number=query.get_version_number(),
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
        edited_query = form.instance
        # getting all parameter strings between curly braces
        param_strings = set(re.findall(r'\{(.*?)\}', form.instance.query))
        # retrieve currently created params
        params = Parameter.objects.filter(query=edited_query)
        # delete any params not represented by param_strings
        for param in params:
            if param.name not in param_strings:
                param.delete()
        # creating params not represented in param_strings
        for param_string in param_strings:
            if not any(param.name == param_string for param in params):
                new_parameter = Parameter(
                    user=self.request.user,
                    query=edited_query,
                    name=param_string,
                    default=""
                )
                new_parameter.save()
        # if the SQL is the different, create new version
        original_query = get_object_or_404(Query, id=self.kwargs.get('pk'))
        if original_query.query != edited_query.query:
            # updating the original version as that will have the original query text
            # TODO: make this better.  It's probably calling the DB more than needed
            new_version = original_query.update_query_text(edited_query.query, user=user)
            edited_query.version = new_version
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
    # fields = ['title', 'database', 'description', 'query']
    fields = ['title', 'database', 'query']
    template_name = 'queries/query_form.html'

    def get_object(self, queryset=None):
        user = self.request.user
        query = get_object_or_404(Query, id=self.kwargs.get('pk'))
        user_can_access_query(user, query)
        clone = Query.objects.create(
            title=f"{query.title} COPY",
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


def query_export(request):
    user = request.user
    export_path = 'export/'
    if not os.path.exists(export_path):
        os.makedirs(export_path)
    if user.is_authenticated:
        profile = user.profile
        databases = Database.objects.filter(organization=profile.selected_organization)
        queries = Query.objects.filter(author=user, database_id__in=databases)
        for query in queries:
            if query.latest_result:
                title = str(query.id).zfill(4)
                title += "-"
                query_title = re.sub('[^0-9a-zA-Z]+', '_', query.title.lower())
                # removing any repeated underscores
                pattern = "(?P<char>[" + re.escape("_") + "])(?P=char)+"
                re.sub(pattern, r"\1", query_title)
                title += query_title
                title = title[0:50]
                title += ".sql"
                with open(f"{export_path}{title}", 'w') as f:
                    f.write(f"-- title:    {query.title}\n")
                    f.write(f"-- version:  {query.get_version_number()}\n")
                    f.write("\n")
                    f.write(query.query)
        return redirect(reverse('queries-home'))


def order_queries(queries, user):
    ordering = user.profile.query_ordering
    if ordering == query_ordering_most_run[0]:
        queries = queries.order_by('-run_count', '-last_run_date')
    elif ordering == query_ordering_recently_added[0]:
        queries = queries.order_by('-date_created')
    elif ordering == query_ordering_recently_viewed[0]:
        queries = queries.order_by('-last_viewed', )
    else:
        # default: query_ordering_recently_run
        queries = queries.order_by('-last_run_date')
    return queries