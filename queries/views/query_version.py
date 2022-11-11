import difflib

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
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
                line['diff'] = "original"
            else:
                before = versions[index - 1].query_text
                after = versions[index].query_text
                diff = ""
                for i, s in enumerate(difflib.ndiff(before, after)):
                    if s[0] == ' ':
                        continue
                    elif s[0] == '-':
                        diff = diff + f"<span style='color: red'>{s[-1]}</span>"
                    elif s[0] == '+':
                        diff = diff + f"<span style='color: green'>{s[-1]}</span>"
                line['diff'] = diff
            queryset.append(line)
        return queryset

    # printing difference: https://stackoverflow.com/questions/17904097/python-difference-between-two-strings
    def get_context_data(self, **kwargs):
        context = super(QueryVersionListView, self).get_context_data(**kwargs)  # get the default context data
        # TODO: get this from queryversion so we don't double-query database for user
        context['query'] = get_object_or_404(Query, id=self.kwargs.get('query_id'))
        context['result_count'] = len(self.object_list)
        return context
