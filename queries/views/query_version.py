import difflib

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from queries.common.access import user_can_access_query
from queries.models import QueryVersion, Query


class QueryVersionListView(LoginRequiredMixin, ListView):
    model = QueryVersion
    template_name = 'queries/query_version_list.html'
    context_object_name = 'versions'

    def get_queryset(self):
        user = self.request.user
        query = get_object_or_404(Query, id=self.kwargs.get('query_id'))
        user_can_access_query(user, query)
        versions = QueryVersion.objects.filter(query=query).order_by('timestamp')
        queryset = []
        for index, version in enumerate(versions):
            line = {'version': version}
            if index == 0:
                line['diff'] = version.query_text
                line['only_diff'] = "original"
            else:
                before = versions[index - 1].query_text
                after = versions[index].query_text
                diff = ""
                only_diff = ""
                for i, s in enumerate(difflib.ndiff(before, after)):
                    if s[0] == ' ':
                        # continue
                        diff += s[-1]
                    elif s[0] == '-':
                        append = f"<span style='color: #FF0099'>{s[-1]}</span>"
                        diff = diff + append
                        only_diff = only_diff + append
                    elif s[0] == '+':
                        append = f"<span style='color: #00FF99'>{s[-1]}</span>"
                        diff = diff + append
                        only_diff = only_diff + append
                line['diff'] = diff
                line['only_diff'] = only_diff
            queryset.append(line)
        queryset.reverse()
        return queryset

    # printing difference: https://stackoverflow.com/questions/17904097/python-difference-between-two-strings
    def get_context_data(self, **kwargs):
        context = super(QueryVersionListView, self).get_context_data(**kwargs)  # get the default context data
        # TODO: get this from queryversion so we don't double-query database for user
        context['query'] = get_object_or_404(Query, id=self.kwargs.get('query_id'))
        context['result_count'] = len(self.object_list)
        return context


class QueryVersionRevertView(QueryVersionListView):

    def get_queryset(self):
        user = self.request.user
        query = get_object_or_404(Query, id=self.kwargs.get('query_id'))
        user_can_access_query(user, query)
        # query_version = get_object_or_404(QueryVersion, query=query, version_number=self.kwargs.get('v'))
        query_version = QueryVersion.objects.filter(query=query, version_number=self.kwargs.get('v')).first()
        if query_version is None:
            raise Http404("Given query version not found....")
        new_version = query.update_query_text(query_version.query_text, user=user)
        if new_version is not None:
            messages.success(self.request, f"Query reverted to version {query_version.version_number}")
        else:
            messages.warning(self.request, f"Current query text not different from selected version. No reversion made.")
        return super().get_queryset()

    def get_success_url(self):
        return reverse('query-versions', args=[self.kwargs.get('pk')])

    def test_func(self):
        return True

