from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView, DeleteView
)

from queries.common.access import user_can_access_org
from queries.models import Organization
from users.models import UserOrganization


class OrganizationListView(ListView):
    model = Organization
    template_name = 'queries/organization_list.html'
    context_object_name = 'orgs'

    def get_queryset(self):
        # TODO: is there a better way to do this with only one query instead of two?
        user_orgs = UserOrganization.objects.filter(user=self.request.user).values_list('organization', flat=True)
        orgs = Organization.objects.filter(pk__in=user_orgs)
        return orgs


class OrganizationCreateView(LoginRequiredMixin, CreateView):
    model = Organization
    fields = ['name']

    def get_success_url(self):
        # TODO: add UserOrganizatioin for user creating this org
        return reverse('organization-list')


class OrganizationEditView(LoginRequiredMixin, UpdateView):
    model = Organization
    fields = ['name']


class OrganizationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Organization

    def get_success_url(self):
        return reverse('organization-list')

    def test_func(self):
        user_can_access_org(self.request.user, self.get_object())
        return True
