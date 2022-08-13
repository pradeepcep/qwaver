from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

from queries.models import UserSearch
from queries.views import get_org_databases


class UserSearchListView(LoginRequiredMixin, ListView):
    model = UserSearch
    template_name = 'queries/search_list.html'
    context_object_name = 'searches'

    def get_queryset(self):
        # https://stackoverflow.com/questions/9410647/how-to-filter-model-results-for-multiple-values-for-a-many-to-many-field-in-djan
        searches = UserSearch.objects.filter(organization=self.request.user.profile.selected_organization).order_by('-timestamp')
        return searches
