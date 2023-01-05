from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView
)

from users.models import Referral


class ReferralListView(LoginRequiredMixin, ListView):
    model = Referral
    template_name = 'users/referral_list.html'

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        # https://stackoverflow.com/questions/9410647/how-to-filter-model-results-for-multiple-values-for-a-many-to-many-field-in-djan
        # queries = Query.objects.filter(database_id__in=get_org_databases(self)).order_by('-run_count', '-date_created')
        sort_by = self.request.GET.get("sort_by")
        if sort_by == 'visits':
            queries = Referral.objects.filter() \
                .order_by('-visit_count', '-pk')
        else:
            queries = Referral.objects.filter() \
                .order_by('-pk')
        return queries


class ReferralAbstract(LoginRequiredMixin):
    model = Referral
    fields = ['title', 'site', 'ref_code', 'url', 'description']

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('referral-list')


class ReferralCreateView(ReferralAbstract, CreateView):
    """subclass"""


class ReferralEditView(ReferralAbstract, UpdateView):
    """subclass"""
