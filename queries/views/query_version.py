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
        versions = QueryVersion.objects.filter(query=query).order_by('-timestamp')
        return versions

    def get_context_data(self, **kwargs):
        context = super(QueryVersionListView, self).get_context_data(**kwargs)  # get the default context data
        # TODO: get this from queryversion so we don't double-query database for user
        context['query'] = get_object_or_404(Query, id=self.kwargs.get('query_id'))
        context['result_count'] = len(self.object_list)
        return context
