from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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
        # adding UserOrganization for user creating this org
        # so that the user hase access to it immediately
        user_org = UserOrganization.objects.create(user=self.request.user, organization=self.object)
        user_org.save()
        return reverse('organization-list')


class OrganizationEditView(LoginRequiredMixin, UpdateView):
    model = Organization
    fields = ['name']

    def get_object(self, queryset=None):
        obj = super().get_object()
        user_can_access_org(self.request.user, obj)
        return obj


class OrganizationDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Organization

    def get_object(self, queryset=None):
        obj = super().get_object()
        user_can_access_org(self.request.user, obj)
        return obj

    def test_func(self):
        return True

    def get_success_url(self):
        org = self.object
        UserOrganization.objects.filter(organization=org).delete()
        return reverse('organization-list')
